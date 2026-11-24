from pathlib import Path
import pandas as pd

PROJECT_ROOT=Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT/"data"/"raw"

def check_file(file_path):
    if not file_path.exists():
        raise FileNotFoundError(
            f"Source file not found: {file_path}"
        )


def extract_customers():
    file_path = RAW_DIR/"customers.csv"
    check_file(file_path)

    return pd.read_csv(file_path)

def extract_orders():
    file_path = RAW_DIR/"orders.csv"
    check_file(file_path)

    return pd.read_csv(file_path)

def extract_order_items():
    file_path=RAW_DIR/"order_items.csv"
    check_file(file_path)

    return pd.read_csv(file_path)

def extract_products():
    file_path = RAW_DIR/"products.json"
    check_file(file_path)

    return pd.read_json(file_path)

def extract_monthly_targets():
    file_path = RAW_DIR/"monthly_targets.xlsx"
    check_file(file_path)

    return pd.read_excel(file_path,sheet_name="Targets")


def extract_all():
    datasets = {
        "customers":extract_customers(),
        "orders":extract_orders(),
        "order_items":extract_order_items(),
        "products":extract_products(),
        "monthly_targets":extract_monthly_targets()
    }

    return datasets


def extract_orders_in_chunks(chunksize=5):

    file_path = RAW_DIR/"orders.csv"
    check_file(file_path)

    try:

        for chunk in pd.read_csv(
           file_path,
           chunksize=chunksize
        ):
            yield chunk
    except Exception as error:
        raise RuntimeError(
            f"Chunk extraction failed : {error}"
        )from error


if __name__ == "__main__":
    datasets = extract_all()

    print("\n========= EXTRACTION SUMMMARY ============")

    for name,df in datasets.items():
        print(f"Dataset: {name}")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        print("-" * 50)

    print("\n=========CHUNK SUMMARY ==================")

    for number,chunk in enumerate(
        extract_orders_in_chunks(chunksize=5),
        start=1
    ):
        print(f"Chunk {number} : {chunk.shape}")

    print("\nExtraction completed successfully!")

