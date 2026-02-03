# pipelines/4_predict.py

import pandas as pd
import joblib
from pathlib import Path

# -----------------------
# Optional monitoring
# -----------------------
try:
    from monitoring.data_drift import check_data_drift
    from monitoring.alerts import send_alert
    MONITORING_AVAILABLE = True
except ImportError:
    MONITORING_AVAILABLE = False

# -----------------------
# CONFIG
# -----------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_FILE = PROJECT_ROOT / "data/raw/telco.csv"
MODEL_FILE = PROJECT_ROOT / "models/churn_model.pkl"
PREPROCESSOR_FILE = PROJECT_ROOT / "models/preprocessor.pkl"
REFERENCE_FILE = PROJECT_ROOT / "monitoring/reference.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs/churn_scored.csv"

DRIFT_THRESHOLD = 0.1
ALERT_EMAIL = "team@example.com"

# -----------------------
# 1. Load raw data
# -----------------------
df = pd.read_csv(DATA_FILE)

# -----------------------
# 2. Load model & preprocessor
# -----------------------
model = joblib.load(MODEL_FILE)
preprocessor = joblib.load(PREPROCESSOR_FILE)

# -----------------------
# 3. Apply preprocessing (SAFE & CORRECT)
# -----------------------
for col, le in preprocessor.items():
    if col in df.columns:
        df[col] = df[col].astype(str)
        df[col] = df[col].map(lambda x: x if x in le.classes_ else le.classes_[0])
        df[col] = le.transform(df[col])

# Build feature matrix (MATCH TRAINING EXACTLY)
X_processed = df.drop(columns=["customerID", "Churn"], errors="ignore")

# -----------------------
# 4. Final safety cleaning (CRITICAL)
# -----------------------
X_processed = X_processed.replace(" ", pd.NA)
X_processed = X_processed.apply(pd.to_numeric, errors="coerce")
X_processed = X_processed.fillna(0)

# -----------------------
# 5. Drift check (SAFE & NON-BLOCKING)
# -----------------------
if MONITORING_AVAILABLE and REFERENCE_FILE.exists():
    try:
        drift_detected = check_data_drift(
            reference_file=REFERENCE_FILE,
            new_data_file=X_processed,
            threshold=DRIFT_THRESHOLD
        )

        if drift_detected:
            send_alert(
                subject="⚠️ Churn Pipeline Alert: Data Drift Detected",
                body="Significant drift detected. Consider retraining.",
                to_email=ALERT_EMAIL
            )
    except Exception as e:
        print(f"⚠️ Drift check skipped: {e}")

# -----------------------
# 6. Predict
# -----------------------
df["churn_probability"] = model.predict_proba(X_processed)[:, 1]

# -----------------------
# 7. Save output
# -----------------------
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print(f"✅ Predictions saved to {OUTPUT_FILE}")