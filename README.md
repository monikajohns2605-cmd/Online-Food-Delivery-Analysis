# Online-Food-Delivery-Analysis
End-to-end data analytics project using Python, Pandas, SQLAlchemy, MySQL, and Streamlit to derive business insights on customer behavior, delivery performance, revenue, and profitability with real-world data handling.

# 🍔 Online Food Delivery Analysis – Data-Driven Business Insights

An end-to-end data analytics project that analyzes online food delivery transactions to uncover customer behavior, operational efficiency, restaurant performance, and revenue insights.  
The project simulates real-world noisy data handling and follows industry-standard analytics practices.

---

## 📌 Project Objectives

- Understand customer ordering behavior
- Analyze delivery performance and operational efficiency
- Identify high and low performing restaurants
- Track revenue, profit, and cancellations
- Store cleaned data in MySQL for scalable analytics
- Build an interactive dashboard for business decision-making

---

## 🛠 Tech Stack

- **Python** (Pandas, NumPy)
- **SQLAlchemy**
- **MySQL**
- **Streamlit**
- **Data Analytics & EDA**
- **Business Intelligence Concepts**

---

## 📂 Project Structure

online_food_delivery_analysis/
│
├── data/
│ ├── ONLINE_FOOD_DELIVERY_ANALYSIS.csv
│ └── cleaned_food_delivery.csv
│
├── src/
│ ├── data_cleaning.py
│ ├── eda_analysis.py
│ ├── streamlit_dashboard.py
│ └── mysql_loader.py
│
├── requirements.txt
└── README.md


---

## 🔄 Project Workflow

### 1️⃣ Data Cleaning & Preprocessing
- Standardized column names
- Handled missing values using mean, median, and mode
- Treated outliers in delivery time and order value
- Corrected invalid ratings
- Ensured logical data consistency

### 2️⃣ Feature Engineering
- Day type (Weekday / Weekend)
- Peak hour identification
- Estimated delivery and platform costs
- Profit and profit margin calculation
- Delivery performance categorization
- Customer age grouping

### 3️⃣ Exploratory Data Analysis (EDA)
- Customer spending behavior
- Weekend vs weekday demand
- City-wise and category-wise revenue
- Delivery time vs rating analysis
- Cancellation rate and reasons
- Payment mode preferences

### 4️⃣ Data Storage (MySQL)
- Created structured MySQL database
- Inserted cleaned data using SQLAlchemy
- Enabled scalable querying and reporting
- Ready for BI tools like Power BI

### 5️⃣ Interactive Dashboard (Streamlit)
- Key KPIs:
  - Total Orders
  - Total Revenue
  - Average Order Value
  - Average Delivery Time
  - Cancellation Rate
  - Average Rating
  - Profit Margin %
- Dynamic filters for city and category
- Business-focused visualizations

---

## ▶️ How to Run the Project

### Step 1: Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate

Step 2: Install Dependencies
pip install -r requirements.txt

Step 3: Run Data Cleaning
python src/data_cleaning.py

Step 4: Load Data into MySQL
python src/mysql_loader.py

Step 5: Run Dashboard
python -m streamlit run src/streamlit_dashboard.py
