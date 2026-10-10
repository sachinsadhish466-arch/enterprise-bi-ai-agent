
from pathlib import Path
import sqlite3

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
DATABASE_PATH = DATA_DIR / "business.db"


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    datasets = {
        "customers": "customers.csv",
        "products": "products.csv",
        "orders": "orders.csv",
    }

    with sqlite3.connect(DATABASE_PATH) as connection:
        for table_name, filename in datasets.items():
            csv_path = DATA_DIR / filename

            if not csv_path.exists():
                raise FileNotFoundError(
                    f"Missing dataset: {csv_path}"
                )

            df = pd.read_csv(csv_path)

            df.to_sql(
                table_name,
                connection,
                if_exists="replace",
                index=False,
            )

            print(
                f"Loaded {len(df)} rows into '{table_name}'"
            )

        # Verify the tables.
        print("\nDATABASE TABLES")
        print("-" * 40)

        for table_name in datasets:
            count = connection.execute(
                f"SELECT COUNT(*) FROM {table_name}"
            ).fetchone()[0]

            print(f"{table_name}: {count} rows")

    print(f"\nDatabase created: {DATABASE_PATH}")


if __name__ == "__main__":
    main()
