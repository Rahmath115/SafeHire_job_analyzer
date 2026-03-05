import streamlit as st

def show_input_page():
    st.title("SafeHire - Job Trust Analyzer")

    st.subheader("Enter Job Details")

    job_link = st.text_input("Job Posting Link (Optional)")
    company_name = st.text_input("Company Name")
    role = st.text_input("Job Role")
    job_description = st.text_area("Job Description")

    analyze = st.button("Analyze Job")

    if analyze:
        if company_name and role and job_description: 
            st.session_state["job_link"] = job_link
            st.session_state["company_name"] = company_name
            st.session_state["role"] = role
            st.session_state["job_description"] = job_description
            st.session_state["page"] = "result"
        else:
            st.warning("Please fill Company Name and role and Job Description")