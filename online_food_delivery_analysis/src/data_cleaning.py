import pandas as pd
import numpy as np
import os

# =====================================================
# 1. SAFE FILE PATH SETUP (NO RELATIVE PATH ERRORS)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_PATH = os.path.join(BASE_DIR, "data", "ONLINE_FOOD_DELIVERY_ANALYSIS.csv")
OUTPUT_PATH = os.path.join(BASE_DIR, "data", "cleaned_food_delivery.csv")

# =====================================================
# 2. LOAD DATA
# =====================================================
df = pd.read_csv(INPUT_PATH)

print("\n✅ CSV Loaded Successfully")
print("Initial Shape:", df.shape)

# =====================================================
# 3. STANDARDIZE COLUMN NAMES
# =====================================================
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\n📌 Available Columns:")
print(df.columns.tolist())

# =====================================================
# 4. HANDLE MISSING VALUES
# =====================================================
num_cols = df.select_dtypes(include=["int64", "float64"]).columns
cat_cols = df.select_dtypes(include=["object"]).columns

df[num_cols] = df[num_cols].fillna(df[num_cols].median())
df[cat_cols] = df[cat_cols].fillna(df[cat_cols].mode().iloc[0])

# =====================================================
# 5. FIX INVALID VALUES
# =====================================================
if "delivery_rating" in df.columns:
    df["delivery_rating"] = df["delivery_rating"].clip(0, 5)

if "delivery_time" in df.columns:
    df["delivery_time"] = df["delivery_time"].clip(
        df["delivery_time"].quantile(0.05),
        df["delivery_time"].quantile(0.95)
    )

# =====================================================
# 6. PROFIT CALCULATION (DERIVED – REAL WORLD LOGIC)
# =====================================================
# Identify order value column
if "order_value" in df.columns:
    order_col = "order_value"
elif "total_amount" in df.columns:
    order_col = "total_amount"
else:
    raise Exception("❌ No order value column found")

# Discount (optional)
discount_col = "discount" if "discount" in df.columns else None

# Estimated costs
df["estimated_delivery_cost"] = df.get("distance_km", 5) * 5
df["estimated_platform_cost"] = df[order_col] * 0.10

# Profit calculation
if discount_col:
    df["profit"] = (
        df[order_col]
        - df[discount_col]
        - df["estimated_delivery_cost"]
        - df["estimated_platform_cost"]
    )
else:
    df["profit"] = (
        df[order_col]
        - df["estimated_delivery_cost"]
        - df["estimated_platform_cost"]
    )

df["profit"] = df["profit"].clip(lower=0)

# =====================================================
# 7. FEATURE ENGINEERING
# =====================================================
# Date handling
df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

# Weekday / Weekend
df["day_type"] = np.where(
    df["order_date"].dt.dayofweek >= 5,
    "Weekend",
    "Weekday"
)

# Hour & Peak Hour
df["hour"] = df["order_date"].dt.hour
df["peak_hour"] = np.where(
    df["hour"].between(12, 14) | df["hour"].between(19, 21),
    "Yes",
    "No"
)

# Profit Margin %
df["profit_margin_pct"] = (df["profit"] / df[order_col]) * 100

# Age Groups
if "customer_age" in df.columns:
    df["age_group"] = pd.cut(
        df["customer_age"],
        bins=[0, 18, 30, 45, 60, 100],
        labels=["Teen", "Young Adult", "Adult", "Mid Age", "Senior"]
    )

# Delivery Performance
if "delivery_time" in df.columns:
    df["delivery_performance"] = pd.cut(
        df["delivery_time"],
        bins=[0, 30, 45, 60, 300],
        labels=["Fast", "Average", "Slow", "Very Slow"]
    )

# =====================================================
# 8. SAVE CLEANED DATA
# =====================================================
df.to_csv(OUTPUT_PATH, index=False)

print("\n✅ DATA CLEANING COMPLETED SUCCESSFULLY")
print("Final Shape:", df.shape)
print(f"📁 Cleaned file saved at: {OUTPUT_PATH}")
