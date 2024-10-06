import streamlit as st
import plotly.express as px
from utils.data_loader import load_data

def show():
    st.title("Perpetrator Analysis")
    
    data = load_data()
    
    # Top 10 most active terrorist groups
    st.subheader("Top 10 Most Active Terrorist Groups")
    top_groups = data['gname'].value_counts().head(10)
    fig = px.bar(top_groups, x=top_groups.index, y=top_groups.values)
    st.plotly_chart(fig)
    
    # Temporal patterns of group activities
    st.subheader("Temporal Patterns of Group Activities")
    selected_group = st.selectbox("Select a group", data['gname'].unique())
    group_data = data[data['gname'] == selected_group]
    yearly_activity = group_data.groupby('iyear').size().reset_index(name='count')
    fig = px.line(yearly_activity, x='iyear', y='count')
    st.plotly_chart(fig)