import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# For reproducible results
np.random.seed(42)
random.seed(42)

# -----------------------------
# Basic data
# -----------------------------

products = {
    "Technology": {
        "Laptop": (40000, 100000),
        "Smartphone": (10000, 80000),
        "Monitor": (8000, 35000),
        "Keyboard": (800, 5000),
        "Mouse": (500, 3000),
    },
    "Furniture": {
        "Chair": (2000, 15000),
        "Table": (5000, 30000),
        "Desk": (4000, 25000),
        "Sofa": (15000, 60000),
    },
    "Home Appliances": {
        "Television": (15000, 100000),
        "Refrigerator": (20000, 90000),
        "Washing Machine": (18000, 70000),
        "Microwave": (6000, 25000),
    },
    "Accessories": {
        "Headphones": (1000, 12000),
        "Speaker": (1500, 15000),
        "Webcam": (1500, 10000),
        "Power Bank": (800, 5000),
    }
}

regions = ["North", "South", "East", "West", "Central"]

first_names = [
    "Aman", "Simran", "Rahul", "Priya", "Arjun",
    "Neha", "Karan", "Anjali", "Rohit", "Mehak",
    "Harpreet", "Navjot", "Manpreet", "Sahil", "Isha"
]

last_names = [
    "Sharma", "Kaur", "Singh", "Kumar", "Verma",
    "Gupta", "Malhotra", "Kapoor", "Patel", "Mehta"
]

# -----------------------------
# Customer data
# -----------------------------

num_customers = 500

customers = []

for i in range(1, num_customers + 1):
    name = random.choice(first_names) + " " + random.choice(last_names)

    customers.append({
        "Customer_ID": f"CUST{i:04d}",
        "Customer_Name": name
    })

# -----------------------------
# Generate sales records
# -----------------------------

num_orders = 5000

start_date = datetime(2024, 1, 1)
end_date = datetime(2026, 8, 31)

date_range = (end_date - start_date).days

records = []

for i in range(1, num_orders + 1):

    # Customer
    customer = random.choice(customers)

    # Category
    category = random.choice(list(products.keys()))

    # Product
    product = random.choice(list(products[category].keys()))

    # Price range
    min_price, max_price = products[category][product]

    unit_price = round(
        random.uniform(min_price, max_price), 2
    )

    # Quantity
    quantity = random.randint(1, 10)

    # Sales
    sales = round(unit_price * quantity, 2)

    # Profit margin between 5% and 25%
    profit_margin = random.uniform(0.05, 0.25)

    profit = round(sales * profit_margin, 2)

    # Random date
    random_days = random.randint(0, date_range)

    order_date = start_date + timedelta(days=random_days)

    # Region
    region = random.choice(regions)

    records.append({
        "Order_ID": f"ORD{i:05d}",
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": customer["Customer_ID"],
        "Customer_Name": customer["Customer_Name"],
        "Product": product,
        "Category": category,
        "Region": region,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Sales": sales,
        "Profit": profit
    })

# -----------------------------
# Create DataFrame
# -----------------------------

df = pd.DataFrame(records)

# -----------------------------
# Save CSV
# -----------------------------

df.to_csv("data/sales.csv", index=False)

print("✅ Dataset generated successfully!")
print(f"Total records: {len(df)}")
print(f"Total columns: {len(df.columns)}")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset saved to:")
print("data/sales.csv")