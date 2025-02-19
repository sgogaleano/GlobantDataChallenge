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

@app.get("/employees_per_quarter/")
def get_hires_per_quarter(db: Session = Depends(get_db)):
    query = text("""
        SELECT d.department, j.job,
               SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime::timestamp) = 1 THEN 1 ELSE 0 END) AS Q1,
               SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime::timestamp) = 2 THEN 1 ELSE 0 END) AS Q2,
               SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime::timestamp) = 3 THEN 1 ELSE 0 END) AS Q3,
               SUM(CASE WHEN EXTRACT(QUARTER FROM he.datetime::timestamp) = 4 THEN 1 ELSE 0 END) AS Q4
        FROM hired_employees he
        JOIN departments d ON he.department_id = d.id
        JOIN jobs j ON he.job_id = j.id
        WHERE he.datetime IS NOT NULL AND he.datetime != '' AND EXTRACT(YEAR FROM he.datetime::timestamp) = 2021
        GROUP BY d.department, j.job
        ORDER BY d.department, j.job;
    """)
    result = db.execute(query).fetchall()
    return [dict(row._mapping) for row in result]