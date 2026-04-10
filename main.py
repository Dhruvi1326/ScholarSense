import os
import uvicorn
import uuid
import time
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import database
import ai_engine
import document_processor 
import vector_service 

app = FastAPI(title="ScholarSense API")

# --- STEP 2: LAZY INITIALIZATION (FIXES PORT 8080 TIMEOUT) ---
# We move table creation inside a startup event so the server binds to the port FIRST.
@app.on_event("startup")
def configure_db():
    try:
        models.Base.metadata.create_all(bind=database.engine)
        print("✅ Database Tables Verified/Created")
    except Exception as e:
        print(f"⚠️ Database connection delayed: {e}")

@app.get("/")
def home():
    return {"status": "Robust Logic Active", "version": "2.0.Secure"}

@app.get("/papers")
def get_papers(db: Session = Depends(database.get_db)):
    papers = db.query(models.Paper).order_by(models.Paper.id.desc()).all()
    return papers

@app.get("/search")
def search_papers(q: str = Query(...)):
    try:
        query_vector = vector_service.model.encode(q).tolist()
        results = vector_service.client.search(
            collection_name=vector_service.COLLECTION_NAME,
            query_vector=query_vector,
            limit=5
        )
        return [
            {
                "title": r.payload.get("title", "Unknown"),
                "score": r.score,
                "abstract": r.payload.get("abstract", "")[:300] + "...",
                "integrity_score": r.payload.get("integrity_score", 0)
            } for r in results
        ]
    except Exception as e:
        print(f"Search Error: {e}")
        return {"error": str(e)}

@app.post("/audit/")
async def audit_paper(
    file: UploadFile = File(...),
    clinical_mode: bool = Form(False),
    db: Session = Depends(database.get_db)
):
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}" # Safer unique filename
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        text_content = document_processor.extract_text(temp_path)
        
        # --- STEP 3: AI RETRY LOGIC (FIXES 503 ERRORS) ---
        audit_result = None
        for attempt in range(3):
            try:
                audit_result = ai_engine.evaluate_paper_integrity(temp_path, clinical_mode)
                if audit_result: break
            except Exception as ai_e:
                if "503" in str(ai_e) or "demand" in str(ai_e).lower():
                    print(f"🔄 AI Engine busy, retrying in {2**attempt}s...")
                    time.sleep(2**attempt)
                    continue
                raise ai_e

        if not audit_result:
            raise Exception("AI Engine failed to provide a result after multiple attempts.")

        # Save to SQL
        new_paper = models.Paper(
            title=file.filename,
            abstract=text_content[:1000], 
            doi=f"REF-{os.urandom(4).hex()}",
            integrity_score=float(audit_result.get("final_score", 0)),
            verdict=audit_result.get("verdict", "No verdict generated"),
            trust_level=audit_result.get("trust_level", "Unknown"),
            citation_apa=f"AI Audit: {file.filename} - 2026"
        )
        
        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)

        # Save to Vector Store
        try:
            vector_service.add_to_vector_store(
                paper_id=new_paper.id, 
                title=file.filename, 
                abstract=text_content, 
                integrity_score=audit_result.get("final_score", 0)
            )
        except Exception as vec_e:
            print(f"⚠️ Vector Store Sync Warning: {vec_e}")

        return audit_result

    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)