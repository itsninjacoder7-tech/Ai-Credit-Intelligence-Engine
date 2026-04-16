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
# Load Model Safely
# -----------------------------------
try:
    model = pickle.load(open("loan_model.pkl", "rb"))
    scaler = pickle.load(open("scaler.pkl", "rb"))
except:
    st.error("🚨 Model or scaler file not found. Please check deployment.")
    st.stop()

# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.title("LoanSahayak")
st.sidebar.write("Smart Loan Intelligence System")
st.sidebar.markdown("---")
st.sidebar.write("**Model Version:** v1.0")
st.sidebar.write("**Last Trained:** Jan 2026")
st.sidebar.markdown("---")
st.sidebar.write("👤 Arnav Singh")

# -----------------------------------
# EMI Calculator
# -----------------------------------
def calculate_emi(principal, tenure_months, annual_rate=10):
    if principal == 0 or tenure_months == 0:
        return 0
    r = annual_rate / 12 / 100
    return (principal * r * (1 + r)**tenure_months) / ((1 + r)**tenure_months - 1)

# -----------------------------------
# Predict Function
# -----------------------------------
def predict_loan(data):
    scaled = scaler.transform(data)
    pred = model.predict(scaled)
    prob = model.predict_proba(scaled)
    return pred, prob

# -----------------------------------
# UI
# -----------------------------------
st.title("🏦 LoanSahayak — AI Loan Intelligence")

tab1, tab2 = st.tabs(["📊 Prediction", "📈 Insights"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        applicant_income = st.number_input("Applicant Income (₹)", min_value=0, step=1000)
        coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, step=1000)
        loan_amount = st.number_input("Loan Amount (₹)", min_value=0, step=1000)
        savings = st.number_input("Savings (₹)", min_value=0, step=1000)

    with col2:
        collateral_value = st.number_input("Collateral Value (₹)", min_value=0, step=1000)
        dependents = st.number_input("Dependents", min_value=0)
        existing_loans = st.number_input("Existing Loans", min_value=0)

    credit_score = st.slider("Credit Score", 300, 900, 650)
    loan_term = st.slider("Loan Term (Months)", 6, 360, 60)
    age = st.slider("Age", 18, 70, 30)

    employment = st.selectbox("Employment", ["Unemployed", "Salaried", "Self-Employed"])
    property_area = st.selectbox("Property Area", ["Rural", "Semi-Urban", "Urban"])
    education = st.selectbox("Education", ["Not Graduate", "Graduate"])
    gender = st.selectbox("Gender", ["Female", "Male"])

    # Reset Button
    if st.button("🔄 Reset"):
        st.experimental_rerun()

    run = st.button("🚀 Analyze Application")

    if run:

        # -----------------------------------
        # Validation
        # -----------------------------------
        if applicant_income <= 0:
            st.error("Income must be greater than 0")
            st.stop()

        if loan_amount <= 0:
            st.error("Loan amount must be greater than 0")
            st.stop()

        total_income = applicant_income + coapplicant_income
        emi = calculate_emi(loan_amount, loan_term)
        emi_ratio = emi / total_income if total_income > 0 else 0

        # -----------------------------------
        # Feature Engineering
        # -----------------------------------
        income_to_loan = total_income / (loan_amount + 1)
        loan_to_collateral = loan_amount / (collateral_value + 1)

        input_data = pd.DataFrame([[ 
            applicant_income, coapplicant_income, loan_amount, credit_score,
            age, dependents, existing_loans, savings, collateral_value,
            loan_term
        ]])

        # -----------------------------------
        # Prediction (with loader)
        # -----------------------------------
        with st.spinner("Analyzing financial profile..."):
            time.sleep(1)
            prediction, probability = predict_loan(input_data)

        approval_prob = probability[0][1] * 100

        # -----------------------------------
        # Metrics
        # -----------------------------------
        st.subheader("📊 Financial Analysis")
        colA, colB, colC = st.columns(3)
        colA.metric("EMI", f"₹{round(emi,2)}")
        colB.metric("Income", f"₹{total_income}")
        colC.metric("EMI Ratio", f"{round(emi_ratio*100,2)}%")

        st.progress(int(approval_prob))
        st.write(f"Approval Probability: {round(approval_prob,2)}%")

        # -----------------------------------
        # Result
        # -----------------------------------
        if prediction[0] == 1:
            st.success("✅ Loan Approved")
        else:
            st.error("❌ Loan Rejected")
            suggested = int(loan_amount * 0.7)
            st.info(f"💡 Try reducing loan to ₹{suggested}")

        # -----------------------------------
        # Risk Score
        # -----------------------------------
        risk_score = 0
        if emi_ratio > 0.4: risk_score += 2
        if credit_score < 650: risk_score += 2
        if existing_loans > 1: risk_score += 1
        if savings < loan_amount * 0.1: risk_score += 1

        st.subheader("📌 Risk Assessment")
        if risk_score >= 4:
            st.error("High Risk")
        elif risk_score >= 2:
            st.warning("Moderate Risk")
        else:
            st.success("Low Risk")

        # -----------------------------------
        # Download Report
        # -----------------------------------
        report = f"""
Loan Report
-----------
Income: {total_income}
Loan: {loan_amount}
Decision: {"Approved" if prediction[0]==1 else "Rejected"}
Probability: {approval_prob}
"""
        st.download_button("📄 Download Report", report)

with tab2:
    st.subheader("📈 Insights")

    # Dummy feature importance (if model supports)
    try:
        importances = model.feature_importances_
        features = ["Income", "Loan", "Credit", "Age", "Dependents",
                    "Loans", "Savings", "Collateral", "Term"]

        df = pd.DataFrame({
            "Feature": features,
            "Importance": importances[:len(features)]
        }).sort_values(by="Importance", ascending=False)

        st.bar_chart(df.set_index("Feature"))

    except:
        st.info("Feature importance not available for this model")

# -----------------------------------
# Footer
# -----------------------------------
st.markdown("---")
st.caption("© 2026 LoanSahayak — AI Credit Intelligence")
