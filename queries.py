import sqlite3
import pandas as pd

conn = sqlite3.connect('olist.db')

queries = {
    "1. Top 10 States by Revenue": """
        SELECT customer_state, 
               SUM(payment_value) AS total_revenue,
               COUNT(DISTINCT order_id) AS total_orders
        FROM orders_full
        GROUP BY customer_state
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "2. Top 10 Product Categories by Revenue": """
        SELECT product_category_name_english,
               SUM(payment_value) AS total_revenue,
               COUNT(DISTINCT order_id) AS total_orders
        FROM orders_full
        WHERE product_category_name_english IS NOT NULL
        GROUP BY product_category_name_english
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "3. Monthly Sales Trend": """
        SELECT order_year_month,
               SUM(payment_value) AS total_revenue,
               COUNT(DISTINCT order_id) AS total_orders
        FROM orders_full
        GROUP BY order_year_month
        ORDER BY order_year_month;
    """,
    "4. Late Delivery Impact on Review Score": """
        SELECT is_late,
               ROUND(AVG(review_score), 2) AS avg_review_score,
               COUNT(DISTINCT order_id) AS order_count
        FROM orders_full
        WHERE review_score IS NOT NULL
        GROUP BY is_late;
    """,
    "5. Payment Type Distribution": """
        SELECT payment_type,
               SUM(payment_value) AS total_revenue,
               COUNT(DISTINCT order_id) AS order_count,
               ROUND(AVG(payment_installments), 1) AS avg_installments
        FROM orders_full
        GROUP BY payment_type
        ORDER BY total_revenue DESC;
    """,
    "6. Top 10 Sellers by Revenue": """
        SELECT seller_id,
               SUM(payment_value) AS total_revenue,
               COUNT(DISTINCT order_id) AS total_orders,
               ROUND(AVG(review_score), 2) AS avg_review
        FROM orders_full
        GROUP BY seller_id
        ORDER BY total_revenue DESC
        LIMIT 10;
    """,
    "7. States with Worst Delivery Performance": """
        SELECT customer_state,
               ROUND(AVG(delivery_days), 1) AS avg_delivery_days,
               ROUND(AVG(is_late) * 100, 1) AS late_delivery_pct
        FROM orders_full
        GROUP BY customer_state
        ORDER BY avg_delivery_days DESC
        LIMIT 10;
    """,
    "8. Repeat vs One-Time Customers": """
        SELECT 
            CASE WHEN order_count > 1 THEN 'Repeat Customer' ELSE 'One-Time Customer' END AS customer_type,
            COUNT(*) AS num_customers
        FROM (
            SELECT customer_unique_id, COUNT(DISTINCT order_id) AS order_count
            FROM orders_full
            GROUP BY customer_unique_id
        ) sub
        GROUP BY customer_type;
    """,
    "9. Average Order Value by State": """
        SELECT customer_state,
               ROUND(SUM(payment_value) / COUNT(DISTINCT order_id), 2) AS avg_order_value
        FROM orders_full
        GROUP BY customer_state
        ORDER BY avg_order_value DESC
        LIMIT 10;
    """,
    "10. Revenue Contribution: Top 10% Sellers": """
        SELECT seller_id, SUM(payment_value) AS total_revenue
        FROM orders_full
        GROUP BY seller_id
        ORDER BY total_revenue DESC
        LIMIT (SELECT CAST(COUNT(DISTINCT seller_id) * 0.1 AS INT) FROM orders_full);
    """
}

for title, query in queries.items():
    print(f"\n=== {title} ===")
    result = pd.read_sql(query, conn)
    print(result)

conn.close()