"""
LoanSahayak — Smart Loan Intelligence
Production-level Streamlit app for AI-powered loan eligibility prediction.
"""

import os
import time
import pickle
import pandas as pd
import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide",
)

# ─────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────
ANNUAL_INTEREST_RATE = 10       # Default interest rate (%)
MAX_EMI_INCOME_RATIO = 0.40     # 40% of income cap for EMI
MIN_INCOME_THRESHOLD = 25_000   # Minimum recommended monthly income (₹)
MIN_CREDIT_SCORE     = 600      # Minimum acceptable credit score
MAX_EXISTING_LOANS   = 3        # Max allowed active loans
MIN_COLLATERAL_RATIO = 0.5      # Minimum collateral-to-loan ratio

MODEL_PATH  = os.path.join(os.path.dirname(__file__), "models", "loan_model.pkl")
SCALER_PATH = os.path.join(os.path.dirname(__file__), "models", "scaler.pkl")

FEATURE_COLUMNS = [
    "Applicant_Income", "Coapplicant_Income", "Loan_Amount", "Credit_Score",
    "Age", "Dependents", "Existing_Loans", "Savings", "Collateral_Value",
    "Loan_Term", "Employment_Status", "Property_Area", "Loan_Purpose",
    "Education_Level", "Gender", "Employer_Category",
]

