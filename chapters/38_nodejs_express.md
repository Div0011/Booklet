# 38. Node.js & Express (Asynchronous Runtime & API Design)

## 1. Introduction

### What it is
Node.js is an open-source, cross-platform, single-threaded JavaScript runtime environment built on Chrome's V8 engine. It allows developers to execute JavaScript on the server. Express.js is a minimal, flexible web application framework for Node.js that provides routing, middleware, and request/response abstraction layers.

### Why it exists
Historically, web servers (like Apache) allocated a dedicated thread for every client request. When concurrency scaled, the system ran out of threads, freezing the server. Ryan Dahl created Node.js in 2009 to implement an event-driven, non-blocking I/O model. By delegating input/output tasks to the operating system kernel, Node.js handles thousands of concurrent client requests on a single execution thread.

### Problems it solves
- **Thread Exhaustion**: Eliminates thread creation overhead by processing client events inside a single loop thread.
- **API Complexity**: Express provides simple abstractions for HTTP verb routing, headers parsing, and payload parsing.
- **Language Fragmentation**: Enables JavaScript to run on both the client and server (Full-Stack JS), allowing code sharing.

### Industry Use Cases
- **Real-Time Web Services**: Powers chat servers, collaboration tools, and live dashboards using WebSockets.
- **RESTful API Gateways**: Orchestrates requests between clients and microservices.
- **Streaming Servers**: Streams video, audio, or large files memory-efficiently.

---

## 2. Core Concepts

### Beginner Concepts
- **CommonJS vs. ES Modules**:
  - **CommonJS (Default in Node)**: Uses `require()` and `module.exports`. Synchronous loading.
  - **ES Modules**: Uses `import` and `export`. Asynchronous loading. Requires `"type": "module"` in `package.json`.
- **Basic HTTP Server**: Creating an API using Node's native `http` module:
  ```javascript
  const http = require('http');
  const server = http.createServer((req, res) => {
      res.writeHead(200, { 'Content-Type': 'text/plain' });
      res.end('Hello from Node.js!');
  });
  server.listen(3000);
  ```
- **Express App Basics**: Routing API requests with Express:
  ```javascript
  const express = require('express');
  const app = express();
  app.use(express.json()); // Middleware to parse JSON request bodies
  app.get('/api/users', (req, res) => res.json({ id: 1 }));
  app.listen(3000);
  ```

### Intermediate Concepts
- **Request Parameters**:
  - `req.params`: Route parameters (e.g. `/users/:id` $\to$ `/users/12` yields `{ id: "12" }`).
  - `req.query`: Query parameters (e.g. `/search?q=books` yields `{ q: "books" }`).
  - `req.body`: Parses payload data sent in the request body.
- **The Middleware Lifecycle**: Middleware functions are blocks that have access to the request (`req`), response (`res`), and the next middleware function in the application's request-response cycle (`next()`).
- **Unified Error Handling**: In Express, any middleware that accepts 4 parameters `(err, req, res, next)` is designated as an error handler.

### Advanced Concepts
- **Node.js Streams**: Data objects processed chunk-by-chunk in memory, avoiding loading massive datasets into RAM.
- **Worker Threads and Clusters**:
  - **Cluster**: Spawns multiple child processes sharing the same port to distribute network requests across multiple CPU cores.
  - **Worker Threads**: Executes heavy CPU-bound computations in separate threads, keeping the main thread free.
- **The Libuv Thread Pool**: Node delegates asynchronous tasks (like filesystem reads, cryptography, or DNS lookups) to Libuv's thread pool (default size is 4), which interacts with the OS kernel.

---

## 3. Internal Working

### The Node.js Event Loop and Libuv Architecture

Node.js executes JavaScript code inside V8, but delegates asynchronous operations to **Libuv**:

```text
[ JS Source Code ] -> V8 Engine
                         |
  +------------------ Node.js Bindings / Runtime ------------------------+
  |                                                                      |
  |  [ Libuv System ]  ---> Manages Event Loop & Thread Pool (C++)       |
  |                                                                      |
  |  +-- [ Libuv Event Loop Phases ] ---------------------------------+  |
  |  |                                                                |  |
  |  |  1. Timers Phase          ---> Executes setTimeout/Interval    |  |
  |  |  2. Pending I/O Phase     ---> Executes deferred OS callbacks  |  |
  |  |  3. Idle/Prepare Phase    ---> Internal operations             |  |
  |  |  4. Poll Phase            ---> Waits for network connections   |  |
  |  |  5. Check Phase           ---> Executes setImmediate           |  |
  |  |  6. Close Phase           ---> Executes 'close' event callbacks|  |
  |  |                                                                |  |
  |  |  * process.nextTick / Promise callbacks run between phases     |  |
  |  +----------------------------------------------------------------+  |
  |                                                                      |
  |  [ Thread Pool ]   ---> Handles fs operations, crypto, bcrypt        |
  +----------------------------------------------------------------------+
```

