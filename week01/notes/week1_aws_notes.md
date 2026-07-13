# Week 1 AWS Notes

# Cloud to Solutions Accelerator – Week 1 Summary

These notes summarise what I learned during Week 1. The goal is to simplify the key concepts and create a quick study guide for revision and future AWS Solutions Architect Associate (SAA-C03) exam preparation.

---

# Day 1 – Programme Foundation & AWS Cloud Quest Introduction

## What I Learned

- The Cloud to Solutions Accelerator programme is designed to prepare learners for the AWS Solutions Architect Associate (SAA-C03) certification.
- The programme combines four learning streams:
  - AWS & Cloud
  - SQL & Data Engineering
  - Python Programming
  - Solutions Architecture
- The FinTrust Bank scenario is used throughout the programme to apply cloud concepts in a real-world business case.

## Cloud Quest Labs Completed

### Cloud First Steps

Objectives completed:
- Launched Amazon EC2 instances.
- Deployed workloads across multiple Availability Zones.
- Learned the importance of High Availability.
- Used Amazon EBS volumes with EC2 instances.

### Key Takeaway

Running workloads in multiple Availability Zones reduces the risk of downtime when a single Availability Zone fails.

---

# Day 2 – AWS Global Infrastructure

## AWS Regions and Availability Zones

A Region is a geographical location that contains AWS data centres.

Each Region contains multiple Availability Zones (AZs).

Benefits:
- High availability
- Fault tolerance
- Disaster recovery
- Reduced latency for users

## How to Choose an AWS Region (CPLG)

### C – Compliance
- Regulatory requirements
- Data residency rules
- POPIA compliance

### P – Proximity
- Choose regions closer to users.
- Improves application responsiveness.

### L – Latency
- Lower latency means faster communication.
- Important for customer-facing applications.

### G – Go-Live Cost
- AWS pricing differs by Region.
- Consider infrastructure and data transfer costs.

## Amazon Machine Images (AMIs)

### What is an AMI?

An AMI is a template used to launch EC2 instances.

It contains:
- Operating system
- Software packages
- Configuration settings

### Important Concepts

#### AMI ID
Unique identifier of an AMI.

Example:
```
ami-1234567890abcdef
```

#### Copy AMI
Used when:
- Migrating workloads to another Region.
- Creating backups of custom AMIs.
- Supporting disaster recovery.

---

# Day 3 – EC2 Compute Services

## Cloud Quest Labs Completed

### Cloud Computing Essentials

Objectives completed:
- Configured static website hosting using Amazon S3.
- Worked with bucket policies.
- Hosted website content in S3.
- Renamed website objects.

### Key Takeaway

Amazon S3 can be used as a highly available, low-cost static website hosting platform.

---

## EC2 Instance Families

### T Family – Burstable

Best for:
- Small applications
- Development environments
- Low traffic websites

Example:
```
t3.micro
```

### C Family – Compute Optimized

Best for:
- CPU-intensive workloads
- Batch processing
- Scientific calculations

### R Family – Memory Optimized

Best for:
- Databases
- Caching systems
- In-memory applications

### I Family – Storage Optimized

Best for:
- High IOPS workloads
- Data warehousing
- NoSQL databases

### P Family – GPU Optimized

Best for:
- AI/ML workloads
- Deep learning
- Graphics rendering

---

## EC2 Pricing Models

### On-Demand

Use when:
- Workloads are unpredictable.
- No long-term commitment is required.

Advantages:
- Flexible
- No upfront costs

### Reserved Instances

Use when:
- Workloads run continuously.
- Long-term savings are needed.

Advantages:
- Significant discounts.

### Spot Instances

Use when:
- Workloads can tolerate interruption.

Advantages:
- Lowest cost.

Disadvantage:
- AWS can reclaim capacity.

### Dedicated Instances

Use when:
- Isolation requirements exist.

### Dedicated Hosts

Use when:
- Specific licensing requirements exist.
- Full visibility of physical servers is needed.

---

# Day 4 – Compute Decision Making & Auto Scaling

## Cloud Quest Labs Completed

### Computing Solutions

Objectives completed:
- Connected to EC2 instances using Systems Manager.
- Viewed instance metadata.
- Changed EC2 instance types.
- Scaled from a smaller instance to a larger instance.

### Key Takeaway

AWS makes it easy to scale compute resources up or down based on workload requirements.

---

## EC2 vs Lambda vs ECS/EKS/Fargate

### EC2

Choose when:
- Full infrastructure control is needed.
- Applications run continuously.
- Custom operating systems are required.

### AWS Lambda

Choose when:
- Execution is event-driven.
- Runtime duration is short.
- No server management is desired.

### ECS/Fargate

Choose when:
- Running containers.
- Simplified container management is required.

### EKS

Choose when:
- Kubernetes is required.
- Advanced container orchestration is needed.

### Quick Comparison

