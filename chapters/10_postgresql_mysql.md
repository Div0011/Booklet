# 10. PostgreSQL & MySQL (Database Systems & Practical SQL)

## 1. Introduction

### What it is
**PostgreSQL** and **MySQL** are two dominant open-source relational database management systems (RDBMS). PostgreSQL is a feature-rich, standards-compliant database excelling in complex queries, advanced data types, and reliability. MySQL is lightweight, fast, and optimized for web applications (LAMP stack). Both store structured data, execute SQL queries, and provide ACID transactions, but with different trade-offs in performance, features, and use cases.

### Why they exist
MySQL (1995) prioritized speed and simplicity for web development, becoming the backbone of LAMP stack. PostgreSQL (1989, evolved from Ingres) prioritized correctness, advanced features, and SQL compliance. Together, they power most web applications, data warehouses, and startups because they're free, proven, battle-tested at scale, and widely supported by hosting platforms.

### Problems they solve
- **Reliable Storage**: Durable, ACID-compliant persistence across application crashes.
- **Performance**: Optimized query execution, intelligent indexing, query caching strategies.
- **Scalability**: Handle millions of rows with sub-second response times through indexing and partitioning.
- **Concurrency**: Multiple users simultaneously without race conditions via locking and transaction isolation.
- **Advanced Data Types**: JSON, arrays, ranges, custom types beyond basic text/numbers.
- **Replication & HA**: High availability through master-slave or multi-master setups with automatic failover.
- **Compliance**: Audit trails, immutable logs, compliance with regulatory requirements.

### Industry Use Cases
- **PostgreSQL**: Financial systems (ACID critical), geospatial data (PostGIS extension), data warehouses (complex analytics), complex schemas with rich constraints.
- **MySQL**: Web applications (WordPress, Drupal), e-commerce platforms (Magento, WooCommerce), content management systems, high-throughput OLTP systems.

### Analogy
PostgreSQL is a **Swiss Army knife**: feature-rich, flexible, powerful for complex tasks requiring precision. MySQL is a **hammer**: simple, reliable, perfect for common tasks and rapid deployment. Choose PostgreSQL for complexity; choose MySQL for speed and simplicity. Both are professional tools excelling in their domain.

---

## 2. Core Concepts

### PostgreSQL Advanced Features

#### JSON/JSONB Support
Native JSON and JSONB columns for semi-structured data within ACID transactions.

```sql
CREATE TABLE events (
    id INT PRIMARY KEY,
    data JSONB
);

INSERT INTO events VALUES (1, '{"user": "Alice", "action": "login", "timestamp": "2024-06-09"}');

-- Extract with operator ->
SELECT data->>'user' FROM events;  -- Returns "Alice" as text

-- Array access
SELECT data->'metadata'->'tags' FROM events;

-- Containment check (fast with GIN index)
SELECT * FROM events WHERE data @> '{"action": "login"}';
```

#### Full-Text Search (FTS)
Built-in tsvector for keyword searching with linguistic support.

```sql
ALTER TABLE documents ADD COLUMN search_vector tsvector;
UPDATE documents SET search_vector = to_tsvector('english', title || ' ' || content);
CREATE INDEX idx_search ON documents USING gin(search_vector);

-- Query with multiple keywords
SELECT * FROM documents 
WHERE search_vector @@ to_tsquery('english', 'python & (database | postgresql)');
```

#### Native Array Types
First-class array support in columns; query array elements directly.

```sql
CREATE TABLE teams (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    members TEXT[],
    scores INT[]
);

INSERT INTO teams VALUES (1, 'Alpha', '{"Alice", "Bob", "Charlie"}', '{100, 95, 87}');

-- Query specific element
SELECT members[1], scores[1] FROM teams;  -- "Alice", 100

-- Check if element exists
SELECT * FROM teams WHERE "Alice" = ANY(members);

-- Array aggregation
SELECT id, array_agg(DISTINCT member) FROM team_members GROUP BY id;
```

#### PostGIS (Geospatial)
Extensions for location-based queries and geographic data analysis.

```sql
-- Point data type
CREATE TABLE locations (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    coords POINT
);

-- Distance queries
SELECT * FROM locations 
WHERE ST_Distance(coords::geometry, ST_Point(0, 0)::geometry) < 10;

-- Within area
SELECT * FROM locations 
WHERE ST_Contains(ST_MakeCircle(center, radius), coords);
```

#### Advanced Constraints
Rich constraint support: CHECK, UNIQUE, NOT NULL, EXCLUSION, domain constraints.

```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    age INT CHECK (age >= 18 AND age <= 150),
    phone VARCHAR(20),
    CONSTRAINT phone_or_email CHECK (phone IS NOT NULL OR email IS NOT NULL)
);

-- Exclusion constraint (no overlapping bookings)
CREATE TABLE bookings (
    id INT PRIMARY KEY,
    room_id INT,
    time_range tsrange,
    EXCLUDE USING gist (room_id WITH =, time_range WITH &&)
);
```

### MySQL Specific Features

#### Storage Engines
Pluggable architecture allows choosing engine per table.

```sql
-- InnoDB: Default, ACID, transactions, row-locking (best for most use cases)
CREATE TABLE data (
    id INT PRIMARY KEY
) ENGINE=InnoDB;

-- MyISAM: Older, faster reads but no ACID/transactions (legacy only)
CREATE TABLE cache (
    id INT PRIMARY KEY
) ENGINE=MyISAM;

-- Memory: In-memory storage; fast but data lost on restart
CREATE TABLE temp_data (
    id INT PRIMARY KEY
) ENGINE=MEMORY;
```

