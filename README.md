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

3. Place your CSV files in the [Data](http://_vscodecontentref_/0) directory.

4. Run the Python script:
    ```bash
    python3 01_loadToDB.py
    ```

## Requirements

- Python 3
- PostgreSQL
- Required Python packages (listed in `requirements.txt`)