# ─────────────────────────────────────────────
# Global CSS
# ─────────────────────────────────────────────
def inject_css() -> None:
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=DM+Sans:wght@300;400;500;600&display=swap');

    :root {
        --gold:          #C9A84C;
        --gold-light:    #E8C97A;
        --gold-dim:      rgba(201,168,76,0.12);
        --bg-deep:       #070B14;
        --bg-card:       rgba(255,255,255,0.03);
        --border:        rgba(201,168,76,0.18);
        --border-bright: rgba(201,168,76,0.45);
        --text-primary:  #F0EBE0;
        --text-secondary:#9A9080;
        --text-muted:    #5A5448;
        --success:       #2ECC71;
        --danger:        #E74C3C;
        --blue:          #3B82F6;
        --font-serif:    'Playfair Display', serif;
        --font-sans:     'DM Sans', sans-serif;
    }

    /* ── Reset ── */
    html, body, [data-testid="stAppViewContainer"] {
        background:  var(--bg-deep)    !important;
        color:       var(--text-primary) !important;
        font-family: var(--font-sans)  !important;
    }

    .main .block-container {
        padding:   2rem 3rem 4rem !important;
        max-width: 1200px          !important;
    }

    /* ── Hero ── */
    .hero {
        position: relative;
        text-align: center;
        padding: 72px 40px 56px;
        border-radius: 24px;
        border: 1px solid var(--border);
        background:
            radial-gradient(ellipse 80% 60% at 50% 0%, rgba(201,168,76,0.08) 0%, transparent 70%),
            linear-gradient(180deg, #0C1525 0%, #070B14 100%);
        overflow: hidden;
        margin-bottom: 12px;
    }
    .hero::after {
        content: '';
        position: absolute;
        top: 0; left: 50%;
        transform: translateX(-50%);
        width: 60%; height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold), transparent);
    }
    .hero-badge {
        display: inline-block;
        padding: 6px 18px;
        border: 1px solid var(--border-bright);
        border-radius: 100px;
        font-size: 11px; letter-spacing: 2.5px;
        text-transform: uppercase;
        color: var(--gold);
        background: var(--gold-dim);
        margin-bottom: 24px;
        font-weight: 600;
    }
    .hero-title {
        font-family: var(--font-serif) !important;
        font-size: 54px !important; font-weight: 700 !important;
        color: var(--text-primary) !important;
        margin: 0 0 14px !important; line-height: 1.1 !important;
    }
    .hero-title span { color: var(--gold); }
    .hero-sub {
        font-size: 16px; color: var(--text-secondary);
        font-weight: 300; letter-spacing: 0.3px;
        max-width: 500px; margin: 0 auto 28px; line-height: 1.7;
    }
    .hero-stats {
        display: flex; justify-content: center; gap: 48px;
        margin-top: 36px; padding-top: 24px;
        border-top: 1px solid var(--border);
    }
    .stat-value {
        font-family: var(--font-serif); font-size: 26px;
        font-weight: 600; color: var(--gold-light);
    }
    .stat-label {
        font-size: 11px; letter-spacing: 1.5px;
        text-transform: uppercase; color: var(--text-muted); margin-top: 4px;
    }

    /* ── Section header ── */
    .section-header {
        display: flex; align-items: center; gap: 12px;
        margin: 36px 0 18px;
        padding-bottom: 14px;
        border-bottom: 1px solid var(--border);
    }
    .section-icon {
        width: 36px; height: 36px; border-radius: 10px;
        background: var(--gold-dim); border: 1px solid var(--border-bright);
        display: flex; align-items: center; justify-content: center;
        font-size: 16px;
    }
    .section-title {
        font-family: var(--font-serif) !important;
        font-size: 20px !important; font-weight: 600 !important;
        color: var(--text-primary) !important; margin: 0 !important;
    }
    .section-desc {
        font-size: 11px; color: var(--text-muted);
        letter-spacing: 1px; text-transform: uppercase; margin-left: auto;
    }

    /* ── Inputs ── */
    label,
    [data-testid="stWidgetLabel"] {
        color: var(--text-secondary) !important;
        font-size: 12px !important; letter-spacing: 1px !important;
        text-transform: uppercase !important; font-weight: 500 !important;
    }
    input[type="number"] {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
        font-size: 15px !important;
        transition: border-color .2s !important;
    }
    input[type="number"]:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px var(--gold-dim) !important;
    }
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.04) !important;
        border: 1px solid var(--border) !important;
        border-radius: 10px !important;
        color: var(--text-primary) !important;
    }
    .stSelectbox > div > div:focus-within {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 3px var(--gold-dim) !important;
    }

    /* ── Slider ── */
    .stSlider > div > div > div        { background: var(--gold) !important; }
    .stSlider > div > div > div > div  {
        background: var(--gold) !important;
        border: 2px solid var(--bg-deep) !important;
        box-shadow: 0 0 0 2px var(--gold) !important;
    }
    [data-testid="stSlider"] > div > div { background: rgba(255,255,255,0.07) !important; }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C 0%, #8B6914 100%) !important;
        color: #070B14 !important; border: none !important;
        border-radius: 12px !important; height: 54px !important;
        font-size: 14px !important; font-weight: 700 !important;
        letter-spacing: 1.5px !important; text-transform: uppercase !important;
        width: 100% !important; font-family: var(--font-sans) !important;
        transition: all .25s ease !important;
        box-shadow: 0 4px 24px rgba(201,168,76,0.25) !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(201,168,76,0.4) !important;
    }

    /* ── Metrics ── */
    [data-testid="metric-container"] {
        background: var(--bg-card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 16px !important;
        padding: 20px 22px !important;
        backdrop-filter: blur(12px) !important;
        transition: border-color .2s !important;
    }
    [data-testid="metric-container"]:hover { border-color: var(--border-bright) !important; }
    [data-testid="stMetricLabel"]  { color: var(--text-muted) !important; font-size: 11px !important; letter-spacing: 1.5px !important; text-transform: uppercase !important; }
    [data-testid="stMetricValue"]  { color: var(--text-primary) !important; font-family: var(--font-serif) !important; font-size: 26px !important; }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: var(--bg-card) !important; border: 1px solid var(--border) !important;
        border-radius: 12px !important; color: var(--text-secondary) !important;
        font-size: 13px !important; letter-spacing: 0.5px !important;
    }
    .streamlit-expanderContent {
        background: rgba(255,255,255,0.02) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important; border-radius: 0 0 12px 12px !important;
    }

    /* ── Alerts ── */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 14px !important; border-left-width: 3px !important;
        font-family: var(--font-sans) !important;
        font-size: 15px !important; padding: 16px 20px !important;
    }

    /* ── Progress bar ── */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--gold), var(--gold-light)) !important;
        border-radius: 100px !important;
    }
    .stProgress > div {
        background: rgba(255,255,255,0.07) !important;
        border-radius: 100px !important; height: 8px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #070B14 !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown li,
    [data-testid="stSidebar"] label {
        color: var(--text-secondary) !important; font-size: 13px !important;
    }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: var(--text-primary) !important;
        font-family: var(--font-serif) !important;
    }

    /* ── Misc ── */
    hr { border-color: var(--border) !important; margin: 28px 0 !important; }
    ::-webkit-scrollbar        { width: 6px; }
    ::-webkit-scrollbar-track  { background: transparent; }
    ::-webkit-scrollbar-thumb  { background: var(--border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--gold); }
    </style>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────
