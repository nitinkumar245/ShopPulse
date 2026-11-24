
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REJECTED_DIR = PROJECT_ROOT / "data" / "rejected"
REPORT_DIR = PROJECT_ROOT / "reports"


def test_files_exist():

    required_files = [
        PROCESSED_DIR / "customers.csv",
        PROCESSED_DIR / "orders.csv",
        PROCESSED_DIR / "order_items.csv",
        PROCESSED_DIR / "products.csv",
        PROCESSED_DIR / "monthly_targets.csv",

        REJECTED_DIR / "orders_rejected.csv",
        REJECTED_DIR / "order_items_rejected.csv",
        REJECTED_DIR / "products_rejected.csv",
        REJECTED_DIR / "monthly_targets_rejected.csv",

        REPORT_DIR / "data_quality_report.csv"
    ]

    for file in required_files:
        assert file.exists(), f"Missing file: {file.name}"

    print("PASS: All output files exist!")


def test_orders():

    orders = pd.read_csv(PROCESSED_DIR / "orders.csv")
    customers = pd.read_csv(PROCESSED_DIR / "customers.csv")

    assert orders["order_id"].notna().all()
    assert orders["order_id"].is_unique

    assert orders["customer_id"].isin(
        customers["customer_id"]
    ).all()

    assert (orders["amount"] >= 0).all()

    print("PASS: Orders validation successful!")


def test_order_items():

    items = pd.read_csv(PROCESSED_DIR / "order_items.csv")
    orders = pd.read_csv(PROCESSED_DIR / "orders.csv")
    products = pd.read_csv(PROCESSED_DIR / "products.csv")

    assert items["order_id"].isin(
        orders["order_id"]
    ).all()

    assert items["product_id"].isin(
        products["product_id"]
    ).all()

    assert (items["quantity"] > 0).all()

    print("PASS: Order items validation successful!")


def test_products():

    products = pd.read_csv(PROCESSED_DIR / "products.csv")

    assert products["product_id"].notna().all()
    assert products["product_id"].is_unique
    assert products["product_name"].notna().all()
    assert products["category"].notna().all()
    assert (products["unit_price"] > 0).all()

    print("PASS: Products validation successful!")


def test_targets():

    targets = pd.read_csv(
        PROCESSED_DIR / "monthly_targets.csv"
    )

    assert targets["category"].notna().all()
    assert targets["category"].is_unique

    for month in ["Jan", "Feb", "Mar"]:
        assert targets[month].notna().all()
        assert (targets[month] >= 0).all()

    print("PASS: Monthly targets validation successful!")

def test_record_counts():

    datasets = [
        ("orders", "orders.csv"),
        ("order_items", "order_items.csv"),
        ("products", "products.json"),
        ("monthly_targets", "monthly_targets.xlsx")
    ]

    for name, raw_filename in datasets:

        raw_path = RAW_DIR / raw_filename

        if raw_filename.endswith(".json"):
            raw = pd.read_json(raw_path)

        elif raw_filename.endswith(".xlsx"):
            raw = pd.read_excel(
                raw_path,
                sheet_name="Targets"
            )

        else:
            raw = pd.read_csv(raw_path)

        processed = pd.read_csv(
            PROCESSED_DIR / f"{name}.csv"
        )

        rejected = pd.read_csv(
            REJECTED_DIR / f"{name}_rejected.csv"
        )

        assert len(raw) == len(processed) + len(rejected), (
            f"Record count mismatch in {name}"
        )

    raw_customers = pd.read_csv(RAW_DIR / "customers.csv")

    processed_customers = pd.read_csv(
        PROCESSED_DIR / "customers.csv"
    )

    assert len(raw_customers) == len(processed_customers)

    print("PASS: All record counts match!")



def run_tests():

    print("\n========== SHOPPULSE TESTING ==========\n")

    test_files_exist()
    test_orders()
    test_order_items()
    test_products()
    test_targets()
    test_record_counts()

    print("\n======================================")
    print("ALL TESTS PASSED SUCCESSFULLY!")
    print("======================================")


if __name__ == "__main__":
    run_tests()