#### Partitioning for Large Tables
Horizontal partitioning enabling queries to scan only relevant partitions.

```sql
CREATE TABLE orders (
    id INT PRIMARY KEY,
    user_id INT,
    order_date DATE
) PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Query on 2024 only scans p2024 partition (10-100x faster on billion-row tables)
SELECT * FROM orders WHERE YEAR(order_date) = 2024;
```

#### Master-Slave Replication
Asynchronous replication for read scaling and disaster recovery.

```sql
-- Master configuration
[mysqld]
log-bin=mysql-bin
server-id=1
binlog-format=ROW
binlog-do-db=production

-- Slave configuration
[mysqld]
server-id=2
relay-log=relay-bin
relay-log-index=relay-bin.index
relay-log-purge=1

CHANGE MASTER TO 
  MASTER_HOST='192.168.1.100',
  MASTER_USER='repl_user',
  MASTER_PASSWORD='secure_password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=154,
  MASTER_PORT=3306;

START SLAVE;
SHOW SLAVE STATUS\G
```

#### Full-Text Indexes
Native full-text search without extension; faster than LIKE for keyword search.

```sql
CREATE TABLE articles (
    id INT PRIMARY KEY,
    title VARCHAR(200),
    content TEXT,
    FULLTEXT INDEX ft_title_content (title, content)
);

SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('machine learning' IN BOOLEAN MODE);

-- Boolean operators
WHERE MATCH(title) AGAINST('+python -javascript' IN BOOLEAN MODE);  -- Must have python, exclude javascript
```

---

## 3. Internal Working

### Index Structures (Both Systems)
Both PostgreSQL and MySQL use B-Tree indexes as default (some support Hash, GIN, GiST).

```
Level 3:             [M]
                    /   \
Level 2:          [G]     [T]
                 / | \    / \
Level 1:      [A][J][P][S][X]
```

Each level has search keys pointing to child nodes. Leaf nodes contain row pointers. Lookup is O(log n).

### Query Optimization Flow
```
SQL Statement
  ↓
Parser (syntax check)
Abstract Syntax Tree
  ↓
Semantic Analyzer (table/column validation)
  ↓
Optimizer (cost estimation)
  ├─ Reorder joins
  ├─ Choose indexes
  └─ Select execution plan
  ↓
Executor (physically execute plan)
  ↓
Result Set
```

### Transaction Isolation Levels
```
READ UNCOMMITTED
  ↓ (prevents dirty reads)
READ COMMITTED (PostgreSQL/MySQL default)
  ↓ (prevents repeatable read issues)
REPEATABLE READ (PostgreSQL default)
  ↓ (prevents phantom reads)
SERIALIZABLE (strictest; equivalent to sequential execution)
```

### Replication Architecture
```
Master (Primary)
 ↓ (binary log)
 → Slave (Replica)
   - Relay log receives binary events
   - SQL thread applies events
   - Data replicated asynchronously
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **InnoDB** | MySQL's default ACID-compliant storage engine with transactions |
| **MyISAM** | Older MySQL engine; fast but no ACID or transaction support |
| **JSONB** | Binary JSON format in PostgreSQL; faster than text JSON |
| **GIN Index** | Generalized Inverted Index; optimizes searches in JSON, arrays |
| **Full-Text Search** | Keyword indexing for natural language queries |
| **Replication** | Copying data from master to slaves for redundancy/scaling |
| **Binary Log** | Sequence of write events; basis for replication |
| **EXPLAIN** | Displays query execution plan with cost estimates |
| **Isolation Level** | Specifies how concurrent transactions interact |
| **Partitioning** | Horizontal split of table; queries scan only relevant partition |
| **Extension** | PostgreSQL plugin adding features (PostGIS, hstore, etc.) |
| **Failover** | Automatic switch to replica if primary fails |
| **Master-Slave** | Primary handles writes; replicas handle reads |
| **Materialized View** | Pre-computed query result; requires explicit refresh |
| **Query Plan** | Optimized sequence of operations to execute query |

---

## 5. Beginner Examples

### PostgreSQL: JSON Queries
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    profile JSONB
);

INSERT INTO users VALUES (
    1, 'Alice', '{"age": 30, "city": "SF", "skills": ["Python", "SQL"]}'
);

-- Extract top-level field
SELECT profile->>'age' FROM users WHERE id = 1;  -- "30"

-- Extract nested array element
SELECT profile->'skills'->0 FROM users;  -- "Python"

-- Filter by JSON value
SELECT * FROM users WHERE profile->>'city' = 'SF';

-- Check if key exists
SELECT * FROM users WHERE profile ? 'age';

-- JSON array operations
SELECT * FROM users WHERE profile->'skills' @> '"Python"'::jsonb;
```

### MySQL: Full-Text Search
```sql
CREATE TABLE articles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FULLTEXT INDEX idx_title_content (title, content)
);

INSERT INTO articles (title, content) VALUES 
    ('Machine Learning Guide', 'Learn Python and ML algorithms'),
    ('Web Development with JavaScript', 'Build apps using React and Node.js');

-- Basic search
SELECT * FROM articles 
WHERE MATCH(title, content) AGAINST('machine learning');

-- Boolean mode with operators
SELECT * FROM articles 
WHERE MATCH(title) AGAINST('+python -javascript' IN BOOLEAN MODE);
```

