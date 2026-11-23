SELECT
    managing_agency,
    COUNT(*)                                   AS funding_records,
    SUM(total_budget)                          AS total_budget,
    SUM(spend_to_date)                         AS total_spend,
    ROUND(100.0 * SUM(spend_to_date)
          / NULLIF(SUM(total_budget), 0), 1)   AS pct_spent
FROM dbo.v_funding_records
WHERE reporting_period = (SELECT MAX(reporting_period)
                          FROM dbo.v_funding_records)
GROUP BY managing_agency
ORDER BY total_budget DESC;