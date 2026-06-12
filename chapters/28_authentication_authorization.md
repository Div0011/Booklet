# 28. Authentication & Authorization

## 1. Introduction

### What it is
Authentication (AuthN) and Authorization (AuthZ) are the distinct dual pillars of application security. **Authentication** answers the question, "Who are you?", verifying a user's, service's, or device's claimed identity. **Authorization** answers the question, "What are you allowed to do?", determining access permissions and enforcing security boundaries once identity is validated.

### Why it exists
Modern software runs on public, zero-trust infrastructure. Without robust authentication and authorization systems, any client can access databases, delete tables, read private user information, or spoof administrator actions. Auth systems enforce security perimeters, protect user privacy, and ensure organizations comply with regulatory standards like GDPR, HIPAA, and PCI-DSS.

### Problems it solves
- **Identity Spoofing**: Verifies that a request originated from the actual owner of the account.
- **Horizontal & Vertical Privilege Escalation**: Prevents general users from accessing administrator actions (vertical) or accessing other users' data (horizontal).
- **Session Hijacking**: Tracks and validates active sessions, expiring credentials automatically after inactivity.
- **Auditing and Compliance**: Records who executed which action and when, generating secure audit trails.
- **Centralized Identity Management**: Enables users to login once and access multiple distinct services securely (Single Sign-On).

### Industry Use Cases
- **B2C SaaS Apps**: User registration, password resets, and logging in using session cookies or JWTs.
- **API Gateways**: Authenticating third-party developer calls using scoped API keys or OAuth 2.0 access tokens.
- **Single Sign-On (SSO)**: Allowing employees to log in using their enterprise identity provider (Okta, Azure AD) to access internal tools like Slack and Jira.
- **Microservices Communication**: Verifying service-to-service calls using Mutual TLS (mTLS) or internal tokens.
- **Healthcare & Financial Systems**: Enforcing Attribute-Based Access Control (ABAC) to restrict patient record views based on doctor schedules and departments.

### Analogy
Authentication is the security guard at an airport check-in desk verifying your passport and matching your face to the photo. Authorization is your boarding pass, which does not prove who you are, but determines which gate you can enter, which plane you can board, and whether you are seated in First Class or Economy.

---

## 2. Core Concepts

### Beginner Concepts
- **Authentication (AuthN)**: The process of verifying a claim of identity using credentials. Factors include: something you know (password), something you have (keycard/token), or something you are (fingerprint).
- **Authorization (AuthZ)**: The process of granting or denying access to resources based on permissions.
- **Stateful Sessions**: The server generates a unique session ID, stores it in a server-side cache (like Redis), and returns it to the client inside a cookie. On subsequent requests, the server looks up the cookie's session ID in its cache to restore the user's identity.
- **Stateless Tokens**: The server encodes the user's identity and permissions inside a token (like a JWT), signs it with a cryptographic key, and returns it to the client. The client sends this token with each request. The server validates the signature without querying a database.
- **Password Hashing, Salting, and Peppering**:
  - *Hashing*: Running a password through a one-way mathematical function (e.g. Argon2) to generate a unique string. Plaintext passwords must never be stored.
  - *Salting*: Appending a random unique string to the password before hashing to prevent rainbow table attacks.
  - *Peppering*: Appending a global system-wide secret to the password before hashing. The pepper is stored in a separate secure vault, not in the database.

### Intermediate Concepts
- **JWT (JSON Web Token)**: A compact, URL-safe container for exchanging claims. It consists of three parts separated by dots (`header.payload.signature`):
  - **Header**: Defines the token type (JWT) and signing algorithm (e.g., HS256, RS256).
  - **Payload**: Contains the claims (e.g., `sub` for user ID, `exp` for expiration, and roles).
  - **Signature**: Formed by hashing the base64-encoded header and payload with a secret key, ensuring token integrity.
- **OAuth 2.0 Framework**: An authorization protocol allowing a third-party application to obtain limited access to a HTTP service on behalf of a resource owner. Core roles: Resource Owner (user), Client (app), Authorization Server, and Resource Server (API).
- **OpenID Connect (OIDC)**: An identity layer built on top of OAuth 2.0. While OAuth 2.0 returns an *Access Token* (for authorization), OIDC returns an *ID Token* (a JWT containing user profile details for authentication).
- **RBAC (Role-Based Access Control)**: Permissions are assigned to roles (e.g. `role: admin`, `role: editor`), and users are assigned to those roles. Easy to manage but struggles with dynamic permissions.
- **ABAC (Attribute-Based Access Control)**: Permissions are evaluated dynamically using policies that combine attributes of the subject (user role, department), resource (file type, owner), and environment (IP address, time of day).

### Advanced Concepts
- **PKCE (Proof Key for Code Exchange)**: An extension to OAuth 2.0 designed to secure public clients (like SPAs and mobile apps) against code interception attacks. It replaces the static client secret with a dynamic challenge generated using a temporary code verifier.
- **Mutual TLS (mTLS)**: A security protocol where both client and server authenticate each other's digital certificates during the TLS handshake, establishing verified cryptographic identity for service-to-service communication.
- **Passkeys & WebAuthn**: A passwordless authentication standard utilizing public-key cryptography. The user registers a hardware authenticator (device fingerprint or face scanner) that signs cryptographic challenges sent by the server. It is immune to phishing attacks because credentials are bound to specific domains.
- **Zero Trust Architecture**: A security model based on the principle "never trust, always verify." It assumes threats exist inside the network, requiring continuous authentication, authorization, and micro-segmentation for every request.
- **Centralized Policy Engines (OPA/Cedar)**: Decoupling authorization logic from application code. The application sends authorization requests to a service like OPA (Open Policy Agent), which evaluates policies written in declarative languages (like Rego) and returns an allow/deny decision.
- **Token Revocation and Rotation Patterns**:
  - *Blacklisting*: Storing revoked tokens (like logged-out JWTs) in a fast Redis cache until their expiration date passes.
  - *Refresh Token Rotation*: Issuing a new refresh token on every token refresh request. If an old refresh token is reused, the server detects it as a theft attempt, invalidates the entire session family, and forces a re-login.

---

## 3. Internal Working

### Session-Based Stateful Authentication Flow
In stateful authentication, session persistence is tied to a shared memory block or cache on the server.

