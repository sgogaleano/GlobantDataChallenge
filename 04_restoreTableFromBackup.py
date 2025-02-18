import fastavro
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from creatingTables import Department, Job, HiredEmployee, Base

# Establish the database connection
DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/globantdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BACKUP_DIR = "backups"

def restore_table(table_name: str, db: Session):
    file_path = f"{BACKUP_DIR}/{table_name}.avro"
    
    if not os.path.exists(file_path):
        return {"error": f"Backup file for table '{table_name}' does not exist."}

    with open(file_path, "rb") as in_file:
        reader = fastavro.reader(in_file)
        rows = [row for row in reader]

    if table_name == "departments":
        for row in rows:
            db.add(Department(id=row["id"], department=row["department"]))
    elif table_name == "jobs":
        for row in rows:
            db.add(Job(id=row["id"], job=row["job"]))
    elif table_name == "hired_employees":
        for row in rows:
            db.add(HiredEmployee(
                id=row["id"], 
                name=row["name"], 
                datetime=row["datetime"], 
                department_id=row["department_id"], 
                job_id=row["job_id"]
            ))
    else:
        return {"error": f"Unknown table '{table_name}'."}

    db.commit()
    return {"message": f"Table '{table_name}' restored successfully."}

if __name__ == "__main__":
    table_name = input("Enter the name of the table to restore: ")
    
    # Create a new database session
    db = SessionLocal()

    try:
        # Call the restore_table function
        result = restore_table(table_name, db)
        if "error" in result:
            print(result["error"])
        else:
            print(result["message"])
    finally:
        # Close the database session
        db.close()