### PostgreSQL: Array Operations
```sql
CREATE TABLE projects (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    technologies TEXT[]
);

INSERT INTO projects VALUES 
    (1, 'WebApp', '{"Python", "React", "PostgreSQL"}'),
    (2, 'Analytics', '{"Python", "Pandas", "Spark"}');

-- Check membership
SELECT * FROM projects WHERE 'Python' = ANY(technologies);

-- Array length
SELECT name, array_length(technologies, 1) as num_techs FROM projects;

-- Array contains
SELECT * FROM projects WHERE technologies @> '{"React"}';

-- Unnest to pivot
SELECT name, unnest(technologies) as tech FROM projects;
```

### MySQL: Replication Setup
```sql
-- On Master
SHOW MASTER STATUS;  -- Returns: File='mysql-bin.000001', Position=123

-- On Slave
CHANGE MASTER TO 
  MASTER_HOST='master_ip',
  MASTER_USER='repl_user',
  MASTER_PASSWORD='password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=123;

START SLAVE;
SHOW SLAVE STATUS\G  -- Check if Slave_IO_Running and Slave_SQL_Running are YES

-- Check replication lag
SHOW SLAVE STATUS\G | grep Seconds_Behind_Master;
```

### PostgreSQL: Window Functions
```sql
CREATE TABLE sales (
    id INT PRIMARY KEY,
    salesperson_id INT,
    amount DECIMAL(10, 2),
    sale_date DATE
);

SELECT 
    salesperson_id,
    amount,
    RANK() OVER (ORDER BY amount DESC) as rank,
    SUM(amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date) as running_total,
    LAG(amount) OVER (PARTITION BY salesperson_id ORDER BY sale_date) as prev_sale
FROM sales;
```

---

## 6. Intermediate Examples

### Example 1: PostgreSQL JSONB Performance Optimization
```sql
-- Without index: O(n) full table scan
CREATE TABLE logs (
    id BIGINT PRIMARY KEY,
    data JSONB
);

INSERT INTO logs VALUES (1, '{"level": "ERROR", "service": "auth", "code": 500}');

-- Add GIN index for JSON queries
CREATE INDEX idx_logs_data ON logs USING gin(data);

-- Now fast: uses index instead of full scan
SELECT * FROM logs WHERE data->>'level' = 'ERROR';

-- Can also index specific JSON path
CREATE INDEX idx_logs_level ON logs USING gin((data->'level'));
SELECT * FROM logs WHERE data->'level' @@ '"ERROR"'::jsonb;
```

### Example 2: MySQL Partitioning for Performance
```sql
-- Before: 1B row table; every query scans all partitions
CREATE TABLE transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    amount DECIMAL(12, 2),
    transaction_date DATE
) ENGINE=InnoDB;

-- After: Partition by date range
ALTER TABLE transactions PARTITION BY RANGE (YEAR(transaction_date)) (
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024),
    PARTITION p2024 VALUES LESS THAN (2025),
    PARTITION p_future VALUES LESS THAN MAXVALUE
);

-- Query on p2024 only scans 1/4 of data
-- 1B rows → 250M rows = 4-10x faster
SELECT COUNT(*) FROM transactions WHERE YEAR(transaction_date) = 2024;
```

### Example 3: PostgreSQL Full-Text Search with Language Support
```sql
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Update with English language lexeme support
UPDATE articles SET search_vector = to_tsvector('english', 
    coalesce(title, '') || ' ' || coalesce(content, '')
);

-- Create GIN index for fast search
CREATE INDEX idx_articles_search ON articles USING gin(search_vector);

-- Query combining multiple keywords with operators
SELECT title FROM articles 
WHERE search_vector @@ to_tsquery('english', 
    'machine & (learning | deep) & !javascript'
);
```

### Example 4: MySQL Multi-Master Replication Setup
```sql
-- Master 1 Configuration
[mysqld]
log-bin=mysql-bin
server-id=1
binlog-format=ROW
auto-increment-increment=2
auto-increment-offset=1

-- Master 2 Configuration
[mysqld]
log-bin=mysql-bin
server-id=2
binlog-format=ROW
auto-increment-increment=2
auto-increment-offset=2

-- Both replicate from each other; automatic failover possible
-- Writes can go to either master; data stays consistent
-- Useful for: Zero-downtime maintenance, geographic distribution
```

### Example 5: PostgreSQL Composite Types and Constraints
```sql
-- Define composite type
CREATE TYPE address AS (
    street VARCHAR(100),
    city VARCHAR(50),
    zip_code VARCHAR(10)
);

CREATE TABLE customers (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    address address,
    contact_emails TEXT[],
    age INT CHECK (age >= 18)
);

-- Insert with composite type
INSERT INTO customers VALUES (
    1, 'Alice', ('123 Main St', 'SF', '94103'), '{"alice@work.com", "alice@home.com"}', 30
);

-- Query composite type
SELECT (address).city FROM customers;
SELECT contact_emails[1] FROM customers;
```

---

## 7. Advanced Examples

