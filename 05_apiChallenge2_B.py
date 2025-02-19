from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from pydantic import BaseModel, Field
from typing import List
import logging
from datetime import datetime
from creatingTables import Department, Job, HiredEmployee, SessionLocal  # Import your ORM models

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/hired_more_than_mean/")
def get_hired_more_than_mean(db: Session = Depends(get_db)):
    query = text("""
        WITH department_hires AS (
            SELECT d.id, d.department, COUNT(he.id) AS hired
            FROM hired_employees he
            JOIN departments d ON he.department_id = d.id
            WHERE he.datetime IS NOT NULL AND he.datetime != '' AND EXTRACT(YEAR FROM he.datetime::timestamp) = 2021
            GROUP BY d.id, d.department
        )
        SELECT * FROM department_hires
        WHERE hired > (SELECT AVG(hired) FROM department_hires)
        ORDER BY hired DESC;
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]