```text
Client (Browser)                           Server                              Redis Cache
  |                                          |                                      |
  | -- 1. POST /login (username, password)-> |                                      |
  |                                          | -- 2. Validate credentials --------> |
  |                                          | -- 3. Generate session ID (UUID) --> |
  |                                          | -- 4. Write session: session_id ---->|
  | <- 5. Set-Cookie: session_id=xyz ------- |                                      |
  |                                          |                                      |
  v (Subsequent Request)                     v                                      v
  | -- 6. GET /dashboard (Cookie: xyz) ----> |                                      |
  |                                          | -- 7. Fetch session: xyz ----------> |
  |                                          | <----- Return session data --------- |
  | <- 8. Render dashboard ----------------- |                                      |
```

*Architectural trade-off*: As traffic scales, multiple server nodes behind a load balancer require either "sticky sessions" (routing users to the same node) or a shared distributed cache (Redis) to verify sessions. If the Redis cache fails, all active user sessions are terminated.

### Stateless JWT Authentication Flow
In stateless authentication, the server relies on cryptographic verification of signatures to assert identity, eliminating database reads during request routing.

```text
Client (Browser)                           Server                              Database
  |                                          |                                      |
  | -- 1. POST /login (username, password)-> |                                      |
  |                                          | -- 2. Validate credentials --------> |
  |                                          | -- 3. Generate JWT Payload --------> |
  |                                          | -- 4. Sign JWT with Private Key ---> |
  | <- 5. Return JWT Token (Bearer token) -- |                                      |
  |                                          |                                      |
  v (Subsequent Request)                     v                                      v
  | -- 6. GET /users (Auth: Bearer jwt) ---> |                                      |
  |                                          | -- 7. Validate JWT Signature --------| (Offline check)
  |                                          | -- 8. Parse user claims (sub, roles)-| (Offline check)
  | <- 9. Return users list ---------------- |                                      |
```

- **Verifying JWTs (HS256 vs RS256)**:
  - **HS256 (Symmetric)**: The server signs and verifies the token using the same secret key. If a backend service needs to verify the token, it must have access to this secret key. If the secret key is leaked, an attacker can sign arbitrary tokens.
  - **RS256 (Asymmetric)**: The authentication server signs the token using a private key, and downstream microservices verify the signature using the corresponding public key. Public keys are distributed via a public endpoint called a **JWKS (JSON Web Key Set)**, ensuring the private key never leaves the identity provider.

### OAuth 2.0 Auth Code Flow with PKCE
Public clients (SPAs and mobile apps) cannot protect client secrets. If an attacker intercepts the authorization code sent to the redirect URI, they can exchange it for an access token. PKCE mitigates this by replacing static secrets with dynamic verifiers.

```text
Client App (SPA)                          Browser/User                       Auth Server
  |                                            |                                  |
  | -- 1. Generate code_verifier (random) ---- |                                  |
  | -- 2. Hash: challenge = SHA256(verifier) - |                                  |
  |                                            |                                  |
  | -- 3. Redirect to Auth Page with challenge ---------------------------------> |
  |                                            | -- 4. Authenticate & Approve --> |
  | <------------------------------------------| -- 5. Return Auth Code --------- |
  |                                            |                                  |
  | -- 6. POST /token (Auth Code + code_verifier) ------------------------------> |
  |                                            |                                  |
  |                                            | -- 7. Verify:                    |
  |                                            |   SHA256(verifier) == challenge  |
  | <-- 8. Return Access & Refresh Tokens --------------------------------------- |
```

---

## 4. Important Terminology

- **Authentication (AuthN)**: The process of verifying a user's identity.
- **Authorization (AuthZ)**: The process of verifying user permissions.
- **JWT (JSON Web Token)**: Cryptographically signed token format for stateless data exchange.
- **Access Token**: A credential representing delegated access authority, used to access resource APIs.
- **Refresh Token**: A long-lived credential used to request new access tokens when they expire.
- **ID Token**: A token containing authenticated user profile attributes, defined by OpenID Connect.
- **PKCE (Proof Key for Code Exchange)**: Cryptographic binding extension protecting public OAuth clients.
- **mTLS (Mutual TLS)**: Secure connection where both client and server present certificates.
- **Passkey**: Phishing-resistant credential using local biometric devices via WebAuthn.
- **RBAC (Role-Based Access Control)**: Enforcing permissions based on predefined roles.
- **ABAC (Attribute-Based Access Control)**: Enforcing permissions dynamically using subject and environment attributes.
- **Open Policy Agent (OPA)**: Open-source, general-purpose policy engine for centralized authorization.
- **JWKS (JSON Web Key Set)**: Public JSON metadata endpoint listing keys used to verify RS256 signatures.
- **CSRF (Cross-Site Request Forgery)**: Vulnerability where an attacker tricks a user's browser into executing unintended actions on a trusted site using session cookies.
- **XSS (Cross-Site Scripting)**: Security vulnerability where arbitrary scripts are injected into web pages, bypassing cookie and session boundaries.
- **Hashing**: One-way mathematical transformation of passwords into secure strings (e.g. Bcrypt).
- **Salting**: Adding a unique random string to passwords before hashing.
- **Peppering**: Adding a global system-wide secret to passwords before hashing.
- **Identity Provider (IdP)**: Centralized system responsible for managing and authenticating identities.
- **Token Rotation**: Issuing a new refresh token on every token refresh request to detect token theft.
- **Session Hijacking**: Exploit where an attacker steals a user's session ID to masquerade as the authenticated user.

---

## 5. Beginner Examples

### Example 1: Password Hashing and Verification with bcrypt
Plaintext passwords must never touch databases. This example demonstrates hashing and verifying passwords securely using salt rounds.

```python
import bcrypt

def hash_new_password(plaintext_password: str) -> bytes:
    # Encode password to bytes
    password_bytes = plaintext_password.encode('utf-8')
    
    # Generate salt with 12 work factor rounds (takes ~100-300ms)
    salt = bcrypt.gensalt(rounds=12)
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def verify_user_password(plaintext_input: str, stored_hash: bytes) -> bool:
    # Bcrypt extracts salt from the stored hash automatically
    return bcrypt.checkpw(plaintext_input.encode('utf-8'), stored_hash)

# Execution:
raw_pass = "admin_super_secret_123"
stored_db_hash = hash_new_password(raw_pass)
print("Stored DB Hash:", stored_db_hash)

# Matching login attempt
login_success = verify_user_password(raw_pass, stored_db_hash)
print("Login verification result:", login_success)
```

### Example 2: Stateful Session Handling (Flask)
A backend service storing session state in memory (or database-backed cookies) and enforcing authentication gates.