1. **Non-Blocking I/O Delegation**:
   - When Node.js executes a non-blocking operation (e.g. `fs.readFile`), it does not wait for the disk to read the file.
   - Instead, it passes the task to Libuv, along with a JavaScript callback function.
   - Libuv delegates the task to the operating system kernel (or its thread pool if the OS doesn't support async filesystem reads).
   - Once completed, the task pushes the callback to the Event Loop queue.
2. **The Libuv Event Loop Phases**:
   - **Timers**: Executes callbacks scheduled by `setTimeout` and `setInterval`.
   - **Pending Callbacks**: Executes I/O callbacks deferred from the previous loop iteration (e.g. TCP errors).
   - **Idle, Prepare**: Used internally by the runtime.
   - **Poll**: Retrieves new I/O events. The loop blocks here to wait for incoming network requests if there are no pending tasks.
   - **Check**: Executes `setImmediate` callbacks.
   - **Close Callbacks**: Executes cleanup callbacks (e.g. `socket.on('close')`).
3. **Tick Transitions (Microtasks)**:
   - Between each phase of the Libuv event loop, Node.js flushes its microtask queues:
     - **`process.nextTick()` queue**: Handled first (highest priority).
     - **Promise queue**: Handled after `nextTick`.

---

## 4. Important Terminology

- **Libuv**: The C++ library that powers Node.js event-driven, asynchronous features, including the thread pool and the event loop.
- **Streams**: Pipelines for reading and writing data in chunks to optimize memory footprint.
- **Middleware**: Functions in Express that execute sequentially during the request-response cycle.
- **Event Loop**: The loop mechanism that coordinates asynchronous task queues and executes callbacks.
- **`process.nextTick`**: A Node.js API that schedules a callback to be run immediately after the current operation finishes, before the event loop continues to the next phase.

---

## 5. Beginner Examples

### Example 1: Basic Express Router with JSON Payload Parsing
This example demonstrates setting up an Express server with routes, query inputs, and JSON body parsing.

```javascript
const express = require('express');
const app = express();

// Parse JSON request payloads
app.use(express.json());

// 1. GET request query input (/api/greet?name=Developer)
app.get('/api/greet', (req, res) => {
    const name = req.query.name || "Guest";
    res.status(200).json({ message: `Hello, ${name}!` });
});

// 2. POST request body payload validation
app.post('/api/users', (req, res) => {
    const { username, email } = req.body;
    if (!username || !email) {
        return res.status(400).json({ error: "Username and email are required" });
    }
    
    // Simulate database insert
    res.status(201).json({ id: 101, username, email });
});

app.listen(3000, () => console.log("Server running on port 3000"));
```

---

## 6. Intermediate Examples

### Example 1: Custom Validation and Error Middleware
This example implements custom validation middleware and a centralized error-handling middleware.

```javascript
const express = require('express');
const app = express();
app.use(express.json());

// 1. Authentication Check Middleware
function authenticateToken(req, res, next) {
    const authHeader = req.headers['authorization'];
    if (!authHeader) {
        // Pass error to error-handling middleware
        const err = new Error("Unauthorized access token missing");
        err.status = 401;
        return next(err); 
    }
    next(); // Pass control to the next middleware or route handler
}

// 2. Protected Route
app.get('/api/secure-data', authenticateToken, (req, res) => {
    res.json({ secret: "This is secure data." });
});

// 3. Custom Error-Handling Middleware (Must have 4 parameters)
app.use((err, req, res, next) => {
    console.error("Centralized Error Log:", err.message);
    
    const statusCode = err.status || 500;
    res.status(statusCode).json({
        status: "error",
        message: err.message || "Internal Server Error"
    });
});

app.listen(3000);
```

---

## 7. Advanced Concepts

### Node.js Memory Performance Optimizations

#### Handling Large Files using Streams
Loading large files into memory using `fs.readFile` allocates a buffer of the same size in RAM, which can crash the server if multiple users download the file at the same time. Using Streams resolves this:

```javascript
const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();

app.get('/download-large-video', (req, res) => {
    const filePath = path.join(__dirname, 'large-video.mp4');
    
    // BAD: fs.readFile loads the entire file into RAM before sending it:
    // fs.readFile(filePath, (err, data) => res.send(data));

    // GOOD: Read and send the file chunk-by-chunk using a Stream:
    const readStream = fs.createReadStream(filePath);
    
    // Stream pipes chunks directly to the response buffer as they are read from disk
    readStream.pipe(res);

    readStream.on('error', (err) => {
        res.status(500).send("File read error");
    });
});

app.listen(3000);
```

### Celery & Redis Distributed Task Queues
Distributed background tasks are essential for offloading long-running operations (like machine learning predictions, video encoding, or bulk mail sends) from web servers to isolated worker pools.

* **Redis as a Broker**: In both environments, Redis serves as an in-memory transport broker. Producers write task payloads to Redis lists, and consumers poll/pop payloads using blocking commands (like `BRPOP`).
* **Node.js (BullMQ + Redis)**: Native Node task manager. Utilizes JavaScript event loops to process jobs asynchronously. Best for I/O-intensive task suites.
* **Python (Celery + Redis)**: Multi-process task manager. Spawns dedicated OS worker processes, making it highly optimized for CPU-bound computations and ML pipelines.

#### Code Example: Celery Task Definition and Client Invocation
This code shows a Python Celery application using Redis as the message broker and result backend.

```python
# tasks.py (Worker Process)
# Run with: celery -A tasks worker --loglevel=info
from celery import Celery
import time

# 1. Initialize Celery with Redis broker and backend
app = Celery(
    'tasks',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

# 2. Define a background task
@app.task
def process_data_payload(data_list):
    print("Initiating heavy CPU processing task...")
    time.sleep(5)  # Simulate 5-second computation
    result = sum(data_list)
    return {"status": "success", "result": result}

# client.py (Application Producer calling the task)
# from tasks import process_data_payload
# 
# # Trigger task asynchronously (returns immediately)
# task_result = process_data_payload.delay([10, 20, 30, 40])
# print(f"Task queued. ID: {task_result.id}")
# 
# # Poll for status
# while not task_result.ready():
#     print("Task in progress...")
#     time.sleep(1)
# 
# print("Result:", task_result.result)
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate your understanding of asynchronous runtime execution. They want to see if you can explain how the Libuv event loop works, handle asynchronous route errors in Express, process file data memory-efficiently using streams, and run CPU-heavy tasks without blocking the server.

### Red Flags
- **Blocking the Event Loop**: Executing synchronous CPU-bound operations (e.g. `fs.readFileSync` or deep nested loops) inside route handlers, which blocks all concurrent requests.
- **Forgetting `next()`**: Writing middleware that does not call `next()` or return a response, leaving the client request hanging indefinitely.
- **Unhandled Promise Rejections**: Writing asynchronous Express routes without `try/catch` wrappers. If an async operation throws an error, Express will not catch it, causing the Node process to crash.

### Green Flags
- **Centralized Error Handling**: Routing errors to a 4-parameter error-handling middleware instead of writing duplicate error logs in every handler.
- **Streams Integration**: Using readable/writable streams to process heavy files memory-efficiently.
- **Worker Thread Execution**: Proposing worker threads or child processes to handle CPU-bound tasks.

### Answers Matrix

| Level | Question: "How does Node.js handle concurrent requests if it is single-threaded?" |
|---|---|
| **Rejected** | "Node.js uses multi-threading behind the scenes to process requests in parallel." |
| **Shortlisted** | "Node.js runs Javascript on a single thread. When it queries a database or filesystem, it delegates the task to the operating system and processes other requests, running the callbacks when ready." |
| **Selected** | "Node.js uses a single execution thread for JavaScript execution, running on an event-driven loop. When an asynchronous I/O operation (like a database query or network request) is initiated, Node delegates the task to Libuv. Libuv interacts with the OS kernel or uses its thread pool to process the task asynchronously in the background. Meanwhile, the main thread continues processing other incoming requests. Once the I/O task completes, Libuv pushes the callback to the event loop's task queue, and V8 executes it when the call stack is empty. This allows Node to handle high concurrency with minimal resource overhead." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is the difference between `setImmediate()` and `setTimeout(fn, 0)`?
- **Detailed Answer**: Both APIs are used to schedule callbacks to run after the current operation finishes, but they run in different phases of the event loop:
  - **`setTimeout(fn, 0)`**: Scheduled in the **Timers Phase**. It requires the runtime to check if the timer threshold has been reached.
  - **`setImmediate(fn)`**: Scheduled in the **Check Phase**, which runs immediately after the Poll phase completes.
  - **Execution Order**: If called from the main thread, the execution order is non-deterministic and depends on the system performance. However, if called inside an I/O cycle (e.g., inside `fs.readFile`), `setImmediate` is guaranteed to execute first because the Check phase follows the Poll phase.
- **Follow-up Questions**: How does `process.nextTick` compare to these? (Answer: `process.nextTick` is not part of the Libuv event loop. It executes immediately after the current operation finishes, before moving to the next phase of the event loop).
- **Interviewer's Expectations**: Distinguish between Timers and Check phases, and explain I/O loop ordering.

#### 2. What is the Libuv thread pool size, and how do you customize it?
- **Detailed Answer**:
  - Libuv handles file system, cryptography (`crypto`), compression (`zlib`), and DNS lookup operations using a thread pool because these operations are blocking on the OS level.
  - The default thread pool size is **4**.
  - We can customize the pool size up to **1024** by setting the environment variable before starting the Node process:
    ```bash
    export UV_THREADPOOL_SIZE=64
    ```
- **Follow-up Questions**: Why not set the thread pool size to 1024 on every server? (Answer: Setting it too high can cause high CPU context-switching overhead, degrading performance).
- **Interviewer's Expectations**: Identify blocking operations that rely on the thread pool and specify how to set environment parameters.

---

### Scenario-Based Questions

#### 3. You need to implement a CPU-intensive image compression service in Express. How do you prevent it from freezing requests?
- **Detailed Answer**:
  - Since Node.js is single-threaded, running image compression directly in a route blocks the event loop, freezing the server for all other users.
  - **Solutions**:
    1. **Worker Threads**: Offload the compression calculations to a separate thread:
       ```javascript
       const { Worker } = require('worker_threads');
       app.post('/compress', (req, res) => {
           const worker = new Worker('./compress-worker.js', { workerData: req.body.image });
           worker.on('message', (data) => res.json(data));
       });
       ```
    2. **Child Process**: Spawn a child process to run an external script (like Python or C++).
    3. **Task Queue**: Move the task to an external background worker queue (like Celery or BullMQ) backed by Redis.
- **Follow-up Questions**: Why are worker threads preferred over child processes for simple JS tasks? (Answer: Worker threads share memory, making data transfer faster and consuming fewer resources than spawning child processes).
- **Interviewer's Expectations**: Propose worker threads, child processes, or external queues, and explain why they prevent event loop blocking.

#### 4. How do you prevent a Node.js API server from crashing when an asynchronous operation throws an error inside an Express route?
- **Detailed Answer**:
  - By default, Express 4 does not catch errors thrown inside asynchronous routes (`async/await`). If an error is thrown and not caught, it results in an unhandled promise rejection, crashing the Node process.
  - **Solutions**:
    1. **Wrap routes in try/catch blocks** and pass the error to `next(err)`:
       ```javascript
       app.get('/users', async (req, res, next) => {
           try {
               const users = await db.fetch();
               res.json(users);
           } catch (error) {
               next(error); // Route to error handler
           }
       });
       ```
    2. **Use a wrapper helper** to catch errors automatically:
       ```javascript
       const asyncHandler = fn => (req, res, next) => {
           Promise.resolve(fn(req, res, next)).catch(next);
       };
       app.get('/users', asyncHandler(async (req, res) => { ... }));
       ```
- **Follow-up Questions**: Does Express 5 change this behavior? (Answer: Yes. Express 5 automatically catches rejected promises and routes them to the error handler).
- **Interviewer's Expectations**: Explain unhandled promise rejection crashes and implement a route wrapper or try/catch blocks.

---

### Debugging Questions

#### 5. Debug the following code which crashes the server when a file is missing, instead of returning an error response:
```javascript
app.get('/read-config', (req, res) => {
    fs.readFile('/non-existent-path.json', 'utf8', (err, data) => {
        if (err) {
            throw err; // Crashes the server
        }
        res.send(data);
    });
});
```
- **Detailed Answer**: The issue is using `throw err` inside an asynchronous callback function. Because the callback executes in a different execution context on the event loop, Express's routing context cannot catch it, causing the Node process to crash.
- **Fix**: Handle the error by sending a response or routing it to the centralized error handler:
  ```javascript
  app.get('/read-config', (req, res, next) => {
      fs.readFile('/non-existent-path.json', 'utf8', (err, data) => {
          if (err) {
              err.status = 404;
              return next(err); // Safe routing to error-handling middleware
          }
          res.send(data);
      });
  });
  ```
- **Follow-up Questions**: Why is it best practice to return when calling `next()`? (Answer: To prevent the code below from executing, which could cause header write conflict errors).
- **Interviewer's Expectations**: Describe asynchronous callback limits and use `next(err)` to handle errors.

---

### System Design Questions

#### 6. Design a secure file upload service in Node.js.
- **Detailed Answer**:
  - We use a multipart parser middleware like **Multer** to parse incoming files.
  - To prevent memory exhaustion, we stream file chunks directly to a storage bucket (like AWS S3) instead of storing the files in memory or writing them to local disk first:
    ```javascript
    const multer = require('multer');
    const multerS3 = require('multer-s3');
    const upload = multer({ storage: multerS3({ s3: s3Instance, bucket: 'uploads' }) });
    ```
  - We validate file types using magic bytes (inspecting file signatures) rather than relying on file extensions, and enforce strict file size limits to prevent Denial of Service (DoS) attacks.
- **Follow-up Questions**: What is a magic byte check? (Answer: Inspecting the first few bytes of a file to verify its true format, preventing users from renaming a `.exe` file to `.jpg`).
- **Interviewer's Expectations**: Cover streaming uploads, file size limits, and security checks.

---

### Real Interview Questions

#### 7. What is the difference between `process.nextTick` and `setImmediate`?
- **Detailed Answer**:
  - `process.nextTick` executes immediately after the current operation finishes, before moving to the next phase of the event loop.
  - `setImmediate` schedules execution in the Check phase of the Event Loop, running after the Poll phase.
  - Consequently, `process.nextTick` executes before `setImmediate`. If called recursively, `process.nextTick` will block the event loop, starving I/O requests.
- **Follow-up Questions**: Why does recursive execution of `setImmediate` not block the event loop? (Answer: Because `setImmediate` yields back control after executing one callback per loop check phase).
- **Interviewer's Expectations**: Explain timing differences and event loop starvation risks.

---

## 10. Common Mistakes

- **Blocking the event loop with sync operations**: Using methods like `fs.readFileSync` or `JSON.parse` on large files inside requests, which halts the event loop for all users.
- **Confusing ES Modules and CommonJS syntax**: Mixing `require` and `import` syntax in the same file without configuring `package.json`.
- **Not terminating requests inside middleware**: Forgetting to call `next()` or send a response inside middleware, leaving requests hanging.

---

## 11. Comparison Section: Asynchronous Sizing and Timers

| Function / Strategy | `process.nextTick` | `setImmediate` | `setTimeout` |
|---|---|---|---|
| **Phase Location** | Between phases (immediate). | Check Phase. | Timers Phase. |
| **I/O Priority** | High (can starve I/O). | Medium. | Low (depends on timer threshold). |
| **Execution Context** | Runs before next tick. | Runs after Poll phase. | Runs after timer expires. |
| **Ideal Use Case** | Clearing buffers or running callbacks instantly before loop transitions. | Running tasks immediately after I/O cycles. | Scheduling tasks after a specified delay. |

---

## 12. Practical Project Ideas

### Beginner
- **Contact API Server**: Build an Express API server with CRUD routes to manage contacts, validating request payloads and returning proper HTTP status codes.

### Intermediate
- **Rate-Limiter Middleware**: Build a custom Express rate-limiter middleware using Redis to track client request timestamps.

### Advanced/Resume-worthy
- **Streaming Media Portal**: Create a video streaming server using Node.js streams. Support range queries (`HTTP range headers`) to let clients stream parts of videos dynamically, keeping RAM footprint minimal.

---

## 13. Internship Preparation Notes

- **Recruiters Focus on**: Core Express routing, request headers, JSON body parsing, and simple callbacks.
- **Product Companies Expect**: Understanding of the Event Loop phases, non-blocking I/O delegation, streams, worker threads, and centralized error-handling.
- **Data Pipelines Integration**: Be ready to explain how Node.js streams process large datasets memory-efficiently.

---

## 14. Cheat Sheet

- **JSON Body Middleware**: `app.use(express.json());`
- **Centralized Error Handler template**:
  ```javascript
  app.use((err, req, res, next) => {
      res.status(err.status || 500).json({ error: err.message });
  });
  ```
- **Increase Thread Pool Size**: `process.env.UV_THREADPOOL_SIZE = 64;`
- **Stream Piping**: `readStream.pipe(writeStream);`

---

## 15. One-Day Revision Guide

- [ ] Trace the execution order of `setTimeout`, `setImmediate`, and `process.nextTick`.
- [ ] Understand why synchronous filesystem methods should not be used in route handlers.
- [ ] Implement a custom Express middleware from memory.
- [ ] Explain how Node.js pipes data memory-efficiently using streams.
- [ ] Describe the role of Libuv in managing asynchronous event cycles.