def calculate_emi(principal: float, tenure_months: int, annual_rate: float = ANNUAL_INTEREST_RATE) -> float:
    """Return monthly EMI. Returns 0 if inputs are invalid."""
    if principal <= 0 or tenure_months <= 0:
        return 0.0
    r = annual_rate / 12 / 100
    return principal * r * (1 + r) ** tenure_months / ((1 + r) ** tenure_months - 1)


def max_loan_from_emi(max_emi: float, tenure_months: int, annual_rate: float = ANNUAL_INTEREST_RATE) -> float:
    """Reverse EMI formula to compute the maximum principal."""
    if tenure_months <= 0:
        return 0.0
    r = annual_rate / 12 / 100
    return max_emi * ((1 + r) ** tenure_months - 1) / (r * (1 + r) ** tenure_months)


@st.cache_resource
def load_artifacts() -> tuple:
    """Load and cache ML model + scaler. Raises on missing files."""
    model  = pickle.load(open(MODEL_PATH,  "rb"))
    scaler = pickle.load(open(SCALER_PATH, "rb"))
    return model, scaler


def section_header(icon: str, title: str, desc: str = "") -> None:
    desc_html = f'<div class="section-desc">{desc}</div>' if desc else ""
    st.markdown(f"""
    <div class="section-header">
        <div class="section-icon">{icon}</div>
        <div class="section-title">{title}</div>
        {desc_html}
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# UI Sections
# ─────────────────────────────────────────────
def render_hero() -> None:
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ AI-Powered Lending Intelligence</div>
        <div class="hero-title">Loan<span>Sahayak</span></div>
        <div class="hero-sub">
            Sophisticated credit analysis and risk assessment —
            engineered for modern lending decisions.
        </div>
        <div class="hero-stats">
            <div><div class="stat-value">83.4%</div><div class="stat-label">Accuracy</div></div>
            <div><div class="stat-value">&lt; 2s</div><div class="stat-label">Decision Time</div></div>
            <div><div class="stat-value">16+</div><div class="stat-label">Risk Factors</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar() -> None:
    sb = st.sidebar
    sb.markdown("""
    <div style="padding:8px 0 20px; border-bottom:1px solid rgba(201,168,76,0.2); margin-bottom:20px;">
        <div style="font-family:'Playfair Display',serif; font-size:22px; color:#F0EBE0; font-weight:700;">LoanSahayak</div>
        <div style="font-size:11px; letter-spacing:2px; text-transform:uppercase; color:#9A9080; margin-top:4px;">Smart Loan Intelligence</div>
    </div>
    <div style="padding:16px; border-radius:14px; background:rgba(59,130,246,0.08); border:1px solid rgba(59,130,246,0.2); color:#9CCBFF; font-size:14px; line-height:1.7;">
        AI-powered system that evaluates loan applications using:<br>
        • Financial indicators<br>
        • Credit score analysis<br>
        • Multi-factor risk assessment
    </div>
    <br>
    <div style="font-size:12px; color:#9A9080; letter-spacing:1px; text-transform:uppercase; margin-bottom:6px;">System Stats</div>
    <div style="font-size:14px; color:#F0EBE0; line-height:1.9;">
        ✔ Accuracy: <span style="color:#C9A84C;">83.4%</span><br>
        ✔ Decision Time: <span style="color:#C9A84C;">&lt; 2s</span><br>
        ✔ Risk Factors: <span style="color:#C9A84C;">16+</span>
    </div>
    <hr style="border-color:rgba(201,168,76,0.18);">
    <div style="font-family:'Playfair Display',serif; font-size:20px; color:#F0EBE0; font-weight:600;">👤 Project Author</div>
    <div style="margin-top:10px; font-size:16px; color:#F0EBE0; font-weight:500;">Arnav Singh</div>
    <div style="font-size:13px; color:#9A9080; margin-top:4px;">Machine Learning Enthusiast · Aspiring Data Scientist</div>
    <br>
    """, unsafe_allow_html=True)

    col1, col2, col3 = sb.columns(3, gap="small")
    _icon_link(col1, "https://www.linkedin.com/in/arnav-singh-a87847351", "rgba(78,161,255,0.08)", "rgba(78,161,255,0.2)", _linkedin_svg())
    _icon_link(col2, "mailto:itsarnav.singh80@gmail.com",                 "rgba(0,255,150,0.08)",  "rgba(0,255,150,0.25)", _email_svg())
    _icon_link(col3, "https://github.com/Arnav-Singh-5080",               "rgba(255,255,255,0.05)","rgba(255,255,255,0.15)", _github_svg())

    sb.markdown("""
    <br>
    <div style="font-size:12px; color:#5A5448; text-align:center;">
        ⭐ If you like this project, consider starring it on GitHub
    </div>
    """, unsafe_allow_html=True)


def _icon_link(col, href: str, bg: str, border: str, svg: str) -> None:
    col.markdown(f"""
    <div style="display:flex; justify-content:center;">
        <a href="{href}" target="_blank">
            <div style="display:flex; align-items:center; justify-content:center;
                        width:40px; height:40px; border-radius:12px;
                        background:{bg}; border:1px solid {border};">
                {svg}
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)