```python
from flask import Flask, session, request, jsonify

app = Flask(__name__)
# Secure secret key used to sign the cookie payload
app.secret_key = "super_secret_session_encryption_key_v1"

# In-memory mock user database
USER_DATABASE = {"admin": "pass_123"}

@app.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")
    
    if username in USER_DATABASE and USER_DATABASE[username] == password:
        # Save session identifier. Flask serializes this into a secure cookie.
        session["user"] = username
        return jsonify({"message": "Session created successfully."}), 200
        
    return jsonify({"error": "Invalid credentials."}), 401

@app.route("/secure-profile", methods=["GET"])
def profile():
    # Verify session presence
    if "user" not in session:
        return jsonify({"error": "Unauthorized session context."}), 401
        
    return jsonify({"profile_info": f"Welcome back, {session['user']}"})
```

### Example 3: Parsing a JWT Payload without Verification (The Danger Zone)
Decoding a base64 JWT payload without checking the signature. This demonstrates why servers must *always* verify signatures.

```python
import base64
import json

def parse_unverified_jwt_payload(jwt_token: str) -> dict:
    """
    Decodes the payload part of a JWT.
    Format is Header.Payload.Signature
    """
    try:
        parts = jwt_token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT format.")
            
        payload_b64 = parts[1]
        
        # Add padding to base64 string if necessary
        padding_needed = len(payload_b64) % 4
        if padding_needed:
            payload_b64 += "=" * (4 - padding_needed)
            
        # Decode base64
        decoded_bytes = base64.urlsafe_b64decode(payload_b64)
        payload_data = json.loads(decoded_bytes.decode('utf-8'))
        return payload_data
    except Exception as e:
        return {"error": f"Failed to parse: {e}"}

# Mock JWT token
mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.SignatureCheckRequired"
print("Decoded Claims:", parse_unverified_jwt_payload(mock_token))
```

---

## 6. Intermediate Examples

### Example 1: JWT Issuance and Verification with RS256
Generating a JWT with asymmetric cryptography (private key for signing, public key for verification) using standard PyJWT library.

```python
import jwt
import datetime
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

# 1. Generate RSA key pair for demonstration (in production, load from vault)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

# Convert private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Convert public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

def issue_access_token(user_id: str, roles: list) -> str:
    now = datetime.datetime.now(datetime.timezone.utc)
    payload = {
        "sub": user_id,
        "roles": roles,
        "iss": "identity_provider_service",
        "aud": "resource_api",
        "exp": now + datetime.timedelta(minutes=15), # Short lived expiration
        "iat": now
    }
    # Sign using the private key
    token = jwt.encode(payload, private_pem, algorithm="RS256")
    return token

def verify_access_token(token: str) -> dict:
    try:
        # Verify using the public key
        decoded_claims = jwt.decode(
            token, 
            public_pem, 
            algorithms=["RS256"], 
            audience="resource_api", 
            issuer="identity_provider_service"
        )
        return decoded_claims
    except jwt.ExpiredSignatureError:
        print("Verification failed: Token signature has expired.")
    except jwt.InvalidSignatureError:
        print("Verification failed: Cryptographic signature mismatch.")
    except jwt.InvalidTokenError as e:
        print(f"Verification failed: {e}")
    return {}

# Execution Check
jwt_token = issue_access_token("user_102", ["editor"])
print("Generated Asymmetric Token:", jwt_token[:80] + "...")
validated = verify_access_token(jwt_token)
print("Validated Sub:", validated.get("sub"))
```

### Example 2: Role-Based Access Control (RBAC) Endpoint Decorator
A python decorator middleware protecting backend routes based on user roles extracted from verified tokens.

```python
from functools import wraps
from flask import request, jsonify

# Simulation of verified request context populated by JWT middleware
def get_current_user_context() -> dict:
    # Mocking authenticated user extraction
    # Normally read from Flask g or request attributes
    return {"user_id": "user_44", "roles": ["editor"]}

def require_permissions(required_role: str):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = get_current_user_context()
            if not user:
                return jsonify({"error": "Unauthenticated access."}), 401
                
            user_roles = user.get("roles", [])
            
            # Authorization Gate
            if required_role not in user_roles and "admin" not in user_roles:
                return jsonify({"error": "Forbidden: Insufficient privileges."}), 403
                
            return f(*args, **kwargs)
        return wrapper
        # Fix: python decorator wraps return name is decorated_function
        return decorated_function
    return decorator

# Example Flask endpoint usage:
# @app.route("/publish", methods=["POST"])
# @require_permissions("editor")
# def publish_article():
#     return "Success"
```

### Example 3: Fetching and Verifying JWTs via JWKS (JSON Web Key Set)
Downstream services dynamically fetching public verification keys from identity servers.

```python
import jwt
from jwt import PyJWKClient

# Mock Auth0 or Okta discovery endpoint
JWKS_ENDPOINT_URL = "https://auth.provider.com/.well-known/jwks.json"

def validate_jwt_against_jwks(token_string: str) -> dict:
    # PyJWKClient automatically downloads and caches keys locally
    jwks_client = PyJWKClient(JWKS_ENDPOINT_URL)
    
    try:
        # Fetch matching key using kid (Key ID) header in JWT
        signing_key = jwks_client.get_signing_key_from_jwt(token_string)
        
        # Verify token using retrieved public key
        payload = jwt.decode(
            token_string,
            signing_key.key,
            algorithms=["RS256"],
            audience="api_identifier"
        )
        return payload
    except Exception as e:
        print("JWKS Verification Failure:", e)
        return {}
```

---

## 7. Advanced Concepts & Examples

### Example 1: Centralized Policy Evaluation with OPA (Open Policy Agent)
Centralizing access control by delegating decisions to a policy engine (OPA) using Rego policy files.

**OPA Rego Policy File (`authz.rego`):**
```rego
package app.authz

# Default deny access
default allow = false

# Allow access if user is admin
allow {
    input.user.roles[_] == "admin"
}

# Allow users to read/write their own profiles
allow {
    input.action == "read"
    input.user.id == input.resource.owner_id
}

# Allow billing department users to read financial reports
allow {
    input.action == "read"
    input.resource.type == "financial_report"
    input.user.department == "billing"
}
```

**Python Policy Execution Wrapper:**
```python
import requests

def query_policy_decision(user_ctx: dict, action: str, resource_ctx: dict) -> bool:
    opa_url = "http://localhost:8181/v1/data/app/authz/allow"
    
    # Structure input query matching Ogo schema expectation
    payload = {
        "input": {
            "user": user_ctx,
            "action": action,
            "resource": resource_ctx
        }
    }
    
    try:
        response = requests.post(opa_url, json=payload, timeout=2.0)
        response.raise_for_status()
        result = response.json()
        
        # OPA returns {"result": true/false}
        return result.get("result", False)
    except requests.exceptions.RequestException:
        # Fail secure if policy engine is unreachable
        return False
```

