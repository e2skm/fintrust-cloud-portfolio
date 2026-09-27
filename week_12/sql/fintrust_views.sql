-- =====================================================
-- FinTrust Database Views and Performance Indexes
-- Week 12 Day 4 - Compliance and Database Performance
-- =====================================================

-- =====================================================
-- Performance Tuning Indexes
-- =====================================================

-- Index for status and transaction date filtering
-- Optimizes queries such as:
--
-- SELECT *
-- FROM transactions
-- WHERE status = 'PENDING'
--   AND transaction_date >= '2024-01-01';
--
-- Partial index reduces index size and
-- improves performance for common statuses.

CREATE INDEX CONCURRENTLY idx_transactions_status_date
ON transactions (
    status,
    transaction_date DESC
)
WHERE status IN (
    'PENDING',
    'PROCESSING'
);

-- =====================================================
-- Additional Join Optimization Indexes
-- =====================================================

CREATE INDEX CONCURRENTLY idx_transactions_customer
ON transactions (customer_id);

CREATE INDEX CONCURRENTLY idx_transactions_account
ON transactions (account_id);

-- =====================================================
-- Validation Query
-- =====================================================

EXPLAIN ANALYZE
SELECT *
FROM transactions
WHERE status = 'PENDING'
  AND transaction_date >= '2024-01-01';

-- =====================================================
-- Transaction Summary View
-- =====================================================

CREATE OR REPLACE VIEW vw_transaction_summary AS
SELECT
    t.transaction_id,
    t.transaction_date,
    t.status,
    t.amount,
    c.customer_id,
    c.customer_name,
    a.account_id,
    a.account_type
FROM transactions t
INNER JOIN customers c
    ON t.customer_id = c.customer_id
INNER JOIN accounts a
    ON t.account_id = a.account_id;

-- =====================================================
-- Performance Test Query
-- =====================================================

EXPLAIN ANALYZE
SELECT
    t.transaction_id,
    t.amount,
    c.customer_name,
    a.account_type
FROM transactions t
JOIN customers c
    ON t.customer_id = c.customer_id
JOIN accounts a
    ON t.account_id = a.account_id
WHERE t.transaction_date >= '2024-01-01'
  AND t.status = 'PENDING'
ORDER BY t.amount DESC
LIMIT 100;
``