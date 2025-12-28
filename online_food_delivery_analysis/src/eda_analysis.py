import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("../data/cleaned_food_delivery.csv")

# -------------------------
# Customer & Order Analysis
# -------------------------
top_customers = df.groupby("customer_id")["order_value"].sum().sort_values(ascending=False).head(10)

age_vs_value = df.groupby("age_group")["order_value"].mean()

weekday_weekend = df.groupby("day_type")["order_id"].count()

# -------------------------
# Revenue & Profit
# -------------------------
df["month"] = pd.to_datetime(df["order_date"]).dt.to_period("M")
monthly_revenue = df.groupby("month")["order_value"].sum()

discount_profit = df.groupby("discount_applied")["profit"].mean()

city_revenue = df.groupby("city")["order_value"].sum().sort_values(ascending=False)

# -------------------------
# Delivery Performance
# -------------------------
delivery_by_city = df.groupby("city")["delivery_time"].mean()

sns.scatterplot(x="distance_km", y="delivery_time", data=df)
plt.title("Distance vs Delivery Time")
plt.show()

sns.boxplot(x="delivery_performance", y="delivery_rating", data=df)
plt.show()

# -------------------------
# Restaurant Performance
# -------------------------
top_restaurants = df.groupby("restaurant_name")["delivery_rating"].mean().sort_values(ascending=False).head(10)

cancellation_rate = df.groupby("restaurant_name")["order_status"].apply(
    lambda x: (x == "Cancelled").mean()
)

# -------------------------
# Operational Insights
# -------------------------
peak_hours = df.groupby("hour")["order_id"].count()

payment_modes = df["payment_mode"].value_counts()

cancel_reasons = df[df["order_status"] == "Cancelled"]["cancellation_reason"].value_counts()

print("✅ EDA & business analytics completed")
