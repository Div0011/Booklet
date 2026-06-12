# 41. System Design Basics (Scalability & Architecture)

## 1. Introduction

### What it is
System Design is the process of defining the architecture, components, modules, interfaces, and databases for a system to satisfy specified technical and business requirements. It focuses on scaling software applications to handle massive user traffic and data volumes.

### Why it exists
A single computer has physical CPU and memory limits. When a web application scales from a few hundred local users to millions of global visitors, a single server will crash under the load. System design provides the architectural patterns, database schemas, and caching layouts required to distribute computational work across clusters of thousands of machines, ensuring high availability and low latency.

### Problems it solves
- **Single Point of Failure (SPOF)**: Eliminates system vulnerability where a single server crash takes down the entire application.
- **Scaling Bottlenecks**: Prevents database congestion, memory exhaustion, and bandwidth limits from stalling application performance.
- **Data Inconsistency**: Manages data synchronization when multiple database instances write updates concurrently.

### Industry Use Cases
- **High-Traffic Web Applications**: Scaling platforms like Google, Netflix, and Amazon to manage millions of concurrent user sessions.
- **Distributed Databases**: Configuring systems like Cassandra, DynamoDB, or PostgreSQL clusters to partition data globally.
- **Real-Time Streaming Systems**: Deploying message brokers (like Kafka or RabbitMQ) to process gigabytes of streaming data per second.

---

## 2. Core Concepts

### Beginner Concepts
- **Vertical vs. Horizontal Scaling**:
  - *Vertical Scaling (Scale-Up)*: Adding more power (CPU, RAM) to a single server. Limited by hardware boundaries and introduces a single point of failure (SPOF).
  - *Horizontal Scaling (Scale-Out)*: Adding more servers to the resource pool. Unlimited scaling potential, requiring load balancers to distribute requests.
- **Load Balancers**: Devices that sit between clients and servers, distributing incoming network traffic across a cluster of backend servers to prevent overload:
  - *Round Robin*: Sends requests sequentially down the list.
  - *Least Connections*: Directs traffic to the server with the active connections.
  - *IP Hash*: Uses client IP addresses to determine which server receives the request, keeping user sessions stable.
- **Monolithic vs. Microservices Architecture**:
  - *Monolith*: Single, unified codebase. Simple to deploy, but difficult to scale independently.
  - *Microservices*: Decoupled services communicating over network APIs (REST, gRPC). Scalable and modular, but introduces network latency and synchronization complexity.

### Intermediate Concepts
- **Caching Strategies**: Storing frequently accessed data in fast memory (like Redis or Memcached) to reduce database load:
  - *Cache-Aside (Lazy Loading)*: The application queries the cache first. If a miss occurs, it queries the database, updates the cache, and returns the data.
  - *Write-Through*: Data is written to the cache and database simultaneously.
  - *Write-Behind (Write-Back)*: Data is written to the cache instantly, and asynchronously written to the database after a delay.
- **Database Partitioning & Sharding**:
  - *Vertical Partitioning*: Splitting tables by columns (e.g. moving heavy text fields to a separate table).
  - *Horizontal Partitioning (Sharding)*: Splitting tables by rows across multiple databases based on a partition key (e.g. users with IDs 1-1M go to Database A, IDs 1M-2M go to Database B).
- **Database Replication**: Copying data across multiple database instances:
  - *Leader-Follower (Master-Slave)*: Writes go to the Leader database, which syncs data to Read-Only Followers. This optimizes read-heavy applications.

### Advanced Concepts
- **CAP Theorem**: States that in a distributed data store, you can only guarantee two out of the three properties:
  - **Consistency (C)**: Every read receives the most recent write or an error.
  - **Availability (A)**: Every non-failing node returns a response, without guaranteeing it contains the most recent write.
  - **Partition Tolerance (P)**: The system continues to operate despite network partition drops.
