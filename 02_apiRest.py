from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import get_db, insert_data  # A module in the same directory

app = FastAPI()

class Transaction(BaseModel):
    id: int
    amount: float
    timestamp: str

@app.post("/insert")
async def insert_transactions(transactions: List[Transaction], db: Session = Depends(get_db)):
    if not (1 <= len(transactions) <= 1000):
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000")

    insert_data(db, transactions)
    return {"message": "Data inserted successfully"}

print("Finish")