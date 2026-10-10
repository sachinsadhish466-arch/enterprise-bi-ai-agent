
from pathlib import Path

import pandas as pd


# Project root: D:\enterprise-bi-ai-agent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"


def load_dataset(filename):
    file_path = DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    return pd.read_csv(file_path)


def validate_dataset(name, df, required_columns):
    print(f"\n{'=' * 50}")
    print(f"DATASET: {name}")
    print("=" * 50)

    print(f"Rows: {len(df)}")
    print(f"Columns: {len(df.columns)}")
    print(f"Column names: {df.columns.tolist()}")

    missing_columns = set(required_columns) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"{name} is missing columns: {missing_columns}"
        )

    missing_values = df.isnull().sum()
    print("\nMissing values:")
    print(missing_values[missing_values > 0]
          if missing_values.any()
          else "No missing values")

    print("\nDuplicate rows:", df.duplicated().sum())


def main():
    customers = load_dataset("customers.csv")
    products = load_dataset("products.csv")
    orders = load_dataset("orders.csv")

    validate_dataset(
        "CUSTOMERS",
        customers,
        [
            "customer_id",
            "customer_name",
            "customer_type",
            "city",
            "region",
            "industry",
        ],
    )

    validate_dataset(
        "PRODUCTS",
        products,
        [
            "product_id",
            "product_name",
            "category",
            "unit_cost",
            "unit_price",
        ],
    )

    validate_dataset(
        "ORDERS",
        orders,
        [
            "order_id",
            "order_date",
            "customer_id",
            "product_id",
            "quantity",
            "discount",
            "region",
        ],
    )

    # Check unique identifiers.
    print("\n" + "=" * 50)
    print("DATA QUALITY CHECKS")
    print("=" * 50)

    print(
        "Duplicate customer IDs:",
        customers["customer_id"].duplicated().sum(),
    )

    print(
        "Duplicate product IDs:",
        products["product_id"].duplicated().sum(),
    )

    print(
        "Duplicate order IDs:",
        orders["order_id"].duplicated().sum(),
    )

    # Check that every order references an existing customer/product.
    unknown_customers = ~orders["customer_id"].isin(
        customers["customer_id"]
    )

    unknown_products = ~orders["product_id"].isin(
        products["product_id"]
    )

    print(
        "Orders with unknown customers:",
        unknown_customers.sum(),
    )

    print(
        "Orders with unknown products:",
        unknown_products.sum(),
    )

    # Check business rules.
    print(
        "Orders with invalid quantities:",
        (orders["quantity"] <= 0).sum(),
    )

    print(
        "Orders with invalid discounts:",
        (~orders["discount"].between(0, 1)).sum(),
    )

    print(
        "Products with invalid prices:",
        (
            (products["unit_cost"] < 0)
            | (products["unit_price"] < 0)
        ).sum(),
    )

    # Preview.
    print("\nFirst five orders:")
    print(orders.head().to_string(index=False))

    print("\nDATA VALIDATION COMPLETED")


if __name__ == "__main__":
    main()
