import streamlit as st
import pandas as pd
import pickle
import numpy as np

# -----------------------------
# PAGE CONFIG (FIXED)
# -----------------------------
st.set_page_config(
    page_title="LoanSahayak — Smart Loan Intelligence",
    page_icon="🏦",
    layout="wide"
)

# -----------------------------
# LOAD MODEL & SCALER (IMPORTANT)
# -----------------------------
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# -----------------------------
# EMI FUNCTION
# -----------------------------
def calculate_emi(principal, tenure_months, annual_rate=10):
    if principal == 0 or tenure_months == 0:
        return 0
    monthly_rate = annual_rate / 12 / 100
    emi = (principal * monthly_rate * (1 + monthly_rate)**tenure_months) / \
          ((1 + monthly_rate)**tenure_months - 1)
    return emi

# -----------------------------
# HEADER
# -----------------------------
st.title("💰 LoanSahayak — Smart Loan Intelligence")
st.markdown("AI-Powered Loan Approval Prediction System")

# -----------------------------
# INPUT SECTION (CLEANED)
# -----------------------------
st.subheader("💼 Financial Details")

col1, col2 = st.columns(2)

with col1:
    applicant_income = st.number_input("Applicant Income (₹)", min_value=0)
    coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0)
    loan_amount = st.number_input("Loan Amount (₹)", min_value=0)
    savings = st.number_input("Savings (₹)", min_value=0)

with col2:
    collateral_value = st.number_input("Collateral Value (₹)", min_value=0)
    dependents = st.number_input("Dependents", min_value=0)
    existing_loans = st.number_input("Existing Loans", min_value=0)
    loan_term = st.slider("Loan Term (Months)", 6, 360, 60)

st.subheader("📊 Personal Details")

col3, col4 = st.columns(2)

with col3:
    credit_score = st.slider("Credit Score", 300, 900, 650)
    age = st.slider("Age", 18, 70, 30)

    employment_dict = {"Unemployed":0,"Salaried":1,"Self-Employed":2}
    employment_status = employment_dict[st.selectbox("Employment Status", employment_dict.keys())]

    property_dict = {"Rural":0,"Semi-Urban":1,"Urban":2}
    property_area = property_dict[st.selectbox("Property Area", property_dict.keys())]

with col4:
    education_dict = {"Not Graduate":0,"Graduate":1}
    education_level = education_dict[st.selectbox("Education Level", education_dict.keys())]

    gender_dict = {"Female":0,"Male":1}
    gender = gender_dict[st.selectbox("Gender", gender_dict.keys())]

    employer_dict = {"Private Sector":0,"Government":1,"Business Owner":2}
    employer_category = employer_dict[st.selectbox("Employer Category", employer_dict.keys())]

    loan_purpose_dict = {
        "Home Loan":0,"Car Loan":1,"Education Loan":2,"Personal Loan":3
    }
    loan_purpose = loan_purpose_dict[st.selectbox("Loan Purpose", loan_purpose_dict.keys())]

# -----------------------------
# BUTTON (FIXED)
# -----------------------------
if st.button("🔎 Analyze Loan Application"):

    total_income = applicant_income + coapplicant_income
    emi = calculate_emi(loan_amount, loan_term)
    emi_ratio = emi / total_income if total_income > 0 else 0

    # -----------------------------
    # DATAFRAME
    # -----------------------------
    input_data = pd.DataFrame([[
        applicant_income, coapplicant_income, loan_amount, credit_score,
        age, dependents, existing_loans, savings, collateral_value,
        loan_term, employment_status, property_area, loan_purpose,
        education_level, gender, employer_category
    ]], columns=[
        'Applicant_Income','Coapplicant_Income','Loan_Amount','Credit_Score',
        'Age','Dependents','Existing_Loans','Savings','Collateral_Value',
        'Loan_Term','Employment_Status','Property_Area','Loan_Purpose',
        'Education_Level','Gender','Employer_Category'
    ])

    scaled_data = scaler.transform(input_data)

    prediction = model.predict(scaled_data)
    probability = model.predict_proba(scaled_data)[0][1] * 100

    # -----------------------------
    # OUTPUT
    # -----------------------------
    st.subheader("📊 Financial Summary")
    colA, colB, colC = st.columns(3)
    colA.metric("EMI", f"₹ {round(emi,2)}")
    colB.metric("Total Income", f"₹ {total_income}")
    colC.metric("EMI Ratio", f"{round(emi_ratio*100,2)}%")

    st.subheader("🧠 Prediction Result")

    if prediction[0] == 1:
        st.success(f"✅ Loan Approved (Confidence: {round(probability,2)}%)")
        risk = "Low Risk"
    elif probability > 40:
        st.warning(f"⚠ Conditional Approval (Confidence: {round(probability,2)}%)")
        risk = "Medium Risk"
    else:
        st.error(f"❌ Loan Rejected (Confidence: {round(100-probability,2)}%)")
        risk = "High Risk"

    st.write(f"### Risk Level: {risk}")

    # -----------------------------
    # INSIGHTS
    # -----------------------------
    st.subheader("📌 Insights")

    if emi_ratio > 0.5:
        st.warning("High EMI-to-income ratio → financial stress risk")
    elif credit_score < 600:
        st.warning("Low credit score → high default probability")
    elif existing_loans > 2:
        st.warning("Too many active loans → high debt burden")
    else:
        st.info("Stable financial profile ✅")
