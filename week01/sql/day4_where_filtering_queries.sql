use fintrust_db;

-- Find all cutomers in Gauteng
SELECT * FROM customers WHERE province = 'Gauteng';

-- Find all customers with a balance over R500
SELECT account_id, account_number, balance
FROM accounts
WHERE balance > 10000;

-- Find all transactions equal to or over R500
SELECT * FROM transactions WHERE amount >= 500;

-- Find customers whose email contains 'gmail'
SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%gmail%';

-- Find accounts whose account_number starts with 'FT-SAV'
SELECT * FROM accounts
WHERE account_number LIKE 'FT-SAV%';

-- Find last names with exactly 4 characters
SELECT last_name FROM customers
WHERE last_name LIKE '____'; -- four underscores

-- IN: match any value in a list (replaces multiple OR conditions)
SELECT * FROM customers
WHERE province IN ('Gauteng', 'Western Cape', 'KwaZulu-Natal');

-- BETWEEN: match values within a range (inclusive of both endpoints)
SELECT * FROM transactions
WHERE amount BETWEEN 100 AND 1000;

-- Equivalent to: WHERE amount >= 100 AND amount <= 1000
SELECT * FROM transactions
WHERE amount >= 100 OR amount <= 1000;

-- Find transactions with an empty merchant_category
SELECT * FROM transactions
WHERE merchant_category IS NULL;

-- Find customers who have provided their province
SELECT * FROM customers
WHERE province IS NOT NULL;


-- AND: BOTH conditions must be true
SELECT * FROM accounts
WHERE account_type = 'SAVINGS' AND balance > 5000;

-- OR: EITHER condition must be true
SELECT * FROM customers
WHERE province = 'Gauteng' OR province = 'Western Cape';

-- NOT: reverses the condition
SELECT * FROM transactions
WHERE NOT transaction_type = 'CREDIT';

-- Equivalent to: WHERE transaction_type != 'CREDIT'
SELECT * FROM transactions
WHERE transaction_type != 'CREDIT';

-- Find Savings and Cheue accounts with a balance over R10000 (Problem)
SELECT * FROM accounts
WHERE account_type = 'SAVINGS' OR account_type = 'CHEQUE'
  AND balance > 10000;

-- Evaluated as: SAVINGS OR (CHEQUE AND balance > 10000)
-- This returns ALL SAVINGS accounts + only high-balance CHEQUE accounts
-- Probably NOT what was intended!

-- SOLUTION: Use parentheses to be explicit
SELECT * FROM accounts
WHERE (account_type = 'SAVINGS' OR account_type = 'CHEQUE')
  AND balance > 10000; -- Now returns SAVINGS or CHEQUE accounts where balance > 10000
  
-- Find all customers who are not from Gauteng.
SELECT * FROM customers
WHERE province != 'Gauteng';

-- Find all accounts with a balance greater than R5,000.
SELECT * FROM accounts 
WHERE balance > 5000;

-- Find all customers whose email address ends in '.co.za'.
SELECT * FROM customers 
WHERE email LIKE '%.co.za';

-- Find all transactions of type DEBIT or PAYMENT (using IN, not multiple ORs).
SELECT * FROM transactions
WHERE transaction_type IN ('DEBIT','PAYMENT');

-- Find all SAVINGS accounts with a balance between R1,000 and R50,000.
SELECT * FROM accounts
WHERE account_type = 'SAVINGS'
AND balance BETWEEN 1000 AND 50000;

-- Find all transactions that DO have a merchant_category recorded (not NULL).
SELECT * FROM transactions
WHERE merchant_category IS NOT NULL;