def _linkedin_svg() -> str:
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="#4EA1FF"><path d="M4.98 3.5C4.98 4.88 3.87 6 2.49 6 1.11 6 0 4.88 0 3.5 0 2.12 1.11 1 2.49 1 3.87 1 4.98 2.12 4.98 3.5ZM.22 8.98H4.75V24H.22V8.98ZM7.98 8.98H12.32V11.04H12.38C13.04 9.86 14.66 8.63 17.04 8.63 22.08 8.63 23 11.88 23 16.13V24H18.47V17.21C18.47 15.46 18.44 13.2 16.02 13.2 13.56 13.2 13.18 15.06 13.18 17.08V24H8.65V8.98H7.98Z"/></svg>'


def _email_svg() -> str:
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="#00FFAA"><path d="M2 4C2 2.9 2.9 2 4 2H20C21.1 2 22 2.9 22 4V20C22 21.1 21.1 22 20 22H4C2.9 22 2 21.1 2 20V4ZM4 4V6L12 13 20 6V4L12 11 4 4ZM20 8L12 15 4 8V20H20V8Z"/></svg>'


def _github_svg() -> str:
    return '<svg height="18" width="18" viewBox="0 0 16 16" fill="#4EA1FF"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.6.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2 .37-2.53-1.37-2.53-1.37-.34-.87-.83-1.1-.83-1.1-.68-.46.05-.45.05-.45.75.05 1.14.77 1.14.77.67 1.14 1.75.81 2.18.62.07-.48.26-.81.47-1-1.78-.2-3.65-.89-3.65-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82a7.69 7.69 0 0 1 2-.27c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38C13.71 14.53 16 11.54 16 8c0-4.42-3.58-8-8-8z"/></svg>'


