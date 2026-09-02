# GATE 2027 Study Chapter: Database Management Systems & Computer Networks

> **Coverage:** CS Sections 9 & 10 + DA Section 5 (Data Warehousing)
> **Weightage (GATE CS):** DBMS ~10-12 marks, Networks ~10-12 marks | **DA:** Data Warehousing ~4-6 marks
> **Last Updated:** 2026-09-01

---

## 1. Introduction

Database Management Systems and Computer Networks form the backbone of modern computing infrastructure. In GATE, these two subjects together contribute **20-25 marks** to the Computer Science paper, making them among the highest-yield topics.

**Why these subjects matter:**
- **DBMS:** Data persistence, integrity, and efficient retrieval are foundational to every application. GATE tests both theoretical foundations (normalization, relational algebra) and practical SQL skills.
- **Networks:** Understanding the TCP/IP stack, routing algorithms, and protocol mechanisms is essential for distributed systems and system design questions.
- **Data Warehousing (DA):** With the rise of data engineering roles, concepts like OLAP, star schema, and ETL have become increasingly relevant.

**GATE Trends (2019-2026):**
- DBMS: Normalization and indexing questions dominate; transaction concurrency control appears almost every year.
- Networks: TCP congestion control, subnetting/CIDR, and routing algorithms are recurring favorites.
- DA: Conceptual questions on star/snowflake schema and OLAP operations are common.

**Interviewer Relevance:** System design interviews at FAANG companies frequently test database sharding, CAP theorem, and network protocol understanding. Mastering these concepts serves double duty.

---

## 2. Core Concepts

### 2.1 Beginner Level

**DBMS Fundamentals:**
- A **Database** is an organized collection of interrelated data; a **DBMS** is the software that manages it.
- **Data abstraction levels:** Physical (how stored) → Logical (tables/relations) → View (user perspective).
- **Schema** (intension) vs. **Instance** (extension): Schema is the structure; instance is the actual data at a point in time.
- **Data Independence:** Logical (changes in schema don't affect views) and Physical (changes in storage don't affect logical schema).
- **Key types:** Superkey, Candidate key, Primary key, Foreign key, Alternate key.
- **ER Model constructs:** Entity (strong/weak), Relationship (1:1, 1:N, M:N), Attribute (simple/composite, single/multi-valued, derived).

**Networks Fundamentals:**
- **OSI Model:** 7 layers (Physical → Data Link → Network → Transport → Session → Presentation → Application).
- **TCP/IP Model:** 5 layers (Physical → Data Link → Network → Transport → Application).
- **Circuit Switching:** Dedicated path; used in telephone networks; bandwidth guaranteed.
- **Packet Switching:** Store-and-forward; packets routed independently; statistical multiplexing.
- **Virtual Circuit:** Logical path established; packets follow same route; connection-oriented packet switching.
- **Performance metrics:** Bandwidth, Latency (propagation + transmission + queuing + processing), Throughput, Bandwidth-Delay Product (BDP).

### 2.2 Intermediate Level

**DBMS Intermediate:**
- **Relational Algebra:** Selection ($\sigma$), Projection ($\pi$), Union ($\cup$), Set Difference ($-$), Cartesian Product ($\times$), Rename ($\rho$).
- **Join variants:** Theta join, Equi-join, Natural join, Left/Right/Full Outer join, Semi join, Anti join.
- **Division:** $r \div s$ finds all tuples in $r$ that combine with every tuple in $s$.
- **Tuple Calculus:** $\{t \mid P(t)\}$ — declarative query language; domain vs. tuple calculus.
- **SQL:** DDL (CREATE, ALTER, DROP), DML (SELECT, INSERT, UPDATE, DELETE), DCL (GRANT, REVOKE), TCL (COMMIT, ROLLBACK, SAVEPOINT).
- **Integrity Constraints:** Entity (NOT NULL, UNIQUE), Referential (FOREIGN KEY), Domain (CHECK), Assertions.
- **Functional Dependencies (FDs):** $X \rightarrow Y$ means $X$ determines $Y$; trivial vs. non-trivial FDs.
- **Normalization:** 1NF (atomic values), 2NF (no partial dependency), 3NF (no transitive dependency), BCNF (every determinant is a candidate key), 4NF (no multi-valued dependency), 5NF (no join dependency).
- **File Organization:** Heap (unordered), Sorted (ordered by key), Hashed (hash function maps to bucket).
- **Indexing:** Dense (index entry per record) vs. Sparse (index entry per block); Primary, Clustering, Secondary.
- **B+ Tree properties:** All data in leaves; leaves linked; balanced; order $p$ means max $p$ pointers, min $\lceil p/2 \rceil$ pointers (except root).

**Networks Intermediate:**
- **Error Detection:** Parity (single/double), Checksum, CRC (polynomial division), Hamming Code (error correction).
- **MAC Protocols:** ALOHA (pure/slotted), CSMA (1-persistent, non-persistent, p-persistent), CSMA/CD (collision detection), CSMA/CA (collision avoidance), Token Passing.
- **Ethernet:** IEEE 802.3; Manchester encoding; frame format (preamble, SFD, DA, SA, length/type, data, FCS); minimum frame size 64 bytes.
- **Routing:** Distance Vector (Bellman-Ford, RIP — hop count, split horizon, poison reverse), Link State (Dijkstra, OSPF — flooding, LSA, LSDB).
- **IPv4 Header:** 20 bytes fixed; fields: Version, IHL, TOS, Total Length, Identification, Flags (DF, MF), Fragment Offset, TTL, Protocol, Header Checksum, Source/Dest IP.
- **Fragmentation:** Offset in units of 8 bytes; MF=1 means more fragments; DF=1 means don't fragment.
- **CIDR:** Classless addressing; notation a.b.c.d/n; subnet mask; VLSM.
- **NAT:** Translates private IP to public IP; types (static, dynamic, PAT/NAT overload).
- **TCP:** Connection-oriented; 3-way handshake (SYN, SYN-ACK, ACK); 4-way termination (FIN, ACK).
- **TCP Flow Control:** Sliding window; receiver advertises window size; zero window probe.
- **TCP Congestion Control:** Slow start (exponential growth), AIMD (additive increase, multiplicative decrease), Fast retransmit, Fast recovery.

