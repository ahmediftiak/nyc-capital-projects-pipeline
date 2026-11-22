import pandas as pd

df = pd.read_csv("data/capital_projects_budget_raw.csv")

print("Columns:", list(df.columns))
print()
print(df.dtypes)
print()
print("Null counts:")
print(df.isna().sum())
print()
print("Reporting periods:", sorted(df["reporting_period"].unique()))
print("Agencies:", df["managing_agency"].nunique())
print("Unique projects (fms_id):", df["fms_id"].nunique())
print("Duplicate (fms_id, period) rows:", df.duplicated(["fms_id", "reporting_period"]).sum())
print()
print(df["current_phase"].value_counts().head(10))