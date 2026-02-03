# monitoring/data_drift.py

import pandas as pd
from pathlib import Path

def _load_data(data):
    """Accept CSV path or DataFrame"""
    if isinstance(data, (str, Path)):
        return pd.read_csv(data)
    elif isinstance(data, pd.DataFrame):
        return data.copy()
    else:
        raise ValueError("data must be a CSV path or DataFrame")

def check_data_drift(reference_file, new_data_file, threshold=0.1):
    ref_df = _load_data(reference_file)
    new_df = _load_data(new_data_file)

    # only compare common numeric columns
    common_cols = (
        set(ref_df.select_dtypes(include="number").columns)
        & set(new_df.select_dtypes(include="number").columns)
    )

    if not common_cols:
        print("⚠️ No common numeric columns for drift check")
        return False

    for col in common_cols:
        ref_mean = ref_df[col].mean()
        new_mean = new_df[col].mean()

        if abs(ref_mean - new_mean) / (abs(ref_mean) + 1e-8) > threshold:
            return True

    return False
