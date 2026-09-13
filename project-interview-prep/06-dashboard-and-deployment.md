# 🖥️ Module 06: Streamlit Web Dashboard, UX Architecture & Deployment

> [!NOTE]
> Presenting data models through production web applications demonstrates full-stack data capabilities. This module details the design, layout, styling, and interactive features of `app.py`.

---

## 🎯 1. Application Architecture Overview

The web dashboard is built using **Streamlit**, **Plotly**, and custom **CSS** injection. It consists of **3 main functional pages** managed via a sidebar navigation router:

1. **📊 Executive Dashboard Page:** High-level executive KPI metrics, interactive global filters, and multi-dimensional Plotly charts.
2. **🔮 Churn Risk Predictor Page:** Form input simulator that passes real-time customer profiles through `churn_prediction.pkl`, renders a Plotly circular risk gauge, and generates targeted retention campaigns based on rule logic.
3. **💻 SQL Business Console Page:** Live query execution interface with 6 pre-loaded business queries, custom SQL code editor, SQLite execution engine, and CSV export functionality.

---

## 🎨 2. UI/UX & Glassmorphism Design Tokens

To deliver a premium visual impression, `app.py` injects custom CSS for dark mode glassmorphism aesthetics, modern typography, and responsive grid layouts:

```css
/* Glassmorphism Metric Cards */
.kpi-card {
    background: rgba(30, 41, 59, 0.45);
    backdrop-filter: blur(12px) saturate(180%);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

.kpi-card:hover {
    transform: translateY(-5px);
    border-color: rgba(124, 58, 237, 0.45);
    box-shadow: 0 12px 30px 0 rgba(124, 58, 237, 0.15);
}
```

### Key Aesthetic Elements:
- **Typography:** Custom Google Fonts imported: `'Outfit'` for body copy and `'Space Grotesk'` for section headers.
- **Color Palette:** Slate Dark (`#0F172A`), Purple Accents (`#8B5CF6`), Emerald Green (`#10B981` for active/low risk), Coral Red (`#EF4444` for churn/high risk).
- **Micro-Interactions:** CSS hover transformations (`translateY(-5px)`), dynamic border glow, responsive glassmorphic cards.

---

## 🔮 3. Interactive Risk Assessment Predictor Logic

When a user submits a customer profile on the **Churn Risk Predictor** page:

1. **Input Payload Structuring:** Collects demographics, billing choices, and service selections into a single-row Pandas DataFrame.
2. **Model Inference:**
   ```python
   prob = model_pipeline.predict_proba(input_df)[0][1] # Probability of Churn (class 1)
   ```
3. **Risk Tier Assignment:**
   - **`prob >= 0.60`:** 🚨 **HIGH CHURN RISK** (Red Alert Badge)
   - **`0.30 <= prob < 0.60`:** ⚠️ **MEDIUM CHURN RISK** (Amber Warning Badge)
   - **`prob < 0.30`:** ✅ **LOW CHURN RISK** (Green Success Badge)
4. **Plotly Gauge Rendering:** Renders a interactive circular gauge chart (`go.Indicator`) visualizing probability percentage with threshold zones.
5. **Rule-Based Retention Action Generator:** Evaluates profile attributes to output concrete intervention strategies:
   - *If `contract == "Month-to-month"`* $\rightarrow$ **Migrate to 12-Month Contract** (Offer $10/mo credit).
   - *If `payment_method == "Electronic check"`* $\rightarrow$ **Auto-Pay Incentive** (Offer $15 bill credit).
   - *If `internet_service == "Fiber optic"` and `online_security == "No"`* $\rightarrow$ **Bundle Free Security & Support for 6 Mos**.
   - *If `tenure <= 6`* $\rightarrow$ **Trigger Early Onboarding Success Touchpoint**.

---

## 💻 4. SQL Business Console Component

The **SQL Business Console** allows non-technical business users or SQL interviewers to execute live SQL queries against `churn.db`:

```python
def run_query(query):
    db_path = os.path.join(os.path.dirname(__file__), "data", "churn.db")
    conn = sqlite3.connect(db_path)
    try:
        result_df = pd.read_sql_query(query, conn)
        return result_df
    except Exception as e:
        return str(e)
    finally:
        conn.close()
```

### Features:
- Dropdown pre-loaded with all 6 business analysis queries from `sql/churn_analysis.sql`.
- Interactive multi-line SQL code editor (`st.text_area`) allowing on-the-fly SQL modification.
- Live rendering into interactive Pandas data tables (`st.dataframe`).
- Instant CSV export download button (`st.download_button`).

---

## 🚀 5. How to Run & Deploy

```bash
# 1. Install Dependencies
pip install pandas numpy scikit-learn matplotlib seaborn streamlit plotly

# 2. Run Database Setup
python3 data/db_setup.py

# 3. Train & Serialize Model
python3 model/train.py

# 4. Launch Streamlit Web App
streamlit run app.py
```

---

## 🎯 6. Dashboard & Deployment Interview Q&A

### Q: How did you optimize application latency in Streamlit?
> **Answer:** *"I utilized Streamlit's `@st.cache_data` decorator on data loading functions (`load_cleaned_data()`). This caches the loaded CSV dataset in memory after initial execution, reducing page load latency from ~1.2 seconds down to under 50 milliseconds upon user re-renders."*

### Q: How would you deploy this Streamlit app to production for enterprise users?
> **Answer:** *"I would containerize the app using Docker (`Dockerfile`), deploy the container to AWS ECS (Elastic Container Service) or Kubernetes (EKS) behind an Application Load Balancer (ALB), and implement OAuth2 / SAML authentication via Streamlit credentials or AWS Cognito."*