- **Consistent Hashing**: A hashing scheme that assigns database servers and data keys to positions on a virtual hash ring. This ensures that when a server is added or removed, only a minimal fraction of keys need to be rehashed and migrated.
- **Rate Limiting**: Algorithms used to control the rate of traffic sent by clients to prevent service overload:
  - *Token Bucket*: Tokens are added to a bucket at a fixed rate. Requests consume a token. If the bucket is empty, requests are rejected. Supports bursts of traffic.
  - *Leaky Bucket*: Requests enter a queue and are processed at a constant rate. Excess requests overflow and are dropped.
- **Message Queues**: Decouples application layers by processing tasks asynchronously using Publish/Subscribe pipelines (e.g. Kafka, RabbitMQ).

---

## 3. Internal Working

### Distributed Web Architecture Pipeline

When millions of users access a modern web application, requests flow through a decoupled, multi-layered infrastructure to optimize latency and reliability:

```text
[ Global Client Users ]
        |
        v
    [ DNS Routing ] ---> Resolves IP to closest CDN Edge
        |
  +-----v-------------- CDN / Edge Caching Node (Caches static images/pages) --+
  | (Cache Miss)                                                               |
  +-----+----------------------------------------------------------------------+
        |
        v
  [ Load Balancer (Nginx) ] ---> SSL Termination & Health checks
        | (Routes traffic using IP Hash or Least Connections)
        v
  [ Web Server Cluster (Next.js / Node / Go) ] ---> Stateless application layer
    /                       \
   v (Cache Aside)           v (Asynchronous task)
[ Cache (Redis) ]        [ Message Queue (Kafka) ] ---> Worker servers
   |                         |
   v (Cache Miss)            v (Database write)
[ Database Shards ]      [ Analytics Engine ]
  - Shard 1 (A-M)
  - Shard 2 (N-Z)
  (Leader-Follower setup)
```

1. **DNS Routing & CDNs**:
   - The DNS routes client requests to the closest **Content Delivery Network (CDN)** edge node.
   - If the request targets static assets (images, CSS, JS), the CDN returns them instantly from edge memory, avoiding server round-trips.
2. **Load Balancer (Nginx/HAProxy)**:
   - Evaluates incoming network traffic, performs SSL termination (decrypting HTTPS traffic to save CPU cycles on application servers), and runs health checks.
   - It routes traffic only to healthy instances using load-balancing algorithms.
3. **Stateless App Servers**:
   - Application servers run stateless code. They do not store user sessions locally; instead, sessions are stored in shared memory (like Redis).
   - This allows the load balancer to route requests to any server in the cluster, making scaling out simple.
4. **Consistent Hashing Ring**:
   - Sharded databases determine key placement using a Consistent Hashing Ring.
   - Both data keys and server nodes are hashed into a range (e.g., $0$ to $2^{32}-1$).
   - A key is stored on the first active server node encountered by moving clockwise from the key's hash position on the ring.
   - If Server `B` crashes, only the keys previously mapped to `B` are migrated to its clockwise neighbor `C`. The rest of the keys on other servers remain untouched, preventing cache stampedes.

---

## 4. Important Terminology

- **SPOF (Single Point of Failure)**: Any component in a system whose failure stops the entire system from working.
- **CAP Theorem**: The distributed database trade-off rule stating that under a network partition, a system must choose between Consistency and Availability.
- **Consistent Hashing**: A hashing layout on a circular ring that minimizes key reshuffling when database instances are added or removed.
- **Replication Lag**: The delay in propagating updates from a Leader database to its read-only Follower replicas.
- **Horizontal Sharding**: Partitioning database table rows across separate physical servers to distribute storage and query loads.

---

## 5. Beginner Examples

### Example 1: Implementing a Round-Robin Load Balancer Simulation
This example simulates a basic load balancer distributing client requests across healthy backend servers sequentially.

