from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database

# Create tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

@app.get("/")
def read_root():
    return {"message": "ScholarSense Backend is Live!", "status": "FinOps Guardrails Active"}

from pydantic import BaseModel

# Schema for incoming data (CS50 Web: Data Validation)
class PaperCreate(BaseModel):
    title: str
    abstract: str
    doi: str

@app.post("/papers/")
def create_paper(paper: PaperCreate, db: Session = Depends(database.get_db)):
    db_paper = models.Paper(
        title=paper.title, 
        abstract=paper.abstract, 
        doi=paper.doi
    )
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    return {"message": "Paper Saved Successfully", "data": db_paper}