import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.express as px
from utils.data_loader import load_data

def show():
    st.title("Predictive Analysis")

    # Load data
    data = load_data()
    if data is None:
        st.error("Failed to load data. Please check your data file.")
        return

    # Display data info
    st.subheader("Dataset Information")
    st.write("Columns in the dataset:", data.columns.tolist())
    st.write("Data types of columns:", data.dtypes)

    # Time Series Analysis
    st.header("1. Time Series Analysis for Attack Success after 2021")
    try:
        success_ts = data.groupby('iyear')['success'].mean()
        model = ARIMA(success_ts, order=(1,1,1))
        results = model.fit()
        forecast = results.get_forecast(steps=5)  # Forecast 5 years ahead
        forecast_mean = forecast.predicted_mean
        forecast_conf_int = forecast.conf_int()

        fig, ax = plt.subplots()
        ax.plot(success_ts.index, success_ts, label='Historical')
        ax.plot(forecast_mean.index, forecast_mean, label='Forecast')
        ax.fill_between(forecast_mean.index, forecast_conf_int.iloc[:,0], forecast_conf_int.iloc[:,1], alpha=0.2)
        ax.set_title('Forecast of Attack Success Rate')
        ax.legend()
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error in Time Series Analysis: {str(e)}")
        st.write("Data range:", success_ts.index.min(), "to", success_ts.index.max())
        st.write("Success rate data:", success_ts)

    # Predicting Active Weapons
    st.header("2. Predicting Active Weapons")
    try:
        # Convert 'iyear' to numeric if it's datetime
        if pd.api.types.is_datetime64_any_dtype(data['iyear']):
            data['iyear'] = data['iyear'].dt.year

        # Encode 'country_txt' as it's categorical
        le = LabelEncoder()
        data['country_encoded'] = le.fit_transform(data['country_txt'])

        # Select only numeric columns for X
        numeric_columns = ['iyear', 'imonth', 'country_encoded']
        X = data[numeric_columns]
        y = data['weaptype1_txt']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        rf_model = RandomForestClassifier(random_state=42)
        rf_model.fit(X_train, y_train)

        # Predict for future years
        last_year = data['iyear'].max()
        future_years = pd.DataFrame({
            'iyear': range(last_year + 1, last_year + 6),
            'imonth': 1,
            'country_encoded': le.transform(['United States']*5)
        })
        predictions = rf_model.predict(future_years)

        st.write("Predicted weapon types for future years:", predictions)
    except Exception as e:
        st.error(f"Error in Predicting Active Weapons: {str(e)}")

    # Cities/Locations with Highest Success Attack Rate
    st.header("3. Cities/Locations with Highest Success Attack Rate")
    if 'city' in data.columns:
        location_column = 'city'
    elif 'location' in data.columns:
        location_column = 'location'
    else:
        st.warning("No city or location data available. Skipping this analysis.")
        location_column = None

    if location_column:
        try:
            location_success = data.groupby(location_column)['success'].mean().sort_values(ascending=False)
            top_locations = location_success.head(10)

            st.bar_chart(top_locations)
            st.write(f"Top 10 {location_column}s with highest attack success rate:", top_locations)
        except Exception as e:
            st.error(f"Error in Cities/Locations Analysis: {str(e)}")

    # Most Dangerous and Safest Countries
    st.header("4. Most Dangerous and Safest Countries")
    try:
        country_stats = data.groupby('country_txt').agg({
            'success': 'mean',
            'nkill': 'sum',
            'nwound': 'sum',
            'iyear': 'count'
        }).reset_index()

        country_stats['danger_score'] = (country_stats['success'] * country_stats['iyear'] * 
                                         (country_stats['nkill'] + country_stats['nwound']))

        most_dangerous = country_stats.sort_values('danger_score', ascending=False).head(10)
        safest = country_stats.sort_values('danger_score').head(10)

        st.write("Most dangerous countries:", most_dangerous['country_txt'].tolist())
        st.write("Safest countries:", safest['country_txt'].tolist())
    except Exception as e:
        st.error(f"Error in Dangerous/Safest Countries Analysis: {str(e)}")

    # Interactive Visualizations
    st.header("5. Interactive Visualizations")
    try:
        # World map of attack frequency
        attack_map = px.choropleth(country_stats, 
                                   locations="country_txt", 
                                   color="iyear", 
                                   hover_name="country_txt", 
                                   color_continuous_scale=px.colors.sequential.Plasma)

        st.plotly_chart(attack_map)

        # Time series of attack types
        attack_types_ts = data.groupby(['iyear', 'attacktype1_txt']).size().unstack()
        attack_types_chart = px.line(attack_types_ts, x=attack_types_ts.index, y=attack_types_ts.columns)
        st.plotly_chart(attack_types_chart)
    except Exception as e:
        st.error(f"Error in Interactive Visualizations: {str(e)}")

if __name__ == "__main__":
    show()