import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------------
# Resource Loading (Cached)
# -----------------------------------
@st.cache_resource
def load_assets():
    """Loads the ML model and scaler with caching to improve performance."""
    try:
        model = pickle.load(open("loan_model.pkl", "rb"))
        scaler = pickle.load(open("scaler.pkl", "rb"))
        return model, scaler
    except FileNotFoundError:
        return None, None

model, scaler = load_assets()

# -----------------------------------
# Premium UI Styling
# -----------------------------------
def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --gold-dim: rgba(201,168,76,0.15);
        --bg-deep: #070B14;
        --bg-card: rgba(255,255,255,0.035);
        --border: rgba(201,168,76,0.2);
        --text-primary: #F0EBE0;
        --text-secondary: #9A9080;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-deep) !important;
        color: var(--text-primary) !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* Noise texture overlay */
    [data-testid="stAppViewContainer"]::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 0.4;
    }

    .hero-wrap {
        text-align: center;
        padding: 60px 40px;
        border-radius: 24px;
        border: 1px solid var(--border);
        background: radial-gradient(ellipse 80% 60% at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%), #0C1525;
        margin-bottom: 25px;
    }

    .hero-title { font-family: 'Playfair Display', serif !important; font-size: 50px !important; color: var(--text-primary); }
    .hero-title span { color: var(--gold); }

    .stButton > button {
        background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%) !important;
        color: #070B14 !important;
        font-weight: 700 !important;
        height: 50px !important;
        border-radius: 12px !important;
        transition: 0.3s;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 30px 0 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid var(--border);
    }

    .result-approved { padding: 30px; border-radius: 20px; border: 1px solid #2ECC71; background: rgba(46,204,113,0.05); text-align: center; }
    .result-rejected { padding: 30px; border-radius: 20px; border: 1px solid #E74C3C; background: rgba(231,76,60,0.05); text-align: center; }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# -----------------------------------
# Sidebar & Header
# -----------------------------------
st.sidebar.markdown("""
<div style="font-family: 'Playfair Display', serif; font-size: 24px; color: #C9A84C;">LoanSahayak</div>
<p style="font-size: 12px; color: #9A9080;">V2.0.1 Premium Intelligence</p>
""", unsafe_allow_html=True)

if model is None:
    st.error("🚨 Critical Error: `loan_model.pkl` or `scaler.pkl` not found. Please upload weights to the root directory.")
    st.stop()

# -----------------------------------
# Hero Section
# -----------------------------------
st.markdown("""
<div class="hero-wrap">
    <div style="color: var(--gold); letter-spacing: 2px; font-size: 12px; font-weight: 600;">ESTABLISHED 2026</div>
    <div class="hero-title">Loan<span>Sahayak</span> AI</div>
    <div style="color: var(--text-secondary); max-width: 600px; margin: 10px auto;">
        Advanced algorithmic credit assessment utilizing 16+ non-linear risk factors for institutional-grade decisioning.
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Input Section
# -----------------------------------
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown('<div class="section-header">💼 Financial Assets</div>', unsafe_allow_html=True)
    app_inc = st.number_input("Applicant Monthly Income (₹)", min_value=0, value=50000, step=1000)
    co_app_inc = st.number_input("Co-Applicant Income (₹)", min_value=0, value=0, step=1000)
    loan_amt = st.number_input("Requested Loan Amount (₹)", min_value=0, value=200000, step=5000)
    savings = st.number_input("Liquid Savings (₹)", min_value=0, value=50000)
    
    st.markdown('<div class="section-header">🛡️ Credit Risk</div>', unsafe_allow_html=True)
    c_score = st.slider("CIBIL / Credit Score", 300, 900, 720)
    existing_loans = st.number_input("Active Debt Accounts", 0, 10, 0)

with col2:
    st.markdown('<div class="section-header">👤 Demographics</div>', unsafe_allow_html=True)
    age = st.slider("Applicant Age", 18, 75, 30)
    deps = st.number_input("Dependents", 0, 10, 0)
    
    edu_dict = {"Graduate": 1, "Not Graduate": 0}
    edu = edu_dict[st.selectbox("Education Level", list(edu_dict.keys()))]
    
    emp_dict = {"Salaried": 1, "Self-Employed": 2, "Unemployed": 0}
    emp = emp_dict[st.selectbox("Employment Status", list(emp_dict.keys()))]
    
    st.markdown('<div class="section-header">🏠 Collateral & Terms</div>', unsafe_allow_html=True)
    collateral = st.number_input("Collateral Value (₹)", min_value=0, value=0)
    term = st.slider("Tenure (Months)", 6, 360, 120)
    
    area_dict = {"Urban": 2, "Semi-Urban": 1, "Rural": 0}
    area = area_dict[st.selectbox("Property Location", list(area_dict.keys()))]

# Hidden mapping for remaining features
purpose_dict = {"Home Loan": 0, "Car Loan": 1, "Education Loan": 2, "Personal Loan": 3}
gender_dict = {"Male": 1, "Female": 0}
employer_dict = {"Private Sector": 0, "Government": 1, "Business Owner": 2}

# -----------------------------------
# Logic & Prediction
# -----------------------------------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 EXECUTE RISK ANALYSIS"):
    # Calculations
    total_income = app_inc + co_app_inc
    monthly_rate = 10.5 / 12 / 100 # Assuming base 10.5%
    emi = (loan_amt * monthly_rate * (1 + monthly_rate)**term) / ((1 + monthly_rate)**term - 1) if loan_amt > 0 else 0
    dti_ratio = (emi / total_income) if total_income > 0 else 0

    # Data Prep
    input_df = pd.DataFrame([[
        app_inc, co_app_inc, loan_amt, c_score, age, deps, existing_loans, 
        savings, collateral, term, emp, area, 0, edu, 1, 0 # placeholders for purpose/gender/employer
    ]], columns=[
        'Applicant_Income','Coapplicant_Income','Loan_Amount','Credit_Score',
        'Age','Dependents','Existing_Loans','Savings','Collateral_Value',
        'Loan_Term','Employment_Status','Property_Area','Loan_Purpose',
        'Education_Level','Gender','Employer_Category'
    ])

    # ML Inference
    scaled_input = scaler.transform(input_df)
    prob = model.predict_proba(scaled_input)[0][1]
    prediction = model.predict(scaled_input)[0]

    # UI Result Display
    st.markdown("---")
    res_col1, res_col2 = st.columns([1, 1])

    with res_col1:
        if prediction == 1:
            st.markdown(f"""
            <div class="result-approved">
                <h2 style="color:#2ECC71; margin:0;">Application Approved</h2>
                <p style="color:#F0EBE0; font-size:18px;">Confidence Score: {round(prob*100, 2)}%</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-rejected">
                <h2 style="color:#E74C3C; margin:0;">Application Declined</h2>
                <p style="color:#F0EBE0; font-size:18px;">Risk Probability: {round((1-prob)*100, 2)}%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.write("")
        st.metric("Estimated Monthly EMI", f"₹{round(emi, 2):,}")
        st.progress(int(prob * 100))

    with res_col2:
        # Visual 1: EMI vs Income
        fig = go.Figure(go.Pie(
            labels=['Disposable Income', 'Loan EMI'],
            values=[total_income - emi, emi],
            hole=.6,
            marker_colors=['#C9A84C', '#E74C3C']
        ))
        fig.update_layout(title="Debt-to-Income Impact", height=250, 
                          margin=dict(l=20, r=20, t=40, b=20),
                          paper_bgcolor='rgba(0,0,0,0)', font_color="#9A9080")
        st.plotly_chart(fig, use_container_width=True)

    # Risk Insights
    st.markdown("### 🔍 Institutional Risk Insights")
    ri1, ri2, ri3 = st.columns(3)
    
    with ri1:
        st.info(f"**DTI Ratio:** {round(dti_ratio*100, 1)}%")
        if dti_ratio > 0.45: st.warning("High Debt-to-Income burden detected.")
    with ri2:
        st.info(f"**LTV Ratio:** {round((loan_amt/collateral*100),1) if collateral > 0 else 'N/A'}%")
        if collateral > 0 and (loan_amt/collateral) > 0.9: st.warning("High Loan-to-Value risk.")
    with ri3:
        st.info(f"**Credit Profile:** {'Strong' if c_score > 750 else 'Average'}")
        if c_score < 600: st.error("Subprime credit score detected.")

# -----------------------------------
# Footer
# -----------------------------------
st.markdown(f"""
<div style="margin-top: 50px; text-align: center; color: #5A5448; font-size: 11px;">
    &copy; 2026 LOANSAHAYAK INTELLIGENCE · SECURE DEPLOYMENT ENGINE · DATA PRIVACY ENCRYPTED
</div>
""", unsafe_allow_html=True)
