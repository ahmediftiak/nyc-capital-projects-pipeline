import urllib.parse

import pandas as pd
from sqlalchemy import create_engine, text

SERVER = "localhost\\SQLEXPRESS"
DATABASE = "NYCCapitalProjects"
TABLE = "dbo.capital_projects"
CSV_PATH = "data/capital_projects_clean.csv"

DATE_COLUMNS = [
    "reporting_date", "fms_data_date", "agency_data_date",
    "actual_design_start", "actual_design_end",
    "actual_construction_start", "actual_construction_end",
    "current_phase_start", "forecast_current_phase_end", "forecast_completion",
]

COLUMNS = [
    "reporting_period", "reporting_date", "managing_agency", "fms_id", "pid",
    "total_budget", "spend_to_date", "pct_spent",
    "fms_project_name", "current_phase", "current_phase_clean",
    "borough", "community_board", "budget_line", "ten_year_plan_category",
    "sponsor_agency", "agency_project_name", "agency_project_description",
    "actual_design_start", "actual_design_end",
    "actual_construction_start", "actual_construction_end",
    "current_phase_start", "forecast_current_phase_end", "forecast_completion",
    "fms_data_date", "agency_data_date",
]

CREATE_TABLE = f"""
CREATE TABLE {TABLE} (
    row_id                      INT IDENTITY(1,1) PRIMARY KEY,
    reporting_period            INT            NOT NULL,
    reporting_date              DATE           NOT NULL,
    managing_agency             NVARCHAR(50)   NOT NULL,
    fms_id                      NVARCHAR(50)   NOT NULL,
    pid                         INT            NULL,
    total_budget                DECIMAL(18,2)  NULL,
    spend_to_date               DECIMAL(18,2)  NULL,
    pct_spent                   DECIMAL(10,4)  NULL,
    fms_project_name            NVARCHAR(255)  NULL,
    current_phase               NVARCHAR(100)  NULL,
    current_phase_clean         NVARCHAR(100)  NULL,
    borough                     NVARCHAR(100)  NULL,
    community_board             NVARCHAR(500)  NULL,
    budget_line                 NVARCHAR(500)  NULL,
    ten_year_plan_category      NVARCHAR(255)  NULL,
    sponsor_agency              NVARCHAR(100)  NULL,
    agency_project_name         NVARCHAR(500)  NULL,
    agency_project_description  NVARCHAR(MAX)  NULL,
    actual_design_start         DATE NULL,
    actual_design_end           DATE NULL,
    actual_construction_start   DATE NULL,
    actual_construction_end     DATE NULL,
    current_phase_start         DATE NULL,
    forecast_current_phase_end  DATE NULL,
    forecast_completion         DATE NULL,
    fms_data_date               DATE NULL,
    agency_data_date            DATE NULL
)
"""
DROP_TABLE = f"DROP TABLE IF EXISTS {TABLE}"

CREATE_INDEX = f"""
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'ux_capital_projects_natural_key')
CREATE UNIQUE INDEX ux_capital_projects_natural_key
ON {TABLE} (fms_id, managing_agency, pid, reporting_period)
"""


def make_engine(database, autocommit=False):
    conn_str = (
        "DRIVER={ODBC Driver 18 for SQL Server};"
        f"SERVER={SERVER};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    options = {"fast_executemany": True}
    if autocommit:
        options["isolation_level"] = "AUTOCOMMIT"
    url = "mssql+pyodbc:///?odbc_connect=" + urllib.parse.quote_plus(conn_str)
    return create_engine(url, **options)


def create_database():
    engine = make_engine("master", autocommit=True)
    with engine.connect() as conn:
        conn.execute(text(f"IF DB_ID('{DATABASE}') IS NULL CREATE DATABASE {DATABASE}"))
    engine.dispose()


def create_table(engine):
    with engine.begin() as conn:
        conn.execute(text(DROP_TABLE))
        conn.execute(text(CREATE_TABLE))
        conn.execute(text(CREATE_INDEX))


def load(engine):
    df = pd.read_csv(CSV_PATH, parse_dates=DATE_COLUMNS)
    df["pid"] = df["pid"].astype("Int64")
    df = df[COLUMNS]

    with engine.begin() as conn:
        conn.execute(text(f"TRUNCATE TABLE {TABLE}"))

    df.to_sql(
        "capital_projects", engine, schema="dbo",
        if_exists="append", index=False, chunksize=5000,
    )

    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {TABLE}")).scalar()
    print(f"Rows in CSV: {len(df)}, rows in SQL Server: {count}")
    assert count == len(df), "Row count mismatch after load"


if __name__ == "__main__":
    create_database()
    engine = make_engine(DATABASE)
    create_table(engine)
    load(engine)
    print("Load complete.")