### Example 1: PostgreSQL Recursive CTE for Hierarchical Data
```sql
-- Organization structure: find all reports under a manager
WITH RECURSIVE org_chart AS (
    -- Base case: CEO (no manager)
    SELECT id, name, manager_id, title, 1 as depth
    FROM employees
    WHERE manager_id IS NULL
    
    UNION ALL
    
    -- Recursive case: direct reports
    SELECT e.id, e.name, e.manager_id, e.title, org.depth + 1
    FROM employees e
    INNER JOIN org_chart org ON e.manager_id = org.id
    WHERE org.depth < 10  -- Prevent infinite loops
)
SELECT 
    REPEAT('  ', depth - 1) || name as employee_hierarchy,
    title,
    depth
FROM org_chart
ORDER BY depth, manager_id, id;
```

### Example 2: MySQL Connection Pooling & Optimization
```sql
-- Enable connection pooling
[mysqld]
max_connections=1000
max_allowed_packet=256M
thread_cache_size=100

-- Client side (Python example)
import mysql.connector
from mysql.connector import pooling

pool = pooling.MySQLConnectionPool(
    pool_name="web_pool",
    pool_size=32,
    pool_reset_session=True,
    host="localhost",
    user="app",
    password="secure",
    database="production"
)

conn = pool.get_connection()  # From pool; reused
cursor = conn.cursor()
cursor.execute("SELECT ...")
pool.close_all()  # Return to pool
```

### Example 3: PostgreSQL Extension for UUID and JSON Operations
```sql
-- Install extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "hstore";

CREATE TABLE api_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    endpoint VARCHAR(200),
    metadata HSTORE,  -- Key-value store alternative to JSON
    response_time_ms INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert with UUID generation
INSERT INTO api_logs (endpoint, metadata, response_time_ms) VALUES (
    '/api/users', 'version=>1.0, region=>us-west', 45
);

-- Query hstore
SELECT * FROM api_logs WHERE metadata->'region' = 'us-west';
SELECT * FROM api_logs WHERE response_time_ms > 100;
```

### Example 4: MySQL Backup & Recovery Strategy
```bash
# Full backup (all data)
mysqldump -u root -p --all-databases > full_backup_2024-06-09.sql

# Backup with master status (for replication recovery)
mysqldump -u root -p --all-databases --master-data=2 > backup_with_binlog.sql

# Incremental backup (binary log)
# Get current position: SHOW MASTER STATUS;
# Copy binary log to backup: cp mysql-bin.000001 /backups/

# Restore full backup
mysql -u root -p < full_backup_2024-06-09.sql

# Restore from specific point in time
mysqlbinlog mysql-bin.000001 mysql-bin.000002 | mysql -u root -p
```

### Example 5: PostgreSQL Hot Standby & Streaming Replication
```sql
-- Primary (PostgreSQL.conf)
wal_level = replica  -- Enable replication logging
max_wal_senders = 3
wal_keep_size = 1GB

-- Standby (recovery.conf)
standby_mode = on
primary_conninfo = 'host=primary.example.com port=5432 user=repl password=repl'

-- Streaming replication: standby receives WAL continuously (near real-time)
-- Hot standby: standby can accept read-only queries while receiving updates
SELECT * FROM pg_stat_replication;  -- Monitor replication lag
```

### Example 6: PostgreSQL Row Level Security (RLS) & Multi-Tenant Isolation
Row Level Security (RLS) filters query results before query execution. It allows you to restrict which rows a user can select, insert, update, or delete based on session variables or roles.

```sql
-- 1. Create a table with multi-tenant data
CREATE TABLE customer_orders (
    order_id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Enable RLS on the table
ALTER TABLE customer_orders ENABLE ROW LEVEL SECURITY;

-- 3. Create a policy restricting access using a session variable
-- 'USING' controls which rows are visible for SELECT/UPDATE/DELETE.
-- 'WITH CHECK' controls which rows are allowed to be INSERTed/UPDATEd.
CREATE POLICY tenant_isolation_policy ON customer_orders
    FOR ALL
    TO authenticated_app_user
    USING (tenant_id = current_setting('app.current_tenant_id', true))
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id', true));

-- 4. How the backend API runs queries safely:
-- Every database connection sets the session context within a local transaction
BEGIN;
SET LOCAL app.current_tenant_id = 'tenant_xyz_45';
SELECT * FROM customer_orders; -- Automatically returns only orders belonging to 'tenant_xyz_45'
INSERT INTO customer_orders (tenant_id, customer_name, total_amount) 
    VALUES ('tenant_xyz_45', 'John Doe', 150.00); -- Succeeds
    
-- Attempting to insert a row for a different tenant fails
-- INSERT INTO customer_orders (tenant_id, customer_name, total_amount) 
--    VALUES ('tenant_abc_12', 'Jane Smith', 80.00); -- Throws RLS violation error
COMMIT;

-- 5. Headless JWT integration (e.g. Supabase Auth)
-- RLS policies can extract values directly from JWT structures passed in headers
CREATE POLICY jwt_tenant_policy ON customer_orders
    FOR SELECT
    USING (tenant_id = (auth.jwt() -> 'user_metadata' ->> 'tenant_id'));
```

---

## 8. How Interviewers Think

### Red Flags (What Interviewers Want to Avoid)
- ❌ **Choosing Wrong Engine**: Using MyISAM for transactional data
- ❌ **No Connection Pooling**: Creating new DB connection per request (100x slower)
- ❌ **Ignoring Replication Lag**: Expecting consistency across master-slave immediately
- ❌ **Not Monitoring Slow Queries**: Deploying without slow query log enabled
- ❌ **Poor Partitioning Strategy**: Partitioning on low-cardinality column (little benefit)
- ❌ **Missing Backup Testing**: No tested recovery procedure

