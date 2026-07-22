-- =====================================================================
-- CUSTOMER CHURN ANALYSIS BUSINESS QUERIES
-- =====================================================================
-- Database: SQLite
-- Table: customers
-- =====================================================================

-- 1. OVERALL CHURN RATE
-- Calculates the total customer base, number of churned customers, and churn rate percentage.
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers;


-- 2. CHURN BY CONTRACT TYPE
-- Examines if long-term contracts significantly reduce churn.
SELECT 
    contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;


-- 3. REVENUE LOST & AVERAGE CHARGES DUE TO CHURN
-- Calculates the monthly revenue lost due to churn and compares monthly billing amounts.
SELECT 
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS total_monthly_revenue_lost,
    ROUND(AVG(CASE WHEN churn = 'Yes' THEN monthly_charges END), 2) AS avg_monthly_bill_churned,
    ROUND(AVG(CASE WHEN churn = 'No' THEN monthly_charges END), 2) AS avg_monthly_bill_active
FROM customers;


-- 4. TOP 10 HIGH-RISK CUSTOMER MICRO-SEGMENTS
-- Identifies combinations of Contract type, Internet Service type, and Payment Method with the highest churn rates.
-- We filter for segments with at least 50 customers to focus on statistically significant customer bases.
SELECT 
    contract,
    internet_service,
    payment_method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY contract, internet_service, payment_method
HAVING total_customers >= 50
ORDER BY churn_rate DESC
LIMIT 10;


-- 5. CHURN BY TENURE COHORT
-- Breaks down churn rates by customer age brackets (tenure groups) to see when customers leave.
SELECT 
    CASE 
        WHEN tenure <= 6 THEN '01. 0-6 Months'
        WHEN tenure <= 12 THEN '02. 7-12 Months'
        WHEN tenure <= 24 THEN '03. 1-2 Years'
        WHEN tenure <= 48 THEN '04. 2-4 Years'
        ELSE '05. 4+ Years'
    END AS tenure_cohort,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY tenure_cohort
ORDER BY tenure_cohort;


-- 6. CHURN RATE BY VALUE-ADDED SERVICES SUBSCRIPTION
-- Compares churn rates between customers with and without online support services.
SELECT 
    tech_support,
    online_security,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY tech_support, online_security
ORDER BY churn_rate DESC;
