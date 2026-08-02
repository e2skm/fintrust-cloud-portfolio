# Fintrust Cloud Portfolio

Fintrust is an online banking application that is currently being developed as part of the Nedbank Cloud Learnership Programme. The project incorporates AWS Services (Free Tier), SQL, Python, and supporting artifacts such as notes in `.md` and `.pdf` formats.

<br>

```text
fintrust-cloud-portfolio/
├── week01/
│   ├── README.md ← Week 1 — Foundation summary
│   ├── sql/
│   │   ├── day3_fintrust_schema.sql ← CREATE TABLE statements
│   │   ├── day4_where_queries.sql ← Lab queries from Day 4 PM
│   │   └── day4_where_challenges.sql ← Challenge queries
│   └── notes/
│       ├── day1_reflection.md ← Day 1 reflection
│       └── week1_aws_notes.md ← Any notes from AM sessions
├── week02/
│   ├── README.md ← Brief summary of what you built this week
│   ├── sql/
│   │   ├── joins_practice.sql ← Day 1 PM: INNER JOIN and LEFT JOIN exercises
│   │   └── aggregates_report.sql ← Day 2 PM: GROUP BY, HAVING, monthly summary
│   ├── python/
│   │   ├── conditionals.py ← Day 4 PM: classify, interest rate, ATM exercises
│   │   ├── day3_exercises.py
│   │   ├── day3_lesson.py
│   │   ├── hello_fintrust.py
│   │   └── transaction_flowchart.py ← Day 4 PM: full decision engine with 5 test cases
│   └── architecture/
│       └── week02_compute_notes.md ← Day 5 AM: Summary of EC2 vs Lambda vs ECS
├── week03/
│   ├── README.md ← Brief summary of Week 3: Python functions, file handling, error handling, logging, and data processing
│   ├── python/
│   │   ├── day1_function_exercises.py
│   │   ├── day2_lesson.py
│   │   ├── day3_input_output_references.py
│   │   ├── fintrust_utils.py
│   │   ├── test_utils.py
│   │   ├── clean_transactions.py
│   │   ├── clean_transactions_v2.py
│   │   ├── error_handling_and_logging_practice.py
│   │   ├── error_handling_and_logging_reference_expanded.py
│   │   ├── data/
│   │   │   ├── raw_transactions.csv
│   │   │   ├── clean_transactions.csv
│   │   │   ├── input.csv
│   │   │   ├── output.csv
│   │   │   ├── out.csv
│   │   │   ├── input.json
│   │   │   ├── config.json
│   │   │   ├── daily_summary.json
│   │   │   ├── file.csv
│   │   │   ├── file.txt
│   │   │   └── test.log
│   │   └── logs/
│   │       ├── pipeline.log
│   │       └── practice.log
│   ├── architecture/
│   │   ├── fintrust_s3_architecture.drawio
│   │   └── fintrust_s3_architecture.png
│   └── notes/
│       └── reflection.md
├──week04/
|  ├── README.md ← Week 4: Building a modular FinTrust data processing pipeline with database integration, reporting, debugging, and custom exception handling
|  ├── python/
|  │   ├── main.py ← Application entry point
|  │   ├── analyse.py ← Transaction analysis and reporting
|  │   ├── pipeline.py ← End-to-end data processing workflow
|  │   ├── transactions.py ← Transaction-related functionality
|  │   ├── creating_custom_exception_classes.py ← Custom exception handling exercises
|  │   ├──SHA_256.py
|  │   ├── debugg_me.py ← Debugging practice and troubleshooting
|  │   └── fintrust_pipeline/
|  │       ├── __init__.py
|  │       ├── loader.py ← Load transaction data
|  │       ├── database.py ← SQLite database operations
|  │       └── reporter.py ← Report generation utilities
|  ├── data/
|  │   ├── transactions.csv ← Source transaction dataset
|  │   ├── transactions_enriched.csv ← Processed and enriched transaction dataset
|  │   ├── daily_report.txt ← Generated transaction report
|  │   └── fintrust_analytics.db ← SQLite database
|  ├── architecture/
|  │   └── db-architecture-diagram.md ← Database design and architecture documentation
|  ├── notes/
|  │   └── reflection.md ← Week 4 reflection and learnings
|  └── requirements.txt ← Python project dependencies
```
