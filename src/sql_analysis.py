import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("database/sales.db")

# Business summary
query = """
SELECT
    Order_ID,
    Product,
    Sales
FROM sales
WHERE Sales > (
    SELECT AVG(Sales)
    FROM sales
)
ORDER BY Sales DESC
LIMIT 20;
"""

result = pd.read_sql_query(query, connection)

print("Business Summary:")
print(result)



connection.close()