# Week 5 Day 2: Connectivity Design & ALB Path-Based Routing

## Overview
This session covered:
- NAT Gateway high availability architecture
- Application Load Balancer (ALB) path-based routing
- Multi-VPC connectivity architecture design
- Reflection and portfolio activities

Source: CDSAP1 ALB Path-Based Routing Lab & Connectivity Design. (Reference: turn1search1)

---

## 1. NAT High Availability Architecture

### Failure Scenario
FinTrust initially deployed a single NAT Gateway in `af-south-1a` and routed private subnets from both Availability Zones through it.

If `af-south-1a` experiences an outage:
- The NAT Gateway becomes unavailable.
- Private subnets in `af-south-1b` lose outbound internet access.
- ECS tasks cannot pull container images.
- External APIs become unreachable.
- OS updates fail.
- The application can become unavailable.

### Best Practice
Deploy one NAT Gateway per Availability Zone and configure each private route table to use the NAT Gateway within the same AZ.

**Key exam takeaway:**
> No single point of failure + private subnets + internet access = one NAT Gateway per Availability Zone.

---

## 2. ALB Path-Based Routing Lab

### Scenario
FinTrust operates:
- Transaction API service: `/api/*`
- Customer portal service: `/portal/*`

A single Application Load Balancer routes traffic to the correct target group based on the URL path.

### Target Groups
#### api-targets
- Protocol: HTTP
- Port: 8080
- VPC: fintrust-vpc
- Health check: `/api/health`

#### portal-targets
- Protocol: HTTP
- Port: 8080
- VPC: fintrust-vpc
- Health check: `/portal/health`

### ALB Configuration
- Name: `fintrust-alb`
- Scheme: Internet-facing
- IP Type: IPv4
- VPC: `fintrust-vpc`
- Subnets:
  - fintrust-public-1a
  - fintrust-public-1b
- Security Group: `alb-sg`

### Listener Rules
| Path | Target Group |
|------|-------------|
| `/api/*` | api-targets |
| `/portal/*` | portal-targets |
| Default | portal-targets |

### Verification
- Two listener rules configured.
- Default rule configured.
- Target groups healthy or ready for ECS registration.
- ALB DNS name recorded for future Route 53 integration.

### Why ALB Instead of NLB?
ALB operates at Layer 7 and can inspect URL paths. NLB operates at Layer 4 and cannot perform path-based routing.

---

## 3. Connectivity Architecture Design Workshop

### Recommended Services

| Requirement | AWS Service | Justification |
|------------|-------------|---------------|
| Connect prod, dev, and audit VPCs with centralized routing and shared internet egress | Transit Gateway | Supports hub-and-spoke design and transitive routing |
| Private access to compliance SaaS API | AWS PrivateLink | Provides private service access without exposing the VPC to the internet |
| Dedicated low-latency connection to on-premises mainframe | AWS Direct Connect | Dedicated private connection with predictable performance |
| Developer laptop access to dev VPC | AWS Client VPN | Secure remote user access |

### Why Not VPC Peering?
1. Each VPC pair requires a separate peering connection.
2. VPC Peering does not support transitive routing.

Transit Gateway solves both limitations.

---

## 4. Reflection Questions

### Default Route Table
A new VPC route table contains a local route by default that enables communication within the VPC CIDR range.

### Undefined ALB Paths
Traffic sent to `/payments/*` would follow the ALB default rule because no matching path-based rule exists.

### Scalability
- Transit Gateway: connect the new VPC to the central hub.
- VPC Peering: create multiple additional peering relationships.

---

## Portfolio Reflection

### Why Direct Connect Over Site-to-Site VPN?
Direct Connect provides a dedicated private connection with consistent performance, lower latency, and stronger regulatory alignment than internet-based VPN connectivity.

### Request Path Walkthrough
1. User sends request to the application URL.
2. DNS resolves to the ALB.
3. ALB evaluates listener rules.
4. Requests matching `/api/transfer` are forwarded to `api-targets`.
5. ECS task receives and processes the request.
6. Response returns through the ALB to the user.

### PrivateLink vs VPC Peering
- PrivateLink exposes only specific services through endpoints.
- VPC Peering allows broader network-level connectivity between VPCs.

---

## Afternoon Checkpoint Summary

### Load Balancer
- fintrust-alb deployed in public subnets.
- `/api/*` routed to `api-targets`.
- `/portal/*` routed to `portal-targets`.
- ALB selected because it supports Layer 7 path inspection.

### Connectivity
- Transit Gateway selected for multi-VPC connectivity.
- Direct Connect selected for mainframe connectivity.
- Client VPN selected for remote DevOps access.

### Completed Artifacts
- ALB configuration notes
- Connectivity design worksheet
- Request path walkthrough