### Example 2: Sliding Refresh Token Rotation and Redis Blacklisting
Preventing session theft by invalidating the entire token family when a refresh token is reused.

```python
import redis
import uuid
import time

# Initialize Redis connection
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def generate_session_tokens(user_id: str, parent_token_id: str = None) -> dict:
    new_refresh_token = str(uuid.uuid4())
    new_access_token = str(uuid.uuid4()) # In prod, this would be a JWT
    
    # Store token metadata in Redis (expires in 7 days)
    # Key: token:refresh:<token_uuid>
    # Value: user_id, status, parent_token_id
    token_key = f"token:refresh:{new_refresh_token}"
    redis_client.hset(token_key, mapping={
        "user_id": user_id,
        "status": "active",
        "parent_token_id": parent_token_id if parent_token_id else ""
    })
    redis_client.expire(token_key, 604800) # 7 days
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }

def refresh_user_session(old_refresh_token: str) -> dict:
    old_token_key = f"token:refresh:{old_refresh_token}"
    
    # 1. Fetch metadata
    token_data = redis_client.hgetall(old_token_key)
    if not token_data:
        raise ValueError("Invalid refresh token.")
        
    user_id = token_data.get("user_id")
    status = token_data.get("status")
    
    # 2. Check for Token Reuse (Indicates Theft)
    if status == "revoked":
        print(f"SECURITY ALERT: Revoked refresh token reused by user {user_id}. Revoking all family tokens!")
        # Revoke all child tokens using parent relations
        # In production, scan and delete keys belonging to this session tree
        redis_client.delete(old_token_key)
        raise PermissionError("Session revoked due to reuse detection.")
        
    # 3. Mark old token as revoked
    redis_client.hset(old_token_key, "status", "revoked")
    redis_client.expire(old_token_key, 86400) # Keep for 24h to catch late packets
    
    # 4. Issue new token pair
    return generate_session_tokens(user_id, parent_token_id=old_refresh_token)
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate security competence by testing if candidates understand the boundary between authentication and authorization, and if they can identify vulnerabilities in custom authentication code. They look for candidates who design APIs with least privilege principles, secure cookies against XSS/CSRF, handle token rotation properly, and avoid rolling their own cryptography or auth frameworks.

### Red Flags
- **Rolling Custom Crypto**: Proposing custom algorithms to encrypt passwords instead of using standard hashing functions (bcrypt, Argon2).
- **Silent JWT Signature Verification**: Designing API endpoints that parse JWT payloads without verifying signatures.
- **Access Token Persistence in LocalStorage**: Storing long-lived access tokens in browser `localStorage`, exposing them to theft via Cross-Site Scripting (XSS) attacks.
- **Authorization Bypass (IDOR)**: Assuming a request is authorized simply because a user is authenticated (e.g. allowing `GET /api/orders/{id}` without verifying the order belongs to the user).

### Green Flags
- **Defense in Depth**: Combining secure cookie flags (`HttpOnly`, `Secure`, `SameSite`) with CORS headers to secure sessions.
- **Asymmetric Signature Verification (RS256)**: Recommending RS256 over HS256 for microservice architectures to keep the private key secure.
- **PKCE implementation**: Requiring OAuth 2.0 with PKCE for single-page applications and mobile clients.
- **Centralized Policy Decoupling**: Suggesting OPA or similar engines for complex authorization rules instead of embedding IF statements in database queries.

### Answers Matrix
| Level | Question: "Where should you store an access token in a React single-page application?" |
|---|---|
| **Rejected** | "In `localStorage` or `sessionStorage` so it persists when pages reload." |
| **Shortlisted** | "In browser memory (React state) so JavaScript cannot access it, fetching new tokens via a refresh token stored in an HttpOnly cookie." |
| **Selected** | "The most secure method is the **BFF (Backend-For-Frontend) pattern**. The React app communicates with a lightweight BFF server. The BFF manages OAuth tokens and stores them in secure session storage. The browser only receives a secure session cookie (`HttpOnly`, `Secure`, `SameSite=Strict`), protecting the tokens from XSS theft." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is the difference between Authentication and Authorization?
- **Detailed Answer**:
- **Authentication (AuthN)**: Verifies the identity of a client. It answers "Who are you?". Examples include validating a username and password, verifying a signature on a TLS certificate, or checking a fingerprint.
- **Authorization (AuthZ)**: Verifies access permissions. It answers "What are you allowed to do?". Examples include checking if a user has admin permissions, verifying resource ownership, or evaluating a access policy.
- *AuthN must occur before AuthZ can be evaluated.*
- **Follow-up Questions**: Can a request be authenticated but not authorized? (Answer: Yes. A user can log in successfully but be blocked when trying to access administrator resources).
- **Interviewer's Expectations**: Define both terms clearly and detail their dependencies.

#### 2. Compare Session-based Authentication and JWT Authentication.
- **Detailed Answer**:
- **Session-based (Stateful)**:
  - *Mechanism*: Server generates a session record in a database or Redis cache and returns the session ID in a cookie. The server must look up the session state on each request.
  - *Pros*: Easy to revoke sessions instantly; cookies are automatically managed by browsers.
  - *Cons*: Difficult to scale horizontally; requires shared cache databases.
- **JWT (Stateless)**:
  - *Mechanism*: Server encodes user data inside the token, signs it, and returns it. The server validates the token signature offline without database reads.
  - *Pros*: Scalable; works across different domains; no server-side session lookup.
  - *Cons*: Revocation is difficult before expiration; tokens cannot be easily invalidated; larger payload size.
- **Follow-up Questions**: How do you handle JWT revocation? (Answer: Keep access token lifetimes short, and store revoked tokens in a Redis blacklist cache until they expire).
- **Interviewer's Expectations**: Compare scalability, revocation capabilities, storage requirements, and security risks.

#### 3. What is JWT? Describe its three parts.
- **Detailed Answer**: A JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact, self-contained way for securely transmitting information between parties. It consists of:
1. **Header**: Base64URL-encoded JSON containing the signing algorithm (e.g. HS256, RS256) and token type (JWT).
2. **Payload**: Base64URL-encoded JSON containing claims. Claims can be registered (`sub`, `iss`, `exp`), public, or private custom claims (e.g. `roles`).
3. **Signature**: Computed by taking the encoded header, encoded payload, and signing them using a secret/private key with the specified algorithm. Used to verify token integrity.
- **Follow-up Questions**: Is the payload encrypted in a standard JWT? (Answer: No, it is only base64 encoded. Anyone can decode and read the claims, so sensitive data like passwords or credit cards must never be stored in the payload).
- **Interviewer's Expectations**: Enumerate all three parts and explain base64 encoding vs. cryptographic signing.

#### 4. Explain the difference between OAuth 2.0 and OpenID Connect (OIDC).
- **Detailed Answer**:
- **OAuth 2.0**: An **authorization framework** designed to grant third-party applications limited access to HTTP resources (APIs) on behalf of a user. It does not verify user identity. It returns an **Access Token** designed for APIs to read.
- **OpenID Connect (OIDC)**: An **identity layer** built on top of OAuth 2.0. It adds authentication capabilities, allowing clients to verify the identity of the user. It returns an **ID Token** (a JWT containing user profile details like name and email) designed for the client application to read.
- **Follow-up Questions**: What is the /.well-known/openid-configuration endpoint? (Answer: A discovery endpoint exposing metadata about the identity provider, listing support scopes, token endpoints, and the JWKS URI).
- **Interviewer's Expectations**: Differentiate authorization delegation (OAuth) from identity verification (OIDC).

#### 5. Why is PKCE needed, and how does it work?
- **Detailed Answer**: Public clients (like SPAs and mobile apps) cannot protect client secrets because their source code is accessible to users. In the standard Authorization Code Flow, an attacker could intercept the authorization code returned by the server and exchange it for an access token.
**PKCE (Proof Key for Code Exchange)** solves this:
1. The client generates a random secret called a `code_verifier`, hashes it using SHA-256 to create a `code_challenge`, and sends the challenge with the initial authorization request.
2. The authorization server saves the challenge and returns the authorization code.
3. The client sends the authorization code along with the plaintext `code_verifier` to exchange it for tokens.
4. The server hashes the verifier and matches it against the saved challenge. An attacker who intercepted the authorization code lacks the verifier, so they cannot exchange the code for tokens.
- **Follow-up Questions**: Can PKCE be used for confidential server-side clients? (Answer: Yes, it is recommended for all clients to protect against authorization code injection attacks).
- **Interviewer's Expectations**: Identify public client limits, explain the code verifier/challenge relationship, and trace the verification step.

#### 6. Compare RBAC and ABAC access control models.
- **Detailed Answer**:
- **RBAC (Role-Based Access Control)**: Access is determined by roles assigned to users (e.g., `user.role == 'manager'`).
  - *Pros*: Simple to design, audit, and maintain.
  - *Cons*: Coarse-grained; leads to "role explosion" when custom permissions are needed (e.g., creating `manager_us_east`, `manager_us_west`).
- **ABAC (Attribute-Based Access Control)**: Access is determined dynamically by evaluating attributes of the user, resource, and environment against policies (e.g., `allow if user.role == 'manager' and resource.region == user.region and time.hour >= 9`).
  - *Pros*: Highly granular; scalable authorization rules.
  - *Cons*: Complex setup; higher processing latency.
- **Follow-up Questions**: How would you implement ABAC on a database query? (Answer: Translate policy attributes into SQL query parameters dynamically, e.g. appending `WHERE region = :user_region`).
- **Interviewer's Expectations**: Compare granularity, scalability, complexity, and explain the dynamic policy evaluation model of ABAC.

#### 7. How do you store passwords securely in a database?
- **Detailed Answer**:
1. **Never store plaintext or reversible encryption**.
2. **Use adaptive, compute-intensive hashing algorithms** designed to resist brute-force attacks (e.g. Argon2id, Bcrypt, or Scrypt).
3. **Use unique salts**: Generate a cryptographically secure random salt for every user, appending it to the password before hashing to prevent rainbow table attacks.
4. **Use a pepper**: Append a system-wide secret key (stored in a secure environment vault, separate from the database) before hashing.
5. **Tune work factors**: Configure hashing iteration counts so that a single validation takes 100-300ms, making brute-forcing slow for attackers without impacting user login latency.
- **Follow-up Questions**: Why is MD5 or SHA-256 unsuitable for password storage? (Answer: They are too fast; an attacker can compute billions of SHA-256 hashes per second using GPUs to crack passwords).
- **Interviewer's Expectations**: Reject simple hashes, recommend adaptive algorithms, and explain the roles of salts and peppers.

#### 8. What is CSRF and how do you protect against it?
- **Detailed Answer**: CSRF (Cross-Site Request Forgery) is an attack where a malicious site tricks a user's browser into performing actions on a trusted site where the user is currently authenticated. Since browsers automatically append session cookies to requests, the malicious request executes with the user's permissions.
**Protection**:
1. **SameSite Cookie Attribute**: Set cookies to `SameSite=Lax` or `SameSite=Strict` so the browser does not send them on cross-site requests.
2. **Anti-CSRF Tokens**: The server generates a unique, cryptographically random token, associates it with the user's session, and embeds it in the HTML form. The server rejects incoming state-changing requests if the token is missing or invalid.
3. **Custom Headers**: Force requests to include custom headers (e.g., `X-Requested-With`), which browser cross-origin policies prevent malicious sites from setting without CORS approval.
- **Follow-up Questions**: Does CSRF affect JWTs sent via the Authorization header? (Answer: No, because browser cookies are appended automatically by the browser, whereas custom Authorization headers must be set manually by JavaScript code).
- **Interviewer's Expectations**: Define the attack vector (session cookie auto-appending) and propose SameSite and anti-CSRF token solutions.

#### 9. What is XSS and how does it impact authentication security?
- **Detailed Answer**: XSS (Cross-Site Scripting) occurs when an application vulnerability allows an attacker to inject and execute malicious JavaScript code in a user's browser.
**Impact on Auth**:
- If access tokens or session IDs are stored in browser memory accessible to JavaScript (e.g., `localStorage`, `sessionStorage`, or standard cookies), the injected script can access and send them to the attacker's server (session hijacking).
**Prevention**:
- Store session identifiers and tokens in `HttpOnly` cookies, which blocks JavaScript read access.
- Sanitize and escape all user-supplied inputs before rendering them in the HTML DOM.
- Configure a Content Security Policy (CSP) header to restrict script sources.
- **Follow-up Questions**: If an auth token is stored in an `HttpOnly` cookie, is it safe from XSS? (Answer: The token cannot be stolen directly, but the attacker can still perform actions on behalf of the user using the open session (XSS session ride-along)).
- **Interviewer's Expectations**: Explain script injection, token theft vectors, and the mitigation provided by `HttpOnly` cookies.

#### 10. How does mTLS function, and when should you choose it?
- **Detailed Answer**: Mutual TLS (mTLS) extends standard TLS by authenticating both parties:
1. The client connects to the server and validates the server's certificate (standard TLS).
2. The server requests the client's certificate.
3. The client presents its certificate, and the server validates it against a trusted CA.
- **When to choose**: Best for machine-to-machine communication, e.g., service-to-service calls inside a microservice network, or connecting to financial payment backends, where certificate distribution can be managed automatically.
- **Follow-up Questions**: Why is mTLS not used for public web browsers? (Answer: Managing and installing client certificates in thousands of user browsers is impractical and creates poor user experience).
- **Interviewer's Expectations**: Detail the bi-directional handshake and identify microservices and machine communication as primary use cases.

---

### Scenario-Based Questions

#### 11. Design a Single Sign-On (SSO) architecture for a company using OIDC.
- **Detailed Answer**:
- **Identity Provider (IdP)**: Implement a centralized IdP (e.g. Okta or Keycloak) that manages the user directory.
- **Client Registration**: Register all company applications (Slack, HR Portal, Email) as Clients in the IdP, configuring redirect URIs.
- **Workflow**:
  1. The user navigates to `HR Portal` and clicks login.
  2. HR Portal redirects the browser to the IdP authorization endpoint: `/authorize?response_type=code&scope=openid profile&client_id=hr_app&redirect_uri=https://hr.company.com/callback`.
  3. The user authenticates at the IdP (e.g. entering credentials and verifying MFA).
  4. The IdP returns an authorization code via redirect to HR Portal's callback.
  5. HR Portal exchanges the code for an Access Token and an ID Token (JWT) at the IdP token endpoint.
  6. HR Portal reads the ID Token claims to log the user in locally.
  7. When the user visits `Slack`, the application redirects to the IdP. The IdP detects the active SSO session cookie in the browser and issues tokens for Slack immediately, bypassing the login prompt.
