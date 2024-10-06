import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
import pandas as pd

# Set page config
st.set_page_config(page_title="Global Terrorism Dashboard", layout="wide")

# Define color scheme
COLOR_SCHEME = {
    "primary": "#8B0000",  # Dark Red
    "secondary": "#B22222",  # Firebrick
    "tertiary": "#CD5C5C",  # Indian Red
    "background": "#FFF5EE",  # Seashell
    "text": "#2F4F4F"  # Dark Slate Gray
}

# Apply the color scheme to Streamlit
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background-color: {COLOR_SCHEME["background"]};
        color: {COLOR_SCHEME["text"]};
    }}
    .sidebar .sidebar-content {{
        background-color: {COLOR_SCHEME["background"]};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

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

# Sidebar for global filters
st.sidebar.header("Global Filters")
start_year, end_year = st.sidebar.slider(
    "Select Year Range",
    min_value=int(yearly_stats.index.min()),
    max_value=int(yearly_stats.index.max()),
    value=(int(yearly_stats.index.min()), int(yearly_stats.index.max()))
)

# Filter data based on selected year range
filtered_stats = yearly_stats[(yearly_stats.index >= start_year) & (yearly_stats.index <= end_year)]

# Create tabs for different sections
tab1, tab2 = st.tabs(["Global Analysis", "Unknown Groups Analysis"])

# Tab 1: Global Analysis
with tab1:
    st.title("Global Terrorism Dashboard")

    # Overview metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attacks", f"{filtered_stats['total_attacks'].sum():,}")
    with col2:
        st.metric("Average Success Rate", f"{filtered_stats['success_rate'].mean():.2%}")
    with col3:
        st.metric("Average Failure Rate", f"{filtered_stats['failure_rate'].mean():.2%}")

    # Time series plot
    st.subheader("Terrorist Attacks Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_stats.index, y=filtered_stats['total_attacks'],
                             mode='lines', name='Total Attacks', line=dict(color=COLOR_SCHEME["primary"])))
    fig.add_trace(go.Scatter(x=filtered_stats.index, y=filtered_stats['success_rate'],
                             mode='lines', name='Success Rate', yaxis='y2', line=dict(color=COLOR_SCHEME["secondary"])))
    fig.update_layout(
        title='Number of Terrorist Attacks and Success Rate by Year',
        yaxis=dict(title='Number of Attacks'),
        yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1]),
        plot_bgcolor=COLOR_SCHEME["background"],
        paper_bgcolor=COLOR_SCHEME["background"],
        font=dict(color=COLOR_SCHEME["text"])
    )
    st.plotly_chart(fig, use_container_width=True)

    # Success vs Failure Rate Over Time
    st.subheader("Success vs Failure Rate Over Time")
    fig_success_failure = px.area(filtered_stats, x=filtered_stats.index, 
                                  y=['success_rate', 'failure_rate'],
                                  title='Success vs Failure Rate Over Time',
                                  labels={'value': 'Rate', 'variable': 'Type'},
                                  color_discrete_map={'success_rate': COLOR_SCHEME["secondary"], 'failure_rate': COLOR_SCHEME["tertiary"]})
    fig_success_failure.update_layout(
        plot_bgcolor=COLOR_SCHEME["background"],
        paper_bgcolor=COLOR_SCHEME["background"],
        font=dict(color=COLOR_SCHEME["text"])
    )
    st.plotly_chart(fig_success_failure, use_container_width=True)

    # Top Groups Analysis
    st.subheader("Top Terrorist Groups Analysis")
    selected_year = st.selectbox('Select Year for Top Groups', sorted(filtered_stats.index, reverse=True))

    @st.cache_data
    def get_top_groups(year):
        year_data = df[df.iyear == year].compute()
        top_groups = year_data['gname'].value_counts().nlargest(10)
        success_rates = year_data.groupby('gname')['success'].mean()
        top_groups_success = success_rates[top_groups.index]
        return pd.DataFrame({'Attacks': top_groups, 'Success Rate': top_groups_success})

    top_groups = get_top_groups(selected_year)

    # Create a bar chart for top groups
    fig_top_groups = go.Figure()
    fig_top_groups.add_trace(go.Bar(x=top_groups.index, y=top_groups['Attacks'],
                                    name='Number of Attacks', yaxis='y', marker_color=COLOR_SCHEME["primary"]))
    fig_top_groups.add_trace(go.Scatter(x=top_groups.index, y=top_groups['Success Rate'],
                                        mode='markers', name='Success Rate', yaxis='y2', marker=dict(color=COLOR_SCHEME["secondary"], size=10)))
    fig_top_groups.update_layout(
        title=f'Top 10 Active Groups in {selected_year}',
        yaxis=dict(title='Number of Attacks'),
        yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1]),
        xaxis=dict(tickangle=45),
        plot_bgcolor=COLOR_SCHEME["background"],
        paper_bgcolor=COLOR_SCHEME["background"],
        font=dict(color=COLOR_SCHEME["text"])
    )
    st.plotly_chart(fig_top_groups, use_container_width=True)

    # Add a data table for more detailed information
    st.subheader(f"Detailed Information for Top Groups in {selected_year}")
    st.dataframe(top_groups.style.format({'Attacks': '{:,}', 'Success Rate': '{:.2%}'}))