### 2.3 Advanced Level

**DBMS Advanced:**
- **Armstrong's Axioms:** Reflexivity (if $Y \subseteq X$, then $X \rightarrow Y$), Augmentation (if $X \rightarrow Y$, then $XZ \rightarrow YZ$), Transitivity (if $X \rightarrow Y$ and $Y \rightarrow Z$, then $X \rightarrow Z$).
- **Derived rules:** Union, Decomposition, Pseudotransitivity.
- **Closure of FDs ($F^+$):** All FDs logically implied by $F$.
- **Attribute closure ($X^+$):** Set of attributes functionally determined by $X$ under $F$.
- **Canonical cover:** Minimal set of FDs equivalent to $F$; no extraneous attributes, no redundant FDs.
- **BCNF Decomposition:** If $X \rightarrow Y$ violates BCNF, decompose into $R_1 = XY$ and $R_2 = R - Y + X$.
- **Lossless Join:** Decomposition is lossless if $R_1 \cap R_2 \rightarrow R_1$ or $R_1 \cap R_2 \rightarrow R_2$.
- **Dependency Preserving:** $\cup F_i^+ = F^+$; not always achievable with BCNF.
- **4NF:** For every non-trivial MVD $X \twoheadrightarrow Y$, $X$ must be a superkey.
- **Transaction ACID:** Atomicity, Consistency, Isolation, Durability.
- **Serializability:** Conflict (swap non-conflicting operations) vs. View (same reads-from, same final write).
- **2PL:** Growing phase (acquire locks) → Shrinking phase (release locks); ensures conflict serializability.
- **Strict 2PL:** Hold all locks until commit/abort; prevents cascading rollbacks.
- **Timestamp Ordering:** W-timestamp(Q), R-timestamp(Q); Thomas' Write Rule.
- **MVCC:** Multi-version concurrency control; readers don't block writers.
- **Deadlock:** Wait-for graph; detection vs. prevention (wait-die, wound-wait).
- **Recovery:** WAL (Write-Ahead Logging), ARIES (Analysis, Redo, Undo), LSN, checkpoint.

**Networks Advanced:**
- **Switching performance:** Throughput = $\frac{\text{Packets}}{\text{Time}}$; latency components.
- **CRC computation:** Generator polynomial $G(x)$; remainder $R(x) = \frac{M(x) \cdot x^k}{G(x)}$; transmitted $T(x) = M(x) \cdot x^k \oplus R(x)$.
- **Hamming distance:** Minimum bits to change to go from one codeword to another; $d_{min} \geq e+1$ to detect $e$ errors; $d_{min} \geq 2e+1$ to correct $e$ errors.
- **Ethernet throughput:** Efficiency = $\frac{T_{prop}}{T_{trans} + 2T_{prop}}$ for CSMA/CD.
- **Routing convergence:** Count-to-infinity problem in DV; triggered updates, hold-down timers.
- **OSPF areas:** Backbone area (0), ABR, ASBR; LSA types (1-7).
- **IPv4 fragmentation math:** If packet size = $L$, MTU = $M$, header = 20: data per fragment = $\lfloor \frac{M-20}{8} \rfloor \times 8$; number of fragments = $\lceil \frac{L-20}{\text{data per fragment}} \rceil$.
- **TCP RTT estimation:** $EstimatedRTT = (1-\alpha) \cdot EstimatedRTT + \alpha \cdot SampleRTT$; $DevRTT = (1-\beta) \cdot DevRTT + \beta \cdot |SampleRTT - EstimatedRTT|$; $Timeout = EstimatedRTT + 4 \cdot DevRTT$.
- **TCP congestion window:** Slow start threshold ($ssthresh$); $cwnd$ grows exponentially until $ssthresh$, then linearly.
- **DNS hierarchy:** Root → TLD → Authoritative; iterative vs. recursive queries; record types (A, AAAA, MX, CNAME, NS, PTR, SOA).
- **HTTP/1.1 vs HTTP/2:** Persistent connections, pipelining, multiplexing, header compression (HPACK), server push.

---

## 3. Internal Working

### 3.1 DBMS Query Processing Pipeline

```
SQL Query
    ↓
Parser → Parse Tree
    ↓
Semantic Checker (catalog lookup)
    ↓
Query Optimizer (relational algebra reordering, cost estimation)
    ↓
Execution Plan (access paths: index scan, table scan, join algorithms)
    ↓
Executor (iterator model: open, next, close)
    ↓
Buffer Manager (page replacement: LRU, clock)
    ↓
Disk I/O
```

**Join Algorithms:**
- **Nested Loop:** $O(|R| \cdot |S|)$; simple, works for any join condition.
- **Block Nested Loop:** $O(\frac{|R| \cdot |S|}{M-2})$ where $M$ = buffer pages; reduces I/O.
- **Index Nested Loop:** $O(|R| \cdot \log|S|)$ if index on $S$; best when one relation is small.
- **Sort-Merge:** $O(|R|\log|R| + |S|\log|S| + |R| + |S|)$; good for sorted output.
- **Hash Join:** $O(|R| + |S|)$ average; build phase + probe phase; grace hash for large relations.

