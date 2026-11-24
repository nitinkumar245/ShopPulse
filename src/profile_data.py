import pandas as pd

from extract import extract_all

def inspect_df(name,df):
    print("\n"+ "=" * 55)
    print(f"DATASET:{name.upper()}")
    print("=" * 55)

    print("\nShape:")
    print(df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nDataFrame Information:")
    df.info()

    print("\nMissing Values:")
    print(df.isna().sum())


    print("\nDuplicated rows:")

    if name == "products":
      print(df.drop(columns=["tags"]).duplicated().sum())
    else:
     print(df.duplicated().sum())

    print("\nStastical summary:")
    print(df.describe())

    print("\nMemory Usage:")
    print(df.memory_usage(deep=True).sum(),"bytes")



def check_customers(customers):

    print("\n=========== CUSTOMERS QUALITY =============")

    duplicate_ids=customers.loc[
        customers["customer_id"].duplicated(keep=False)
    ]

    print("\nDuplicate Customer Ids:")
    print(duplicate_ids)

    print("\nMissing Customer Segment:")
    print(
        customers.loc[
            customers["segment"].isna()
        ]
    )

    signup_dates = pd.to_datetime(
        customers["signup_date"],
        errors="coerce"
    )

    invalid_dates = (
        customers["signup_date"].notna() &
        signup_dates.isna()
    )

    print("\nInvalid Signup Dates:")
    print(customers.loc[invalid_dates])



def check_orders(orders,customers):
    print("\n============== ORDERS QUALITY ================")

    duplicate_ids = (
        orders["order_id"].notna() &
        orders["order_id"].duplicated(keep=False)
    )

    print("\nDuplicate Order IDs:")
    print(orders.loc[duplicate_ids])

    print("\nMissing Order IDs:")
    print(orders.loc[orders["order_id"].isna()])


    print("\nMissing Customer IDs:")
    print(orders.loc[orders["customer_id"].isna()])

    parsed_date=pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    invalid_date_mask = (
        orders["order_date"].notna() &
        parsed_date.isna()
    )

    print("\nInvalid Order Dates:")
    print(orders.loc[invalid_date_mask])

    numeric_amounts = pd.to_numeric(
        orders["amount"],
        errors="coerce"
    )

    invalid_amount_mask = (
        orders["amount"].notna() &
        numeric_amounts.isna()
    )

    print("\nInvalid Amounts:")
    print(orders.loc[invalid_amount_mask])

    negative_amount_mask = numeric_amounts < 0

    print("\nNegative Amounts:")
    print(orders.loc[negative_amount_mask])

    valid_statuses = [
        "Delivered",
        "Pending",
        "Cancelled"
    ]

    invalid_status_mask = (
        orders["status"].notna() &
        ~orders["status"].isin(valid_statuses)
    )

    print("\nInvalid Statuses:")
    print(orders.loc[invalid_status_mask])

    unmatched_customers = (
        orders["customer_id"].notna() &
        ~orders["customer_id"].isin(
            customers["customer_id"]
        )
    )

    print("\nUnmatched Customer IDs:")
    print(orders.loc[unmatched_customers])




def check_order_items(order_items,orders,products):
    print("\n================ ORDER ITEMS QUALITY =================")

    unmatched_orders = (
        order_items["order_id"].notna() &
        ~order_items["order_id"].isin(
            orders["order_id"].dropna()
        )
    )

    print("\nUnmatched Order IDs:")
    print(order_items.loc[unmatched_orders])

    unmatched_products = (
        order_items["product_id"].notna() &
        ~order_items["product_id"].isin(
            products["product_id"]
        )
    )

    print("\nUnmatched Product IDs:")
    print(order_items.loc[unmatched_products])


    print("\nMissing Values:")
    print(order_items.isna().sum())

    print("\nDuplicate Rows:")
    print(
        order_items.loc[
            order_items.duplicated(keep=False)
        ]
    )


def check_products(products):
    print("\n============= PRODUCTS QUALITY =============")

    duplicate_ids = products.loc[
        products["product_id"].duplicated(keep=False)
    ]

    print("\nDuplicate Product IDs:")
    print(duplicate_ids)

    print("\nMissing Values:")
    print(products.isna().sum())

    print("\nProduct Categories:")
    print(products["category"].unique())


def check_targets(monthly_targets):
    print("\n============ TARGETS QUALITY ===============")

    print("\nMissing Values:")
    print(monthly_targets.isna().sum())

    print("\nDuplicate Categories:")
    print(
        monthly_targets.loc[
            monthly_targets["category"].duplicated(keep=False)
        ]
    )
    print("\nTarget Statistics:")
    print(monthly_targets.describe())


def main():
    datasets = extract_all()

    customers = datasets["customers"]
    orders = datasets["orders"]
    order_items = datasets["order_items"]
    products = datasets["products"]
    monthly_targets = datasets["monthly_targets"]


    for name,df in datasets.items():
        inspect_df(name,df)

    check_customers(customers)

    check_orders(orders,customers)

    check_order_items(order_items,orders,products)

    check_products(products)

    check_targets(monthly_targets)

    print("\n================= DATA QUALITY INSPECTION COMPLETE =================")


if __name__ == "__main__":
    main()