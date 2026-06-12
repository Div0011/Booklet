# 9. SQL & Relational Theory (Databases & Data)

## 1. Introduction

### What it is
**SQL (Structured Query Language)** is a declarative language for managing and querying relational databases. **Relational theory** is the mathematical foundation: tables represent relations, rows are tuples, columns are attributes. Together, they enable organizing vast datasets, querying with complex conditions, and maintaining data integrity through constraints and ACID transactions.

### Why it exists
Created in the 1970s by IBM, SQL standardized database operations across platforms. Relational theory (Codd, 1970) proved that normalized data structures prevent redundancy and anomalies. SQL made databases accessible to non-programmers; you describe *what* data you want, not *how* to fetch it. This abstraction enabled databases to optimize queries, apply indexes, and scale to petabytes.

### Problems it solves
- **Data Organization**: Structured storage preventing chaos (spreadsheets fail at scale).
- **Atomicity**: Transactions ensure all-or-nothing updates (no partial writes on failure).
- **Consistency**: Constraints enforce data validity (no invalid states).
- **Query Flexibility**: Complex questions answered in seconds without scanning entire files.
- **Multi-User Safety**: Locks and isolation prevent race conditions.
- **Backup & Recovery**: Durability guarantees data survives crashes.

### Industry Use Cases
- **OLTP**: E-commerce (transactions, inventory, orders), banking (accounts, transfers), SaaS (user data).
- **OLAP**: Data warehouses (analytics, BI dashboards), financial reporting, historical analysis.
- **Compliance**: Regulatory audit trails (immutable logs), audit trails (who changed what).
- **Social Networks**: User relationships (graphs), messaging (timelines), recommendations.
- **Search**: Full-text indexing (PostgreSQL), geo-spatial queries (PostGIS).

### Analogy
Think of a relational database as a **filing cabinet with superpowers**. Each table is a cabinet drawer. Rows are individual files. Columns are file attributes. Relationships (foreign keys) are cross-references between files. SQL is the **magical query language** that can instantly find all files matching complex criteria without human effort.

---

## 2. Core Concepts

### Beginner Concepts

#### Tables and Rows
A table is a two-dimensional grid. Rows are records; columns are attributes.

```sql
-- users table
id | name    | email            | age
1  | Alice   | alice@test.com   | 30
2  | Bob     | bob@test.com     | 25
3  | Charlie | charlie@test.com | 35
```

#### Primary Keys
Unique identifier for each row. Enforces uniqueness; used for indexing and relationships.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100)
);
```

#### Foreign Keys
Link rows in one table to rows in another. Prevents orphaned records.

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT REFERENCES users(id),
    amount DECIMAL(10, 2)
);
```

#### SELECT, WHERE, ORDER BY
Fundamental query operations.

```sql
SELECT name, email FROM users WHERE age > 25 ORDER BY age DESC;
```

#### JOIN
Combine rows from multiple tables.

```sql
SELECT users.name, orders.amount
FROM users INNER JOIN orders ON users.id = orders.user_id;
```

### Intermediate Concepts

#### Normalization (1NF, 2NF, 3NF)
Decomposing tables to eliminate redundancy.

- **1NF**: Atomic values (no lists in columns).
- **2NF**: No partial dependencies (non-key columns depend on entire primary key).
- **3NF**: No transitive dependencies (non-key columns depend only on primary key).

#### ACID Transactions
- **Atomicity**: All-or-nothing; partial updates never happen.
- **Consistency**: Data satisfies all constraints before and after transaction.
- **Isolation**: Concurrent transactions don't interfere.
- **Durability**: Committed data persists even if system crashes.

#### Indexes
Speed up lookups by organizing data into B-Trees or Hash tables.

```
Without index: O(n) scan
With index: O(log n) lookup
```

#### Aggregation Functions
GROUP BY, COUNT, SUM, AVG, MAX, MIN.

```sql
SELECT department, COUNT(*) as employees, AVG(salary)
FROM employees
GROUP BY department;
```

### Advanced Concepts

#### Window Functions
Apply functions over a sliding "window" of rows without collapsing groups.

```sql
SELECT name, salary,
       RANK() OVER (ORDER BY salary DESC) as rank,
       LAG(salary) OVER (ORDER BY salary DESC) as prev_salary
FROM employees;
```

#### Common Table Expressions (CTEs)
Named temporary result sets for complex queries.

```sql
WITH manager_avg AS (
    SELECT manager_id, AVG(salary) as avg_sal
    FROM employees
    GROUP BY manager_id
)
SELECT e.name, m.avg_sal
FROM employees e
JOIN manager_avg m ON e.manager_id = m.manager_id;
```

#### Query Optimization
Query planner analyzes different execution paths and chooses the fastest.

```
SELECT * FROM orders WHERE user_id = 5 AND status = 'shipped'
→ Index on (user_id, status)
→ Cost: 0.32 (fast)
```

