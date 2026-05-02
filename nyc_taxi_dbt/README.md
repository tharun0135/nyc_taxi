# 🚖 NYC Taxi Data Warehouse Pipeline

An end-to-end Data Engineering pipeline using the **Medallion Architecture**. This project processes 30M+ records of NYC Taxi data from AWS S3 to an interactive Streamlit dashboard.

## 🛠️ Tech Stack
- **Cloud:** AWS S3 (Data Lake)
- **Warehouse:** DuckDB (OLAP Engine)
- **Transformation:** dbt (Data Build Tool)
- **Visualization:** Streamlit & Plotly
- **Language:** Python & SQL

## 🏗️ Architecture (Medallion)
1. **Bronze (Raw):** Ingested Parquet files from AWS S3.
2. **Silver (Cleaned):** Processed via Python/DuckDB to filter noise and engineer features (trip duration).
3. **Gold (Analytics):** Summarized monthly statistics modeled using dbt.

## 🚀 How to Run
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the pipeline: `python scripts/duckdb_warehouse.py`
4. Run dbt models: `cd nyc_taxi_dbt && dbt run`
5. Launch Dashboard: `streamlit run app.py`