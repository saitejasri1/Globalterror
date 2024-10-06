import streamlit as st
import plotly.express as px
from utils.data_loader import load_data
from utils.visualization import create_yearly_trend_chart

def show():
    st.title("Terrorism Analysis Overview")
    
    data = load_data()
    
    # Yearly trend of attacks
    st.subheader("Yearly Trend of Attacks")
    fig = create_yearly_trend_chart(data)
    st.plotly_chart(fig)
    
    # Top 10 countries with most attacks
    st.subheader("Top 10 Countries with Most Attacks")
    top_countries = data['country_txt'].value_counts().head(10)
    fig = px.bar(top_countries, x=top_countries.index, y=top_countries.values)
    st.plotly_chart(fig)
    
    # Attack types distribution
    st.subheader("Attack Types Distribution")
    attack_types = data['attacktype1_txt'].value_counts()
    fig = px.pie(attack_types, values=attack_types.values, names=attack_types.index)
    st.plotly_chart(fig)