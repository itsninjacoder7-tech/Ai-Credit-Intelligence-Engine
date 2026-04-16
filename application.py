import streamlit as st
import pandas as pd
import pickle
import numpy as np
import time

# -----------------------------------
# Page Config
# -----------------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

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
# INPUT UI (same structure simplified)
# -----------------------------------
st.title("🏦 LoanSahayak — Smart Loan Intelligence")

col1, col2 = st.columns(2)

with col1:
    applicant_income = st.number_input("Applicant Income", 0)
    coapplicant_income = st.number_input("Coapplicant Income", 0)
    loan_amount = st.number_input("Loan Amount", 0)
    savings = st.number_input("Savings", 0)

with col2:
    collateral_value = st.number_input("Collateral Value", 0)
    dependents = st.number_input("Dependents", 0)
    existing_loans = st.number_input("Existing Loans", 0)

credit_score = st.slider("Credit Score", 300, 900, 650)
loan_term = st.slider("Loan Term", 6, 360, 60)
age = st.slider("Age", 18, 70, 30)

employment_status = st.selectbox("Employment", ["Unemployed", "Salaried", "Self-Employed"])
employment_status = {"Unemployed":0,"Salaried":1,"Self-Employed":2}[employment_status]

property_area = st.selectbox("Property Area", ["Rural","Semi-Urban","Urban"])
property_area = {"Rural":0,"Semi-Urban":1,"Urban":2}[property_area]

loan_purpose = st.selectbox("Loan Purpose", ["Home","Car","Education","Personal"])
loan_purpose = {"Home":0,"Car":1,"Education":2,"Personal":3}[loan_purpose]

education_level = st.selectbox("Education", ["Not Graduate","Graduate"])
education_level = {"Not Graduate":0,"Graduate":1}[education_level]

gender = st.selectbox("Gender", ["Female","Male"])
gender = {"Female":0,"Male":1}[gender]

employer_category = st.selectbox("Employer", ["Private","Government","Business"])
employer_category = {"Private":0,"Government":1,"Business":2}[employer_category]

# -----------------------------------
# BUTTON
# -----------------------------------
run = st.button("Analyse Loan Application")

# -----------------------------------
# PREDICTION
# -----------------------------------
if run:
    progress_bar = st.progress(0)
    status_text = st.empty()

    steps = [
        "🔍 Collecting financial data...",
        "📊 Analyzing profile...",
        "🧠 Running AI model...",
        "⚖️ Evaluating risk...",
        "✅ Finalizing decision..."
    ]

    for i, step in enumerate(steps):
        status_text.write(step)
        progress_bar.progress((i+1)*20)
        time.sleep(0.4)

    status_text.empty()
    progress_bar.empty()

    total_income = applicant_income + coapplicant_income
    emi = calculate_emi(loan_amount, loan_term)
    emi_ratio = emi / total_income if total_income > 0 else 0

    input_data = pd.DataFrame([[  
        applicant_income, coapplicant_income, loan_amount, credit_score,
        age, dependents, existing_loans, savings, collateral_value,
        loan_term, employment_status, property_area, loan_purpose,
        education_level, gender, employer_category
    ]])

    scaled = scaler.transform(input_data)
    prediction = model.predict(scaled)
    prob = model.predict_proba(scaled)[0][1]*100

    st.write("### 📊 Financial Analysis")
    st.write(f"EMI: ₹{round(emi,2)}")
    st.write(f"Income: ₹{total_income}")
    st.write(f"EMI Ratio: {round(emi_ratio*100,2)}%")

    st.progress(int(prob))
    st.write(f"Approval Probability: {round(prob,2)}%")

    if prediction[0]==1:
        st.success("✅ Loan Approved")
    else:
        st.error("❌ Loan Rejected")

    # -----------------------------------
    # DOWNLOAD REPORT (FIXED)
    # -----------------------------------
    report = f"""
LOAN REPORT
-----------------
Income: {total_income}
Loan: {loan_amount}
EMI: {emi}
Decision: {"APPROVED" if prediction[0]==1 else "REJECTED"}
Confidence: {round(prob,2)}%
"""

    st.download_button("📄 Download Report", report, "loan_report.txt")
