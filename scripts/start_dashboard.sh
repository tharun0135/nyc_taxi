#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

# Start Streamlit in the background and keep it running.
# Log output to streamlit_dashboard.log.
nohup streamlit run app.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false > streamlit_dashboard.log 2>&1 &

echo "Streamlit dashboard started in the background."
echo "Open http://localhost:8501 to view it."
echo "Logs: $(pwd)/streamlit_dashboard.log"