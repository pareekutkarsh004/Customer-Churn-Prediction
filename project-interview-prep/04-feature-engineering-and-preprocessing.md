# ⚙️ Module 04: Feature Engineering, Preprocessing & Data Leakage Prevention

> [!NOTE]
> ML data pipelines require strict modular preprocessing to prevent target leakage and handle categorical/numerical features. This module covers `ColumnTransformer`, `StandardScaler`, `OneHotEncoder`, and stratification strategy in `model/train.py`.

---

## 🎯 1. Feature Breakdown & Data Typing

Features are partitioned into target, numerical predictors, and categorical predictors:

### Target Variable:
- **`churn`**: Converted from string (`'Yes'`/`'No'`) to binary integers (`1` = Churned, `0` = Stayed).

### Excluded Attributes:
- **`customer_id`**: Dropped prior to model fitting as it is a unique primary key identifier that holds zero predictive signal and would cause memorization/overfitting.

### Numerical Features (4 attributes):
- `tenure` (Integer months: 0 to 72)
- `monthly_charges` (Float dollars: $18.25 to $118.75)
- `total_charges` (Float cumulative dollars: $0.0 to $8684.8)
- `senior_citizen` (Binary flag: 0 or 1)

### Categorical Features (15 attributes):
`gender`, `partner`, `dependents`, `phone_service`, `multiple_lines`, `internet_service`, `online_security`, `online_backup`, `device_protection`, `tech_support`, `streaming_tv`, `streaming_movies`, `contract`, `paperless_billing`, `payment_method`.

---

## ⚙️ 2. Scikit-Learn Preprocessing Pipeline (`ColumnTransformer`)

To transform raw data into a numerical matrix ready for machine learning algorithms, we construct a Scikit-Learn `ColumnTransformer`:

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

numerical_cols = ['tenure', 'monthly_charges', 'total_charges', 'senior_citizen']
categorical_cols = [col for col in X.columns if col not in numerical_cols]

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_cols),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols)
    ]
)
```

### Technical Design Decisions:

1. **`StandardScaler()` for Numerical Columns:**
   - **Formula:** $z = \frac{x - \mu}{\sigma}$
   - **Why?** Logistic Regression utilizes gradient-based optimization ($\text{L2}$ regularization penalty). Features with large raw scales (e.g., `total_charges` up to $8,684 vs. `senior_citizen` at 0/1) would dominate gradient updates and bias coefficient weights without standard scaling to zero mean and unit variance.

2. **`OneHotEncoder(drop='first')` for Categorical Columns:**
   - **Why `drop='first'`?** For binary categorical variables (e.g., `gender`: Female/Male), creating 2 dummy columns introduces perfect linear dependence ($\text{Female} + \text{Male} = 1$). Dropping the first category prevents the **Dummy Variable Trap** (multicollinearity), which makes matrix inversion $(\mathbf{X}^T\mathbf{X})^{-1}$ unstable in linear models.
   - **`handle_unknown='ignore'`:** Ensures that if unseen categorical levels appear during production inference, the encoder transforms them into all zeros instead of raising a runtime `ValueError`.

---

## 🛡️ 3. Data Leakage Prevention Strategy

Data leakage occurs when information from the test dataset or target label unintentionally influences model training preprocessing, leading to overly optimistic test performance that fails in production.

```
                           +----------------------------------------+
                           |       Full Dataset (7,043 rows)        |
                           +----------------------------------------+
                                                |
                                    train_test_split(stratify=y)
                                                |
                      +-------------------------+-------------------------+
                      |                                                   |
                      v                                                   v
           +----------------------+                            +----------------------+
           | Training Set (80%)   |                            |   Test Holdout (20%) |
           |  (5,634 rows)        |                            |    (1,409 rows)      |
           +----------------------+                            +----------------------+
                      |                                                   |
             fit_transform()                                          transform()
                      |                                                   |
                      v                                                   v
           Scaled Train Matrix                                 Scaled Test Matrix
```

### Prevention Protocol Implemented:
1. **Split First, Preprocess Second:** `train_test_split()` is called BEFORE fitting any scaler or encoder.
2. **`Pipeline` Encapsulation:** By placing `preprocessor` inside a Scikit-Learn `Pipeline(steps=[('preprocessor', preprocessor), ('classifier', model)])`, calling `pipeline.fit(X_train, y_train)` fits parameters ($\mu, \sigma$, categories) **strictly on `X_train`**.
3. **`transform()` on Holdout:** Calling `pipeline.predict(X_test)` applies the exact training $\mu$ and $\sigma$ parameters to scale `X_test`, ensuring zero test data leakage.

---

## ⚖️ 4. Stratified Split Rationale

- **Dataset Class Balance:** 73.46% Non-Churn (`0`) vs 26.54% Churn (`1`).
- **Code:**
  ```python
  X_train, X_test, y_train, y_test = train_test_split(
      X, y, test_size=0.2, random_state=42, stratify=y
  )
  ```
- **Why `stratify=y`?** A standard random split on an imbalanced dataset might accidentally assign 30% churners to the training set and only 15% to the test set. Stratification guarantees both train (`5,634` rows) and test (`1,409` rows) holdouts maintain the exact **26.54% target churn ratio**.

---

## 🎯 5. Feature Engineering Interview Q&A

### Q: Why didn't you use LabelEncoding for categorical columns like `contract`?
> **Answer:** *"LabelEncoding converts categories into arbitrary ordinal integers (e.g., Month-to-month=0, One year=1, Two year=2). Algorithms like Logistic Regression or Random Forest interpret higher numerical values as higher magnitudes (2 > 0), imposing an artificial linear distance. One-Hot Encoding creates independent binary indicator vectors, preventing false ordinal assumptions."*

### Q: How would you handle high-cardinality categorical features if you added Zip Codes?
> **Answer:** *"For high-cardinality attributes like 5-digit Zip Codes (thousands of categories), One-Hot Encoding creates extreme matrix sparsity and high dimensionality. I would use Target Encoding (Mean Target Probability per Zip Code) with smoothing, or Feature Hashing (Hashing Trick) to map categories into fixed dimensions."*
