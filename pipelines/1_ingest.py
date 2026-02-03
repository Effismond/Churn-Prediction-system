from pathlib import Path
import pandas as pd

# Always resolve from project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA = PROJECT_ROOT / "data" / "raw" / "Telco_Customer_Churn_Dataset.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "telco.csv"

def main():
    print("📥 Ingesting raw data...")

    df = pd.read_csv(RAW_DATA)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"✅ Raw data saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()