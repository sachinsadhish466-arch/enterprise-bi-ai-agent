import pandas as pd


def main():
    file_path = "data/products.csv"

    products = pd.read_csv(file_path)

    print("Products:")
    print(products)

    print("\nDataset shape:")
    print(products.shape)

    print("\nProduct categories:")
    print(products["category"].value_counts())

    products["profit_per_unit"] = (
        products["unit_price"] - products["unit_cost"]
    )

    products["profit_margin"] = (
        products["profit_per_unit"] / products["unit_price"]
    ) * 100

    print("\nProducts with profit:")
    print(
        products[
            [
                "product_name",
                "unit_cost",
                "unit_price",
                "profit_per_unit",
                "profit_margin",
            ]
        ]
    )


if __name__ == "__main__":
    main()