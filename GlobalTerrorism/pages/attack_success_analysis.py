import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

def show():
    st.title("Attack Success Analysis")
    
    data = load_data()
    
    # Success rate trends over time
    st.subheader("Success Rate Trends Over Time")
    yearly_success = data.groupby('iyear')['success'].mean().reset_index()
    fig = px.line(yearly_success, x='iyear', y='success')
    st.plotly_chart(fig)
    
    # Success rates across attack types
    st.subheader("Success Rates Across Attack Types")
    attack_type_success = data.groupby('attacktype1_txt')['success'].mean().sort_values(ascending=False)
    fig = px.bar(attack_type_success, x=attack_type_success.index, y=attack_type_success.values)
    st.plotly_chart(fig)