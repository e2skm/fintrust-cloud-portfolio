# FinTrust 7-Layer Database Architecture Diagram

## Architecture Flow

```text
                     FinTrust 7-Layer AWS Database Stack

  Flat-File NAS
        |
        | AWS DMS (Full Load + CDC)
        v
+-------------------------------+
| L1: RDS PostgreSQL Multi-AZ   |
| Region: af-south-1            |
+-------------------------------+
              |
              +----------------------> +------------------------------+
              |                         | L2: Aurora PostgreSQL       |
              |                         | Read Replica                |
              |                         | Region: af-south-1          |
              |                         +------------------------------+
              |
              +----------------------> +------------------------------+
              |                         | L4: Amazon QLDB            |
              |                         | Region: af-south-1         |
              |                         +------------------------------+
              |
              +----------------------> +------------------------------+
              |                         | L5: Amazon DocumentDB      |
              |                         | Region: af-south-1         |
              |                         +------------------------------+
              |
              +----------------------> +------------------------------+
              |                         | L6: ElastiCache Redis      |
              |                         | Region: af-south-1         |
              |                         +------------------------------+

+----------------------------------+
| L3: DynamoDB Global Tables       |
| Regions: af-south-1, eu-west-1   |
+----------------------------------+

+----------------------------------+
| L7: Amazon Redshift              |
| Region: af-south-1               |
+----------------------------------+
```

## Service Summary

| Layer | Service | Region(s) | Role | Why This Service Was Chosen |
|-------|---------|-----------|------|-----------------------------|
| L1 | RDS PostgreSQL Multi-AZ | af-south-1 | Core transactions, balances, payments and transfers | Chosen because financial transactions require ACID compliance and Multi-AZ failover to maintain availability during infrastructure failures. |
| L2 | Aurora PostgreSQL Read Replica | af-south-1 | Reporting and analytics queries | Chosen to offload read traffic from the primary database and improve reporting performance without impacting transactional workloads. |
| L3 | DynamoDB Global Tables | af-south-1, eu-west-1 | Customer sessions and login state | Chosen to provide active-active multi-region writes with very low latency and automatic replication between regions. |
| L4 | Amazon QLDB | af-south-1 | Regulatory audit ledger | Chosen because FinTrust requires a tamper-evident and cryptographically verifiable history of transaction changes. |
| L5 | Amazon DocumentDB | af-south-1 | Trade confirmation documents | Chosen because flexible JSON document structures support different trade types without frequent schema changes. |
| L6 | ElastiCache for Redis | af-south-1 | FX rates cache and leaderboards | Chosen because in-memory storage delivers sub-millisecond responses and supports high-performance caching with Multi-AZ resilience. |
| L7 | Amazon Redshift | af-south-1 | Historical analytics and risk reporting | Chosen because columnar storage and MPP processing make large-scale analytical queries much faster than transactional databases. |

## Migration Path

```text
Flat-File NAS
    |
    | AWS Database Migration Service (DMS)
    | Full Load + CDC (Change Data Capture)
    v
RDS PostgreSQL Multi-AZ (af-south-1)
```

**CDC (Change Data Capture)** ensured that changes made to the source system during migration were continuously replicated to RDS PostgreSQL, enabling a near zero-downtime cutover.