#### Constraints
CHECK, UNIQUE, NOT NULL, FOREIGN KEY.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age >= 18)
);
```

---

## 3. Internal Working

### B-Tree Index Structure
```
                    [50]
                   /    \
              [25]        [75]
             /   \       /    \
         [10][35][60][85]
```

Balanced tree allows O(log n) searches. Leaf nodes contain row pointers.

### Transaction Isolation Levels
```
Level 1: READ UNCOMMITTED (dirty reads allowed)
Level 2: READ COMMITTED (only committed data visible)
Level 3: REPEATABLE READ (consistent snapshot)
Level 4: SERIALIZABLE (completely isolated)
```

### Query Execution Pipeline
```
SQL Query
  ↓ (Parser)
Abstract Syntax Tree
  ↓ (Validator)
Semantic Check
  ↓ (Optimizer)
Execution Plan (cheapest)
  ↓ (Executor)
Row Data
  ↓ (Formatter)
Result Set
```

### Locking Mechanisms
```
Shared Lock (Read): Multiple readers; no writers
Exclusive Lock (Write): Single writer; no readers
Deadlock: Circular lock dependencies (DBMS detects & aborts)
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **ACID** | Atomicity, Consistency, Isolation, Durability |
| **Normalization** | Process of decomposing tables to eliminate redundancy |
| **Denormalization** | Combining normalized tables for performance (read caching) |
| **Primary Key** | Unique identifier for a row; used for indexing |
| **Foreign Key** | Reference to primary key in another table |
| **Join** | Combining rows from multiple tables by matching columns |
| **Index** | Data structure (B-Tree, Hash) for fast lookups |
| **Window Function** | Applies aggregation over a sliding window of rows |
| **CTE** | Common Table Expression; named temporary result set |
| **Aggregation** | Grouping rows and computing statistics (COUNT, SUM, AVG) |
| **Query Plan** | Optimized execution path chosen by query optimizer |
| **Constraint** | Rule enforced on data (CHECK, UNIQUE, NOT NULL, FK) |
| **Transaction** | Atomic unit of work; all-or-nothing execution |
| **Isolation Level** | How much concurrent transactions can interact |
| **Deadlock** | Circular lock dependency; prevents progress |

---

## 5. Beginner Examples

### Example 1: Create Table with Constraints
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age >= 18),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email, age) VALUES ('Alice', 'alice@test.com', 30);
SELECT * FROM users WHERE age > 25 ORDER BY created_at DESC;
```

### Example 2: Simple JOIN
```sql
SELECT users.name, orders.id, orders.amount
FROM users
INNER JOIN orders ON users.id = orders.user_id
WHERE users.age > 25;
```

### Example 3: Aggregation
```sql
SELECT department, AVG(salary) as avg_salary
FROM employees
GROUP BY department
ORDER BY avg_salary DESC;
```

### Example 4: Transaction
```sql
BEGIN TRANSACTION;
UPDATE account SET balance = balance - 50 WHERE id = 101;
UPDATE account SET balance = balance + 50 WHERE id = 102;
COMMIT;
```

### Example 5: Indexing
```sql
CREATE INDEX idx_email ON users(email);
-- Now: SELECT * FROM users WHERE email = 'alice@test.com'
-- Uses index; O(log n) instead of O(n)
```

---

## 6. Intermediate Examples

### Example 1: Complex Multi-Table JOIN
```sql
SELECT 
    u.name,
    COUNT(o.id) as total_orders,
    SUM(o.amount) as total_spent,
    MAX(o.created_at) as last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.age > 20
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 2
ORDER BY total_spent DESC;
```

**Explanation**: 
- LEFT JOIN includes users even with no orders
- GROUP BY aggregates all orders per user
- HAVING filters groups (not individual rows)
- ORDER BY sorts by computed total

### Example 2: Window Functions for Ranking
```sql
WITH ranked_employees AS (
    SELECT 
        name,
        salary,
        RANK() OVER (ORDER BY salary DESC) as salary_rank,
        DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank,
        ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num,
        LAG(salary) OVER (ORDER BY salary DESC) as prev_salary,
        LEAD(salary) OVER (ORDER BY salary DESC) as next_salary
    FROM employees
)
SELECT * FROM ranked_employees WHERE salary_rank <= 10;
```

**Key Functions**:
- RANK(): Skips ranks after ties (1,1,3)
- DENSE_RANK(): Continuous ranks (1,1,2)
- ROW_NUMBER(): Sequential numbers
- LAG/LEAD: Access previous/next row values

### Example 3: Normalization Refactor
**Before (denormalized, redundant)**:
```sql
orders table:
id | user_name | user_email | user_phone | product | qty | price
```

**After (normalized, separate tables)**:
```sql
users: id, name, email, phone
orders: id, user_id, created_at
order_items: id, order_id, product_id, qty
products: id, name, price
```

Benefits: 
- Update user info once (not per order)
- Consistent data
- Smaller storage
- Faster queries on individual entities

### Example 4: Subquery & CTE Pattern
```sql
-- Subquery approach
SELECT u.name, u.order_count
FROM (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
) as user_orders
JOIN users u ON u.id = user_orders.user_id
WHERE order_count > 5;

