CREATE OR ALTER VIEW dbo.v_funding_records AS
SELECT *
FROM (
    SELECT
        cp.*,
        ROW_NUMBER() OVER (
            PARTITION BY fms_id, managing_agency, reporting_period
            ORDER BY row_id
        ) AS rn
    FROM dbo.capital_projects AS cp
) AS ranked
WHERE rn = 1;