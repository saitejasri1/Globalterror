import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
import pandas as pd

# Load your data with Dask
@st.cache_data
def load_data():
    df = dd.read_csv('/Users/saitejasriyerramsetti/Documents/Globalterror/Data/success_failure_data.csv')
    return df

df = load_data()

# Compute aggregations with Dask
@st.cache_data
def get_yearly_stats():
    yearly_stats = df.groupby('iyear').agg({
        'iyear': 'count',
        'success': 'mean'
    }).compute()
    yearly_stats.columns = ['total_attacks', 'success_rate']
    yearly_stats['failure_rate'] = 1 - yearly_stats['success_rate']
    return yearly_stats

yearly_stats = get_yearly_stats()

# Create the main plot with Plotly
fig = go.Figure()
fig.add_trace(go.Scatter(x=yearly_stats.index, y=yearly_stats['total_attacks'],
                         mode='lines', name='Total Attacks'))
fig.add_trace(go.Scatter(x=yearly_stats.index, y=yearly_stats['success_rate'],
                         mode='lines', name='Success Rate', yaxis='y2'))
fig.update_layout(
    title='Number of Terrorist Attacks and Success Rate by Year',
    yaxis=dict(title='Number of Attacks'),
    yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1])
)

# Display the plot in Streamlit
st.plotly_chart(fig, use_container_width=True)

# Add interactivity
start_year = st.slider('Start Year', min_value=yearly_stats.index.min(), 
                       max_value=yearly_stats.index.max())
filtered_stats = yearly_stats[yearly_stats.index >= start_year]

# Update the plot with filtered data
fig_filtered = go.Figure()
fig_filtered.add_trace(go.Scatter(x=filtered_stats.index, y=filtered_stats['total_attacks'],
                                  mode='lines', name='Total Attacks'))
fig_filtered.add_trace(go.Scatter(x=filtered_stats.index, y=filtered_stats['success_rate'],
                                  mode='lines', name='Success Rate', yaxis='y2'))
fig_filtered.update_layout(
    title=f'Attacks and Success Rate from {start_year} onwards',
    yaxis=dict(title='Number of Attacks'),
    yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1])
)
st.plotly_chart(fig_filtered, use_container_width=True)

# Display top groups for a selected year
selected_year = st.selectbox('Select Year for Top Groups', yearly_stats.index)

@st.cache_data
def get_top_groups(year):
    year_data = df[df.iyear == year].compute()
    top_groups = year_data['gname'].value_counts().nlargest(10)
    success_rates = year_data.groupby('gname')['success'].mean()
    top_groups_success = success_rates[top_groups.index]
    return pd.DataFrame({'Attacks': top_groups, 'Success Rate': top_groups_success})

top_groups = get_top_groups(selected_year)
st.write(f"Top 10 Active Groups in {selected_year}")

# Create a bar chart for top groups
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

# Success vs Failure Rate Over Time
st.write("Success vs Failure Rate Over Time")
fig_success_failure = px.area(yearly_stats, x=yearly_stats.index, 
                              y=['success_rate', 'failure_rate'],
                              title='Success vs Failure Rate Over Time',
                              labels={'value': 'Rate', 'variable': 'Type'})
st.plotly_chart(fig_success_failure, use_container_width=True)