def render_financial_inputs() -> dict:
    section_header("💼", "Financial Profile", "Income & Loan Details")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        applicant_income   = st.number_input("Applicant Income (₹)",   min_value=0, step=1_000)
        coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=1_000)
        loan_amount        = st.number_input("Loan Amount (₹)",        min_value=0, step=1_000)
        savings            = st.number_input("Savings (₹)",            min_value=0, step=1_000)

    with col2:
        collateral_value = st.number_input("Collateral Value (₹)",    min_value=0, step=1_000)
        dependents       = st.number_input("Number of Dependents",    min_value=0)
        existing_loans   = st.number_input("Existing Active Loans",   min_value=0)

    col3, col4 = st.columns(2, gap="large")
    with col3:
        credit_score = st.slider("Credit Score", 300, 900, 650)
    with col4:
        loan_term = st.slider("Loan Term (Months)", 6, 360, 60)

    col5, _ = st.columns(2, gap="large")
    with col5:
        age = st.slider("Applicant Age", 18, 70, 30)

    return dict(
        applicant_income=applicant_income,
        coapplicant_income=coapplicant_income,
        loan_amount=loan_amount,
        savings=savings,
        collateral_value=collateral_value,
        dependents=int(dependents),
        existing_loans=int(existing_loans),
        credit_score=credit_score,
        loan_term=loan_term,
        age=age,
    )


def render_background_inputs() -> dict:
    section_header("👤", "Applicant Background", "Demographic & Employment")
    col6, col7 = st.columns(2, gap="large")

    with col6:
        employment_status = {"Unemployed": 0, "Salaried": 1, "Self-Employed": 2}
        property_area     = {"Rural": 0, "Semi-Urban": 1, "Urban": 2}
        loan_purpose      = {"Home Loan": 0, "Car Loan": 1, "Education Loan": 2, "Personal Loan": 3}
        emp_val  = employment_status[st.selectbox("Employment Status", list(employment_status.keys()))]
        prop_val = property_area    [st.selectbox("Property Area",     list(property_area.keys()))]
        purp_val = loan_purpose     [st.selectbox("Loan Purpose",      list(loan_purpose.keys()))]

    with col7:
        education_level   = {"Not Graduate": 0, "Graduate": 1}
        gender            = {"Female": 0, "Male": 1}
        employer_category = {"Private Sector": 0, "Government": 1, "Business Owner": 2}
        edu_val  = education_level  [st.selectbox("Education Level",    list(education_level.keys()))]
        gen_val  = gender           [st.selectbox("Gender",             list(gender.keys()))]
        empl_val = employer_category[st.selectbox("Employer Category",  list(employer_category.keys()))]

    return dict(
        employment_status=emp_val,
        property_area=prop_val,
        loan_purpose=purp_val,
        education_level=edu_val,
        gender=gen_val,
        employer_category=empl_val,
    )


