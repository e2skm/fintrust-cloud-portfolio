use fintrust_db;

-- WRONG: first_name and last_name not in GROUP BY
SELECT
    c.first_name,         -- Not aggregated
    c.last_name,          -- Not aggregated
    c.province,           -- Not aggregated
    COUNT(t.transaction_id) AS transaction_count
FROM customers c
INNER JOIN transactions t ON ...  -- abbreviated
GROUP BY c.province;              -- Only province — ERROR or wrong results

-- CORRECT: All non-aggregated columns in GROUP BY
SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id) AS transaction_count
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY
    c.customer_id,   -- Include customer_id to ensure uniqueness
    c.first_name,
    c.last_name,
    c.province
ORDER BY transaction_count DESC;

-- The SQL execution order (conceptual):
-- 1. FROM / JOIN    — Combine tables
-- 2. WHERE          — Filter individual rows
-- 3. GROUP BY       — Create groups
-- 4. HAVING         — Filter groups
-- 5. SELECT         — Calculate output columns
-- 6. ORDER BY       — Sort

-- Example: FinTrust provinces with high credit volume
SELECT
    c.province,
    COUNT(t.transaction_id)  AS credit_count,
    SUM(t.amount)            AS total_credits
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'credit'    -- Step 2: filter rows to credits only
GROUP BY c.province                    -- Step 3: group by province
HAVING SUM(t.amount) > 100000         -- Step 4: keep only high-volume provinces
ORDER BY total_credits DESC;           -- Step 6: sort result

SELECT
    c.customer_id,
    CONCAT(c.first_name, ' ', c.last_name)  AS customer_name,
    c.province,
    COUNT(DISTINCT a.account_id)             AS num_accounts,
    COUNT(t.transaction_id)                  AS total_transactions,
    SUM(CASE WHEN t.transaction_type = 'credit'
             THEN t.amount ELSE 0 END)       AS total_deposits,
    SUM(CASE WHEN t.transaction_type = 'debit'
             THEN t.amount ELSE 0 END)       AS total_withdrawals,
    AVG(t.amount)                            AS avg_transaction,
    MAX(t.amount)                            AS largest_transaction,
    MAX(a.balance)                           AS highest_balance
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
ORDER BY total_deposits DESC;