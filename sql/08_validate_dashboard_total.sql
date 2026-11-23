SELECT SUM(total_budget) AS dashboard_total_budget
FROM dbo.v_dashboard
WHERE reporting_period = (SELECT MAX(reporting_period) FROM dbo.v_dashboard);