-- SQL Window Functions - OVER, PARTITION BY, ORDER BY
-- Generated from training material

/* ======================================================
   A01 - Window Function Syntax Template
====================================================== */
SELECT
    column1,
    column2,
    window_function() OVER (
        PARTITION BY partition_column
        ORDER BY sort_column ASC
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) AS result_column
FROM table_name;

/* ======================================================
   A02 - Ranking Functions Example
   Top transaction per account per month
====================================================== */
WITH ranked_transactions AS (
    SELECT
        account_id,
        transaction_date,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY account_id, DATE_TRUNC('month', transaction_date)
            ORDER BY amount DESC
        ) AS rank_in_month
    FROM transactions
)
SELECT *
FROM ranked_transactions
WHERE rank_in_month = 1;

/* ======================================================
   A03 - Aggregate Windows and Lead/Lag
====================================================== */
SELECT
    account_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        PARTITION BY account_id
        ORDER BY transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS running_total,

    AVG(amount) OVER (
        PARTITION BY account_id
        ORDER BY transaction_date
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
    ) AS seven_day_avg,

    LAG(amount, 1, 0) OVER (
        PARTITION BY account_id
        ORDER BY transaction_date
    ) AS prev_amount,

    LEAD(amount, 1, 0) OVER (
        PARTITION BY account_id
        ORDER BY transaction_date
    ) AS next_amount
FROM transactions;

/* ======================================================
   Exercise 1
   Top 3 transactions by amount for each customer
====================================================== */
WITH customer_rankings AS (
    SELECT
        customer_id,
        transaction_date,
        amount,
        ROW_NUMBER() OVER (
            PARTITION BY customer_id
            ORDER BY amount DESC
        ) AS txn_rank
    FROM transactions
)
SELECT
    customer_id,
    transaction_date,
    amount,
    txn_rank
FROM customer_rankings
WHERE txn_rank <= 3;

/* ======================================================
   Exercise 2
   Month-over-month percentage change per account
====================================================== */
WITH monthly_totals AS (
    SELECT
        account_id,
        DATE_TRUNC('month', transaction_date) AS month_start,
        SUM(amount) AS monthly_total
    FROM transactions
    GROUP BY account_id, DATE_TRUNC('month', transaction_date)
),
monthly_change AS (
    SELECT
        account_id,
        month_start,
        monthly_total,
        LAG(monthly_total) OVER (
            PARTITION BY account_id
            ORDER BY month_start
        ) AS previous_month_total
    FROM monthly_totals
)
SELECT
    account_id,
    month_start,
    monthly_total,
    previous_month_total,
    ROUND(
        ((monthly_total - previous_month_total)
        / NULLIF(previous_month_total, 0)) * 100,
        2
    ) AS percentage_change,
    CASE
        WHEN ABS(
            ((monthly_total - previous_month_total)
            / NULLIF(previous_month_total, 0)) * 100
        ) > 50 THEN 'FLAG'
        ELSE 'OK'
    END AS status
FROM monthly_change;

/* ======================================================
   Exercise 3
   Quartiles based on yearly transaction volume
====================================================== */
WITH account_totals AS (
    SELECT
        account_id,
        SUM(amount) AS total_transaction_volume
    FROM transactions
    WHERE EXTRACT(YEAR FROM transaction_date) = EXTRACT(YEAR FROM CURRENT_DATE)
    GROUP BY account_id
)
SELECT
    account_id,
    total_transaction_volume,
    NTILE(4) OVER (
        ORDER BY total_transaction_volume DESC
    ) AS quartile
FROM account_totals;
