# Sales-data-analysis
Analyzing sales data and customer behavior in chain stores: Focusing on the effectiveness of advertising campaigns

```markdown
🛒 Retail Chain Sales & Customer Behavior Analysis

📌 Overview
A predictive analytics project to forecast daily sales in chain stores and extract insights into customer behavior.  
The model is designed to help optimize **inventory management, marketing campaigns, and operational planning**.

📂 Dataset
- **Source:** Real-world daily sales transactions (`data.csv`)
- **Key Features:**
  - Store ID
  - Day of week
  - Date
  - Sales (target)
  - Customers
  - Promo (promotions)
  - StateHoliday
  - SchoolHoliday

🛠 Methods & Models
- **Data Cleaning:** Remove closed store days, zero-sales entries, and outliers.
- **Feature Engineering:**
  - Temporal features: year, month, week, day
  - Rolling means (7 & 30 days)
  - Lag features (previous week/day sales)
  - Sales per customer
- **Model:** LightGBM (Gradient Boosting)

📊 Model Performance
| Metric | Value |
|---|---|
| **R²** | 0.9079 |
| **RMSE** | 790.73 |
| **MAE** | 573.16 |

💡 Insights
- Store-specific differences have a major impact on sales.
- Rolling averages and lag features capture seasonal/weekly behavior.
- Promotions significantly boost daily sales.

to run the web application, run the following line in terminal:
streamlit run app.py
