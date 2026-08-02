# Week 4 Reflection

## 1. AWS Database Selection

FinTrust originally stored transactions, login sessions, trade documents, audit history, and analytics data in a single PostgreSQL database. Splitting these workloads across RDS, Aurora, DynamoDB, QLDB, DocumentDB, and Redshift is justified because each workload has different performance, consistency, and scalability requirements. For example, RDS provides ACID-compliant transactions, DynamoDB Global Tables supports active-active multi-region session management, QLDB provides immutable audit records, and Redshift is optimized for OLAP analytics over billions of rows. A single large RDS instance could perform all functions, but it would become a bottleneck and force transactional, caching, document, and analytics workloads to compete for the same resources. The operational cost is increased complexity because teams must manage multiple services, monitoring dashboards, backup strategies, security policies, and data integration paths between platforms.

## 2. ETL Pipeline

If two instances of pipeline.py ran simultaneously against the same SQLite database, file locking and concurrent write issues could occur because SQLite is a file-based database and is not designed for highly concurrent multi-user workloads. RDS Multi-AZ solves infrastructure availability by synchronously replicating writes to a standby instance in another Availability Zone, providing near-zero RPO and automatic failover if the primary instance fails. However, Multi-AZ does not solve read scaling or database migration requirements. Read Replicas solve read-scaling by serving reporting queries, while AWS DMS with CDC solves continuous replication and zero-downtime migration by keeping source and target systems synchronized during cutover.

## 3. Python Packaging

Refactoring pipeline.py into a fintrust_pipeline package makes it much easier to separate extraction, transformation, validation, configuration, and loading logic into reusable modules. Instead of maintaining one large script, individual components can be imported and tested independently using unit tests. New functionality can be added without modifying unrelated code, which reduces the risk of introducing defects. The package structure also makes deployment, versioning, documentation, and collaboration easier because developers can work on separate modules while sharing a common package.

## 4. Week 4 to Week 5 Bridge

The first required network configuration is placing RDS PostgreSQL, Aurora, Redshift, and ElastiCache Redis in private subnets. This prevents direct internet access and ensures that only approved application servers or internal services can connect through controlled security group rules. The second configuration is a DynamoDB Gateway Endpoint inside the VPC. The Gateway Endpoint allows private access to DynamoDB without traversing the public internet, improving security and reducing dependency on NAT gateways. Together, private subnets and Gateway Endpoints help enforce network isolation while still allowing the database services to communicate with approved workloads inside the VPC.