```python
class RoundRobinLoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0

    def get_server(self, client_ip):
        if not self.servers:
            return None
        
        # Select the server at the current index
        selected_server = self.servers[self.current_index]
        
        # Advance the index, wrapping around to 0 when the end is reached
        self.current_index = (self.current_index + 1) % len(self.servers)
        
        print(f"Routing request from {client_ip} to: {selected_server}")
        return selected_server

# Demonstration
lb = RoundRobinLoadBalancer(["Server-A", "Server-B", "Server-C"])
clients = ["192.168.1.1", "192.168.1.2", "192.168.1.3", "192.168.1.4"]

for client in clients:
    lb.get_server(client)
# Expected Output:
# Routing request from 192.168.1.1 to: Server-A
# Routing request from 192.168.1.2 to: Server-B
# Routing request from 192.168.1.3 to: Server-C
# Routing request from 192.168.1.4 to: Server-A
```

---

## 6. Intermediate Examples

### Example 1: Consistent Hashing Implementation
A simple Python simulation demonstrating how keys and nodes are placed on a virtual ring using hashing.

```python
import hashlib

class ConsistentHashRing:
    def __init__(self, nodes=None):
        self.ring = {}  # Maps sorted hash values to server nodes
        self.sorted_keys = [] # List of sorted hash values on the ring
        if nodes:
            for node in nodes:
                self.add_node(node)

    def _hash(self, key: str) -> int:
        # Generate MD5 hash and convert it to an integer
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_node(self, node: str):
        node_hash = self._hash(node)
        self.ring[node_hash] = node
        self.sorted_keys.append(node_hash)
        self.sorted_keys.sort()

    def remove_node(self, node: str):
        node_hash = self._hash(node)
        if node_hash in self.ring:
            del self.ring[node_hash]
            self.sorted_keys.remove(node_hash)

    def get_node(self, key: str) -> str:
        if not self.ring:
            return None
        
        key_hash = self._hash(key)
        
        # Traverse the ring clockwise to find the first node with hash >= key_hash
        for val in self.sorted_keys:
            if key_hash <= val:
                return self.ring[val]
                
        # If key_hash is greater than all nodes, wrap around to the first node
        return self.ring[self.sorted_keys[0]]

# Usage
ring = ConsistentHashRing(["Server-1", "Server-2", "Server-3"])
data_keys = ["user_101", "product_402", "order_902"]

for key in data_keys:
    print(f"Key '{key}' is stored on: {ring.get_node(key)}")
```

---

## 7. Advanced Concepts

### CAP Theorem Deep Dive & Distributed Consistency Models

#### CP vs. AP Distributed Database Implementations
When a network partition occurs (represented as a network connection drop between databases), a distributed system must choose between:
- **CP (Consistency / Partition Tolerance)**: The system rejects incoming write requests on isolated nodes to prevent data conflicts. It prioritizes data correctness over availability (e.g. HBase, Redis Cluster setups).
- **AP (Availability / Partition Tolerance)**: Nodes continue to accept writes and reads. However, data will differ across database partitions until the network issue is resolved and synchronization completes. It prioritizes availability over immediate consistency (e.g. Cassandra, DynamoDB).

```text
[ Network Partition Event ]
Database Node A (Isolated)  <--X-- (Link Down) --X-->  Database Node B (Active)
          |                                                      |
    [ Client Request ]                                     [ Client Request ]
       "Write User=Alex"                                     "Read User"
          |                                                      |
    If CP: Rejects write (Errors)                          If AP: Returns old data ("User=null")
    If AP: Accepts write (Saves locally)
```

#### Eventual Consistency
In AP systems, replica nodes synchronize asynchronously.
- **Eventual Consistency**: The system guarantees that if no new updates are made, all replicas will eventually sync and return the same data. However, there is a window where reads can return stale data.
- **Strong Consistency**: Every write must be committed to a quorum of nodes before the write is confirmed, ensuring subsequent reads always return the latest write, but increasing latency.

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for structured problem-solving, trade-off analysis, and clear communication. They do not want you to jump directly to drawing boxes. Instead, they evaluate how you clarify requirements, calculate resource estimations, identify bottlenecks, and make architectural decisions.

