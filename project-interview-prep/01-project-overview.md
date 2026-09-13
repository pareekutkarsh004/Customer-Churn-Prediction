# 📘 Module 01: Comprehensive Project Overview & Architecture

> [!NOTE]
> This document provides an exhaustive breakdown of the project background, business context, architecture, end-to-end data pipeline flow, and tech stack rationale suitable for senior DS/DA technical interviews.

---

## 🎯 1. Business Problem & Project Objective

In subscription-based businesses (such as telecommunications, SaaS, streaming services, and broadband providers), **customer churn**—the percentage of subscribers who cancel their contracts—is the single biggest threat to long-term recurring revenue.

### Key Industry Dynamics:
1. **Acquisition vs. Retention Cost:** Customer Acquisition Cost (CAC) in telecom is **5x to 7x higher** than the cost of retaining an existing subscriber through proactive engagement, loyalty discounts, or service bundles.
2. **Predictive Intervention Window:** Once a customer submits a cancellation request, it is usually too late to retain them. Effective retention requires **predicting churn intent months in advance** while intervention strategies can still succeed.
3. **Revenue Leakage:** Unchecked churn compound-erodes monthly recurring revenue (MRR), reducing Customer Lifetime Value (CLV) and depressing enterprise valuation.

### Core Objectives of this Project:
- **Analyze Portfolio Churn:** Determine overall churn rate, revenue leakage, and cohort dynamics using SQL analytics.
- **Uncover Behavioral Drivers:** Identify key risk drivers (contract type, payment method friction, service bundles, pricing sensitivity) using exploratory data analysis and statistical model coefficients.
- **Predictive Risk Engine:** Train and evaluate classification algorithms (Logistic Regression, Decision Tree, Random Forest) to predict individual customer churn probabilities.
- **Deploy Decision Platform:** Package the solution into a web dashboard for business stakeholders, complete with an interactive risk simulator and automated retention action recommendations.

---

## 🏗️ 2. End-to-End System Architecture

The project follows a modular, production-ready architecture spanning data engineering, SQL storage, ML modeling, and web deployment.

```
                                    +-----------------------------------+
                                    |     IBM Telco Churn Dataset       |
                                    |     (7,043 rows, 21 columns)     |
                                    +-----------------------------------+
                                                      |
                                                      v
                                    +-----------------------------------+
                                    |   Data Hygiene & Cleaning Script  |
                                    |         (data/db_setup.py)        |
                                    |  - Standardize column names       |
                                    |  - Impute TotalCharges (tenure=0) |
                                    |  - Deduplicate records            |
                                    +-----------------------------------+
                                             /                 \
                                            /                   \
                                           v                     v
            +----------------------------------+    +----------------------------------+
            |      Clean CSV Storage           |    |     SQLite Database Storage      |
            | (data/customer_churn_cleaned.csv)|    |        (data/churn.db)           |
            +----------------------------------+    +----------------------------------+
                             |                                   |
                             v                                   v
            +----------------------------------+    +----------------------------------+
            |   Machine Learning Pipeline      |    |       SQL Analytics Engine       |
            |       (model/train.py)           |    |      (sql/churn_analysis.sql)   |
            | - ColumnTransformer              |    | - Churn rate & MRR lost          |
            | - Train-Test Split (Stratified)  |    | - High-risk micro-segments       |
            | - LogReg / DecTree / RandomForest|    | - Service cohort analysis        |
            +----------------------------------+    +----------------------------------+
                             |
                             v
            +----------------------------------+
            |     Serialized Best Pipeline     |
            |   (model/churn_prediction.pkl)   |
            +----------------------------------+
                             \                                   /
                              \                                 /
                               v                               v
            +------------------------------------------------------------------+
            |              Interactive Streamlit Web Application               |
            |                            (app.py)                              |
            |  - Executive Dashboard (Plotly Charts & KPI Glassmorphic Cards)   |
            |  - Real-Time Customer Risk Assessment Simulator                  |
            |  - SQL Business Query Execution Console                          |
            +------------------------------------------------------------------+
```

---

## 🛠️ 3. Tech Stack & Framework Justification

In technical interviews, interviewers frequently ask **"Why did you choose tool X over tool Y?"**. Below are explicit justifications for every component of our stack:

### A. Data Processing & Pipeline (`Python`, `Pandas`, `NumPy`)
- **Why Python?** Standard industry ecosystem for data science, seamlessly connecting database operations, ML frameworks, and web rendering.
- **Why Pandas & NumPy?** Vectorized array operations deliver high execution performance for tabular data manipulation, feature encoding, and dataset aggregation.

### B. Database Layer (`SQLite3`)
- **Why SQLite?** Lightweight, serverless SQL database embedded directly in Python standard library (`sqlite3`). Allows writing native ANSI SQL queries without requiring external database servers (PostgreSQL/MySQL) while maintaining full ACID compliance for desktop and lightweight web dashboard querying.

### C. Machine Learning Engine (`Scikit-Learn`)
- **Why Scikit-Learn Pipelines?** Using `Pipeline` and `ColumnTransformer` guarantees that all feature scaling and One-Hot Encodings are calculated strictly on training data during cross-validation/train-test splitting, eliminating **data leakage**.

### D. Data Visualization (`Plotly`, `Seaborn`, `Matplotlib`)
- **Why Plotly for Web Dashboard?** Plotly generates responsive, interactive JavaScript visualizations (hover tooltips, zooming, filtering) native to web browsers, outperforming static images produced by Matplotlib/Seaborn.

### E. Application Deployment (`Streamlit`)
- **Why Streamlit?** Rapid production web app creation purely in Python. Combines metric rendering, user input sliders, interactive charts, and live model prediction without needing React/Vue frontend overhead.

---

## 📁 4. Project Directory Structure Map

- 📂 **[data/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/)**
  - 📄 **[customer_churn.csv](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/customer_churn.csv)** - Raw dataset (7,043 rows, 21 columns).
  - 📄 **[customer_churn_cleaned.csv](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/customer_churn_cleaned.csv)** - Cleaned, standardized CSV dataset.
  - 📄 **[db_setup.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/db_setup.py)** - Data hygiene pipeline and SQLite database population script.
  - 🗄️ **[churn.db](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/data/churn.db)** - SQLite relational database storing `customers` table.
- 📂 **[notebooks/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/notebooks/)**
  - 📓 **[EDA.ipynb](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/notebooks/EDA.ipynb)** - Jupyter Notebook with pre-run exploratory plots and correlation matrices.
- 📂 **[sql/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/sql/)**
  - 📄 **[churn_analysis.sql](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/sql/churn_analysis.sql)** - Business intelligence queries answering contract, segment, cohort, and revenue churn questions.
- 📂 **[model/](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/)**
  - 📄 **[train.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/train.py)** - Model training, evaluation, odds-ratio calculation, and pipeline serialization script.
  - 💾 **[churn_prediction.pkl](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/model/churn_prediction.pkl)** - Serialized Scikit-Learn Random Forest pipeline.
- 💻 **[app.py](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/app.py)** - Streamlit web app (Dashboard, Predictor Simulator, SQL Console).
- 📄 **[README.md](file:///Users/utarshpareek/Desktop/Customer-Churn-Prediction%20DA%20PROJ/README.md)** - Documentation & project overview.
