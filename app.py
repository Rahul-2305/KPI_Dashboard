import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="Executive KPI Dashboard",
    layout="wide"
)

st.title("📊 Executive KPI Dashboard")


# -----------------------------------
# LOAD DATA
# -----------------------------------

sales_query = """
SELECT *
FROM sales_data;
"""

marketing_query = """
SELECT *
FROM marketing_data;
"""

product_query = """
SELECT *
FROM product_data;
"""
sales_df = pd.read_csv('data/sales_data.csv')
marketing_df = pd.read_csv('data/marketing_data.csv')
product_df = pd.read_csv('data/product_data.csv')
# -----------------------------------
# DATA PREP
# -----------------------------------

sales_df['order_date'] = pd.to_datetime(
    sales_df['order_date']
)

sales_df['month'] = sales_df['order_date'].dt.strftime('%Y-%m')

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    sales_df['region'].unique(),
    default=sales_df['region'].unique()
)

selected_channel = st.sidebar.multiselect(
    "Select Channel",
    sales_df['channel'].unique(),
    default=sales_df['channel'].unique()
)

filtered_sales = sales_df[
    (sales_df['region'].isin(selected_region)) &
    (sales_df['channel'].isin(selected_channel))
]

# -----------------------------------
# KPI SECTION
# -----------------------------------

total_revenue = filtered_sales['revenue'].sum()

total_profit = filtered_sales['profit'].sum()

profit_margin = (
    total_profit / total_revenue
) * 100

total_units = filtered_sales['units_sold'].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Revenue",
    f"${total_revenue:,.0f}"
)

col2.metric(
    "📈 Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "📊 Profit Margin",
    f"{profit_margin:.2f}%"
)

col4.metric(
    "📦 Units Sold",
    f"{total_units:,}"
)

st.divider()

# -----------------------------------
# MONTHLY SALES TREND
# -----------------------------------

monthly_sales = (
    filtered_sales
    .groupby('month')['revenue']
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x='month',
    y='revenue',
    title='Monthly Revenue Trend',
    markers=True
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)

# -----------------------------------
# REGION ANALYSIS
# -----------------------------------

region_sales = (
    filtered_sales
    .groupby('region')[['revenue', 'profit']]
    .sum()
    .reset_index()
)

fig_region = px.bar(
    region_sales,
    x='region',
    y='revenue',
    color='profit',
    title='Region-wise Revenue & Profit'
)

st.plotly_chart(
    fig_region,
    use_container_width=True
)

# -----------------------------------
# PRODUCT PERFORMANCE
# -----------------------------------

merged_df = filtered_sales.merge(
    product_df,
    on='product_id'
)

top_products = (
    merged_df
    .groupby('product_name')['revenue']
    .sum()
    .reset_index()
    .sort_values(by='revenue', ascending=False)
    .head(10)
)

fig_products = px.bar(
    top_products,
    x='product_name',
    y='revenue',
    title='Top Products'
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# -----------------------------------
# MARKETING PERFORMANCE
# -----------------------------------

marketing_summary = (
    marketing_df
    .groupby('platform')
    .agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'spend': 'sum'
    })
    .reset_index()
)

marketing_summary['CTR'] = (
    marketing_summary['clicks']
    /
    marketing_summary['impressions']
) * 100

fig_marketing = px.bar(
    marketing_summary,
    x='platform',
    y='CTR',
    title='Platform CTR Comparison'
)

st.plotly_chart(
    fig_marketing,
    use_container_width=True
)

# -----------------------------------
# BUSINESS INSIGHTS
# -----------------------------------

st.subheader("📌 Business Recommendations")

top_region = (
    region_sales
    .sort_values(by='revenue', ascending=False)
    .iloc[0]['region']
)

worst_region = (
    region_sales
    .sort_values(by='profit')
    .iloc[0]['region']
)

top_product = (
    top_products
    .iloc[0]['product_name']
)

st.markdown(f"""
### Key Insights

- ✅ Highest revenue generating region: **{top_region}**
- ⚠️ Lowest profitability region: **{worst_region}**
- 🏆 Best performing product: **{top_product}**
- 📈 Consider increasing marketing investment in high-performing regions.
- 💡 Optimize pricing or promotions in low-profit regions.
""")


with st.expander("About this App"):
    st.write("Created by Beeraboina Rahul")
    st.write("Made in Python & Streamlit")
    st.write("Know more about Beeraboina Rahul at https://beeraboina-rahul-website.streamlit.app/")

st.caption("© 2026 Beeraboina Rahul")
