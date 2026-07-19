# Week 02 — Compute, SQL Aggregates & Python Fundamentals

## What I Built
- SQL queries demonstrating INNER JOIN, LEFT JOIN, GROUP BY, and HAVING
  on the FinTrust Bank transactions dataset
- Python functions implementing a real-time fraud decision engine
  using if/elif/else, Boolean logic, and the `in` operator

## Key Concepts Demonstrated
- EC2 vs Lambda vs ECS: when to use each compute service
- EBS volume type selection (gp3 vs io2)
- SQL aggregate functions with GROUP BY and HAVING
- Python: Decimal for currency, conditional logic, early return pattern

## How to Run
```bash
# SQL (requires SQLite)
sqlite3 :memory: ".read sql/joins_practice.sql"

# Python
python python/transaction_flowchart.py
python python/conditionals.py
```

## Architecture Context
All FinTrust artifacts are part of a 16-week cloud project simulating
a South African digital bank operating in the af-south-1 Region.
See `/architecture/week02_compute_notes.md` for service decisions.

## Files
| File | Description |
|------|-------------|
| `sql/joins_practice.sql` | INNER JOIN and LEFT JOIN exercises |
| `sql/aggregates_report.sql` | Monthly transaction summary with GROUP BY |
| `python/conditionals.py` | Transaction classifier, interest rate, ATM logic |
| `python/transaction_flowchart.py` | Full fraud decision engine with 5 test cases |