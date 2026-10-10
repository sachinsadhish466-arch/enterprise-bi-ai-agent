import pandas as pd


def main():
    file_path = "data/customers.csv"

    customers = pd.read_csv(file_path)

    print("First 5 customers:")
    print(customers.head())

    print("\nDataset shape:")
    print(customers.shape)

    print("\nColumns:")
    print(customers.columns.tolist())

    print("\nCustomer distribution by region:")
    print(customers["region"].value_counts())


if __name__ == "__main__":
    main()