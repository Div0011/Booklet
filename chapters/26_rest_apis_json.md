# 26. REST APIs & JSON (Web Service Interfaces)

## 1. Introduction

### What it is
REST (Representational State Transfer) is an architectural style designed by Roy Fielding in 2000 for building distributed hypermedia systems. It is not a protocol, format, or standard, but a set of architectural constraints (client-server, statelessness, cacheability, uniform interface, layered system, and code-on-demand). JSON (JavaScript Object Notation) is a lightweight, language-independent text format used to represent structured data, serving as the dominant payload serialization format for REST services.

### Why it exists
Prior to REST, web service integration relied on heavy protocols like SOAP (Simple Object Access Protocol) and XML-RPC. These required XML schemas (WSDL) and custom message wrappers, which consumed significant bandwidth and made clients tightly coupled to backend services. REST was introduced to utilize the existing features of the HTTP protocol (caching, status codes, standard verbs, and stateless routing) to provide clean, lightweight, human-readable interfaces, decoupling client applications from backend logic.

### Problems it solves
- **Tight Coupling**: Standardizing URL paths, HTTP verbs, and standard headers separates the frontend presentation from backend data modeling.
- **Payload Verbosity**: JSON replaces XML, reducing payload sizes by up to 50% and lowering network bandwidth costs.
- **Inability to Scale**: The stateless constraint ensures that any request can be handled by any server instance behind a load balancer, enabling horizontal scaling without sharing session state.
- **Inconsistent Interfaces**: RESTful guidelines structure API endpoints, preventing teams from designing arbitrary API methods (e.g., replacing `/getUsers`, `/removeUser` with `/users` and standard GET/DELETE verbs).

### Industry Use Cases
- **Public Developer Platforms**: Companies like Stripe, Twilio, and GitHub expose RESTful APIs to allow third-party integrations.
- **Mobile and Single-Page Web Applications**: React, iOS, and Android applications fetch JSON payloads from backend REST services to dynamically render UI.
- **Microservice Orchestration**: Communication between independent services (e.g., an Order Service requesting data from a User Service).
- **Webhooks**: Servers pushing real-time event notifications (e.g., Stripe notifying a backend that a payment succeeded) using POST requests.

### Analogy
A restaurant menu: The menu is the REST API (standardized interface). The items on the menu are resources (nouns). Your order is the HTTP request (GET = request to see a dish, POST = place an order, DELETE = cancel a dish). The waiter is the HTTP protocol carrying the request. The order slip is the JSON payload containing the custom choices. The kitchen response is the HTTP status code (200 = food ready, 404 = out of stock, 401 = need reservation).

---

## 2. Core Concepts

### Beginner Concepts
- **HTTP Verbs (Methods)**:
  - `GET`: Retrieves a representation of a resource. Safe (does not modify server state) and idempotent (multiple identical requests yield the same result).
  - `POST`: Creates a new resource. Neither safe nor idempotent (running it twice creates two resources).
  - `PUT`: Replaces an existing resource or creates it if it does not exist. Idempotent (repeatedly sending the same replacement payload yields the same state).
  - `PATCH`: Applies partial updates to a resource. Not strictly idempotent (e.g., adding an item to an array).
  - `DELETE`: Removes a resource. Idempotent (subsequent deletes return 404 or 204 but the resource state remains deleted).
- **HTTP Status Codes**:
  - `2xx (Success)`: `200 OK` (generic success), `201 Created` (POST success, includes `Location` header), `204 No Content` (DELETE or PUT success, no body returned).
  - `3xx (Redirection)`: `301 Moved Permanently` (resource has new URL), `304 Not Modified` (client cache is valid).
  - `4xx (Client Error)`: `400 Bad Request` (validation error), `401 Unauthorized` (identity unknown), `403 Forbidden` (identity known, but lacks permissions), `404 Not Found` (resource missing), `429 Too Many Requests` (rate limit hit).
  - `5xx (Server Error)`: `500 Internal Server Error` (uncaught crash), `502 Bad Gateway` (upstream server failed), `503 Service Unavailable` (overloaded or down).
- **URL Structure**: URLs must use nouns representing collections or documents (e.g., `/users` for a collection, `/users/{id}` for a document). Avoid verbs (e.g., `/getUsers`).
- **JSON Data Types**: Strings, numbers, booleans (`true`/`false`), arrays (ordered lists), objects (key-value pairs), and `null`.

### Intermediate Concepts
- **Request Components**: Consists of a Request Line (Method, Path, HTTP Version), Headers (metadata like `Authorization`, `Content-Type`), Query Parameters (`?sort=desc`), and a Request Body (JSON payload).
- **HTTP Headers**:
  - `Content-Type`: Defines the media type of the current request body (e.g., `application/json`).
  - `Accept`: Specifies the media types the client is willing to receive.
  - `Authorization`: Carries credentials (e.g., `Bearer <token>`).
  - `Idempotency-Key`: A unique UUID passed to guarantee safe retries of POST requests.
- **Content Negotiation**: The process where a client and server negotiate the format of data exchanged (e.g., a client sending `Accept: application/xml` forces the server to return XML instead of JSON).
- **Pagination**: Splitting large lists into manageable chunks:
  - **Offset Pagination**: Uses `limit` and `offset` parameters. Easy to write but degrades in performance at high offsets (requires SQL `OFFSET` scans) and suffers from drift (skipped/duplicated items if records are added/deleted).
  - **Cursor Pagination**: Uses a cursor pointing to a specific record (e.g., `starting_after=user_9921`). Fast (uses indexed indexes) and resilient to dataset mutations.
- **Versioning**: Managing changes to the API schema. Done via URL paths (e.g., `/v1/users`), query parameters (e.g., `/users?version=1`), or custom media headers (e.g., `Accept: application/vnd.company.v1+json`).

### Advanced Concepts
- **HATEOAS (Hypermedia As The Engine Of Application State)**: A constraint of REST stating that the server response must return hypermedia links. This allows the client to navigate resources dynamically without hardcoding URLs:
  ```json
  {
    "id": 12,
    "name": "Jane",
    "links": [
      { "rel": "self", "href": "/api/v1/users/12" },
      { "rel": "orders", "href": "/api/v1/users/12/orders" }
    ]
  }
  ```
- **Rate Limiting**: Enforcing thresholds on API calls to prevent Denial of Service (DoS). Implemented using algorithms like Token Bucket (allows bursts), Leaky Bucket (smooths outflow), and Sliding Window Log (precise window checks).
- **Idempotency Keys**: Generates a unique token for transactional operations. The server stores the initial response in a database/cache associated with the key. If a duplicate request arrives, the server returns the cached response instead of re-processing.
- **Webhooks**: An event-driven architecture where a server notifies external clients of state changes via HTTP POST callbacks. Requires signature verification (e.g., using HMAC-SHA256) to ensure the webhook payload was not tampered with.

### Deep-Dive: Flask Core Web Framework
- **Routing & Variable Rules**: Flask uses Werkzeug's routing system to map URLs to view functions. Dynamic variables can be embedded in paths using `<converter:name>`, where converters include `string`, `int`, `float`, `path`, and `uuid` (e.g., `/users/<int:user_id>`).
- **Context Locals**: Flask manages concurrency using local proxy contexts bound to the current thread or greenlet.
  - **Application Context**: Exposes application-level variables like `current_app` (the active application instance) and `g` (a temporary global namespace for a single request).
  - **Request Context**: Exposes request-specific data like `request` (headers, args, form data) and `session` (signed cookie-based user session).
