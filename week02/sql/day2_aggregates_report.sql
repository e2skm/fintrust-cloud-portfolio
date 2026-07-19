use fintrust_db;

-- Total number of transactions
SELECT COUNT(*) AS total_transactions
FROM transactions;

-- Total value of all credits (deposits)
SELECT SUM(amount) AS total_deposits
FROM transactions
WHERE transaction_type = 'credit';

-- Average account balance across all accounts
SELECT AVG(balance) AS avg_balance
FROM accounts;

-- Highest single transaction amount
SELECT MAX(amount) AS largest_transaction
FROM transactions;

-- Total transactions per account type
SELECT
    a.account_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount)           AS total_amount
FROM accounts a
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY a.account_type
ORDER BY total_amount DESC;

-- Average balance by province
SELECT
    c.province,
    COUNT(a.account_id)  AS account_count,
    AVG(a.balance)       AS avg_balance,
    SUM(a.balance)       AS total_deposits
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.province
ORDER BY total_deposits DESC;

-- Customer transaction summary — total transactions and amount per customer
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id)  AS total_transactions,
    SUM(t.amount)            AS total_amount,
    AVG(t.amount)            AS avg_transaction
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
ORDER BY total_amount DESC;

-- WRONG: Cannot use aggregate in WHERE
SELECT c.province, COUNT(*) AS account_count
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
WHERE COUNT(*) > 2   -- ERROR: can't use aggregate in WHERE
GROUP BY c.province;

-- CORRECT: Use HAVING for aggregate filter
SELECT c.province, COUNT(*) AS account_count
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.province
HAVING COUNT(*) > 2  -- Filter GROUPS where count > 2
ORDER BY account_count DESC;

-- Combined: WHERE filters rows, HAVING filters groups
SELECT
    c.province,
    a.account_type,
    COUNT(t.transaction_id) AS transaction_count,
    SUM(t.amount)           AS total_amount
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
WHERE t.transaction_type = 'debit'     -- Filter rows: debits only
GROUP BY c.province, a.account_type
HAVING SUM(t.amount) > 50000           -- Filter groups: high-volume only
ORDER BY total_amount DESC;

-- Monthly transaction volumes by account type
SELECT
    YEAR(t.transaction_date)   AS year,
    MONTH(t.transaction_date)  AS month,
    a.account_type,
    COUNT(t.transaction_id)    AS transaction_count,
    SUM(t.amount)              AS monthly_volume
FROM accounts a
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY
    YEAR(t.transaction_date),
    MONTH(t.transaction_date),
    a.account_type
ORDER BY year DESC, month DESC, monthly_volume DESC;

-- Top 5 FinTrust customers by total transaction amount
SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id)  AS num_transactions,
    SUM(t.amount)            AS total_transacted,
    MAX(t.amount)            AS largest_single_transaction
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
ORDER BY total_transacted DESC
LIMIT 5;

-- Exercise 1: Transactions summary per customer
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.province,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_transaction_amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
HAVING COUNT(t.transaction_id) > 0
ORDER BY total_transaction_amount DESC;

-- Exercise 2: Average balance per account type
SELECT
    account_type,
    COUNT(*) AS number_of_accounts,
    AVG(balance) AS average_balance
FROM accounts
GROUP BY account_type
ORDER BY average_balance DESC;

-- Exercise 3: Provinces with deposits exceeding R100,000
SELECT
    c.province,
    SUM(t.amount) AS total_deposit_amount,
    COUNT(t.transaction_id) AS credit_transaction_count
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'CREDIT'
GROUP BY c.province
HAVING SUM(t.amount) > 100000
ORDER BY total_deposit_amount DESC;

-- Exercise 4: Monthly transaction summary
SELECT
    YEAR(transaction_date) AS txn_year,
    MONTH(transaction_date) AS txn_month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_transaction_amount
FROM transactions
GROUP BY
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY 
	txn_year,
	txn_month;
    
-- Exercise 5: Custom*rs with more than 3 debit transact*ons in one day
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    DATE(t.transaction_date) AS transaction_day,
    COUNT(*) AS debit_count
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    DATE(t.transaction_date)
HAVING COUNT(*) > 3
ORDER BY debit_count DESC, transaction_day;