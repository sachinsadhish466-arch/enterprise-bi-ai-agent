import pandas as pd


def main():
    orders = pd.read_csv("data/orders.csv")
    products = pd.read_csv("data/products.csv")

    # Join orders with product information
    order_data = orders.merge(
        products,
        on="product_id",
        how="left"
    )

    # Calculate revenue after discount
    order_data["gross_revenue"] = (
        order_data["unit_price"] *
        order_data["quantity"]
    )

    order_data["discount_amount"] = (
        order_data["gross_revenue"] *
        order_data["discount"]
    )

    order_data["revenue"] = (
        order_data["gross_revenue"] -
        order_data["discount_amount"]
    )

    # Calculate cost
    order_data["total_cost"] = (
        order_data["unit_cost"] *
        order_data["quantity"]
    )

    # Calculate profit
    order_data["profit"] = (
        order_data["revenue"] -
        order_data["total_cost"]
    )

    print("\nOrder Analysis:")
    print(
        order_data[
            [
                "order_id",
                "product_name",
                "quantity",
                "revenue",
                "total_cost",
                "profit"
            ]
        ]
    )

    print("\nTotal Revenue:")
    print(order_data["revenue"].sum())

    print("\nTotal Cost:")
    print(order_data["total_cost"].sum())

    print("\nTotal Profit:")
    print(order_data["profit"].sum())


if __name__ == "__main__":
    main()