-- CTE approach (clearer)
WITH user_orders AS (
    SELECT user_id, COUNT(*) as order_count
    FROM orders
    GROUP BY user_id
)
SELECT u.name, uo.order_count
FROM user_orders uo
JOIN users u ON u.id = uo.user_id
WHERE order_count > 5;
```

### Example 5: Transaction with Error Handling
```sql
BEGIN TRANSACTION;
SAVEPOINT sp1;

UPDATE inventory SET qty = qty - 1 WHERE product_id = 101;
IF @@error <> 0 THEN
    ROLLBACK TO SAVEPOINT sp1;
    -- Retry logic
ELSE
    INSERT INTO orders (user_id, product_id, qty) VALUES (5, 101, 1);
    COMMIT;
END IF;
```

---

## 7. Advanced Examples

### Example 1: Recursive CTE (Hierarchical Data)
```sql
-- Find all employees under a manager (organizational tree)
WITH RECURSIVE subordinates AS (
    -- Base case: CEO
    SELECT id, name, manager_id, 1 as depth
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: employees reporting to above
    SELECT e.id, e.name, e.manager_id, s.depth + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.id
    WHERE s.depth < 5
)
SELECT * FROM subordinates ORDER BY depth, id;
```

**Use Case**: Org hierarchies, threaded comments, category trees.

### Example 2: Partitioning Strategy for Scaling
```sql
-- Original table (millions of rows)
CREATE TABLE events (
    id INT PRIMARY KEY,
    user_id INT,
    event_type VARCHAR(50),
    created_at DATE
) PARTITION BY RANGE (YEAR(created_at)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Query on 2024 only scans p2024 partition (10x faster)
SELECT * FROM events WHERE YEAR(created_at) = 2024;
```

### Example 3: Full-Text Search
```sql
-- PostgreSQL
ALTER TABLE documents ADD COLUMN search tsvector;
UPDATE documents SET search = to_tsvector('english', title || ' ' || content);
CREATE INDEX idx_search ON documents USING gin(search);

SELECT title FROM documents 
WHERE search @@ to_tsquery('english', 'machine & learning');

-- MySQL
CREATE FULLTEXT INDEX idx_title_content ON articles(title, content);
SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('python database' IN BOOLEAN MODE);
```

### Example 4: JSON Handling (PostgreSQL)
```sql
CREATE TABLE user_profiles (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    metadata JSONB
);

INSERT INTO user_profiles VALUES (
    1, 'Alice', '{"preferences": {"theme": "dark"}, "tags": ["python", "ml"]}'
);

-- Extract nested data
SELECT metadata->'preferences'->>'theme' FROM user_profiles;

-- Filter by JSON
SELECT * FROM user_profiles WHERE metadata @> '{"preferences": {"theme": "dark"}}';

-- Index for performance
CREATE INDEX idx_metadata ON user_profiles USING gin(metadata);
```

### Example 5: Materialized View for Analytics
```sql
-- Expensive query computed daily
CREATE MATERIALIZED VIEW user_monthly_stats AS
SELECT 
    DATE_TRUNC('month', o.created_at) as month,
    u.country,
    COUNT(DISTINCT u.id) as unique_users,
    SUM(o.amount) as total_revenue,
    AVG(o.amount) as avg_order_value
FROM orders o
JOIN users u ON o.user_id = u.id
GROUP BY DATE_TRUNC('month', o.created_at), u.country;

-- Instant query (pre-computed)
SELECT * FROM user_monthly_stats WHERE month >= '2024-01-01';

-- Refresh periodically
REFRESH MATERIALIZED VIEW user_monthly_stats;
```

---

## 8. How Interviewers Think

### Red Flags (What Interviewers Want to Avoid)
- ❌ **N+1 Queries**: Looping queries instead of single JOIN
  - "I'll fetch users, then loop and fetch orders for each"
  - Better: Single JOIN with aggregation

- ❌ **No Indexes on WHERE Clause**: O(n) scans on large tables
  - Missing `CREATE INDEX` on frequently searched columns

- ❌ **Denormalization Without Reason**: Redundant data causes update anomalies
  - "I'll duplicate user info in orders table to avoid JOINs"
  - Better: Normal form + indexes

- ❌ **No Transaction Handling**: Race conditions in concurrent access
  - "Separate UPDATE statements" instead of ACID transactions

- ❌ **Ignoring Query Plans**: No EXPLAIN analysis or optimization effort

### Green Flags (What Interviewers Want to See)
- ✅ **Schema Design Thinking**: 1NF → 3NF progression
- ✅ **ACID Awareness**: Explains transactions and isolation levels
- ✅ **Index Strategy**: Considers selectivity, cardinality, query patterns
- ✅ **Window Functions**: Uses RANK(), LAG/LEAD, running totals
- ✅ **CTE/Subquery Clarity**: Readable, maintainable queries
- ✅ **Optimization Discussion**: EXPLAIN, index choices, partitioning

### Answer Matrix
**Q: "How would you optimize a slow query?"**
- 🟢 Analyze with EXPLAIN; check indexes on WHERE/JOIN columns; consider materialized views
- 🟡 Add index to WHERE clause
- 🔴 "Try rewriting it" (no methodology)

---

## 9. Frequently Asked Interview Questions

### Beginner Questions

**Q1: What is a primary key and why do we need it?**
A: A primary key uniquely identifies each row. It enforces uniqueness (no duplicates) and enables fast indexing. Foreign keys reference primary keys to maintain relationships. Example: `user_id INT PRIMARY KEY AUTO_INCREMENT` in users table.

**Q2: Explain the difference between INNER JOIN, LEFT JOIN, and FULL JOIN.**
A: 
- INNER JOIN: Only matching rows from both tables
- LEFT JOIN: All rows from left table; matching rows from right
- FULL JOIN: All rows from both tables
```sql
INNER: A ∩ B
LEFT: A ∪ (A ∩ B)
FULL: A ∪ B
```

**Q3: What is normalization and why is it important?**
A: Decomposing tables to eliminate redundancy and anomalies.
- 1NF: Atomic values (no lists)
- 2NF: Non-key columns depend on entire PK
- 3NF: Non-key columns don't depend on other non-key columns
Benefits: Reduces data duplication, prevents update anomalies.

**Q4: How do indexes improve query performance?**
A: Indexes organize data in B-Trees or Hash tables enabling O(log n) lookup instead of O(n) table scan. Trade-off: slower writes (must update index) but much faster reads. Use on frequently searched columns.

**Q5: Explain ACID properties.**
A: 
- Atomicity: All-or-nothing; partial updates never happen
- Consistency: Data satisfies constraints before and after
- Isolation: Concurrent transactions don't interfere
- Durability: Committed data persists even after crashes

**Q6: What is a foreign key constraint?**
A: Links a column in one table to the primary key in another. Prevents orphaned records (invalid references). Example: `user_id INT REFERENCES users(id)` in orders table.

**Q7: How do you handle duplicate rows?**
A: Use DISTINCT or GROUP BY. Example: `SELECT DISTINCT user_id FROM orders;`

**Q8: What is a transaction and when would you use it?**
A: Atomic unit of work. Use for multi-step operations that must all succeed or all fail. Example: Transfer money between accounts (debit + credit).

**Q9: Explain the difference between WHERE and HAVING.**
A: WHERE filters rows before grouping; HAVING filters groups after aggregation.
```sql
WHERE user_id > 5  -- Applied first
GROUP BY user_id
HAVING COUNT(*) > 10  -- Applied to groups
```

**Q10: What is a subquery?**
A: Query inside another query. Useful for filtering based on computed results.
```sql
SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE amount > 100);
```

**Q11: Explain the difference between COUNT(*) and COUNT(column_name).**
A: COUNT(*) counts all rows (including NULLs); COUNT(column) counts non-NULL values.

**Q12: What is database sharding and why might you use it?**
A: Horizontal partitioning across multiple servers. Use for massive datasets that don't fit on one machine. Example: user_id % 10 determines which shard.

**Q13: How do you prevent SQL injection?**
A: Use parameterized queries/prepared statements.
```python
# Bad
query = f"SELECT * FROM users WHERE id = {user_input}"

