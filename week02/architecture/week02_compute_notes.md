flowchart LR
    A\[Customer Transaction\] --\> B{Lambda: assess\_transaction}
    B -- BLOCKED --\> C\[Reject + Log\]
    B -- PENDING --\> D\[Send OTP via SNS\]
    B -- REVIEW --\> E\[Flag in DynamoDB\]
    B -- APPROVED --\> F\[Process via Core Banking API on ECS Fargate\]
    F --\> G\[(RDS PostgreSQL)\]

## AWS Compute Services Comparison

| Feature | AWS EC2 | AWS Lambda | AWS ECS |
|---------|---------|------------|---------|
| Service Type | Virtual machines | Serverless functions | Container orchestration service |
| Management | User manages OS, patches, and scaling | AWS manages infrastructure | AWS manages orchestration; user manages containers |
| Scaling | Manual or Auto Scaling | Automatic per invocation | Automatic via service scaling |
| Pricing Model | Pay for instance runtime | Pay per request and execution time | Pay for underlying compute resources |
| Best For | Long-running applications, custom environments | Event-driven workloads, APIs, automation | Containerized microservices and applications |
| Startup Time | Minutes | Milliseconds to seconds | Seconds to minutes depending on task/image |
| Stateful Workloads | Supported | Generally stateless | Supported through containerized architectures |