| Factor | EC2 | Lambda | ECS/Fargate | EKS |
|----------|----------|----------|----------|----------|
| Infrastructure Control | High | None | Medium | High |
| Stateful Apps | Good | Limited | Good | Good |
| Long Running Jobs | Excellent | Not Ideal | Excellent | Excellent |
| Operational Overhead | High | Low | Medium | High |

---

## Auto Scaling Groups (ASG)

### Purpose

Automatically add or remove EC2 instances based on demand.

Benefits:
- Better availability
- Improved performance
- Cost optimisation

### ASG Capacity Settings

#### Minimum Capacity
Lowest number of instances.

#### Desired Capacity
Target number of instances.

#### Maximum Capacity
Highest number of instances.

---

## Scaling Policies

### Target Tracking
Maintain a metric at a target value.

Example:
- Keep CPU at 50%.

### Step Scaling
Scale based on threshold ranges.

### Predictive Scaling
Uses historical patterns to predict demand.

### Scheduled Scaling
Scale at specific times.

Example:
- Scale every weekday at 08:00.

---

## Advanced Auto Scaling Features

### Lifecycle Hooks
Pause instances during launch or termination.

Used for:
- Configuration tasks
- Validation checks

### Warm Pools
Pre-initialised instances ready for fast scaling.

### Instance Refresh
Gradually replace existing instances.

Used for:
- New AMIs
- Security updates
- Application updates

---

## Placement Groups

### Cluster Placement Group

Purpose:
- Maximum performance
- Low network latency

### Spread Placement Group

Purpose:
- Maximum fault isolation

### Partition Placement Group

Purpose:
- Large distributed workloads
- Reduce impact of partition failures

---

## EC2 Instance Lifecycle

### Pending
- Instance is launching.
- Billing starts.

### Running
- Instance is active.
- Billing continues.

### Stopping
- Instance shuts down.

### Stopped
- Compute charges stop.
- EBS charges continue.

### Hibernated
- RAM contents saved.
- Faster restart.
- Storage charges continue.

### Terminating
- Instance deleted.
- Instance store data lost.

---

# Day 5 – Architecting for Availability, Recovery & Governance

## Decoupling

Decoupling reduces dependencies between application components.

Benefits:
- Better resilience
- Easier scaling
- Reduced failure impact

Common AWS services:
- SQS
- SNS
- EventBridge

---

## Disaster Recovery

### Two Questions to Ask

#### RPO (Recovery Point Objective)

How much data can we afford to lose?

#### RTO (Recovery Time Objective)

How quickly must we recover?

---

## Disaster Recovery Strategies

### Backup and Restore

Cheapest option.

Characteristics:
- Higher RTO
- Higher RPO

### Pilot Light

Critical systems always running.

Characteristics:
- Faster recovery
- Lower RTO

### Warm Standby

Smaller version of production environment always running.

Characteristics:
- Quick recovery
- Moderate cost

### Multi-Site Active-Active

Full environments running simultaneously.

Characteristics:
- Lowest RTO
- Lowest RPO
- Highest cost

---

## Multi-Account Strategy

### AWS Organizations

Used to centrally manage multiple AWS accounts.

Benefits:
- Governance
- Billing management
- Security controls

### Service Control Policies (SCPs)

Purpose:
- Define maximum permissions.

Remember:
- SCPs do NOT grant permissions.
- SCPs only limit permissions.

### IAM Policies

Purpose:
- Grant permissions to users, groups and roles.

#### Easy Exam Memory Aid

SCP = Guardrails

IAM = Access

---

## AWS Control Tower

Purpose:
- Simplify multi-account setup.
- Apply governance automatically.

### Account Factory

Used to:
- Create standardised AWS accounts.
- Apply governance consistently.

---

# AWS Solutions Architect Associate (SAA-C03) Exam Strategy

## The Four-Step Strategy

### 1. Identify the Requirements

Ask:
- What does the business need?
- What problem must be solved?

### 2. Identify the Constraints

Look for words like:
- Lowest cost
- Lowest latency
- Highest availability
- Most secure
- Serverless

### 3. Eliminate Wrong Answers

Remove options that:
- Don't meet requirements.
- Violate constraints.
- Overcomplicate the solution.

### 4. Reason Through What Remains

Compare remaining answers and choose the AWS service that best satisfies the scenario.

---

# Week 1 Key Takeaways

By the end of Week 1 I understood:

- AWS global infrastructure (Regions and Availability Zones).
- How to choose a Region using CPLG.
- The purpose of AMIs and EC2 instances.
- EC2 instance families and pricing models.
- When to choose EC2, Lambda, ECS, EKS or Fargate.
- Auto Scaling Groups and scaling policies.
- Lifecycle hooks, warm pools and instance refresh.
- Placement groups.
- EC2 lifecycle, billing and data persistence.
- Load balancing concepts.
- Disaster recovery strategies and recovery objectives.
- Multi-account governance using AWS Organizations and Control Tower.
- A repeatable strategy for approaching SAA-C03 exam questions.

Week 1 built the foundation for designing secure, scalable, resilient and cost-effective cloud architectures on AWS.
