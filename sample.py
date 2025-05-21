import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text


warehouse = "postgresql://airyll_user:iKiLhVkL0nHuRn2BFTsGWdmM4vEQI7Ls@dpg-d0k5tbruibrs73983cs0-a.singapore-postgres.render.com/airyll"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()


# Load and cache data
@st.cache_data
def load_data():
    query = """
        SELECT "Product", COUNT(*) AS count
        FROM final
        GROUP BY "Product";
    """
    result = connection.execute(text(query))
    return pd.DataFrame(result.mappings().all())

df = load_data()
df = df.sort_values(by="count", ascending=False)
total_sales = df["count"].sum()
df["percentage"] = round(df["count"] / total_sales * 100, 2)

# ================================
# 🖥️ Streamlit Layout
# ================================
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Product Sales Dashboard")
st.markdown("### Visualizing product sales from your database")

# Total sales KPI
col1, col2 = st.columns(2)
col1.metric("🧾 Total Sales", f"{total_sales:,}")
col2.metric("🛍️ Total Products", df.shape[0])

# Bar chart for Top 5 products
st.subheader("🏆 Top 5 Best-Selling Products")
top5 = df.head(5)
bar_fig = px.bar(top5, x="Product", y="count", text="count", color="Product",
                 title="Top 5 Products by Sales")
st.plotly_chart(bar_fig, use_container_width=True)

# Pie chart: Sales breakdown
st.subheader("📈 Sales Percentage by Product")
pie_fig = px.pie(df, names="Product", values="percentage", hole=0.4,
                 title="Share of Each Product")
st.plotly_chart(pie_fig, use_container_width=True)

# Least sold product
st.subheader("📉 Least Sold Product")
least = df.tail(1).iloc[0]
st.markdown(f"""
- **Product**: `{least['Product']}`
- **Sales**: `{least['count']}` units
- **Share**: `{least['percentage']}%` of total
""")
