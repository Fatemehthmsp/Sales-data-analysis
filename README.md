Sales-data-analysis

Overview
A predictive analytics project to forecast daily sales in chain stores and extract insights into customer behavior.  
The model is designed to help optimize **inventory management, marketing campaigns, and operational planning**.

Dataset
- Source: Real-world daily sales transactions (`data.csv`)
- Key Features:
  - Store ID
  - Day of week
  - Date
  - Sales (target)
  - Customers
  - Promo (promotions)
  - StateHoliday
  - SchoolHoliday

Methods & Models
- Data Cleaning: Remove closed store days, zero-sales entries, and outliers.
- Feature Engineering:
  - Temporal features: year, month, week, day
  - Rolling means (7 & 30 days)
  - Lag features (previous week/day sales)
  - Sales per customer
- Model: LightGBM (Gradient Boosting)

Tools & Libraries
pandas, numpy, scikit-learn, lightgbm, matplotlib, seaborn

to run the web application, run the following line in terminal:
streamlit run app.py