- **Database Session Management**: Flask-SQLAlchemy integrates SQLAlchemy. It binds a scoped session to Flask's request lifecycle. A transaction starts when database actions are called and automatically rolls back if an uncaught exception is raised, with the session closing (`session.remove()`) at request teardown.
- **Modular Blueprints**: Blueprints allow dividing a large Flask application into independent modules. Each blueprint can define its own routing rules, template folders, static paths, and error handlers, registered to the central application object using a common prefix.

---

## 3. Internal Working

### HTTP Request/Response Anatomy
HTTP is a text-based application-layer protocol running over TCP. When a client initiates a request, it opens a TCP connection to the server's port (usually 80 or 443) and transmits raw text matching the HTTP RFC spec.

```text
CLIENT REQUEST RAW TEXT:
----------------------------------------
POST /api/v1/users HTTP/1.1
Host: api.example.com
Authorization: Bearer xyz123
Content-Type: application/json
Content-Length: 35

{"name": "Alice", "role": "admin"}
----------------------------------------

              |
              v TCP Socket Transmission / Server Ingestion
              |

SERVER RESPONSE RAW TEXT:
----------------------------------------
HTTP/1.1 201 Created
Date: Thu, 11 Jun 2026 15:20:00 GMT
Content-Type: application/json
Content-Length: 47
Location: /api/v1/users/8922

{"id": 8922, "name": "Alice", "role": "admin"}
----------------------------------------
```

The server parses this raw text, routes it based on the URL and HTTP verb, executes business logic, and serializes a JSON payload back to the network socket, appending the `Content-Length` header so the client knows when to stop reading the TCP stream.

### RESTful Resource Modeling
REST models APIs around resource hierarchies. Relational structures are mapped directly to URL sub-resources.
- **Collection**: `/api/v1/companies` (Represents the set of all companies).
- **Sub-resource Collection**: `/api/v1/companies/102/employees` (Employees working at company 102).
- **Complex Operations**: REST maps actions to resource states rather than remote procedure calls (RPC). For example, instead of `/cancelInvoice?id=44`, REST uses `POST /api/v1/invoices/44/cancellations` or `PATCH /api/v1/invoices/44` with a body of `{"status": "cancelled"}`.

### Idempotency & Safety Matrix
Safety and Idempotency are mathematically defined properties of HTTP methods:
- **Safety**: $f(x) = x$. A safe request does not mutate resource state.
- **Idempotency**: $f(f(x)) = f(x)$. Running the request $N$ times has the exact same side-effects on the server as running it $1$ time.

| Method | Safe | Idempotent | Side-effects on repeat | Expected Response (1st vs Nth) |
|---|---|---|---|---|
| **GET** | Yes | Yes | None | `200 OK` / `200 OK` |
| **POST** | No | No | Creates duplicate resources | `201 Created` / `201 Created` (Duplicate) |
| **PUT** | No | Yes | Replaces resource (no cumulative change) | `200 OK` or `204` / `200 OK` or `204` |
| **PATCH** | No | No | Depends on operation (e.g. increments) | `200 OK` / `200 OK` (with cumulative updates) |
| **DELETE** | No | Yes | Removes resource (already gone on repeat) | `204 No Content` / `404 Not Found` |

---

## 4. Important Terminology

- **Representational State Transfer (REST)**: An architectural style for distributed hypermedia systems.
- **JSON (JavaScript Object Notation)**: Text-based format for structuring data.
- **Endpoint**: The combination of a URL path and HTTP verb exposing a service.
- **Idempotency**: A property where repeating an API call yields the same server state as a single call.
- **Safe Method**: An HTTP method that does not modify the target resource's server state (e.g. GET).
- **Content Negotiation**: The process of determining the response data format (JSON, XML) using headers.
- **Cursor Pagination**: Fetching data chunks by referencing a unique index key from the last fetched item.
- **Offset Pagination**: Fetching data chunks using a numeric offset (skipping $N$ rows in database).
- **HATEOAS**: REST constraint requiring responses to contain navigational hyperlinks.
- **Rate Limiting**: Throttling client requests to prevent API overload.
- **Token Bucket**: Rate-limiting algorithm allowing bursts by consuming pre-filled tokens from a bucket.
- **Leaky Bucket**: Rate-limiting algorithm smoothing traffic by outputting requests at a constant rate.
- **Sliding Window Log**: Rate-limiting algorithm storing timestamps of all client requests to check bounds.
- **Webhook**: User-defined HTTP callback triggered by events on a server.
- **HMAC Signature**: Hash-based Message Authentication Code used to verify the integrity and origin of webhook events.
- **CORS (Cross-Origin Resource Sharing)**: Browser security mechanism allowing/restricting web page requests to other domains.
- **API Gateway**: Reverse proxy acting as a single entry point to route, rate-limit, and authenticate APIs.
- **Idempotency-Key**: A unique header used to identify and deduplicate repeated requests.
- **Keep-Alive**: Persistent HTTP connection reuse across multiple requests to reduce TCP handshake overhead.
- **Content-Length**: Header specifying the size of the request/response body in bytes.

---

## 5. Beginner Examples

### Example 1: GET Request with curl
Fetching user details with customized headers.
```bash
curl -i -X GET https://api.example.com/v1/users/8821 \
  -H "Accept: application/json" \
  -H "Authorization: Bearer token_abc123"
```
*Expected Output:*
```text
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 64

{"id":8821,"username":"dev_ninja","email":"ninja@example.com"}
```

### Example 2: POST JSON Body
Creating a new user profile by passing a raw JSON payload.
```bash
curl -i -X POST https://api.example.com/v1/users \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"username":"coding_star","email":"star@example.com"}'
```
*Expected Output:*
```text
HTTP/1.1 201 Created
Location: /v1/users/9002
Content-Type: application/json
Content-Length: 66

{"id":9002,"username":"coding_star","email":"star@example.com"}
```

### Example 3: Python Requests Usage
Using Python to query a resource collection with parameters and error handling.
```python
import requests

def get_active_users(api_url: str, token: str) -> list:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }
    params = {
        "status": "active",
        "limit": 10
    }
    
    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=5.0)
        # Raise an exception for 4xx or 5xx status codes
        response.raise_for_status()
        
        # Parse JSON payload
        data = response.json()
        return data.get("users", [])
        
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout:
        print("The request timed out.")
    return []

### Example 4: Basic Flask Application with Custom Routing
Setting up a minimal Flask application with dynamic URL route converters and JSON responses.

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database
USERS = {
    1: {"name": "Alice", "role": "Developer"},
    2: {"name": "Bob", "role": "Designer"}
}

# Dynamic route parameters using type converters
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = USERS.get(user_id)
    if not user:
        # Return JSON error and matching 404 client error code
        return jsonify({"error": "User not found"}), 404
    
    # Return user details with standard 200 OK status
    return jsonify(user), 200

# Route handling request arguments (query parameters)
@app.route("/users", methods=["GET"])
def list_users():
    role_filter = request.args.get("role")
    results = USERS
    if role_filter:
        results = {k: v for k, v in USERS.items() if v["role"].lower() == role_filter.lower()}
    
    return jsonify(list(results.values())), 200

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 6. Intermediate Examples

### Example 1: Cursor-based Pagination Retrieval Loop
Fetching a large list of orders using cursor pagination to prevent offset performance degradation.

```python
import requests
import time

