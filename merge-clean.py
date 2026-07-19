import pandas as pd

orders = pd.read_csv('olist_orders_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')
order_items = pd.read_csv('olist_order_items_dataset.csv')
payments = pd.read_csv('olist_order_payments_dataset.csv')
reviews = pd.read_csv('olist_order_reviews_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')
sellers = pd.read_csv('olist_sellers_dataset.csv')
category_translation = pd.read_csv('product_category_name_translation.csv')

print("=== ROW COUNTS ===")
print(f"Orders: {len(orders)}")
print(f"Customers: {len(customers)}")
print(f"Order Items: {len(order_items)}")
print(f"Payments: {len(payments)}")
print(f"Reviews: {len(reviews)}")
print(f"Products: {len(products)}")
print(f"Sellers: {len(sellers)}")

date_cols = ['order_purchase_timestamp', 'order_approved_at',
             'order_delivered_carrier_date', 'order_delivered_customer_date',
             'order_estimated_delivery_date']
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

orders = orders[orders['order_status'] == 'delivered']
orders = orders.dropna(subset=['order_delivered_customer_date'])

products = products.merge(category_translation, on='product_category_name', how='left')

df = orders.merge(customers, on='customer_id', how='left')
df = df.merge(order_items, on='order_id', how='left')
df = df.merge(products, on='product_id', how='left')
df = df.merge(sellers, on='seller_id', how='left')

payments_agg = payments.groupby('order_id').agg({
    'payment_value': 'sum',
    'payment_installments': 'max',
    'payment_type': lambda x: x.mode()[0] if not x.mode().empty else 'unknown'
}).reset_index()
df = df.merge(payments_agg, on='order_id', how='left')

reviews_dedup = reviews.sort_values('review_answer_timestamp').drop_duplicates('order_id', keep='last')
df = df.merge(reviews_dedup[['order_id', 'review_score']], on='order_id', how='left')

df['delivery_days'] = (df['order_delivered_customer_date'] - df['order_purchase_timestamp']).dt.days
df['estimated_days'] = (df['order_estimated_delivery_date'] - df['order_purchase_timestamp']).dt.days
df['delivery_delay_days'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days
df['is_late'] = df['delivery_delay_days'] > 0

df['order_year'] = df['order_purchase_timestamp'].dt.year
df['order_month'] = df['order_purchase_timestamp'].dt.month
df['order_year_month'] = df['order_purchase_timestamp'].dt.to_period('M').astype(str)

df = df.drop_duplicates()

print("\n=== FINAL MERGED DATA ===")
print(f"Total Rows: {len(df)}")
print(f"Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
print(f"Date Range: {df['order_purchase_timestamp'].min()} to {df['order_purchase_timestamp'].max()}")
print(f"Unique Customers: {df['customer_unique_id'].nunique()}")
print(f"Unique Sellers: {df['seller_id'].nunique()}")
print(f"Total Revenue: R${df['payment_value'].sum():,.2f}")
print(f"Late Delivery %: {df['is_late'].mean() * 100:.1f}%")

df.to_csv('olist_merged_cleaned.csv', index=False)
print("\n✅ Saved merged and cleaned data to 'olist_merged_cleaned.csv'")