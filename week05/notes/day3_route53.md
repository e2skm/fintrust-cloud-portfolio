# Day 3 - Route 53 Hosted Zone Lab & Routing Quiz

## Group Discussion

### 1. What is TTL propagation delay, and why does it matter for Failover routing? What TTL would you set?

TTL (Time To Live) is the amount of time DNS resolvers cache a DNS response before requesting a fresh lookup. TTL propagation delay refers to the time it takes for cached DNS records to expire and for resolvers to obtain updated DNS information.

This is important for Failover routing because users may continue using a cached DNS record that points to a failed primary endpoint until the TTL expires. A lower TTL allows DNS resolvers to request updated records more frequently, enabling faster failover to the standby endpoint.

**Recommended TTL:** 60 seconds for failover scenarios because it balances quick recovery with acceptable DNS query traffic.

---

### 2. FinTrust wants to block users from specific countries due to regulatory restrictions. Which policy enables this? Can it block traffic entirely?

**Geolocation Routing** is the appropriate Route 53 policy because it routes traffic based on the user's geographic location (country, continent, or state in some regions).

However, Route 53 cannot directly block traffic. It can route users from specific countries to a different endpoint, a restricted access page, or a sinkhole endpoint. Complete blocking should be implemented using services such as AWS WAF, CloudFront geographic restrictions, network controls, or application-level logic.

---

### 3. How does Latency routing differ from Geolocation routing? Can a South African user be routed to the US East region under Latency routing?

| Routing Policy | Decision Factor | Purpose |
|---------------|----------------|---------|
| Geolocation | User geographic location | Compliance, legal, and regional requirements |
| Latency | Lowest network latency (RTT) | Best performance and fastest response time |

Yes. Under **Latency Routing**, a South African user could be routed to the **US East** region if AWS determines that the network latency to US East is lower than the latency to other available regions at that time.

---

## Individual Reflection

### 1. Explain the weighted routing configuration you built. How would you change the weights for a gradual rollout (0% → 10% → 50% → 100%)?

The lab used **Weighted Routing** to support a canary deployment strategy.

- Production ALB: Weight 90
- Canary ALB: Weight 10

This configuration sends approximately 90% of traffic to the production environment and 10% to the new version.

A gradual rollout could follow this process:

| Stage | Production | Canary |
|---------|------------|--------|
| Initial | 100 | 0 |
| Test | 90 | 10 |
| Expanded | 50 | 50 |
| Full Deployment | 0 | 100 |

This reduces deployment risk because traffic is shifted incrementally while monitoring application health and performance.

---

### 2. In what scenario would Geoproximity routing be better than Geolocation routing?

Geoproximity routing is better when traffic should be routed to the closest AWS Region or resource based on geographic distance rather than strict country boundaries.

Example:

- Geolocation: All users in South Africa must go to the Cape Town region.
- Geoproximity: Users are routed to the nearest available resource and traffic can be adjusted using bias values.

This is useful for optimizing performance, balancing traffic between regions, and supporting business expansion without relying on fixed geographic rules.

---

### 3. A client asks: “Can Route 53 replace my load balancer?” How do you answer?

No. Route 53 and Application Load Balancers serve different purposes.

**Route 53:**
- DNS service
- Directs users to endpoints
- Makes routing decisions before a connection is established
- Supports policies such as Weighted, Failover, Latency, and Geolocation

**Application Load Balancer (ALB):**
- Distributes traffic across targets
- Performs health checks
- Supports Layer 7 routing features
- Handles active application traffic

Route 53 can distribute traffic between endpoints at the DNS level, but it cannot replace the advanced traffic management and request processing capabilities of a load balancer. In most architectures, Route 53 and ALB work together.

---

## Key Takeaways

- Alias records are preferred for AWS resources because they are free, support root domains, and automatically track resource IP changes.
- CNAME records can only be used for subdomains and cannot be used at the zone apex.
- Weighted routing is ideal for canary deployments.
- Failover routing requires health checks and typically benefits from a low TTL (around 60 seconds).
- Geolocation routing supports compliance requirements, while Latency routing optimizes performance.
