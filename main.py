import os
import uvicorn
import uuid
import time
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Query
from sqlalchemy.orm import Session

# Initialize FastAPI immediately - THIS MUST BE FAST
app = FastAPI(title="ScholarSense API")

# --- STEP A: INSTANT HEALTH CHECK ---
@app.get("/")
def home():
    return {"status": "ScholarSense API is Live", "version": "4.0.Production"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# --- STEP B: SAFE LAZY IMPORTS ---
def get_audit_logic():
    # We import inside the function so the main process starts instantly
    import models, database, ai_engine, document_processor, vector_service
    return models, database, ai_engine, document_processor, vector_service

# --- STEP C: ROUTES ---

@app.get("/papers")
def get_papers():
    models, database, _, _, _ = get_audit_logic()
    db = next(database.get_db())
    try:
        return db.query(models.Paper).order_by(models.Paper.id.desc()).all()
    finally:
        db.close()

@app.get("/search")
def search_papers(q: str = Query(...)):
    _, _, _, _, vector_service = get_audit_logic()
    try:
        model = vector_service.get_model()
        client = vector_service.get_client()
        query_vector = model.encode(q).tolist()
        results = client.search(
            collection_name=vector_service.COLLECTION_NAME,
            query_vector=query_vector,
            limit=5
        )
        return [{"title": r.payload.get("title"), "score": r.score} for r in results]
    except Exception as e:
        return {"error": str(e)}

@app.post("/audit/")
async def audit_paper(file: UploadFile = File(...), clinical_mode: bool = Form(False)):
    models, database, ai_engine, document_processor, vector_service = get_audit_logic()
    db = next(database.get_db())
    temp_path = f"temp_{uuid.uuid4()}_{file.filename}"
    try:
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        text = document_processor.extract_text(temp_path)
        audit_result = ai_engine.evaluate_paper_integrity(temp_path, clinical_mode)

        new_paper = models.Paper(
            title=file.filename,
            abstract=text[:1000],
            integrity_score=float(audit_result.get("final_score", 0)),
            verdict=audit_result.get("verdict", "Audit Complete")
        )
        db.add(new_paper)
        db.commit()
        
        # Async-style vector sync
        try:
            vector_service.add_to_vector_store(new_paper.id, file.filename, text, new_paper.integrity_score)
        except: pass 

        return audit_result
    finally:
        db.close()
        if os.path.exists(temp_path): os.remove(temp_path)

if __name__ == "__main__":
    # Binding to 0.0.0.0 is the ONLY way Cloud Run works
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)