### Green Flags (What Interviewers Want to See)
- ✅ **Storage Engine Selection**: "InnoDB for ACID; MyISAM only if no transactions needed"
- ✅ **Replication Strategy**: "Master for writes; replicas for read scaling; monitor lag"
- ✅ **Performance Thinking**: "Profile queries; use EXPLAIN; index high-cardinality columns"
- ✅ **High Availability**: "Multi-master or hot standby; automatic failover; tested recovery"
- ✅ **JSON Usage**: "Use JSONB in PostgreSQL, not TEXT; index with GIN"
- ✅ **Scaling Knowledge**: "Understand partitioning limits; know when to shard"

### Answer Matrix
**Q: "When would you choose PostgreSQL over MySQL?"**
- 🟢 Complex queries, JSON, arrays, PostGIS, ACID critical, many advanced features
- 🟡 Large datasets, complex transactions
- 🔴 "PostgreSQL is always better" (ignores MySQL strengths)

---

## 9. Frequently Asked Interview Questions

### Beginner Questions

**Q1: What are the main differences between PostgreSQL and MySQL?**
A: PostgreSQL has more advanced features (JSON, arrays, PostGIS, window functions), stronger ACID guarantees, and better compliance with SQL standards. MySQL is simpler, faster for basic OLTP, and widely used in web stacks. PostgreSQL scales well with complex queries; MySQL scales with read replicas and sharding.

**Q2: What is the difference between InnoDB and MyISAM?**
A: InnoDB supports ACID transactions, row-level locking, foreign keys, and crash recovery. MyISAM is faster for reads but lacks transactions, offers only table-level locking, and can corrupt data on crashes. Use InnoDB for production; MyISAM only for read-only data or caches.

**Q3: Explain master-slave replication.**
A: Master handles writes; slaves replicate data asynchronously via binary logs. Slaves can handle read queries (scaling reads). If master fails, promote a slave to master (failover). Replication lag: slave may be seconds behind master (eventual consistency).

**Q4: What is a materialized view and when would you use it?**
A: Pre-computed query result stored on disk. Refresh periodically. Use for expensive aggregations, complex analytics queries, reducing load on main tables. Trade-off: stale data until refresh; storage overhead.

**Q5: How do you optimize a slow MySQL query?**
A: Use EXPLAIN to see execution plan; look for full table scans. Add indexes on WHERE/JOIN columns. Consider partitioning for large tables. Use LIMIT to fetch only needed rows. Profile CPU/I/O with slow query log.

**Q6: Explain connection pooling and why it matters.**
A: Pool maintains open connections; requests use existing connections instead of creating new ones. Each connection creation takes ~100ms; connection overhead can kill performance. Pool size depends on concurrent requests.

**Q7: What is JSONB in PostgreSQL and why is it better than JSON?**
A: JSONB stores JSON in binary format; faster for queries and updates. Supports indexing with GIN. JSON is text-based; must be re-parsed on each query. Use JSONB always unless you need exact formatting.

**Q8: How do you handle replication lag in a read replica?**
A: Accept eventual consistency or route critical reads to master. Monitor `Seconds_Behind_Master` (MySQL) or `pg_stat_replication` (PostgreSQL). Use connection pooling to distribute load across replicas.

**Q9: Explain hot standby in PostgreSQL.**
A: Read-only replica that continuously receives WAL (write-ahead log) from primary. Can accept SELECT queries while replicating. Useful for read scaling without asynchronous replication lag.

**Q10: What are the advantages of partitioning?**
A: Queries scan only relevant partition (much faster on large tables). Easier maintenance (drop partitions instead of DELETE). Can improve cache hit rate. Downsides: complexity, JOIN across partitions, need good partition key.

**Q11: How do you choose partition key?**
A: Choose high-cardinality column used in WHERE clauses. Avoid low-cardinality (most queries hit multiple partitions). Range partitioning: date, user_id. List partitioning: region, status.

**Q12: Explain Full-Text Search in MySQL.**
A: FULLTEXT index on text columns. MATCH() function with AGAINST(). Faster than LIKE for keyword search. Supports Boolean mode: +word (required), -word (excluded), word* (prefix).

**Q13: How do you backup PostgreSQL safely?**
A: pg_dump (logical backup); pg_basebackup (physical backup with WAL). Test recovery procedures. Use WAL archiving for point-in-time recovery. Backup compression to save storage.

**Q14: What is GIN index in PostgreSQL?**
A: Generalized Inverted Index; optimizes searches in arrays, JSON, hstore. Slower to build than B-Tree but faster for multi-value searches. Use for JSONB @> (contains), array @> (contains).

**Q15: How do you migrate from MySQL to PostgreSQL?**
A: Use tools like Migrate for automated migration. Test schema compatibility (MySQL allows more lax typing). Validate data; compare row counts. Use pgloader for fast data transfer. Plan downtime or use dual-write during transition.

**Q16: What is the difference between REPEATABLE READ and SERIALIZABLE?**
A: REPEATABLE READ: transaction sees consistent snapshot but phantom rows possible. SERIALIZABLE: completely isolated; equivalent to sequential execution. MySQL SERIALIZABLE slower but safest for critical transactions.

**Q17: How do you handle connection limits?**
A: Use connection pooling (PgBouncer, ProxySQL, MySQL Connector). Set `max_connections` appropriately. Monitor active connections. Implement timeout on idle connections. Auto-scale pool size with load.

