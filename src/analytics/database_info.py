import sqlite3


DATABASE_PATH = "data/business.db"


def main():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    cursor = connection.cursor()

    print("\nDatabase Tables")
    print("=" * 50)

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
    """)

    tables = cursor.fetchall()

    for table in tables:

        table_name = table[0]

        cursor.execute(
            f"SELECT COUNT(*) FROM {table_name}"
        )

        row_count = cursor.fetchone()[0]

        print(
            f"{table_name:<15} "
            f"{row_count:>10,} rows"
        )

    connection.close()


if __name__ == "__main__":
    main()