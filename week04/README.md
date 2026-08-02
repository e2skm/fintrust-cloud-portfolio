# week04 Folder Structure

# Week 04 – FinTrust Data Processing Pipeline

## Overview

This week focused on building a modular Python data processing pipeline for FinTrust. The project demonstrates how to organize Python applications using packages, interact with databases, perform data analysis, generate reports, implement custom exception handling, and apply debugging techniques.

The solution processes transaction data, enriches records, stores information in a database, and produces analytical reports.

---

## Learning Objectives

- Build modular Python applications
- Organize code using packages and modules
- Work with SQLite databases
- Implement custom exception classes
- Debug Python applications
- Process and analyze CSV data
- Generate automated reports
- Apply software engineering best practices

---

## Project Structure

```text
week04/
├── README.md
├── python/
│   ├── main.py
│   ├── analyse.py
│   ├── pipeline.py
│   ├── transactions.py
│   ├── creating_custom_exception_classes.py
│   ├── debugg_me.py
│   └── fintrust_pipeline/
│       ├── __init__.py
│       ├── loader.py
│       ├── database.py
│       └── reporter.py
├── data/
│   ├── transactions.csv
│   ├── transactions_enriched.csv
│   ├── daily_report.txt
│   └── fintrust_analytics.db
├── architecture/
│   └── db-architecture-diagram.md
├── notes/
│   └── reflection.md
└── requirements.txt
```

---

## Key Components

### Data Ingestion

The pipeline loads transaction data from CSV files and prepares it for further processing.

### Database Integration

Transaction data is stored in a SQLite database to support querying and reporting.

### Data Analysis

Analytical scripts evaluate transaction activity and generate insights from the processed data.

### Reporting

The reporting module generates daily reports summarizing transaction information and key metrics.

### Exception Handling

Custom exception classes were implemented to improve error handling and produce more meaningful feedback when problems occur.

### Debugging Practice

Debugging exercises were completed to identify, troubleshoot, and resolve issues within Python applications.

---

## Files Created

### Python Scripts

- `main.py`
- `analyse.py`
- `pipeline.py`
- `transactions.py`
- `creating_custom_exception_classes.py`
- `debugg_me.py`

### Package Modules

- `loader.py`
- `database.py`
- `reporter.py`

### Data Files

- `transactions.csv`
- `transactions_enriched.csv`
- `daily_report.txt`
- `fintrust_analytics.db`

### Documentation

- `db-architecture-diagram.md`
- `reflection.md`

---

## Technologies Used

- Python 3
- SQLite
- CSV Processing
- Object-Oriented Programming
- Custom Exceptions
- Modular Programming
- Git & GitHub

---

## Outcomes

By completing this project, I gained practical experience in:

- Designing modular Python applications
- Building reusable packages
- Managing structured data with SQLite
- Creating data processing pipelines
- Debugging and troubleshooting code
- Implementing robust exception handling
- Generating automated reports

---

## Reflection

This week strengthened my understanding of how real-world data engineering and analytics workflows are structured. Building the FinTrust pipeline helped reinforce software development best practices, modular design principles, and the importance of writing maintainable and reliable Python applications.
