import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import sqlalchemy

# 1. CLOUD-READY IMPORTS
import models
import database
import ai_engine
import verifier
import document_processor # Moved to top for cleaner execution
from vector_service import initialize_vector_db, add_to_vector_store, client, COLLECTION_NAME

# --- DATABASE SAFETY NET ---
# If columns are addedto models.py, SQLite sometimes needs a nudge to update.
# create_all will only create tables if they don't exist.
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

@app.get("/")
def home():
    return {"status": "Robust Logic Active", "version": "2.0.Secure"}

@app.post("/audit/")
async def audit_paper(
    file: UploadFile = File(...),
    clinical_mode: bool = Form(False),
    db: Session = Depends(database.get_db)
):
    temp_path = f"temp_{file.filename}"
    try:
        # Save temp file for processing
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # 1. Extract Text
        text_content = document_processor.extract_text(temp_path)
        
        # 2. AI Forensic Audit
        gemini_file = document_processor.upload_to_gemini(temp_path)
        audit_result = ai_engine.evaluate_paper_integrity(gemini_file, clinical_mode)

        # 3. Save to SQL Database (SYCED WITH MODELS.PY)
        # Ensure keys match your models.py columns exactly
        new_paper = models.Paper(
            title=file.filename,
            abstract=text_content[:1000], 
            doi=f"REF-{hash(file.filename)}", # Matches your model's DOI requirement
            integrity_score=float(audit_result.get("final_score", 0)),
            verdict=audit_result.get("verdict", "No verdict generated"),
            trust_level=audit_result.get("trust_level", "Unknown"),
            citation_apa=f"AI Audit: {file.filename} - 2026"
        )
        
        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)

        # 4. Save to Vector Memory (Qdrant)
        try:
            add_to_vector_store(text_content, {"paper_id": new_paper.id, "title": file.filename})
        except Exception as vec_e:
            print(f"Vector Store Warning: {vec_e}") # Don't crash if Qdrant is slow

        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        return audit_result

    except Exception as e:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        # Print error to logs so we can see it in Cloud Run
        print(f"CRITICAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Audit failed: {str(e)}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)