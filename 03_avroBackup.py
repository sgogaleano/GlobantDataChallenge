import fastavro
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import ProgrammingError
import json

# Establish the database connection
DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/globantdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BACKUP_DIR = "backups"

def get_avro_type(sqlalchemy_type):
    if isinstance(sqlalchemy_type, str):
        return "string"
    elif isinstance(sqlalchemy_type, int):
        return "int"
    elif isinstance(sqlalchemy_type, float):
        return "float"
    elif isinstance(sqlalchemy_type, bool):
        return "boolean"
    else:
        return "string"

def backup_table(table_name: str, db: Session):
    try:
        query = db.execute(text(f"SELECT * FROM {table_name}"))
        rows = query.fetchall()
    except ProgrammingError:
        return {"error": f"Table '{table_name}' does not exist."}

    schema = {
        "type": "record",
        "name": table_name,
        "fields": [{"name": col, "type": get_avro_type(type(rows[0][col]))} for col in query.keys()]
    }
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    file_path = f"{BACKUP_DIR}/{table_name}.avro"

    parsed_schema = fastavro.parse_schema(schema)

    with open(file_path, "wb") as out_file:
        fastavro.writer(out_file, parsed_schema, [dict(row._mapping) for row in rows])

    return {"message": f"Backup created for {table_name}"}

if __name__ == "__main__":
    # Prompt the user for the table name
    table_name = input("Enter the name of the table to create the backup: ")

    # Create a new database session
    db = SessionLocal()

    try:
        # Call the backup_table function
        result = backup_table(table_name, db)
        if "error" in result:
            print(result["error"])
        else:
            print(result["message"])
    finally:
        # Close the database session
        db.close()