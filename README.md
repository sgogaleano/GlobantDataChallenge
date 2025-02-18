# Globant Test Project

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/sgogaleano/GlobantDataChallenge.git
    cd GlobantDataChallenge
    ```

2. Run the setup script:
    ```bash
    chmod +x 00_setup_environment.sh
    ./00_setup_environment.sh
    ```

3. Place your CSV files in the `Data` directory.

4. Load the CSV data into the database:
    ```bash
    python3 01_loadCSVtoDB.py
    ```

5. Run the FastAPI server:
    ```bash
    uvicorn 02_apiRest:app --reload
    ```

## Requirements

- Python 3
- PostgreSQL
- Required Python packages (listed in `requirements.txt`)

## API Endpoints

### Batch Insert
- **URL:** `/batch_insert/`
- **Method:** `POST`
- **Description:** Batch insert departments, jobs, and employees.
- **Request Body:**
    ```json
    {
        "departments": [
            {"id": 1, "department": "HR"}
        ],
        "jobs": [
            {"id": 1, "job": "Manager"}
        ],
        "employees": [
            {"id": 1, "name": "John Doe", "datetime": "2023-01-01T00:00:00", "department_id": 1, "job_id": 1}
        ]
    }
    ```

## Backup and Restore

### Backup Tables
- **Script:** `03_avroBackup.py`
- **Description:** Backs up all tables to Avro files in the `backups` directory.

### Restore Tables
- **Script:** `04_restoreTableFromBackup.py`
- **Description:** Restores a table from an Avro backup file.