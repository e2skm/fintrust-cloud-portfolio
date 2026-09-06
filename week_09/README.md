# Week 09 Python Projects

This directory contains Python scripts developed during Week 09 of the Cloud to Solutions Accelerator programme. The projects focus on AWS governance, cost management, migration monitoring, disaster testing, and data transfer planning using the AWS SDK for Python (`boto3`).

## Folder Structure

```text
week_09/
└── README.md
└── python/
    ├── fintrust_governance_report.py
    ├── fintrust_monthly_report.py
    ├── fintrust_tco_break_even.py
    └── fis_experiment_status_checker.py
```

## Project Overview

### 1. fintrust_governance_report.py

**Purpose:**  
Generates a FinTrust governance and compliance report by auditing AWS resource tags and identifying non-compliant resources.

**Key Features**
- Uses the AWS Resource Groups Tagging API.
- Identifies resources missing required tags.
- Groups violations by AWS service.
- Supports governance reporting and compliance tracking.
- Can be extended for automatic tag remediation.

**AWS Services**
- Resource Groups Tagging API
- Amazon S3
- AWS Service Catalog

---

### 2. fintrust_monthly_report.py

**Purpose:**  
Produces a monthly operational or governance summary for FinTrust cloud environments.

**Potential Reporting Areas**
- Resource inventory
- Tagging compliance
- Service usage
- Governance metrics
- Cost allocation summaries

**AWS Services**
- AWS Service Catalog
- Resource Groups Tagging API
- Amazon S3

---

### 3. fintrust_tco_break_even.py

**Purpose:**  
Calculates migration and transfer planning metrics to determine Total Cost of Ownership (TCO) and break-even points for large-scale data migration projects.

**Key Features**
- Snow Family transfer planning.
- Device capacity calculations.
- Transfer timeline estimation.
- Comparison between network and offline migration methods.
- Migration cost modelling support.

**AWS Services**
- AWS Snowball Edge
- AWS Snowcone
- AWS Snowmobile

---

### 4. fis_experiment_status_checker.py

**Purpose:**  
Monitors and reports on AWS Fault Injection Simulator (FIS) experiments.

**Key Features**
- Lists recent FIS experiments.
- Retrieves experiment details.
- Displays experiment status and stop conditions.
- Supports resilience and chaos engineering initiatives.
- Tracks experiment lifecycle events.

**AWS Services**
- AWS Fault Injection Simulator (FIS)
- Amazon CloudWatch

---

## Skills Demonstrated

- Python scripting
- AWS SDK for Python (boto3)
- Governance automation
- Tag compliance auditing
- Cost governance
- Migration planning
- Disaster recovery testing
- Operational reporting
- AWS service integrations

---

## Requirements

Install dependencies:

```bash
pip install boto3
```

Configure AWS credentials:

```bash
aws configure
```

Required permissions vary by script but may include:

- Resource Groups Tagging API access
- Service Catalog access
- AWS Fault Injection Simulator access
- Amazon S3 permissions
- Migration and governance-related IAM permissions

---

## Learning Outcomes

These projects demonstrate practical cloud engineering skills including:

- Automating governance controls.
- Building compliance reporting tools.
- Monitoring migration activities.
- Planning large-scale data transfers.
- Assessing resilience through chaos engineering.
- Applying FinOps and cloud governance principles in AWS.

---