# Good
query = "SELECT * FROM users WHERE id = ?"
cursor.execute(query, [user_input])
```

**Q14: What is denormalization and when would you use it?**
A: Combining normalized tables for performance. Trade-off: redundancy for read speed. Use for read-heavy analytics or caching scenarios.

**Q15: Explain the difference between DELETE and TRUNCATE.**
A: DELETE removes rows (slower, can rollback); TRUNCATE removes all rows instantly (cannot rollback). Use TRUNCATE for clearing tables.

**Q16: What are constraints and give examples.**
A: Rules enforced on data. Examples: PRIMARY KEY (unique), UNIQUE, NOT NULL, CHECK (age >= 18), FOREIGN KEY.

**Q17: How do you optimize a GROUP BY query?**
A: Index on GROUP BY columns; use HAVING sparingly; avoid complex aggregation functions in HAVING.

**Q18: Explain the difference between relational and NoSQL databases.**
A: Relational uses fixed schema and ACID; NoSQL uses flexible schema and eventual consistency. Choose relational for structured data; NoSQL for massive scale or unstructured data.

**Q19: What is a view in SQL?**
A: Virtual table based on a query. Simplifies complex queries, provides data abstraction.
```sql
CREATE VIEW active_users AS SELECT * FROM users WHERE status = 'active';
```

**Q20: How do you handle NULL values in SQL?**
A: Use IS NULL or IS NOT NULL. COUNT(column) excludes NULLs; COUNT(*) includes them. Use COALESCE to provide defaults: `COALESCE(phone, 'N/A')`.

### Intermediate Questions

**Q21: Write a query to find the second highest salary in the employees table.**
A: 
```sql
SELECT MAX(salary) FROM employees WHERE salary < (SELECT MAX(salary) FROM employees);
-- Or with window functions:
SELECT DISTINCT salary FROM employees ORDER BY salary DESC LIMIT 1 OFFSET 1;
-- Or more reliable:
SELECT salary FROM (SELECT salary, DENSE_RANK() OVER (ORDER BY salary DESC) as rank FROM employees) t WHERE rank = 2;
```

**Q22: Explain the difference between RANK(), DENSE_RANK(), and ROW_NUMBER().**
A: 
- RANK(): Skips ranks after ties (1, 1, 3)
- DENSE_RANK(): Continuous ranks (1, 1, 2)
- ROW_NUMBER(): Sequential (1, 2, 3)

**Q23: How do you implement pagination efficiently in SQL?**
A: Use LIMIT and OFFSET, but be aware OFFSET becomes slow on large numbers.
```sql
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;
-- Better for pagination: use keyset pagination
SELECT * FROM users WHERE id > last_seen_id ORDER BY id LIMIT 20;
```

**Q24: Write a query to find users who placed orders in both 2023 and 2024.**
A:
```sql
SELECT u.id, u.name
FROM users u
WHERE u.id IN (SELECT user_id FROM orders WHERE YEAR(created_at) = 2023)
  AND u.id IN (SELECT user_id FROM orders WHERE YEAR(created_at) = 2024);
