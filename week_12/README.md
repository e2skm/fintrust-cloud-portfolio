# Week 12 Portfolio

This directory contains the Python and SQL deliverables completed during Week 12 of the FinTrust Cloud Solutions Accelerator program.

## Folder Structure

```text
week_12/
├── python/
│   ├── __init__.py
│   ├── cost_reporting.py
│   ├── generate_report.py
│   └── lambda_function.py
│
└── sql/
    └── fintrust_views.sql
```

## Contents

### Python

| File | Description |
|--------|------------|
| `__init__.py` | Package initialization file that exports reusable functions. |
| `cost_reporting.py` | Cost Explorer reporting module used to retrieve AWS cost data and generate reports. |
| `generate_report.py` | Script that generates CSV and HTML cost reports and uploads them to Amazon S3. |
| `lambda_function.py` | AWS Lambda handler used to automate scheduled cost reporting through EventBridge. |

### SQL

| File | Description |
|--------|------------|
| `fintrust_views.sql` | FinTrust SQL views and performance optimization indexes created for compliance and database tuning exercises. |

## Skills Demonstrated

- AWS Cost Explorer API integration with Boto3
- Automated CSV and HTML report generation
- Amazon S3 file uploads
- AWS Lambda development
- Amazon EventBridge scheduling
- Python package development
- PostgreSQL query optimization
- SQL indexing strategies
- Database performance tuning
- Compliance-driven database configuration
