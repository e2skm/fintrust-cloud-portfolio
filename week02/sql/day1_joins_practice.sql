use fintrust_db;

-- INNER JOIN: only customers WITH accounts
SELECT c.first_name, c.last_name, a.account_type
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id;

-- LEFT JOIN: ALL customers, NULL for those without accounts
SELECT c.first_name, c.last_name, a.account_type
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id;

-- Anti-JOIN: ONLY customers WITHOUT accounts
SELECT c.first_name, c.last_name
FROM customers c
LEFT JOIN accounts a ON c.customer_id = a.customer_id
WHERE a.account_id IS NULL;

-- FinTrust: Complete customer transaction history
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance  AS current_balance,
    t.transaction_id,
    t.amount,
    t.transaction_type,    -- 'credit' or 'debit'
    t.transaction_date
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
ORDER BY
    c.last_name,
    t.transaction_date DESC;
    
-- Challenge 1: Find all customers who have a cheque account with a balance below R 1,000. Show: first name, last name, province, and balance. 
-- Sort by balance ascending.
SELECT 
	c.first_name,
    c.last_name,
    c.province, 
    a.balance
FROM customers c 
INNER JOIN accounts a
	ON c.customer_id = a.customer_id
WHERE (a.balance < 1000)
ORDER BY a.balance;

-- Challenge 2: List all transactions made by customers from Western Cape. Show: customer name, transaction amount, transaction type,
-- and date. Use a 3-table JOIN. Sort by date descending.
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    t.amount,
    t.transaction_type,
    t.transaction_date
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE c.province = 'Western Cape'
ORDER BY t.transaction_date DESC;
    
    
-- Challenge 3: Find all accounts that have NO transactions recorded. Use a LEFT JOIN from accounts to transactions. 
-- Show: account_id, account_type, balance, and customer name (requires joining to customers too).
SELECT 
    a.account_id,
    a.account_type,
    a.balance,
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name
FROM accounts a
LEFT JOIN customers c
    ON a.customer_id = c.customer_id
LEFT JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.account_id IS NULL;

-- FinTrust: All Gauteng customers with savings accounts
SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.account_type = 'savings'
ORDER BY a.balance DESC;

-- FinTrust: Large transactions for a specific customer
SELECT
    c.first_name,
    c.last_name,
    t.amount,
    t.transaction_type,
    t.transaction_date
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
INNER JOIN transactions t ON a.account_id = t.account_id
WHERE c.last_name = 'Nkosi'
  AND t.amount > 5000
ORDER BY t.transaction_date DESC;

-- Return customer first name, last name, account type, and current balance for all customers. Sort by balance descending.
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

-- Find all customers from Gauteng with a balance greater than R 25,000. Show: name, province, account type, balance.
SELECT 
	CONCAT(c.first_name, ' ', last_name) as customer_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
	ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng' 
	AND (a.balance > 25000);
    
-- Join all three tables. Show: customer name, account type, transaction amount, and transaction date. Filter to only debit transactions.
-- Sort by transaction date descending    
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    a.account_type,
    t.amount AS transaction_amount,
    t.transaction_date
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'Debit'
ORDER BY t.transaction_date DESC;

-- Find any customers who have never made a transaction. Use a LEFT JOIN from customers → accounts → transactions with an IS NULL filter.
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.province
FROM customers c
LEFT JOIN accounts a
    ON c.customer_id = a.customer_id
LEFT JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_id IS NULL;

-- Find all transactions greater than R 10,000 for customers in Western Cape or KwaZulu-Natal. 
-- Show customer name, province, and transaction amount. Sort by amount descending
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
    c.province,
    t.amount AS transaction_amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE c.province IN ('Western Cape', 'KwaZulu-Natal')
    AND t.amount > 10000
ORDER BY t.amount DESC;