import pandas as pd
import matplotlib.pyplot as plt

# 1. Cleaned CSV read karo
df = pd.read_csv("data/cleaned_data.csv")

# 2. Total Amount calculate (✅ CAPITAL P & Q)
df['Total Amount'] = df['Price'] * df['Quantity']

# 3. Purchase Type distribution
plt.figure(figsize=(6,4))
df['Purchase Type'].value_counts().plot(kind='bar')
plt.title('Purchase Type Distribution')
plt.xlabel('Purchase Type')
plt.ylabel('Number of Customers')
plt.tight_layout()
plt.show()

# 4. Top 5 customers by total amount
top_customers = (
    df.groupby('Name')['Total Amount']
      .sum()
      .sort_values(ascending=False)
      .head(5)
)

plt.figure(figsize=(8,4))
top_customers.plot(kind='bar')
plt.title('Top 5 Customers by Total Purchase Amount')
plt.xlabel('Customer Name')
plt.ylabel('Total Amount (₹)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
