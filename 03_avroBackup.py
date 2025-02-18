import fastavro
import os
from sqlalchemy import create_engine, text, inspect, Integer, String, Float, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import ProgrammingError
from creatingTables import Department, Job, HiredEmployee, Base

# Establish the database connection
DATABASE_URL = "postgresql://testuser:testpass@localhost:5432/globantdb"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

BACKUP_DIR = "backups"

def get_avro_type(sqlalchemy_type):
    if isinstance(sqlalchemy_type, Integer):
        return "int"
    elif isinstance(sqlalchemy_type, String):
        return "string"
    elif isinstance(sqlalchemy_type, Float):
        return "float"
    elif isinstance(sqlalchemy_type, Boolean):
        return "boolean"
    elif isinstance(sqlalchemy_type, DateTime):
        return "string"
    else:
        return "string"

def convert_none_to_default(row):
    return {key: (value if value is not None else "") for key, value in row.items()}

def backup_table(table_name: str, db: Session):
    try:
        query = db.execute(text(f"SELECT * FROM {table_name}"))
        rows = query.fetchall()
    except ProgrammingError:
        return {"error": f"Table '{table_name}' does not exist."}

    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    schema = {
        "type": "record",
        "name": table_name,
        "fields": [{"name": col["name"], "type": get_avro_type(col["type"])} for col in columns]
    }
    
    os.makedirs(BACKUP_DIR, exist_ok=True)
    file_path = f"{BACKUP_DIR}/{table_name}.avro"

    parsed_schema = fastavro.parse_schema(schema)

    with open(file_path, "wb") as out_file:
        fastavro.writer(out_file, parsed_schema, [convert_none_to_default(dict(row._mapping)) for row in rows])

    return {"message": f"Backup created for {table_name}"}

def backup_all_tables(db: Session):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    results = []
    for table in tables:
        result = backup_table(table, db)
        results.append(result)
    return results

if __name__ == "__main__":
    # Create a new database session
    db = SessionLocal()

    try:
        # Call the backup_all_tables function
        results = backup_all_tables(db)
        for result in results:
            if "error" in result:
                print(result["error"])
            else:
                print(result["message"])
    finally:
        # Close the database session
        db.close()