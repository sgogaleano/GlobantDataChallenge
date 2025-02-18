from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List
import logging
from datetime import datetime
from creatingTables import Department, Job, HiredEmployee  # Import your ORM models

app = FastAPI()
logging.basicConfig(filename="errors.log", level=logging.ERROR)

# Pydantic Models for Validation
class DepartmentCreate(BaseModel):
    id: int
    department: str = Field(..., min_length=1)

class JobCreate(BaseModel):
    id: int
    job: str = Field(..., min_length=1)

class EmployeeCreate(BaseModel):
    id: int
    name: str = Field(..., min_length=1)
    datetime: str
    department_id: int
    job_id: int

class BatchInsert(BaseModel):
    departments: List[DepartmentCreate] = []
    jobs: List[JobCreate] = []
    employees: List[EmployeeCreate] = []

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/batch_insert/")
def batch_insert(data: BatchInsert, db: Session = Depends(get_db)):
    try:
        # Insert Departments
        for dept in data.departments:
            if not db.query(Department).filter(Department.id == dept.id).first():
                db.add(Department(id=dept.id, department=dept.department))
        
        # Insert Jobs
        for job in data.jobs:
            if not db.query(Job).filter(Job.id == job.id).first():
                db.add(Job(id=job.id, job=job.job))
        
        # Insert Employees (validations)
        for emp in data.employees:
            if not db.query(Department).filter(Department.id == emp.department_id).first():
                raise HTTPException(status_code=400, detail=f"Department ID {emp.department_id} does not exist")
            if not db.query(Job).filter(Job.id == emp.job_id).first():
                raise HTTPException(status_code=400, detail=f"Job ID {emp.job_id} does not exist")
            
            new_emp = HiredEmployee(
                id=emp.id, name=emp.name,
                datetime=datetime.fromisoformat(emp.datetime),
                department_id=emp.department_id, job_id=emp.job_id
            )
            db.add(new_emp)
        
        db.commit()
        return {"message": "Batch insertion successful!"}
    except Exception as e:
        logging.error(f"Insertion failed: {str(e)}")
        db.rollback()
        return {"error": "Some transactions failed, check logs."}