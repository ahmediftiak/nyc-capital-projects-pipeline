import pandas as pd

df = pd.read_csv("data/capital_projects_clean.csv")

candidate_keys = {
    "fms_id + period": ["fms_id", "reporting_period"],
    "fms_id + agency + period": ["fms_id", "managing_agency", "reporting_period"],
    "fms_id + agency + budget_line + period": [
        "fms_id", "managing_agency", "budget_line", "reporting_period"
    ],
    "fms_id + agency + pid + period": [
        "fms_id", "managing_agency", "pid", "reporting_period"
    ],
}

for name, cols in candidate_keys.items():
    n = df.duplicated(cols, keep=False).sum()
    print(f"{name}: {n} rows still share a key")

ratio = (df["spend_to_date"] / df["total_budget"]).where(df["total_budget"] > 0)
diff = (ratio - df["spend_to_date_1"]).abs()
matches = (diff < 0.001).sum()
print(f"\nspend_to_date_1 matches spend/budget: {matches} of {diff.notna().sum()} rows")