# 💰 Module 08: Business Impact, Retention Strategy & Financial ROI Modeling

> [!NOTE]
> Demonstrating commercial awareness and translating model outputs into quantified business ROI is what separates top-tier Data Scientists and Analysts in executive interviews.

---

## 📉 1. The Cost of Inaction (Current State)

From our SQL database analysis (`sql/churn_analysis.sql`):
- **Annualized Revenue Lost to Churn:**
  $$\text{Annual Lost Revenue} = \$139,130.85 \text{ / month} \times 12 \text{ months} = \mathbf{\$1,669,570.20 \text{ / year}}$$
- **High-Risk Segment Concentration:**
  - **1,307 subscribers** belong to the *Month-to-month + Fiber Optic + Electronic Check* segment.
  - **789 churned** (60.37% churn rate), resulting in **$63,120 per month in lost revenue** from this single segment alone.

---

## 🎯 2. Top 4 Actionable Retention Campaigns

Based on exploratory data analysis, Logistic Regression odds ratios, and machine learning risk scoring, we formulate 4 targeted, data-backed retention initiatives:

```
+-----------------------------------------------------------------------------------+
|                        TOP 4 RETENTION INITIATIVES                                |
+-----------------------------------------------------------------------------------+
| 1. Promotional Contract Migration Campaign                                         |
|    Target: Month-to-Month subscribers (42.71% churn rate)                        |
|    Action: $10/month contract credit for upgrading to 12-month commitment        |
+-----------------------------------------------------------------------------------+
| 2. Auto-Pay Enrollment Campaign                                                   |
|    Target: Electronic Check users (45.29% churn rate)                             |
|    Action: One-time $15 bill credit for switching to automatic card/bank pay      |
+-----------------------------------------------------------------------------------+
| 3. Early Onboarding Success Milestones                                            |
|    Target: Subscribers in Months 0-6 (52.9% churn rate)                           |
|    Action: Automated check-in calls & setup support at Months 1, 3, and 5         |
+-----------------------------------------------------------------------------------+
| 4. Security & Tech Support Bundling                                               |
|    Target: Fiber Optic users without security add-ons (48.91% churn rate)         |
|    Action: Bundle free Online Security & Tech Support into core broadband plans   |
+-----------------------------------------------------------------------------------+
```

---

## 💡 3. Campaign Deep Dives & Mechanics

### Campaign 1: Promotional Contract Migration
- **Data Finding:** Month-to-month contract churn is **42.71%**, compared to 11.27% for 1-year contracts.
- **Odds Ratio Signal:** 2-Year contracts reduce churn odds by **73%** ($\text{OR} = 0.27$).
- **Strategic Action:** Launch automated email/SMS campaigns targeting month-to-month subscribers who pass a medium/high ML risk threshold ($\text{prob} \ge 0.35$). Offer a **$10/month credit for 12 months** in exchange for signing a 1-year contract lock-in.

### Campaign 2: Auto-Pay Enrollment Push
- **Data Finding:** Electronic check payment method incurs a **45.29% churn rate** (vs 15.24% for automatic credit card and 16.71% for automatic bank transfer).
- **Odds Ratio Signal:** Electronic check increases churn risk by **47%** ($\text{OR} = 1.47$).
- **Strategic Action:** Offer a **one-time $15 bill credit** upon enrolling in automatic recurring credit card or bank transfer payments, eliminating manual billing friction.

### Campaign 3: Early Onboarding Success Milestones
- **Data Finding:** **52.94% of all customer churn occurs in the first 6 months** of tenure (`tenure <= 6`).
- **Strategic Action:** Implement an automated early-lifecycle onboarding workflow:
  - **Month 1:** Welcome call & setup verification.
  - **Month 3:** Digital satisfaction pulse survey & speed check.
  - **Month 5:** Proactive tech support outreach before contract renewal options.

### Campaign 4: Security & Support Bundling
- **Data Finding:** Customers with no Online Security or Tech Support churn at **48.91%**, whereas those subscribed to both churn at just **9.01%**.
- **Strategic Action:** Re-package standalone security add-ons by bundling free basic Online Security and Tech Support into premium Fiber Optic internet packages.

---

## 💰 4. Financial ROI & Business Case Simulation

Let's model the financial impact of deploying our ML Risk Predictor and Campaign 1 (Contract Migration) on the **1,869 churned customer base**:

### Cost-Benefit Framework Parameters:
- **Baseline Annual Lost Revenue:** $\$1,669,570$
- **Target Population:** High-Risk Customers identified by model ($\text{Recall} = 72\%$ at tuned threshold $\rightarrow 1,345$ churners targeted).
- **Campaign Conversion Rate:** Assume **25% of targeted churners accept** the 1-year contract upgrade offer ($336$ customers saved).
- **Average Customer Monthly Value:** $\$74.44 \text{ / month}$ ($\$893.28 \text{ / year}$).
- **Incentive Offer Cost:** $\$10 \text{ / month}$ credit ($\$120 \text{ / year}$ per customer).

### Net Financial ROI Calculation:
$$\text{Gross Revenue Retained} = 336 \text{ saved customers} \times \$893.28 = \mathbf{\$300,142 \text{ / year}}$$

$$\text{Total Campaign Cost} = 336 \text{ saved customers} \times \$120 = \mathbf{\$40,320 \text{ / year}}$$

$$\text{Net Annual Financial Profit} = \$300,142 - \$40,320 = \mathbf{+\$259,822 \text{ / year}}$$

$$\text{Campaign ROI} = \frac{\text{Net Profit}}{\text{Campaign Cost}} \times 100 = \frac{\$259,822}{\$40,320} \times 100 = \mathbf{644.4\% \text{ Net ROI}}$$

---

## 🎯 5. Business Impact Interview Q&A

### Q: How would you present these recommendations to non-technical business stakeholders?
> **Answer:** *"I avoid leading with model algorithms or accuracy metrics. Instead, I open with the business financial problem ($1.67M lost annually to churn), highlight the core root-cause drivers discovered in the data (month-to-month contract friction and electronic check payments), present our 4 retention campaigns, and demonstrate a projected 644% ROI ($260k net annual bottom-line savings) backed by interactive dashboard simulations."*

### Q: How would you evaluate the success of these retention campaigns in production?
> **Answer:** *"I would execute an A/B Test (Randomized Controlled Trial). High-risk customers identified by our model would be randomly assigned to Treatment (receiving the contract upgrade discount offer) vs Control (receiving standard messaging). After 60 days, I would run a two-sample hypothesis test ($Z$-test for proportions) to verify statistically significant churn reduction in the Treatment group."*
