import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from pathlib import Path
import joblib
import scipy.sparse as sp

print("⚙️ Preprocessing data...")

# ===============================
# Paths (pipeline safe)
# ===============================
RAW_PATH = Path("data/raw/telco.csv")
PROCESSED_DIR = Path("data/processed")
MODEL_DIR = Path("models")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# Load data
# ===============================
df = pd.read_csv(RAW_PATH)

# Fix TotalCharges issue
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce")
df = df.dropna()

# ===============================
# Split X / y
# ===============================
y = df["Churn"].map({"Yes": 1, "No": 0})
X = df.drop(["Churn", "customerID"], axis=1)

# ===============================
# Column types
# ===============================
cat_cols = X.select_dtypes(include="object").columns
num_cols = X.select_dtypes(exclude="object").columns

# ===============================
# Preprocessor
# ===============================
preprocessor = ColumnTransformer(
    transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=True), cat_cols),
        ("num", "passthrough", num_cols),
    ]
)

# ===============================
# Fit + transform
# ===============================
X_t = preprocessor.fit_transform(X)

# ===============================
# Save preprocessor
# ===============================
joblib.dump(preprocessor, MODEL_DIR / "preprocessor.pkl")

# ===============================
# Save processed data
# ===============================
if sp.issparse(X_t):
    X_t = X_t.toarray()

pd.DataFrame(X_t).to_csv(PROCESSED_DIR / "features.csv", index=False)
pd.DataFrame(y, columns=["Churn"]).to_csv(PROCESSED_DIR / "target.csv", index=False)

print("✅ Preprocessing complete")
print(f"📦 Features saved to: {PROCESSED_DIR / 'features.csv'}")
print(f"📦 Target saved to: {PROCESSED_DIR / 'target.csv'}")
print(f"🧠 Preprocessor saved to: {MODEL_DIR / 'preprocessor.pkl'}")