### 3.2 B+ Tree Operations

**Search:** Start at root; at each internal node, find smallest key $k_i > x$, follow pointer $P_{i-1}$; continue until leaf.

**Insert:**
1. Find leaf $L$ where key belongs.
2. If $L$ has space, insert in sorted order.
3. If $L$ is full (has $p$ keys), split into $L$ and $L'$:
   - First $\lceil p/2 \rceil$ keys stay in $L$.
   - Remaining keys go to $L'$.
   - Copy up middle key to parent.
   - If parent is full, split recursively (may reach root → new root, tree grows).

**Delete:**
1. Find and remove key from leaf.
2. If leaf has $\geq \lceil p/2 \rceil$ keys, done.
3. Else try to redistribute from sibling.
4. If redistribution impossible, merge with sibling; delete separator key from parent (may cascade).

### 3.3 Transaction State Machine

```
Active
  ↓ (first statement)
Partially Committed
  ↓ (statement succeeds)
Committed ← (COMMIT)
  ↓
Failed ← (statement fails)
  ↓
Aborted ← (ROLLBACK)
  ↓
Terminated
```

### 3.4 TCP State Machine

```
Client: CLOSED → SYN_SENT → ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
Server: CLOSED → LISTEN → SYN_RCVD → ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED
```

**3-Way Handshake:**
1. Client → Server: SYN=1, seq=x
2. Server → Client: SYN=1, ACK=1, seq=y, ack=x+1
3. Client → Server: ACK=1, seq=x+1, ack=y+1

**4-Way Termination:**
1. Active closer → FIN
2. Passive closer → ACK
3. Passive closer → FIN
4. Active closer → ACK (waits 2MSL)

### 3.5 Routing Algorithm Internals

**Bellman-Ford (Distance Vector):**
```
Initialize: D(x) = 0, D(v) = ∞ for all v ≠ x
Repeat |V|-1 times:
    For each edge (u,v):
        D(v) = min(D(v), D(u) + c(u,v))
Check for negative cycles: if any D(v) can be reduced, negative cycle exists
```

**Dijkstra (Link State):**
```
Initialize: S = ∅, d[s] = 0, d[v] = ∞ for v ≠ s
While S ≠ V:
    u = vertex in V\S with minimum d[u]
    S = S ∪ {u}
    For each neighbor v of u:
        d[v] = min(d[v], d[u] + w(u,v))
```

---

## 4. Important Terminology

| Term | Definition | Context |
|------|-----------|---------|
| **Superkey** | Set of attributes that uniquely identifies a tuple | DBMS |
| **Candidate Key** | Minimal superkey | DBMS |
| **Primary Key** | Chosen candidate key for identification | DBMS |
| **Foreign Key** | Attribute referencing primary key of another relation | DBMS |
| **Functional Dependency** | $X \rightarrow Y$: X determines Y | DBMS |
| **Closure ($F^+$)** | All FDs logically implied by F | DBMS |
| **Canonical Cover** | Minimal equivalent set of FDs | DBMS |
| **BCNF** | Every determinant is a candidate key | DBMS |
| **MVD** | Multi-valued dependency $X \twoheadrightarrow Y$ | DBMS |
| **Conflict Serializability** | Schedule equivalent to serial via non-conflicting swaps | DBMS |
| **2PL** | Growing then shrinking lock phases | DBMS |
| **WAL** | Write-Ahead Logging: log before data | DBMS |
| **MTU** | Maximum Transmission Unit (1500 bytes for Ethernet) | Networks |
| **BDP** | Bandwidth-Delay Product = bandwidth × RTT | Networks |
| **CRC** | Cyclic Redundancy Check | Networks |
| **CSMA/CD** | Carrier Sense Multiple Access with Collision Detection | Networks |
| **CIDR** | Classless Inter-Domain Routing | Networks |
| **NAT** | Network Address Translation | Networks |
| **MSS** | Maximum Segment Size | Networks |
| **RTO** | Retransmission Timeout | Networks |
| **LSA** | Link State Advertisement | Networks |
| **Star Schema** | Fact table surrounded by dimension tables | DA |
| **OLAP** | Online Analytical Processing | DA |
| **ETL** | Extract, Transform, Load | DA |

---

## 5. Beginner Examples

### Example 1: ER to Relational Mapping
**Q:** Convert an ER diagram with entities Student (sid, name) and Course (cid, title), and M:N relationship Enroll (grade) to relational schema.

**A:**
```
Student(sid PK, name)
Course(cid PK, title)
Enroll(sid FK→Student, cid FK→Course, grade)
```
The M:N relationship becomes a separate table with composite primary key (sid, cid).

### Example 2: Basic Relational Algebra
**Q:** Given Employee(eid, name, dept, salary), find names of employees in 'Sales' department.

**A:**
$$\pi_{name}(\sigma_{dept='Sales'}(Employee))$$

### Example 3: IPv4 Subnetting
**Q:** How many hosts can be addressed in subnet 192.168.1.0/26?

**A:** /26 means 26 network bits, 6 host bits. Hosts = $2^6 - 2 = 62$ (subtract network and broadcast addresses).

### Example 4: SQL Query
**Q:** Write SQL to find the second highest salary from Employee table.