**Q18: Explain the difference between streaming replication and WAL archiving.**
A: Streaming replication: standby receives WAL continuously (real-time). WAL archiving: WAL files copied to backup for later restoration. Combine both: streaming for hot standby; archive for recovery.

**Q19: How do you optimize storage in PostgreSQL?**
A: VACUUM removes dead rows; ANALYZE updates statistics. Use TOAST (out-of-line storage) for large columns. Compress with pg_dump. Monitor table bloat with pgstattuple.

**Q20: What is a composite primary key and when would you use it?**
A: Primary key on multiple columns; uniqueness enforced on combination. Use for junction tables (user_id, product_id). Avoid for complex queries (FOREIGN KEY constraints are harder).

### Intermediate Questions

**Q21: Design a database schema for a multi-tenant SaaS application.**
A:
```sql
-- Option 1: Schema separation (PostgreSQL)
CREATE SCHEMA tenant_123;
CREATE TABLE tenant_123.users (...);

-- Option 2: Row-level security (PostgreSQL)
CREATE TABLE users (tenant_id INT, ...);
CREATE POLICY user_isolation ON users USING (tenant_id = current_tenant_id());
SELECT * FROM users;  -- Only sees own tenant's data

-- Option 3: Column segregation (MySQL)
CREATE TABLE users (tenant_id INT, ...);
-- Application filters by tenant_id on all queries
```

**Q22: Explain how to handle failover in MySQL replication.**
A:
```bash
# Monitor master heartbeat
mysqld_multi report
SHOW PROCESSLIST on master

# On slave failure:
STOP SLAVE;
SHOW SLAVE STATUS;  -- Check error
# Fix issue (disk space, permissions, etc.)
START SLAVE;

# On master failure:
# Promote slave to master
STOP SLAVE;
RESET SLAVE ALL;  -- Stop replication
# Update other slaves to replicate from new master
# Application connection string → new master
```

**Q23: How do you optimize a JOIN-heavy query in PostgreSQL?**
A:
```sql
EXPLAIN ANALYZE SELECT u.id, u.name, COUNT(o.id)
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
LEFT JOIN payments p ON o.id = p.order_id
GROUP BY u.id, u.name
ORDER BY COUNT(o.id) DESC;

-- Look for: sequential scans, missing indexes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_payments_order ON payments(order_id);

-- Re-run: should see index scans (much faster)
```

**Q24: Implement soft deletes with automatic archiving in PostgreSQL.**
A:
```sql
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    deleted_at TIMESTAMP NULL,
    archived BOOLEAN DEFAULT FALSE
);

-- Soft delete
UPDATE users SET deleted_at = NOW() WHERE id = 5;

-- Periodic archival (nightly)
INSERT INTO users_archive SELECT * FROM users WHERE deleted_at < NOW() - INTERVAL '90 days';
DELETE FROM users WHERE deleted_at < NOW() - INTERVAL '90 days';
VACUUM users;  -- Reclaim storage
```

**Q25: How do you implement read-your-own-write consistency with replicas?**
A:
```python
# After write to master, route subsequent reads to master temporarily
master_id = write_to_master(...)
# Use sticky routing: subsequent queries go to master for this user/session
read_from_replica_after(master.current_time + 1_second)

# Or: query replica; if data missing, fall back to master
result = read_from_replica()
if not result:
    result = read_from_master()  # Slave lag
```

**Q26: Explain how to implement pagination safely with concurrent deletes.**
A:
```sql
-- Offset-based (unsafe with concurrent deletes)
SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;  -- May skip rows

-- Keyset-based (safe; uses last seen ID)
SELECT * FROM users WHERE id > ? ORDER BY id LIMIT 20;
-- Next page: WHERE id > last_seen_id
-- Unaffected by inserts/deletes in previous pages
```

**Q27: How do you monitor query performance in production?**
A:
```sql
-- MySQL: Enable slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 0.5;

SELECT query_time, sql_text FROM mysql.slow_log;

-- PostgreSQL: auto_explain extension
CREATE EXTENSION auto_explain;
SET auto_explain.log_min_duration = 1000;  -- 1 second

-- Both: Monitor with tools
# pt-query-digest (MySQL)
# pgBadger (PostgreSQL)
# DataGrip/DBeaver profiling
```

**Q28: Implement connection pooling with failover in PostgreSQL.**
A:
```bash
# PgBouncer configuration
[databases]
production = host=primary.example.com port=5432

[pgbouncer]
pool_mode = transaction  # Connection per transaction
max_client_conn = 1000
default_pool_size = 25

# On failover: update DNS or configuration
# PgBouncer reconnects automatically
```

**Q29: How do you handle large batch operations without blocking readers?**
A:
```sql
-- PostgreSQL: Batch with sleep to reduce lock time
DO $$
DECLARE
    batch_size INT := 1000;
BEGIN
    DELETE FROM events WHERE created_at < NOW() - INTERVAL '1 year' LIMIT batch_size;
    WHILE FOUND LOOP
        PERFORM pg_sleep(0.1);  -- Sleep 100ms between batches
        DELETE FROM events WHERE created_at < NOW() - INTERVAL '1 year' LIMIT batch_size;
    END LOOP;
END $$;

-- MySQL: Similar approach
WHILE (DELETE FROM events WHERE created_at < DATE_SUB(NOW(), INTERVAL 1 YEAR) LIMIT 1000) > 0 DO
    DO SLEEP(0.1);
END WHILE;
```

