import os
import streamlit as st
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

warehouse = os.getenv("warehouse = "postgresql://airyll_user:iKiLhVkL0nHuRn2BFTsGWdmM4vEQI7Ls@dpg-d0k5tbruibrs73983cs0-a.singapore-postgres.render.com/airyll"
")
if not warehouse:
    st.error("❌ Environment variable DATABASE_URL not set!")
    st.stop()

# ✅ Connect to PostgreSQL
engine = create_engine(warehouse, client_encoding='utf8')
connection = engine.connect()

# ✅ Load and cache data from DB
@st.cache_data
def load_data():
    query = """
        SELECT "Product", COUNT(*) AS count
        FROM all_data
        GROUP BY "Product";
    """
    result = connection.execute(text(query))
    return pd.DataFrame(result.mappings().all())

# Load data
df = load_data()

# Preprocess
df = df.sort_values(by="count", ascending=False)
total_sales = df["count"].sum()
df["percentage"] = round(df["count"] / total_sales * 100, 2)

# ======================
# 🖥️ Streamlit UI Layout
# ======================
st.set_page_config(page_title="📊 Sales Dashboard", layout="wide")
st.title("📊 Sales Dashboard")
st.markdown("### Overview of Product Sales from your Database")

# Display total stats
col1, col2 = st.columns(2)
col1.metric("🧾 Total Sales", f"{total_sales:,}")
col2.metric("🛍️ Total Products", df.shape[0])

# Top product
top_product = df.iloc[0]
st.subheader("🏆 Most Sold Product")
st.markdown(f"""
- **Product**: `{top_product['Product']}`
- **Units Sold**: `{top_product['count']}`
- **Share**: `{top_product['percentage']}%` of total sales
""")

# Bar chart for top 5
st.subheader("📦 Top 5 Products by Sales")
st.bar_chart(df.head(5).set_index("Product")["count"])

# Least sold product
least_product = df.tail(1).iloc[0]
st.subheader("📉 Least Sold Product")
st.markdown(f"""
- **Product**: `{least_product['Product']}`
- **Units Sold**: `{least_product['count']}`
- **Share**: `{least_product['percentage']}%` of total sales
""")

# Full table
st.subheader("📋 Full Product Sales Data")
st.dataframe(df, use_container_width=True)
