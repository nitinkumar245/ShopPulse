
from pathlib import Path
import pandas as pd




PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)



def generate_customers():

    customers = pd.DataFrame({
        "customer_id": [201, 202, 203, 204, 205],

        "customer_name": [
            "Nitin", "Rahul", "Aman", "Priya", "Neha"
        ],

        "city": [
            "Delhi", "Noida", "Delhi", "Gurgaon", "Delhi"
        ],

        "signup_date": [
            "2025-05-01",
            "2025-06-10",
            "2025-07-15",
            "2025-08-20",
            "2025-09-01"
        ],

        "segment": [
            "Regular", "Premium", "Regular", "Premium", None
        ]
    })

    customers.to_csv(
        RAW_DIR / "customers.csv",
        index=False
    )

    return customers



def generate_orders():

    orders = pd.DataFrame({
        "order_id": [
            1001, 1002, 1003, 1004, 1005,
            1006, 1007, 1008, 1009, 1010,
            1011, 1002, None
        ],

        "customer_id": [
            201, 202, 203, 204, 205,
            201, 202, 999, 203, None,
            204, 202, 205
        ],

        "order_date": [
            "2026-01-05",
            "2026-01-12",
            "2026-01-18",
            "invalid",
            "2026-02-05",
            "2026-02-11",
            "2026-02-14",
            "2026-02-20",
            "2026-03-03",
            "2026-03-09",
            "2026-03-14",
            "2026-01-12",
            "2026-03-20"
        ],

        "status": [
            "Delivered",
            "Delivered",
            "Pending",
            "Delivered",
            "Cancelled",
            "Delivered",
            "Delivered",
            "Delivered",
            "Unknown",
            "Pending",
            "Delivered",
            "Delivered",
            "Pending"
        ],

        "amount": [
            "2500", "1800", "3200", "1500",
            "900", "invalid", "-500", "2100",
            "2700", "1200", "2600", "1800", "1400"
        ]
    })

    orders.to_csv(
        RAW_DIR / "orders.csv",
        index=False
    )

    orders.iloc[:6].to_csv(
        RAW_DIR / "orders_part1.csv",
        index=False
    )

    orders.iloc[6:].to_csv(
        RAW_DIR / "orders_part2.csv",
        index=False
    )

    return orders




def generate_order_items():

    order_items = pd.DataFrame({
        "order_id": [
            1001, 1001, 1002, 1003, 1003,
            1004, 1005, 1006, 1007, 1008,
            1009, 1011, 1011, 9999
        ],

        "product_id": [
            301, 302, 303, 301, 302,
            304, 305, 301, 303, 999,
            305, 302, 304, 301
        ],

        "quantity": [
            1, 2, 1, 1, 3, 1, 2,
            2, 1, 1, 3, 2, 1, 1
        ]
    })

    order_items.to_csv(
        RAW_DIR / "order_items.csv",
        index=False
    )

    return order_items




def generate_products():

    products = pd.DataFrame({
        "product_id": [301, 302, 303, 304, 305],

        "product_name": [
            "Keyboard",
            "Mouse",
            "Office Chair",
            "Desk",
            "Notebook"
        ],

        "category": [
            "Electronics",
            "Electronics",
            "Furniture",
            "Furniture",
            "Stationery"
        ],

        "unit_price": [1200, 600, 3500, 7000, 100],

        "tags": [
            ["computer", "accessory"],
            ["computer", "accessory"],
            ["office", "furniture"],
            ["office", "furniture"],
            ["office", "paper"]
        ]
    })

    products.to_json(
        RAW_DIR / "products.json",
        orient="records",
        indent=2
    )

    return products



def generate_monthly_targets():

    monthly_targets = pd.DataFrame({
        "category": [
            "Electronics",
            "Furniture",
            "Stationery"
        ],

        "Jan": [100000, 80000, 50000],

        "Feb": [120000, 90000, 60000],

        "Mar": [150000, 100000, 70000]
    })

    monthly_targets.to_excel(
        RAW_DIR / "monthly_targets.xlsx",
        sheet_name="Targets",
        index=False
    )

    return monthly_targets



def main():

    print("Generating ShopPulse raw datasets...\n")

    datasets = {
        "customers": generate_customers(),
        "orders": generate_orders(),
        "order_items": generate_order_items(),
        "products": generate_products(),
        "monthly_targets": generate_monthly_targets()
    }

    print("\n========== DATA GENERATION SUMMARY ==========\n")

    for name, df in datasets.items():

        print(f"Dataset: {name}")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
        print("-" * 40)

    print("\nAll raw datasets generated successfully!")
    print(f"Output location: {RAW_DIR}")


if __name__ == "__main__":
    main()