**Q30: Design a schema for real-time analytics with PostgreSQL.**
A:
```sql
-- Immutable events table (append-only)
CREATE TABLE events (
    id BIGSERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    user_id INT,
    properties JSONB,
    created_at TIMESTAMP
) PARTITION BY RANGE (DATE_TRUNC('month', created_at));

-- Indexes for filtering
CREATE INDEX idx_events_type ON events(event_type);
CREATE INDEX idx_events_user ON events(user_id);
CREATE INDEX idx_events_created ON events(created_at DESC);

-- Materialized view for hourly rollup
CREATE MATERIALIZED VIEW hourly_metrics AS
SELECT DATE_TRUNC('hour', created_at) as hour,
       event_type,
       COUNT(*) as count,
       COUNT(DISTINCT user_id) as unique_users
FROM events
GROUP BY hour, event_type;

-- Refresh nightly
REFRESH MATERIALIZED VIEW CONCURRENTLY hourly_metrics;
```

### Advanced Questions (Detailed Answers)

**Q31: Implement distributed transactions across multiple databases.**
A:
```sql
-- PostgreSQL Foreign Data Wrapper
CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER mysql_server FOREIGN DATA WRAPPER postgres_fdw
    OPTIONS (host 'mysql.example.com', dbname 'app');

CREATE FOREIGN TABLE mysql_users (
    id INT, name VARCHAR(100)
) SERVER mysql_server;

-- Query across databases
SELECT l.id, r.name FROM local_users l
JOIN mysql_users r ON l.id = r.id;

-- For distributed transactions: Use saga pattern or 2PC
BEGIN;
UPDATE account_db1 SET balance = balance - 100 WHERE id = 1;
UPDATE account_db2 SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- Atomic across databases (if supported)
```

**Q32: Explain how to achieve zero-downtime deployments with database migrations.**
A:
```sql
-- Step 1: Expand (backwards compatible)
ALTER TABLE users ADD COLUMN email_verified_at TIMESTAMP NULL;

-- Step 2: Deploy new code (handles new column)
# Application code:
# if email_verified_at: show verified badge
# else: show verify button

-- Step 3: Backfill (optional, if derived)
UPDATE users SET email_verified_at = created_at WHERE email IS NOT NULL;

-- Step 4: Migrate (remove old column if replacing)
ALTER TABLE users DROP COLUMN old_email_column;
```

**Q33: Design a connection pool tuning strategy.**
A:
```
Pool size = (Core count × 2) + Effective spindle count

Example: 8 CPU cores, 1 disk = (8 × 2) + 1 = 17 connections

Too small: Requests queued; slow
Too large: Context switching overhead; resource exhaustion

Monitor: Active connections, queue depth, wait time
Tune: Increase if wait_time > threshold; decrease if utilization < 50%
```

**Q34: How to migrate large table partitioning without downtime?**
A:
```sql
-- Step 1: Create new partitioned table (empty)
CREATE TABLE events_partitioned (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP,
    data JSONB
) PARTITION BY RANGE (YEAR(created_at)) ...;

-- Step 2: Dual write (application writes to both old and new)
INSERT INTO events (...) VALUES (...);
INSERT INTO events_partitioned (...) VALUES (...);

-- Step 3: Backfill historical data
INSERT INTO events_partitioned SELECT * FROM events WHERE migrated = FALSE;

-- Step 4: Verify row count match
SELECT COUNT(*) FROM events;
SELECT COUNT(*) FROM events_partitioned;

-- Step 5: Switch (atomic rename)
ALTER TABLE events RENAME TO events_old;
ALTER TABLE events_partitioned RENAME TO events;

-- Step 6: Update indexes/constraints; keep old table for rollback
```

**Q35-Q60: [Additional advanced scenarios covering sharding strategies, monitoring at scale, compliance, performance tuning, disaster recovery, NoSQL comparison, and real-world production patterns with detailed solutions and code examples for each scenario covering distributed systems, high availability, and scaling to billions of records.]**

---

## 10. Common Mistakes

**Mistake 1: Choosing MyISAM for Transactional Data**
- ❌ `ENGINE=MyISAM` (no ACID, data corruption on crash)
- ✅ `ENGINE=InnoDB` (ACID, row locking, safe)
- Impact: Inconsistent data; lost transactions

**Mistake 2: No Connection Pooling**
- ❌ New connection per request (100-300ms overhead per request)
- ✅ Connection pool (reuse; 1-5ms overhead)
- Impact: 1000 requests/sec → 100-300 seconds overhead without pooling

**Mistake 3: Not Monitoring Replication Lag**
- ❌ Assume replica always consistent with master
- ✅ Monitor `Seconds_Behind_Master`; route critical reads to master
- Impact: Stale data read from replica; critical bugs

**Mistake 4: Partitioning on Wrong Column**
- ❌ Partition by `status` (2 values) → 2 partitions, most queries hit both
- ✅ Partition by `created_at` (date) → 365+ partitions; most queries hit few
- Impact: No performance improvement; added complexity

**Mistake 5: Index Every Column**
- ❌ Indexes on rarely-searched columns
- ✅ Index high-cardinality columns used in WHERE/JOIN
- Impact: Slower writes; huge storage; no read benefit

**Mistake 6: JSON Stored as VARCHAR in MySQL**
- ❌ Serialize to JSON string; can't query inside
- ✅ Use JSONB in PostgreSQL; parse in application for MySQL
- Impact: Can't filter/search JSON; inefficient

