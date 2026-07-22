import pandas as pd
import numpy as np
import pickle
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report

def run_ml_pipeline():
    data_path = "data/customer_churn_cleaned.csv"
    model_dir = "model"
    model_output_path = os.path.join(model_dir, "churn_prediction.pkl")
    
    print("Loading cleaned dataset...")
    df = pd.read_csv(data_path)
    
    # Define Target and Features
    target = 'churn'
    # Drop customer_id as it is an identifier, and target
    X = df.drop(columns=['customer_id', target])
    y = df[target].map({'Yes': 1, 'No': 0})
    
    # Identify numerical and categorical features
    numerical_cols = ['tenure', 'monthly_charges', 'total_charges', 'senior_citizen']
    categorical_cols = [col for col in X.columns if col not in numerical_cols]
    
    print(f"Features list - Categorical: {len(categorical_cols)}, Numerical: {len(numerical_cols)}")
    
    # Train-test split
    # Stratify to ensure same churn ratio in train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Train set size: {X_train.shape[0]}, Test set size: {X_test.shape[0]}")
    
    # Define Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numerical_cols),
            ('cat', OneHotEncoder(drop='first', handle_unknown='ignore'), categorical_cols)
        ]
    )
    
    # Define Models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(max_depth=5, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=150, max_depth=8, random_state=42)
    }
    
    best_roc_auc = 0.0
    best_pipeline = None
    best_model_name = ""
    results = {}
    
    print("\nTraining and evaluating models...")
    for name, clf in models.items():
        # Build training pipeline
        pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', clf)
        ])
        
        # Fit model
        pipeline.fit(X_train, y_train)
        
        # Predict
        y_pred = pipeline.predict(X_test)
        y_prob = pipeline.predict_proba(X_test)[:, 1]
        
        # Evaluate
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob)
        
        results[name] = {
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1-Score': f1,
            'ROC-AUC': auc
        }
        
        print(f"\n=== {name} Metrics ===")
        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1-Score : {f1:.4f}")
        print(f"ROC-AUC  : {auc:.4f}")
        
        # Track the best model based on ROC-AUC
        if auc > best_roc_auc:
            best_roc_auc = auc
            best_pipeline = pipeline
            best_model_name = name
            
    print(f"\nBest Model selected: {best_model_name} with ROC-AUC = {best_roc_auc:.4f}")
    
    # Save the best model pipeline
    print(f"Saving best model pipeline to: {model_output_path}...")
    with open(model_output_path, 'wb') as f:
        pickle.dump(best_pipeline, f)
    
    print("Model serialized successfully!")
    
    # -------------------------------------------------------------
    # Logistic Regression Coeffs Interpretation (explainability bonus)
    # -------------------------------------------------------------
    if 'Logistic Regression' in models:
        lr_pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', models['Logistic Regression'])
        ]).fit(X_train, y_train)
        
        # Extract feature names after transformer
        ohe_features = lr_pipeline.named_steps['preprocessor'].named_transformers_['cat'].get_feature_names_out(categorical_cols)
        all_features = numerical_cols + list(ohe_features)
        coefficients = lr_pipeline.named_steps['classifier'].coef_[0]
        
        coef_df = pd.DataFrame({
            'Feature': all_features,
            'Coefficient': coefficients,
            'Odds_Ratio': np.exp(coefficients)
        }).sort_values(by='Coefficient', ascending=False)
        
        print("\n=== Logistic Regression Feature Influence (Top 5 Positive & Negative) ===")
        print("\nFactors increasing churn probability (Positive coefficients):")
        print(coef_df.head(5).to_string(index=False))
        
        print("\nFactors reducing churn probability (Negative coefficients):")
        print(coef_df.tail(5).to_string(index=False))

if __name__ == "__main__":
    run_ml_pipeline()
