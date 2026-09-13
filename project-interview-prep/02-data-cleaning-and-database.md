# 🧹 Module 02: Data Cleaning, Preprocessing Hygiene & Database Schema

> [!NOTE]
> Data cleaning and relational schema setup are primary topics in Data Analyst and Data Engineer interview loops. This module covers data quality issues, code implementations from `data/db_setup.py`, and database design.

---

## 📊 1. Raw Dataset Characteristics

The project utilizes the **IBM Telco Customer Churn dataset** comprising **7,043 rows** and **21 feature attributes**:
- **Target Feature (`Churn`):** Categorical binary string (`Yes` or `No`).
- **Demographics:** `gender`, `SeniorCitizen`, `Partner`, `Dependents`.
- **Account & Billing Details:** `tenure`, `Contract`, `PaperlessBilling`, `PaymentMethod`, `MonthlyCharges`, `TotalCharges`.
- **Subscribed Telecom Services:** `PhoneService`, `MultipleLines`, `InternetService`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`.

---

## 🧼 2. Key Data Quality Issues & Hygiene Rules

### Issue A: Missing Values & Whitespace Strings in `TotalCharges`
- **Symptom:** `TotalCharges` is stored as `object` (string) rather than `float64` in the raw CSV.
- **Root Cause Analysis:** 11 records in the dataset contain empty spaces (`' '`) instead of numeric values or `NaN`.
- **Investigation:** Running a filter on these 11 records revealed that **all of them had `tenure == 0`**.
  ```python
  null_rows = df[df['TotalCharges'].isnull()]
  print(null_rows['tenure'].value_counts())
  # Output: tenure 0: 11
  ```
- **Business Rationale:** Customers with `tenure == 0` are brand-new subscribers who signed up during the current billing cycle and have not yet received their first monthly bill.
- **Resolution Strategy:** 
  1. Replace whitespace patterns with `np.nan`: `df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True)`.
  2. Coerce column data type to float: `pd.to_numeric(df['TotalCharges'])`.
  3. Impute `0.0` for missing values rather than dropping records or imputing column means (which would artificially inflate new customer billing).

### Issue B: Duplicate Records Verification
- **Check:** `df.duplicated().sum()`.
- **Result:** 0 duplicate rows found in raw dataset. If duplicates exist, `df.drop_duplicates()` ensures unique customer entity resolution.

### Issue C: Column Naming Standardisation (`snake_case`)
- Raw dataset uses inconsistent mixed case (`customerID`, `SeniorCitizen`, `tenure`, `PaperlessBilling`).
- Re-mapped all 21 columns to standardized database `snake_case` (e.g., `customerID` $\rightarrow$ `customer_id`, `MonthlyCharges` $\rightarrow$ `monthly_charges`).

---

## 💻 3. Python Data Cleaning Pipeline Code (`data/db_setup.py`)

Below is the complete implementation script used to automate data cleaning, export clean CSVs, and load the SQLite database:

```python
import pandas as pd
import numpy as np
import sqlite3
import os

