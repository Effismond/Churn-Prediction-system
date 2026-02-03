import pandas as pd

df = pd.read_csv("outputs/churn_scored.csv")

df["CLV"] = df["MonthlyCharges"] * df["tenure"]

at_risk = df[df["churn_probability"] > 0.7]
high_value = df[df["CLV"] > df["CLV"].quantile(0.75)]

at_risk.to_csv("segmentation/at_risk_customers.csv", index=False)
high_value.to_csv("segmentation/high_value_customers.csv", index=False)
df.to_csv("segmentation/customer_clv.csv", index=False)
