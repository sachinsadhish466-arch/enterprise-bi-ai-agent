from pyspark.sql import functions as F
from pyspark.sql.window import Window

from spark_engine import (
    create_spark_session,
    load_orders,
    load_products,
    load_customers
)


def main():

    spark = create_spark_session()

    print("\n" + "=" * 70)
    print("ENTERPRISE BUSINESS INTELLIGENCE - PYSPARK ANALYTICS")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. LOAD DATA
    # ---------------------------------------------------------

    orders = load_orders(spark)
    products = load_products(spark)
    customers = load_customers(spark)

    print("\nDataset Counts")
    print("-" * 40)

    print("Orders    :", orders.count())
    print("Products  :", products.count())
    print("Customers :", customers.count())

    # ---------------------------------------------------------
    # 2. CREATE SALES DATASET
    # ---------------------------------------------------------

    sales = (
        orders
        .join(
            products,
            on="product_id",
            how="left"
        )
        .join(
            customers.select(
                "customer_id",
                "customer_name",
                "customer_type",
                "industry"
            ),
            on="customer_id",
            how="left"
        )
        .withColumn(
            "gross_revenue",
            F.col("unit_price") * F.col("quantity")
        )
        .withColumn(
            "discount_amount",
            F.col("gross_revenue") * F.col("discount")
        )
        .withColumn(
            "revenue",
            F.col("gross_revenue") - F.col("discount_amount")
        )
        .withColumn(
            "total_cost",
            F.col("unit_cost") * F.col("quantity")
        )
        .withColumn(
            "profit",
            F.col("revenue") - F.col("total_cost")
        )
    )

    # ---------------------------------------------------------
    # 3. TOTAL BUSINESS PERFORMANCE
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("1. TOTAL BUSINESS PERFORMANCE")
    print("=" * 70)

    total_metrics = (
        sales
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit"),
            F.sum("quantity").alias("total_units"),
            F.countDistinct("customer_id").alias("unique_customers"),
            F.countDistinct("order_id").alias("total_orders")
        )
    )

    total_metrics.show(truncate=False)

    # ---------------------------------------------------------
    # 4. REVENUE BY REGION
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("2. REVENUE BY REGION")
    print("=" * 70)

    (
        sales
        .groupBy("region")
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit"),
            F.countDistinct("order_id").alias("orders")
        )
        .orderBy(
            F.col("total_revenue").desc()
        )
        .show(truncate=False)
    )

    # ---------------------------------------------------------
    # 5. REVENUE BY PRODUCT
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("3. TOP 10 PRODUCTS BY REVENUE")
    print("=" * 70)

    (
        sales
        .groupBy(
            "product_id",
            "product_name"
        )
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit"),
            F.sum("quantity").alias("units_sold")
        )
        .orderBy(
            F.col("total_revenue").desc()
        )
        .show(10, truncate=False)
    )

    # ---------------------------------------------------------
    # 6. CUSTOMER ANALYTICS
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("4. TOP 10 CUSTOMERS BY REVENUE")
    print("=" * 70)

    customer_sales = (
        sales
        .groupBy(
            "customer_id",
            "customer_name",
            "customer_type",
            "industry"
        )
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit"),
            F.countDistinct("order_id").alias("order_count")
        )
        .orderBy(
            F.col("total_revenue").desc()
        )
    )

    customer_sales.show(10, truncate=False)

    # ---------------------------------------------------------
    # 7. REVENUE BY INDUSTRY
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("5. REVENUE BY INDUSTRY")
    print("=" * 70)

    (
        sales
        .groupBy("industry")
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit")
        )
        .orderBy(
            F.col("total_revenue").desc()
        )
        .show(truncate=False)
    )

    # ---------------------------------------------------------
    # 8. MONTHLY REVENUE
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("6. MONTHLY REVENUE")
    print("=" * 70)

    monthly_sales = (
        sales
        .withColumn(
            "year_month",
            F.date_format("order_date", "yyyy-MM")
        )
        .groupBy("year_month")
        .agg(
            F.sum("revenue").alias("total_revenue"),
            F.sum("profit").alias("total_profit"),
            F.countDistinct("order_id").alias("orders")
        )
        .orderBy("year_month")
    )

    monthly_sales.show(30, truncate=False)

    # ---------------------------------------------------------
    # 9. PROFIT MARGIN
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("7. PRODUCT PROFIT MARGIN")
    print("=" * 70)

    (
        sales
        .groupBy(
            "product_id",
            "product_name"
        )
        .agg(
            F.sum("revenue").alias("revenue"),
            F.sum("profit").alias("profit")
        )
        .withColumn(
            "profit_margin",
            F.when(
                F.col("revenue") != 0,
                F.col("profit") / F.col("revenue") * 100
            ).otherwise(0)
        )
        .orderBy(
            F.col("profit_margin").desc()
        )
        .show(10, truncate=False)
    )

    # ---------------------------------------------------------
    # 10. WINDOW FUNCTION
    # ---------------------------------------------------------

    print("\n" + "=" * 70)
    print("8. PRODUCT RANKING BY REVENUE")
    print("=" * 70)

    product_revenue = (
        sales
        .groupBy(
            "product_id",
            "product_name"
        )
        .agg(
            F.sum("revenue").alias("total_revenue")
        )
    )

    revenue_window = Window.orderBy(
        F.col("total_revenue").desc()
    )

    (
        product_revenue
        .withColumn(
            "revenue_rank",
            F.rank().over(revenue_window)
        )
        .orderBy("revenue_rank")
        .show(10, truncate=False)
    )

    # ---------------------------------------------------------
    # STOP SPARK
    # ---------------------------------------------------------

    spark.stop()

    print("\n" + "=" * 70)
    print("PYSPARK ANALYTICS COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()