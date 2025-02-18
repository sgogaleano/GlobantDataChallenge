import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from creatingTables import Department, Job, HiredEmployee  # Import your ORM models

# Define your database URL
DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/globantdb"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

wd = os.getcwd() + "/Data"

def load_csv_to_db():
    session = SessionLocal()
    
    # Load Departments
    file_path = os.path.join(wd, "departments.csv")
    df_dept = pd.read_csv(file_path, header=None, names=["id", "department"])
    try:
        for _, row in df_dept.iterrows():
            if session.query(Department).filter_by(id=row["id"]).first():
                print(f"Skipping duplicate department id: {row['id']}")
                continue
            session.add(Department(id=row["id"], department=row["department"]))
    except KeyError as e:
        print(f"Error processing departments.csv: {e}")
        session.rollback()
        return
    
    # Load Jobs
    file_path = os.path.join(wd, "jobs.csv")
    df_jobs = pd.read_csv(file_path, header=None, names=["id", "job"])
    try:
        for _, row in df_jobs.iterrows():
            if session.query(Job).filter_by(id=row["id"]).first():
                print(f"Skipping duplicate job id: {row['id']}")
                continue
            session.add(Job(id=row["id"], job=row["job"]))
    except KeyError as e:
        print(f"Error processing jobs.csv: {e}")
        session.rollback()
        return
    
    session.commit()    #Send the independent tables departments and jobs
    session = SessionLocal() #Restart the session to avoid conflicts with the previous commit

    # Load Hired Employees
    file_path = os.path.join(wd, "hired_employees.csv")
    df_employees = pd.read_csv(file_path, header=None, names=["id", "name", "datetime", "department_id", "job_id"])
    try:
        for _, row in df_employees.iterrows():
            # Validate and convert datetime
            datetime_str = row["datetime"]
            try:
                datetime_obj = pd.to_datetime(datetime_str)
                if pd.isna(datetime_obj):
                    raise ValueError("NaT (Not a Time)")
            except ValueError:
                print(f"Invalid datetime format: {datetime_str}")
                datetime_obj = None  # Set to None for invalid datetime formats
            
            # Handle NaN values in job_id
            job_id = row["job_id"]
            if pd.isna(job_id):
                print(f"Skipping row with NaN job_id: {row}")
                continue
            
            # Ensure id is an integer
            try:
                employee_id = int(row["id"])
            except ValueError:
                print(f"Invalid id format: {row['id']}")
                continue
            
            # Ensure department_id is an integer
            try:
                department_id = int(row["department_id"])
            except ValueError:
                print(f"Invalid department_id format: {row['department_id']}")
                continue
            
            # Ensure job_id exists in jobs table
            if not session.query(Job).filter_by(id=int(job_id)).first():
                print(f"Skipping row with non-existent job_id: {row['job_id']}")
                continue
            
            session.add(HiredEmployee(
                id=employee_id, 
                name=row["name"],
                datetime=datetime_obj,  # Use the converted datetime object
                department_id=department_id, 
                job_id=int(job_id)  # Ensure job_id is an integer
            ))
            #print("Added employee:", row["id"])
    except KeyError as e:
        print(f"Error processing hired_employees.csv: {e}")
        session.rollback()
        return

    session.commit()
    session.close()

if __name__ == "__main__":
    load_csv_to_db()