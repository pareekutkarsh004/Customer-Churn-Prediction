# ⚡ Customer Churn Prediction - 5-Minute Last-Minute Interview Revision Sheet

> [!TIP]
> **Read this file 10 minutes before your interview.** It contains the elevator pitch, exact metrics, key findings, model trade-offs, and top interview answers to recall instantly.

---

## 🎯 1. 30-Second Elevator Pitch
> *"In this project, I built an end-to-end Customer Churn Analytics and Predictive Modeling platform for a subscription-based telecom provider to reduce revenue loss. I cleaned and loaded 7,043 customer records into SQLite, conducted SQL cohort and micro-segmentation analysis, engineered ML preprocessing pipelines using Scikit-Learn (Logistic Regression, Decision Tree, Random Forest), and serialized the top-performing Random Forest model (ROC-AUC 84.27%). Finally, I deployed an interactive Streamlit executive dashboard featuring a real-time risk assessment simulator and automated retention action generator."*

---

## 📊 2. Core Numbers & Key Metrics Cheat Sheet

| Metric | Exact Value | Interview Relevance / Key Takeaway |
| :--- | :--- | :--- |
| **Total Customer Base** | **7,043** customers | Raw dataset size (IBM Telco Churn dataset) |
| **Total Churned Base** | **1,869** customers | 26.54% overall portfolio churn rate |
| **Monthly Revenue Lost** | **$139,130.85** / month | Financial magnitude of churn ($1.67M annualized) |
| **Avg Bill (Churned vs Active)** | **$74.44** vs. **$61.27** | Churned customers pay **21.5% higher** monthly bills |
| **Month-to-Month Contract Churn** | **42.71%** | 88% of all churn comes from month-to-month contracts |
| **1-Year & 2-Year Contract Churn** | **11.27%** & **2.83%** | Long-term contracts reduce churn risk by **Up to 93%** |
| **Electronic Check Churn Rate** | **45.29%** | Payment method with highest friction (vs ~15-16% Auto-Pay) |
| **High-Risk Segment Churn** | **60.37%** | Month-to-Month + Fiber Optic + Electronic Check (789/1,307 churned) |
| **Early Tenure Churn (0-6 Mos)** | **52.9%** | Over half of early joiners churn in the first 6 months |

---

## 🤖 3. Machine Learning Model Comparison Summary

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC | Key Advantage |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | 80.70% | 66.04% | **56.15%** | **60.69%** | 84.22% | **Highest Recall & Business Interpretability (Odds Ratios)** |
| **Decision Tree** (max_depth=5) | 79.42% | 63.12% | 54.01% | 58.21% | 82.67% | Non-linear tree structure visualization |
| **Random Forest** (n_est=150, depth=8) | **80.34%** | **67.64%** | 49.73% | 57.32% | **84.27%** | **Best overall rank-ordering (ROC-AUC) & lowest false positive rate** |

> [!NOTE]
> **Why Random Forest was serialized:** Random Forest achieved the highest ROC-AUC (84.27%) and precision (67.64%), minimizing wasted retention campaign budgets on non-churners. If the business prioritized catching every single churner regardless of cost, Logistic Regression (Recall 56.15%) or threshold tuning on Random Forest (lowering threshold to ~0.3) would be deployed.

---

## 🔍 4. Logistic Regression Odds Ratios (Feature Influences)

$$\text{Odds Ratio} = \exp(\beta_i)$$

- **Fiber Optic Internet:** Odds Ratio = **3.26** $\rightarrow$ Increases churn risk by **226%** (High cost / service friction).
- **Electronic Check Payment:** Odds Ratio = **1.47** $\rightarrow$ Increases churn risk by **47%** (Manual payment friction).
- **Senior Citizen:** Odds Ratio = **1.28** $\rightarrow$ Increases churn risk by **28%**.
- **2-Year Contract:** Odds Ratio = **0.27** $\rightarrow$ Reduces churn risk by **73%** (Contract lock-in effect).
- **Tenure:** Odds Ratio = **0.29** per standard unit $\rightarrow$ Each unit of tenure reduces churn risk by **71%** (Loyalty effect).

---

## 🚀 5. Top 4 Retention Recommendations (Business Value)

1. **Contract Migration Campaign:** Incentive (e.g., $10/mo credit for 12 mos) for month-to-month subscribers to upgrade to 1-year contracts.
2. **Auto-Pay Enrollment Push:** One-time $15 account credit to move electronic check users to automatic card/bank payments.
3. **Early Onboarding Success:** Automated touchpoints at Months 1, 3, and 5 to assist new users (where 52.9% churn occurs).
4. **Security & Support Bundling:** Bundle Tech Support and Online Security into Fiber Optic plans (reduces churn from 49% to 9%).

---

## 💡 6. Technical Stack Quick Cheat Sheet
- **Language & Core:** Python 3.8+, Pandas, NumPy
- **Database Analysis:** SQLite (`sqlite3` module), SQL aggregation, `CASE WHEN`, `HAVING`, `GROUP BY`
- **Machine Learning:** `scikit-learn` (`ColumnTransformer`, `StandardScaler`, `OneHotEncoder(drop='first')`, `train_test_split(stratify=y)`)
- **Model Storage:** `pickle` (`churn_prediction.pkl`)
- **Dashboard & UI:** Streamlit (`app.py`), Plotly Express & Graph Objects (`px.pie`, `px.bar`, `go.Indicator` gauge chart)

---

## ❓ 7. Top 5 "Must-Know" Interview Questions & Instant Answers

### Q1: "What problem does this project solve?"
> **Answer:** *"Subscription churn loses our business $139.1k in monthly revenue (26.54% churn rate). By analyzing customer behavior and building a machine learning model, we identify high-risk customers early and trigger targeted retention campaigns (like contract upgrades and auto-pay incentives) to save revenue."*

### Q2: "How did you handle missing values in `TotalCharges`?"
> **Answer:** *"11 rows in `TotalCharges` contained whitespace strings `' '`. I examined their tenure and found `tenure == 0`, meaning these were brand-new customers who hadn't been billed yet. I coerced the column to float using `pd.to_numeric()` and imputed `0.0` instead of dropping rows or using arbitrary mean imputation."*

### Q3: "Why did you use `drop='first'` in OneHotEncoder?"
> **Answer:** *"To prevent multi-collinearity (the dummy variable trap), especially for linear models like Logistic Regression where collinear features introduce severe instability in coefficient estimation."*

### Q4: "Why did you stratify the train-test split?"
> **Answer:** *"Our dataset is imbalanced (26.5% churn vs 73.5% non-churn). `stratify=y` guarantees that both training (80%) and test (20%) sets maintain the exact 26.5% target distribution, preventing sample bias."*

### Q5: "If Recall is low (49.73% for Random Forest), how do you fix it for business deployment?"
> **Answer:** *"By default, sklearn classifies outputs using a probability threshold of $0.5$. In churn prediction, missing a churner (False Negative) is far more expensive than contacting a non-churner (False Positive). In production, I would lower the decision threshold to $0.35$ or $0.30$, which boosts Recall to >75% while accepting slightly lower Precision."*
