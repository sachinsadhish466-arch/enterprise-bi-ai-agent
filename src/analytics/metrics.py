
from pathlib import Path
import sqlite3
from datetime import date


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "business.db"


def execute_query(query, parameters=()):
    """Execute a read-only business query and return its results."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(query, parameters)
        return [dict(row) for row in cursor.fetchall()]


def total_business_metrics():
    query = """
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS unique_customers,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue,
        SUM(
            (p.unit_price * (1 - o.discount) - p.unit_cost)
            * o.quantity
        ) AS total_profit
    FROM orders o
    JOIN products p ON o.product_id = p.product_id;
    """
    return execute_query(query)[0]


def revenue_by_region():
    query = """
    SELECT
        o.region,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY o.region
    ORDER BY total_revenue DESC;
    """
    return execute_query(query)


def revenue_by_product():
    query = """
    SELECT
        p.product_name,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_revenue DESC;
    """
    return execute_query(query)


def top_customers(limit=5):
    query = """
    SELECT
        c.customer_name,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_id, c.customer_name
    ORDER BY total_revenue DESC
    LIMIT ?;
    """
    return execute_query(query, (limit,))


def monthly_revenue():
    query = """
    SELECT
        strftime('%Y-%m', o.order_date) AS year_month,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    GROUP BY year_month
    ORDER BY year_month;
    """
    return execute_query(query)

def business_metrics_by_date(start_date: str, end_date: str):
    """
    Return business metrics for an inclusive date range.

    Dates must use YYYY-MM-DD format.
    """
    try:
        start = date.fromisoformat(start_date)
        end = date.fromisoformat(end_date)
    except (ValueError, TypeError):
        raise ValueError(
            "Dates must use the YYYY-MM-DD format."
        ) from None

    if start.isoformat() != start_date or end.isoformat() != end_date:
        raise ValueError("Dates must use the YYYY-MM-DD format.")

    if start > end:
        raise ValueError("start_date cannot be after end_date.")

    query = """
    SELECT
        COUNT(DISTINCT o.order_id) AS total_orders,
        COUNT(DISTINCT o.customer_id) AS unique_customers,
        COALESCE(
            SUM(p.unit_price * o.quantity * (1 - o.discount)),
            0
        ) AS total_revenue,
        COALESCE(
            SUM(
                (p.unit_price * (1 - o.discount) - p.unit_cost)
                * o.quantity
            ),
            0
        ) AS total_profit
    FROM orders o
    JOIN products p ON o.product_id = p.product_id
    WHERE date(o.order_date) BETWEEN date(?) AND date(?);
    """

    return execute_query(
        query,
        (start.isoformat(), end.isoformat()),
    )[0]

if __name__ == "__main__":
    print("\nTOTAL BUSINESS METRICS")
    print(total_business_metrics())

    print("\nREVENUE BY REGION")
    for row in revenue_by_region():
        print(row)

    print("\nREVENUE BY PRODUCT")
    for row in revenue_by_product():
        print(row)

    print("\nTOP 5 CUSTOMERS")
    for row in top_customers():
        print(row)

    print("\nMONTHLY REVENUE")
    for row in monthly_revenue():
        print(row)
