# Week 08 - AWS Data Lake Architecture

## Overview

This project demonstrates the design and deployment of an AWS Data Lake Architecture as part of the FinTrust Cloud Portfolio learning journey.

The architecture illustrates how data can be ingested, stored, processed, and accessed using AWS cloud services while following modern data lake principles.

---

## Project Structure

```text
week_08/
│
├── architecture/
│   └── THE_AWS_DATA_LAKE_ARCHITECTURE.png
│
├── application/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── deployment/
│   ├── kubernetes/
│   │   ├── deployment.yaml
│   │   └── service.yaml
│   │
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
└── README.md
```

---

## Architecture Diagram

The architecture diagram can be found in:

```text
architecture/THE_AWS_DATA_LAKE_ARCHITECTURE.png
```

### Key Components

- Data Sources
- Amazon S3 Data Lake Storage
- Data Ingestion Layer
- Data Processing Layer
- Analytics Layer
- Monitoring and Security Services

---

## Application Verification

The deployed containerized application was successfully accessed through the browser and displayed the following message:

> You did it! This is your second containerized App!!

This confirms successful deployment and accessibility of the application.

---

## Technologies Used

- AWS Cloud
- Amazon S3
- Docker
- Kubernetes
- GitHub
- Infrastructure as Code (Terraform)
- Linux

---

## Learning Outcomes

Through this project, the following skills were demonstrated:

- Designing cloud-native architectures
- Working with AWS storage services
- Building and deploying containerized applications
- Version control using Git and GitHub
- Infrastructure automation
- Cloud architecture documentation

---
