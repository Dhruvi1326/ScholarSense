import os
import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

# 1. CLOUD-READY IMPORTS (Moved to top for faster execution)
import models
import database
import ai_engine
import verifier
from vector_service import initialize_vector_db, add_to_vector_store, client, COLLECTION_NAME, model

# Initialize SQL Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

# Initialize Vector Memory on Startup
@app.on_event("startup")
async def startup_event():
    initialize_vector_db()

class PaperCreate(BaseModel):
    title: str
    abstract: str
    doi: str

@app.get("/")
def read_root():
    return {"message": "ScholarSense Backend Live", "status": "Robust Logic Active"}

@app.post("/papers/")
async def create_paper(paper: PaperCreate, db: Session = Depends(database.get_db)):
    # 1. Local Duplicate Check
    existing_paper = db.query(models.Paper).filter(models.Paper.doi == paper.doi).first()
    if existing_paper:
        raise HTTPException(status_code=400, detail="Paper already exists in ScholarSense.")

    # 2. External Registry Verification (Crossref)
    verification = await verifier.verify_doi_with_crossref(paper.doi)
    
    # 3. AI Scientific Audit
    ai_audit = ai_engine.evaluate_paper_integrity(paper.title, paper.abstract)
    base_ai_score = ai_audit.get("score", 0)

    # 4. ROBUST SCORING (Fairness Logic)
    if not verification["is_valid"] and base_ai_score > 80:
        final_integrity_score = base_ai_score - 5 
        registry_note = "Registry Pending / Content High"
    elif not verification["is_valid"]:
        final_integrity_score = base_ai_score * 0.8 
        registry_note = "Unverified Source"
    else:
        final_integrity_score = base_ai_score
        registry_note = "Registry Confirmed"

    # 5. Trust Labeling
    if final_integrity_score > 85:
        trust_label = "Gold Standard / Peer-Verified"
    elif final_integrity_score > 65:
        trust_label = "Credible / Methodological Review Suggested"
    else:
        trust_label = "High Risk / Poor Documentation"

    # 6. Save to SQL Database
    db_paper = models.Paper(
        title=verification.get("official_title", paper.title),
        abstract=paper.abstract,
        doi=paper.doi,
        integrity_score=final_integrity_score,
        citation_apa=f"[{trust_label}] {ai_audit.get('summary')}"
    )
    
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)

    # 7. Index in Semantic Memory (Qdrant)
    add_to_vector_store(
        paper_id=db_paper.id,
        title=db_paper.title,
        abstract=db_paper.abstract,
        integrity_score=final_integrity_score
    )

    return {
        "audit_report": {
            "verdict": ai_audit.get("verdict"),
            "trust_level": trust_label,
            "final_score": final_integrity_score,
            "registry": registry_note,
            "red_flags": ai_audit.get("red_flags", [])
        },
        "data": db_paper
    }

@app.get("/search/")
async def semantic_search(query: str, limit: int = 3):
    """
    Searches by MEANING using Vector Math.
    """
    try:
        # 1. Convert question to vector (Global 'model' used here)
        query_vector = model.encode(query).tolist()
        
        # 2. Search Qdrant
        try:
            results = client.search(
                collection_name=COLLECTION_NAME,
                query_vector=query_vector,
                limit=limit
            )
        except AttributeError:
            # Fallback for different library versions
            from qdrant_client.models import SearchRequest
            results = client.query_points(
                collection_name=COLLECTION_NAME,
                query=query_vector,
                limit=limit
            ).points
        
        # 3. Format output
        return [
            {
                "title": res.payload.get("title", "Unknown Title"),
                "score": res.payload.get("integrity_score", 0),
                "relevance": f"{round(res.score * 100, 2)}%" if hasattr(res, 'score') else "N/A"
            } for res in results
        ]
    except Exception as e:
        print(f"❌ Search Error Detail: {e}")
        return {"error": f"Search failed: {str(e)}"}

# 2. DYNAMIC PORT HANDLING (Critical for Cloud Run)
if __name__ == "__main__":
    # Cloud Run provides a $PORT env variable. Default to 8080.
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)