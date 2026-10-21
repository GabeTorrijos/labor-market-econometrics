-- Labor Market Econometrics
-- Survey-weighted annual wage income by education
-- Data: 2024 ACS (IPUMS USA)

SELECT
    education_label,
    COUNT(*) AS observations,
    ROUND(SUM(PERWT), 0) AS weighted_population,
    ROUND(
        SUM(INCWAGE * PERWT) / SUM(PERWT),
        2
    ) AS weighted_average_wage
FROM workers
GROUP BY education_label
ORDER BY weighted_average_wage DESC;