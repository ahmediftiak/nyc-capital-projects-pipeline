SELECT
    SUM(total_budget) AS naive_total_budget,
    (SELECT SUM(total_budget)
     FROM dbo.v_funding_records
     WHERE reporting_period = 202605) AS correct_total_budget
FROM dbo.capital_projects
WHERE reporting_period = 202605;