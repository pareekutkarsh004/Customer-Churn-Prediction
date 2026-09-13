# ⚖️ Module 07: Technical Decisions, Architectural Trade-offs & Alternatives

> [!NOTE]
> Senior interviewers heavily scrutinize architectural decisions and alternative approaches. This module details the trade-offs evaluated across modeling, class imbalance, database selection, and deployment stacks.

---

## 🤖 1. Model Selection: Logistic Regression vs. Decision Tree vs. Random Forest

| Evaluated Dimension | Logistic Regression | Decision Tree (`depth=5`) | Random Forest (`n_est=150`) | Winning Choice & Justification |
| :--- | :--- | :--- | :--- | :--- |
| **ROC-AUC Score** | 84.22% | 82.67% | **84.27%** | **Random Forest** (Highest overall rank ordering) |
| **Precision** | 66.04% | 63.12% | **67.64%** | **Random Forest** (Lowest false positive rate) |
| **Recall (Default 0.5)** | **56.15%** | 54.01% | 49.73% | **Logistic Regression** |
| **Explainability** | **Extremely High** (Odds Ratios) | High (Tree Diagrams) | Moderate (Feature Importance) | **Logistic Regression** for business slides |
| **Non-Linear Interactions** | Poor (Requires manual terms) | Moderate | **Excellent** | **Random Forest** |

### The Core Trade-off Answered:
- **Why Random Forest was serialized:** Random Forest delivered the overall best generalizability (ROC-AUC 84.27%) and precision (67.64%), minimizing wasted financial spend on retention offers sent to customers who wouldn't have churned anyway.
- **How to resolve the lower Recall in production:** In churn prediction, False Negatives (losing a $74/mo subscriber) are 5x more costly than False Positives ($15 campaign offer). In production deployment, we **adjust the decision threshold from 0.50 down to 0.35**, which elevates Random Forest Recall to >72%.

---

## ⚖️ 2. Class Imbalance Strategies Evaluated

Our target variable is imbalanced: **26.54% Churn (`1`) vs 73.46% Stayed (`0`)**.

```
                        +-----------------------------------------+
                        |        Imbalance Management Options     |
                        +-----------------------------------------+
                         /                    |                  \
                        /                     |                   \
                       v                      v                    v
          +-----------------------+ +------------------+ +-------------------+
          |  Stratified Splitting | |   Class Weights  | |   SMOTE Sampling  |
          |   (Implemented in     | |(class_weight=    | | (Synthetic Over- |
          |    train_test_split)  | |   'balanced')    | |    sampling)      |
          +-----------------------+ +------------------+ +-------------------+
```

1. **Stratified Splitting (Chosen Implementation):**
   - Preserves natural 26.5% distribution across train and test sets.
   - Prevents artificial distribution distortion during baseline evaluation.
2. **Cost-Sensitive Class Weighting (`class_weight='balanced'`):**
   - Penalizes errors on minority class by multiplying loss by ratio $\frac{N_{\text{samples}}}{2 \times N_{\text{churn}}}$.
   - Significantly increases Recall (to ~75-80%) while dropping Precision (to ~45-50%).
3. **SMOTE Over-sampling:**
   - Synthesizes artificial minority samples in feature space using k-nearest neighbors.
   - Risk: Can create noisy synthetic points along ambiguous decision boundaries in high-dimensional categorical One-Hot space.

---

## 🗄️ 3. Database Selection: SQLite vs. PostgreSQL / Snowflake

- **Why SQLite was selected for this project:**
  - Zero-configuration, serverless, self-contained binary stored in repository (`data/churn.db`).
  - Perfect for single-node web dashboards (Streamlit) executing lightweight analytical SQL queries (<10,000 rows).
- **When to upgrade to PostgreSQL / Snowflake:**
  - If data volume exceeds millions of streaming daily event logs.
  - If multiple concurrent dashboard sessions require parallel write transactions (SQLite locks entire DB file during writes).
  - If advanced analytical windowing or spatial GIS extensions are required.

---

## 💻 4. Dashboard Stack: Streamlit vs. PowerBI / Tableau

- **Why Streamlit was selected:**
  - **Full Code Control:** Native Python code enables embedding Scikit-Learn `Pipeline.predict_proba()` directly inside UI callbacks.
  - **Custom Aesthetics:** Full CSS injection flexibility (`st.markdown`) for dark-mode glassmorphic styling.
  - **Embedded SQL Console:** Allows building interactive query editors and custom web tools impossible in standard BI tools.
- **Trade-off vs Tableau/PowerBI:**
  - Tableau offers non-technical drag-and-drop report creation, but cannot run custom Python ML pipelines on real-time user inputs without complex external server extensions (TabPy).

---

## 🎯 5. Technical Decision Interview Q&A

### Q: Why didn't you select XGBoost or LightGBM for this project?
> **Answer:** *"XGBoost and LightGBM are state-of-the-art gradient boosted tree models. However, for a 7,043-row tabular dataset, Random Forest constrained to `max_depth=8` achieves near-identical ROC-AUC (84.27%) without the risk of gradient overfitting or hyperparameter tuning overhead. For production scaled to millions of rows, LightGBM would be the preferred choice due to histogram-based training speed."*

### Q: If business leaders ask for pure explainability, which model would you deploy?
> **Answer:** *"I would deploy Logistic Regression. It allows presenting exact Odds Ratios to C-suite executives—e.g., 'Switching a customer to a 2-year contract reduces churn risk by 73%'—making business recommendations direct and statistically transparent."*
