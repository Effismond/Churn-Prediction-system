# analytics/churn_kpis.py

import pandas as pd
import json
from pathlib import Path

# -----------------------
# CONFIG
# -----------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_FILE = PROJECT_ROOT / "outputs/churn_scored.csv"
OUTPUT_FILE = PROJECT_ROOT / "outputs/churn_kpis.json"

# -----------------------
# 1. Load scored data
# -----------------------
if not INPUT_FILE.exists():
    raise FileNotFoundError(f"❌ Scored data not found: {INPUT_FILE}")

df = pd.read_csv(INPUT_FILE)

# Ensure proper column names
expected_columns = ["Churn", "gender", "Contract"]
for col in expected_columns:
    if col not in df.columns:
        raise KeyError(f"❌ Expected column not found in dataset: {col}")

# -----------------------
# 2. Compute KPIs
# -----------------------
kpis = {
    "overall_churn": round(df["Churn"].mean() * 100, 2),
    "gender_churn": {
        k: round(v * 100, 2) for k, v in df.groupby("gender")["Churn"].mean().to_dict().items()
    },
    "contract_churn": {
        k: round(v * 100, 2) for k, v in df.groupby("Contract")["Churn"].mean().to_dict().items()
    }
}

# -----------------------
# 3. Save KPIs to JSON
# -----------------------
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(kpis, f, indent=4)

print(f"✅ KPIs saved to {OUTPUT_FILE}")
print(kpis)
