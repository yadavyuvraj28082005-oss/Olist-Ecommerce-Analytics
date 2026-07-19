import pandas as pd

df = pd.read_csv('olist_merged_cleaned.csv')
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])

print("=== 1. REVENUE BY STATE ===")
state_revenue = df.groupby('customer_state').agg(
    total_revenue=('payment_value', 'sum'),
    total_orders=('order_id', 'nunique')
).sort_values('total_revenue', ascending=False)
print(state_revenue.head(10))

print("\n=== 2. TOP PRODUCT CATEGORIES BY REVENUE ===")
category_revenue = df.groupby('product_category_name_english').agg(
    total_revenue=('payment_value', 'sum'),
    total_orders=('order_id', 'nunique')
).sort_values('total_revenue', ascending=False)
print(category_revenue.head(10))

print("\n=== 3. MONTHLY SALES TREND ===")
monthly_trend = df.groupby('order_year_month').agg(
    total_revenue=('payment_value', 'sum'),
    total_orders=('order_id', 'nunique')
).sort_index()
print(monthly_trend)

print("\n=== 4. DELIVERY DELAY VS REVIEW SCORE ===")
review_by_delay = df.dropna(subset=['review_score']).groupby('is_late').agg(
    avg_review_score=('review_score', 'mean'),
    order_count=('order_id', 'nunique')
)
print(review_by_delay)

print("\n=== 5. PAYMENT TYPE DISTRIBUTION ===")
payment_dist = df.groupby('payment_type').agg(
    total_revenue=('payment_value', 'sum'),
    order_count=('order_id', 'nunique'),
    avg_installments=('payment_installments', 'mean')
).sort_values('total_revenue', ascending=False)
print(payment_dist)

print("\n=== 6. AVERAGE DELIVERY TIME BY STATE ===")
delivery_by_state = df.groupby('customer_state').agg(
    avg_delivery_days=('delivery_days', 'mean'),
    late_delivery_pct=('is_late', 'mean')
).sort_values('avg_delivery_days', ascending=False)
delivery_by_state['late_delivery_pct'] = (delivery_by_state['late_delivery_pct'] * 100).round(1)
print(delivery_by_state.head(10))

print("\n=== 7. TOP SELLERS BY REVENUE ===")
seller_revenue = df.groupby('seller_id').agg(
    total_revenue=('payment_value', 'sum'),
    total_orders=('order_id', 'nunique'),
    avg_review=('review_score', 'mean')
).sort_values('total_revenue', ascending=False)
print(seller_revenue.head(10))

state_revenue.to_csv('analysis_state_revenue.csv')
category_revenue.to_csv('analysis_category_revenue.csv')
monthly_trend.to_csv('analysis_monthly_trend.csv')
delivery_by_state.to_csv('analysis_delivery_by_state.csv')
payment_dist.to_csv('analysis_payment_distribution.csv')
seller_revenue.to_csv('analysis_seller_revenue.csv')

print("\n✅ Saved all analysis tables as separate CSVs for Power BI/Excel use")