### Red Flags
- **Database Sharding by Default**: Recommending database sharding immediately to solve a database load issue, without considering simpler optimizations like caching, indexing, or read replicas.
- **Violating the CAP Theorem**: Claiming a distributed architecture guarantees both strong consistency and 100% availability under a network partition.
- **Ignoring Resource Estimations**: Designing a media streaming platform without calculating storage sizes, bandwidth limits, or read/write ratios.

### Green Flags
- **Requirement Clarification**: Spending the first 5 minutes of the interview asking questions to define system scale (e.g. Daily Active Users, read/write ratios, latency budgets).
- **Evaluating Trade-offs**: Discussing the trade-offs of different solutions (e.g. SQL vs NoSQL, Latency vs Consistency).
- **Graceful Degradation**: Proposing backpressure management, rate limiting, and fallback options (e.g. queuing tasks when traffic spikes).

### Answers Matrix

| Level | Question: "How would you design a scalable image upload microservice?" |
|---|---|
| **Rejected** | "Build an API endpoint. When an image arrives, write it to the local disk, update the SQL database, and return a success response." |
| **Shortlisted** | "Implement an API. Send images directly to a storage bucket like S3. Save the image metadata and URL in a sharded database, and cache images using a CDN." |
| **Selected** | "First, estimate the write volume. To handle high traffic and avoid blocking application threads, clients request a presigned upload URL from our API gateway. The client then uploads the image directly to a storage bucket (like AWS S3), bypassing our application servers. S3 triggers an event that pushes a task to a Message Queue (like RabbitMQ). Background workers consume tasks from the queue to generate image thumbnails asynchronously. Image URLs and metadata are stored in a relational database with read replicas, and static images are cached globally using a CDN (like Cloudflare) to ensure fast delivery." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the CAP Theorem and its real-world implications.
- **Detailed Answer**: The CAP Theorem states that a distributed data store can guarantee at most two out of three properties: Consistency, Availability, and Partition Tolerance.
  - In practice, network partitions (P) are inevitable in distributed systems. Therefore, systems must choose between:
    - **Consistency (CP)**: Rejects writes on isolated nodes to prevent data conflicts, sacrificing Availability.
    - **Availability (AP)**: Accepts reads and writes on all nodes, returning stale or conflicting data, sacrificing Consistency.
  - For example, banking systems prioritize CP to prevent balance inconsistencies. Social media feeds prioritize AP to keep the app functional even if posts are temporarily out of sync.
- **Follow-up Questions**: How does the PACELC theorem extend this? (Answer: PACELC states that even when the system is running normally without partitions (E), it must choose between Latency (L) and Consistency (C)).
- **Interviewer's Expectations**: Define each property accurately and explain the trade-offs under network partitions.

#### 2. How does Consistent Hashing prevent cache stampedes when scaling database clusters?
- **Detailed Answer**: In standard hashing (e.g. `hash(key) % N`), adding or removing a server node changes the divisor $N$. This changes the target location for almost all keys. If a cache cluster scales out, all cached items are invalidated, causing a cache stampede that overwhelms the database.
  - **Consistent Hashing** maps both keys and servers to a virtual ring. When a server is added or removed, only keys close to that server's position are remapped. This minimizes key migration, protecting database performance.
- **Follow-up Questions**: How do you prevent key clustering if server hashes are not evenly distributed? (Answer: Use Virtual Nodes. Each physical server is mapped to multiple virtual positions on the ring, ensuring an even distribution of keys).
- **Interviewer's Expectations**: Contrast standard hashing with consistent hashing and explain key migration logic.

---

### Scenario-Based Questions

