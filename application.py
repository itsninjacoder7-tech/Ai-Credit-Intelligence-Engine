import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="AI Credit Intelligence Engine",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# Premium UI Styling
# -----------------------------------
st.markdown("""
<style>

/* App background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg,#0f172a,#020617);
    color: white;
}

/* Button */
.stButton>button {
    background: linear-gradient(135deg,#00c6ff,#0072ff);
    color:white;
    border:none;
    border-radius:10px;
    height:48px;
    font-size:16px;
    font-weight:600;
    width:100%;
    transition:0.3s;
}

.stButton>button:hover {
    transform:scale(1.03);
    box-shadow:0px 4px 15px rgba(0,114,255,0.6);
}

/* Hero Section */
.hero {
    text-align: center;
    padding: 60px 20px;
    border-radius: 22px;
    background: linear-gradient(135deg,#020617,#0f172a,#1e293b);
    color: white;
    box-shadow: 0px 10px 40px rgba(0,0,0,0.6);
}

.hero h1 {
    font-size: 50px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 20px;
    opacity: 0.9;
}

.tagline {
    font-size: 15px;
    margin-top: 15px;
    color: #94a3b8;
}

/* Section cards */
.section-card {
    padding:14px;
    border-radius:14px;
    background: linear-gradient(135deg,#0f172a,#1e293b);
    color:white;
    font-weight:600;
    font-size:18px;
    margin-top:28px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0px 6px 20px rgba(0,0,0,0.5);
}

/* Metrics */
[data-testid="metric-container"] {
    background: linear-gradient(135deg,#020617,#0f172a);
    border:1px solid rgba(255,255,255,0.08);
    padding:12px;
    border-radius:12px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.5);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#020617,#0f172a);
}

/* Progress bar */
.stProgress > div > div {
    background: linear-gradient(90deg,#22c55e,#4ade80);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# HERO HEADER
# -----------------------------------
st.markdown("""
<div class="hero">
    <h1>💰 AI Credit Intelligence Engine</h1>
    <p>AI-Powered Smart Loan Decision System</p>
    <div class="tagline">Advanced Risk Analytics for Intelligent Lending</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------
# Sidebar Info
# -----------------------------------
st.sidebar.title("AI Credit Intelligence Engine")

st.sidebar.info("""
This AI system evaluates loan applications using financial indicators,
credit score analysis, and risk assessment.

The model predicts whether a loan should be recommended based on the
applicant’s financial profile.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Project Author")
st.sidebar.write("**Arnav Singh**")
st.sidebar.write("Machine Learning Enthusiast | Aspiring Data Scientist")
st.sidebar.markdown("📧 Email: itsarnav.singh80@gmail.com")
st.sidebar.markdown("[🔗 LinkedIn](https://www.linkedin.com/in/arnav-singh-a87847351)")
st.sidebar.markdown("[💻 GitHub](https://github.com/Arnav-Singh-5080)")

# -----------------------------------
# Load Model
# -----------------------------------
model = pickle.load(open("loan_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# -----------------------------------
# EMI Calculator
# -----------------------------------
def calculate_emi(principal, tenure_months, annual_rate=10):
    if principal == 0 or tenure_months == 0:
        return 0

    monthly_rate = annual_rate / 12 / 100

    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / \
          ((1 + monthly_rate)**tenure_months - 1)

    return emi

# -----------------------------------
# Financial Details
# -----------------------------------
st.markdown('<div class="section-card">💼 Applicant Financial Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    applicant_income = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0, step=1000)
    credit_score = st.slider("Credit Score", 300, 900, 650)
    age = st.slider("Age", 18, 70, 30)
    dependents = st.number_input("Dependents", min_value=0)
    existing_loans = st.number_input("Existing Loans", min_value=0)
    savings = st.number_input("Savings (₹)", min_value=0, step=1000)

with col2:
    collateral_value = st.number_input("Collateral Value (₹)", min_value=0, step=1000)
    loan_term = st.slider("Loan Term (Months)", 6, 360, 60)

# -----------------------------------
# Background Details
# -----------------------------------
st.markdown('<div class="section-card">👤 Applicant Background Details</div>', unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    employment_dict = {"Unemployed":0,"Salaried":1,"Self-Employed":2}
    employment_status = st.selectbox("Employment Status", list(employment_dict.keys()))
    employment_status = employment_dict[employment_status]

    property_dict = {"Rural":0,"Semi-Urban":1,"Urban":2}
    property_area = st.selectbox("Property Area", list(property_dict.keys()))
    property_area = property_dict[property_area]

    loan_purpose_dict = {
        "Home Loan":0,
        "Car Loan":1,
        "Education Loan":2,
        "Personal Loan":3
    }
    loan_purpose = st.selectbox("Loan Purpose", list(loan_purpose_dict.keys()))
    loan_purpose = loan_purpose_dict[loan_purpose]

with col4:
    education_dict = {"Not Graduate":0,"Graduate":1}
    education_level = st.selectbox("Education Level", list(education_dict.keys()))
    education_level = education_dict[education_level]

    gender_dict = {"Female":0,"Male":1}
    gender = st.selectbox("Gender", list(gender_dict.keys()))
    gender = gender_dict[gender]

    employer_category_dict = {
        "Private Sector":0,
        "Government":1,
        "Business Owner":2
    }
    employer_category = st.selectbox("Employer Category", list(employer_category_dict.keys()))
    employer_category = employer_category_dict[employer_category]

# -----------------------------------
# Prediction
# -----------------------------------
if st.button("🔎 Analyze Loan Application"):

    total_income = applicant_income + coapplicant_income
    emi = calculate_emi(loan_amount, loan_term)
    emi_ratio = emi / total_income if total_income > 0 else 0

    with st.expander("📋 Applicant Summary"):
        st.write("Total Income:", total_income)
        st.write("Loan Amount:", loan_amount)
        st.write("Credit Score:", credit_score)

    input_data = pd.DataFrame([[applicant_income, coapplicant_income, loan_amount, credit_score,
                                age, dependents, existing_loans, savings, collateral_value,
                                loan_term, employment_status, property_area, loan_purpose,
                                education_level, gender, employer_category]],
                                columns=['Applicant_Income','Coapplicant_Income','Loan_Amount','Credit_Score',
                                'Age','Dependents','Existing_Loans','Savings','Collateral_Value',
                                'Loan_Term','Employment_Status','Property_Area','Loan_Purpose',
                                'Education_Level','Gender','Employer_Category'])

    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)
    probability = model.predict_proba(scaled_data)

    st.markdown("---")
    st.subheader("📊 Financial Analysis")

    colA, colB, colC = st.columns(3)
    colA.metric("Monthly EMI (₹)", f"{round(emi,2)}")
    colB.metric("Total Monthly Income (₹)", f"{total_income}")
    colC.metric("EMI / Income Ratio", f"{round(emi_ratio*100,2)} %")

    st.markdown("---")
    st.markdown("## 🧠 AI Decision Engine")

    approval_prob = probability[0][1] * 100
    st.progress(int(approval_prob))

    # Improved Decision Logic
    if prediction[0] == 1:
        st.success(f"✅ Loan Recommended (Confidence: {round(approval_prob,2)}%)")
        risk_level = "🟢 Low Risk"
    elif approval_prob > 40:
        st.warning(f"⚠️ Loan Conditionally Recommended (Confidence: {round(approval_prob,2)}%)")
        risk_level = "🟡 Medium Risk"
    else:
        st.error(f"❌ Loan Not Recommended (Confidence: {round(100-approval_prob,2)}%)")
        risk_level = "🔴 High Risk"

    st.markdown(f"### 📊 Risk Level: {risk_level}")

    st.markdown("### 📌 Risk Assessment Insight")

    # Improved Insights
    if emi_ratio > 0.5:
        st.warning("The applicant has a high EMI-to-income ratio, indicating potential financial stress and repayment risk.")
    elif credit_score < 600:
        st.warning("The applicant's credit score is below the acceptable threshold, increasing the probability of loan rejection.")
    elif existing_loans > 2:
        st.warning("The applicant holds multiple existing liabilities, which may impact repayment capacity.")
    else:
        st.info("The applicant demonstrates stable financial behavior with a balanced income-to-loan ratio and a reliable credit profile.")

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("""
<div style="
margin-top:80px;
padding:25px;
border-radius:15px;
background:linear-gradient(135deg,#0f2027,#203a43);
color:#dcdcdc;
text-align:center;
font-size:14px;">
© 2026 AI Credit Intelligence Engine • Built by Arnav Singh
</div>
""", unsafe_allow_html=True)
