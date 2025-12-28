import streamlit as st
import pandas as pd
import os

# =====================================================
# 1. PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Online Food Delivery Dashboard",
    layout="wide"
)

st.title("🍔 Online Food Delivery Analysis Dashboard")

# =====================================================
# 2. SAFE FILE PATH
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_food_delivery.csv")

if not os.path.exists(DATA_PATH):
    st.error("❌ cleaned_food_delivery.csv not found. Run data_cleaning.py first.")
    st.stop()

df = pd.read_csv(DATA_PATH)

# =====================================================
# 3. SHOW AVAILABLE COLUMNS (DEBUG FRIENDLY)
# =====================================================
with st.expander("📌 Available Columns in Dataset"):
    st.write(df.columns.tolist())

# =====================================================
# 4. KPI METRICS
# =====================================================
total_orders = len(df)
total_revenue = df["order_value"].sum() if "order_value" in df.columns else 0
avg_order_value = df["order_value"].mean() if "order_value" in df.columns else 0
avg_delivery_time = df["delivery_time"].mean() if "delivery_time" in df.columns else 0
cancellation_rate = (
    (df["order_status"] == "Cancelled").mean() * 100
    if "order_status" in df.columns else 0
)
avg_rating = df["delivery_rating"].mean() if "delivery_rating" in df.columns else 0
profit_margin = df["profit_margin_pct"].mean() if "profit_margin_pct" in df.columns else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("🧾 Total Orders", f"{total_orders:,}")
col2.metric("💰 Total Revenue", f"₹ {total_revenue:,.0f}")
col3.metric("🛒 Avg Order Value", f"₹ {avg_order_value:,.2f}")
col4.metric("⏱ Avg Delivery Time", f"{avg_delivery_time:.1f} mins")

col5, col6, col7 = st.columns(3)
col5.metric("❌ Cancellation Rate", f"{cancellation_rate:.2f}%")
col6.metric("⭐ Avg Delivery Rating", f"{avg_rating:.2f}")
col7.metric("📈 Avg Profit Margin", f"{profit_margin:.2f}%")

st.divider()

# =====================================================
# 5. SIDEBAR FILTERS (SAFE)
# =====================================================
st.sidebar.header("🔎 Filters")

# City filter
if "city" in df.columns:
    city_filter = st.sidebar.multiselect(
        "Select City",
        options=df["city"].unique(),
        default=df["city"].unique()
    )
else:
    city_filter = df.index

# Cuisine / Category filter (AUTO-DETECT)
cuisine_col = None
for col in ["cuisine", "food_type", "category", "restaurant_type"]:
    if col in df.columns:
        cuisine_col = col
        break

if cuisine_col:
    cuisine_filter = st.sidebar.multiselect(
        f"Select {cuisine_col.replace('_',' ').title()}",
        options=df[cuisine_col].unique(),
        default=df[cuisine_col].unique()
    )
else:
    cuisine_filter = df.index

# Apply filters safely
filtered_df = df.copy()

if "city" in df.columns:
    filtered_df = filtered_df[filtered_df["city"].isin(city_filter)]

if cuisine_col:
    filtered_df = filtered_df[filtered_df[cuisine_col].isin(cuisine_filter)]

# =====================================================
# 6. VISUAL ANALYTICS
# =====================================================
st.subheader("📊 Business Insights")

colA, colB = st.columns(2)

with colA:
    st.write("### Revenue by City")
    if "city" in filtered_df.columns:
        city_revenue = filtered_df.groupby("city")["order_value"].sum()
        st.bar_chart(city_revenue)
    else:
        st.info("City data not available")

with colB:
    st.write("### Orders by Category")
    if cuisine_col:
        st.bar_chart(filtered_df[cuisine_col].value_counts())
    else:
        st.info("Cuisine / category data not available")

colC, colD = st.columns(2)

with colC:
    st.write("### Delivery Performance")
    if "delivery_performance" in filtered_df.columns:
        st.bar_chart(filtered_df["delivery_performance"].value_counts())
    else:
        st.info("Delivery performance data not available")

with colD:
    st.write("### Payment Mode Preference")
    if "payment_mode" in filtered_df.columns:
        st.bar_chart(filtered_df["payment_mode"].value_counts())
    else:
        st.info("Payment mode data not available")

# =====================================================
# 7. CANCELLATION ANALYSIS
# =====================================================
st.subheader("❌ Cancellation Analysis")

if "order_status" in filtered_df.columns:
    cancelled = filtered_df[filtered_df["order_status"] == "Cancelled"]

    if not cancelled.empty and "cancellation_reason" in cancelled.columns:
        st.bar_chart(cancelled["cancellation_reason"].value_counts())
    else:
        st.info("No cancellation reason data available")
else:
    st.info("Order status column not available")

# =====================================================
# 8. TOP RESTAURANTS
# =====================================================
st.subheader("🏆 Top Rated Restaurants")

if "restaurant_name" in filtered_df.columns and "delivery_rating" in filtered_df.columns:
    top_restaurants = (
        filtered_df
        .groupby("restaurant_name")["delivery_rating"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    st.table(top_restaurants)
else:
    st.info("Restaurant or rating data not available")

# =====================================================
# 9. FOOTER
# =====================================================
st.divider()
st.caption("📌 Capstone Project | Python • Pandas • Streamlit")
