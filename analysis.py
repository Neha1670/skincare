import pandas as pd

# Load cleaned data
df = pd.read_csv("data/cleaned_data.csv")

print("=== First 5 rows ===")
print(df.head())

print("\n=== Column info ===")
print(df.info())

print("\n=== Summary statistics (Price & Quantity) ===")
print(df[['Price', 'Quantity']].describe())

print("\n=== Purchase Type count ===")
print(df['Purchase Type'].value_counts())

# ✅ FIX HERE (Price & Quantity – capital P & Q)
df['Total Amount'] = df['Price'] * df['Quantity']

print("\n=== Top 5 customers by total purchase amount ===")
top_customers = (
    df.groupby('Name')['Total Amount']
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_customers)
