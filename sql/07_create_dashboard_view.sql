CREATE OR ALTER VIEW dbo.v_dashboard AS
SELECT
    reporting_period,
    reporting_date,
    managing_agency,
    fms_id,
    COALESCE(fms_project_name, agency_project_name, fms_id) AS project_name,
    borough,
    current_phase_clean,
    CASE
        WHEN current_phase_clean IN ('Initiation', 'Pre-Design', 'Pending')
            THEN 'Planning'
        WHEN current_phase_clean IN ('Design', 'Design Built', 'Design Build')
            THEN 'Design'
        WHEN current_phase_clean IN ('Construction', 'Construction Procurement')
            THEN 'Construction'
        WHEN current_phase_clean IN ('Close-out', 'Closeout', 'Completed')
            THEN 'Closeout / Completed'
        WHEN current_phase_clean IN ('Cancelled', 'Withdrawn', 'Terminated',
                                     'Defaulted', 'Inactive', 'On-hold',
                                     'Transferred', 'Capitally Ineligible',
                                     'Rescinded')
            THEN 'Inactive / Ended'
        ELSE 'Programs & Other'
    END AS phase_group,
    total_budget,
    spend_to_date,
    pct_spent
FROM dbo.v_funding_records;