```

**Q25: Explain the N+1 query problem and how to solve it.**
A: Fetching parent, then looping through children with individual queries.
```python
# Bad: N+1 queries
users = get_all_users()
for user in users:
    orders = get_orders_for_user(user.id)  # Repeated query

# Good: Single JOIN
SELECT u.*, o.* FROM users u LEFT JOIN orders o ON u.id = o.user_id;
```

**Q26: How do you find duplicate values in a table?**
A:
```sql
SELECT email, COUNT(*) FROM users GROUP BY email HAVING COUNT(*) > 1;
```

**Q27: Write a query to update salary based on department.**
A:
```sql
UPDATE employees SET salary = salary * 1.1 WHERE department = 'Engineering';
-- Or conditional:
UPDATE employees SET salary = CASE 
    WHEN department = 'Engineering' THEN salary * 1.15
    WHEN department = 'Sales' THEN salary * 1.10
    ELSE salary
END;
```

**Q28: How do you achieve row-level security in SQL?**
A: Add filtering conditions based on user context. Many databases support row-level security (RLS) with policies.
```sql
CREATE POLICY user_data ON users USING (user_id = current_user_id());
```

**Q29: Explain the difference between HAVING and WHERE in aggregation.**
A: WHERE filters rows before grouping; HAVING filters groups after aggregation.

**Q30: How do you find the top 3 products by sales in each category?**
A:
```sql
SELECT category, product_id, total_sales
FROM (
    SELECT 
        category, 
        product_id, 
        SUM(sales) as total_sales,
        RANK() OVER (PARTITION BY category ORDER BY SUM(sales) DESC) as rank
    FROM sales
    GROUP BY category, product_id
) ranked
WHERE rank <= 3;
```

**Q31: What is the difference between database views and materialized views?**
A: Views execute query every time; materialized views pre-compute and store results. Views are always current but slower; materialized views are fast but need refreshes.

**Q32: How do you handle time-series data efficiently?**
A: Partition by date range; use time-based indexes; aggregate into buckets.
```sql
SELECT DATE_TRUNC('day', created_at) as day, COUNT(*) as events
FROM events
GROUP BY DATE_TRUNC('day', created_at);
```

**Q33: Explain window frame specification (ROWS, RANGE, GROUPS).**
A: Define which rows to include in window function.
```sql
SELECT salary, SUM(salary) OVER (ORDER BY id ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING) as moving_avg
FROM employees;
```

**Q34: How do you prevent concurrent modification conflicts?**
A: Use optimistic (version numbers) or pessimistic (locks) concurrency control.
```sql
-- Optimistic: check version
UPDATE products SET price = 100, version = version + 1 WHERE id = 5 AND version = 3;

-- Pessimistic: lock
SELECT * FROM products WHERE id = 5 FOR UPDATE;  -- Lock until transaction ends
```

**Q35: Write a query to find products with missing inventory records.**
A:
```sql
SELECT p.id, p.name FROM products p
LEFT JOIN inventory i ON p.id = i.product_id
WHERE i.product_id IS NULL;
```

**Q36: How do you optimize database backup and recovery?**
A: Incremental backups, test recovery procedures, use write-ahead logging, replicate to standby.

**Q37: Explain composite indexes and when to use them.**
A: Index on multiple columns. Useful when queries filter on multiple columns.
```sql
CREATE INDEX idx_user_date ON orders(user_id, created_at);
-- Optimizes: WHERE user_id = 5 AND created_at > '2024-01-01'
```

**Q38: How do you handle time zone conversions in SQL?**
A:
```sql
-- Store in UTC
INSERT INTO events (created_at) VALUES (CURRENT_TIMESTAMP AT TIME ZONE 'UTC');