#### 3. Design a URL shortening service like TinyURL.
- **Detailed Answer**:
  - **Estimations**: Assume 100M URLs generated per month.
    - Total Writes: $100\text{M} / 30\text{ days} / 86400\text{s} \approx 40 \text{ writes/sec}$.
    - Assuming a 10:1 read/write ratio, Reads $\approx 400 \text{ reads/sec}$.
    - Storage: If each entry is 500 bytes, total storage per year is:
      $$100\text{M} \times 12 \text{ months} \times 500 \text{ bytes} \approx 600\text{ GB per year}$$
  - **URL Generation**: Convert auto-incrementing database IDs to **Base62** strings (using characters `a-z, A-Z, 0-9`). A 6-character string yields $62^6 \approx 56.8 \text{ billion}$ unique URLs.
  - **Database Choice**: A NoSQL key-value store (like DynamoDB or Cassandra) is ideal since we only need simple key-value lookups (`ShortURL -> LongURL`), which NoSQL databases handle with high throughput and horizontal scalability.
  - **Caching**: Cache popular URLs in Redis using an LRU (Least Recently Used) eviction policy.
- **Follow-up Questions**: How do you prevent duplicate URL generation in a distributed environment? (Answer: Use a Distributed Range Coordinator, like ZooKeeper, to assign distinct ID blocks to each server).
- **Interviewer's Expectations**: Perform resource estimations, design the URL hashing logic, select the database, and propose caching strategies.

#### 4. Design a distributed Rate Limiter for an API gateway.
- **Detailed Answer**:
  - To implement a rate limiter across a cluster of servers, we need a shared data store. We use **Redis** to store request counts.
  - We select the **Token Bucket** algorithm for efficiency:
    - Each user key maps to a Redis hash containing two fields: `tokens` (current count) and `last_updated` (timestamp).
    - When a request arrives:
      1. Fetch the user's bucket data from Redis.
      2. Calculate how many tokens should be added based on the time elapsed since `last_updated`.
      3. If tokens exist, decrement the token count by 1 and allow the request. Otherwise, reject it.
      4. Save the updated token count and timestamp back to Redis.
  - To prevent race conditions from concurrent requests, we execute the check inside a **Redis Lua script**, which runs atomically.
- **Follow-up Questions**: How do you handle rate-limiting if Redis crashes? (Answer: Fall back to local in-memory rate limiting or allow requests to pass, prioritizing availability over rate enforcement).
- **Interviewer's Expectations**: Detail the database schema, rate-limiting algorithm, and atomic execution patterns.

---

### Debugging Questions

#### 5. Debug a system bottleneck where a database's primary node is overwhelmed by read operations during peak traffic.
- **Detailed Answer**:
  - **Root Cause**: The system uses a single database instance to process both write and read operations. During peak traffic, the volume of read requests consumes all available database connections and disk I/O, slowing down writes.
  - **Fixes**:
    1. **Implement Database Replication**: Deploy read-only database replicas (Followers). Configure the application to send write operations to the primary node and read operations to the replicas.
    2. **Introduce a Cache**: Cache popular query results in Redis.
    3. **Query Optimization**: Add indexes to slow-running queries and optimize execution plans.
- **Follow-up Questions**: How do you handle replication lag when a user updates their profile and immediately views it? (Answer: Route user-specific queries to the primary database for a short window after a write, or enforce read-your-own-writes consistency).
- **Interviewer's Expectations**: Propose read replicas, caching, and index optimizations.

---

### System Design Questions

#### 6. Design a scalable real-time chat application.
- **Detailed Answer**:
  - **Connection Protocol**: Use **WebSockets** for persistent, bidirectional communication.
  - **Connection Management**: Spawns a cluster of WebSocket servers. A Load Balancer distributes connections using sticky sessions or consistent hashing.
  - **Session Tracking**: Store active user connections and server IDs in Redis.
  - **Message Delivery**: When User A sends a message to User B:
    1. Query Redis to find which server User B is connected to.
    2. Publish the message to a **Redis Pub/Sub channel** matching User B's server ID.
    3. User B's server receives the event and pushes the message to User B over their active WebSocket connection.
  - **Data Archiving**: Write messages to a distributed database (like Cassandra) asynchronously using a message queue.
