-- Labor Market Econometrics
-- Research Question: how do wages differ by education level?
-- Data: 2024 ACS (IPUMS USA)

SELECT
    education_label,
    COUNT(*) AS observations,
    ROUND(AVG(INCWAGE), 2) AS average_wage,
    ROUND(MIN(INCWAGE), 2) AS minimum_wage,
    ROUND(MAX(INCWAGE), 2) AS maximum_wage
FROM workers
GROUP BY education_label
ORDER BY average_wage DESC;