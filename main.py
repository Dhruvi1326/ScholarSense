from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, database

# Create tables automatically
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="ScholarSense API")

@app.get("/")
def read_root():
    return {"message": "ScholarSense Backend is Live!", "status": "FinOps Guardrails Active"}