def render_affordability(fin: dict) -> None:
    section_header("💰", "Loan Affordability Checker", "Know your borrowing capacity")

    total_income = fin["applicant_income"] + fin["coapplicant_income"]

    if total_income <= 0:
        st.info("Enter applicant / coapplicant income to see affordability analysis.")
        return

    max_emi_allowed = total_income * MAX_EMI_INCOME_RATIO
    max_loan        = max_loan_from_emi(max_emi_allowed, fin["loan_term"])
    current_emi     = calculate_emi(fin["loan_amount"], fin["loan_term"]) if fin["loan_amount"] > 0 else 0
    emi_ratio_pct   = (current_emi / total_income * 100) if current_emi > 0 else 0

    # ── Metrics ──
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Monthly Income",        f"₹ {total_income:,.0f}")
    c2.metric("Max EMI You Can Afford",       f"₹ {max_emi_allowed:,.0f}/mo",
              help=f"Banks cap EMI at {int(MAX_EMI_INCOME_RATIO*100)}% of monthly income")
    c3.metric("Estimated Maximum Loan",       f"₹ {max_loan:,.0f}",
              help=f"Based on {ANNUAL_INTEREST_RATE}% interest over {fin['loan_term']} months")

    st.markdown("---")
    st.info(
        "**Affordability estimate only.**  "
        "Final approval depends on credit score, employment stability, "
        "savings, collateral, and model risk assessment."
    )

    # ── Risk warnings ──
    section_header("⚠️", "Risk Factors")
    warnings = _collect_risk_warnings(fin, total_income)
    if warnings:
        for w in warnings:
            st.warning(w)
    else:
        st.success("No major risk factors detected.")

    # ── Loan vs. limit ──
    if fin["loan_amount"] > 0:
        if fin["loan_amount"] > max_loan:
            excess    = fin["loan_amount"] - max_loan
            excess_pct = excess / max_loan * 100
            st.error(
                f"**Loan Exceeds Affordability Limit**\n\n"
                f"- Requested: ₹ {fin['loan_amount']:,.0f}\n"
                f"- Limit: ₹ {max_loan:,.0f}\n"
                f"- Excess: ₹ {excess:,.0f} ({excess_pct:.0f}% above limit)\n\n"
                f"*Tip: Reduce loan amount or extend tenure.*"
            )
        else:
            buffer     = max_loan - fin["loan_amount"]
            buffer_pct = buffer / max_loan * 100
            st.success(
                f"**Loan Within Affordable Range**\n\n"
                f"- Requested: ₹ {fin['loan_amount']:,.0f}\n"
                f"- Limit: ₹ {max_loan:,.0f}\n"
                f"- Buffer: ₹ {buffer:,.0f} ({buffer_pct:.0f}% below limit)\n\n"
                f"Your EMI of ~₹ {current_emi:,.0f}/mo is {emi_ratio_pct:.1f}% of income."
            )

    # ── EMI progress bar ──
    if current_emi > 0:
        util_pct = min(100, current_emi / max_emi_allowed * 100) if max_emi_allowed > 0 else 0
        st.caption(f"**EMI:** ₹ {current_emi:,.0f}/mo  ·  {emi_ratio_pct:.1f}% of income")
        st.markdown("**EMI utilisation of affordable limit:**")
        st.progress(int(util_pct))
        if util_pct > 100:
            st.warning("EMI exceeds recommended limit.")
        elif util_pct > 80:
            st.info("EMI is close to the recommended limit.")
        else:
            st.success("EMI is within comfortable limits.")


def _collect_risk_warnings(fin: dict, total_income: float) -> list[str]:
    warns = []
    if fin["credit_score"] < MIN_CREDIT_SCORE:
        warns.append(f"Low credit score ({fin['credit_score']}) — minimum recommended: {MIN_CREDIT_SCORE}")
    elif fin["credit_score"] < 700:
        warns.append(f"Fair credit score ({fin['credit_score']}) — consider improving before applying")
    if total_income < MIN_INCOME_THRESHOLD:
        warns.append(f"Monthly income below recommended ₹{MIN_INCOME_THRESHOLD:,}")
    if fin["savings"] == 0:
        warns.append("No savings detected")
    elif fin["loan_amount"] > 0 and fin["savings"] < fin["loan_amount"] * 0.1:
        warns.append(f"Low savings — only {fin['savings']/fin['loan_amount']*100:.1f}% of loan amount")
    if fin["dependents"] > 3:
        warns.append(f"High number of dependents ({fin['dependents']})")
    if fin["existing_loans"] > MAX_EXISTING_LOANS:
        warns.append(f"Multiple existing loans ({fin['existing_loans']})")
    if fin["employment_status"] == 0:
        warns.append("Currently unemployed — high risk factor")
    return warns


