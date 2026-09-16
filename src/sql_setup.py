import pandas as pd
import sqlite3

# Load sales data
df = pd.read_csv("data/sales.csv")

# Connect to SQLite database
connection = sqlite3.connect("database/sales.db")

# Create sales table
df.to_sql("sales", connection, if_exists="replace", index=False)

print("Sales data successfully imported into SQLite!")

# Close connection
connection.close()