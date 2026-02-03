# pipelines/3_train.py

import pandas as pd
import numpy as np
import joblib
import mlflow
import mlflow.sklearn
import os
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from pathlib import Path

# -----------------------
# CONFIG
# -----------------------
DATA_FILE = Path("data/raw/Telco_Customer_Churn_Dataset.csv")
MODEL_DIR = Path("models")
MODEL_DIR.mkdir(exist_ok=True)

# -----------------------
# 1. Load & Clean Data
# -----------------------
df = pd.read_csv(DATA_FILE)

df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})

# -----------------------
# 2. Feature Engineering
# -----------------------
cat_cols = df.select_dtypes(include="object").columns
preprocessor = {}

for c in cat_cols:
    le = LabelEncoder()
    df[c] = le.fit_transform(df[c])
    preprocessor[c] = le

joblib.dump(preprocessor, MODEL_DIR / "preprocessor.pkl")
print(f"✅ Preprocessor saved to {MODEL_DIR / 'preprocessor.pkl'}")

# -----------------------
# 3. Split Data
# -----------------------
X = df.drop(["Churn", "customerID"], axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------
# 4. Train Model
# -----------------------
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
print(f"✅ ROC-AUC Score: {auc:.4f}")

joblib.dump(model, MODEL_DIR / "churn_model.pkl")
print(f"✅ Model saved to {MODEL_DIR / 'churn_model.pkl'}")

# -----------------------
# 5. SAVE REFERENCE DATA FOR DRIFT MONITORING ✅
# -----------------------
os.makedirs("monitoring", exist_ok=True)
X_train.to_csv("monitoring/reference.csv", index=False)
print("📊 Reference data saved to monitoring/reference.csv")

# -----------------------
# 6. Customer Lifetime Value (CLV)
# -----------------------
df["CLV"] = df["MonthlyCharges"] * df["tenure"]
print(df[["customerID", "CLV"]].head())

# -----------------------
# 7. Log to MLflow
# -----------------------
mlflow.set_experiment("Churn_Prediction")
with mlflow.start_run(run_name="3_train"):
    mlflow.log_metric("roc_auc", auc)
    mlflow.sklearn.log_model(model, "churn_model")
    mlflow.sklearn.log_model(preprocessor, "preprocessor")
    print("✅ MLflow logging completed")