- **Follow-up Questions**: How does Single Logout (SLO) work? (Answer: The client triggers a logout request to the IdP, which redirects to all registered clients to clear their local sessions).
- **Interviewer's Expectations**: Detail IdP redirection, OIDC token exchange (ID tokens), and browser-based session recognition.

#### 12. Design a rate-limiting and lockout strategy to protect your login endpoint from brute-force attacks.
- **Detailed Answer**:
- **Rate Limiting**: Enforce a strict rate limit of 5 login attempts per IP address per minute using a Redis-backed sliding window.
- **Account Lockout**:
  - If a specific user account (e.g., `alice@example.com`) fails login 5 consecutive times, set a block in Redis: `Key: lockout:user:alice@example.com, Value: blocked` with an expiry of 15 minutes.
  - Return a generic error message: "Invalid credentials or account locked. Please try again later" to prevent username enumeration.
- **IP Captcha Challenge**: If an IP generates high volumes of failed login attempts across different usernames, prompt a Captcha challenge (e.g., reCAPTCHA) before processing the credentials.
- **Follow-up Questions**: How do you prevent Denial of Service (DoS) where an attacker intentionally locks out legitimate users? (Answer: Use progressive delays, e.g., waiting 5s, 30s, 5m on consecutive failures, instead of complete lockouts, or verify identity via email link verification).
- **Interviewer's Expectations**: Propose IP rate limits, account lockouts, progressive backoffs, and generic error messages.