-- Convert for display
SELECT created_at AT TIME ZONE 'America/New_York' FROM events;
```

**Q39: Explain the difference between CROSS JOIN and INNER JOIN.**
A: CROSS JOIN produces Cartesian product (all combinations); INNER JOIN matches on condition.

**Q40: How do you implement soft deletes in SQL?**
A: Add `deleted_at` column instead of actually deleting.
```sql
ALTER TABLE users ADD deleted_at TIMESTAMP NULL;

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 5;

-- Query active users
SELECT * FROM users WHERE deleted_at IS NULL;
```

### Advanced Questions

**Q41: Design a schema for a social media platform (users, posts, likes, comments).**
A:
```sql
users: id, name, email, created_at
posts: id, user_id, content, created_at
likes: id, post_id, user_id, created_at
comments: id, post_id, user_id, content, created_at

-- Indexes
CREATE INDEX idx_post_user ON posts(user_id);
CREATE INDEX idx_like_post ON likes(post_id);
CREATE INDEX idx_comment_post ON comments(post_id);
CREATE UNIQUE INDEX idx_user_post_like ON likes(user_id, post_id);
```

**Q42: Explain database scaling strategies (vertical, horizontal, sharding, replication).**
A:
- **Vertical**: More powerful server (limited by hardware)
- **Horizontal**: Multiple servers with replication/sharding
- **Sharding**: Partition by key (e.g., user_id % 10) across servers
- **Replication**: Copy data for read scaling (master-slave)

**Q43: How do you handle large data migrations without downtime?**
A: Use dual-write pattern, validation, backfill, then switch.
1. Start writing to new schema alongside old
2. Backfill old data to new
3. Validate consistency
4. Switch to new schema
5. Stop writing to old

**Q44: Design a high-performance search engine query (full-text + filters).**
A:
```sql
-- PostgreSQL with GIN index
SELECT id, title, RANK() OVER (ORDER BY ts_rank(search_vector, query) DESC) as relevance
FROM documents
WHERE search_vector @@ query AND status = 'published' AND created_at > '2024-01-01'
ORDER BY relevance DESC
LIMIT 20;
```

**Q45: Explain query optimization techniques (query rewriting, join reordering, index usage).**
A: Query optimizer uses cost-based analysis to choose execution plan.
- Join reordering: Execute selective filters first
- Index usage: Use indexes on high-cardinality columns with low selectivity
- Materialization: Pre-compute expensive aggregations

**Q46: How do you implement distributed transactions across databases?**
A: Use two-phase commit (2PC) or saga pattern.
- 2PC: Coordinator ensures all participate or all rollback
- Saga: Choreograph local transactions with compensating actions

**Q47: Design a schema for an e-commerce system with inventory management.**
A:
```sql
products: id, name, sku, price
inventory: product_id, warehouse_id, quantity
orders: id, user_id, status, created_at
order_items: order_id, product_id, quantity, price
shipments: order_id, warehouse_id, status

-- Constraints
ALTER TABLE inventory ADD CONSTRAINT check_qty CHECK (quantity >= 0);
CREATE UNIQUE INDEX idx_product_warehouse ON inventory(product_id, warehouse_id);
```

**Q48: How do you handle GDPR compliance (data deletion, retention).**
A:
```sql
-- Soft delete with retention period
ALTER TABLE users ADD deleted_at TIMESTAMP NULL, retention_until TIMESTAMP NULL;

-- Hard delete after retention
DELETE FROM users WHERE deleted_at < NOW() - INTERVAL 90 DAY;

-- Anonymize instead of deleting
UPDATE users SET email = MD5(id), name = 'Anonymous' WHERE deleted_at IS NOT NULL;
```

**Q49: Explain columnar vs row-oriented storage and when to use each.**
A:
- **Row-oriented** (OLTP): Fast for transactional queries (all columns for few rows)
- **Columnar** (OLAP): Fast for analytical queries (few columns for many rows, compression)

**Q50: Design a schema for a real-time analytics dashboard (events, metrics, aggregations).**
A:
```sql
events: id, user_id, event_type, value, created_at (partitioned by date)
event_metrics: hourly aggregated view (materialized)

-- Pre-aggregate for dashboard
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT DATE_TRUNC('hour', created_at) as hour, event_type, COUNT(*) as count, SUM(value) as total
FROM events
GROUP BY hour, event_type;
```

**Q51: How do you detect and prevent deadlocks?**
A: Order lock acquisition consistently; set lock timeouts; use row versioning.

**Q52: Explain the difference between optimistic and pessimistic locking.**
A:
- **Optimistic**: Version numbers; fail if version changed
- **Pessimistic**: Lock rows; wait until lock released

**Q53: Design a schema for a content recommendation system.**
A:
```sql
users: id, name
content: id, title, category
user_preferences: user_id, category, score
interactions: user_id, content_id, type (view/like/share), created_at

