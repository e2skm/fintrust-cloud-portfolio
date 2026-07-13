Use fintrust_db;

-- Find customers by partial name (useful for search boxes)
SELECT * FROM customers
WHERE last_name LIKE 'Nk%'; -- finds Nkosi, Nkuna, Nkabinde...

-- Find branches in the Central Business District
SELECT * FROM branches
WHERE branch_name LIKE '%CBD'; 

-- Find transactions over 1000
SELECT * FROM transactions
WHERE amount > 1000 ; 

-- Find accounts by prefix pattern
SELECT * FROM accounts
WHERE account_number LIKE 'FT-CHQ%'; -- all cheque accounts

-- Find corporate email addresses in SA
SELECT * FROM customers
WHERE email LIKE '%.%@%.co.za'; -- firstname.lastname@domain

-- Find all non-gmail, non-outlook customers
SELECT * FROM customers
WHERE email NOT LIKE '%gmail%'
  AND email NOT LIKE '%outlook%';
  
-- This might miss transactions at 14:30:00 on 2026-07-09
SELECT * FROM transactions
WHERE transaction_date < '2026-07-09';

-- Better: use DATE() function to compare date portion only
SELECT * FROM transactions
WHERE DATE(transaction_date) < '2026-07-09';

-- Transactions in July 2026
SELECT * FROM transactions
WHERE transaction_date BETWEEN '2026-07-01' AND '2026-07-31 23:59:59';

-- Transactions in the last 30 days (relative)
SELECT * FROM transactions
WHERE transaction_date >= NOW() - INTERVAL 30 DAY;

-- Find all transactions in a specific year
SELECT * FROM transactions
WHERE YEAR(transaction_date) = 2026;

-- Find all transactions in July of any year
SELECT * FROM transactions
WHERE MONTH(transaction_date) = 7;

-- Combine: July 2026 specifically
SELECT * FROM transactions
WHERE YEAR(transaction_date) = 2026
  AND MONTH(transaction_date) = 7;
  
-- Combine: 8 July 2026 specifically
SELECT * FROM transactions
WHERE YEAR(transaction_date) = 2026
  AND MONTH(transaction_date) = 7
  AND DAY(transaction_date) = 8;
  
-- NULL is NOT the same as zero
SELECT * FROM accounts WHERE balance = 0;   -- returns accounts WITH balance of zero
SELECT * FROM accounts WHERE balance IS NULL; -- returns accounts where balance was never set

-- NULL is NOT the same as empty string
SELECT * FROM customers WHERE province = '';      -- empty string (0 chars)
SELECT * FROM customers WHERE province IS NULL;   -- truly unknown/unset

-- THE CLASSIC MISTAKE: comparing with = NULL always returns nothing
SELECT * FROM transactions WHERE merchant_category = NULL; -- WRONG! Returns 0 rows
SELECT * FROM transactions WHERE merchant_category IS NULL; -- CORRECT

-- NULL in aggregations: COUNT(*) includes NULL rows, COUNT(col) excludes them
SELECT
    COUNT(*)                  AS total_transactions,
    COUNT(merchant_category)  AS transactions_with_merchant,
    COUNT(*) - COUNT(merchant_category) AS transactions_no_merchant
FROM transactions;

-- Step 1: Get all DEBIT transactions
SELECT * FROM transactions
WHERE transaction_type = 'DEBIT';

-- Step 2: Add amount filter
SELECT * FROM transactions
WHERE transaction_type = 'DEBIT'
  AND amount > 500;  
  
-- Step 3: Add date range
SELECT * FROM transactions
WHERE transaction_type = 'DEBIT'
  AND amount > 500
  AND YEAR(transaction_date) = 2026;
  
-- Step 4: Also include PAYMENT type with same amount threshold
SELECT * FROM transactions
WHERE (transaction_type = 'DEBIT' OR transaction_type = 'PAYMENT')
  AND amount > 500
  AND YEAR(transaction_date) = 2026;

-- Cleaner version using IN:
SELECT * FROM transactions
WHERE transaction_type IN ('DEBIT', 'PAYMENT')
  AND amount > 500
  AND YEAR(transaction_date) = 2026;

-- Find all customers NOT from Gauteng or Western Cape.  
SELECT * FROM customers
WHERE province NOT IN ('Gauteng', 'Western Cape');

-- Find all accounts with a balance between R1,000 and R20,000 (inclusive) of type CHEQUE or SAVINGS.
SELECT * FROM accounts
WHERE balance BETWEEN 1000 AND 20000 
AND account_type IN ('CHEQUE','SAVINGS');

-- Find all transactions with a merchant_category that contains the word 'Food' OR 'Groceries', for amounts over R200.
SELECT * FROM transactions
WHERE merchant_category = 'Food' OR merchant_category = 'Groceries';

-- Find all DEBIT transactions where no merchant_category was recorded AND the amount is greater than R100.
SELECT * FROM transactions
WHERE transaction_type = 'DEBIT' 
AND merchant_category IS NULL 
AND amount > 100;

--  Find all customers whose email address ends in either '.co.za' or '.com', 
-- ordered by last_name ascending, and who have their province recorded.
SELECT * FROM customers
WHERE email LIKE '%.co.za' OR email LIKE '%.com'
AND province IS NOT NULL
ORDER BY last_name;


  