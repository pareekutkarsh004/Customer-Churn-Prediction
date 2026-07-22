import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
import os
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------------------
# App Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title="Telco Churn Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------------
# Premium Dark Theme Custom CSS Injection
# -------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');

/* Global Font Settings */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
    color: #E2E8F0;
}

/* Background Color */
.main {
    background-color: #0F172A;
    background-image: radial-gradient(circle at 10% 20%, rgba(30, 41, 59, 0.4) 0%, rgba(15, 23, 42, 0.9) 100%);
}

/* Sidebar Custom Styling */
section[data-testid="stSidebar"] {
    background-color: #0B0F19;
    border-right: 1px solid rgba(255, 255, 255, 0.05);
}

/* Glassmorphic Metrics Card Styling */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 20px;
    margin-bottom: 25px;
}

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

.kpi-title {
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: #94A3B8;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 34px;
    font-weight: 700;
    margin: 5px 0;
    letter-spacing: -0.5px;
}

.val-default {
    background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.val-red {
    background: linear-gradient(135deg, #FF3B30 0%, #FF7B72 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.val-purple {
    background: linear-gradient(135deg, #8B5CF6 0%, #C084FC 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.val-cyan {
    background: linear-gradient(135deg, #06B6D4 0%, #67E8F9 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Metric Subtext */
.kpi-subtext {
    font-size: 12px;
    color: #64748B;
    margin-top: 4px;
}

/* Styled Section Header */
.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 24px;
    font-weight: 700;
    color: #F8FAFC;
    margin-top: 20px;
    margin-bottom: 20px;
    border-left: 4px solid #8B5CF6;
    padding-left: 12px;
}

/* Predictor recommendation cards */
.rec-box {
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 12px;
    padding: 16px;
    margin-top: 10px;
}

.rec-title {
    color: #34D399;
    font-weight: 600;
    margin-bottom: 8px;
    font-size: 15px;
}

.risk-high {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #FCA5A5;
    border-radius: 8px;
    padding: 12px;
    font-weight: 600;
    text-align: center;
}

.risk-medium {
    background: rgba(245, 158, 11, 0.15);
    border: 1px solid rgba(245, 158, 11, 0.3);
    color: #FCD34D;
    border-radius: 8px;
    padding: 12px;
    font-weight: 600;
    text-align: center;
}

.risk-low {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #6EE7B7;
    border-radius: 8px;
    padding: 12px;
    font-weight: 600;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------
@st.cache_data
def load_cleaned_data():
    df = pd.read_csv("data/customer_churn_cleaned.csv")
    return df

def run_query(query):
    conn = sqlite3.connect("data/churn.db")
    try:
        result_df = pd.read_sql_query(query, conn)
        return result_df
    except Exception as e:
        return str(e)
    finally:
        conn.close()

# Load Dataset
try:
    df_clean = load_cleaned_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}. Please ensure data collection and cleaning runs first.")
    df_clean = pd.DataFrame()

# Load ML Model
model_pipeline = None
if os.path.exists("model/churn_prediction.pkl"):
    try:
        with open("model/churn_prediction.pkl", "rb") as f:
            model_pipeline = pickle.load(f)
    except Exception as e:
        st.warning(f"Error loading ML model: {e}")
else:
    st.info("Predictive model pickle file not found. Prediction tab will run in demonstration mode.")

# -------------------------------------------------------------
# Sidebar Navigation
# -------------------------------------------------------------
st.sidebar.markdown(
    "<h2 style='text-align: center; font-family: Space Grotesk; background: linear-gradient(135deg, #8B5CF6 0%, #EC4899 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>ChurnInsight</h2>", 
    unsafe_allow_html=True
)
st.sidebar.markdown("<p style='text-align: center; color: #64748B; font-size: 13px; margin-top: -10px;'>Telecom Retention Strategy Platform</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "Navigation Menu",
    ["📊 Executive Dashboard", "🔮 Churn Risk Predictor", "💻 SQL Business Console"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📈 Project Overview")
st.sidebar.info(
    "This platform helps analyze why customers are leaving, segments customer risk, "
    "and offers recommendations using SQL Analytics & Machine Learning (Random Forest)."
)

# -------------------------------------------------------------
# PAGE 1: EXECUTIVE DASHBOARD
# -------------------------------------------------------------
if menu == "📊 Executive Dashboard":
    st.markdown("<h1 style='font-family: Space Grotesk; font-weight: 700; margin-bottom: 5px;'>Executive Retention Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 25px;'>Monitor key churn KPIs, analyze risk drivers, and identify customer churn segments.</p>", unsafe_allow_html=True)
    
    if not df_clean.empty:
        # Sidebar filters for dashboard interactivity
        st.sidebar.markdown("### 🔍 Dashboard Filters")
        contract_filter = st.sidebar.multiselect("Contract Type", options=df_clean['contract'].unique(), default=df_clean['contract'].unique())
        payment_filter = st.sidebar.multiselect("Payment Method", options=df_clean['payment_method'].unique(), default=df_clean['payment_method'].unique())
        internet_filter = st.sidebar.multiselect("Internet Service", options=df_clean['internet_service'].unique(), default=df_clean['internet_service'].unique())
        
        # Apply filters to data
        filtered_df = df_clean[
            (df_clean['contract'].isin(contract_filter)) &
            (df_clean['payment_method'].isin(payment_filter)) &
            (df_clean['internet_service'].isin(internet_filter))
        ]
        
        # Calculate dynamic KPIs based on filters
        total_cust = len(filtered_df)
        churned_cust = len(filtered_df[filtered_df['churn'] == 'Yes'])
        churn_rate = (churned_cust / total_cust * 100) if total_cust > 0 else 0.0
        
        revenue_lost = filtered_df[filtered_df['churn'] == 'Yes']['monthly_charges'].sum()
        avg_tenure = filtered_df['tenure'].mean() if total_cust > 0 else 0.0
        
        # HTML template for premium metric cards
        st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-card">
                <div class="kpi-title">Total Customers</div>
                <div class="kpi-value val-default">{total_cust:,}</div>
                <div class="kpi-subtext">Active & Churned portfolio</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Churn Rate</div>
                <div class="kpi-value val-red">{churn_rate:.2f}%</div>
                <div class="kpi-subtext">Industry Avg: ~15-20%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Monthly Revenue Lost</div>
                <div class="kpi-value val-purple">${revenue_lost:,.2f}</div>
                <div class="kpi-subtext">From churned customers</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Avg Tenure</div>
                <div class="kpi-value val-cyan">{avg_tenure:.1f} mos</div>
                <div class="kpi-subtext">Customer lifetime duration</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Grid layout for charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<div class='section-header'>Overall Churn Distribution</div>", unsafe_allow_html=True)
            if total_cust > 0:
                fig_pie = px.pie(
                    filtered_df, 
                    names='churn', 
                    title="Stayed (No Churn) vs. Left (Churned)",
                    color='churn',
                    color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                    hole=0.4
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E2E8F0',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            else:
                st.warning("No data matches current filters.")
                
        with col2:
            st.markdown("<div class='section-header'>Churn Rate by Contract Type</div>", unsafe_allow_html=True)
            if total_cust > 0:
                contract_counts = filtered_df.groupby('contract')['churn'].value_counts(normalize=True).rename('percentage').reset_index()
                contract_counts['percentage'] *= 100
                fig_contract = px.bar(
                    contract_counts,
                    x='contract',
                    y='percentage',
                    color='churn',
                    barmode='group',
                    title='Churn Percentage within Contract Lengths',
                    labels={'percentage': 'Percentage (%)', 'contract': 'Contract Type', 'churn': 'Churn Status'},
                    color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'}
                )
                fig_contract.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E2E8F0',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_contract, use_container_width=True)
            else:
                st.warning("No data matches current filters.")
                
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown("<div class='section-header'>Customer Distribution by Tenure & Churn</div>", unsafe_allow_html=True)
            if total_cust > 0:
                fig_tenure = px.histogram(
                    filtered_df,
                    x='tenure',
                    color='churn',
                    marginal='box',
                    title='Tenure Distribution (Months)',
                    labels={'tenure': 'Tenure (Months)', 'count': 'Number of Customers', 'churn': 'Churn Status'},
                    color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                    barmode='overlay',
                    opacity=0.6
                )
                fig_tenure.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E2E8F0',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_tenure, use_container_width=True)
            else:
                st.warning("No data matches current filters.")
                
        with col4:
            st.markdown("<div class='section-header'>Churn Rate by Payment Method</div>", unsafe_allow_html=True)
            if total_cust > 0:
                pm_counts = filtered_df.groupby('payment_method')['churn'].value_counts(normalize=True).rename('percentage').reset_index()
                pm_counts['percentage'] *= 100
                fig_pm = px.bar(
                    pm_counts,
                    y='payment_method',
                    x='percentage',
                    color='churn',
                    barmode='group',
                    title='Churn Percentage by Payment Category',
                    labels={'percentage': 'Percentage (%)', 'payment_method': 'Payment Method', 'churn': 'Churn Status'},
                    color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'},
                    orientation='h'
                )
                fig_pm.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E2E8F0',
                    legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_pm, use_container_width=True)
            else:
                st.warning("No data matches current filters.")

        # Additional interactive row for services
        st.markdown("<div class='section-header'>Churn Drivers: Core Support & Security Services</div>", unsafe_allow_html=True)
        col5, col6, col7 = st.columns(3)
        
        services_list = [
            ('tech_support', 'Tech Support Churn', col5),
            ('online_security', 'Online Security Churn', col6),
            ('online_backup', 'Online Backup Churn', col7)
        ]
        
        for col_name, title_lbl, column in services_list:
            with column:
                counts = filtered_df.groupby(col_name)['churn'].value_counts(normalize=True).rename('percentage').reset_index()
                counts['percentage'] *= 100
                fig_srv = px.bar(
                    counts,
                    x=col_name,
                    y='percentage',
                    color='churn',
                    barmode='group',
                    title=title_lbl,
                    labels={'percentage': 'Percentage (%)', col_name: 'Subscription Status'},
                    color_discrete_map={'No': '#10B981', 'Yes': '#EF4444'}
                )
                fig_srv.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color='#E2E8F0',
                    showlegend=False
                )
                st.plotly_chart(fig_srv, use_container_width=True)

    else:
        st.info("Empty dataset. Please load the customer data to display the analytics dashboard.")

# -------------------------------------------------------------
# PAGE 2: CHURN RISK PREDICTOR
# -------------------------------------------------------------
elif menu == "🔮 Churn Risk Predictor":
    st.markdown("<h1 style='font-family: Space Grotesk; font-weight: 700; margin-bottom: 5px;'>Predictive Churn Risk Assessment</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 25px;'>Input customer attributes to estimate churn probability and view proactive mitigation strategies.</p>", unsafe_allow_html=True)
    
    if model_pipeline is None:
        st.error("⚠️ Predictive model pipeline pickle not found! Please run the training script `python3 model/train.py` in the workspace to serialize the model.")
    else:
        st.markdown("<div class='section-header'>Customer Profile Input Form</div>", unsafe_allow_html=True)
        
        # Multi-column form layout
        with st.form("churn_form"):
            col_left, col_mid, col_right = st.columns(3)
            
            with col_left:
                st.subheader("👤 Demographics")
                gender = st.selectbox("Gender", ["Female", "Male"])
                senior_citizen = st.selectbox("Senior Citizen (Age >= 65)", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
                partner = st.selectbox("Has Partner", ["Yes", "No"])
                dependents = st.selectbox("Has Dependents", ["Yes", "No"])
                
            with col_mid:
                st.subheader("📄 Contract & Billing")
                tenure = st.slider("Tenure (Months with company)", min_value=0, max_value=72, value=12)
                contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
                paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
                payment_method = st.selectbox(
                    "Payment Method", 
                    ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"]
                )
                monthly_charges = st.number_input("Monthly Charges ($)", min_value=15.0, max_value=120.0, value=70.0, step=1.0)
                # Estimate TotalCharges as monthly_charges * tenure or let user change
                estimated_total = monthly_charges * tenure
                total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=8500.0, value=estimated_total, step=50.0)
                
            with col_right:
                st.subheader("🔌 Services Subscribed")
                phone_service = st.selectbox("Phone Service", ["Yes", "No"])
                multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
                internet_service = st.selectbox("Internet Service Type", ["Fiber optic", "DSL", "No"])
                
                # Check internet status for security services
                has_internet = internet_service != "No"
                sec_opts = ["No", "Yes"] if has_internet else ["No internet service"]
                
                online_security = st.selectbox("Online Security Service", sec_opts)
                online_backup = st.selectbox("Online Backup Service", sec_opts)
                device_protection = st.selectbox("Device Protection Service", sec_opts)
                tech_support = st.selectbox("Tech Support Service", sec_opts)
                streaming_tv = st.selectbox("Streaming TV", sec_opts)
                streaming_movies = st.selectbox("Streaming Movies", sec_opts)
                
            # Submit Button
            submitted = st.form_submit_button("🔍 Run Churn Assessment")
            
        if submitted:
            # Build input dictionary
            input_dict = {
                'gender': gender,
                'senior_citizen': int(senior_citizen),
                'partner': partner,
                'dependents': dependents,
                'tenure': int(tenure),
                'phone_service': phone_service,
                'multiple_lines': multiple_lines,
                'internet_service': internet_service,
                'online_security': online_security,
                'online_backup': online_backup,
                'device_protection': device_protection,
                'tech_support': tech_support,
                'streaming_tv': streaming_tv,
                'streaming_movies': streaming_movies,
                'contract': contract,
                'paperless_billing': paperless_billing,
                'payment_method': payment_method,
                'monthly_charges': float(monthly_charges),
                'total_charges': float(total_charges)
            }
            
            # Convert to Dataframe for Scikit-Learn
            input_df = pd.DataFrame([input_dict])
            
            # Predict Churn probability
            try:
                prob = model_pipeline.predict_proba(input_df)[0][1]
                churn_prediction = model_pipeline.predict(input_df)[0]
                
                # Layout results
                res_col1, res_col2 = st.columns([1, 2])
                
                with res_col1:
                    st.markdown("<div class='section-header'>Assessment Output</div>", unsafe_allow_html=True)
                    
                    # Risk Classification
                    if prob >= 0.6:
                        st.markdown("<div class='risk-high'>🚨 HIGH CHURN RISK</div>", unsafe_allow_html=True)
                    elif prob >= 0.3:
                        st.markdown("<div class='risk-medium'>⚠️ MEDIUM CHURN RISK</div>", unsafe_allow_html=True)
                    else:
                        st.markdown("<div class='risk-low'>✅ LOW CHURN RISK</div>", unsafe_allow_html=True)
                        
                    # Circular Gauge for risk probability
                    fig_gauge = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = prob * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Churn Probability", 'font': {'size': 18, 'color': '#E2E8F0'}},
                        gauge = {
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#E2E8F0"},
                            'bar': {'color': "#8B5CF6"},
                            'bgcolor': "rgba(30, 41, 59, 0.4)",
                            'borderwidth': 2,
                            'bordercolor': "rgba(255, 255, 255, 0.1)",
                            'steps': [
                                {'range': [0, 30], 'color': 'rgba(16, 185, 129, 0.15)'},
                                {'range': [30, 60], 'color': 'rgba(245, 158, 11, 0.15)'},
                                {'range': [60, 100], 'color': 'rgba(239, 68, 68, 0.15)'}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 60
                            }
                        }
                    ))
                    fig_gauge.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        font={'color': "#E2E8F0", 'family': "Outfit"},
                        height=250,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig_gauge, use_container_width=True)
                    
                with res_col2:
                    st.markdown("<div class='section-header'>Automated Retention Recommendations</div>", unsafe_allow_html=True)
                    
                    st.markdown(f"**Customer Profile Summary:** Tenure: `{tenure}` months | Contract Type: `{contract}` | Billing: `${monthly_charges}/mo` | Payment: `{payment_method}`")
                    
                    # Core Retention Rules
                    recommendations = []
                    
                    if contract == "Month-to-month":
                        recommendations.append(
                            "**Migrate to Long-Term Commitment:** Month-to-month contracts are the #1 churn driver. "
                            "Target this customer with an incentive (e.g., offer $10/month off for 12 months) to convert "
                            "them to a 1-Year or 2-Year Contract. This reduces churn probability by up to 75%."
                        )
                        
                    if payment_method == "Electronic check":
                        recommendations.append(
                            "**Auto-Pay Enrollment Incentive:** Paying via electronic check causes billing friction. "
                            "Provide a one-time $15 bill credit if they enroll in automatic credit card or bank transfer pay."
                        )
                        
                    if internet_service == "Fiber optic" and online_security == "No":
                        recommendations.append(
                            "**Value-Added Services Bundle:** Customer is on high-speed Fiber Optic but has no Online Security. "
                            "Secure their subscription by bundling 6 months of free Online Security and Tech Support add-ons."
                        )
                        
                    if tenure <= 6:
                        recommendations.append(
                            "**Early Lifecycle Nurturing:** Customer is in their first 6 months (the high-risk onboarding zone). "
                            "Schedule a proactive customer success call to verify satisfaction, offer setup assistance, or check device compatibility."
                        )
                        
                    if monthly_charges > 75.0 and tenure < 24:
                        recommendations.append(
                            "**Price Sensitivity Promotion:** This high-value customer has high monthly bills and moderate tenure. "
                            "Offer a loyalty bundle or downgrade option to a slightly cheaper plan that fits their needs "
                            "better rather than risk losing their entire contract."
                        )
                        
                    if len(recommendations) == 0:
                        st.success("This customer shows very low churn risk factors! Continue with standard service campaigns.")
                    else:
                        for rec in recommendations:
                            st.markdown(f"""
                            <div class="rec-box">
                                <div class="rec-title">🎯 Targeted Retention Action</div>
                                <div style="font-size: 14px; line-height: 1.5; color: #CBD5E1;">{rec}</div>
                            </div>
                            """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Prediction failed: {e}")

# -------------------------------------------------------------
# PAGE 3: SQL BUSINESS CONSOLE
# -------------------------------------------------------------
elif menu == "💻 SQL Business Console":
    st.markdown("<h1 style='font-family: Space Grotesk; font-weight: 700; margin-bottom: 5px;'>SQL Business Analysis Console</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #94A3B8; font-size: 16px; margin-bottom: 25px;'>Run SQL business intelligence queries directly against the customer database.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>Select Business Analysis Query</div>", unsafe_allow_html=True)
    
    # Pre-configured queries
    queries = {
        "1. Overall Churn Count & Rate": """-- Overall Customer Churn Ratio
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate_percent
FROM customers;""",

        "2. Churn by Contract Length": """-- Contract Duration vs. Churn Behavior
SELECT 
    contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY contract
ORDER BY churn_rate DESC;""",

        "3. Average Revenue Lost in Billing": """-- Average Billing Comparison and Revenue Loss
SELECT 
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN churn = 'Yes' THEN monthly_charges ELSE 0 END), 2) AS total_monthly_revenue_lost,
    ROUND(AVG(CASE WHEN churn = 'Yes' THEN monthly_charges END), 2) AS avg_monthly_bill_churned,
    ROUND(AVG(CASE WHEN churn = 'No' THEN monthly_charges END), 2) AS avg_monthly_bill_active
FROM customers;""",

        "4. Top 10 High-Risk Customer Segments": """-- High Churn Customer Demographics & Packages
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
LIMIT 10;""",

        "5. Churn Rate by Tenure Cohort": """-- Customer Age brackets vs Churn Probability
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
ORDER BY tenure_cohort;""",

        "6. Churn and Utility Security Services": """-- Influence of Value Added Security & Support Services on Churn
SELECT 
    tech_support,
    online_security,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(CAST(SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 2) AS churn_rate
FROM customers
GROUP BY tech_support, online_security
ORDER BY churn_rate DESC;"""
    }
    
    selected_query_name = st.selectbox("Choose pre-loaded SQL query", list(queries.keys()))
    
    # Custom editor containing selected query text
    query_text = st.text_area("SQL Editor (Make changes or write your own query here)", queries[selected_query_name], height=180)
    
    # Run query button
    if st.button("⚡ Run Query"):
        with st.spinner("Executing SQL query on SQLite database..."):
            res = run_query(query_text)
            
            if isinstance(res, pd.DataFrame):
                st.success("Query executed successfully!")
                st.dataframe(res, use_container_width=True)
                
                # Download as CSV button
                csv_data = res.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Results as CSV",
                    data=csv_data,
                    file_name="churn_query_results.csv",
                    mime="text/csv"
                )
            else:
                st.error(f"SQL Execution Error: {res}")
