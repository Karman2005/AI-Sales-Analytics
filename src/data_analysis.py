import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Load dataset
df = pd.read_csv("data/sales.csv")

# Show first 5 rows
print("First 5 rows:")
print(df.head())

# Show number of rows and columns
print("\nDataset Shape:")
print(df.shape)

# Show column information
print("\nDataset Information:")
print(df.info())

# Check missing values data cleaning
print("\nMissing Values:")
print(df.isnull().sum())

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)

# Convert Order_Date to datetime
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

print("\nUpdated Data Types:")
print(df.dtypes)

# Statistical summary
print("\nStatistical Summary:")
print(df.describe())

# Total Sales
total_sales = df["Sales"].sum()

# Total Profit
total_profit = df["Profit"].sum()

print("\nTotal Sales:", total_sales)
print("Total Profit:", total_profit)

# Total Orders
total_orders = df["Order_ID"].nunique()

print("Total Orders:", total_orders)

# Total Customers
total_customers = df["Customer_ID"].nunique()

print("Total Customers:", total_customers)

# Top 10 Products by Sales
top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Sales:")
print(top_products)

# Visualize Top 10 Products
top_products.plot(kind="bar")

plt.title("Top 10 Products by Sales")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Sales by Category
category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Category:")
print(category_sales)

# Visualize Sales by Category
category_sales.plot(kind="bar")

plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

print("\nTop 10 Products by Sales (Readable):")

for product, sales in top_products.items():
    print(f"{product}: ₹{sales:,.2f}")


# Sales by Region
region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

print("\nSales by Region:")
print(region_sales)

# Visualize Sales by Region
region_sales.plot(kind="bar")

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)

plt.tight_layout()
plt.show()

# Monthly Sales
monthly_sales = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"]
    .sum()
)

print("\nMonthly Sales:")
print(monthly_sales)

# Convert period to string for plotting
monthly_sales.index = monthly_sales.index.astype(str)

monthly_sales.plot(kind="line", marker="o")

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")

plt.tight_layout()
plt.show()

# Create monthly sales DataFrame
monthly_sales_df = monthly_sales.reset_index()

monthly_sales_df.columns = ["Month", "Sales"]

print("\nMonthly Sales DataFrame:")
print(monthly_sales_df)

# Save monthly sales data
monthly_sales_df.to_csv("data/monthly_sales.csv", index=False)

print("\nMonthly sales file saved successfully!")

# Top 10 Products by Profit
top_profit_products = (
    df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTop 10 Products by Profit:")
print(top_profit_products)

# Visualize Top 10 Products by Profit
top_profit_products.plot(kind="bar")

plt.title("Top 10 Products by Profit")
plt.xlabel("Product")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Calculate Profit Margin
df["Profit_Margin"] = (df["Profit"] / df["Sales"]) * 100

print("\nProfit Margin:")
print(df["Profit_Margin"].describe())

# Sales vs Profit Relationship
plt.scatter(df["Sales"], df["Profit"])

plt.title("Sales vs Profit")
plt.xlabel("Sales")
plt.ylabel("Profit")

plt.tight_layout()
plt.show()

correlation = df["Sales"].corr(df["Profit"])

print("\nSales-Profit Correlation:", correlation)