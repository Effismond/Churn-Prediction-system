# api/main.py

from fastapi import FastAPI, Query, HTTPException
import pandas as pd
from pathlib import Path
from functools import lru_cache
from monitoring.data_drift import check_data_drift

# ------------------------------
# FastAPI app with metadata
# ------------------------------
app = FastAPI(title="Churn API", version="1.0.0")

# ------------------------------
# File paths
# ------------------------------
DATA_FILE = Path(__file__).resolve().parents[1] / "segmentation" / "at_risk_customers.csv"
REFERENCE_FILE = Path(__file__).resolve().parents[1] / "monitoring" / "reference.csv"

# ------------------------------
# Load CSV data with caching
# ------------------------------
@lru_cache(maxsize=1)
def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    return pd.read_csv(DATA_FILE)

# ------------------------------
# Root endpoint (health check)
# ------------------------------
@app.get("/")
def read_root():
    return {"message": "Churn API is up and running!"}

# ------------------------------
# At-risk customers endpoint
# ------------------------------
@app.get("/at-risk")
def at_risk(limit: int = Query(50, ge=1, le=500)):
    """
    Returns top N at-risk customers.
    """
    try:
        df = load_data()
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return df.head(limit).to_dict("records")

# ------------------------------
# Data drift monitoring endpoint
# ------------------------------
@app.get("/check-drift")
def run_drift(threshold: float = 0.1, alert_email: str = "recipient@example.com"):
    """
    Checks for data drift in numeric columns.
    Sends email alert if drift is detected.
    Returns drift status.
    """
    if not REFERENCE_FILE.exists():
        raise HTTPException(status_code=404, detail=f"Reference file not found: {REFERENCE_FILE}")
    
    drift = check_data_drift(
        reference_file=REFERENCE_FILE,
        new_data_file=DATA_FILE,
        threshold=threshold,
        alert_email=alert_email
    )
    
    return {"drift_detected": drift}