- **Follow-up Questions**: How do you store messages offline if a user is disconnected? (Answer: Save messages to the database marked as unread. When the user reconnects, fetch unread messages during initialization).
- **Interviewer's Expectations**: Propose WebSockets, Redis Pub/Sub routing, and database archiving.

---

### Real Interview Questions

#### 7. What is the difference between Latency and Throughput?
- **Detailed Answer**:
  - **Latency**: The time taken to process a single request (measured in milliseconds).
  - **Throughput**: The number of requests a system can handle per second.
  - **Implication**: A system can have low latency but poor throughput if it can only process one request at a time. Conversely, a parallel processing pipeline can have high throughput but high latency per request. The goal is to balance both based on application requirements.
- **Follow-up Questions**: How does adding a message queue impact latency and throughput? (Answer: It increases latency because tasks are queued, but increases throughput by allowing workers to process tasks in parallel).
- **Interviewer's Expectations**: Define both metrics and explain their relationship in distributed systems.

---

## 10. Common Mistakes

- **Jumping to Microservices Prematurely**: Proposing a complex microservices architecture for simple systems with low scale. Start with a clean monolith design and scale out as needed.
- **Violating the CAP Theorem**: Designing distributed systems that claim to guarantee both strong consistency and 100% availability during network partitions.
- **Neglecting Database Indices**: Assuming slow query performance requires database sharding when simply adding an index resolves the bottleneck.

---

## 11. Comparison Section: Database and Communication Models

| Feature / Protocol | SQL (Relational) | NoSQL (Non-Relational) | REST (HTTP/JSON) | gRPC (Protocol Buffers) |
|---|---|---|---|---|
| **Data Schema** | Strict, structured schemas. | Flexible schemas. | N/A | N/A |
| **Scaling Model** | Vertical (Horizontal via replication). | Horizontal sharding by default. | N/A | N/A |
| **Transaction Model** | ACID compliance. | Eventual consistency. | N/A | N/A |
| **Network Latency** | N/A | N/A | Medium (text serialization). | Low (binary serialization). |
| **Best Use Case** | Financial ledger transactions. | User catalogs and dynamic data. | Standard public APIs. | High-performance microservices. |

---

## 12. Practical Project Ideas

### Beginner
- **In-Memory Cache with TTL**: Write an in-memory cache class in Python that stores key-value pairs with a Time-To-Live (TTL) expiration, clean expired keys periodically.

### Intermediate
- **Rate-Limiting Middleware**: Build an Express API server with a custom rate-limiting middleware that uses Redis to track request counts.

### Advanced/Resume-worthy
- **Distributed Key-Value Store**: Build a lightweight distributed key-value database. Implement a consistent hashing ring to distribute keys across multiple local server nodes, handling node joins and failures dynamically.

---

## 13. Internship Preparation Notes

- **Recruiters Focus on**: Core concepts of scaling, simple load balancing, and basic database choices.
- **Product Companies Expect**: High proficiency in system design patterns, requirement clarification, estimations, CAP theorem, consistent hashing, caching, and sharding.
- **System Sizing**: Practice calculating storage and bandwidth requirements for large systems.

---

## 14. Cheat Sheet

- **Token Bucket algorithm**: Best for handling bursts of traffic.
- **Leaky Bucket algorithm**: Best for enforcing a constant processing rate.
- **Database Scaling**: Caching $\to$ Read Replicas $\to$ Partitioning $\to$ Sharding.
- **CAP Theorem options**: Under a network partition, choose either CP (Consistency) or AP (Availability).

---

## 15. One-Day Revision Guide

- [ ] Explain the difference between vertical scaling and horizontal scaling.
- [ ] List the three properties of the CAP Theorem and explain the AP/CP trade-off.
- [ ] Describe how consistent hashing assigns keys on a virtual ring.
- [ ] Design a simple URL shortener service from memory.
- [ ] Understand why load balancers run SSL termination.