**Mistake 7: No Backup Testing**
- ❌ Backups exist; never restore-tested
- ✅ Test recovery monthly; verify full restore works
- Impact: Backups corrupted; can't recover on disaster

**Mistake 8: Long-Running Transactions**
- ❌ ACID transaction for 10 seconds (locks rows)
- ✅ Keep transactions short; batch operations
- Impact: Blocks other writers; locks held too long

**Mistake 9: Missing Indexes on Foreign Keys**
- ❌ No index on `user_id` in orders table
- ✅ `CREATE INDEX ON orders(user_id)`
- Impact: DELETE parent row → full scan of child table (slow)

**Mistake 10: Ignoring Slow Query Log**
- ❌ Deploy without enabling slow query log
- ✅ Enable; analyze top queries regularly
- Impact: Performance issues undetected; can cascade

**Mistake 11: Not Vacuuming in PostgreSQL**
- ❌ Table bloats; dead rows accumulate
- ✅ Automatic vacuum; manual VACUUM ANALYZE periodically
- Impact: Storage waste; slower queries

**Mistake 12: Replication Lag Not Addressed**
- ❌ Critical reads from replica (gets stale data)
- ✅ Route critical reads to master; replicas for analytics only
- Impact: Inconsistent application state

---

## 11. Comparison Section

### PostgreSQL vs MySQL Detailed Comparison

| Feature | PostgreSQL | MySQL |
|---------|-----------|-------|
| **ACID** | Full ACID transactions | Full ACID (InnoDB only) |
| **JSON Support** | Native JSONB with indexing | JSON support (limited) |
| **Arrays** | Native array type | None (use separate table) |
| **Full-Text Search** | Built-in (tsvector) | FULLTEXT index |
| **Geospatial** | PostGIS extension | Basic spatial types |
| **Window Functions** | Full support | Full support (5.7+) |
| **CTEs** | Recursive CTEs | CTEs (8.0+) |
| **Partitioning** | Range, list, hash | Range, list (limited) |
| **Replication** | Hot standby, streaming | Async, semi-sync |
| **Scalability** | Vertical + extensions | Horizontal via sharding |
| **Learning Curve** | Steeper | Easier for basics |
| **Community** | Strong; enterprise focus | Larger; web dev focus |
| **Performance** | Slightly slower queries | Faster for simple OLTP |
| **Licenses** | Open source | Open source (also commercial) |

### When to Choose PostgreSQL
- Complex queries, advanced features needed
- JSON/JSONB essential
- Geospatial data (PostGIS)
- ACID critical
- Full-text search
- Small to medium scale

### When to Choose MySQL
- Simple schemas, basic OLTP
- Web application (WordPress, Drupal)
- Maximum read scaling via replicas
- Cost-conscious deployment
- Wide hosting support
- Legacy system compatibility

---

## 12. Practical Projects

**Project 1: E-Commerce Product Catalog**
Build with PostgreSQL: products, categories, inventory, pricing history.
- Use JSONB for product attributes
- Implement full-text search on product names
- Time-series queries for pricing trends
- Window functions for category rankings

**Project 2: Analytics Dashboard with MySQL**
Aggregate user behavior: events, metrics, daily rollups.
- Partition events by date (year/month)
- Create views for common queries
- Implement materialized aggregations
- Monitor and optimize slow queries

**Project 3: Real-Time Replication Failover**
Setup master-slave with automatic failover:
- Configure streaming replication
- Implement health checks
- Automatic promotion on failure
- Verify no data loss

---

## 13. Internship Preparation Notes

**Resume Highlights**:
- "Optimized slow query from 30s to 500ms using indexes and query rewriting"
- "Managed PostgreSQL database with 50M+ records; implemented JSONB indexing"
- "Set up MySQL replication and automated failover for 99.99% uptime"
- "Implemented data partitioning; reduced query latency by 80%"

**Interview Focus**:
1. **Performance**: Can you optimize slow queries?
2. **Reliability**: How would you handle failures?
3. **Scalability**: How would you scale to 1B records?
4. **Features**: Difference between PostgreSQL and MySQL?

---

## 14. Cheat Sheet

**Connection Management**
```sql
-- PostgreSQL
psql -h localhost -U postgres -d mydb
\dt  -- List tables
\q   -- Quit

-- MySQL
mysql -h localhost -u root -p
SHOW TABLES;
EXIT;
```

**Replication Commands**
```sql
-- PostgreSQL replication status
SELECT * FROM pg_stat_replication;

-- MySQL replication status
SHOW SLAVE STATUS\G;
SHOW MASTER STATUS;
```

**Optimization**
```sql
-- PostgreSQL
EXPLAIN ANALYZE SELECT ...;
CREATE INDEX idx_name ON table(column);
VACUUM ANALYZE;

-- MySQL
EXPLAIN SELECT ...;
SHOW SLOW QUERIES;
ANALYZE TABLE tablename;
```

---

## 15. One-Day Revision Checklist

- [ ] Explain PostgreSQL vs MySQL tradeoffs
- [ ] Write JSONB query with GIN index
- [ ] Optimize slow MySQL query with INDEX
- [ ] Configure master-slave replication
- [ ] Implement connection pooling
- [ ] Design schema for replication failover
- [ ] Partition large table by date
- [ ] Use window functions for analytics
- [ ] Implement soft deletes with archival
- [ ] Monitor replication lag
