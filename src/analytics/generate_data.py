import os
import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

DATA_DIR = "data"

NUMBER_OF_CUSTOMERS = 1000
NUMBER_OF_PRODUCTS = 100
NUMBER_OF_ORDERS = 50000
NUMBER_OF_EMPLOYEES = 100


# ============================================================
# REFERENCE DATA
# ============================================================

REGIONS = {
    "North": [
        "Delhi",
        "Jaipur",
        "Lucknow",
        "Chandigarh",
        "Dehradun"
    ],
    "South": [
        "Chennai",
        "Bengaluru",
        "Hyderabad",
        "Coimbatore",
        "Kochi"
    ],
    "West": [
        "Mumbai",
        "Pune",
        "Ahmedabad",
        "Surat",
        "Nashik"
    ],
    "East": [
        "Kolkata",
        "Bhubaneswar",
        "Patna",
        "Ranchi",
        "Guwahati"
    ],
    "Central": [
        "Bhopal",
        "Indore",
        "Nagpur",
        "Raipur",
        "Jabalpur"
    ],
    "Northeast": [
        "Guwahati",
        "Agartala",
        "Shillong",
        "Imphal",
        "Aizawl"
    ]
}


INDUSTRIES = [
    "Technology",
    "Finance",
    "Healthcare",
    "Retail",
    "Manufacturing",
    "Education",
    "Logistics",
    "Energy",
    "Telecommunications",
    "Automotive"
]


PRODUCT_CATEGORIES = {
    "Computers": [
        "Laptops",
        "Desktops",
        "Monitors"
    ],
    "Accessories": [
        "Keyboards",
        "Mice",
        "Webcams"
    ],
    "Networking": [
        "Routers",
        "Switches",
        "Access Points"
    ],
    "Infrastructure": [
        "Servers",
        "Storage",
        "Backup Systems"
    ],
    "Software": [
        "Cybersecurity",
        "Analytics",
        "Productivity"
    ],
    "Cloud Services": [
        "Storage",
        "Compute",
        "Backup"
    ]
}


FIRST_NAMES = [
    "Arun",
    "Rahul",
    "Priya",
    "Karthik",
    "Sneha",
    "Vijay",
    "Anjali",
    "Rohit",
    "Divya",
    "Suresh",
    "Meena",
    "Amit",
    "Neha",
    "Manoj",
    "Kavya",
    "Naveen",
    "Pooja",
    "Raj",
    "Swathi",
    "Akash"
]


LAST_NAMES = [
    "Sharma",
    "Kumar",
    "Patel",
    "Reddy",
    "Iyer",
    "Nair",
    "Singh",
    "Das",
    "Rao",
    "Verma",
    "Gupta",
    "Mehta",
    "Joshi",
    "Menon",
    "Pillai"
]


# ============================================================
# CUSTOMER GENERATION
# ============================================================

def generate_customers():

    customers = []

    region_names = list(REGIONS.keys())

    for i in range(1, NUMBER_OF_CUSTOMERS + 1):

        region = random.choice(region_names)

        city = random.choice(REGIONS[region])

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        customer_name = (
            f"{first_name} {last_name} Enterprises"
        )

        customer_type = random.choices(
            ["Enterprise", "SMB", "Mid-Market"],
            weights=[30, 40, 30]
        )[0]

        industry = random.choice(INDUSTRIES)

        customers.append({
            "customer_id": f"C{i:05d}",
            "customer_name": customer_name,
            "customer_type": customer_type,
            "city": city,
            "region": region,
            "industry": industry
        })

    return pd.DataFrame(customers)


# ============================================================
# PRODUCT GENERATION
# ============================================================

def generate_products():

    products = []

    product_number = 1

    for category, sub_categories in PRODUCT_CATEGORIES.items():

        for sub_category in sub_categories:

            products_per_subcategory = (
                NUMBER_OF_PRODUCTS // len(
                    [
                        item
                        for values in PRODUCT_CATEGORIES.values()
                        for item in values
                    ]
                )
            )

            for _ in range(products_per_subcategory):

                if product_number > NUMBER_OF_PRODUCTS:
                    break

                unit_cost = random.randint(
                    500,
                    200000
                )

                margin = random.uniform(
                    0.15,
                    0.45
                )

                unit_price = round(
                    unit_cost * (1 + margin),
                    2
                )

                product_name = (
                    f"{sub_category} "
                    f"Product {product_number}"
                )

                products.append({
                    "product_id": f"P{product_number:04d}",
                    "product_name": product_name,
                    "category": category,
                    "sub_category": sub_category,
                    "unit_cost": unit_cost,
                    "unit_price": unit_price
                })

                product_number += 1

    return pd.DataFrame(products)


# ============================================================
# EMPLOYEE GENERATION
# ============================================================

def generate_employees():

    employees = []

    departments = [
        "Sales",
        "Finance",
        "Operations",
        "Marketing",
        "Technology",
        "HR"
    ]

    region_names = list(REGIONS.keys())

    for i in range(1, NUMBER_OF_EMPLOYEES + 1):

        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)

        employees.append({
            "employee_id": f"E{i:04d}",
            "employee_name": f"{first_name} {last_name}",
            "department": random.choice(departments),
            "region": random.choice(region_names)
        })

    return pd.DataFrame(employees)


# ============================================================
# ORDER GENERATION
# ============================================================

def generate_orders(customers, products):

    orders = []

    start_date = datetime(2025, 1, 1)

    end_date = datetime(2026, 9, 1)

    date_range = (
        end_date - start_date
    ).days

    customer_ids = customers["customer_id"].tolist()

    product_ids = products["product_id"].tolist()

    customer_region_map = dict(
        zip(
            customers["customer_id"],
            customers["region"]
        )
    )

    for i in range(1, NUMBER_OF_ORDERS + 1):

        customer_id = random.choice(
            customer_ids
        )

        product_id = random.choice(
            product_ids
        )

        order_date = (
            start_date +
            timedelta(
                days=random.randint(
                    0,
                    date_range
                )
            )
        )

        quantity = random.randint(
            1,
            20
        )

        discount = random.choice([
            0,
            0.02,
            0.03,
            0.05,
            0.08,
            0.10,
            0.15
        ])

        region = customer_region_map[
            customer_id
        ]

        orders.append({
            "order_id": f"O{i:07d}",
            "order_date": order_date.strftime(
                "%Y-%m-%d"
            ),
            "customer_id": customer_id,
            "product_id": product_id,
            "quantity": quantity,
            "discount": discount,
            "region": region
        })

    return pd.DataFrame(orders)


# ============================================================
# MAIN
# ============================================================

def main():

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    print("Generating enterprise dataset...")

    customers = generate_customers()

    products = generate_products()

    employees = generate_employees()

    orders = generate_orders(
        customers,
        products
    )

    customers.to_csv(
        f"{DATA_DIR}/customers.csv",
        index=False
    )

    products.to_csv(
        f"{DATA_DIR}/products.csv",
        index=False
    )

    employees.to_csv(
        f"{DATA_DIR}/employees.csv",
        index=False
    )

    orders.to_csv(
        f"{DATA_DIR}/orders.csv",
        index=False
    )

    print("\nDataset generation completed.")

    print("\nCustomers:")
    print(len(customers))

    print("\nProducts:")
    print(len(products))

    print("\nEmployees:")
    print(len(employees))

    print("\nOrders:")
    print(len(orders))

    print("\nFiles created:")

    print("data/customers.csv")
    print("data/products.csv")
    print("data/employees.csv")
    print("data/orders.csv")


if __name__ == "__main__":
    main()