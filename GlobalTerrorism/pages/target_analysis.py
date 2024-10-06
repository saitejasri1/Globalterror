import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

def show():
    st.title("Target Analysis")
    
    data = load_data()
    
    # Target type frequency analysis
    st.subheader("Target Type Frequency Analysis")
    target_types = data['targtype1_txt'].value_counts()
    fig = px.pie(target_types, values=target_types.values, names=target_types.index)
    st.plotly_chart(fig)
    
    # Cross-analysis of target types with casualty rates
    st.subheader("Casualty Rates by Target Type")
    target_casualties = data.groupby('targtype1_txt')[['nkill', 'nwound']].mean().reset_index()
    fig = px.bar(target_casualties, x='targtype1_txt', y=['nkill', 'nwound'], barmode='group')
    st.plotly_chart(fig)