from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import SessionLocal, ConflictoMaceda as ConflictoMacedaModel, TierrasTitulomerced as TierrasTitulomercedModel
from schemas import ConflictoMaceda, TierrasTitulomerced
from typing import List  # Importación de List

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/conflicto/", response_model=List[ConflictoMaceda])
def read_conflicto(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(ConflictoMacedaModel).offset(skip).limit(limit).all()
    return [ConflictoMaceda.from_orm(item) for item in items]

@app.get("/tierras/", response_model=List[TierrasTitulomerced])
def read_tierras(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(TierrasTitulomercedModel).offset(skip).limit(limit).all()
    return [TierrasTitulomerced.from_orm(item) for item in items]