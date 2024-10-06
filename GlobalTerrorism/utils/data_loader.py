import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    """
    Load and preprocess the terrorism dataset.
    Uses Streamlit's caching to avoid reloading on every rerun.
    """
    # Adjust the path as necessary
    df = pd.read_csv('/Users/saitejasriyerramsetti/Documents/Globalterror/GlobalTerrorism/Data/success_failure_data.csv')
    
    # Preprocessing steps
    df['iyear'] = pd.to_datetime(df['iyear'], format='%Y')
    df['success'] = df['success'].astype(bool)
    
    # Handle missing values
    df['nkill'] = df['nkill'].fillna(0)
    df['nwound'] = df['nwound'].fillna(0)
    
    # Convert 'multiple' and 'suicide' to boolean
    df['multiple'] = df['multiple'].astype(bool)
    df['suicide'] = df['suicide'].astype(bool)
    
    return df

def filter_data(df, start_year=None, end_year=None, countries=None, attack_types=None):
    """
    Filter the dataset based on user selections.
    """
    if start_year:
        df = df[df['iyear'].dt.year >= start_year]
    if end_year:
        df = df[df['iyear'].dt.year <= end_year]
    if countries:
        df = df[df['country_txt'].isin(countries)]
    if attack_types:
        df = df[df['attacktype1_txt'].isin(attack_types)]
    return df