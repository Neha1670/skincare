import pandas as pd

# 1. Excel file read karo
file_path = "data/rewa_clients_data.xlsx"
df = pd.read_excel(file_path)

# 2. Missing values aur cleaning
df['Purchase Type'] = df['Purchase Type'].fillna('One-Time')
df['Name'] = df['Name'].str.strip()
df['Address'] = df['Address'].str.strip()
df = df.drop_duplicates()

# 3. CSV me save karo
cleaned_path = "data/cleaned_data.csv"
df.to_csv(cleaned_path, index=False)

print(f"✅ Cleaned data saved at {cleaned_path}")