# Tab 2: Unknown Groups Analysis
with tab2:
    st.title("Analysis of Attacks by Unknown Groups")

    # Filter data for unknown groups
    @st.cache_data
    def get_unknown_groups_data():
        unknown_groups_data = df[df['gname'] == 'Unknown'].compute()
        return unknown_groups_data

    unknown_groups_data = get_unknown_groups_data()

    # Yearly stats for unknown groups
    @st.cache_data
    def get_unknown_group_yearly_stats():
        unknown_stats = unknown_groups_data.groupby('iyear').agg({
            'iyear': 'count',
            'success': 'mean'
        })
        unknown_stats.columns = ['total_attacks', 'success_rate']
        unknown_stats['failure_rate'] = 1 - unknown_stats['success_rate']
        return unknown_stats

    unknown_stats = get_unknown_group_yearly_stats()

    # Overview metrics for unknown groups
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Attacks by Unknown Groups", f"{unknown_stats['total_attacks'].sum():,}")
    with col2:
        st.metric("Average Success Rate", f"{unknown_stats['success_rate'].mean():.2%}")
    with col3:
        st.metric("Average Failure Rate", f"{unknown_stats['failure_rate'].mean():.2%}")

    # Visualization: Terrorist Attacks Over Time by Unknown Groups
    st.subheader("Terrorist Attacks Over Time by Unknown Groups")
    fig_unknown = go.Figure()
    fig_unknown.add_trace(go.Scatter(x=unknown_stats.index, y=unknown_stats['total_attacks'],
                                     mode='lines', name='Total Attacks', line=dict(color=COLOR_SCHEME["primary"])))
    fig_unknown.add_trace(go.Scatter(x=unknown_stats.index, y=unknown_stats['success_rate'],
                                     mode='lines', name='Success Rate', yaxis='y2', line=dict(color=COLOR_SCHEME["secondary"])))
    fig_unknown.update_layout(
        title='Number of Attacks and Success Rate by Unknown Groups (Yearly)',
        yaxis=dict(title='Number of Attacks'),
        yaxis2=dict(title='Success Rate', overlaying='y', side='right', range=[0, 1]),
        plot_bgcolor=COLOR_SCHEME["background"],
        paper_bgcolor=COLOR_SCHEME["background"],
        font=dict(color=COLOR_SCHEME["text"])
    )
    st.plotly_chart(fig_unknown, use_container_width=True)

    # Detailed data table for unknown groups
    st.subheader("Detailed Information for Unknown Groups")
    st.dataframe(unknown_groups_data)

