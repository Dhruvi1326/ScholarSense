from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, ai_engine, verifier  
from pydantic import BaseModel

# Initialize database tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

class PaperCreate(BaseModel):
    title: str
    abstract: str
    doi: str

@app.get("/")
def read_root():
    return {
        "message": "ScholarSense Backend is Live!", 
        "status": "AI Engine & Truth Layer Connected"
    }

@app.post("/papers/")
async def create_paper(paper: PaperCreate, db: Session = Depends(database.get_db)):
    """
    Day 3 Workflow: 
    1. Check Local DB -> 2. Verify External DOI -> 3. AI Audit -> 4. Weighted Save
    """
    
    # 1. Local Data Integrity Check
    existing_paper = db.query(models.Paper).filter(models.Paper.doi == paper.doi).first()
    if existing_paper:
        raise HTTPException(status_code=400, detail="Paper with this DOI already exists in our database.")

    # 2. External Truth Layer (Crossref Verification)
    print(f"Verifying DOI: {paper.doi} via Crossref...")
    verification = await verifier.verify_doi_with_crossref(paper.doi)
    
    # 3. AI Brain Audit (Nature Auditor Protocol)
    print(f"Auditing Content: {paper.title}...")
    ai_audit = ai_engine.evaluate_paper_integrity(paper.title, paper.abstract)
    
    # 4. Hybrid Scoring Logic (The Research Guardrail)
    # If the DOI is invalid, penalize the AI score significantly (multiplied by 0.2)
    base_ai_score = ai_audit.get("score", 0)
    final_integrity_score = base_ai_score if verification["is_valid"] else (base_ai_score * 0.2)

    # 5. Create the Record
    db_paper = models.Paper(
        # prefer the official registry title if the DOI is valid
        title=verification.get("official_title", paper.title),
        abstract=paper.abstract,
        doi=paper.doi,
        integrity_score=final_integrity_score,
        # Store the verification status in the citation field for now
        citation_apa=f"Verified: {verification['is_valid']}. Summary: {ai_audit.get('summary')}"
    )
    
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    
    return {
        "message": "Audit Complete",
        "verification_status": "Registry Confirmed" if verification["is_valid"] else "Registry Failure",
        "ai_verdict": ai_audit.get("verdict"),
        "final_score": final_integrity_score,
        "data": db_paper
    }