def run_prediction(fin: dict, bg: dict, model, scaler) -> None:
    """Animate, predict, and render the decision UI."""
    # ── Validation ──
    if fin["applicant_income"] == 0 or fin["loan_amount"] == 0:
        st.error("⚠ Applicant Income and Loan Amount must be greater than zero.")
        st.stop()

    # ── Progress animation ──
    steps = [
        "🔍 Collecting financial data…",
        "📊 Analysing income & liabilities…",
        "🧠 Running ML model inference…",
        "⚖️ Evaluating risk parameters…",
        "✅ Finalising decision…",
    ]
    bar    = st.progress(0)
    status = st.empty()
    for i, step in enumerate(steps):
        status.markdown(f"<span style='color:#C9A84C; font-family:var(--font-sans);'>{step}</span>",
                        unsafe_allow_html=True)
        bar.progress((i + 1) * 20)
        time.sleep(0.4)
    status.empty()
    bar.empty()

    # ── Derived values ──
    total_income = fin["applicant_income"] + fin["coapplicant_income"]
    emi          = calculate_emi(fin["loan_amount"], fin["loan_term"])
    emi_ratio    = emi / total_income if total_income > 0 else 0

    # ── Application summary ──
    with st.expander("📋 Application Summary"):
        s1, s2, s3 = st.columns(3)
        s1.metric("Total Household Income", f"₹ {total_income:,}")
        s2.metric("Loan Amount Requested",  f"₹ {fin['loan_amount']:,}")
        s3.metric("Credit Score",           fin["credit_score"])

    # ── ML inference ──
    input_df = pd.DataFrame([[
        fin["applicant_income"], fin["coapplicant_income"], fin["loan_amount"],
        fin["credit_score"], fin["age"], fin["dependents"], fin["existing_loans"],
        fin["savings"], fin["collateral_value"], fin["loan_term"],
        bg["employment_status"], bg["property_area"], bg["loan_purpose"],
        bg["education_level"], bg["gender"], bg["employer_category"],
    ]], columns=FEATURE_COLUMNS)

    scaled      = scaler.transform(input_df)
    prediction  = model.predict(scaled)[0]
    proba       = model.predict_proba(scaled)[0]
    approval_pct = proba[1] * 100

    # ── Financial analysis ──
    st.markdown("---")
    section_header("📊", "Financial Analysis")
    m1, m2, m3 = st.columns(3)
    m1.metric("Monthly EMI",         f"₹ {emi:,.2f}")
    m2.metric("Total Monthly Income",f"₹ {total_income:,}")
    m3.metric("EMI / Income Ratio",  f"{emi_ratio * 100:.2f}%")

    # ── Confidence bar ──
    st.markdown("---")
    st.progress(int(approval_pct))
    st.markdown(f"**Approval Probability: {approval_pct:.1f}%**")
    st.markdown("<br>", unsafe_allow_html=True)

    # ── Quick risk flag ──
    if emi_ratio > 0.5:
        st.warning("⚠ High EMI ratio — exceeds 50% of income")
    elif fin["credit_score"] < MIN_CREDIT_SCORE:
        st.warning("⚠ Low credit score")
    else:
        st.info("✓ Profile looks stable")

    # ── Decision banner ──
    if prediction == 1:
        st.success(f"✓ Loan **Approved** — Confidence: {approval_pct:.2f}%")
    else:
        st.error(f"✕ Loan **Rejected** — Confidence: {100 - approval_pct:.2f}%")
        reasons = _rejection_reasons(fin, total_income, emi_ratio)
        if reasons:
            section_header("⚠️", "Reasons for Rejection", "Key Risk Factors")
            for r in reasons:
                st.write(f"• {r}")
        else:
            st.write("Application does not meet the bank's approval criteria.")

    # ── PDF report ──
    pdf_bytes = _build_pdf_report(fin, total_income, emi, fin["credit_score"],
                                  prediction, approval_pct,
                                  _rejection_reasons(fin, total_income, emi_ratio) if prediction == 0 else [])
    st.download_button(
        label="📄 Download PDF Report",
        data=pdf_bytes,
        file_name="LoanSahayak_Report.pdf",
        mime="application/pdf",
    )


def _rejection_reasons(fin: dict, total_income: float, emi_ratio: float) -> list[str]:
    reasons = []
    if total_income < MIN_INCOME_THRESHOLD:
        reasons.append(f"Total household income is below ₹{MIN_INCOME_THRESHOLD:,}/month.")
    if emi_ratio > 0.5:
        reasons.append("EMI-to-income ratio exceeds 50%.")
    if fin["credit_score"] < MIN_CREDIT_SCORE:
        reasons.append(f"Credit score ({fin['credit_score']}) is below the minimum of {MIN_CREDIT_SCORE}.")
    if fin["existing_loans"] > MAX_EXISTING_LOANS:
        reasons.append(f"Too many active loans ({fin['existing_loans']}).")
    if fin["collateral_value"] < fin["loan_amount"] * MIN_COLLATERAL_RATIO:
        reasons.append("Collateral value is insufficient for the requested loan.")
    return reasons


