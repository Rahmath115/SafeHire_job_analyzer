import streamlit as st
from input_page import show_input_page
from result_page import show_result_page

# Page settings
st.set_page_config(
    page_title="SafeHire",
    page_icon="🛡️",
    layout="centered"
)

# Theme styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #0E1A2B;
}

h1, h2, h3 {
    color: #00C2A8;
}

.stButton>button {
    background-color: #00C2A8;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# Navigation logic
if "page" not in st.session_state:
    st.session_state["page"] = "input"

if st.session_state["page"] == "input":
    show_input_page()
elif st.session_state["page"] == "result":
    show_result_page()
