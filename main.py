import os
import uvicorn
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 1. CLOUD-READY IMPORTS
import models
import database
import ai_engine
import verifier
from vector_service import initialize_vector_db, add_to_vector_store, client, COLLECTION_NAME

# 2. THE MAGIC FIX: Initialize SQL Tables on Startup
# This ensures papers.db is created immediately when Cloud Run wakes up
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
    try:
        # Save temp file for processing
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())

        # 1. Extract Text
        import document_processor
        text_content = document_processor.extract_text(temp_path)
        
        # 2. AI Forensic Audit
        # Using the renamed function we fixed in ai_engine.py
        gemini_file = document_processor.upload_to_gemini(temp_path)
        audit_result = ai_engine.evaluate_paper_integrity(gemini_file, clinical_mode)

        # 3. Save to SQL Database
        new_paper = models.Paper(
            title=file.filename,
            abstract=text_content[:500], # Storing snippet
            integrity_score=audit_result["final_score"],
            verdict=audit_result["verdict"],
            trust_level=audit_result["trust_level"]
        )
        db.add(new_paper)
        db.commit()
        db.refresh(new_paper)

        # 4. Save to Vector Memory (Qdrant)
        add_to_vector_store(text_content, {"paper_id": new_paper.id, "title": file.filename})

        # Cleanup
        os.remove(temp_path)

        return audit_result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)