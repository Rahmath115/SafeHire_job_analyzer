import streamlit as st
import pickle

# ===== LOAD AI MODEL =====
with open("models/job_model.pkl", "rb") as f:
    ai_model = pickle.load(f)

with open("models/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

def show_result_page():

    trust_score = 50
    positive_reasons = []
    negative_reasons = []

    st.title("SafeHire - AI Job Trust Analyzer")

    company = st.session_state.get("company_name", "")
    role = st.session_state.get("role", "")
    description = st.session_state.get("job_description", "")

    st.subheader("📄 Job Summary")
    st.write(f"Company: {company}")
    st.write(f"Role: {role}")
    st.write(f"Description: {description}")

    description_lower = description.lower()
    company_lower = company.lower()

    # ===== RISK DETECTION =====
    if "no registration fee" in description_lower:
     risk_flag = False
    else:
     risk_flag = any(word in description_lower for word in [
        "registration fee", "payment", "pay fee", "interview fee"
    ])

    earning_scam = (
        "earn" in description_lower and
        ("daily" in description_lower or "weekly" in description_lower or "monthly" in description_lower)
    )

    unskilled_high_income = (
        "no experience" in description_lower and
        ("earn" in description_lower or "salary" in description_lower)
    )

    mass_hiring = any(word in description_lower for word in [
        "urgent hiring", "mass hiring", "immediate joining"
    ])

    # ===== AI PREDICTION =====
    desc_vector = vectorizer.transform([description])
    ai_prediction = ai_model.predict(desc_vector)[0]

    # ===== COMPANY VERIFICATION =====
    company_verified = any(word in company_lower for word in [
        "pvt", "ltd", "limited", "inc", "llp", "solutions", "technologies"
    ])

    # ===== COMPANY CLASSIFICATION =====
    if any(word in company_lower for word in ["ngo", "foundation", "trust", "society"]):
        company_type = "NGO"

    elif any(word in company_lower for word in ["startup", "labs", "ventures", "innovations"]):
        company_type = "Startup"

    elif any(word in company_lower for word in ["gov", "government", "ministry", "india", "department"]):
        company_type = "Government"

    elif any(word in company_lower for word in ["pvt", "ltd", "limited", "inc", "solutions", "technologies"]):
        company_type = "Corporate"

    else:
        company_type = "Unknown"

    # ===== TRUST LOGIC =====
    if ai_prediction == 0:
        trust_score -= 20
        negative_reasons.append("⚠ AI detected suspicious hiring pattern")
    else:
        positive_reasons.append("✔ AI found job pattern realistic")

    if risk_flag:
        trust_score -= 30
        negative_reasons.append("⚠ Asking for payment / registration fee")
    else:
        positive_reasons.append("✔ No payment risk detected")

    if earning_scam:
        trust_score -= 25
        negative_reasons.append("⚠ Unrealistic earning promise")

    if unskilled_high_income:
        trust_score -= 30
        negative_reasons.append("⚠ High income with no skills")

    if mass_hiring:
        trust_score -= 15
        negative_reasons.append("⚠ Mass hiring pressure detected")

    if company_verified:
        positive_reasons.append("✔ Company verified")
    else:
        trust_score -= 10
        negative_reasons.append("⚠ Company not verified")

    # ===== UI OUTPUT =====
    st.subheader("🔍 Trust Analysis")

    col1, col2, col3 = st.columns(3)

    if company_verified:
        col1.success("Company Verified")
    else:
        col1.error("Company Not Verified")

    if ai_prediction == 1:
        col2.success("Role Looks Realistic")
    else:
        col2.warning("Unrealistic Role")

    if not risk_flag:
        col3.success("No Risk Signals")
    else:
        col3.error("Payment Risk Found")

    st.subheader("🏢 Company Classification")
    st.info(company_type)

    st.subheader("📌 Positive Signals")
    for reason in positive_reasons:
        st.success(reason)

    st.subheader("⚠ Risk Signals")
    for reason in negative_reasons:
        st.error(reason)

    st.subheader("📊 Final Trust Score")

    if trust_score >= 70:
        st.success(f"Trust Score: {trust_score}% (Safe)")
    elif trust_score >= 40:
        st.warning(f"Trust Score: {trust_score}% (Moderate Risk)")
    else:
        st.error(f"Trust Score: {trust_score}% (High Risk)")

    if st.button("⬅ Back"):
        st.session_state.page = "input"