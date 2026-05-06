-- ============================================================
-- Project 4: Healthcare KPI Monitoring Dashboard
-- SQL Analysis Queries
-- ============================================================

-- 1. Department KPI Summary
SELECT
    department,
    COUNT(admission_id)                                    AS total_admissions,
    ROUND(AVG(length_of_stay_days), 1)                     AS avg_length_of_stay,
    ROUND(AVG(wait_time_min), 0)                           AS avg_wait_time_min,
    ROUND(SUM(CASE WHEN readmitted_30d=1 THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS readmission_rate_pct,
    ROUND(AVG(treatment_cost), 2)                          AS avg_treatment_cost,
    SUM(CASE WHEN discharge_status='Deceased' THEN 1 ELSE 0 END) AS mortality_count
FROM admissions
GROUP BY department
ORDER BY total_admissions DESC;

-- 2. Monthly Admissions Trend
SELECT
    DATE_FORMAT(admission_date, '%Y-%m') AS month,
    COUNT(*)                             AS total_admissions,
    COUNT(CASE WHEN admission_type='Emergency' THEN 1 END) AS emergency_admissions,
    ROUND(AVG(wait_time_min), 0)         AS avg_wait_time_min,
    ROUND(AVG(length_of_stay_days), 1)  AS avg_los
FROM admissions
GROUP BY DATE_FORMAT(admission_date, '%Y-%m')
ORDER BY month;

-- 3. Bed Occupancy by Department (Monthly Average)
SELECT
    department,
    DATE_FORMAT(date, '%Y-%m')         AS month,
    ROUND(AVG(occupancy_rate_pct), 1)  AS avg_occupancy_pct,
    MAX(occupancy_rate_pct)            AS peak_occupancy_pct,
    SUM(CASE WHEN occupancy_rate_pct >= 95 THEN 1 ELSE 0 END) AS days_at_critical_capacity
FROM bed_occupancy
GROUP BY department, DATE_FORMAT(date, '%Y-%m')
ORDER BY month, avg_occupancy_pct DESC;

-- 4. Emergency Wait Time Analysis (Key Patient Safety KPI)
SELECT
    department,
    ROUND(AVG(wait_time_min), 0)                               AS avg_wait_min,
    MIN(wait_time_min)                                         AS min_wait_min,
    MAX(wait_time_min)                                         AS max_wait_min,
    SUM(CASE WHEN wait_time_min > 120 THEN 1 ELSE 0 END)      AS breaches_over_2hr,
    ROUND(SUM(CASE WHEN wait_time_min > 120 THEN 1 ELSE 0 END)*100.0/COUNT(*), 1) AS breach_rate_pct
FROM admissions
WHERE admission_type = 'Emergency'
GROUP BY department
ORDER BY avg_wait_min DESC;

-- 5. Patient Demographics & Cost
SELECT
    CASE
        WHEN p.age < 18  THEN '0–17'
        WHEN p.age < 40  THEN '18–39'
        WHEN p.age < 60  THEN '40–59'
        WHEN p.age < 75  THEN '60–74'
        ELSE '75+'
    END                               AS age_group,
    p.insurance_type,
    COUNT(a.admission_id)             AS admissions,
    ROUND(AVG(a.length_of_stay_days),1) AS avg_los,
    ROUND(AVG(a.treatment_cost), 2)   AS avg_cost,
    ROUND(SUM(a.treatment_cost), 2)   AS total_cost
FROM admissions a
JOIN patients p ON a.patient_id = p.patient_id
GROUP BY age_group, p.insurance_type
ORDER BY age_group, p.insurance_type;

-- 6. Top Diagnoses by Volume and Cost
SELECT
    diagnosis,
    department,
    COUNT(*)                          AS cases,
    ROUND(AVG(length_of_stay_days),1) AS avg_los,
    ROUND(AVG(treatment_cost), 2)     AS avg_cost,
    ROUND(SUM(treatment_cost), 2)     AS total_cost
FROM admissions
GROUP BY diagnosis, department
ORDER BY cases DESC
LIMIT 20;

-- 7. Readmission Rate by Department and Admission Type
SELECT
    department,
    admission_type,
    COUNT(*)                                                 AS total,
    SUM(readmitted_30d)                                      AS readmissions,
    ROUND(SUM(readmitted_30d)*100.0/COUNT(*), 2)             AS readmission_rate_pct
FROM admissions
GROUP BY department, admission_type
ORDER BY readmission_rate_pct DESC;

-- 8. Revenue and Cost Analysis
SELECT
    DATE_FORMAT(admission_date, '%Y-%m') AS month,
    department,
    COUNT(*)                             AS admissions,
    ROUND(SUM(treatment_cost), 2)        AS total_revenue,
    ROUND(AVG(treatment_cost), 2)        AS avg_revenue_per_admission
FROM admissions
GROUP BY DATE_FORMAT(admission_date, '%Y-%m'), department
ORDER BY month, total_revenue DESC;
