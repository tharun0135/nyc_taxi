# 🚖 NYC Taxi Data Warehouse Pipeline

An end-to-end Data Engineering pipeline using the **Medallion Architecture**. This project processes 30M+ records of NYC Taxi data from AWS S3 to an interactive Streamlit dashboard.

## 🏗️ Architecture
1. **Bronze (Raw):** Ingested Parquet files from AWS S3.
2. **Silver (Cleaned):** Processed via Python/DuckDB to filter noise and engineer features.
3. **Gold (Analytics):** Summarized monthly statistics modeled using dbt.

## 🚀 How to Run
1. Clone the repo.
2. Install dependencies: `pip install streamlit duckdb plotly dbt-duckdb`
3. Run the dashboard: `streamlit run app.py`
