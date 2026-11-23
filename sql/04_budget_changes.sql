SELECT TOP 20
    cur.managing_agency,
    cur.fms_id,
    cur.fms_project_name,
    prev.total_budget                      AS budget_prev,
    cur.total_budget                       AS budget_cur,
    cur.total_budget - prev.total_budget   AS budget_change
FROM dbo.v_funding_records AS cur
JOIN dbo.v_funding_records AS prev
    ON  prev.fms_id          = cur.fms_id
    AND prev.managing_agency = cur.managing_agency
    AND prev.reporting_period = 202505
WHERE cur.reporting_period = 202605
  AND cur.total_budget <> prev.total_budget
ORDER BY ABS(cur.total_budget - prev.total_budget) DESC;