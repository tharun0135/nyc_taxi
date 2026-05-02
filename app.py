import streamlit as st
import duckdb
import plotly.express as px

st.set_page_config(page_title="NYC Taxi Analytics", layout="wide")
st.title("🚖 NYC Taxi Data Warehouse Dashboard")
st.markdown("Real-time insights from our **Gold Layer** (DuckDB + dbt)")

# Connect to the warehouse
con = duckdb.connect('nyc_taxi.db')
df = con.execute("SELECT * FROM monthly_taxi_stats").df()

# Display Summary Metrics
m1, m2, m3 = st.columns(3)
m1.metric("Total Trips", f"{df['total_trips'].sum():,}")
m2.metric("Avg Distance", f"{df['avg_distance_miles'].mean():.2f} mi")
m3.metric("Avg Duration", f"{df['avg_duration_mins'].mean():.2f} min")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Trip Volume")
    fig1 = px.bar(df, x='trip_month', y='total_trips', color_discrete_sequence=['#FF4B4B'])
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Average Trip Distance")
    fig2 = px.line(df, x='trip_month', y='avg_distance_miles', markers=True)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Warehouse Data Preview")
st.dataframe(df, use_container_width=True)
