import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv('olist_merged_cleaned.csv')

monthly = df.groupby('order_year_month')['payment_value'].sum().reset_index()
monthly = monthly[monthly['order_year_month'] >= '2017-01']
monthly = monthly.sort_values('order_year_month').reset_index(drop=True)

monthly['month_index'] = range(len(monthly))

X = monthly[['month_index']]
y = monthly['payment_value']

model = LinearRegression()
model.fit(X, y)

future_index = pd.DataFrame({'month_index': [len(monthly), len(monthly) + 1, len(monthly) + 2]})
future_predictions = model.predict(future_index)

last_period = pd.Period(monthly['order_year_month'].iloc[-1], freq='M')
future_months = [(last_period + i).strftime('%Y-%m') for i in range(1, 4)]

forecast_df = pd.DataFrame({
    'order_year_month': future_months,
    'payment_value': future_predictions
})

print("=== ACTUAL MONTHLY REVENUE ===")
print(monthly[['order_year_month', 'payment_value']])

print("\n=== FORECASTED REVENUE (Next 3 Months) ===")
print(forecast_df)

print(f"\nModel R2 Score: {model.score(X, y):.3f}")
print(f"Avg Monthly Growth: R${model.coef_[0]:,.2f}")

all_months = list(monthly['order_year_month']) + list(forecast_df['order_year_month'])
all_values = list(monthly['payment_value']) + list(forecast_df['payment_value'])

plt.figure(figsize=(10, 5))
plt.plot(monthly['order_year_month'], monthly['payment_value'], marker='o', label='Actual Revenue', color='#2E5395')
plt.plot(forecast_df['order_year_month'], forecast_df['payment_value'], marker='o', linestyle='--', label='Forecast', color='#F5A524')
plt.xticks(rotation=45)
plt.ylabel('Revenue (R$)')
plt.title('Monthly Revenue: Actual vs Forecast (Next 3 Months)')
plt.legend()
plt.tight_layout()
plt.savefig('revenue_forecast.png', dpi=150)
print("\nSaved chart as revenue_forecast.png")

forecast_df.to_csv('revenue_forecast.csv', index=False)
print("Saved forecast data as revenue_forecast.csv")