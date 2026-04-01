from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    abstract = Column(Text)
    doi = Column(String, unique=True, index=True)
    
    # UVP: unique research validation score
    integrity_score = Column(Float, default=0.0) 
    citation_apa = Column(Text)

 