def clean_and_setup_db():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = os.path.join(base_dir, "customer_churn.csv")
    cleaned_path = os.path.join(base_dir, "customer_churn_cleaned.csv")
    db_path = os.path.join(base_dir, "churn.db")
    
    print("Loading raw customer churn dataset...")
    df = pd.read_csv(raw_path)
    
    # 1. Deduplication
    duplicates_count = df.duplicated().sum()
    if duplicates_count > 0:
        df = df.drop_duplicates()
        
    # 2. TotalCharges whitespace handling & coercion
    df['TotalCharges'] = df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True)
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges']).fillna(0.0)
    
    # 3. Standardize Column Names to snake_case
    col_mapping = {
        'customerID': 'customer_id',
        'gender': 'gender',
        'SeniorCitizen': 'senior_citizen',
        'Partner': 'partner',
        'Dependents': 'dependents',
        'tenure': 'tenure',
        'PhoneService': 'phone_service',
        'MultipleLines': 'multiple_lines',
        'InternetService': 'internet_service',
        'OnlineSecurity': 'online_security',
        'OnlineBackup': 'online_backup',
        'DeviceProtection': 'device_protection',
        'TechSupport': 'tech_support',
        'StreamingTV': 'streaming_tv',
        'StreamingMovies': 'streaming_movies',
        'Contract': 'contract',
        'PaperlessBilling': 'paperless_billing',
        'PaymentMethod': 'payment_method',
        'MonthlyCharges': 'monthly_charges',
        'TotalCharges': 'total_charges',
        'Churn': 'churn'
    }
    df = df.rename(columns=col_mapping)
    
    # 4. Export Cleaned CSV
    df.to_csv(cleaned_path, index=False)
    
    # 5. Populate SQLite Database
    conn = sqlite3.connect(db_path)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    
    # Verify DB Integrity
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers;")
    count = cursor.fetchone()[0]
    print(f"Successfully loaded {count} rows into SQLite table 'customers'.")
    conn.close()

if __name__ == "__main__":
    clean_and_setup_db()
```

---

## 🗄️ 4. Relational Database Schema (`churn.db` - `customers` Table)

| Column Name | SQLite Data Type | Key Type | Business Description |
| :--- | :--- | :--- | :--- |
| `customer_id` | `TEXT / VARCHAR(50)` | Primary Key | Unique alphanumeric identifier for each customer |
| `gender` | `TEXT` | Attribute | Female / Male |
| `senior_citizen` | `INTEGER` | Attribute | 1 if customer age >= 65, else 0 |
| `partner` | `TEXT` | Attribute | Yes / No (whether customer has a partner) |
| `dependents` | `TEXT` | Attribute | Yes / No (whether customer has dependents) |
| `tenure` | `INTEGER` | Attribute | Number of months subscriber has stayed with company |
| `phone_service` | `TEXT` | Attribute | Yes / No |
| `multiple_lines` | `TEXT` | Attribute | No / Yes / No phone service |
| `internet_service`| `TEXT` | Attribute | Fiber optic / DSL / No |
| `online_security` | `TEXT` | Attribute | No / Yes / No internet service |
| `online_backup` | `TEXT` | Attribute | No / Yes / No internet service |
| `device_protection`| `TEXT` | Attribute | No / Yes / No internet service |
| `tech_support` | `TEXT` | Attribute | No / Yes / No internet service |
| `streaming_tv` | `TEXT` | Attribute | No / Yes / No internet service |
| `streaming_movies`| `TEXT` | Attribute | No / Yes / No internet service |
| `contract` | `TEXT` | Attribute | Month-to-month / One year / Two year |
| `paperless_billing`| `TEXT` | Attribute | Yes / No |
| `payment_method` | `TEXT` | Attribute | Electronic check / Mailed check / Bank transfer (automatic) / Credit card (automatic) |
| `monthly_charges` | `REAL / FLOAT` | Metric | Current monthly bill amount ($) |
| `total_charges` | `REAL / FLOAT` | Metric | Total cumulative billing to date ($) |
| `churn` | `TEXT` | Target | Target binary label: `Yes` or `No` |

---

## 🎯 5. Data Hygiene Interview Q&A

### Q: Why did you convert `TotalCharges` missing values to 0.0 instead of using median imputation?
> **Answer:** *"Median or mean imputation assumes the data is Missing Randomly (MAR). In our dataset, all missing `TotalCharges` values corresponded to `tenure == 0`. Using median imputation (~$1,397) would inject false historical charges for brand-new customers who haven't completed their first billing cycle. Setting `TotalCharges = 0.0` accurately reflects domain reality."*

### Q: What primary keys and index strategies would you apply if scaling this SQLite schema to PostgreSQL/Snowflake?
> **Answer:** *"I would set `customer_id` as the Primary Key (`VARCHAR(50)`). For indexing, I would create a composite B-Tree index on `(contract, churn)` and `(payment_method, churn)` since these columns are heavily filtered and grouped during BI query execution."*