-- Find recommendations
SELECT c.id, c.title
FROM content c
JOIN user_preferences up ON c.category = up.category
WHERE up.user_id = ? AND up.score > 0.5
ORDER BY up.score DESC;
```

**Q54: How do you monitor query performance in production?**
A: Query logs, slow query logs, EXPLAIN ANALYZE, performance dashboards tracking latency, throughput, resource usage.

**Q55: Explain the CAP theorem and how it applies to database design.**
A: Can only have 2 of: Consistency (all nodes see same data), Availability (system always up), Partition tolerance (survive network splits). SQL databases choose CA; NoSQL choose AP or CP.

**Q56: Design a schema for a multi-tenant SaaS application.**
A:
```sql
tenants: id, name, plan
users: id, tenant_id, name, email
data: id, tenant_id, content  -- Every table includes tenant_id for isolation

-- Row-level security
CREATE POLICY tenant_isolation ON data USING (tenant_id = current_tenant_id());
```

**Q57: How do you handle schema migrations on large tables without downtime?**
A: Expand-migrate-contract pattern. Create new column, backfill, switch, then drop old column.

**Q58: Explain the difference between replication and sharding.**
A:
- **Replication**: Copy data across servers (increases availability, read scale)
- **Sharding**: Partition data across servers (increases write scale, storage)

**Q59: Design a schema for real-time notifications system.**
A:
```sql
users: id, name
notifications: id, user_id, title, message, read_at, created_at
notification_settings: user_id, type, enabled