def fetch_all_orders(api_url: str, api_token: str) -> list:
    all_orders = []
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Accept": "application/json"
    }
    
    # Initialize query parameters
    params = {"limit": 100}
    next_cursor = None
    
    while True:
        if next_cursor:
            params["starting_after"] = next_cursor
            
        response = requests.get(f"{api_url}/orders", headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        payload = response.json()
        orders = payload.get("data", [])
        all_orders.extend(orders)
        
        # Check if there are more items using cursor markers
        has_more = payload.get("has_more", False)
        if not has_more or len(orders) == 0:
            break
            
        # Set cursor to the ID of the last item in the list
        next_cursor = orders[-1]["id"]
        time.sleep(0.1) # Rate limiting courtesy delay
        
    return all_orders
```

### Example 2: Retry Handler with Exponential Backoff and Jitter
Handling rate limits (`429 Too Many Requests`) and server timeouts (`503 Service Unavailable`) using robust retry logic.

```python
import requests
import time
import random

def request_with_backoff(url: str, max_retries: int = 5) -> requests.Response:
    base_backoff = 1.0 # 1 second
    
    for attempt in range(max_retries):
        response = requests.get(url, timeout=5)
        
        # If success, return response immediately
        if response.status_code == 200:
            return response
            
        # Handle Rate Limit (429) or Service Unavailable (503)
        if response.status_code in [429, 503]:
            # Inspect response header for recommended retry wait
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                wait_time = float(retry_after)
            else:
                # Exponential Backoff formula: base * 2^attempt
                # Add Full Jitter (randomness) to prevent thundering herd problem
                backoff = base_backoff * (2 ** attempt)
                wait_time = random.uniform(0, backoff)
                
            print(f"Status {response.status_code}. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            continue
            
        # Raise exception for other errors (e.g. 400, 401, 404)
        response.raise_for_status()
        
    raise RuntimeError("Max retries exceeded for service request.")
```

### Example 3: Inbound Request Validation using Pydantic (FastAPI style)
Validating incoming API payloads to enforce type constraints before executing business operations.

```python
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List

class EmployeeCreateSchema(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Legal first and last name")
    email: EmailStr = Field(..., description="Corporate email address")
    role: str = Field(..., description="Assigned engineering role")
    years_experience: int = Field(..., ge=0, le=50, description="Years of experience")
    skills: List[str] = Field(default_factory=list)
    manager_id: Optional[int] = None
    
    # Custom Validator
    @field_validator("role")
    @classmethod
    def validate_role_type(cls, value: str) -> str:
        valid_roles = ["Frontend", "Backend", "Data Scientist", "DevOps"]
        if value not in valid_roles:
            raise ValueError(f"Role must be one of: {valid_roles}")
        return value

# Example Validation Execution:
raw_json_payload = {
    "name": "Jane Doe",
    "email": "jane.doe@company.com",
    "role": "Backend",
    "years_experience": 8,
    "skills": ["Python", "Docker", "SQL"]
}

try:
    validated_employee = EmployeeCreateSchema(**raw_json_payload)
    print("Validation Succeeded. Object:", validated_employee.model_dump())
except ValueError as e:
    print("Validation Failed. Error log:", e)
```

### Example 4: FastAPI Engine - High-Performance Asynchronous Endpoint
This example demonstrates a complete FastAPI implementation featuring Pydantic schemas, dependency injection (using FastAPI's `Depends` system for database sessions), dynamic route parameters, and asynchronous database/network I/O handlers.

```python
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import AsyncGenerator
import httpx
import uvicorn

app = FastAPI(
    title="Employee API Engine",
    description="High-performance backend API featuring asynchronous I/O",
    version="1.0.0"
)

# 1. Input/Output Schemas
class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: str

class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    profile_picture_url: str

# 2. Dependency Injection: Simulate Asynchronous Database Client Setup
async def get_db() -> AsyncGenerator[str, None]:
    db_session = "db_session_connection_pool"
    try:
        # Yield connection to route handler
        yield db_session
    finally:
        # Automatic connection cleanup after response finishes
        pass

# 3. Third-party Asynchronous API Fetch Dependency
async def fetch_avatar_url(email: str) -> str:
    # Use asynchronous HTTP client instead of requests to prevent blocking the event loop
    async with httpx.AsyncClient() as client:
        try:
            # Simulated call to external avatar service
            response = await client.get(f"https://api.adorable.io/avatars/{email}", timeout=2.0)
            return response.url if response.status_code == 200 else "https://api.adorable.io/avatars/default"
        except Exception:
            return "https://api.adorable.io/avatars/default"

# 4. Asynchronous API Handler Route
@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee profile asynchronously"
)
async def create_employee(
    payload: EmployeeCreate,
    db: str = Depends(get_db), # Injected database dependency
):
    # Retrieve avatar asynchronously (non-blocking call)
    avatar_url = await fetch_avatar_url(payload.email)
    
    # Simulate saving to database using async engine
    # await db.execute("INSERT ...")
    
    new_employee = {
        "id": 101,
        "name": payload.name,
        "email": payload.email,
        "role": payload.role,
        "profile_picture_url": avatar_url
    }
    return new_employee

# Command to run locally:
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

### Example 5: Flask CRUD API with Flask-SQLAlchemy
A Flask REST API integrated with SQLAlchemy database schemas to perform CRUD operations.

```python
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure SQLite memory database for testing
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# 1. Model Definition
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author}

# Initialize database tables
with app.app_context():
    db.create_all()

# 2. CRUD Route Handlers
@app.route("/books", methods=["POST"])
def create_book():
    data = request.get_json()
    if not data or "title" not in data or "author" not in data:
        return jsonify({"error": "Missing title or author"}), 400
    
    new_book = Book(title=data["title"], author=data["author"])
    db.session.add(new_book)
    db.session.commit()  # Save changes to database
    return jsonify(new_book.to_dict()), 201

@app.route("/books", methods=["GET"])
def get_books():
    books = Book.query.all()
    return jsonify([b.to_dict() for b in books]), 200

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    data = request.get_json()
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    db.session.commit()
    return jsonify(book.to_dict()), 200

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"}), 200

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 7. Advanced Concepts & Examples

### Example 1: Implementing a Sliding Window Log Rate Limiter
A clean Python class simulating a Redis sliding window log algorithm to track API limits.

```python
import time

class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window_seconds = window_seconds
        # In-memory storage mapping clients to request timestamp lists
        self.client_logs = {}
        
    def is_rate_limited(self, client_ip: str) -> bool:
        now = time.time()
        # Initialize client log list if missing
        if client_ip not in self.client_logs:
            self.client_logs[client_ip] = []
            
        timestamps = self.client_logs[client_ip]
        
        # 1. Prune timestamps outside the current sliding window
        window_start = now - self.window_seconds
        pruned_timestamps = [t for t in timestamps if t > window_start]
        self.client_logs[client_ip] = pruned_timestamps
        
        # 2. Check if the current timestamp count exceeds the limit
        if len(pruned_timestamps) >= self.limit:
            return True # Rate limited
            
        # 3. Log current request timestamp and allow access
        self.client_logs[client_ip].append(now)
        return False
```

### Example 2: Idempotent POST Payment Handler
A backend service implementation showing how to safely handle payment creation retries without double-charging.

```python
import uuid
import time

# Mock database connections
DB_IDEMPOTENCY_STORE = {} # Maps key -> (status, response_payload, expiry)
DB_ACCOUNT_BALANCES = {"user_1": 1000.00}

def process_idempotent_payment(
    idempotency_key: str, 
    user_id: str, 
    charge_amount: float
) -> tuple[int, dict]:
    
    # 1. Validate Idempotency Key presence
    if not idempotency_key:
        return 400, {"error": "Missing Idempotency-Key header."}
        
    now = time.time()
    
    # 2. Check cache for matching key
    if idempotency_key in DB_IDEMPOTENCY_STORE:
        status, response_payload, expiry = DB_IDEMPOTENCY_STORE[idempotency_key]
        if now < expiry:
            print("Idempotency key match found. Returning cached response.")
            return status, response_payload
            
    # 3. Acquire distributed lock (represented as simple state update)
    # Check balance and deduct
    balance = DB_ACCOUNT_BALANCES.get(user_id, 0.0)
    if balance < charge_amount:
        status = 400
        payload = {"error": "Insufficient funds."}
    else:
        # Deduct balance
        DB_ACCOUNT_BALANCES[user_id] -= charge_amount
        transaction_id = str(uuid.uuid4())
        status = 201
        payload = {
            "status": "SUCCEEDED",
            "transaction_id": transaction_id,
            "amount_charged": charge_amount,
            "new_balance": DB_ACCOUNT_BALANCES[user_id]
        }
        
    # 4. Save response to Idempotency Store (expire in 1 hour)
    DB_IDEMPOTENCY_STORE[idempotency_key] = (status, payload, now + 3600)
    return status, payload
```

### Example 3: Webhook Verification using HMAC-SHA256
Verifying incoming webhooks signatures to protect endpoints from malicious spoofing attacks.

```python
import hmac
import hashlib
import time

def verify_webhook_signature(
    payload_body: bytes, 
    received_signature_header: str, 
    webhook_secret: str,
    max_drift_seconds: int = 300
) -> bool:
    """
    Validates that a webhook payload was generated by our official source.
    Format of header: t=1781290312,s=25409aef8d99c...
    """
    if not received_signature_header or not webhook_secret:
        return False
        
    # 1. Parse timestamp and signature hash from header
    try:
        parts = dict(item.split("=") for item in received_signature_header.split(","))
        timestamp = parts.get("t")
        received_signature = parts.get("s")
    except ValueError:
        return False
        
    if not timestamp or not received_signature:
        return False
        
    # 2. Check for time-drift replay attacks
    now = int(time.time())
    if abs(now - int(timestamp)) > max_drift_seconds:
        print("Webhook failed: Time drift limit exceeded.")
        return False
        
    # 3. Recreate signing payload: <timestamp>.<raw_body>
    signing_message = f"{timestamp}.".encode("utf-8") + payload_body
    
    # 4. Compute expected HMAC-SHA256 signature
    key = webhook_secret.encode("utf-8")
    expected_signature = hmac.new(
        key, 
        signing_message, 
        hashlib.sha256
    ).hexdigest()
    
    # 5. Use constant-time comparison to prevent timing attacks
    # 5. Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(expected_signature, received_signature)
```

### Example 4: Modular Flask Microservice with Blueprints
Structuring a scalable Flask application using blueprints, middleware pre-request actions, and application configurations.

`project/auth.py`:
```python
from flask import Blueprint, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"token": "jwt_token_secret_123"}), 200
```

`project/main.py`:
```python
from flask import Flask, jsonify, g, request
import time
from auth import auth_bp

