
from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATABASE_PATH = PROJECT_ROOT / "data" / "business.db"


def main():
    query = """
    SELECT
        p.product_name,
        SUM(p.unit_price * o.quantity * (1 - o.discount))
            AS total_revenue,
        SUM(
            (p.unit_price * (1 - o.discount) - p.unit_cost)
            * o.quantity
        ) AS total_profit
    FROM orders AS o
    JOIN products AS p
        ON o.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY total_revenue DESC;
    """

    with sqlite3.connect(DATABASE_PATH) as connection:
        cursor = connection.execute(query)

        print("\nPRODUCT REVENUE AND PROFIT")
        print("-" * 65)

        for row in cursor.fetchall():
            print(
                f"{row[0]:25} "
                f"Revenue: ₹{row[1]:,.2f} | "
                f"Profit: ₹{row[2]:,.2f}"
            )


if __name__ == "__main__":
    main()