#### 13. Design a secure communication channel between microservices in an enterprise network.
- **Detailed Answer**:
- **mTLS Service Mesh**: Use a service mesh (like Istio or Linkerd) to enforce mTLS between all microservice containers automatically, offloading encryption and certificate management from application code.
- **Identity Validation (SPIFFE)**: Authenticate services using SPIFFE IDs embedded in certificate Subject Alternative Names (SANs) (e.g., `spiffe://domain/ns/prod/sa/order-service`).
- **Authorization Policies**: Enforce least-privilege access rules at the proxy level:
  ```yaml
  apiVersion: security.istio.io/v1beta1
  kind: AuthorizationPolicy
  spec:
    selector:
      matchLabels:
        app: payment-service
    rules:
    - from:
      - source:
          principals: ["cluster.local/ns/prod/sa/order-service"]
      to:
      - operation:
          methods: ["POST"]
          paths: ["/charges"]
  ```
- **Follow-up Questions**: What happens if the service mesh proxy is compromised? (Answer: The attacker gains access only to the network permissions of that specific container node; traffic is still isolated from other parts of the mesh).
- **Interviewer's Expectations**: Recommend mTLS, automated CA issuance, and policy-based access control rules.

#### 14. Your multi-tenant SaaS application needs to enforce tenant isolation. How do you implement this in your authorization code?
- **Detailed Answer**:
- **Claim Injection**: Inject the user's `tenant_id` into their JWT token claims at login.
- **Middleware Assertion**: Create an authorization filter that intercepts all API requests:
  1. Extract `tenant_id` from the verified JWT claims.
  2. Extract `tenant_id` from the target resource URL (e.g., `/api/v1/tenants/{tenant_id}/projects`) or query context.
  3. Deny the request immediately if they do not match.
