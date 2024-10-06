import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import dask.dataframe as dd
import pandas as pd

# Set page config
st.set_page_config(page_title="Terrorist Attack Success Rate Analysis", layout="wide")

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

# Main content
st.title("Factors Influencing Terrorist Attack Success Rates")

# Function to get success rates by various factors
@st.cache_data
def get_success_rates_by_factor(factor):
    success_rates = df.groupby(factor)['success'].mean().compute().sort_values(ascending=False)
    return success_rates

# Factor selection
factor = st.selectbox("Select a factor to analyze", 
                      ["attacktype1_txt", "targtype1_txt", "weaptype1_txt", "region_txt"])

success_rates_by_factor = get_success_rates_by_factor(factor)

# Visualize success rates by selected factor
fig_success_by_factor = px.bar(
    success_rates_by_factor,
    x=success_rates_by_factor.index,
    y=success_rates_by_factor.values,
    title=f'Success Rates by {factor.replace("_txt", "").title()}',
    labels={'y': 'Success Rate', 'x': factor.replace("_txt", "").title()},
    color=success_rates_by_factor.values,
    color_continuous_scale=px.colors.sequential.Reds
)
fig_success_by_factor.update_layout(
    xaxis_tickangle=-45,
    plot_bgcolor=COLOR_SCHEME["background"],
    paper_bgcolor=COLOR_SCHEME["background"],
    font=dict(color=COLOR_SCHEME["text"])
)
st.plotly_chart(fig_success_by_factor, use_container_width=True)

# Success rate over time for top categories in selected factor
st.subheader(f"Success Rate Trends for Top {factor.replace('_txt', '').title()} Categories")

top_categories = success_rates_by_factor.nlargest(5).index.tolist()  # Convert to list

@st.cache_data
def get_success_rate_trends(factor, categories):
    trends = df[df[factor].isin(categories)].groupby(['iyear', factor])['success'].mean().compute().unstack()
    return trends

trends = get_success_rate_trends(factor, top_categories)

fig_trends = px.line(
    trends,
    x=trends.index,
    y=trends.columns,
    title=f'Success Rate Trends for Top 5 {factor.replace("_txt", "").title()} Categories',
    labels={'x': 'Year', 'y': 'Success Rate', 'variable': factor.replace("_txt", "").title()},
    color_discrete_sequence=px.colors.qualitative.Set1
)
fig_trends.update_layout(
    plot_bgcolor=COLOR_SCHEME["background"],
    paper_bgcolor=COLOR_SCHEME["background"],
    font=dict(color=COLOR_SCHEME["text"])
)
st.plotly_chart(fig_trends, use_container_width=True)

# Correlation analysis
st.subheader("Correlation Analysis")

numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns
correlation_columns = st.multiselect(
    "Select columns for correlation analysis",
    options=numeric_columns,
    default=['success', 'nkill', 'nwound']
)

@st.cache_data
def get_correlation_matrix(columns):
    return df[columns].corr().compute()

if correlation_columns:
    corr_matrix = get_correlation_matrix(correlation_columns)
    fig_corr = px.imshow(
        corr_matrix,
        color_continuous_scale='RdBu_r',
        title='Correlation Matrix',
        zmin=-1,
        zmax=1
    )
    fig_corr.update_layout(
        plot_bgcolor=COLOR_SCHEME["background"],
        paper_bgcolor=COLOR_SCHEME["background"],
        font=dict(color=COLOR_SCHEME["text"])
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.write("Interpretation of correlations:")
    for col1 in correlation_columns:
        for col2 in correlation_columns:
            if col1 != col2:
                corr = corr_matrix.loc[col1, col2]
                st.write(f"- Correlation between {col1} and {col2}: {corr:.2f}")

# Footer
st.markdown("---")
st.markdown("Data source: Global Terrorism Database")
st.markdown("Dashboard created with Streamlit and Plotly")