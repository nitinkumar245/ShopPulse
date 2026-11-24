import pandas as pd

from extract import extract_all

def clean_customers(customers):
    customers= customers.copy()

    customers["segment"] = customers["segment"].fillna("Unknown")

    customers["signup_date"]=pd.to_datetime(
        customers["signup_date"],
        errors="coerce"
    )

    return customers


def clean_orders(orders,customers):
    orders = orders.copy()

    orders["order_date"]=pd.to_datetime(
        orders["order_date"],
        errors="coerce"
    )

    orders["amount"]=pd.to_numeric(
        orders["amount"],
        errors="coerce"
    )

    orders["reject_reason"]= ""

    mask = orders["order_id"].isna()
    orders.loc[mask,"reject_reason"] = "Missing Order Id"

    mask=(
        orders["order_id"].notna() &
        orders["order_id"].duplicated(keep="first") &
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"] = "Duplicate Order Id"


    mask = (
        orders["customer_id"].isna()&
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"] = "Missing Customer Id"

    mask=(
        orders["customer_id"].notna() &
        ~orders["customer_id"].isin(customers["customer_id"]) &
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"] = "Unmatched Customer Id"

    mask = (
        orders["order_date"].isna() &
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"] = "Invalid order date"

    mask = (
        orders["amount"].isna() &
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"]="Invalid Amount"

    mask=(
        (orders["amount"]<0)&
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"] = "Negative Amount"

    valid_statuses = ["Delivered","Pending","Cancelled"]
    mask=(
        ~orders["status"].isin(valid_statuses) &
        orders["reject_reason"].eq("")
    )
    orders.loc[mask,"reject_reason"]="Invalid Status"

    valid_orders=orders.loc[
        orders["reject_reason"] == ""
    ].copy()

    rejected_orders = orders.loc[
        orders["reject_reason"] != ""
    ].copy()

    valid_orders=valid_orders.drop(columns=["reject_reason"])

    return valid_orders,rejected_orders



def clean_order_items(order_items,valid_orders,products):
    order_items = order_items.copy()

    order_items["reject_reason"] = ""

    mask=(
        order_items['order_id'].isna() &
        order_items["reject_reason"].eq("")
    )
    order_items.loc[mask,"reject_reason"] = "Missing Order Id"

    mask = (
        order_items['order_id'].notna()&
        ~order_items["order_id"].isin(valid_orders["order_id"])&
        order_items["reject_reason"].eq("")
    )

    order_items.loc[mask,"reject_reason"] = 'Unmatched Order ID'

    mask = (
        order_items["product_id"].isna()&
        order_items["reject_reason"].eq("")
    )
    order_items.loc[mask,"reject_reason"] = "Missing Product Id"

    mask = (
        order_items["product_id"].notna() &
        ~order_items["product_id"].isin(products["product_id"]) &
        order_items["reject_reason"].eq("")
    )

    order_items.loc[mask,"reject_reason"] = "Unmatched Product Id"

    mask = (
        (order_items["quantity"]<=0) &
        order_items["reject_reason"].eq("")
    )
    order_items.loc[mask,"reject_reason"] = "Invalid Quantity"

    valid_items=order_items.loc[
        order_items["reject_reason"]== ""
    ].copy()
    rejected_items = order_items.loc[
        order_items["reject_reason"] != ""
    ].copy()

    valid_items=valid_items.drop(columns=["reject_reason"])

    return valid_items,rejected_items


def clean_products(products):
    products = products.copy()

    products["reject_reason"] = ""

    mask = products["product_id"].isna()

    products.loc[mask,"reject_reason"] = "Missing Product Id"

    mask = (
        products["product_id"].notna() &
        products["product_id"].duplicated(keep='first') &
        products["reject_reason"].eq("")
    )
    products.loc[mask,"reject_reason"] = "Duplicate Product Id"

    mask = (
        products["product_name"].isna()&
        products["reject_reason"].eq("")
    )
    products.loc[mask,"reject_reason"] = "Missing Product Name"

    mask = (
        products["category"].isna() &
        products["reject_reason"].eq("")
    )
    products.loc[mask,"reject_reason"] = "Missing Category"

    products["unit_price"] = pd.to_numeric(
        products["unit_price"],
        errors="coerce"
    )

    mask = (
        (products["unit_price"].isna() |
         (products["unit_price"] <= 0)) &
         products["reject_reason"].eq("")
    )
    products.loc[mask,"reject_reason"] = "Invalid Unit Price"

    valid_products = products.loc[
        products["reject_reason"] == ""
    ].copy()

    rejected_products = products.loc[
        products["reject_reason"] != ""
    ].copy()

    valid_products=valid_products.drop(columns=["reject_reason"])
    return valid_products,rejected_products


def clean_targets(monthly_targets):

    monthly_targets = monthly_targets.copy()

    monthly_targets["reject_reason"] = ""

    # 1. Missing Category
    mask = monthly_targets["category"].isna()
    monthly_targets.loc[mask, "reject_reason"] = "Missing Category"

    # 2. Duplicate Category
    mask = (
        monthly_targets["category"].notna() &
        monthly_targets["category"].duplicated(keep="first") &
        monthly_targets["reject_reason"].eq("")
    )
    monthly_targets.loc[mask, "reject_reason"] = "Duplicate Category"

    month_columns = ["Jan", "Feb", "Mar"]

    for column in month_columns:

        # Convert month values to numeric
        monthly_targets[column] = pd.to_numeric(
            monthly_targets[column],
            errors="coerce"
        )

        # 3. Invalid / Missing Target
        mask = (
            monthly_targets[column].isna() &
            monthly_targets["reject_reason"].eq("")
        )
        monthly_targets.loc[mask, "reject_reason"] = (
            f"Invalid {column} Target"
        )

        # 4. Negative Target
        mask = (
            (monthly_targets[column] < 0) &
            monthly_targets["reject_reason"].eq("")
        )
        monthly_targets.loc[mask, "reject_reason"] = (
            f"Negative {column} Target"
        )

    # Separate valid and rejected records
    valid_targets = monthly_targets.loc[
        monthly_targets["reject_reason"] == ""
    ].copy()

    rejected_targets = monthly_targets.loc[
        monthly_targets["reject_reason"] != ""
    ].copy()

    valid_targets = valid_targets.drop(columns=["reject_reason"])

    return valid_targets, rejected_targets


def transform_all(datasets):

    customers = datasets["customers"]
    orders = datasets["orders"]
    order_items=datasets["order_items"]
    products=datasets["products"]
    monthly_targets=datasets["monthly_targets"]

    cleaned_customers=clean_customers(customers)

    valid_orders,rejected_orders=clean_orders(
        orders,cleaned_customers
    )

    valid_products,rejected_products=clean_products(products)

    valid_items,rejected_items=clean_order_items(order_items,valid_orders,valid_products)

    valid_targets,rejected_targets=clean_targets(monthly_targets)

    transformed_data = {
        "customers":cleaned_customers,
        "orders":valid_orders,
        "order_items":valid_items,
        "products":valid_products,
        "monthly_targets":valid_targets
    }

    rejected_data = {
        "orders":rejected_orders,
        "order_items":rejected_items,
        "products":rejected_products,
        "monthly_targets":rejected_targets
    }

    return transformed_data,rejected_data


def main():
    datasets = extract_all()

    print("\n========= TRANSFORMATION STARTED===========")

    tranformed_data, rejected_data = transform_all(datasets)

    print("\n==========TRANSFORMATION SUMMARY===========")

    print("\nVALID DATASETS")

    for name,df in tranformed_data.items():
        print(f"{name}:{len(df)} records")


    print("\nREJECTED DATASETS")

    for name,df in rejected_data.items():
        print(f"{name}:{len(df)} records")    


    print("\n===============TRANSFORMATION COMPLETED===========") 


if __name__ == "__main__":
    main()
