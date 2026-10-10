from pyspark.sql import SparkSession


def create_spark_session():

    spark = (
        SparkSession.builder
        .appName("EnterpriseBI")
        .master("local[*]")
        .getOrCreate()
    )

    return spark


def load_orders(spark):

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/orders.csv")
    )


def load_products(spark):

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/products.csv")
    )


def load_customers(spark):

    return (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv("data/customers.csv")
    )