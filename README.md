
# ShopPulse - E-Commerce ETL Pipeline

ShopPulse is a Python-based ETL (Extract, Transform, Load) project designed to process e-commerce datasets, clean inconsistent data, validate records, and generate data quality reports.

## Features

- Extract data from CSV, JSON, and Excel files.
- Handle missing and invalid values.
- Remove duplicate records.
- Validate customer, order, and product relationships.
- Separate valid and rejected records.
- Save cleaned datasets as CSV files.
- Generate automated data quality reports.
- Run automated pipeline tests.

## Technologies Used

- Python
- Pandas
- NumPy
- OpenPyXL

## Project Structure

ShopPulse/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── reports/
│
├── src/
│   ├── generate_data.py
│   ├── extract.py
│   ├── profile_data.py
│   ├── transform.py
│   ├── load.py
│   ├── report.py
│   ├── test_pipeline.py
│   └── main.py
│
├── requirements.txt
└── README.md

## ETL Workflow

1. Extract: Reads CSV, JSON, and Excel datasets.
2. Transform: Cleans data and validates records.
3. Load: Saves processed and rejected datasets.
4. Report: Generates a data quality report.

## Installation

Clone the repository:

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the project:

cd ShopPulse

Install dependencies:

pip install -r requirements.txt

## Run the Project

Generate sample datasets:

python src/generate_data.py

Run the complete ETL pipeline:

python src/main.py

Run automated tests:

python src/test_pipeline.py

## Output

- Cleaned datasets in data/processed/
- Rejected records in data/rejected/
- Data quality report in reports/

## Author

Nitin Rathore
