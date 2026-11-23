SELECT
    current_phase_clean,
    COUNT(*)          AS funding_records,
    SUM(total_budget) AS total_budget
FROM dbo.v_funding_records
WHERE reporting_period = (SELECT MAX(reporting_period)
                          FROM dbo.v_funding_records)
GROUP BY current_phase_clean
ORDER BY total_budget DESC;