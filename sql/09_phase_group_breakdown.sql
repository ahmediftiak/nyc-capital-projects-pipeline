SELECT
    phase_group,
    COUNT(*)          AS funding_records,
    SUM(total_budget) AS total_budget
FROM dbo.v_dashboard
WHERE reporting_period = (SELECT MAX(reporting_period) FROM dbo.v_dashboard)
GROUP BY phase_group
ORDER BY total_budget DESC;