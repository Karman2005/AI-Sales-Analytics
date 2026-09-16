import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# Load data
df = pd.read_csv("data/sales.csv")
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Monthly sales
monthly_sales = (
    df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order_Date"] = monthly_sales["Order_Date"].dt.to_timestamp()

# Create time feature
monthly_sales["Month_Number"] = range(1, len(monthly_sales) + 1)

# Train model
X = monthly_sales[["Month_Number"]]
y = monthly_sales["Sales"]

model = LinearRegression()
model.fit(X, y)

# Predict
monthly_sales["Predicted_Sales"] = model.predict(X)

print("\nMonthly Sales Forecast:")
print(monthly_sales)

# Save results
monthly_sales.to_csv("data/monthly_sales_forecast.csv", index=False)

# Plot
plt.figure(figsize=(10, 5))

plt.plot(
    monthly_sales["Order_Date"],
    monthly_sales["Sales"],
    marker="o",
    label="Actual Sales"
)

plt.plot(
    monthly_sales["Order_Date"],
    monthly_sales["Predicted_Sales"],
    marker="o",
    label="Predicted Sales"
)

plt.xlabel("Month")
plt.ylabel("Sales")
plt.title("Sales Forecasting")
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\nSales forecasting completed successfully!")