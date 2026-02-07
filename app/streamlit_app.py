import streamlit as st
import pandas as pd
import time
import requests
import os
import sys

# -----------------------
# PROJECT ROOT (for config)
# -----------------------
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from config.regions import REGIONS

# -----------------------
# SETTINGS
# -----------------------
st.set_page_config(page_title="Fintech Churn Dashboard", layout="wide")
st.title("📊 Real-Time Fintech Customer Intelligence")
APP_VERSION = "1.2.0"

# -----------------------
# Load main data
# -----------------------
df = pd.read_csv("outputs/churn_scored.csv")

# -----------------------
# Sidebar for region selection
# -----------------------
region_code = st.sidebar.selectbox("Select Region", options=list(REGIONS.keys()))
region = REGIONS[region_code]

# Optional: Filter by churn risk
risk_filter = st.sidebar.multiselect(
    "Filter by Churn Risk Band",
    options=["High Risk", "Medium Risk", "Low Risk"],
    default=["High Risk", "Medium Risk", "Low Risk"]
)

# -----------------------
# Ensure numeric churn and create risk bands
# -----------------------
if "Churn_num" not in df.columns:
    if df["Churn"].dtype == object:
        df["Churn_num"] = df["Churn"].map({"Yes": 1, "No": 0})
    else:
        df["Churn_num"] = df["Churn"]

if "churn_risk_band" not in df.columns:
    if "churn_probability" in df.columns:
        df["churn_risk_band"] = pd.cut(
            df["churn_probability"],
            bins=[-0.01, 0.3, 0.7, 1],
            labels=["Low Risk", "Medium Risk", "High Risk"]
        )
    else:
        df["churn_risk_band"] = df["Churn_num"].map({0: "Low Risk", 1: "High Risk"})

# Apply risk filter
df_filtered = df[df["churn_risk_band"].isin(risk_filter)].copy()

# -----------------------
# Helper: format monetary values
# -----------------------
def format_currency(val, region):
    if pd.isna(val):
        return ""
    val = round(float(val), 2)
    return f"{region['currency']}{val}" if region["symbol_position"] == "before" else f"{val}{region['currency']}"

# -----------------------
# KPI CARDS: Churn Risk
# -----------------------
risk_counts = df_filtered["churn_risk_band"].value_counts().to_dict()

def risk_color(risk):
    return {
        "High Risk": "#ff4b4b",
        "Medium Risk": "#ffbf00",
        "Low Risk": "#4CAF50"
    }.get(risk, "#ccc")

st.markdown("<h2>Churn Risk KPIs</h2>", unsafe_allow_html=True)
cols = st.columns(3)
for i, risk_band in enumerate(["High Risk", "Medium Risk", "Low Risk"]):
    count = risk_counts.get(risk_band, 0)
    cols[i].markdown(
        f"""
        <div style="background-color:{risk_color(risk_band)}; padding:20px; border-radius:10px; text-align:center; color:white;">
            <h3>{risk_band}</h3>
            <h2>{count}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------
# GENERAL METRICS
# -----------------------
col1, col2, col3 = st.columns(3)
col1.metric("Overall Churn Rate", f"{round(df_filtered['Churn_num'].mean()*100, 2)}%")
col2.metric("Customers", df_filtered.shape[0])
col3.metric("Avg Monthly Charges", format_currency(df_filtered['MonthlyCharges'].mean(), region))

# -----------------------
# At-Risk Customers (API)
# -----------------------
st.subheader("At-Risk Customers")

# Read from Streamlit Secrets
API_URL = st.secrets["API_URL"]
st.write("API URL:", API_URL)  # optional: confirms connection

max_retries = 5
retry_delay = 2  # seconds

for attempt in range(1, max_retries + 1):
    try:
        response = requests.get(f"{API_URL}/at-risk", timeout=5)
        response.raise_for_status()
        data = response.json()
        at_risk_df = pd.DataFrame(data)

        # Format monetary columns
        for col in ["CLV", "MonthlyCharges"]:
            if col in at_risk_df.columns:
                at_risk_df[col] = at_risk_df[col].apply(lambda x: format_currency(x, region))

        st.dataframe(at_risk_df.head(50))
        break

    except requests.exceptions.RequestException as e:
        if attempt < max_retries:
            st.warning(f"API not ready, retrying... ({attempt}/{max_retries})")
            time.sleep(retry_delay)
        else:
            st.error("API not connected after several attempts.")
            st.caption(str(e))

# Full Dataset
# -----------------------
st.subheader("Full Dataset")
df_display = df_filtered.copy()
for col in ["CLV", "MonthlyCharges"]:
    if col in df_display.columns:
        df_display[col] = df_display[col].apply(lambda x: format_currency(x, region))

st.dataframe(df_display.head(100))

# -----------------------
# Footer
# -----------------------
st.caption(f"Dashboard Version: {APP_VERSION}")