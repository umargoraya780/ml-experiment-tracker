import os
from fastapi import FastAPI, Depends
from sqlalchemy import create_all_tables, create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# 1. Database Configuration [cite: 62-67]
DB_USER = os.getenv("DB_USER", "mluser")
DB_PASS = os.getenv("DB_PASSWORD", "mlpassword")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "mltracker")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 2. Experiment Model Definition [cite: 18-25]
class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String)
    dataset_name = Column(String)
    accuracy = Column(Float)
    loss = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine) # Auto-create table [cite: 59]

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

# 3. API Endpoints [cite: 29-48]
@app.get("/health")
def health_check():
    return {"status": "running"}

@app.post("/experiments")
def create_experiment(exp_data: dict, db: Session = Depends(get_db)):
    new_exp = Experiment(**exp_data)
    db.add(new_exp)
    db.commit()
    return {"message": "Experiment logged"}

@app.get("/experiments")
def get_experiments(model_name: str = None, db: Session = Depends(get_db)):
    query = db.query(Experiment)
    if model_name:
        query = query.filter(Experiment.model_name == model_name)
    return query.all()