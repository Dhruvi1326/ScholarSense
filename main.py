import os
import uvicorn
import uuid
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models
import database
import ai_engine
import document_processor 
import vector_service # Ensure this is imported for the search endpoint

# Initialize SQL Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

@app.get("/")
def home():
    return {"status": "Robust Logic Active", "version": "2.0.Secure"}

# --- NEW: HISTORY ENDPOINT (Clears the Research Library warning) ---
@app.get("/papers")
def get_papers(db: Session = Depends(database.get_db)):
    """Fetches all previously audited papers from the local SQL database."""
    papers = db.query(models.Paper).order_by(models.Paper.id.desc()).all()
    return papers

# --- NEW: NEURAL SEARCH ENDPOINT (Clears the Neural Discovery warning) ---
@app.get("/search")
def search_papers(q: str = Query(...)):
    """Searches your Qdrant Cloud memory using AI vector embeddings."""
    try:
        # 1. Convert user query to vector
        query_vector = vector_service.model.encode(q).tolist()
        
        # 2. Search Qdrant Cloud
        results = vector_service.client.search(
            collection_name=vector_service.COLLECTION_NAME,
            query_vector=query_vector,
            limit=5
        )
        
        # 3. Format results for the Streamlit UI
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
    temp_path = f"temp_{file.filename}"
    try:
        # Save temp file
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # 1. Extract Text
        text_content = document_processor.extract_text(temp_path)
        
        # 2. AI Forensic Audit (Gemini 2.5 Flash - Stable 2026)
        audit_result = ai_engine.evaluate_paper_integrity(temp_path, clinical_mode)
        print(f"DEBUG AI RESPONSE: {audit_result}")

        # 3. Save to SQL Database
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

        # 4. Save to Vector Memory (Qdrant Cloud)
        try:
            vector_service.add_to_vector_store(
                paper_id=new_paper.id, 
                title=file.filename, 
                abstract=text_content, 
                integrity_score=audit_result.get("final_score", 0)
            )
        except Exception as vec_e:
            print(f"⚠️ Vector Store Sync Warning: {vec_e}")

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return audit_result

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)