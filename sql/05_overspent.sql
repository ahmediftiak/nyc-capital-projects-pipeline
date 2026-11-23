SELECT TOP 20
    managing_agency,
    fms_id,
    fms_project_name,
    current_phase_clean,
    total_budget,
    spend_to_date,
    spend_to_date - total_budget AS over_by
FROM dbo.v_funding_records
WHERE reporting_period = (SELECT MAX(reporting_period)
                          FROM dbo.v_funding_records)
  AND total_budget > 0
  AND spend_to_date > total_budget
ORDER BY over_by DESC;