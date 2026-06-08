import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# 1. Generate Raw Mock Data
np.random.seed(42)
dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='D')
n_records = 1000

raw_data = {
    'Transaction_ID': [f'TXN{1000+i}' for i in range(n_records)],
    'Date': np.random.choice(dates, n_records),
    'Product_Category': np.random.choice(['Electronics', 'Apparel', 'Home & Kitchen', 'Books', 'Beauty'], n_records, p=[0.3, 0.25, 0.2, 0.15, 0.1]),
    'Units_Sold': np.random.randint(1, 10, n_records),
    'Unit_Price': np.random.choice([15.0, 25.0, 50.0, 120.0, 300.0, 500.0], n_records, p=[0.2, 0.25, 0.2, 0.15, 0.1, 0.1]),
    'Region': np.random.choice(['North', 'South', 'East', 'West'], n_records)
}

df = pd.DataFrame(raw_data)
df['Total_Revenue'] = df['Units_Sold'] * df['Unit_Price']
df['Month'] = pd.to_datetime(df['Date']).dt.to_period('M').astype(str)

# 2. Compute KPI Metrics
total_revenue = df['Total_Revenue'].sum()
total_units = df['Units_Sold'].sum()
avg_order_value = df['Total_Revenue'].mean()

# 3. Build Dashboard Subplots
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Monthly Revenue Trend", "Revenue by Product Category", "Regional Sales Distribution", "Top Revenue Generating Transactions"),
    specs=[[{"type": "scatter"}, {"type": "bar"}],
           [{"type": "domain"}, {"type": "table"}]]
)

# Visual 1: Monthly Trend Line
trend = df.groupby('Month')['Total_Revenue'].sum().reset_index()
fig.add_trace(go.Scatter(x=trend['Month'], y=trend['Total_Revenue'], mode='lines+markers', name='Revenue'), row=1, col=1)

# Visual 2: Category Bar Chart
cat_data = df.groupby('Product_Category')['Total_Revenue'].sum().sort_values(ascending=False).reset_index()
fig.add_trace(go.Bar(x=cat_data['Product_Category'], y=cat_data['Total_Revenue'], name='Category Rev'), row=1, col=2)

# Visual 3: Regional Pie Chart
region_data = df.groupby('Region')['Total_Revenue'].sum().reset_index()
fig.add_trace(go.Pie(labels=region_data['Region'], values=region_data['Total_Revenue'], name='Region Split'), row=2, col=1)

# Visual 4: Granular Data Table
top_txns = df.sort_values(by='Total_Revenue', ascending=False).head(5)
fig.add_trace(go.Table(
    header=dict(values=['TXN ID', 'Category', 'Revenue'], fill_color='paleturquoise', align='left'),
    cells=dict(values=[top_txns.Transaction_ID, top_txns.Product_Category, top_txns.Total_Revenue], fill_color='lavender', align='left')
), row=2, col=2)

# Update layout styling and display KPI text at top
fig.update_layout(
    title_text=f"Sales & Revenue Dashboard Summary <br><sub>Total Revenue: ${total_revenue:,.2f} | Total Units Sold: {total_units:,} | AOV: ${avg_order_value:,.2f}</sub>",
    height=800, showlegend=False
)

# Open interactive dashboard in browser
fig.show()
