import pandas as pd

RAW_PATH = "data/capital_projects_budget_raw.csv"
CLEAN_PATH = "data/capital_projects_clean.csv"

DATE_COLUMNS = [
    "fms_data_date",
    "agency_data_date",
    "actual_design_start",
    "actual_design_end",
    "actual_construction_start",
    "actual_construction_end",
    "current_phase_start",
    "forecast_current_phase_end",
    "forecast_completion",
]


def clean(df):
    df = df.copy()

    # 1. Trim stray whitespace in text columns
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.strip()

    # 2. Turn 202605 into a real date (2026-05-01)
    df["reporting_date"] = pd.to_datetime(
        df["reporting_period"].astype(str), format="%Y%m"
    )

    # 3. Parse date columns; warn if any real values fail to convert
    for col in DATE_COLUMNS:
        before = df[col].notna().sum()
        df[col] = pd.to_datetime(df[col], errors="coerce")
        lost = before - df[col].notna().sum()
        if lost:
            print(f"WARNING: {col}: {lost} values could not be parsed")

    # 4. pid is an ID, not a measurement: nullable integer
    df["pid"] = df["pid"].astype("Int64")

    # 5. Cleaned phase label (original column kept)
    df["current_phase_clean"] = (
        df["current_phase"].str.replace(r"[()]", "", regex=True).str.strip()
    )

    # 6. Drop rows that are exact copies of each other
    exact = df.duplicated().sum()
    df = df.drop_duplicates()
    print(f"Dropped {exact} exact duplicate rows")

    # 7. Give the unclear column its real name (it is spend / budget)
    df = df.rename(columns={"spend_to_date_1": "pct_spent"})

    return df


def validate(df):
    print("\n--- Validation ---")

    key = ["fms_id", "managing_agency", "pid", "reporting_period"]
    dups = df.duplicated(key, keep=False).sum()
    print(f"Rows sharing the full natural key: {dups} (expected 0)")
    assert dups == 0, "Natural key is not unique: investigate before loading"

    print("Negative budgets:", (df["total_budget"] < 0).sum())
    print("Negative spend:", (df["spend_to_date"] < 0).sum())
    print("Zero budgets:", (df["total_budget"] == 0).sum())
    print("Spend above budget:", (df["spend_to_date"] > df["total_budget"]).sum())


if __name__ == "__main__":
    raw = pd.read_csv(RAW_PATH)
    print("Raw shape:", raw.shape)
    df = clean(raw)
    validate(df)
    df.to_csv(CLEAN_PATH, index=False)
    print("\nClean shape:", df.shape)
    print("Saved to", CLEAN_PATH)