from pathlib import Path
import pandas as pd
from extract import extract_all
from transform import transform_all

PROJECT_ROOT=Path(__file__).resolve().parents[1]

PROCESSED_DIR=PROJECT_ROOT/"data"/"processed"
REJECTED_DIR=PROJECT_ROOT/"data"/"rejected"

def create_output_directories():
    PROCESSED_DIR.mkdir(parents=True,exist_ok=True)
    REJECTED_DIR.mkdir(parents=True,exist_ok=True)


def save_processed_data(transformed_data):
    print("\nSaving processed data....")

    for name,df in transformed_data.items():
        file_path=PROCESSED_DIR/f"{name}.csv"
        df.to_csv(file_path,index=False)

        print(f"{name}.csv saved | Records: {len(df)}")


def save_rejected_data(rejected_data):
    print("\nSaving rejected data....")

    for name,df in rejected_data.items():
        file_path = REJECTED_DIR/f"{name}_rejected.csv"

        df.to_csv(file_path,index=False)

        print(f"{name}_rejected.csv saved | Records: {len(df)}")


def load_all(transformed_data,rejected_data):
    create_output_directories()

    save_processed_data(transformed_data)

    save_rejected_data(rejected_data)


    print("\nData loading completed successfully")


def main():
    print("Starting ShopPulse ETL loading...")

    datasets = extract_all()

    transformed_data, rejected_data = transform_all(datasets)

    load_all(transformed_data,rejected_data)



if __name__ == "__main__":
    main()