**A:**
```sql
SELECT MAX(salary) FROM Employee
WHERE salary < (SELECT MAX(salary) FROM Employee);
```
Or using `LIMIT/OFFSET`:
```sql
SELECT DISTINCT salary FROM Employee
ORDER BY salary DESC LIMIT 1 OFFSET 1;
```

### Example 5: Normalization Check
**Q:** Is R(A,B,C) with FDs {A→B, B→C} in 3NF?

**A:** Candidate key is A. B→C is a transitive dependency (A→B, B→C, so A→C transitively). Since B is not a superkey and C is not prime, this violates 3NF. **Not in 3NF.**

---

## 6. Intermediate Examples

### Example 6: Natural Join vs Theta Join
**Q:** Given R(A,B) = {(1,2), (3,4)} and S(B,C) = {(2,5), (4,6)}, compute $R \bowtie S$ and $R \bowtie_{R.A > S.C} S$.

**A:**
- **Natural Join** (on B): {(1,2,5), (3,4,6)}
- **Theta Join** (R.A > S.C): Empty (no pairs satisfy A > C)

### Example 7: BCNF Decomposition
**Q:** Decompose R(A,B,C,D) with FDs {A→B, B→C} into BCNF. Is it dependency preserving?

**A:**
- Candidate key: AD
- A→B violates BCNF (A is not superkey)
- Decompose: R1(A,B), R2(A,C,D)
- In R2, B→C is lost (B not in R2). Check A→C: A→B and B→C implies A→C, but B→C itself is lost.
- **Not dependency preserving.**

### Example 8: TCP Sequence Numbers
**Q:** TCP sender has ISN=1000, sends segments of 100 bytes each. What are sequence numbers for first 3 segments? If ACK 1300 received, what does it mean?

**A:**
- Segment 1: seq=1000, bytes 1000-1099
- Segment 2: seq=1100, bytes 1100-1199
- Segment 3: seq=1200, bytes 1200-1299
- ACK 1300 means all bytes up to 1299 received; next expected byte is 1300.

### Example 9: Fragmentation Calculation
**Q:** A 4000-byte IP datagram (20-byte header) must traverse a link with MTU=1500. Calculate fragments.

**A:**
- Data per fragment: MTU - header = 1500 - 20 = 1480 bytes
- Offset must be multiple of 8: $\lfloor 1480/8 \rfloor \times 8 = 1480$ (already divisible)
- Total data: 4000 - 20 = 3980 bytes
- Fragments: $\lceil 3980/1480 \rceil = 3$ fragments
- Fragment 1: offset=0, data=1480, total=1500, MF=1
- Fragment 2: offset=185 (1480/8), data=1480, total=1500, MF=1
- Fragment 3: offset=370, data=1020, total=1040, MF=0

### Example 10: Conflict Serializability
**Q:** Check if schedule S: r1(A), w2(A), r2(B), w1(B), r3(C), w3(C) is conflict serializable.

**A:**
- Precedence graph: T1→T2 (r1(A) before w2(A)), T2→T1 (r2(B) before w1(B))
- Cycle exists: T1 → T2 → T1
- **Not conflict serializable.**

---

## 7. Advanced Examples

### Example 11: Armstrong's Axioms Proof
**Q:** Prove that if $X \rightarrow Y$ and $WY \rightarrow Z$, then $WX \rightarrow Z$ (Pseudotransitivity).

**A:**
1. $X \rightarrow Y$ (given)
2. $WXY \rightarrow WY$ (augmentation with W)
3. $WY \rightarrow Z$ (given)
4. $WXY \rightarrow Z$ (transitivity on 2,3)
5. $WX \rightarrow WXY$ (reflexivity, since $WX \subseteq WXY$)
6. $WX \rightarrow Z$ (transitivity on 5,4) ∎

### Example 12: 4NF Decomposition
**Q:** R(A,B,C) with MVD $A \twoheadrightarrow B$. Is it in 4NF? Decompose if needed.

**A:**
- A is not necessarily a superkey (depends on FDs). If no FDs, candidate key is ABC.
- $A \twoheadrightarrow B$ is non-trivial MVD, A is not superkey → violates 4NF.
- Decompose: R1(A,B), R2(A,C)
- Both in 4NF (no non-trivial MVDs that violate).

### Example 13: TCP Congestion Window Trace
**Q:** TCP connection starts with cwnd=1 MSS, ssthresh=8 MSS. Trace cwnd for RTTs 1-10 assuming no loss.

**A:**
| RTT | cwnd | Phase |
|-----|------|-------|
| 1 | 1 | Slow Start |
| 2 | 2 | Slow Start |
| 3 | 4 | Slow Start |
| 4 | 8 | Slow Start (reaches ssthresh) |
| 5 | 9 | Congestion Avoidance |
| 6 | 10 | Congestion Avoidance |
| 7 | 11 | Congestion Avoidance |
| 8 | 12 | Congestion Avoidance |
| 9 | 13 | Congestion Avoidance |
| 10 | 14 | Congestion Avoidance |

### Example 14: B+ Tree Insertion
**Q:** Insert 25 into B+ tree of order 3 (max 3 pointers, max 2 keys per node) with leaves: [10,20] → [30,40] → [50,60].

**A:**
- Find leaf [30,40]: 25 < 30, go to leaf [10,20]
- Insert 25: leaf becomes [10,20,25] — overflow!
- Split: [10,20] and [25]; copy up 25 to parent
- Parent becomes [25,30] (was [30])
- Leaves: [10,20] → [25] → [30,40] → [50,60]

### Example 15: View Serializability vs Conflict Serializability
**Q:** Schedule S: r1(A), r2(A), w1(A), w2(A). Is it view serializable? Conflict serializable?

