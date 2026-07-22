# Customer Churn Analysis & Prediction Dashboard

This repository contains a comprehensive, end-to-end data analysis and machine learning pipeline to understand, analyze, and predict customer churn in a subscription business (telecom provider).

## 📊 Business Problem & Objective
Customer retention is one of the most critical challenges in subscription-based services. Retaining existing customers is significantly more cost-effective than acquiring new ones. The goal of this project is to:
1. **Identify the churn rate:** How many customers are leaving?
2. **Discover churn drivers:** What factors influence a customer's decision to leave?
3. **Build predictive models:** Can we anticipate which customers are likely to churn before they do?
4. **Formulate retention strategies:** What concrete, data-driven actions can the business take to mitigate churn?

---

## 🛠️ Tech Stack & Architecture
- **Data Analysis & Cleaning:** Python, [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
- **Database Analysis:** SQL (SQLite3)
- **Data Visualization:** [Plotly](https://plotly.com/python/), [Seaborn](https://seaborn.pydata.org/), [Matplotlib](https://matplotlib.org/)
- **Machine Learning:** [Scikit-learn](https://scikit-learn.org/) (Logistic Regression, Decision Tree, Random Forest)
- **Dashboard & User Interface:** [Streamlit](https://streamlit.io/) (Premium Web Interface)

---

## 📂 Repository Structure
All core files are listed below with clickable links for instant inspection:

- 📂 **[data/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/)** - Contains the database setup and data storage
  - 📄 **[customer_churn.csv](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/customer_churn.csv)** - The raw IBM customer churn dataset (7,043 rows, 21 columns)
  - 📄 **[customer_churn_cleaned.csv](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/customer_churn_cleaned.csv)** - Cleaned, preprocessed dataset ready for modeling and dashboarding
  - 📄 **[db_setup.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/db_setup.py)** - Python script that cleans data, handles missing values, and populates SQLite
  - 🗄️ **[churn.db](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/churn.db)** - SQLite database containing the final `customers` table
- 📂 **[notebooks/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/notebooks/)** - Jupyter exploratory notebooks
  - 📓 **[EDA.ipynb](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/notebooks/EDA.ipynb)** - Pre-run Jupyter Notebook containing all data cleaning notes, plots, and business insights
- 📂 **[sql/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/sql/)** - Analytical database queries
  - 📄 **[churn_analysis.sql](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/sql/churn_analysis.sql)** - Business intelligence queries answering contract, segment, cohort, and revenue churn questions
- 📂 **[model/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/)** - Machine Learning assets
  - 📄 **[train.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/train.py)** - Python script that trains Logistic Regression, Decision Tree, and Random Forest models, prints results, and serializes the best estimator
  - 💾 **[churn_prediction.pkl](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/churn_prediction.pkl)** - Best trained Random Forest prediction pipeline pickle file
- 💻 **[app.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/app.py)** - The premium interactive Streamlit dashboard and risk predictor application

---

## 🗄️ Database Schema & SQL Business Insights
We load the customer data into SQLite as the `customers` table with the following core columns:

| Column | Type | Description |
| :--- | :--- | :--- |
| `customer_id` | `VARCHAR(50)` (PK) | Unique identifier for each customer |
| `gender` | `VARCHAR(10)` | Male / Female |
| `senior_citizen` | `INTEGER` | 1 if senior citizen, 0 if not |
| `tenure` | `INTEGER` | Number of months the customer has been with the company |
| `contract` | `VARCHAR(20)` | Month-to-month, One year, Two year |
| `monthly_charges` | `REAL` | Current monthly bill amount |
| `total_charges` | `REAL` | Total amount billed to date |
| `churn` | `VARCHAR(5)` | Target field: Yes (customer left) or No (customer stayed) |
| `payment_method` | `VARCHAR(30)` | Payment type (Electronic check, Mailed check, Automatic card/bank) |
| `internet_service` | `VARCHAR(20)` | Type of internet connection (Fiber optic, DSL, None) |
| `tech_support` | `VARCHAR(20)` | Tech support subscription (Yes, No, No internet service) |

Key SQL business metrics from **[churn_analysis.sql](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/sql/churn_analysis.sql)**:
- **Overall Churn Rate:** **26.54%** of the portfolio (1,869 / 7,043 customers).
- **Revenue Leakage:** Churn accounts for **$139,130.85 per month** in lost monthly charges.
- **Contract Impact:** Month-to-month contract churn is **42.71%**, compared to 11.27% for 1-year and 2.83% for 2-year contracts.
- **Payment Method Friction:** Electronic checks show a high churn rate of **45.29%**, compared to automatic credit cards (15.24%) and automatic bank transfers (16.71%).
- **High-Risk Segment:** Month-to-month customers using **Fiber Optic + Electronic check** show a massive churn rate of **60.37%** (789 out of 1,307 customers in this segment churned).

---

## 🤖 Machine Learning Model Performance
We trained three classifiers to predict if a customer will churn. Features are preprocessed using standard scaling (numerical) and one-hot encoding (categorical). The models are evaluated on a 20% holdout test set.

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 80.70% | 66.04% | **56.15%** | **60.69%** | 84.22% |
| **Decision Tree** | 79.42% | 63.12% | 54.01% | 58.21% | 82.67% |
| **Random Forest** | **80.34%** | **67.64%** | 49.73% | 57.32% | **84.27%** |

### Logistic Regression Odds-Ratio Analysis
Since explainability is crucial for data analyst business insights, we analyze Logistic Regression coefficients:
- **Fiber Optic Internet:** Odds ratio is **3.26** (increases risk of churn by 226%).
- **Electronic Check Payments:** Odds ratio is **1.47** (increases risk of churn by 47%).
- **2-Year Contracts:** Odds ratio is **0.27** (reduces risk of churn by **73%**).
- **Tenure:** Odds ratio is **0.29** per standard unit (each unit of tenure reduces risk by **71%**).

*Note: The Random Forest pipeline (achieving the highest overall ROC-AUC of 84.27%) is serialized to `model/churn_prediction.pkl`.*

---

## 🚀 How to Run the Project Locally

### 1. Requirements
Ensure you have Python 3.8+ installed. Install required packages:
```bash
pip install pandas numpy scikit-learn matplotlib seaborn streamlit plotly nbformat nbconvert
```

### 2. Run Data Pipeline (Cleaning & SQL Loading)
This script cleans raw data, handles missing values, and writes to SQLite database:
```bash
python3 data/db_setup.py
```

### 3. Run Machine Learning Pipeline (Model Training)
This script trains the models, prints evaluation metrics, and exports the prediction pipeline:
```bash
python3 model/train.py
```

### 4. Launch Streamlit Web Dashboard
Launch the interactive dashboard, customer profile predictor, and SQL play console in your browser:
```bash
streamlit run app.py
```

---

## 🎯 Strategic Business Recommendations
Based on the EDA and predictive modelling, here are the top 4 data-driven retention campaigns:

1. **Promotional Contract Migration:**
   - **Insight:** Month-to-month customers represent 88% of all churned accounts.
   - **Action:** Launch a targeted email/SMS campaign targeting month-to-month subscribers offering a $10/month contract credit if they upgrade to a 12-month commitment.

2. **Auto-Pay Enrollment Push:**
   - **Insight:** Electronic Check payment method causes the highest billing friction (45.3% churn).
   - **Action:** Offer a one-time $15 account credit for enrolling in Auto-Pay via credit card or bank transfer, migrating customers off manual electronic checks.

3. **Early Tenure Welcome Program:**
   - **Insight:** Over 52.9% of new customer churn happens in the first 6 months.
   - **Action:** Trigger automated onboarding success touchpoints (support check-ins, starter guide emails, feedback calls) at Months 1, 3, and 5.

4. **Security & Support Bundling:**
   - **Insight:** Customers with no Online Security or Tech Support churn at ~49%, while those with both churn at just 9.0%.
   - **Action:** Bundle value-added security features into core premium fiber-optic internet packages instead of selling them as standalone add-ons.
