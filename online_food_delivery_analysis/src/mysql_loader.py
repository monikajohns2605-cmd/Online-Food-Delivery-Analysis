import pandas as pd
from sqlalchemy import create_engine, text
import os

# =====================================================
# 1. SAFE FILE PATH (ABSOLUTE – NO ERRORS)
# =====================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_food_delivery.csv")

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        "❌ cleaned_food_delivery.csv not found. Run data_cleaning.py first."
    )

df = pd.read_csv(DATA_PATH)

print("✅ Cleaned CSV loaded")
print("Rows:", df.shape[0], "Columns:", df.shape[1])

# =====================================================
# 2. MYSQL CONNECTION DETAILS (STRINGS ONLY!)
# =====================================================
DB_USER = "root"                 # or "food_user"
DB_PASSWORD = "root"   # 🔴 CHANGE TO YOUR PASSWORD
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "food_delivery_db"

# =====================================================
# 3. CREATE SQLALCHEMY ENGINE
# =====================================================
engine = create_engine(
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False
)

# =====================================================
# 4. TEST MYSQL CONNECTION
# =====================================================
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("✅ MySQL connection successful")
except Exception as e:
    print("❌ MySQL connection failed")
    raise e

# =====================================================
# 5. CREATE TABLE WITH PROPER DATA TYPES
# =====================================================
create_table_sql = """
CREATE TABLE IF NOT EXISTS food_orders (
    order_id BIGINT,
    customer_id BIGINT,
    restaurant_name VARCHAR(255),
    city VARCHAR(100),
    order_date DATETIME,
    order_value FLOAT,
    discount FLOAT,
    delivery_time FLOAT,
    delivery_rating FLOAT,
    order_status VARCHAR(50),
    payment_mode VARCHAR(50),
    estimated_delivery_cost FLOAT,
    estimated_platform_cost FLOAT,
    profit FLOAT,
    profit_margin_pct FLOAT,
    day_type VARCHAR(20),
    peak_hour VARCHAR(10),
    age_group VARCHAR(20),
    delivery_performance VARCHAR(20)
);
"""

with engine.connect() as conn:
    conn.execute(text(create_table_sql))

print("✅ MySQL table created / verified")

# =====================================================
# 6. INSERT DATA USING SQLALCHEMY (SCALABLE)
# =====================================================
df.to_sql(
    name="food_orders",
    con=engine,
    if_exists="replace",   # replaces table safely
    index=False,
    chunksize=5000,
    method="multi"
)

print("✅ Data inserted into MySQL successfully")

# =====================================================
# 7. VALIDATION QUERY
# =====================================================
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM food_orders"))
    total_rows = result.scalar()

print(f"📊 Total records in MySQL table: {total_rows}")