**A:**
- **Conflict serializable?** No — r1(A) and w2(A) conflict, r2(A) and w1(A) conflict; cycle in precedence graph.
- **View serializable?** Check view equivalence to T1;T2 or T2;T1:
  - View of S: T1 reads initial A, T2 reads initial A, final write by T2
  - T1;T2: T1 reads initial, T2 reads T1's write, final by T2 — different reads-from
  - T2;T1: T2 reads initial, T1 reads T2's write, final by T1 — different final write
  - **Not view serializable either.**

---

## 8. How Interviewers Think

### DBMS Interview Patterns:

**Pattern 1: "Design a database for X"**
- Start with requirements → ER diagram → relational schema → normalization check
- Discuss indexing strategy (which columns, B+ tree vs hash)
- Consider sharding/partitioning for scale
- Mention CAP theorem trade-offs

**Pattern 2: "Why is normalization important?"**
- Reduces redundancy, prevents update anomalies
- But: over-normalization hurts performance (more joins)
- Denormalization for read-heavy workloads

**Pattern 3: "How does a transaction ensure ACID?"**
- Atomicity: undo logging
- Consistency: constraints + application logic
- Isolation: locking or MVCC
- Durability: WAL + force-write at commit

### Networks Interview Patterns:

**Pattern 1: "What happens when you type a URL?"**
- DNS resolution → TCP handshake → HTTP request → server processing → response
- Include: ARP for gateway, TLS handshake for HTTPS, load balancers

**Pattern 2: "Why does TCP have 3-way handshake?"**
- Prevent old duplicate connections from causing confusion
- Both sides agree on initial sequence numbers
- 2-way is insufficient: server doesn't know client received its SYN-ACK

**Pattern 3: "How does Netflix stream video?"**
- CDN for edge caching
- TCP for reliable delivery (not UDP for video-on-demand)
- Adaptive bitrate streaming (DASH/HLS)
- Congestion control adapts to available bandwidth

### DA Interview Patterns:

**Pattern 1: "Star vs Snowflake schema"**
- Star: denormalized dimensions, simpler queries, more storage
- Snowflake: normalized dimensions, less redundancy, more joins
- Choice depends on query patterns and storage constraints

**Pattern 2: "OLAP vs OLTP"**
- OLTP: many short transactions, normalized, current data
- OLAP: complex queries, aggregated, historical data, denormalized

---

## 9. FAQs

### Conceptual FAQs

**Q1: What is the difference between 3NF and BCNF?**
A: 3NF allows $X \rightarrow Y$ if $X$ is a superkey OR $Y$ is a prime attribute. BCNF requires $X$ to be a superkey always. Every BCNF is 3NF, but not vice versa. BCNF may not be dependency preserving.

**Q2: Why is B+ tree preferred over B-tree for databases?**
A: In B+ trees, all data pointers are in leaves, and leaves are linked. This gives: (1) better cache performance for range queries, (2) all searches take same time (balanced), (3) internal nodes have more keys → shorter tree.

**Q3: What is the difference between TCP and UDP?**
A: TCP is connection-oriented, reliable, flow/congestion controlled, ordered delivery. UDP is connectionless, unreliable, no flow control, lower overhead. Use TCP for file transfer, web; UDP for streaming, DNS, gaming.

**Q4: Why does distance vector routing have count-to-infinity problem?**
A: When a link fails, routers slowly increase distance to infinity because they rely on each other's possibly outdated information. Solutions: split horizon, poison reverse, hold-down timers.

**Q5: What is the difference between conflict and view serializability?**
A: Conflict serializability requires equivalence via swapping non-conflicting operations. View serializability requires same reads-from relationships and same final write. All conflict serializable schedules are view serializable, but not vice versa.

### Scenario-Based FAQs

**Q6: A query is slow. How do you optimize it?**
A: (1) Check execution plan for full table scans, (2) Add appropriate indexes, (3) Rewrite subqueries as joins, (4) Consider denormalization, (5) Update statistics, (6) Partition large tables.

**Q7: Two transactions deadlock. How does DBMS handle it?**
A: DBMS detects deadlock via wait-for graph cycle detection. It chooses a victim (youngest, least work, etc.), rolls it back, and releases its locks. The other transaction proceeds.

**Q8: A TCP connection has high latency but low bandwidth utilization. Why?**
A: Likely due to small congestion window (slow start phase), receiver window limitation, or Nagle's algorithm buffering. Check cwnd, rwnd, and RTT.

**Q9: How do you design a data warehouse for an e-commerce company?**
A: Star schema with fact table (sales transactions) and dimensions (product, customer, time, store). Use surrogate keys, slowly changing dimensions (Type 1/2/3), aggregate tables for common queries.

**Q10: Why does HTTP/2 use multiplexing instead of HTTP/1.1 pipelining?**
A: HTTP/1.1 pipelining suffers from head-of-line blocking at the application layer. HTTP/2 multiplexes streams over a single TCP connection, allowing interleaved responses without blocking.

### Debugging FAQs

**Q11: SQL query returns duplicate rows. Why?**
A: Missing JOIN condition (Cartesian product), or GROUP BY missing columns, or UNION ALL instead of UNION. Check for many-to-many relationships without proper join.

**Q12: B+ tree search is slow despite index. Why?**
A: Index may not be used due to: function on indexed column (`WHERE UPPER(name)='ABC'`), implicit type conversion, low selectivity, or outdated statistics causing optimizer to choose table scan.

**Q13: TCP connection stuck in TIME_WAIT. Why?**
A: Normal behavior — TIME_WAIT lasts 2MSL to handle delayed segments. If too many connections in TIME_WAIT, reduce with `tcp_tw_reuse` (Linux) or increase ephemeral port range.