- **Database Scope Enforcement**: Use Row-Level Security (RLS) in the database (e.g., PostgreSQL). Set a tenant session variable on the database connection and write policies that filter rows based on `tenant_id`, preventing data leaks even if application code fails.
- **Follow-up Questions**: What is an IDOR attack? (Answer: Insecure Direct Object Reference; a vulnerability where an attacker accesses other tenants' data by changing ID parameters in requests, prevented by checking tenant ownership).
- **Interviewer's Expectations**: Suggest JWT claim checks, API gateway mapping validations, and database Row-Level Security.

#### 15. Design a passwordless authentication flow using email magic links.
- **Detailed Answer**:
- **Initiation**: The user enters their email (e.g. `user@example.com`) and clicks "Send Link".
- **Token Generation**:
  1. Generate a secure, cryptographically random token (UUIDv4 or a signed JWT).
  2. Store the token in Redis with key: `magic:token:<token>` and value: `user@example.com`, set to expire in 10 minutes.
  3. Send an email containing the URL: `https://app.com/login/verify?token=<token>`.
- **Verification**:
  1. The user clicks the link. The browser sends a GET request to the verify endpoint.
  2. The server queries Redis for the token.
  3. If found, retrieve the email, delete the token from Redis (to ensure single use), generate session credentials (JWT or session cookie), and redirect the user to the dashboard.
- **Follow-up Questions**: How do you prevent link pre-fetching by email scanners from logging the user in and invalidating the token? (Answer: The email link should redirect to a confirmation page with a "Verify Login" button that makes a POST request to complete the login, preventing automated GET scans from invalidating the token).
- **Interviewer's Expectations**: Propose secure tokens, single-use mechanisms (immediate delete), short lifetimes, and POST validations to prevent pre-fetching.

---

### Debugging Questions

#### 16. A client reports that their JWT authentication fails intermittently. How do you debug this?
- **Detailed Answer**:
1. **Clock Skew (Time Drift)**: Compare the system time of the authentication server and the resource server. If the resource server's clock is ahead of the authentication server's clock, it may reject newly issued tokens as not yet valid (`nbf` claim) or expired (`exp` claim). Add a clock skew tolerance (e.g., 60 seconds) during token validation.
2. **JWKS Cache Expiry**: If the identity provider rotates signing keys, the resource server's cached JWKS keys may become stale. Check if the server is failing to fetch new keys when a signature validation fails.
3. **Load Balancer Routing**: If symmetric keys (HS256) are used, check if one server node in the cluster has an incorrect secret key config.
- **Follow-up Questions**: How do you fix time drift issues in Docker containers? (Answer: Sync host and container clocks using NTP services).
- **Interviewer's Expectations**: Identify clock skew (clock drift), JWKS caching, and key synchronization issues as common causes of intermittent auth failures.

#### 17. After deploying a new version of your backend application, all users are logged out. Explain the cause and fix.
- **Detailed Answer**:
- **Cause**: The application is likely using stateful sessions stored in-memory (local RAM) on the server instance. When the server restarted during deployment, the memory space was cleared, destroying all session records and forcing clients to re-login.
- **Fix**: Move session storage from server memory to a persistent, distributed cache (e.g., Redis) or a database:
  ```python
  # Configure session interface to use Redis
  app.config['SESSION_TYPE'] = 'redis'
  app.config['SESSION_REDIS'] = redis.Redis(host='redis-server', port=6379)
  ```
- **Follow-up Questions**: What is the alternative stateless fix? (Answer: Switch to JWT tokens. Since JWTs store session data on the client and are verified using cryptographic keys, deploying new backend code does not invalidate sessions as long as the keys remain the same).
- **Interviewer's Expectations**: Identify in-memory session loss and recommend distributed caching (Redis) or stateless tokens.

#### 18. A user finds that by decoding the JWT access token, they can view their username and user ID. They report this as a data breach. How do you respond?
- **Detailed Answer**: I will explain that this is expected behavior. JWTs are designed to be **digitally signed to guarantee integrity**, but they are **not encrypted to guarantee confidentiality** (unless JWE is used). Any client can decode base64 strings to read the payload claims. Because of this, it is standard security practice never to store sensitive private data (like passwords, credit cards, or private PII) inside the JWT payload. The token only contains identifier claims (like user ID) needed to route requests.
- **Follow-up Questions**: How do you ensure the token was not tampered with? (Answer: The server validates the cryptographic signature using the secret or public key before trusting the claims).
- **Interviewer's Expectations**: Explain the difference between encryption and signing, and reiterate that sensitive data should not be stored in JWT payloads.

#### 19. A developer reports that when they add the Authorization header to API calls, their browser blocks the request with a CORS error. Explain and fix.
- **Detailed Answer**:
- **Explanation**: Adding a custom header (like `Authorization`) makes the request a "non-simple request" under CORS rules. The browser must send a preflight `OPTIONS` request to verify the server allows custom headers. The server is likely returning a CORS error because it is not configured to accept the `OPTIONS` method or lacks the authorization header allowance rules.
- **Fix**: Configure the server to handle OPTIONS requests and return:
  ```http
  Access-Control-Allow-Headers: Authorization, Content-Type
  Access-Control-Allow-Methods: GET, POST, OPTIONS
  ```
- **Follow-up Questions**: Should authorization middleware run on preflight OPTIONS requests? (Answer: No. Preflight requests do not carry credentials, so running auth checks on OPTIONS will cause 401 errors. Bypass auth checks for OPTIONS methods).
- **Interviewer's Expectations**: Explain preflight requirements for custom headers and specify the configuration changes needed to resolve the block.

#### 20. Your application uses asymmetric keys (RS256) for token signing. A security scan reports that your JWKS endpoint is returning expired keys. What are the operational impacts and fixes?
- **Detailed Answer**:
- **Impacts**: Downstream microservices that validate JWT signatures against the JWKS endpoint will reject incoming user tokens, resulting in application-wide authentication failures.
- **Fix**:
  1. Check the key rotation cron job. Ensure the private key rotation script is running and successfully publishing the new public keys to the JWKS endpoint.
  2. Implement grace periods during rotation: keep the old public key active on the JWKS endpoint for a duration (e.g. 24 hours) after the new key is deployed, allowing old tokens to expire naturally without authentication failures.
- **Follow-up Questions**: What claims in the JWKS determine key matching? (Answer: The `kid` (Key ID) header in the JWT matches the `kid` property of the target key in the JWKS list).
- **Interviewer's Expectations**: Identify token verification failures and outline how to implement key rotation grace periods.

---

### System Design Questions

#### 21. Design a secure microservices authentication and authorization architecture for a banking application.
- **Detailed Answer**:
- **Edge Security**: Deploy an API Gateway (e.g., Kong) at the edge. The gateway validates external user requests (OAuth 2.0 / JWT) and terminates TLS.
- **Identity Propagation**: The gateway translates external user tokens into short-lived, internal transit JWTs signed by a private key. The gateway attaches this token as a header (e.g., `X-Transit-Token`) before forwarding the request internally.
- **Service-to-Service Security**: Enforce mutual TLS (mTLS) using a service mesh (e.g. Istio) to secure communication between internal microservices.
- **Authorization**:
  - DOWNSTREAM: Individual microservices extract the user's scopes and tenant IDs from the transit token.
  - Granular permissions (e.g., verifying if a user is allowed to transfer funds from a specific account) are evaluated by querying a centralized policy service (like OPA).
- **Follow-up Questions**: Why not pass the original user JWT directly between microservices? (Answer: Because if one microservice is compromised, it could abuse the original user token to call other services; short-lived, scoped transit tokens limit the attack surface).
- **Interviewer's Expectations**: Detail edge API gateways, transit token wrappers, mTLS service meshes, and granular policy evaluations.

#### 22. Design a passwordless authentication system using passkeys (WebAuthn).
- **Detailed Answer**:
- **Registration Flow**:
  1. The user clicks "Register Passkey" in the client app.
  2. The server generates a random challenge, user ID, and registration parameters, saving them in a cache.
  3. The client calls the browser's credential API: `navigator.credentials.create()`. The browser prompts the user for biometrics.
  4. The device generates an asymmetric key pair. The private key is saved in the device's secure enclave.
  5. The client sends the public key, credential ID, and a cryptographic signature of the challenge back to the server.
  6. The server verifies the signature against the saved challenge and stores the `credential_id` and `public_key` in the database associated with the user account.
- **Authentication Flow**:
  1. The user enters their username and clicks "Login with Passkey".
  2. The server retrieves the user's `credential_id` and generates a new random challenge.
  3. The client calls: `navigator.credentials.get()`. The browser prompts the user for biometrics.
  4. The device private key signs the challenge. The client sends the signature to the server.
  5. The server verifies the signature using the stored public key and logs the user in.
- **Follow-up Questions**: Why are passkeys immune to phishing? (Answer: The browser enforces that the WebAuthn API only releases signatures if the request origin matches the domain bound to the credential).
- **Interviewer's Expectations**: Detail public-key registration and authentication steps, biometrics integration, and origin security bindings.

#### 23. Design a secure secrets management system for microservices, ensuring applications never expose API keys or database passwords.
- **Detailed Answer**:
- **Decoupled Vault**: Use a dedicated secrets manager (e.g., HashiCorp Vault, AWS Secrets Manager, or Google Cloud Secret Manager).
- **Service Identity**: Bind microservices to secure identities (e.g., Kubernetes Service Accounts or AWS IAM Roles).
- **Authentication**: When a microservice starts up, it authenticates with the Secrets Vault using its IAM identity token, receiving a short-lived Vault Token.
- **Runtime Access**: The microservice requests secrets from the Vault at startup, loading them directly into environment variables or memory. Secrets must never be committed to Git repositories or written to log files.
- **Dynamic Secrets & Rotation**: Configure the Vault to automatically generate temporary database credentials (e.g., valid for 1 hour) and rotate API keys periodically.
- **Follow-up Questions**: What is the risk of loading secrets into environment variables? (Answer: If a vulnerability allows an attacker to dump process environment variables or read `/proc/self/environ`, the secrets are compromised; loading secrets into memory-mapped files is more secure).
- **Interviewer's Expectations**: Reject hardcoded configs, recommend dedicated vault managers, IAM integration, and dynamic rotation.

---

## 10. Common Mistakes

- **Storing Plaintext Passwords or Reversible Hashes**: Using MD5, SHA-1, or simple encryption to store passwords, allowing attackers to read them if the database is compromised.
- **Parsing JWTs without verifying signatures**: Reading payload claims without running cryptographic checks first, which allows clients to bypass authorization gates by forging claims.
- **Storing sensitive data in local storage**: Storing access tokens or PII in `localStorage`, where they are vulnerable to theft via XSS attacks.
- **Missing Token Expiration**: Issuing access tokens without an expiration date, which makes them permanently valid if stolen.
- **Lack of IDOR Verification**: Verifying user identity (AuthN) but failing to verify if the authenticated user owns the resource they are requesting (AuthZ).

---

## 11. Comparison Section: Stateful Sessions vs. Stateless JWTs vs. mTLS

| Feature | Stateful Sessions | Stateless JWTs | Mutual TLS (mTLS) |
|---|---|---|---|
| **State Storage** | Server-side (cache/Redis) | Client-side (encrypted payload) | None (identity is in certificate) |
| **Revocation Speed** | Instant (delete session key) | Slow (must wait for token expiry) | Instant (using CRL or OCSP revocation) |
| **Scale Limits** | Moderate (shares DB/cache access) | High (verification is offline) | High (verification is inline TLS) |
| **CSRF Vulnerability** | High (if using cookies) | Low (if passed via headers) | None (machine-to-machine) |
| **XSS Vulnerability** | Low (if using HttpOnly cookies) | High (if stored in JS memory) | None (certificates are isolated) |
| **Best For** | Standard web apps, user portals. | SPA clients, mobile apps, public APIs. | Microservices, secure server networks. |

---

## 12. Practical Project Ideas

### Beginner: Secure Login System with Bcrypt Hashing
Build a registration and login server in Python using Flask or FastAPI. Store user records in a local database (like SQLite), hashing passwords with Bcrypt. Protect routes by checking session cookies and return a generic login error for invalid credentials.

### Intermediate: JWT Auth Service with Role-Based Middleware
Create an API that issues RS256-signed JWT access tokens (15m expiry) and UUID-based refresh tokens. Write a custom python decorator to verify access tokens and restrict API routes to specific roles (Viewer, Editor, Admin). Store revoked refresh tokens in a Redis blacklist.

### Advanced/Resume-worthy: Decentralized Policy-Based Microservices Mesh
Deploy three microservices using Docker Compose. Centralize access control using Open Policy Agent (OPA). Configure mTLS between services and route all authorization checks to OPA sidecar containers to evaluate permissions dynamically.

---

## 13. Internship Preparation Notes

- **Recruiters focus on**: The differences between authentication and authorization, standard password storage practices (hashing + salting), and security vulnerabilities (XSS, CSRF).
- **Engineering Teams expect**: Hands-on experience implementing session or JWT authentication, configuring secure cookie flags, and checking user permissions before performing database operations.

---

## 14. Cheat Sheet

- **AuthN vs. AuthZ**: AuthN = Identity (Who). AuthZ = Permissions (What).
- **Password storage**:
  - Hashing (Bcrypt/Argon2) = Yes.
  - Encryption/MD5 = No.
- **Secure Cookie Flags**:
  - `HttpOnly`: Mitigates XSS.
  - `Secure`: Mitigates plaintext leaks.
  - `SameSite`: Mitigates CSRF.
- **JWT Parts**: Header (alg, typ) $\to$ Payload (claims) $\to$ Signature (integrity).

---

## 15. One-Day Revision Guide

- [ ] Explain the difference between stateful sessions and stateless tokens.
- [ ] Draw the message flow of OAuth 2.0 with PKCE.
- [ ] Detail the structure and verification steps of a JWT.
- [ ] Describe how to protect against XSS and CSRF attacks.
- [ ] Explain how mTLS secures service-to-service communication.
