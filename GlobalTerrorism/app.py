import streamlit as st
from pages import overview, perpetrator_analysis, target_analysis, attack_success_analysis, predictive_analysis

st.set_page_config(page_title="Terrorism Analysis Dashboard", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Overview", "Perpetrator Analysis", "Target Analysis", "Attack Success Analysis", "Predictive Analysis"])

if page == "Overview":
    overview.show()
elif page == "Perpetrator Analysis":
    perpetrator_analysis.show()
elif page == "Target Analysis":
    target_analysis.show()
elif page == "Attack Success Analysis":
    attack_success_analysis.show()
elif page == "Predictive Analysis":
    predictive_analysis.show()
    