app = Flask(__name__)

# Register Blueprint module under route prefix
app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

# Application middleware: hook executed before every request
@app.before_request
def start_timer():
    g.start_time = time.time()  # Store timestamp in request context 'g'

# Application middleware: hook executed after every request
@app.after_request
def log_request_performance(response):
    duration = time.time() - g.start_time
    # Inject profiling metadata into response headers
    response.headers["X-Response-Time-Ms"] = str(int(duration * 1000))
    return response

@app.route("/api/v1/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(port=8000)
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate API engineering competence by testing how candidates design interfaces under real-world constraints (scaling, reliability, and security). They look for precision in status code usage, deep understanding of safety/idempotency rules, appreciation for pagination limits, and awareness of authentication risks.

### Red Flags
- **HTTP Semantics Abuse**: Proposing `GET` calls that mutate database states, or returning `200 OK` responses containing custom JSON error logs (e.g. `{"status": "error", "code": 500}`).
- **Infinite Offset Scans**: Using offset pagination for large tables without understanding database cost ($O(N)$ index traversal).
- **Security Vulnerability Blanks**: Suggesting webhooks without webhook signature validation or data transit without SSL verification.
- **RPC in REST Clothes**: Creating endpoint naming structures like `/api/v1/updateUserEmail` or `/api/v1/deleteArticle`.

### Green Flags
- **Strict Adherence to Standards**: Recommending proper status codes (e.g., `201 Created` with a `Location` header, `204 No Content` for deletions).
- **Cursor-based Pagination**: Proposing cursor-based pagination by default for tables exceeding 1 million rows.
- **Idempotency keys**: Suggesting idempotency keys when designing financial or mutation-heavy endpoints.
- **HMAC Signatures**: Proactively suggesting webhook signature validation and time-drift checks to mitigate replay attacks.

### Answers Matrix
| Level | Question: "What status code do you return when a client attempts to delete a non-existent item?" |
|---|---|
| **Rejected** | "I'll return `200 OK` and a message: 'Not found'." |
| **Shortlisted** | "I will return a `404 Not Found` because the item does not exist." |
| **Selected** | "There are two valid approaches depending on API context: First, return `404 Not Found` if the API wants to inform the client of a target missing error. Second, return `204 No Content` (or `200 OK`) because the ultimate goal of a DELETE request is achieved (the resource is gone). The latter is preferred to prevent errors on rapid client retries, maintaining idempotency." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is REST and what are its six core constraints?
- **Detailed Answer**: REST (Representational State Transfer) is an architectural style for designing networked applications. It defines six constraints:
1. **Client-Server Architecture**: Separates user interface concerns from data storage concerns.
2. **Statelessness**: Every request from a client must contain all context needed to process it. No session state is stored on the server.
3. **Cacheability**: Responses must define themselves as cacheable or not to improve network efficiency.
4. **Uniform Interface**: Simplifies and decouples architecture via standardized URIs, HTTP verbs, resource representations (JSON), and hypermedia links (HATEOAS).
5. **Layered System**: Clients cannot detect if they are connected directly to the end server or an intermediate proxy (load balancer, cache).
6. **Code on Demand (Optional)**: Servers can extend client functionality by transmitting executable code (e.g., JavaScript).
- **Follow-up Questions**: Why is statelessness critical for horizontal scaling? (Answer: Statelessness means any incoming request can route to any application server node since no node depends on local memory session state).
- **Interviewer's Expectations**: Enumerate all 6 constraints, explain client-server decoupling, and explain the architectural benefit of statelessness.

#### 2. What is the difference between PUT and PATCH?
- **Detailed Answer**:
- `PUT` is used to **replace** a resource in its entirety. The client must upload the complete representation of the resource. If fields are omitted, the server overwrites them with default values or nulls. PUT is idempotent.
- `PATCH` is used for **partial updates**. The client only transmits the specific fields it wishes to change. PATCH is not strictly idempotent (e.g., if the payload instructs the server to append a string or increment a counter).
- **Follow-up Questions**: How do you make PATCH idempotent? (Answer: Restrict the patch operations to static value assignments or use JSON Merge Patch schemas).
- **Interviewer's Expectations**: Differentiate complete replacement (PUT) from partial mutation (PATCH), and explain the differences in their idempotency specifications.

#### 3. How do safety and idempotency differ in HTTP methods?
- **Detailed Answer**:
- **Safety**: A method is safe if it does not change the state of the server. GET, HEAD, and OPTIONS are safe methods. They are read-only.
- **Idempotency**: A method is idempotent if executing it multiple times yields the exact same server state as executing it once. PUT, DELETE, GET, and HEAD are idempotent. POST is not.
- *All safe methods are idempotent, but not all idempotent methods are safe* (e.g., DELETE modifies server state, so it is not safe, but running it multiple times yields the same final state, so it is idempotent).
- **Follow-up Questions**: Is PATCH idempotent? (Answer: Under RFC 5789, PATCH is not required to be idempotent, though specific API implementations can enforce it).
- **Interviewer's Expectations**: Distinguish read-only operations (Safety) from identical results on repeat execution (Idempotency).

#### 4. What is the difference between 401 Unauthorized and 403 Forbidden?
- **Detailed Answer**:
- **401 Unauthorized**: Means the user's identity is unauthenticated. The server does not know who the user is. The response must include a `WWW-Authenticate` header prompting credentials.
- **403 Forbidden**: Means the user's identity is authenticated, but they do not have the required permissions to access the target resource (authorization failure).
- **Follow-up Questions**: In what scenario would you return a 404 instead of a 403? (Answer: If disclosing the existence of a restricted resource is a security leak, return 404 to hide it).
- **Interviewer's Expectations**: Clearly separate authentication (401) from authorization (403).

#### 5. Explain HATEOAS and its benefits.
- **Detailed Answer**: HATEOAS (Hypermedia As The Engine Of Application State) is a constraint of RESTful system design. It requires the server to return hypermedia links detailing all possible actions the client can take from the current state.
Benefits:
- Decouples client code from API URL endpoints. The client only needs to know the initial root URL; subsequent actions are discovered dynamically.
- Permits changing backend URL routing paths without updating client code.
- **Follow-up Questions**: Why is HATEOAS rarely used in modern web APIs? (Answer: It adds significant parsing complexity to frontend apps, increases payload sizes, and lacks strong support in client generators).
- **Interviewer's Expectations**: Explain the dynamic link navigation concept and contrast its theoretical benefit with practical industry implementation.

#### 6. What is Content Negotiation and how does it work?
- **Detailed Answer**: Content Negotiation is the mechanism that allows a client and server to agree on the media type, language, and character encoding of the response. It is implemented via HTTP headers:
- The client sends headers specifying preferences: `Accept` (e.g. `application/json, text/html`), `Accept-Language` (e.g., `fr, en`), `Accept-Encoding` (e.g., `gzip`).
- The server analyzes these headers, selects the best matching format it supports, and returns the response alongside corresponding metadata headers: `Content-Type: application/json` and `Content-Language: fr`.
- **Follow-up Questions**: What is a "406 Not Acceptable" status code? (Answer: The server returns 406 if it cannot produce a representation matching the client's `Accept` headers).
- **Interviewer's Expectations**: Describe the client-server negotiation handshake and the role of headers like `Accept` and `Content-Type`.

#### 7. Compare Offset Pagination and Cursor Pagination.
- **Detailed Answer**:
- **Offset Pagination**: Uses `limit` and `offset` (e.g. `LIMIT 50 OFFSET 1000`).
  - *Pros*: Simple to write; allows jumping to arbitrary pages.
  - *Cons*: Slow for high offset values because databases must scan and discard $N$ rows; unstable if elements are added or deleted while the user is paginating.
- **Cursor Pagination**: Uses a unique cursor pointing to the last retrieved record (e.g., `starting_after=id_9821`).
  - *Pros*: Fast ($O(1)$ lookup using indexed ID queries); immune to page-drift anomalies.
  - *Cons*: Cannot jump to arbitrary pages; requires sorting on a unique, sequential index.
- **Follow-up Questions**: When is offset pagination acceptable? (Answer: When the total row count is guaranteed to remain small, or when arbitrary page jumping is a core business requirement).
- **Interviewer's Expectations**: Compare the performance profile ($O(N)$ vs. $O(1)$), details of dataset drift, and layout use cases.

#### 8. What is CORS and how do you resolve CORS errors?
- **Detailed Answer**: CORS (Cross-Origin Resource Sharing) is a browser-enforced security mechanism that prevents web applications running on one domain (origin) from requesting resources on a different domain.
- **Mechanism**: The browser sends a preflight `OPTIONS` request before making cross-origin requests. The server must respond with headers like `Access-Control-Allow-Origin: *` or a specific domain.
- **Resolution**:
1. Configure backend server middleware to return appropriate CORS headers (`Access-Control-Allow-Origin`, `Access-Control-Allow-Methods`, `Access-Control-Allow-Headers`).
2. Use an API gateway or reverse proxy to serve both the frontend and backend from the same domain origin.
- **Follow-up Questions**: Does a CORS block prevent the server from executing the request? (Answer: Not necessarily; the browser blocks the *read response* action on the client side, but the server may have processed the mutation).
- **Interviewer's Expectations**: Explain the browser-based nature of CORS, the preflight OPTIONS handshake, and backend header remedies.

#### 9. Explain the rate-limiting algorithms: Token Bucket and Leaky Bucket.
- **Detailed Answer**:
- **Token Bucket**: A bucket is filled with tokens at a constant rate up to a max capacity. Each incoming request consumes a token. If the bucket is empty, the request is rejected.
  - *Behavior*: Permits traffic **bursts** up to the bucket's max capacity.
- **Leaky Bucket**: Requests enter a bucket and are queued. The bucket leaks requests at a constant, smooth rate. If the queue fills up, new requests overflow and are rejected.
  - *Behavior*: Enforces a **smooth, uniform rate** of execution, eliminating bursts.
- **Follow-up Questions**: Which algorithm is preferred for API gateways serving human users? (Answer: Token Bucket, as users often generate short bursts of requests during page loads).
- **Interviewer's Expectations**: Differentiate bursty traffic handling (Token Bucket) from smooth traffic shaping (Leaky Bucket).

#### 10. What is a webhook, and how do you secure it?
- **Detailed Answer**: A webhook is a user-defined HTTP POST callback. When an event occurs on a source server (e.g. user subscription renewed), the server makes an HTTP POST request carrying JSON data to a URL registered by the client.
Security measures:
1. **HMAC Signatures**: The server signs the payload using a shared secret and sends the hash in the headers (e.g., `X-Signature`). The client computes the HMAC of the raw body and matches it.
2. **Timestamp Header**: Include a timestamp in the signed header to prevent replay attacks where a third party intercepts and replays the same request.
3. **HTTPS**: Force HTTPS on the client webhook receiver.
- **Follow-up Questions**: How do you prevent a timing attack during signature verification? (Answer: Use a constant-time comparison helper like `hmac.compare_digest`).
- **Interviewer's Expectations**: Detail the signature validation workflow, timestamp verification, and timing attack mitigation.

---

### Scenario-Based Questions

#### 11. Design a pagination scheme for a system displaying millions of log messages.
- **Detailed Answer**:
- I will implement **Cursor Pagination**.
- The database schema has logs stored with a sequential, indexed `id` (or timestamp + unique ID combination).
- The API endpoint will accept parameters: `limit` (max records per page, default 50) and `cursor` (the base64 encoded ID of the last log message from the previous page).
- **SQL Query**:
  ```sql
  SELECT * FROM logs 
  WHERE id > :cursor_id 
  ORDER BY id ASC 
  LIMIT :limit;
  ```
- The API response payload will return the data list, a boolean `has_more`, and a `next_cursor` referencing the ID of the last item in the returned page list.
- **Follow-up Questions**: Why base64 encode the cursor? (Answer: It abstracts the database implementation details from the client, allowing us to change the cursor structure in the future).
- **Interviewer's Expectations**: Recommend cursor pagination over offset pagination, and detail the SQL query design and cursor structure.

#### 12. Design an API endpoint to handle massive file uploads (e.g., 5GB videos).
- **Detailed Answer**: A direct POST request with a 5GB payload will cause network timeouts and consume server memory.
- **Design: Presigned Multipart Uploads**:
  1. The client sends a request: `POST /api/v1/uploads` with metadata (`file_name`, `file_size`, `content_type`).
  2. The server coordinates with object storage (e.g., AWS S3) and returns an upload session ID and a list of **Presigned URLs** (one for each chunk, e.g. 50MB chunks).
  3. The client uploads each file chunk directly to the presigned URLs in parallel.
  4. Once all uploads succeed, the client sends a `POST /api/v1/uploads/{id}/completion` request.
  5. The server instructs the object store to merge the uploaded chunks into the final file.
- **Follow-up Questions**: How do you handle a chunk upload failure? (Answer: The client simply retries the failed chunk's presigned URL without re-uploading the entire file).
- **Interviewer's Expectations**: Propose chunk-based uploads, presigned URLs, and decoupling files from the application server.

#### 13. You need to support versioning for a rapidly evolving API. Which strategy (URL path, query param, or header) do you select, and why?
- **Detailed Answer**: I will choose **URL Path Versioning** (e.g., `/api/v1/users`) for public APIs, and **Header-based Versioning** for enterprise APIs.
- **URL Path Versioning**:
  - *Pros*: Discoverable, easy to test in browsers, integrates with API gateway routing rules.
  - *Cons*: Violates REST theory that a resource should have a single URI; can lead to code duplication.
- **Header-based Versioning**:
  - *Pros*: Keeps URLs clean; allows fine-grained versioning of individual resources.
  - *Cons*: Difficult to test; requires custom client setups.
- **Selection**: I choose URL path versioning because of its simplicity for developers and its compatibility with CDN caching rules.
- **Follow-up Questions**: How does versioning impact caching? (Answer: Paths cache separately automatically, whereas header-based versioning requires adding `Vary: Accept-Version` to response headers to prevent cache pollution).
- **Interviewer's Expectations**: Compare versioning styles and explain how they interact with caching layers.

#### 14. Design an endpoint to process credit card payments that is resilient to client network drops.
- **Detailed Answer**:
- I will design a `POST /api/v1/payments` endpoint that requires an `Idempotency-Key` header.
- **Backend Workflow**:
  1. Receive payment request. Validate presence of `Idempotency-Key` (UUID).
  2. Start database transaction.
  3. Query `idempotency_store` matching the key.
     - If key exists and status is `SUCCESS`, return the cached response immediately.
     - If key exists and status is `PROCESSING`, return `409 Conflict` or a message informing the client to wait.
  4. If key does not exist, insert key with status `PROCESSING`. Commit initial database insert.
  5. Execute payment gateway call (e.g. Stripe API).
  6. Save payment result to database. Update `idempotency_store` status to `SUCCESS` and save the response payload.
  7. Commit transaction and return response.
- **Follow-up Questions**: What is the expiry time of idempotency keys? (Answer: Typically 24 hours, cached in Redis or a fast-access database).
- **Interviewer's Expectations**: Detail database locking, cache states (processing, success), and integration with external gateways.

#### 15. Design a notification system where clients receive real-time updates when an order status changes.
- **Detailed Answer**: Standard polling wastes resources.
- **Option A: Webhooks**: Best for server-to-server notifications. The client registers a webhook URL. When the order status changes, our server sends a signed POST request.
- **Option B: Server-Sent Events (SSE)**: Best for browser clients. It provides a unidirectional persistent stream using standard HTTP/1.1 chunked transfer encoding (`text/event-stream`).
- **Option C: WebSockets**: Best for bidirectional real-time communications.
- **Selection**: For client browsers, I will use **SSE** as it is lightweight and handles reconnects automatically. For third-party servers, I will use **Webhooks** with HMAC validation.
- **Follow-up Questions**: Why is SSE preferred over WebSockets for one-way updates? (Answer: SSE runs over standard HTTP/1.1 or HTTP/2, requires no protocol upgrades, and supports automatic reconnection).
- **Interviewer's Expectations**: Compare real-time protocols and choose the right one for server-to-server vs. server-to-client scenarios.

---

### Debugging Questions

#### 16. A client reports getting a 500 error from your endpoint, but your server logs show no exceptions. What could be the cause?
- **Detailed Answer**:
1. **API Gateway / Proxy Block**: The request may have been rejected by an upstream proxy (like Nginx, Cloudflare, or an AWS ALB) before reaching the application server. This occurs if:
   - The payload size exceeded the proxy's limit (`client_max_body_size`), returning `500` or `502`.
   - The request headers were too large.
2. **Database Connection Pool Exhaustion**: The application server is running but hangs on database connection retrieval, timing out at the gateway layer.
3. **Response Serialization Failures**: The application processed the request successfully but failed when converting the response object to JSON (e.g. trying to serialize a circular reference or an unparseable database object).
- **Follow-up Questions**: How do you isolate this? (Answer: Inspect the gateway/load balancer logs to check if the request was forwarded to the application server IP).
- **Interviewer's Expectations**: Identify upstream gateway limits and response serialization bugs as common causes of unlogged 500 errors.

#### 17. Your frontend client is blocked from making API requests, showing: "CORS policy: No Access-Control-Allow-Origin header is present." Explain and fix.
- **Detailed Answer**:
- **Explanation**: The browser blocked the response because the frontend code is hosted on Origin A (e.g. `http://localhost:3000`) while the API is hosted on Origin B (e.g., `https://api.example.com`). The API server response did not include the header permitting requests from Origin A.
- **Fix**: Configure CORS middleware on the API server to return:
  ```http
  Access-Control-Allow-Origin: http://localhost:3000
  Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS
  Access-Control-Allow-Headers: Content-Type, Authorization
  Access-Control-Allow-Credentials: true
  ```
  Also, ensure the backend handles the preflight `OPTIONS` request and returns a `204 No Content` response immediately.
- **Follow-up Questions**: Why is setting `Access-Control-Allow-Origin: *` dangerous in production? (Answer: It allows any malicious website to make authenticated cross-origin requests on behalf of users if credentials are enabled).
- **Interviewer's Expectations**: Explain the browser origin model and provide the exact CORS headers needed to resolve the block.

#### 18. A database query takes 10ms, but the overall API endpoint response time is over 1 second. How do you troubleshoot this latency?
- **Detailed Answer**:
1. **Network Overhead**: The server and database may be close, but the client is far away, or the server response payload is too large.
2. **Response Serialization Bottlenecks**: Serializing thousands of database rows into a massive JSON string in Python can block the single-threaded event loop (e.g., using slow serializers).
3. **External API Calls**: The endpoint may be making synchronous blocking calls to external services (e.g., payment gateways or geo-IP lookup tools) during the request lifecycle.
4. **N+1 Query Issue**: While one query takes 10ms, the application may be executing 100 subsequent queries in a loop to fetch related records.
- **Follow-up Questions**: How do you debug this? (Answer: Use profiling tools like APMs to trace function execution times, check log timestamps, and inspect payload sizes).
- **Interviewer's Expectations**: Identify serialization issues, blocking API calls, and network transfers as potential bottlenecks.

#### 19. A client reports duplicate charges on a payment endpoint. The client says they only clicked "pay" once. How did this happen and how do you fix it?
- **Detailed Answer**:
- **How it happened**: The client clicked once, but their network connection dropped before they received the response. The client browser (or HTTP library) automatically retried the POST request under the hood, or the client refreshed the page. Since POST is not idempotent, the server processed two separate transactions.
- **Fix**: Implement an `Idempotency-Key` header on the server. Force the frontend to generate a unique UUID for the payment button action and send it with the request, allowing the server to deduplicate retries.
- **Follow-up Questions**: What happens if two identical requests arrive at the exact same millisecond? (Answer: The database must use unique constraints or distributed locks on the idempotency key to force the second request to wait).
- **Interviewer's Expectations**: Identify network retry behaviors and recommend idempotency keys as the standard resolution.

#### 20. Your JSON parser fails on incoming payloads because of special characters. How do you debug and resolve this?
- **Detailed Answer**:
- **Diagnosis**: JSON requires strings to be encoded in UTF-8 and control characters to be escaped. If a client transmits raw control characters (like carriage returns or tabs) without escaping them, or uses incorrect character sets (like ISO-8859-1), the JSON parser will throw errors.
- **Resolution**:
1. Ensure the client sends the header: `Content-Type: application/json; charset=utf-8`.
2. Use standard JSON serialization libraries on the client side (e.g., `JSON.stringify` in JS) instead of concatenating strings manually.
3. Validate client encoding formats on the server before passing data to the JSON parser.
- **Follow-up Questions**: How do you escape backslashes in JSON? (Answer: Escape them with a double backslash `\\`).
- **Interviewer's Expectations**: Focus on encoding validation, header assertions, and standard serialization libraries.

---

### System Design Questions

#### 21. Design a public API for a SaaS application that will be consumed by thousands of external developers.
- **Detailed Answer**:
- **Endpoint Structure**: RESTful URL paths with resource names and versioning (e.g. `/v1/projects`).
- **Authentication**: Provide developer API keys passed via `Authorization: Bearer <key>` headers.
- **Rate Limiting**: Enforce rate limits (e.g., 100 requests/min) per key using a Redis-backed token bucket algorithm. Return `429 Too Many Requests` on breach with headers `X-RateLimit-Limit`, `X-RateLimit-Remaining`, and `Retry-After`.
- **Documentation & SDKs**: Provide an OpenAPI/Swagger specification to generate documentation and SDKs in multiple languages.
- **Errors**: Return consistent error schemas:
  ```json
  {
    "error": {
      "code": "invalid_api_key",
      "message": "The provided API key is invalid.",
      "request_id": "req_8812"
    }
  }
  ```
- **Follow-up Questions**: How do you rotate developer API keys securely? (Answer: Support active key pairs so developers can migrate to a new key without downtime).
- **Interviewer's Expectations**: Detail versioning, developer onboarding (keys), rate limiting headers, Open API specification, and consistent error patterns.

#### 22. Design a high-reliability webhook delivery system.
- **Detailed Answer**:
- **Event Capture**: When an event occurs, push it to a message queue (e.g., RabbitMQ or AWS SQS).
- **Worker Pipeline**: Webhook workers consume events from the queue, look up the target client URL and secret key, and perform an HTTP POST request.
- **Retry Logic**: If the client server returns a non-2xx status code or times out, trigger an exponential backoff retry schedule (e.g., retry after 1m, 5m, 15m, 1h, up to 24 hours).
- **Dead Letter Queue (DLQ)**: If all retries fail, move the webhook to a DLQ for client review.
- **Security**: Compute an HMAC-SHA256 signature of the payload using the shared secret and include it in the headers alongside a timestamp.
- **Circuit Breaker**: If a client's server is consistently down (e.g., 1000 consecutive timeouts), temporarily disable their webhook subscription.
- **Follow-up Questions**: How do you handle webhook delivery order guarantees? (Answer: Use partitioned queues, e.g. Kafka or SQS FIFO, matching client accounts to guarantee sequential delivery).
- **Interviewer's Expectations**: Propose queues, worker clusters, exponential retries, DLQ routing, security headers, and circuit breaker patterns.

#### 23. Design an API Gateway architecture to handle authentication, rate limiting, and request routing for 100 microservices.
- **Detailed Answer**:
- **Layering**: Deploy an API Gateway (e.g., Kong, Envoy, or AWS API Gateway) at the edge of the network.
- **Routing**: The gateway acts as a reverse proxy, mapping public URLs to internal microservice IPs (e.g. routing `/v1/billing/*` to Billing Service clusters).
- **Shared Authentication**: The gateway intercepts requests, validates JWT tokens, and injects user identity headers (e.g., `X-User-Id`, `X-User-Roles`) before forwarding requests internally.
- **Distributed Rate Limiting**: The gateway queries a central Redis cluster using a sliding window algorithm to throttle clients before they hit internal services.
- **SSL Termination**: The gateway decrypts SSL/TLS traffic, allowing internal service-to-service communication to run on HTTP to reduce CPU overhead.
- **Follow-up Questions**: How does SSL termination improve backend service performance? (Answer: It offloads SSL handshake calculations from individual microservice containers to the gateway hardware).
- **Interviewer's Expectations**: Propose reverse proxying, token authorization delegation, centralized rate-limiting, and SSL termination.

---

#### 61. Explain Flask's application and request contexts. How do they work under the hood, and how are they managed in multi-threaded environments?
- **Detailed Answer**: Flask uses a context-based design to make variables like `request` or `current_app` globally accessible inside view functions without explicitly passing them as arguments.
  - **The Two Contexts**:
    1. **Application Context**: Bound to the lifespan of the Flask application object. It manages variables like `current_app` (the active application instance) and `g` (a temporary global namespace for a single request, often used for database connections or timers).
    2. **Request Context**: Bound to the lifespan of a single HTTP request. It manages variables like `request` (incoming request payload/headers) and `session` (signed cookie data).
  - **Under the Hood (Werkzeug Local Proxies)**:
    - Flask uses **Thread-Local Storage** (specifically Werkzeug's `LocalStack` and `LocalProxy`). 
    - When an HTTP request arrives, Flask identifies the thread handling the request and pushes the corresponding application and request context objects onto their respective thread-local stacks.
    - Global variables like `request` are actually `LocalProxy` objects. When accessed (e.g. `request.args`), the proxy dynamically forwards the attribute lookup to the top item on the active thread's local stack.
    - In multi-threaded or asynchronous environments (like greenlets or asyncio), Werkzeug uses greenlet/task identifiers instead of OS thread IDs to isolate stacks, ensuring that parallel requests do not leak data or access other clients' payloads.
    - At the end of the request-response lifecycle, Flask pops both contexts from the stack, clearing the thread-local storage to prevent memory leaks.
- **Follow-up Questions**: Why do you get a `RuntimeError: Working outside of application context` when running background tasks or scripts? (Answer: Outside of an active HTTP request, the local stacks are empty. You must manually push an application context using the `with app.app_context():` context manager to access variables like `current_app` or database models).
- **Interviewer's Expectations**: Define the two context types (application vs. request), explain thread-local storage stacks, describe how `LocalProxy` resolves variables dynamically, and detail context creation/cleanup on request lifecycle.

---

#### 62. Describe the database session lifecycle in Flask-SQLAlchemy. How does it handle connection pools, transaction boundaries, and request teardown?
- **Detailed Answer**: Flask-SQLAlchemy manages database connections and ORM transactions by linking the SQLAlchemy `Session` to Flask's request lifecycle:
  - **Initialization & Scoped Session**:
    - Flask-SQLAlchemy creates a `scoped_session`, which acts as a thread-safe registry of database sessions. When `db.session` is called, it returns a session unique to the active request context/thread.
  - **Connection Pool**:
    - Under the hood, SQLAlchemy maintains a connection pool (e.g., `QueuePool`). When the session needs to query the database, it checks out a physical TCP connection from the pool.
  - **Transaction Boundaries**:
    - A transaction begins automatically (lazy initialization) when the first SQL statement is executed.
    - The developer staging changes using `db.session.add(item)` or `db.session.delete(item)` updates the session's internal state. Calling `db.session.commit()` commits the active database transaction and returns the connection to the pool.
  - **Request Teardown & Cleanup**:
    - Flask registers a teardown handler (`@app.teardown_request` or `@app.teardown_appcontext`).
    - At the end of every request (after the response is sent), Flask invokes `db.session.remove()`. This method calls `session.close()`, which rolls back any uncommitted transactions (preventing dangling locks), clears all cached objects in the session identity map, and returns the physical database connection to the pool.
- **Follow-up Questions**: What is the danger of not closing or removing a session in a web application? (Answer: Unclosed sessions keep database connections checked out, eventually exhausting the database server's connection limits and causing subsequent requests to time out or crash).
- **Interviewer's Expectations**: Define scoped sessions, explain connection pooling, detail automatic transaction rollback/closure during request teardown, and identify resource exhaustion risks of unmanaged sessions.

---

## 10. Common Mistakes

- **Verbs in Endpoint URLs**: Naming endpoints `/api/getProfile` or `/api/deletePost` instead of `/api/profiles` and `/api/posts` with appropriate HTTP verbs.
- **Status Code Standard Violation**: Returning `200 OK` for error states, or using `404 Not Found` when a request fails authentication (use `401 Unauthorized` instead).
- **Missing Pagination Limits**: Exposing list endpoints without pagination, which can crash the application or database when the dataset grows to millions of rows.
- **Missing Webhook Validation**: Accepting webhook notifications on client servers without validating the HMAC signature.
- **Ignoring CORS in Early API Design**: Writing client code and API servers on separate origins without configuring preflight handling, resulting in production CORS blocks.

---

## 11. Comparison Section: REST vs. GraphQL vs. gRPC

| Feature | REST | GraphQL | gRPC |
|---|---|---|---|
| **Underlying Protocol** | HTTP/1.1 or HTTP/2 | HTTP/1.1 or HTTP/2 | HTTP/2 |
| **Payload Serialization** | JSON (dominant), XML | JSON | Protocol Buffers (Binary) |
| **Data Fetching Model** | Multiple endpoints (resources) | Single endpoint (`/graphql`) | Remote Procedure Call (RPC) |
| **Over/Under Fetching** | Common (returns fixed payload) | None (client requests specific fields) | None (defined by proto message) |
| **Streaming Support** | Limited (SSE/chunked) | Subscriptions | Bidirectional streaming |
| **Performance / Latency** | Moderate | Moderate (parsing query trees adds cost) | High (compact binary payloads) |
| **Type Safety** | Optional (via OpenAPI/JSON Schema) | Inherent (defined by Schema SDL) | Inherent (defined by `.proto` files) |
| **Use Cases** | Public APIs, web applications. | Complex frontend apps, mobile data fetching. | High-performance microservices. |

---

## 12. Practical Project Ideas

### Beginner: Simple CRUD Book Catalog API
Build a REST API in Python (using Flask or FastAPI) that manages a collection of books. Support GET, POST, PUT, and DELETE operations. Ensure it returns correct status codes (201 for POST, 204 for DELETE, and 404 for missing records). Validate inputs using Pydantic schemas.

### Intermediate: Secure Webhook Server with HMAC Signature Verification
Build a server that exposes a `/webhooks` endpoint designed to receive event data. Write code to validate that incoming payloads match an HMAC-SHA256 signature generated using a shared secret. Log errors for time-drift violations or signature mismatches.

### Advanced/Resume-worthy: Paginated Search API with Sliding Window Rate Limiting
Design a high-performance REST API. Implement cursor-based pagination over a database containing 1 million rows. Add a sliding-window rate limiter utilizing Redis to restrict clients to 60 requests per minute, returning custom `429` headers and retry metadata.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of GET vs POST, PUT vs PATCH, and safety/idempotency properties; basic understanding of status codes (200, 201, 204, 400, 401, 403, 404, 429, 500).
- **What Engineering Teams expect**: Hands-on experience designing REST URLs using resource structures, pagination models, and handling JWT authentication at the API layer.

---

## 14. Cheat Sheet

- **Resource URLs**: Always use plural nouns: `/api/v1/users` (Collection), `/api/v1/users/12` (Document).
- **Idempotency Rules**:
  - `POST` is NOT idempotent.
  - `PUT`, `DELETE`, `GET` ARE idempotent.
- **Success Codes**:
  - `200` = Generic success.
  - `201` = Resource created successfully.
  - `204` = Action succeeded, no content to return.
- **Client Error Codes**:
  - `400` = Invalid parameters.
  - `401` = Missing/invalid credentials.
  - `403` = Authenticated, but unauthorized.
  - `404` = Resource does not exist.
  - `429` = Rate limit exceeded.

---

## 15. One-Day Revision Guide

- [ ] Memorize the idempotency and safety characteristics of all HTTP verbs.
- [ ] Understand the difference between `401 Unauthorized` and `403 Forbidden`.
- [ ] Explain how cursor-based pagination differs from offset-based pagination.
- [ ] Review the HMAC signature verification algorithm for securing webhooks.
- [ ] Describe the preflight `OPTIONS` request flow in CORS.
