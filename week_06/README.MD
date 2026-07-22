# 📊 Brazilian E-Commerce (Olist) Data Engineering & Analytics Dashboard

## 📌 Project Overview

This project is an end-to-end Data Engineering and Analytics solution developed using the Brazilian E-Commerce (Olist) Public Dataset. The project covers the complete data lifecycle, including data cleaning, preprocessing, feature engineering, exploratory data analysis (EDA), and an interactive web dashboard built with Flask and Bootstrap.

The objective is to transform raw transactional data into meaningful business insights through interactive visualizations and analytics.

---

# 🎯 Objectives

- Load and integrate multiple datasets
- Perform comprehensive data cleaning
- Handle missing values and outliers
- Engineer business-focused features
- Conduct exploratory data analysis
- Generate business insights
- Build an interactive analytics dashboard
- Export clean datasets and reports

---

# 📂 Dataset

**Dataset Name**

Brazilian E-Commerce Public Dataset by Olist

Dataset includes:

- Customers
- Orders
- Order Items
- Products
- Sellers
- Payments
- Reviews
- Geolocation
- Product Category Translation

---

# 🛠 Technologies Used

## Programming

- Python 3.x

## Data Analysis

- Pandas
- NumPy

## Visualization

- Matplotlib
- Seaborn

## Web Framework

- Flask

## Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Chart.js

---

# 📁 Project Structure

```
olist_dashboard/

│
├── app.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── css/
│   │      style.css
│   │
│   ├── js/
│   │      dashboard.js
│   │
│   └── images/
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── sales.html
│   ├── customer.html
│   ├── product.html
│   ├── seller.html
│   ├── payment.html
│   └── dataset.html
│
├── data/
│      final_cleaned_dataset.csv
│
└── notebook/
       Olist_Data_Analysis.ipynb
```

---

# 📊 Project Workflow

## Phase 1 – Data Understanding

- Load datasets
- Explore dataset dimensions
- Merge multiple tables
- Understand relationships
- Identify data types
- Generate descriptive statistics

---

## Phase 2 – Data Cleaning

- Handle missing values
- Remove duplicates
- Correct data types
- Detect invalid records
- Handle outliers using IQR
- Validate cleaned dataset

---

## Phase 3 – Feature Engineering

Created business features including:

- Delivery Time
- Shipping Duration
- Order Processing Time
- Customer Lifetime Value
- Total Order Value
- Average Product Price
- Average Review Score
- Customer Purchase Count
- Seller Performance Score
- Revenue Per Customer
- Monthly Sales
- Repeat Customer Indicator

---

## Phase 4 – Exploratory Data Analysis

Performed analysis on:

### Sales

- Monthly Sales Trend
- Revenue by Category
- Revenue by State
- Average Order Value

### Customers

- Customer Distribution
- Repeat Customers
- Customer Spending
- Top Purchasing Cities

### Products

- Best Selling Products
- Category Performance
- Product Pricing
- Product Popularity

### Sellers

- Top Sellers
- Revenue by Seller
- Seller Locations
- Delivery Performance

### Delivery

- Average Delivery Time
- Shipping Performance
- Delayed Deliveries

### Payment

- Payment Methods
- Installment Usage
- Payment Value Distribution

### Reviews

- Review Score Distribution
- Positive vs Negative Reviews
- Review Trend

---

# 🌐 Dashboard Features

## Dashboard

- KPI Cards
- Revenue Overview
- Monthly Revenue Trend
- Payment Analysis
- Product Categories
- Revenue by State
- Top Sellers
- Monthly Orders
- Order Status
- Review Analysis

---

## Sales Analytics

- Revenue Trends
- Category Performance
- Revenue by State
- Best Selling Products

---

## Customer Analytics

- Customer Distribution
- Repeat Customers
- Customer Lifetime Value
- Top Purchasing Cities

---

## Product Analytics

- Category Analysis
- Best Selling Products
- Product Pricing
- Product Popularity

---

## Seller Analytics

- Seller Performance
- Revenue by Seller
- Geographic Distribution
- Delivery Performance

---

## Payment & Review Analytics

- Payment Methods
- Installment Analysis
- Review Distribution
- Customer Satisfaction

---

## Dataset Explorer

- Search
- Filter
- Sort
- Pagination
- Export CSV

---

# 📈 Dashboard Visualizations

- Line Chart
- Bar Chart
- Horizontal Bar Chart
- Pie Chart
- Donut Chart
- Treemap
- Area Chart
- Histograms
- Heatmaps
- Boxplots

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/olist-dashboard.git
```

Navigate to the project

```bash
cd olist_dashboard
```

Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Install Dependencies

```bash
pip install -r requirements.txt
```

Run Flask Application

```bash
python app.py
```

Open Browser

```
http://127.0.0.1:5000
```

---

# 📊 Business Insights

The dashboard helps analyze:

- Revenue Performance
- Customer Purchasing Behavior
- Product Demand
- Seller Performance
- Payment Preferences
- Customer Satisfaction
- Delivery Efficiency

---

# 📦 Deliverables

- Complete Jupyter Notebook
- Clean Dataset
- Feature Engineered Dataset
- Data Quality Report
- Interactive Flask Dashboard
- Business Visualizations
- Project Documentation

---

# 👩‍💻 Author

**Harini Loganathan**

MCA Student

Data Analytics & Python Developer

---

# 📄 License

This project is developed for educational and academic purposes using the Brazilian E-Commerce (Olist) Public Dataset.
