# 🤖 Module 05: Machine Learning Models, Metrics Comparison & Serialization

> [!NOTE]
> ML algorithm mechanics, quantitative metrics comparison, coefficient interpretation (odds ratios), and pipeline serialization (`model/train.py`) are core machine learning interview topics.

---

## 🎯 1. Algorithms Evaluated

We trained and evaluated three distinct classification models representing linear, single-tree, and ensemble architecture paradigms:

1. **Logistic Regression (`LogisticRegression(max_iter=1000, random_state=42)`):**
   - Parametric linear classifier that models the log-odds of churn as a linear combination of input features:
     $$\log\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1 x_1 + \dots + \beta_k x_k$$
   - Key Strength: High interpretability via Odds Ratios ($\exp(\beta_i)$).

2. **Decision Tree Classifier (`DecisionTreeClassifier(max_depth=5, random_state=42)`):**
   - Non-parametric recursive splitting model using Gini impurity to construct decision boundaries.
   - Constrained to `max_depth=5` to prevent tree memorization and overfitting.

3. **Random Forest Classifier (`RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)`):**
   - Ensemble bagging method combining 150 decorrelated decision trees built on bootstrap samples with random feature sub-space selection ($\sqrt{k}$ features per split).
   - Constrained to `max_depth=8` to ensure strong generalization.

---

## 📊 2. Model Performance Matrix

Evaluated on the 20% holdout test set (**1,409 customers**):

| Model | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Test ROC-AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | 80.70% | 66.04% | **56.15%** | **60.69%** | 84.22% |
| **Decision Tree** | 79.42% | 63.12% | 54.01% | 58.21% | 82.67% |
| **Random Forest** | **80.34%** | **67.64%** | 49.73% | 57.32% | **84.27%** |

---

## 🔍 3. Evaluation Metrics Explained (Interview Definitions)

- **Accuracy:** Overall proportion of correct predictions:
  $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Precision:** Of all customers predicted to churn, what percentage actually churned?
  $$\text{Precision} = \frac{TP}{TP + FP}$$
  *Business Impact:* High Precision minimizes wasted retention campaign expenditure on false alarms (False Positives).
- **Recall (Sensitivity):** Of all customers who actually churned, what percentage did the model capture?
  $$\text{Recall} = \frac{TP}{TP + FN}$$
  *Business Impact:* High Recall minimizes missed churners (False Negatives), preventing lost monthly recurring revenue.
- **F1-Score:** Harmonic mean of Precision and Recall:
  $$\text{F1} = 2 \times \frac{\text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$
- **ROC-AUC (Receiver Operating Characteristic - Area Under Curve):** Measures the model's ability to rank-order customer churn risk across all possible probability thresholds ($0.0$ to $1.0$).

---

## 📈 4. Explainability: Logistic Regression Odds Ratios

In business presentations, executive stakeholders demand explainability. We extract model coefficients from Logistic Regression and exponentiate them to obtain **Odds Ratios**:

$$\text{Odds Ratio} = e^{\beta_i}$$

```python
# Code snippet from model/train.py
lr_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('classifier', LogisticRegression())])
lr_pipeline.fit(X_train, y_train)

coefficients = lr_pipeline.named_steps['classifier'].coef_[0]
odds_ratios = np.exp(coefficients)
```

### Top Factors Increasing Churn Probability ($\text{Odds Ratio} > 1$):
1. **`internet_service_Fiber optic`** ($\beta = +1.18$, $\text{OR} = \mathbf{3.26}$):
   - Customers with Fiber Optic are **3.26x as likely to churn** (226% risk increase), driven by higher service prices ($70-$100/mo) and competitor switching options.
2. **`payment_method_Electronic check`** ($\beta = +0.38$, $\text{OR} = \mathbf{1.47}$):
   - Electronic check users are **47% more likely to churn** due to manual billing friction compared to auto-pay.
3. **`senior_citizen`** ($\beta = +0.25$, $\text{OR} = \mathbf{1.28}$):
   - Senior citizens have **28% higher odds** of churning.

### Top Factors Decreasing Churn Probability ($\text{Odds Ratio} < 1$):
1. **`contract_Two year`** ($\beta = -1.30$, $\text{OR} = \mathbf{0.27}$):
   - A 2-year contract **reduces churn odds by 73%** ($\text{Risk Reduction} = 1 - 0.27$).
2. **`tenure`** ($\beta = -1.24$, $\text{OR} = \mathbf{0.29}$ per std dev):
   - Each standard deviation unit of tenure **reduces churn odds by 71%**.

---

## 💾 5. Model Serialization Pipeline (`churn_prediction.pkl`)

The best-performing model pipeline based on ROC-AUC (Random Forest) is serialized using `pickle`:

```python
import pickle
import os

model_output_path = os.path.join(base_dir, "churn_prediction.pkl")

# Save complete end-to-end pipeline (Preprocessor + Classifier)
with open(model_output_path, 'wb') as f:
    pickle.dump(best_pipeline, f)
```

> [!TIP]
> **Production Best Practice:** Pickling the entire `Pipeline` object (rather than just the raw model weights) ensures that when `app.py` loads `churn_prediction.pkl`, it automatically executes scaling and one-hot encoding on raw user inputs in a single line: `pipeline.predict_proba(raw_input_df)`.

---

## 🎯 6. Machine Learning Interview Q&A

### Q: Why did Logistic Regression get higher Recall (56.15%) than Random Forest (49.73%) at default threshold 0.5?
> **Answer:** *"Logistic Regression outputs smooth, linear log-odds probabilities that are evenly distributed around the default threshold. Random Forest ensembles tend to produce probability predictions clustered tighter around the base rate (26.5%). At default 0.5 threshold, Random Forest acts more conservatively, boosting Precision (67.64%) at the expense of Recall. By tuning the Random Forest decision threshold down to 0.35, Recall jumps to >70% while preserving high ROC-AUC."*

### Q: How would you improve model performance further if given another sprint?
> **Answer:** *"I would implement XGBoost/LightGBM with hyperparameter optimization via `Optuna`, apply SMOTE (Synthetic Minority Over-sampling Technique) to balance training classes, and perform threshold tuning using a cost-matrix function that weights False Negatives ($74 monthly revenue loss) against False Positives ($10 retention campaign credit)."*
