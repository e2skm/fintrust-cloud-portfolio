-- SQL Common Table Expressions (CTEs) and Recursive Queries

/*====================================================
A01 - Basic CTE Example
====================================================*/
WITH monthly_totals AS (
    SELECT
        account_id,
        DATE_TRUNC(''month'', transaction_date) AS txn_month,
        SUM(amount) AS total_amount,
        COUNT(*) AS txn_count
    FROM transactions
    GROUP BY account_id, DATE_TRUNC(''month'', transaction_date)
)
SELECT
    account_id,
    txn_month,
    total_amount
FROM monthly_totals
WHERE total_amount > 50000
ORDER BY total_amount DESC;

/*====================================================
A02 - Chaining Multiple CTEs
====================================================*/
WITH recent_activity AS (
    SELECT
        account_id,
        COUNT(*) AS txn_count_30d,
        SUM(amount) AS total_30d
    FROM transactions
    WHERE transaction_date >= CURRENT_DATE - INTERVAL ''30 days''
    GROUP BY account_id
),
avg_velocity AS (
    SELECT
        AVG(txn_count_30d) AS avg_count,
        STDDEV(txn_count_30d) AS stddev_count
    FROM recent_activity
),
flagged_accounts AS (
    SELECT
        r.account_id,
        r.txn_count_30d,
        r.total_30d
    FROM recent_activity r, avg_velocity a
    WHERE r.txn_count_30d > a.avg_count + (2 * a.stddev_count)
)
SELECT
    f.account_id,
    a.customer_name,
    f.txn_count_30d,
    f.total_30d
FROM flagged_accounts f
JOIN accounts a
    ON f.account_id = a.account_id
ORDER BY f.txn_count_30d DESC;

/*====================================================
A03 - Recursive CTE
====================================================*/
WITH RECURSIVE account_hierarchy AS (
    SELECT
        account_id,
        parent_account_id,
        account_name,
        0 AS depth
    FROM accounts
    WHERE parent_account_id IS NULL

    UNION ALL

    SELECT
        a.account_id,
        a.parent_account_id,
        a.account_name,
        h.depth + 1
    FROM accounts a
    JOIN account_hierarchy h
        ON a.parent_account_id = h.account_id
)
SELECT
    account_id,
    account_name,
    depth
FROM account_hierarchy
ORDER BY depth, account_name;

/*====================================================
Exercise 1 - Month-over-Month Growth
====================================================*/
WITH monthly_totals AS (
    SELECT
        account_id,
        DATE_TRUNC(''month'', transaction_date) AS month_start,
        SUM(amount) AS monthly_total
    FROM transactions
    GROUP BY account_id, DATE_TRUNC(''month'', transaction_date)
),
previous_month AS (
    SELECT
        account_id,
        month_start,
        monthly_total,
        LAG(monthly_total) OVER (
            PARTITION BY account_id
            ORDER BY month_start
        ) AS previous_total
    FROM monthly_totals
),
growth_rates AS (
    SELECT
        account_id,
        month_start,
        monthly_total,
        previous_total,
        ((monthly_total - previous_total)
          / NULLIF(previous_total,0)::NUMERIC) * 100 AS growth_pct
    FROM previous_month
)
SELECT *,
       CASE WHEN growth_pct > 100 THEN ''FLAG'' ELSE ''OK'' END AS status
FROM growth_rates;

/*====================================================
Exercise 2 - Top 10 Percent Accounts Using DENSE_RANK
====================================================*/
WITH account_totals AS (
    SELECT
        account_id,
        SUM(amount) AS total_transaction_value
    FROM transactions
    GROUP BY account_id
),
ranked_accounts AS (
    SELECT
        account_id,
        total_transaction_value,
        DENSE_RANK() OVER (
            ORDER BY total_transaction_value DESC
        ) AS rank_value
    FROM account_totals
),
rank_stats AS (
    SELECT MAX(rank_value) AS max_rank
    FROM ranked_accounts
)
SELECT
    r.account_id,
    r.total_transaction_value,
    r.rank_value
FROM ranked_accounts r
CROSS JOIN rank_stats s
WHERE r.rank_value <= CEILING(s.max_rank * 0.10)
ORDER BY r.rank_value, r.total_transaction_value DESC;
