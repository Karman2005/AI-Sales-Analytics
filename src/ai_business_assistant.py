import pandas as pd

# Load sales data
df = pd.read_csv("data/sales.csv")

def answer_question(question):
    question = question.lower()

    if "total sales" in question:
        return f"Total Sales: ₹{df['Sales'].sum():,.2f}"

    elif "total profit" in question:
        return f"Total Profit: ₹{df['Profit'].sum():,.2f}"

    elif "top product" in question:
        top_product = (
            df.groupby("Product")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )
        return f"Top product by sales: {top_product}"

    elif "top region" in question:
        top_region = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )
        return f"Top region by sales: {top_region}"

    elif "profit margin" in question:
        margin = df["Profit"].sum() / df["Sales"].sum() * 100
        return f"Overall Profit Margin: {margin:.2f}%"

    else:
        return "I can answer questions about total sales, total profit, top product, top region and profit margin."


print("AI Business Assistant")
print("Type 'exit' to stop.\n")

while True:
    question = input("Ask a business question: ")

    if question.lower() == "exit":
        break

    print(answer_question(question))
    print()