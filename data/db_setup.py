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
    
    # 1. Check and remove duplicate rows
    duplicates_count = df.duplicated().sum()
    print(f"Duplicate records found: {duplicates_count}")
    if duplicates_count > 0:
        df = df.drop_duplicates()
        print("Duplicates removed.")
        
    # 2. Inspect and handle missing values in TotalCharges
    # Replace empty spaces with NaN
    df['TotalCharges'] = df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True)
    
    # Check count of missing values
    null_total_charges = df['TotalCharges'].isnull().sum()
    print(f"Missing values in TotalCharges: {null_total_charges}")
    
    # Examine rows with null TotalCharges
    if null_total_charges > 0:
        null_rows = df[df['TotalCharges'].isnull()]
        print("Tenure values for rows with missing TotalCharges:")
        print(null_rows['tenure'].value_counts())
        
        # Since tenure is 0 for these customers, they have just joined and total charges are 0.
        # Coerce to float and fill NaN with 0.0 or MonthlyCharges. Filling with 0.0 is accurate.
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
        df['TotalCharges'] = df['TotalCharges'].fillna(0.0)
        print("Filled missing TotalCharges with 0.0")
    else:
        df['TotalCharges'] = pd.to_numeric(df['TotalCharges'])
        
    # Double check other columns for missing values
    missing_other = df.isnull().sum().sum()
    print(f"Other missing values in dataset: {missing_other}")
    
    # 3. Standardize Column Names (convert to lowercase snake_case)
    # Mapping table from CamelCase / mixed to snake_case
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
    
    # 4. Save Cleaned Dataset to CSV
    df.to_csv(cleaned_path, index=False)
    print(f"Saved cleaned dataset to: {cleaned_path}")
    
    # 5. Store in SQLite database
    print(f"Connecting to database: {db_path}...")
    conn = sqlite3.connect(db_path)
    
    # Save the dataframe to 'customers' table. Overwrite if exists.
    df.to_sql("customers", conn, if_exists="replace", index=False)
    print("Successfully wrote dataset to SQLite table 'customers'.")
    
    # Verify by running a quick count query
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customers;")
    count = cursor.fetchone()[0]
    print(f"Verified row count in database table 'customers': {count}")
    
    # Close connection
    conn.close()
    print("Database setup complete!")

if __name__ == "__main__":
    clean_and_setup_db()
