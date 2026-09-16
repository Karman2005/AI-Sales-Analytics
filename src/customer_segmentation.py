import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# 1. Load sales data
df = pd.read_csv("data/sales.csv")

# 2. Convert date
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# 3. Create customer-level RFM data
reference_date = df["Order_Date"].max() + pd.Timedelta(days=1)

rfm = df.groupby("Customer_ID").agg(
    Recency=("Order_Date", lambda x: (reference_date - x.max()).days),
    Frequency=("Order_ID", "nunique"),
    Monetary=("Sales", "sum")
).reset_index()

print("\nCustomer RFM Data:")
print(rfm.head())

# 4. Select features
features = ["Recency", "Frequency", "Monetary"]

X = rfm[features]

# 5. Standardize features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Apply K-Means
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)

rfm["Cluster"] = kmeans.fit_predict(X_scaled)

# 7. Display cluster information
print("\nCustomer Segments:")
print(rfm.groupby("Cluster")[features].mean())

print("\nCustomer Count per Cluster:")
print(rfm["Cluster"].value_counts().sort_index())

# 8. Save result
rfm.to_csv("data/customer_segments.csv", index=False)

# 9. Visualize
plt.figure(figsize=(8, 5))

plt.scatter(
    rfm["Frequency"],
    rfm["Monetary"],
    c=rfm["Cluster"],
    s=50
)

plt.xlabel("Frequency")
plt.ylabel("Monetary (Total Sales)")
plt.title("Customer Segmentation using K-Means")
plt.show()

print("\nCustomer segmentation completed successfully!")