import pandas as pd

df = pd.read_csv("data/capital_projects_clean.csv")
group = ["fms_id", "managing_agency", "reporting_period"]

multi = df[df.duplicated(group, keep=False)]
stats = multi.groupby(group).agg(
    rows=("fms_id", "size"),
    distinct_budgets=("total_budget", "nunique"),
    distinct_spend=("spend_to_date", "nunique"),
)

print("Groups with several rows:", len(stats))
print("Budget identical across the rows:", (stats["distinct_budgets"] == 1).sum())
print("Budget differs across the rows:", (stats["distinct_budgets"] > 1).sum())
print()
print(stats.sort_values("rows", ascending=False).head(5))

print()
print("Rows with no pid:", df["pid"].isna().sum())
print(df[df["pid"].isna()]["current_phase_clean"].value_counts().head(5))

print("Spend differs across the rows:", (stats["distinct_spend"] > 1).sum())