def _build_pdf_report(
    fin: dict,
    total_income: float,
    emi: float,
    credit_score: int,
    prediction: int,
    approval_pct: float,
    reasons: list[str],
) -> bytes:
    """Build a PDF report and return raw bytes."""
    path   = "/tmp/loan_report.pdf"
    doc    = SimpleDocTemplate(path, pagesize=A4)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle", parent=styles["Title"],
        alignment=TA_CENTER, textColor=colors.HexColor("#C9A84C"),
    )
    section_style = ParagraphStyle(
        "SectionHead", parent=styles["Heading2"],
        textColor=colors.HexColor("#3B82F6"),
    )
    decision_style = ParagraphStyle(
        "Decision", parent=styles["Heading1"],
        alignment=TA_CENTER,
        textColor=colors.green if prediction == 1 else colors.red,
    )

    body = []
    body.append(Paragraph("LoanSahayak", title_style))
    body.append(Spacer(1, 6))
    body.append(Paragraph("AI Loan Analysis Report", styles["Italic"]))
    body.append(Spacer(1, 20))

    # Financial summary table
    body.append(Paragraph("Financial Summary", section_style))
    body.append(Spacer(1, 10))
    fin_table = Table([
        ["Metric",       "Value"],
        ["Total Income", f"₹ {total_income:,}"],
        ["Loan Amount",  f"₹ {fin['loan_amount']:,}"],
        ["Loan Term",    f"{fin['loan_term']} months"],
        ["Monthly EMI",  f"₹ {emi:,.2f}"],
    ])
    fin_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#C9A84C")),
        ("GRID",       (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    body.append(fin_table)
    body.append(Spacer(1, 20))

    # Credit profile table
    body.append(Paragraph("Credit Profile", section_style))
    body.append(Spacer(1, 10))
    credit_table = Table([
        ["Credit Score",   credit_score],
        ["Dependents",     fin["dependents"]],
        ["Existing Loans", fin["existing_loans"]],
    ])
    credit_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    body.append(credit_table)
    body.append(Spacer(1, 20))

    # Decision
    label = "APPROVED" if prediction == 1 else "REJECTED"
    body.append(Paragraph(label, decision_style))
    body.append(Spacer(1, 10))
    body.append(Paragraph(f"Confidence: {approval_pct:.2f}%", styles["Normal"]))
    body.append(Spacer(1, 20))

    if reasons:
        body.append(Paragraph("Reasons for Rejection", section_style))
        body.append(Spacer(1, 10))
        for r in reasons:
            body.append(Paragraph(f"• {r}", styles["Normal"]))
        body.append(Spacer(1, 20))

    body.append(Paragraph("Generated by LoanSahayak AI", styles["Italic"]))
    doc.build(body)

    with open(path, "rb") as f:
        return f.read()


# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
def render_footer() -> None:
    st.markdown("""
    <div style="
        margin-top:100px; padding:28px 32px; border-radius:16px;
        border:1px solid rgba(201,168,76,0.12); background:rgba(255,255,255,0.02);
        display:flex; justify-content:space-between; align-items:center;
        font-size:12px; letter-spacing:1px; color:#5A5448;">
        <div>© 2026 <span style='color:#C9A84C;'>LoanSahayak</span> — All Rights Reserved</div>
        <div style='text-transform:uppercase; letter-spacing:2px;'>AI · Credit · Intelligence</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────
def main() -> None:
    inject_css()
    render_hero()
    render_sidebar()

    model, scaler = load_artifacts()

    financial_inputs   = render_financial_inputs()
    background_inputs  = render_background_inputs()

    render_affordability(financial_inputs)

    st.markdown("<div style='margin-top:36px;'></div>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 1.2, 1])
    with col_btn:
        analyse = st.button("⬡  Analyse Loan Application")

    if analyse:
        run_prediction(financial_inputs, background_inputs, model, scaler)

    render_footer()


if __name__ == "__main__":
    main()
