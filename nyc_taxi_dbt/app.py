import streamlit as st
import duckdb
import plotly.express as px

# Basic Page Config
st.set_page_config(page_title="NYC Taxi Analytics", layout="wide")
st.title("🚖 NYC Taxi Data Warehouse Dashboard")
st.markdown("Real-time insights from the **Gold Layer** of our local warehouse.")

# Connect to the DuckDB file created by dbt
con = duckdb.connect('nyc_taxi.db')
df = con.execute("SELECT * FROM monthly_taxi_stats").df()

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Trip Volume")
    # Using 'total_trips'
    fig1 = px.bar(df, x='trip_month', y='total_trips', 
                  color_discrete_sequence=['#FF4B4B'],
                  labels={'trip_month': 'Month', 'total_trips': 'Number of Trips'})
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Avg Trip Duration (Minutes)")
    # Swapped 'avg_fare_amount' for 'avg_duration_mins'
    fig2 = px.line(df, x='trip_month', y='avg_duration_mins', 
                   markers=True,
                   labels={'trip_month': 'Month', 'avg_duration_mins': 'Avg Duration (Min)'})
    st.plotly_chart(fig2, use_container_width=True)

# Show the raw data table at the bottom
st.divider()
st.subheader("Warehouse Data Preview (monthly_taxi_stats)")
st.dataframe(df, use_container_width=True)