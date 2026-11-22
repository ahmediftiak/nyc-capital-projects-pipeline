import pandas as pd

df = pd.read_csv("data/capital_projects_clean.csv")

text_cols = [c for c in df.columns if pd.api.types.is_string_dtype(df[c])]

lengths = {
    c: int(df[c].dropna().astype(str).str.len().max())
    for c in text_cols
}

print(pd.Series(lengths).sort_values(ascending=False))