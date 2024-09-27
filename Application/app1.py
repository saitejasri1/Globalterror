import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
import pandas as pd

st.set_page_config(page_title="Terrorism Analysis: Success Rates and Perpetrators", layout="wide")

@st.cache_data
def load_data():
    df = dd.read_csv('/Users/saitejasriyerramsetti/Documents/Globalterror/Data/success_failure_data.csv')
    return df

df = load_data()

st.title("Terrorism Analysis: Success Rates and Perpetrator Profiles")

# Success Rate Over Time
@st.cache_data
def get_yearly_success_rate():
    return df.groupby('iyear')['success'].mean().compute()

yearly_success_rate = get_yearly_success_rate()
fig_success_time = px.line(x=yearly_success_rate.index, y=yearly_success_rate.values,
                           title='Success Rate of Attacks Over Time',
                           labels={'x': 'Year', 'y': 'Success Rate'})
st.plotly_chart(fig_success_time, use_container_width=True)

# Success Rate by Attack Type
@st.cache_data
def get_attack_type_success():
    return df.groupby('attacktype1_txt')['success'].mean().compute()

attack_type_success = get_attack_type_success()
fig_attack_type = px.bar(x=attack_type_success.index, y=attack_type_success.values,
                         title='Success Rate by Attack Type',
                         labels={'x': 'Attack Type', 'y': 'Success Rate'})
st.plotly_chart(fig_attack_type, use_container_width=True)

# Top Perpetrator Groups
st.subheader("Top Perpetrator Groups Analysis")
selected_year = st.selectbox('Select Year', sorted(df.iyear.unique().compute()))

@st.cache_data
def get_top_groups(year):
    year_data = df[df.iyear == year].compute()
    top_groups = year_data['gname'].value_counts().nlargest(10)
    success_rates = year_data.groupby('gname')['success'].mean()
    top_groups_success = success_rates[top_groups.index]
    return pd.DataFrame({'Attacks': top_groups, 'Success Rate': top_groups_success})

top_groups = get_top_groups(selected_year)
fig_top_groups = go.Figure()
fig_top_groups.add_trace(go.Bar(x=top_groups.index, y=top_groups['Attacks'],
                                name='Number of Attacks', yaxis='y'))
fig_top_groups.add_trace(go.Scatter(x=top_groups.index, y=top_groups['Success Rate'],
                                    mode='markers', name='Success Rate', yaxis='y2'))
fig_top_groups.update_layout(
    title=f'Top 10 Active Groups in {selected_year}',
    yaxis=dict(title='Number of Attacks'),
    yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1]),
    xaxis=dict(tickangle=45)
)
st.plotly_chart(fig_top_groups, use_container_width=True)

# Target Type Analysis
@st.cache_data
def get_target_type_analysis():
    target_counts = df['targtype1_txt'].value_counts().compute()
    target_success = df.groupby('targtype1_txt')['success'].mean().compute()
    return pd.DataFrame({'Count': target_counts, 'Success Rate': target_success})

target_analysis = get_target_type_analysis()
fig_targets = go.Figure()
fig_targets.add_trace(go.Bar(x=target_analysis.index, y=target_analysis['Count'],
                             name='Number of Attacks', yaxis='y'))
fig_targets.add_trace(go.Scatter(x=target_analysis.index, y=target_analysis['Success Rate'],
                                 mode='markers', name='Success Rate', yaxis='y2'))
fig_targets.update_layout(
    title='Target Type Analysis',
    yaxis=dict(title='Number of Attacks'),
    yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1]),
    xaxis=dict(tickangle=45)
)
st.plotly_chart(fig_targets, use_container_width=True)

# Regional Success Rate Map
@st.cache_data
def get_country_success_rates():
    return df.groupby('country_txt')['success'].mean().compute()

country_success = get_country_success_rates()
fig_map = px.choropleth(locations=country_success.index, 
                        locationmode="country names",
                        color=country_success.values,
                        hover_name=country_success.index,
                        color_continuous_scale="Viridis",
                        title="Success Rates by Country")
st.plotly_chart(fig_map, use_container_width=True)

st.write("Note: This dashboard presents sensitive information about global terrorism. "
         "Please interpret the data responsibly and in the appropriate context.")