-- Indexes for fast retrieval
CREATE INDEX idx_user_created ON notifications(user_id, created_at DESC);
```

**Q60: How do you measure and optimize database query cost?**
A: Use EXPLAIN ANALYZE; measure I/O (seeks, scans), CPU, memory; profile hot queries; optimize with indexes, partitioning, materialization; monitor production metrics (latency, throughput).

---

## 10. Common Mistakes

**Mistake 1: Missing Indexes on Frequently Searched Columns**
- ❌ No index on WHERE clause columns
- ✅ Create index: `CREATE INDEX idx_email ON users(email);`
- Impact: O(n) vs O(log n) for 1M row table = 100x slower

**Mistake 2: N+1 Query Problem**
- ❌ Loop fetching related data: `for user in users: get_orders(user.id)`
- ✅ Single JOIN: `SELECT u.*, o.* FROM users u JOIN orders o ON u.id = o.user_id;`
- Impact: 1000 users = 1001 queries vs 1 query

**Mistake 3: Denormalization Without Justification**
- ❌ Store user info in orders table
- ✅ Keep normalized; use JOIN or materialized view
- Impact: Update anomalies, redundancy, data inconsistency

**Mistake 4: Not Using Transactions for Multi-Step Operations**
- ❌ Separate UPDATEs (money transfer: debit then credit)
- ✅ ACID transaction: all-or-nothing
- Impact: Incomplete transfers, data inconsistency

**Mistake 5: Ignoring Query Execution Plans**
- ❌ Assume query is efficient
- ✅ Use EXPLAIN; check for full table scans
- Impact: Slow queries undetected in production

**Mistake 6: Using SELECT * When Only Few Columns Needed**
- ❌ `SELECT * FROM users WHERE id = 5;`
- ✅ `SELECT id, name, email FROM users WHERE id = 5;`
- Impact: Network overhead, I/O, caching inefficiency

**Mistake 7: No Foreign Key Constraints**
- ❌ Manually enforce referential integrity
- ✅ Add FK constraints: `REFERENCES users(id)`
- Impact: Orphaned records, data corruption

**Mistake 8: Using COUNT(*) to Check Existence**
- ❌ `IF COUNT(*) > 0: process()`
- ✅ `IF EXISTS (SELECT 1 FROM ...)`
- Impact: Counts all rows (slow) vs checking first row (fast)

**Mistake 9: Not Partitioning Large Tables**
- ❌ Single billion-row table; all queries scan entire table
- ✅ Partition by date, user_id, region
- Impact: Query speed + maintenance burden

**Mistake 10: Insufficient Testing of Transaction Isolation**
- ❌ Assume isolation level is correct
- ✅ Test for dirty reads, phantom reads, etc.
- Impact: Race conditions in production

**Mistake 11: Storing Objects/JSON in VARCHAR**
- ❌ Serialize to JSON string; lost query ability
- ✅ Use native JSON columns (PostgreSQL JSONB)
- Impact: Can't query inside objects; must deserialize

**Mistake 12: No Backup/Recovery Testing**
- ❌ Backups exist; never tested
- ✅ Test restore procedures regularly
- Impact: Backups corrupted; can't recover

---

## 11. Comparison Section

### SQL vs NoSQL

| Aspect | SQL (PostgreSQL, MySQL) | NoSQL (MongoDB, Redis) |
|--------|------------------------|----------------------|
| **Schema** | Fixed; changes require migration | Flexible; evolving schema |
| **Data Type** | Structured (tables, rows) | Unstructured (documents, KV) |
| **ACID** | Full ACID transactions | Eventually consistent (some support ACID) |
| **Scale** | Vertical (single powerful server) | Horizontal (distributed across servers) |
| **Joins** | Native; efficient with indexes | No joins; denormalize |
| **Query Language** | SQL (standardized) | Custom (e.g., MongoDB query language) |
| **Use Case** | Relational data (users, orders) | Fast caching, massive scale |

### Relational vs Document Databases

| Aspect | Relational | Document |
|--------|-----------|----------|
| **Relationships** | Foreign keys; cross-table | Embed nested data |
| **Atomicity** | Row-level ACID | Document-level ACID |
| **Queries** | JOINs across tables | Query within document |
| **Consistency** | Strong | Eventual |

---

## 12. Practical Projects

**Project 1: E-Commerce Database**
Build schema for: users, products, categories, inventory, orders, payment, shipping.
- Implement normalization (1NF-3NF)
- Add foreign key constraints
- Create indexes for performance
- Write complex queries (top products by sales, user purchase history, etc.)

**Project 2: Social Media Analytics**
Track: users, posts, likes, comments, followers.
- Use window functions to rank users by post engagement
- Calculate trending topics with aggregation
- Implement soft deletes for GDPR compliance
- Partition events by date for OLAP queries

**Project 3: Real-Time Monitoring Dashboard**
Aggregate metrics: system events, user activities, performance metrics.
- Partition events by hour
- Use materialized views for pre-aggregation
- Implement efficient time-series queries
- Design backup/recovery strategy

---

## 13. Internship Preparation Notes

**Resume Tips**:
- Mention schema design experience: "Designed normalized database schema for X with 500K+ users"
- Highlight optimization: "Optimized slow query from 10s to 100ms using indexes and query rewriting"
- Emphasize scale: "Managed PostgreSQL database with 1B+ records, 100K+ QPS"

**Interview Focus Areas**:
1. **Schema Design**: Can you normalize? Identify 1NF, 2NF, 3NF issues?
2. **Query Performance**: Can you optimize? Use EXPLAIN? Understand indexes?
3. **ACID & Transactions**: When to use? How to prevent race conditions?
4. **Real-World Experience**: Any production issues? How did you solve them?

**Projects to Build**:
- E-commerce system (inventory, orders, payments)
- Social network (users, posts, followers)
- Analytics dashboard (events, metrics, aggregations)

---

## 14. Cheat Sheet

**DDL (Data Definition Language)**
```sql
CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));
ALTER TABLE users ADD email VARCHAR(100) UNIQUE;
DROP TABLE users;
```

**DML (Data Manipulation Language)**
```sql
INSERT INTO users VALUES (1, 'Alice', 'alice@test.com');
UPDATE users SET name = 'Alicia' WHERE id = 1;
DELETE FROM users WHERE id = 1;
```

**Query Operations**
```sql
SELECT * FROM users WHERE age > 25;
SELECT DISTINCT department FROM employees;
SELECT * FROM users ORDER BY age DESC LIMIT 10;
```

**Joins**
```sql
INNER JOIN: SELECT * FROM a INNER JOIN b ON a.id = b.a_id;
LEFT JOIN: SELECT * FROM a LEFT JOIN b ON a.id = b.a_id;
FULL JOIN: SELECT * FROM a FULL JOIN b ON a.id = b.a_id;
CROSS JOIN: SELECT * FROM a CROSS JOIN b;
```

**Aggregation**
```sql
SELECT department, COUNT(*), AVG(salary) FROM employees GROUP BY department;
HAVING COUNT(*) > 5;
```

**Window Functions**
```sql
RANK() OVER (ORDER BY salary DESC)
ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC)
LAG(salary) OVER (ORDER BY date)
SUM(sales) OVER (ORDER BY date ROWS BETWEEN 7 PRECEDING AND CURRENT ROW)
```

**Indexes**
```sql
CREATE INDEX idx_email ON users(email);
CREATE UNIQUE INDEX idx_user_product ON likes(user_id, product_id);
DROP INDEX idx_email;
```

**Transactions**
```sql
BEGIN TRANSACTION;
UPDATE account SET balance = balance - 100 WHERE id = 1;
UPDATE account SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

---

## 15. One-Day Revision Checklist

- [ ] Explain normalization (1NF, 2NF, 3NF)
- [ ] Write INNER/LEFT/FULL JOIN query
- [ ] Optimize slow query with EXPLAIN
- [ ] Design schema for real-world scenario
- [ ] Implement transaction for multi-step operation
- [ ] Use window functions (RANK, LAG, SUM OVER)
- [ ] Write CTE for hierarchical data
- [ ] Handle NULL values correctly
- [ ] Create indexes on right columns
- [ ] Explain ACID properties with example
