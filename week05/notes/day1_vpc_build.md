# Day 1 VPC Build - FinTrust Multi-AZ VPC Lab

## Overview
This lab translates AWS VPC networking theory into a real-world implementation. You will build a highly available Multi-AZ VPC architecture in the **af-south-1 (Cape Town)** region, including subnets, route tables, an Internet Gateway (IGW), NAT Gateways, and layered Security Groups.

---

## Target Architecture

### VPC
| Resource | Name | CIDR | Scope |
|----------|------|------|------|
| VPC | fintrust-vpc | 10.0.0.0/16 | Regional |

### Subnets
| Resource | Name | CIDR | Availability Zone |
|----------|------|------|-------------------|
| Public Subnet 1 | fintrust-public-1a | 10.0.0.0/24 | af-south-1a |
| Public Subnet 2 | fintrust-public-1b | 10.0.1.0/24 | af-south-1b |
| App Subnet 1 | fintrust-app-1a | 10.0.10.0/24 | af-south-1a |
| App Subnet 2 | fintrust-app-1b | 10.0.11.0/24 | af-south-1b |
| Data Subnet 1 | fintrust-data-1a | 10.0.20.0/24 | af-south-1a |
| Data Subnet 2 | fintrust-data-1b | 10.0.21.0/24 | af-south-1b |

---

## Build Steps

### 1. Create the VPC
- Open **VPC Console** → **Create VPC**.
- Select **VPC Only**.
- Name: `fintrust-vpc`
- IPv4 CIDR: `10.0.0.0/16`
- Tenancy: Default

### 2. Create the Subnets
Create all six subnets listed in the architecture table.

Requirements:
- Correct Availability Zone assignment.
- No overlapping CIDR ranges.
- Do not enable auto-assign public IPs yet.

### 3. Create and Attach Internet Gateway
- Create IGW named `fintrust-igw`.
- Attach it to `fintrust-vpc`.
- Verify status is **Attached**.

### 4. Create Public Route Table
Create route table:
- Name: `fintrust-rt-public`
- VPC: `fintrust-vpc`

Add route:
- `0.0.0.0/0` → `fintrust-igw`

Associate:
- fintrust-public-1a
- fintrust-public-1b

### 5. Create NAT Gateways
Allocate:
- 2 Elastic IP addresses

Create:
- `fintrust-nat-1a` in `fintrust-public-1a`
- `fintrust-nat-1b` in `fintrust-public-1b`

Wait until both NAT Gateways reach **Available** status.

### 6. Create Private Route Tables
#### fintrust-rt-private-1a
Route:
- `0.0.0.0/0` → `fintrust-nat-1a`

Associate:
- fintrust-app-1a
- fintrust-data-1a

#### fintrust-rt-private-1b
Route:
- `0.0.0.0/0` → `fintrust-nat-1b`

Associate:
- fintrust-app-1b
- fintrust-data-1b

> Each AZ must use its own NAT Gateway to avoid creating a single-AZ dependency.

### 7. Create Security Groups

#### alb-sg
Inbound:
- HTTPS (443) from `0.0.0.0/0`

#### app-sg
Inbound:
- TCP 8080 from `alb-sg` only

#### db-sg
Inbound:
- PostgreSQL 5432 from `app-sg`
- Redis 6379 from `app-sg`
- MongoDB 27017 from `app-sg`

---

## Verification Checklist

- [ ] VPC exists with CIDR 10.0.0.0/16
- [ ] Six subnets created with correct CIDRs and AZs
- [ ] Internet Gateway attached
- [ ] Public route table configured correctly
- [ ] Both NAT Gateways show Available
- [ ] Private route tables point to the correct NAT Gateway
- [ ] Security Groups created and configured correctly

### Common Mistake
Do **not** associate private application or data subnets with the public route table. Doing so exposes resources to internet routing.

---

## Security Group vs NACL Challenge

### 1. Block all traffic from 41.0.0.0/8
**Answer:** NACL Rule

**Reason:**
Security Groups cannot explicitly deny traffic. NACLs support DENY rules and can block a malicious IP range at the subnet boundary.

### 2. Allow ALB traffic to ECS tasks on port 8080
**Answer:** Security Group Rule

**Reason:**
Allow inbound TCP 8080 on `app-sg` from `alb-sg`.

### 3. Database tier only accessible from the application tier
**Answer:** Security Group Rule

**Reason:**
Configure `db-sg` to allow access only from `app-sg`. This controls access by workload identity rather than IP address.

---

## NACL Statelessness Extension

Scenario:
- Inbound HTTP (80) allowed.
- No outbound rule configured.

Result:
- Client requests reach the server.
- Server responses are blocked.

Why?
- NACLs are stateless.
- Return traffic must be explicitly allowed.

Required outbound ports:
- Ephemeral ports `1024-65535`

---

## Reflection Answers

### Traffic Path: Internet to ECS Task
1. Client sends HTTPS request.
2. Traffic reaches the Internet Gateway.
3. Public route table directs traffic to the ALB in a public subnet.
4. `alb-sg` allows HTTPS traffic.
5. ALB forwards traffic to ECS tasks on port 8080.
6. `app-sg` allows traffic only from `alb-sg`.
7. ECS task processes the request in a private application subnet.

### Public vs Private Route Table
**Public Route Table**
- Contains route `0.0.0.0/0` to an Internet Gateway.
- Enables internet connectivity.

**Private Route Table**
- Routes internet-bound traffic through a NAT Gateway.
- Prevents direct inbound internet access.

**Why it matters:**
Private resources remain protected while still being able to access updates and external services when required.

### One Key Learning
High availability in AWS networking requires separate NAT Gateways and private route tables per Availability Zone to avoid a single point of failure.

---

## Afternoon Checkpoint Summary

### VPC Built
- VPC: `fintrust-vpc`
- CIDR: `10.0.0.0/16`
- Region: `af-south-1`
- Six subnets across two AZs
- One Internet Gateway
- Two NAT Gateways (one per AZ)
- Two private route tables

### Security Layering
- `alb-sg`: 443 from the internet
- `app-sg`: 8080 from ALB only
- `db-sg`: 5432, 6379, and 27017 from app tier only

### Portfolio Artifacts
- VPC architecture notes
- Security Group vs NACL challenge answers
- Traffic path walkthrough (Internet → ECS Task)
