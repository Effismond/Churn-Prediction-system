# monitoring/data_drift.py

import pandas as pd
from pathlib import Path
from monitoring.alerts import send_alert

def _load_data(data):
    """Accept CSV path or DataFrame"""
    if isinstance(data, (str, Path)):
        return pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        return data.copy()
    else:
        raise ValueError("data must be a CSV path or DataFrame")


def check_data_drift(reference_file, new_data_file, threshold=0.1, alert_email=None):
    """
    Checks for drift in numeric columns.
    If drift is detected, optionally sends an alert email.
    """
    ref_df = _load_data(reference_file)
    new_df = _load_data(new_data_file)

    # compare only common numeric columns
    common_cols = (
        set(ref_df.select_dtypes(include="number").columns)
        & set(new_df.select_dtypes(include="number").columns)
    )

    if not common_cols:
        print("⚠️ No common numeric columns for drift check")
        return False

    drift_detected = False
    drift_cols = []

    for col in common_cols:
        ref_mean = ref_df[col].mean()
        new_mean = new_df[col].mean()
        relative_change = abs(ref_mean - new_mean) / (abs(ref_mean) + 1e-8)

        if relative_change > threshold:
            drift_detected = True
            drift_cols.append((col, ref_mean, new_mean, relative_change))

    if drift_detected:
        print(f"⚠️ Data drift detected in columns: {', '.join([c[0] for c in drift_cols])}")
        if alert_email:
            subject = "Data Drift Alert 🚨"
            body = "Data drift detected in columns:\n"
            for col, ref, new, change in drift_cols:
                body += f"{col}: ref={ref:.4f}, new={new:.4f}, change={change:.2%}\n"
            send_alert(subject, body, alert_email)

    return drift_detected
