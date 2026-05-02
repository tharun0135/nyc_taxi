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

## 📊 Live Dashboard
Access the interactive NYC Taxi Analytics Dashboard:

**🌐 [View Full-Screen Dashboard](https://redesigned-tribble-qwgxjxrg5xxhrq7-8501.app.github.dev/)**

> **💡 Pro Tip:** For the best experience, view the dashboard in full-screen mode by clicking the fullscreen icon (⛶) in the top-right corner of the Streamlit interface.

### Dashboard Features:
- 📈 **Monthly Trip Volume** - Track taxi usage patterns over time
- 📏 **Average Trip Distance** - Analyze distance trends by month
- 📊 **Key Metrics** - Total trips, average distance, and duration
- 📋 **Data Preview** - Raw monthly statistics table

### Tech Stack:
- **Frontend:** Streamlit (Python)
- **Database:** DuckDB (fast analytical queries)
- **ETL:** dbt (data transformation)
- **Visualization:** Plotly (interactive charts)

## 🌍 Public Deployment
This project is now prepared for public deployment on **Streamlit Cloud**.

To deploy:
1. Push the repo to GitHub.
2. Sign in to Streamlit Cloud.
3. Create a new app and connect it to this repo.
4. Set the main file to `app.py`.

The app uses a local DuckDB database file, so the dataset is included in the repository and will be available to the deployed app.

## 🧱 Auto-Start Dashboard
The dashboard is configured to start automatically in the devcontainer environment using `.devcontainer/devcontainer.json`.

If you want to keep the dashboard running locally without manually typing `streamlit run app.py`, use the helper script:

```bash
./scripts/start_dashboard.sh
```

This launches the app in the background and keeps it available on **http://localhost:8501**.
