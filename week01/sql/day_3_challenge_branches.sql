-- ════════════════════════════════════════════════════════════
-- FinTrust Bank — Core Database Schema
-- Database: fintrust_db
-- Region: af-south-1 (Cape Town) — POPIA data residency
-- ════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS fintrust_db
    CHARACTER SET utf8mb4     -- supports all Unicode characters (names, emojis)
    COLLATE utf8mb4_unicode_ci; -- case-insensitive comparison

USE fintrust_db;

-- ────────────────────────────────────────────────────────────
-- TABLE: customers
-- One row per FinTrust Bank account holder.
-- ────────────────────────────────────────────────────────────
CREATE TABLE customers (
    customer_id  INT   PRIMARY KEY AUTO_INCREMENT, -- Auto-incrementing PK: no manual ID management
    first_name   VARCHAR(100)  NOT NULL,  -- 100 chars covers all names including compound names
    last_name    VARCHAR(100)  NOT NULL,
    email        VARCHAR(200)  UNIQUE NOT NULL, -- UNIQUE: one account per email. NOT NULL: required field.
    province     VARCHAR(50),  -- Nullable: customers may not disclose province
    created_at   DATETIME DEFAULT CURRENT_TIMESTAMP -- Audit timestamp — set by DB, not application code
);

-- ────────────────────────────────────────────────────────────
-- TABLE: accounts
-- One row per bank account. One customer may have multiple accounts.
-- ────────────────────────────────────────────────────────────
CREATE TABLE accounts (
    account_id  INT PRIMARY KEY AUTO_INCREMENT,
    customer_id  INT NOT NULL,  -- FK to customers — references parent customer
    account_type  ENUM('CHEQUE','SAVINGS','CREDIT','BUSINESS') NOT NULL, -- ENUM: database enforces valid values
    account_number  VARCHAR(20)   UNIQUE NOT NULL, -- VARCHAR not INT: account numbers have prefixes (FT-CHQ-...)
    balance   DECIMAL(15,2) DEFAULT 0.00, -- DECIMAL not FLOAT: exact financial values
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)-- Referential integrity: no orphaned accounts
);

-- ────────────────────────────────────────────────────────────
-- TABLE: transactions
-- One row per financial event. Links to accounts via FK.
-- ────────────────────────────────────────────────────────────
CREATE TABLE transactions (
    transaction_id INT  PRIMARY KEY AUTO_INCREMENT,
    account_id INT  NOT NULL,   -- FK to accounts
    transaction_type  ENUM('DEBIT','CREDIT','PAYMENT') NOT NULL,
    amount DECIMAL(15,2) NOT NULL, -- NOT NULL: every transaction must have an amount
    merchant_category VARCHAR(100), -- Nullable: internal transfers have no merchant
    transaction_date  DATETIME DEFAULT CURRENT_TIMESTAMP,-- Immutable audit timestamp
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

SHOW TABLES;

SELECT COUNT(*) AS total_rows FROM customers;

SHOW CREATE TABLE accounts;

CREATE TABLE branches(
	branch_id INT PRIMARY KEY AUTO_INCREMENT,
	branch_name ENUM('Sandton City Center', 'Cape Town CBD', 'Johhanesburg CBD', 'Pretoria CBD','Melrose',
	'Rosebank','Polokwane CBD','Mokopane','Hillbrow ','New Town','Port Elizabeth CBD','Soweto CBD',
	'Clear Water branch', 'Four Ways branch') NOT NULL,
	province ENUM('Eastern Cape','Free State','Gauteng','KwaZulu-Nata','Limpopo','Mpumalanga','Northern Cape',
	'North West','Western Cape') NOT NULL,
	city ENUM('Johannesburg','Cape Town','Durban','Pretoria','Pietermaritzburg','Gqeberha','East London','Bloemfontein',
	'Vereeniging','Soweto') NOT NULL,
    created_at DATETIME      DEFAULT CURRENT_TIMESTAMP
);

SHOW TABLES;

ALTER TABLE accounts ADD COLUMN branch_id INT, ADD FOREIGN KEY (branch_id) REFERENCES branches(branch_id);


-- CUSTOMERS: 5 rows across different provinces
INSERT INTO customers (first_name, last_name, email, province) VALUES
    ('Thabo',    'Nkosi',    'thabo.nkosi@gmail.com',      'Gauteng'),
    ('Amahle',   'Dlamini',  'amahle.dlamini@outlook.com', 'KwaZulu-Natal'),
    ('Sipho',    'Mokoena',  'sipho.m@fintrust.co.za',    'Gauteng'),
    ('Zanele',   'Khumalo',  'zanele.k@gmail.com',        'Western Cape'),
    ('Bongani',  'Zulu',  'b.zulu@webmail.co.za',      'Eastern Cape');

-- ACCOUNTS: 5 rows (some customers have multiple accounts)
INSERT INTO accounts (customer_id, account_type, account_number, balance) VALUES
    (1, 'CHEQUE',   'FT-CHQ-000001', 15250.00),
    (1, 'SAVINGS',  'FT-SAV-000001', 42000.75),
    (2, 'CHEQUE',   'FT-CHQ-000002',  8900.50),
    (3, 'BUSINESS', 'FT-BUS-000001', 120000.00),
    (4, 'SAVINGS',  'FT-SAV-000002',  3250.25);

-- TRANSACTIONS: 5 rows referencing the accounts above
INSERT INTO transactions (account_id, transaction_type, amount, merchant_category) VALUES
    (1, 'DEBIT',   250.00,  'Groceries'),
    (1, 'DEBIT',   1500.00, 'Electronics'),
    (2, 'CREDIT',  5000.00, 'Salary'),
    (3, 'DEBIT',   89.99,   'Fuel'),
    (4, 'PAYMENT', 350.00,  'Utilities');

-- BRANCHES: 5 rows referencing the accounts above
INSERT INTO branches (branch_name, province, city)VALUES
    ('Sandton City Center', 'Gauteng', 'Johannesburg'),
    ('Cape Town CBD', 'Western Cape', 'Cape Town'),
    ('Pretoria CBD', 'Gauteng', 'Pretoria'),
    ('Port Elizabeth CBD', 'Eastern Cape', 'Gqeberha'),
    ('Soweto CBD', 'Gauteng', 'Soweto');
    
-- Verify all three tables have data
SELECT * FROM customers;
SELECT * FROM accounts;
SELECT * FROM transactions;
SELECT * FROM branches;

-- Count rows in each table
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'accounts',   COUNT(*) FROM accounts
UNION ALL
SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL
SELECT 'branches', COUNT(*) FROM branches;      