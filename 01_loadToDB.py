import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def read_and_move_csv_to_db(directory: str, db_url: str, table_prefix: str = "historical_"):
    
    #Reads each CSV file in a directory, 
    #Resets the DataFrame for each file,
    #Inserts the data into a PostgreSQL database.

    #:param directory: Path to the directory containing CSV files.
    #:param db_url: PostgreSQL connection string (e.g., "postgresql://user:password@host:port/database").
    #:param table_prefix: Prefix for table names in the database (default is "historical_").
    
    # Connect to PostgreSQL database
    engine = create_engine(db_url)

    processed_files = []

    for file in os.listdir(directory):
        if file.endswith(".csv"):  # Check if the file is a CSV
            file_path = os.path.join(directory, file)
            
            try:
                # Read CSV into a DataFrame
                df = pd.read_csv(file_path)
                
                # Define table name (based on filename)
                table_name = table_prefix + os.path.splitext(file)[0]  # Prefix + filename without extension
                
                # Insert data into the database
                df.to_sql(table_name, engine, if_exists="replace", index=False)  # Overwrite table if it exists
                
                print(f"Processed and inserted data from: {file} into table: {table_name}")

                processed_files.append(file)  # Store filename
            except (pd.errors.EmptyDataError, SQLAlchemyError) as e:
                print(f"Failed to process file {file}: {e}")

    # Print all processed file names
    print("\nAll processed files:")
    for file in processed_files:
        print(file)

#Go:
wd = os.getcwd() + "/Data"
#database_url = "postgresql://postgres:postgres@localhost:5432/globantdb"
database_url = "postgresql://testuser:testpass@localhost:5432/globantdb"

read_and_move_csv_to_db(wd, database_url)