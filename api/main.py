from fastapi import FastAPI, Query
import pandas as pd
from pathlib import Path
from functools import lru_cache

# FastAPI app with metadata
app = FastAPI(title="Churn API", version="1.0.0")

# Path to your CSV file
DATA_FILE = Path(__file__).resolve().parents[1] / "segmentation" / "at_risk_customers.csv"

# Function to load data with caching
@lru_cache(maxsize=1)
def load_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")
    return pd.read_csv(DATA_FILE)

# Root endpoint
@app.get("/")
def read_root():
    """
    Simple root endpoint to verify the API is running.
    """
    return {"message": "Churn API is up and running!"}

# At-risk customers endpoint
@app.get("/at-risk")
def at_risk(limit: int = Query(50, ge=1, le=500)):
    """
    Returns top N at-risk customers.
    """
    df = load_data()
    return df.head(limit).to_dict("records")