**Q14: Routing loop in OSPF. Possible causes?**
A: Misconfigured areas, inconsistent LSDB, duplicate router IDs, or area border router misconfiguration. Check `show ip ospf database` for inconsistencies.

### System Design FAQs

**Q15: How to design a URL shortener?**
A: Hash function (MD5/SHA) → base62 encoding → store in key-value DB (Redis for cache, Cassandra for persistence). Handle collisions, use consistent hashing for sharding.

**Q16: How to implement a distributed cache?**
A: Consistent hashing for key distribution, replication for fault tolerance, LRU eviction, cache-aside or write-through policy. Handle cache invalidation carefully.

**Q17: Design a chat application like WhatsApp?**
A: WebSocket for real-time messaging, message queue for offline delivery, end-to-end encryption (Signal protocol), media storage in object store (S3), presence via heartbeat.

### Advanced FAQs

**Q18: What is the CAP theorem?**
A: A distributed system can satisfy at most two of: Consistency (all nodes see same data), Availability (every request gets response), Partition tolerance (system works despite network partitions). In practice, partition tolerance is mandatory, so choose CP or AP.

**Q19: How does ARIES handle recovery?**
A: Three phases: (1) Analysis — determine dirty pages and active transactions at crash, (2) Redo — repeat history by reapplying updates from log, (3) Undo — rollback incomplete transactions using undo log records.

**Q20: What is the difference between strict 2PL and rigorous 2PL?**
A: Strict 2PL holds exclusive locks until commit/abort (shared locks can be released earlier). Rigorous 2PL holds ALL locks until commit/abort. Rigorous 2PL simplifies recovery.

---

## 10. Common Mistakes

### DBMS Mistakes:

1. **Confusing 2NF with 3NF:** 2NF is about partial dependencies (non-prime attribute dependent on part of candidate key). 3NF is about transitive dependencies.

2. **Assuming BCNF is always achievable with dependency preservation:** BCNF decomposition may lose FDs. Sometimes 3NF (which is always dependency preserving) is preferred.

3. **Forgetting that natural join eliminates duplicate columns:** Natural join on attribute A produces single A column, not two.

4. **Misunderstanding B+ tree order:** Order $p$ = max pointers, not max keys. Max keys = $p-1$.

5. **Confusing conflict serializability with view serializability:** All conflict serializable schedules are view serializable, but not conversely.

6. **Ignoring the difference between dense and sparse index:** Dense has entry for every record; sparse has entry for every block.

7. **Wrong fragmentation calculation:** Offset is in units of 8 bytes, not bytes. Data per fragment must be multiple of 8.

### Networks Mistakes:

1. **Confusing propagation delay with transmission delay:** Propagation = distance/speed; Transmission = packet size/bandwidth.

2. **Forgetting to subtract header for fragmentation:** Data per fragment = MTU - header size.

3. **Mixing up CSMA/CD and CSMA/CA:** CD for wired (Ethernet), CA for wireless (WiFi).

4. **Incorrect subnet calculation:** Remember to subtract 2 for network and broadcast addresses (unless /31 or /32).

5. **Confusing TCP flags:** SYN for connection establishment, FIN for termination, RST for abort.

6. **Misunderstanding NAT:** NAT modifies IP addresses, not ports (unless PAT). PAT modifies both.

7. **Wrong RTT estimation formula:** Timeout = EstimatedRTT + 4×DevRTT, not just EstimatedRTT.

### DA Mistakes:

1. **Confusing fact and dimension tables:** Fact contains measures (quantitative), dimensions contain descriptors.

2. **Mixing up slice and dice:** Slice = select one dimension (reduce dimensionality). Dice = select range on multiple dimensions (subcube).

3. **Forgetting ETL vs ELT:** ETL transforms before loading; ELT loads raw then transforms (modern cloud approach).

---

## 11. Comparison Tables

### Normal Forms Comparison:

| Normal Form | Condition | Preserves FDs? | Lossless? |
|-------------|-----------|----------------|-----------|
| 1NF | Atomic values, no repeating groups | — | — |
| 2NF | 1NF + no partial dependency | Yes | Yes |
| 3NF | 2NF + no transitive dependency | Yes | Yes |
| BCNF | Every determinant is superkey | Not always | Yes |
| 4NF | BCNF + no non-trivial MVD with non-superkey | Not always | Yes |
| 5NF | 4NF + no join dependency | Not always | Yes |

### Join Types Comparison:

| Join Type | Condition | NULL Padding |
|-----------|-----------|--------------|
| Inner Join | Match on condition | No |
| Left Outer | All left tuples + matches | Right side NULL |
| Right Outer | All right tuples + matches | Left side NULL |
| Full Outer | All tuples from both | Both sides NULL |
| Semi Join | Left tuples with match in right | No |
| Anti Join | Left tuples with NO match in right | No |

### Routing Protocol Comparison:

| Feature | RIP (DV) | OSPF (LS) |
|---------|----------|-----------|
| Algorithm | Bellman-Ford | Dijkstra |
| Metric | Hop count | Cost (bandwidth) |
| Convergence | Slow | Fast |
| Max hops | 15 | Unlimited |
| Updates | Full table periodically | LSA on change |
| Classful/Classless | Classless (RIPv2) | Classless |
| Authentication | Yes (RIPv2) | Yes |

### TCP Congestion Control Algorithms:

| Algorithm | Loss Detection | Window Adjustment |
|-----------|---------------|-------------------|
| Tahoe | Timeout or 3 dup ACK | Reset to 1, slow start |
| Reno | 3 dup ACK | Fast recovery, cwnd/2 |
| NewReno | 3 dup ACK | Handles multiple losses |
| CUBIC | 3 dup ACK | Cubic function growth |
| BBR | Model-based | Based on BDP estimate |

### HTTP Versions Comparison:

| Feature | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---------|----------|----------|--------|--------|
| Connections | One per request | Persistent | Multiplexed | Multiplexed |
| Head-of-line blocking | Yes | Yes (app layer) | No (TCP layer) | No |
| Header compression | No | No | HPACK | QPACK |
| Transport | TCP | TCP | TCP | QUIC (UDP) |
| Server push | No | No | Yes | Yes |

---

## 12. Practical Projects

### Project 1: Mini DBMS Engine
**Scope:** Implement a simple relational database with:
- Parser for subset of SQL (SELECT, INSERT, CREATE TABLE)
- Storage engine with heap file organization
- B+ tree index implementation
- Buffer pool with LRU replacement
- Simple query optimizer (push selections down)

**Skills:** C++/Rust, data structures, file I/O, memory management

### Project 2: TCP-like Reliable Transport Protocol
**Scope:** Build over UDP:
- Connection management (3-way handshake)
- Sliding window flow control
- Sequence numbers and ACKs
- Retransmission timeout (Jacobson's algorithm)
- Simple congestion control (slow start + AIMD)

**Skills:** Python/C, sockets, network programming, state machines

### Project 3: Network Simulator
**Scope:** Simulate network topologies:
- Graph representation of network
- Dijkstra and Bellman-Ford implementations
- Packet routing simulation
- Link failure and convergence visualization
- Performance metrics collection

**Skills:** Python, graph algorithms, visualization (matplotlib)

### Project 4: Data Warehouse ETL Pipeline
**Scope:** Build ETL for e-commerce analytics:
- Extract from OLTP database (PostgreSQL)
- Transform (cleaning, aggregation, surrogate keys)
- Load into star schema (fact_sales, dim_product, dim_customer, dim_time)
- OLAP queries (roll-up, drill-down, slice, dice)
- Dashboard with aggregated metrics

**Skills:** Python, SQL, Apache Airflow, PostgreSQL, BI tools

### Project 5: Distributed Key-Value Store
**Scope:** Implement with:
- Consistent hashing for partitioning
- Replication (configurable factor)
- Quorum reads/writes (R + W > N)
- Gossip protocol for membership
- Simple transactions (read committed)

**Skills:** Go/Rust, distributed systems, consensus basics

---

## 13. Internship Preparation

### Technical Screening Topics:

**Must-Know (High Frequency):**
1. SQL: JOINs, GROUP BY, HAVING, subqueries, window functions
2. Normalization: Identify normal form, decompose to BCNF/3NF
3. B+ trees: Insert, delete, search complexity
4. TCP: 3-way handshake, flow control, congestion control
5. Subnetting: CIDR, subnet mask, number of hosts
6. Routing: Dijkstra, Bellman-Ford, count-to-infinity

**Good to Know (Medium Frequency):**
1. Transaction serializability: Conflict vs view
2. Deadlock: Detection, prevention, avoidance
3. Indexing: Clustered vs non-clustered, composite indexes
4. HTTP: Status codes, methods, cookies vs sessions
5. DNS: Resolution process, record types
6. CRC/Hamming: Error detection/correction

**Advanced (Low Frequency but Impressive):**
1. ARIES recovery algorithm
2. MVCC implementation details
3. OSPF areas and LSA types
4. TCP CUBIC/BBR congestion control
5. Data warehouse modeling (star/snowflake)
6. CAP theorem and its implications

### Behavioral Preparation:

**Common Questions:**
- "Tell me about a time you debugged a difficult issue"
- "How do you prioritize when multiple deadlines approach?"
- "Describe a project where you had to learn new technology quickly"

**STAR Method:** Situation → Task → Action → Result

### System Design Basics for Interns:

1. **Clarify requirements:** Functional vs non-functional
2. **Estimate scale:** QPS, storage, bandwidth
3. **High-level design:** Components, data flow
4. **Deep dive:** Database schema, API design, caching
5. **Identify bottlenecks:** Single points of failure, scaling limits

---

## 14. Cheat Sheet

### DBMS Formulas:

| Concept | Formula/Rule |
|---------|--------------|
| B+ tree max keys | $p-1$ (order $p$) |
| B+ tree min keys (non-root) | $\lceil p/2 \rceil - 1$ |
| B+ tree height | $O(\log_{\lceil p/2 \rceil} n)$ |
| Index levels | $\log_{fanout}(records)$ |
| Join cost (nested loop) | $B_R + B_R \cdot B_S$ |
| Join cost (sort-merge) | $2B_R(1 + \log_M B_R) + 2B_S(1 + \log_M B_S)$ |
| Buffer pages needed | $M \geq \sqrt{B_{outer}}$ for good performance |

### Networks Formulas:

| Concept | Formula |
|---------|---------|
| Bandwidth-Delay Product | $BDP = bandwidth \times RTT$ |
| Throughput (TCP) | $\approx \frac{0.75 \times W}{RTT}$ where $W$ = window |
| Utilization (ALOHA) | $S = Ge^{-2G}$ (max $1/2e \approx 0.184$) |
| Utilization (Slotted ALOHA) | $S = Ge^{-G}$ (max $1/e \approx 0.368$) |
| CRC remainder | $R(x) = remainder(\frac{M(x) \cdot x^k}{G(x)})$ |
| Fragment offset | $\frac{data\_offset}{8}$ |
| Subnet hosts | $2^{(32-n)} - 2$ for /n |
| TCP timeout | $EstimatedRTT + 4 \times DevRTT$ |

### Quick Reference:

**SQL Execution Order:**
```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

**TCP Flags:**
```
SYN=0x02, ACK=0x10, FIN=0x01, RST=0x04, PSH=0x08, URG=0x20
```

**HTTP Status Codes:**
```
200 OK, 201 Created, 301 Moved, 304 Not Modified
400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found
500 Internal Error, 502 Bad Gateway, 503 Service Unavailable
```

**DNS Record Types:**
```
A (IPv4), AAAA (IPv6), MX (mail), CNAME (alias), NS (nameserver), PTR (reverse), SOA (authority)
```

**OSPF LSA Types:**
```
1: Router, 2: Network, 3: Summary, 4: ASBR Summary, 5: External, 7: NSSA External
```

---

## 15. One-Day Revision Checklist

### Morning Session (3 hours) — DBMS

- [ ] **ER Model:** Can draw ER diagram for given scenario; know weak entity representation
- [ ] **Relational Algebra:** Can write expressions for selection, projection, joins, division
- [ ] **SQL:** Can write queries with JOINs, GROUP BY, HAVING, subqueries, window functions
- [ ] **Normalization:** Can identify normal form; decompose to 3NF/BCNF; check lossless/dependency preserving
- [ ] **FDs:** Can compute attribute closure, canonical cover, apply Armstrong's axioms
- [ ] **B+ trees:** Can trace insert/delete; know order vs. height relationship
- [ ] **Transactions:** Can check conflict serializability via precedence graph; know 2PL, strict 2PL
- [ ] **Concurrency:** Understand timestamp ordering, MVCC, deadlock detection/prevention
- [ ] **Recovery:** Know WAL, ARIES phases, checkpointing

### Afternoon Session (3 hours) — Networks

- [ ] **Layering:** Can list OSI/TCP-IP layers; know functions of each
- [ ] **Switching:** Can differentiate circuit/packet/virtual circuit; calculate performance metrics
- [ ] **Data Link:** Can compute CRC; understand CSMA/CD, Ethernet frame format
- [ ] **MAC:** Know ALOHA throughput, CSMA persistence, token passing
- [ ] **Routing:** Can trace Dijkstra and Bellman-Ford; understand count-to-infinity, OSPF areas
- [ ] **IPv4:** Can calculate fragmentation; understand CIDR, subnetting, NAT
- [ ] **TCP:** Can trace 3-way handshake, flow control window, congestion control (slow start, AIMD)
- [ ] **TCP Timing:** Can compute RTT estimate, timeout, throughput
- [ ] **Application Layer:** Know DNS hierarchy/records, HTTP versions, status codes

### Evening Session (2 hours) — Data Warehousing (DA)

- [ ] **DW Concepts:** Can differentiate OLTP vs OLAP
- [ ] **Schemas:** Can design star/snowflake schema; know fact vs dimension tables
- [ ] **OLAP:** Can perform roll-up, drill-down, slice, dice, pivot operations
- [ ] **ETL:** Understand extraction, transformation, loading processes
- [ ] **Concept Hierarchies:** Know how to define and use for drill-down/roll-up

### Quick Fire Review (30 minutes):

**DBMS:**
- B+ tree order $p$ = max pointers, max keys = $p-1$
- 3NF: $X \rightarrow Y$ OK if $X$ superkey OR $Y$ prime
- BCNF: Every determinant must be superkey
- Conflict serializable → View serializable (not vice versa)
- Strict 2PL: Hold X-locks until commit

**Networks:**
- Fragment offset in units of 8 bytes
- Subnet hosts = $2^{(32-n)} - 2$
- TCP timeout = EstimatedRTT + 4 × DevRTT
- ALOHA max throughput: $1/2e$ (pure), $1/e$ (slotted)
- OSPF uses Dijkstra; RIP uses Bellman-Ford

**DA:**
- Star schema: denormalized dimensions
- Snowflake: normalized dimensions
- Slice: reduce dimensions; Dice: select range on multiple dimensions

### Formula Card (Memorize):

| Formula | Context |
|---------|---------|
| $2^h \geq n$ for B+ tree height | DBMS |
| $\lceil \frac{L-20}{8} \rceil$ for fragment count | Networks |
| $cwnd$ doubles each RTT in slow start | Networks |
| $EstimatedRTT = (1-\alpha)E + \alpha S$ | Networks |
| $S = Ge^{-G}$ (slotted ALOHA max) | Networks |
| $MSS = MTU - 40$ (TCP/IP header) | Networks |

### Last-Minute Tips:

1. **Time Management:** DBMS and Networks each have ~10 questions; allocate time accordingly
2. **Numerics:** Practice subnetting, fragmentation, B+ tree, throughput calculations
3. **Theory:** Focus on normalization, serializability, TCP congestion control
4. **Common Traps:**
   - Natural join removes duplicate columns (not keeps)
   - Fragment offset is in 8-byte units
   - BCNF may not preserve FDs
   - TIME_WAIT is 2 × MSL
   - ACK number = next expected byte

### Exam Day Strategy:

1. **First Pass:** Solve all 1-mark questions (conceptual, quick numericals)
2. **Second Pass:** Solve 2-mark questions (calculations, proofs)
3. **Third Pass:** Attempt MSQs (multiple select questions) — no negative marking
4. **Review:** Check numerical answers for common errors (off-by-one, unit confusion)

---

**Good luck with GATE 2027!**