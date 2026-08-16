USE fintrust_db;

-- Anatomy of a Window Function --
SELECT
    a.customer_id,
    t.amount,
    SUM(t.amount) OVER (
        PARTITION BY a.customer_id
        ORDER BY t.transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total
FROM transactions t
JOIN accounts a
    ON t.account_id = a.account_id;

-- Practical: Top 3 Transactions Per Branch
WITH ranked_txns AS (
    SELECT
        t.transaction_id,
        t.branch_code,
        t.amount,
        t.customer_id,
        ROW_NUMBER() OVER (
            PARTITION BY t.branch_code
            ORDER BY t.amount DESC
        ) AS rn
    FROM transactions t
    WHERE t.transaction_date >= '2024-06-01'
)
SELECT branch_code, transaction_id, amount, customer_id
FROM  ranked_txns
WHERE rn <= 3
ORDER BY branch_code, rn;

-- Month-on-Month Transaction Volume Change
WITH monthly_totals AS (
    SELECT
        DATE_TRUNC('month', transaction_date) AS month_start,
        branch_code,
        SUM(amount) AS total_amount,
        COUNT(*) AS txn_count
    FROM  transactions
    GROUP BY DATE_TRUNC('month', transaction_date), branch_code
)
SELECT
    month_start,
    branch_code,
    total_amount,
    LAG(total_amount) OVER (
        PARTITION BY branch_code
        ORDER BY month_start
    ) AS prev_month_amount,
    ROUND(
        (total_amount - LAG(total_amount) OVER (
            PARTITION BY branch_code ORDER BY month_start
        )) /
        NULLIF(LAG(total_amount) OVER (
            PARTITION BY branch_code ORDER BY month_start
        ), 0) * 100
    , 1) AS pct_change
FROM  monthly_totals
ORDER BY branch_code, month_start;

-- Challenge 1: Customer Spend Ranking --
WITH customer_spend AS (
    SELECT
        c.customer_id,
        CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
        SUM(t.amount) AS total_spend
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN transactions t
        ON a.account_id = t.account_id
    WHERE t.transaction_type IN ('DEBIT', 'PAYMENT')
      AND YEAR(t.transaction_date) = 2024
      AND MONTH(t.transaction_date) = 6
    GROUP BY c.customer_id, customer_name
),
spend_tiers AS (
    SELECT *,
        CASE
            WHEN total_spend >= 2000 THEN 'Premium'
            WHEN total_spend >= 500 THEN 'Standard'
            ELSE 'Basic'
        END AS spend_tier
    FROM customer_spend
)
SELECT
    customer_id,
    customer_name,
    total_spend,
    spend_tier,
    DENSE_RANK() OVER (
        PARTITION BY spend_tier
        ORDER BY total_spend DESC
    ) AS tier_rank
FROM spend_tiers
ORDER BY spend_tier, tier_rank;

-- Challenge 2: Running Fraud Exposure --
WITH suspicious_txns AS (
    SELECT
        b.branch_id,
        b.branch_name,
        t.transaction_id,
        t.transaction_date,
        t.amount
    FROM transactions t
    JOIN accounts a
        ON t.account_id = a.account_id
    JOIN branches b
        ON a.branch_id = b.branch_id
    WHERE t.amount > 1000
)
SELECT
    branch_name,
    transaction_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY branch_id
        ORDER BY transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING
                 AND CURRENT ROW
    ) AS running_fraud_exposure
FROM suspicious_txns
ORDER BY branch_name, transaction_date;

-- Challenge 3: Detect Spending Spikes --
WITH monthly_spend AS (
    SELECT
        c.customer_id,
        DATE_FORMAT(t.transaction_date, '%Y-%m-01') AS spend_month,
        SUM(t.amount) AS month_spend
    FROM customers c
    JOIN accounts a
        ON c.customer_id = a.customer_id
    JOIN transactions t
        ON a.account_id = t.account_id
    WHERE t.transaction_type IN ('DEBIT', 'PAYMENT')
      AND t.transaction_date >= '2024-01-01'
      AND t.transaction_date < '2024-07-01'
    GROUP BY
        c.customer_id,
        DATE_FORMAT(t.transaction_date, '%Y-%m-01')
),
spend_comparison AS (
    SELECT
        customer_id,
        spend_month,
        month_spend,
        LAG(month_spend) OVER (
            PARTITION BY customer_id
            ORDER BY spend_month
        ) AS previous_month_spend
    FROM monthly_spend
)
SELECT
    customer_id,
    spend_month AS spike_month,
    month_spend AS current_month_amount,
    previous_month_spend
FROM spend_comparison
WHERE previous_month_spend IS NOT NULL
  AND month_spend > (previous_month_spend * 3)
ORDER BY customer_id, spend_month;