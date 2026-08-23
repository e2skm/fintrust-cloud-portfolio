USE fintrust_db;

-- Query 1: Top 10 Customers by Suspicious Transaction Ratio
WITH total_transactions AS (
    SELECT
        customer_id,
        COUNT(*) AS total_count
    FROM transactions
    WHERE transaction_date >= '2024-01-01'
      AND transaction_date < '2025-01-01'
    GROUP BY customer_id
),

flagged_transactions AS (
    SELECT
        customer_id,
        COUNT(*) AS flagged_count
    FROM transactions
    WHERE transaction_date >= '2024-01-01'
      AND transaction_date < '2025-01-01'
      AND flag_suspicious = TRUE
    GROUP BY customer_id
)

SELECT
    tt.customer_id,
    tt.total_count,
    COALESCE(ft.flagged_count, 0) AS flagged_count,
    ROUND(
        COALESCE(ft.flagged_count, 0) * 1.0 / tt.total_count,
        4
    ) AS ratio
FROM total_transactions tt
LEFT JOIN flagged_transactions ft
    ON tt.customer_id = ft.customer_id
WHERE COALESCE(ft.flagged_count, 0) * 1.0 / tt.total_count > 0.05
ORDER BY ratio DESC
LIMIT 10;

-- Query 2: Branch Month-on-Month Suspicious Amount Change
WITH may_totals AS (
    SELECT
        branch_code,
        SUM(amount) AS may_amount
    FROM transactions
    WHERE flag_suspicious = TRUE
      AND transaction_date >= '2024-05-01'
      AND transaction_date < '2024-06-01'
    GROUP BY branch_code
),

june_totals AS (
    SELECT
        branch_code,
        SUM(amount) AS june_amount
    FROM transactions
    WHERE flag_suspicious = TRUE
      AND transaction_date >= '2024-06-01'
      AND transaction_date < '2024-07-01'
    GROUP BY branch_code
)

SELECT
    j.branch_code,
    m.may_amount,
    j.june_amount,
    ROUND(
        ((j.june_amount - m.may_amount) * 100.0)
        / m.may_amount,
        2
    ) AS percentage_change
FROM june_totals j
JOIN may_totals m
    ON j.branch_code = m.branch_code
WHERE ((j.june_amount - m.may_amount) * 100.0)
      / m.may_amount > 20
ORDER BY percentage_change DESC;