import pandas as pd
import sqlite3

df = pd.read_csv('olist_merged_cleaned.csv')

conn = sqlite3.connect('olist.db')

df.to_sql('orders_full', conn, if_exists='replace', index=False)

print("✅ Data loaded into olist.db -> table name: orders_full")
print(f"Total rows loaded: {len(df)}")

check = pd.read_sql("SELECT COUNT(*) as total_rows FROM orders_full", conn)
print(check)

conn.close()