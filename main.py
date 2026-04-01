from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database, ai_engine  # Added ai_engine import
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
    return {"message": "ScholarSense Backend is Live!", "status": "AI Engine Connected"}

@app.post("/papers/")
def create_paper(paper: PaperCreate, db: Session = Depends(database.get_db)):
    # 1. Check if DOI already exists (Data Integrity check)
    existing_paper = db.query(models.Paper).filter(models.Paper.doi == paper.doi).first()
    if existing_paper:
        raise HTTPException(status_code=400, detail="Paper with this DOI already exists.")

    # 2. Call the AI Brain (The AI Engine)
    print(f"Auditing Paper: {paper.title}...")
    ai_audit = ai_engine.evaluate_paper_integrity(paper.title, paper.abstract)
    
    # 3. Create the Database Record with AI Insights
    db_paper = models.Paper(
        title=paper.title,
        abstract=paper.abstract,
        doi=paper.doi,
        integrity_score=ai_audit.get("score", 0),  # AI Result 1
        citation_apa=ai_audit.get("summary", "N/A") # AI Result 2 (Using summary for now)
    )
    
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    
    return {
        "message": "Paper Audited & Saved",
        "ai_verdict": ai_audit.get("verdict"),
        "data": db_paper
    }