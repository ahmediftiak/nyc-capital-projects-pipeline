import pandas as pd

df = pd.read_csv("data/capital_projects_clean.csv")
key = ["fms_id", "reporting_period"]
dups = df[df.duplicated(key, keep=False)]

# 1. One example: show only the columns that differ between the copies
example = dups[dups["fms_id"] == "ACEDOE211"].sort_values("reporting_period").tail(2)
differ = [c for c in example.columns if example[c].nunique(dropna=False) > 1]
print("Columns that differ for ACEDOE211, latest period:")
print(example[key + differ].T)

# 2. Across ALL duplicate groups, which columns differ most often?
counts = {}
for col in df.columns:
    n = dups.groupby(key)[col].nunique(dropna=False)
    counts[col] = int((n > 1).sum())
print("\nHow many duplicate groups differ in each column:")
print(pd.Series(counts).sort_values(ascending=False).head(10))

# 3. How many duplicate groups are in the latest period?
latest = dups[dups["reporting_period"] == dups["reporting_period"].max()]
print("\nDuplicate groups in the latest period:", latest[key].drop_duplicates().shape[0])