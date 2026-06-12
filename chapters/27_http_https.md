# 27. HTTP/HTTPS (Web Protocol Deep Dive)

## 1. Introduction

### What it is
HTTP (Hypertext Transfer Protocol) is an application-layer protocol in the Internet Protocol Suite (IP) used to transmit hypermedia documents, such as HTML, images, and API payloads. HTTPS (HTTP Secure) is an extension of HTTP where communication is encrypted using TLS (Transport Layer Security) or its predecessor, SSL (Secure Sockets Layer), protecting data transit over public networks.

### Why it exists
HTTP was originally designed in 1989 (HTTP/0.9) as a simple, stateless protocol to retrieve static HTML pages from servers. As the internet evolved into a commercial platform for financial transactions, health services, and personal communication, transmitting raw text became a massive security risk. HTTPS was developed to integrate cryptographic mechanisms into the transport layer, ensuring that data moving between client and server remains private, unaltered, and verified.

### Problems it solves
- **Eavesdropping (Packet Sniffing)**: Prevents adversaries from intercepting Wi-Fi or router packets to steal passwords, session cookies, and private API data.
- **Data Tampering (Man-in-the-Middle Attacks)**: Prevents intermediate proxies or ISP routers from injecting advertisements, malware, or malicious scripts into the HTTP response.
- **Server Impersonation (Phishing)**: Authenticates server identity using digital certificates, proving that the client is connected to the real domain rather than an attacker's server.
- **Latency and Head-of-Line Blocking**: Addresses performance limits of older protocol versions (like HTTP/1.1's limit of 6 TCP connections) through multiplexing (HTTP/2) and connection migration (HTTP/3).

### Industry Use Cases
- **Enterprise Web Access**: All modern browsers restrict or display security warnings for sites not serving content over HTTPS.
- **PCI-DSS Compliance**: E-commerce checkouts and financial processing services must run exclusively over HTTPS.
- **Securing JWTs and Auth Sessions**: Cookies containing credentials or session IDs must be transmitted via HTTPS to prevent session hijacking.
- **CDN Edge Acceleration**: CDNs use HTTPS edge servers to cache static files close to users, terminating TLS sessions at the edge to reduce origin server load.

### Analogy
HTTP is a postcard: anyone handling it along its postal route can read the text, copy it, or write over it. HTTPS is a secure, armored envelope signed with a wax seal (digital certificate). If the envelope is intercepted, the contents cannot be read, and if the seal is broken or tampered with, the recipient immediately detects the compromise and rejects the delivery.

---

## 2. Core Concepts

### Beginner Concepts
- **Request/Response Model**: Communication is initiated by a client (e.g. browser) sending an HTTP Request. The server processes it and returns an HTTP Response.
- **URI/URL Structure**:
  ```text
  https://example.com:443/v1/users?status=active#profile
  |__/_  |__________/ |_/ |_______/ |____________/ |______/
  Scheme      Host     Port   Path    Query Params  Fragment
  ```
- **HTTP Header Metadata**: Key-value pairs containing control instructions:
  - `Host`: Specifies the domain name of the server (critical for virtual hosting on shared IPs).
  - `User-Agent`: Identifies the client software (browser, version, OS) making the request.
  - `Content-Type`: Dictates the MIME type of the payload (e.g. `application/json`, `text/html`).
- **HTTP Status Code Families**:
  - `1xx`: Informational (e.g. `101 Switching Protocols` for WebSockets).
  - `2xx`: Success (e.g. `200 OK`, `201 Created`).
  - `3xx`: Redirection (e.g. `301 Moved Permanently`, `304 Not Modified`).
  - `4xx`: Client Errors (e.g. `400 Bad Request`, `401 Unauthorized`, `404 Not Found`).
  - `5xx`: Server Errors (e.g. `500 Internal Error`, `503 Service Unavailable`).

### Intermediate Concepts
- **HTTP/1.1 Persistent Connections**: Reuses a single TCP socket connection for multiple requests (`Connection: keep-alive`), eliminating the CPU and latency overhead of repeating the 3-way TCP handshake ($SYN \to SYN-ACK \to ACK$) for every image or stylesheet.
- **HTTP/2 Multiplexing & Binary Framing**: Replaces text-based parser lines with binary frames. Introduces **Streams**, allowing a client to send hundreds of requests concurrently over a single TCP connection without waiting for responses in order. This eliminates HTTP-level Head-of-Line blocking.
- **HTTP/3 QUIC Transport**: Replaces TCP with **QUIC** (Quick UDP Internet Connections) running over UDP. QUIC integrates TLS 1.3 directly into the connection handshake, providing packet-level recovery, which resolves TCP-level Head-of-Line blocking (where a single dropped packet stalls all streams).
- **CORS Preflight (OPTIONS)**: When a web page requests resource mutations from another origin, the browser sends an `OPTIONS` request. The browser only proceeds with the actual request if the server's preflight response contains headers permitting the origin, method, and headers.
- **Cookie Flags**:
  - `Secure`: Cookie is transmitted only over encrypted HTTPS connections.
  - `HttpOnly`: Blocks browser-side JavaScript from accessing the cookie, mitigating Cross-Site Scripting (XSS) token theft.
  - `SameSite`: Controls if cookies are sent with cross-site requests. Options: `Strict` (never sent on cross-site requests), `Lax` (sent only on top-level GET navigations), `None` (sent on all requests, requires `Secure`).

### Advanced Concepts
- **ALPN (Application-Layer Protocol Negotiation)**: An extension to TLS where the client and server negotiate which protocol version (HTTP/1.1, HTTP/2, HTTP/3) to use during the initial secure handshake, avoiding additional round trips.
- **OCSP Stapling**: Solves slow certificate revocation checks. Instead of the client querying the Certificate Authority (CA) to check if a server's certificate is revoked, the server queries the CA periodically and "staples" a time-stamped digital signature of the status to the TLS handshake.
- **HSTS (HTTP Strict Transport Security)**: A response header (`Strict-Transport-Security: max-age=31536000; includeSubDomains`) instructing the browser to automatically convert all future HTTP requests to HTTPS before transmitting any data over the network.
- **Certificate Pinning**: Hardcoding the expected public key hash of the server's certificate inside a client application (common in mobile apps), preventing connection if an attacker attempts to substitute a certificate issued by a compromised Certificate Authority.
- **Connection Coalescing**: Allows an HTTP/2 client to reuse an existing open TCP connection for a different origin if the domain resolves to the same IP address and the connection's TLS certificate covers both hostnames.
- **TLS 1.3 Handshake Optimization**: Reduces handshake latency from 2 Round Trips (2-RTT) in TLS 1.2 to 1-RTT. It achieves this by combining key exchange and cipher negotiation into a single step, while dropping support for weak cryptographic algorithms like MD5, RC4, and static RSA.

---

## 3. Internal Working

### Cryptographic Handshakes (TLS 1.2 vs. TLS 1.3)

#### TLS 1.2 Handshake (2-RTT)
The TLS 1.2 handshake requires two round-trip times (RTT) to establish keys and verify identity before encrypted application data can be sent. It relies on explicit cipher negotiation steps.

```text
Client                                  Server
  |                                       |
  | -------- 1. ClientHello ------------> | (Sends supported cipher suites, random bytes, SNI)
  | <------- 2. ServerHello ------------- | (Chooses cipher suite, sends server random bytes)
  | <------- 3. Certificate ------------- | (Sends SSL/TLS certificate chain)
  | <------- 4. ServerKeyExchange ------- | (Sends Diffie-Hellman parameters, signed by private key)
  | <------- 5. ServerHelloDone --------- |
  | -------- 6. ClientKeyExchange ------> | (Sends client DH public parameters)
  | -------- 7. ChangeCipherSpec -------->| (Signals transition to encrypted mode)
  | -------- 8. Finished ---------------> | (Verifies handshake integrity)
  | <------- 9. ChangeCipherSpec -------- |
  | <------- 10. Finished --------------- |
  v                                       v
[================ Encrypted Session Data ===============]
```

#### TLS 1.3 Handshake (1-RTT)
TLS 1.3 streamlines this process by assuming the client will use a modern key exchange algorithm (like Elliptic-Curve Diffie-Hellman). The client sends its public key share in the first message.

```text
Client                                  Server
  |                                       |
  | -------- 1. ClientHello ------------> | (Sends cipher suites, random bytes, and public Key Share)
  | <------- 2. ServerHello ------------- | (Chooses cipher suite, returns server public Key Share)
  | <------- 3. EncryptedExtensions ----- | (Configures protocol constraints)
  | <------- 4. Certificate ------------- | (Sends certificate chain, encrypted)
  | <------- 5. CertificateVerify ------- | (Proves ownership of private key via signature)
  | <------- 6. Finished ---------------- | (Verifies handshake integrity)
  v                                       v
[================ Encrypted Session Data ===============]
```

*Mathematical Diffie-Hellman Key Exchange Concept*:
During the key exchange, both parties agree on a prime $p$ and base $g$. The client generates private key $a$ and sends public share $A = g^a \pmod p$. The server generates private key $b$ and sends public share $B = g^b \pmod p$.
Both compute the shared secret $S$:
$$S = B^a \pmod p = (g^b)^a \pmod p = g^{ab} \pmod p$$
$$S = A^b \pmod p = (g^a)^b \pmod p = g^{ab} \pmod p$$
An eavesdropper only intercepts $A$ and $B$, but cannot compute $S$ without solving the discrete logarithm problem.

### HTTP/2 Binary Framing
In HTTP/1.x, requests are parsed as ASCII text lines separated by carriage returns. If a header is malformed, parsing breaks.
HTTP/2 compiles headers and data into **Binary Frames**. Every communication is split into frames, which are multiplexed over a single TCP stream.

```text
HTTP/2 Binary Frame Structure:
+-----------------------------------------------+
|                 Length (24-bit)               |
+---------------+---------------+---------------+
|  Type (8-bit) | Flags (8-bit) |
+---------------+---------------+---------------+
|R|            Stream Identifier (31-bit)       |
+-----------------------------------------------+
|                   Frame Payload               |
+-----------------------------------------------+
```
- **Type**: Indicates whether the frame is a `HEADERS` frame (carrying compressed HTTP headers) or a `DATA` frame (carrying application data).
- **Stream Identifier**: Associating frames with unique Stream IDs allows the client and server to interleave frames from different requests on the same connection. If Stream 3 drops a frame, the browser can still process frames for Stream 5, mitigating Head-of-Line blocking.

### HTTP/3 QUIC Transport Mechanics
Under HTTP/2, multiplexed streams run over a single TCP connection. At the IP network layer, TCP guarantees in-order delivery. If a packet carrying Stream 1 data is dropped in transit, the TCP stack buffers all subsequent packets (including those for Stream 2 and 3) until the lost packet is retransmitted and acknowledged. This is **TCP Head-of-Line (HoL) Blocking**.

HTTP/3 runs over **QUIC (UDP)**. QUIC implements connection recovery at the stream level rather than the packet level.

```text
HTTP/2 over TCP:
[TCP Packet 1: Stream A] [TCP Packet 2: Stream B] [TCP Packet 3: Stream C]
                         ^^^^^^^^^^ DROPPED PACKET
Result: TCP halts processing of Packet 3 (Stream C) until Packet 2 is retransmitted.

HTTP/3 over QUIC (UDP):
[UDP/QUIC: Stream A] [UDP/QUIC: Stream B] [UDP/QUIC: Stream C]
                     ^^^^^^^^^^ DROPPED PACKET
Result: QUIC continues delivering Stream A and Stream C to the application. Only Stream B is paused.
```

- **Connection Migration**: QUIC identifies connections using a unique **Connection ID** instead of the traditional IP/Port tuple (socket). If a user switches from Wi-Fi to cellular data, their IP address changes, which would break a TCP connection. A QUIC connection survives because the Connection ID remains the same, allowing data transmission to continue without renegotiating a handshake.

---

## 4. Important Terminology

- **HTTP (Hypertext Transfer Protocol)**: Stateless application-layer protocol for web data transfer.
- **HTTPS**: HTTP running over a cryptographically secured TLS/SSL connection.
- **TLS (Transport Layer Security)**: Cryptographic protocol securing transport layer communications.
- **SSL (Secure Sockets Layer)**: Deprecated predecessor of TLS.
- **Certificate Authority (CA)**: A trusted third-party entity that issues and signs digital certificates.
- **Cipher Suite**: A set of cryptographic algorithms (key exchange, bulk encryption, MAC) negotiated during the TLS handshake.
- **CORS (Cross-Origin Resource Sharing)**: Browser policy controlling cross-origin HTTP requests.
- **Preflight OPTIONS Request**: A preliminary HTTP request sent to verify if the destination origin permits cross-origin mutations.
- **SameSite Cookie**: Cookie attribute restricting cross-site transmission to prevent Cross-Site Request Forgery (CSRF).
- **HttpOnly Cookie**: Cookie flag blocking JavaScript read access (mitigates XSS).
- **Secure Cookie**: Cookie flag enforcing transmission exclusively over HTTPS.
- **ALPN**: Protocol allowing version negotiation (HTTP/2 vs 1.1) during the TLS handshake.
- **OCSP Stapling**: Performance optimization where servers cache certificate revocation status from the CA and send it during the TLS handshake.
- **HSTS (HTTP Strict Transport Security)**: Header forcing browsers to convert all site requests to HTTPS.
- **Certificate Pinning**: Hardcoding expected certificate keys in the client to prevent MITM attacks.
- **HPACK**: Huffman-coding-based compression algorithm used to compress HTTP/2 headers.
- **QPACK**: Header compression algorithm modified for HTTP/3 to handle out-of-order streams.
- **QUIC**: UDP-based multiplexed transport protocol developed by Google.
- **TCP Head-of-Line Blocking**: Network delay where packet loss stalls all multiplexed streams on a connection.
- **SNI (Server Name Indication)**: TLS extension indicating which hostname the client wants to connect to at the start of the handshake, enabling virtual hosting on single IPs.
- **0-RTT Session Resumption**: TLS 1.3 feature allowing clients to send encrypted data on their first request using keys from a previous session.
- **Connection Coalescing**: Consolidating requests to different domains onto a single TCP connection if certificates match.
- **Diffie-Hellman (DH)**: Cryptographic key exchange algorithm enabling two parties to establish a shared secret over an insecure channel.

---

## 5. Beginner Examples

### Example 1: Inspecting Request and Response Headers with curl
Using curl verbose flags to analyze headers and TLS handshakes.
```bash
curl -v https://example.com
```
*Expected Output Details (Partial):*
```text
*   Trying 93.184.215.14:443...
* Connected to example.com (93.184.215.14) port 443
* ALPN: offers h2, http/1.1
* TLS 1.3 connection using TLS_AES_256_GCM_SHA384
* Server certificate: CA issued...
> GET / HTTP/2
> Host: example.com
> User-Agent: curl/8.4.0
> Accept: */*
> 
< HTTP/2 200 OK
< content-type: text/html; charset=UTF-8
< cache-control: max-age=604800
< content-length: 1256
< 
<!DOCTYPE html>...
```

### Example 2: POST JSON Request with Headers via python-requests
Using python to send a POST request with headers and parse the response.
```python
import requests

url = "https://httpbin.org/post"
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
payload = {
    "username": "coder1",
    "role": "engineer"
}

response = requests.post(url, headers=headers, json=payload, timeout=5)
print("Status Code:", response.status_code)
print("Response JSON Content-Type Header:", response.headers.get("Content-Type"))
```

### Example 3: Inspecting TLS Certificates via openssl command line
Verifying certificate validation dates and issuing authority directly from the terminal.
```bash
openssl s_client -connect github.com:443 -servername github.com </dev/null 2>/dev/null | openssl x509 -noout -dates -issuer -subject
```
*Expected Output:*
```text
notBefore=Jan  6 00:00:00 2026 GMT
notAfter=Jan  6 23:59:59 2027 GMT
issuer=C = US, O = DigiCert Inc, CN = DigiCert TLS RSA SHA256 2020 CA1
subject=C = US, ST = California, L = San Francisco, O = "GitHub, Inc.", CN = github.com
```

---

## 6. Intermediate Examples

### Example 1: Mock CORS Preflight and Actual Exchange
When a client application hosted on `https://client.app` attempts to make a `POST` request with custom headers to `https://api.service.com/data`, the browser automatically performs a preflight exchange.

```text
STEP 1: PREFLIGHT REQUEST (Browser to API Server)
----------------------------------------
OPTIONS /data HTTP/1.1
Host: api.service.com
Origin: https://client.app
Access-Control-Request-Method: POST
Access-Control-Request-Headers: authorization, content-type
----------------------------------------

STEP 2: PREFLIGHT RESPONSE (API Server to Browser)
----------------------------------------
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: https://client.app
Access-Control-Allow-Methods: GET, POST, OPTIONS, DELETE
Access-Control-Allow-Headers: authorization, content-type
Access-Control-Max-Age: 86400
Connection: keep-alive
----------------------------------------

STEP 3: ACTUAL MUTATION REQUEST (Browser to API Server)
----------------------------------------
POST /data HTTP/1.1
Host: api.service.com
Origin: https://client.app
Authorization: Bearer session_token_123
Content-Type: application/json

{"score": 98}
----------------------------------------

STEP 4: ACTUAL RESPONSE (API Server to Browser)
----------------------------------------
HTTP/1.1 200 OK
Access-Control-Allow-Origin: https://client.app
Content-Type: application/json
Content-Length: 18

{"status":"saved"}
----------------------------------------
```

### Example 2: Cache-Control Headers in Production
This example details response headers configured for a Content Delivery Network (CDN) caching strategy.

```text
HTTP/1.1 200 OK
Content-Type: application/javascript; charset=UTF-8
Cache-Control: public, max-age=31536000, immutable
ETag: "w/3a8c1f0923b9d"
```
- `public`: Indicates the script can be cached by browser clients and shared CDNs.
- `max-age=31536000`: Sets the cache freshness duration to one year (31,536,000 seconds).
- `immutable`: Instructs the browser never to send a conditional validation request (like `If-None-Match`) while the file remains in its cache.
- `ETag`: A unique hash representing the file content. If the cache expires, the client sends this hash back. If the file has not changed, the server returns a `304 Not Modified` status code, saving bandwidth.

### Example 3: Secure Session Cookie Backend Configuration (Python FastAPI)
Setting secure, isolated session cookies that are protected from client-side script access.

```python
from fastapi import FastAPI, Response, Cookie
from typing import Optional

app = FastAPI()

@app.post("/login")
def login_user(response: Response):
    # Mock session generation
    session_token = "secure_token_session_hash_9921"
    
    # Set Cookie with security flags
    response.set_cookie(
        key="session_id",
        value=session_token,
        httponly=True,        # Prevents JavaScript reading (mitigates XSS)
        secure=True,          # Enforces cookie transmission over HTTPS only
        samesite="lax",       # Protects against standard CSRF attacks
        max_age=86400,        # Cookie expires in 24 hours
        path="/"              # Valid for all paths on this domain
    )
    return {"message": "Logged in successfully."}
```

---

## 7. Advanced Examples

### Example 1: Implementing HSTS and Security Headers in Python/FastAPI
Applying security headers to protect connections from protocol downgrade attacks and cross-site framing exploits.

```python
from fastapi import FastAPI, Request, Response
from fastapi.middleware.base import BaseHTTPMiddleware

app = FastAPI()

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response: Response = await call_next(request)
        
        # 1. Enforce HSTS (HTTP Strict Transport Security)
        # Instructs the browser to use HTTPS exclusively for the next year
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
        
        # 2. X-Frame-Options (Clickjacking Protection)
        # Prevents the application from being embedded in an iframe on other sites
        response.headers["X-Frame-Options"] = "DENY"
        
        # 3. Content-Type Sniffing Protection
        # Forces the browser to stick to the content type declared in headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # 4. Content Security Policy (CSP)
        # Limits script execution sources to mitigate XSS
        response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://trustedscripts.com;"
        
        return response

app.add_middleware(SecurityHeadersMiddleware)
```

### Example 2: TLS 1.3 0-RTT Session Resumption Simulator
Demonstrates the performance optimization and security risks associated with 0-RTT (Zero Round Trip Time) session tickets.

```python
# Conceptual Python Representation of 0-RTT Client-Server interaction
class ServerSessionHandler:
    def __init__(self, shared_secret_key: bytes):
        self.secret_key = shared_secret_key
        # Memory table to track processed session tickets to prevent replay attacks
        self.processed_tickets = set()

    def process_request(self, ticket: str, request_data: str, is_retry: bool) -> tuple[int, str]:
        # 1. Validate if ticket has been used (Replay Attack Check)
        if ticket in self.processed_tickets:
            # If ticket matched and it's a mutation request, reject 0-RTT to prevent duplication
            if "POST" in request_data or is_retry:
                return 401, "0-RTT Rejected: Replay attack vector detected."
                
        # 2. Authenticate session using decrypted ticket ticket
        self.processed_tickets.add(ticket)
        
        # 3. Process safe operations (GET requests) instantly
        if "GET" in request_data:
            return 200, "Safe data delivered without handshake delay."
            
        return 201, "POST processed securely."
```

### Example 3: Parsing a custom HTTP/2 Frame Header
A script showing how to unpack binary frames from an HTTP/2 network stream.

```python
import struct

def parse_http2_frame_header(frame_bytes: bytes) -> dict:
    """
    Parses a 9-byte HTTP/2 frame header.
    Format spec:
    - 24-bit Length (3 bytes)
    - 8-bit Type (1 byte)
    - 8-bit Flags (1 byte)
    - 31-bit Stream Identifier (4 bytes, ignoring the first reserved bit)
    """
    if len(frame_bytes) < 9:
        raise ValueError("HTTP/2 frame header must be exactly 9 bytes.")
        
    # Unpack binary fields
    # '>B' unpacks 1 byte, '>H' 2 bytes, '>I' 4 bytes
    # To get 24-bit length, we read 3 bytes
    length_high, length_low = struct.unpack(">BH", frame_bytes[0:3])
    payload_length = (length_high << 16) | length_low
    
    frame_type = struct.unpack(">B", frame_bytes[3:4])[0]
    flags = struct.unpack(">B", frame_bytes[4:5])[0]
    
    # Read 32-bit word, strip the first reserved bit (R) by masking
    stream_id_raw = struct.unpack(">I", frame_bytes[5:9])[0]
    stream_id = stream_id_raw & 0x7FFFFFFF
    
    return {
        "length": payload_length,
        "type": frame_type,
        "flags": flags,
        "stream_id": stream_id
    }

# Mock 9-byte headers representing HEADERS frame on Stream 5, length 24
# Hex: 000018 (Length 24), 01 (Headers Type), 04 (End Headers Flag), 00000005 (Stream 5)
mock_frame = b'\x00\x00\x18\x01\x04\x00\x00\x00\x05'
print(parse_http2_frame_header(mock_frame))
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate networking and infrastructure candidates by testing their understanding of HTTP/HTTPS concepts beyond basic API requests. They check if candidates can trace a byte from a browser through the TCP/TLS handshake, explain multiplexing mechanics, configure secure cookie flags, and identify replay vulnerabilities in 0-RTT handshakes.

### Red Flags
- ** पोस्ट/गेट म्यूटेशन कन्फ्यूजन (Post/Get Mutation Confusion)**: Suggesting sensitive actions (like money transfers or login authentication) can run safely over GET queries because "HTTPS encrypts URL paths anyway." (Warning: URLs are frequently logged in plain text in proxy servers, CDN caches, and browser histories).
- **Ignoring Cookie Flags**: Design proposal of cookie-based session stores without adding `HttpOnly` or `Secure` flags, leaving cookies vulnerable to XSS.
- **Protocol Overhead Blanks**: Incapacity to describe the performance problems of HTTP/1.1 (such as TCP connection exhaustion and head-of-line blocking).
- **SSL/TLS Impersonation Ignorance**: Believing that encryption guarantees server identity without understanding public key infrastructure (PKI) and Certificate Authority validation.

### Green Flags
- **Handshake Flow Precision**: Drawing and detailing the difference between a TLS 1.2 (2-RTT) and TLS 1.3 (1-RTT) handshake, including ECDH parameters.
- **Security Headers Mastery**: Proactively applying headers like HSTS, Content-Security-Policy (CSP), and `X-Frame-Options` in system design.
- **QUIC Stream understanding**: Explaining how QUIC resolves Head-of-Line blocking at the UDP packet level by handling stream recovery independently.
- **0-RTT Security Aware**: Explaining that 0-RTT requests are vulnerable to Replay Attacks and proposing restrictions to limit 0-RTT to GET requests.

### Answers Matrix
| Level | Question: "If HTTPS encrypts the connection, can an eavesdropper see the URL host name?" |
|---|---|
| **Rejected** | "No, HTTPS encrypts the entire request, so everything is invisible." |
| **Shortlisted** | "Yes, the hostname must be visible to DNS routers so they can route the packet." |
| **Selected** | "Yes, the hostname is visible during the initial connection setup. First, the browser must make a plaintext DNS query to resolve the domain. Second, during the TLS handshake, the browser sends the hostname in plaintext inside the **SNI (Server Name Indication)** extension of the ClientHello packet so the server can choose the correct certificate. Modern mitigations like encrypted SNI (ECH) exist, but traditionally hostnames are visible in transit, whereas paths, queries, and headers are fully encrypted." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Trace the steps of what happens when you type `https://google.com` in a browser and hit enter.
- **Detailed Answer**:
1. **URL Parsing**: The browser extracts the scheme (https), host (google.com), and path.
2. **DNS Resolution**: The browser checks its local cache, OS hosts file, resolver, and finally DNS name servers to resolve the domain to an IP address (using A/AAAA records).
3. **TCP Connection**: The browser establishes a 3-way TCP handshake ($SYN \to SYN-ACK \to ACK$) on Port 443.
4. **TLS Handshake**: The browser performs a TLS handshake (TLS 1.3: ClientHello with key shares $\to$ ServerHello with certificates and public key $\to$ shared secret generation $\to$ Finished).
5. **HTTP Request**: The browser sends an encrypted HTTP GET request containing headers (`Host`, `User-Agent`) and path `/`.
6. **Server Processing**: Google's servers decrypt the request, route it through load balancers, fetch the HTML page, and return an HTTP response (e.g. `200 OK`) containing the body.
7. **Rendering**: The browser decrypts the response, parses the HTML, fetches referenced assets (JS/CSS) over the same connection (using HTTP/2/3), and renders the page.
- **Follow-up Questions**: How does the browser know if Google's certificate is valid? (Answer: It verifies the digital signature of the certificate against the public keys of root Certificate Authorities pre-installed in the browser/OS).
- **Interviewer's Expectations**: Detail DNS lookup, TCP handshake, TLS handshake, HTTP request transmission, and asset downloading.

#### 2. What is the difference between HTTP/1.1 and HTTP/2?
- **Detailed Answer**:
- **HTTP/1.1**: Text-based protocol. It is sequential: requests must be sent one after another, or using up to 6 separate TCP connections. Suffer from HTTP Head-of-Line blocking. Headers are sent in plain text.
- **HTTP/2**: Binary framing protocol. It supports **Multiplexing**, allowing thousands of concurrent streams to share a single TCP connection. It compresses headers using **HPACK**, reducing bandwidth.
- **Follow-up Questions**: Why does multiplexing save memory? (Answer: It eliminates the overhead of keeping multiple TCP socket descriptors open, reducing memory utilization on both client and server).
- **Interviewer's Expectations**: Contrast text vs. binary formatting, sequential vs. multiplexed streams, and mention HPACK header compression.

#### 3. How does HTTP/3 improve on HTTP/2?
- **Detailed Answer**: HTTP/2 runs over TCP. If a packet is lost on the network, the TCP stack blocks *all* multiplexed streams until the packet is retransmitted.
HTTP/3 runs over **QUIC (UDP)**. QUIC handles packet loss recovery at the stream level. If Stream A loses a packet, only Stream A is delayed; Stream B and C continue delivery. Additionally, QUIC merges the connection (TCP) and encryption (TLS 1.3) handshakes into a single round trip (1-RTT) and supports **Connection Migration**, allowing sessions to persist when a client switches IP addresses.
- **Follow-up Questions**: Why does QUIC use UDP instead of TCP? (Answer: TCP is hardcoded into OS kernels, making updates difficult. UDP is supported globally, allowing QUIC to run in user space and evolve quickly).
- **Interviewer's Expectations**: Describe TCP-level Head-of-Line blocking, explain QUIC's stream-level reliability, and explain Connection Migration.

#### 4. What are secure cookie flags and why do they matter?
- **Detailed Answer**: Secure cookie flags protect credentials from interception:
- `HttpOnly`: Prevents JavaScript code (e.g. `document.cookie`) from reading the cookie. This protects the cookie from theft via Cross-Site Scripting (XSS) attacks.
- `Secure`: Instructs the browser to only transmit the cookie over encrypted HTTPS connections, preventing credential leaks over plaintext HTTP.
- `SameSite`: Prevents the cookie from being sent on cross-site requests, mitigating Cross-Site Request Forgery (CSRF).
- **Follow-up Questions**: If a cookie is set with `Secure`, does it prevent XSS access? (Answer: No, `Secure` only restricts transmission to HTTPS. You must use `HttpOnly` to block JavaScript access).
- **Interviewer's Expectations**: Define the security purpose of `HttpOnly` (XSS mitigation), `Secure` (eavesdropping mitigation), and `SameSite` (CSRF protection).

#### 5. Explain HSTS (HTTP Strict Transport Security).
- **Detailed Answer**: HSTS is a response header sent by HTTPS servers:
```text
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```
Once received, the browser stores this rule. For the specified duration (`max-age`), any attempt to connect to the domain using plain HTTP (e.g. typing `http://example.com`) is intercepted by the browser and converted to HTTPS (`https://example.com`) locally before sending any network packets. This protects users from SSL stripping attacks.
- **Follow-up Questions**: What is the HSTS Preload list? (Answer: A list hardcoded into browsers containing domains that must *always* connect via HTTPS, protecting the user's very first connection to the site).
- **Interviewer's Expectations**: Explain client-side redirection, protection against protocol downgrade (SSL stripping), and the HSTS preload list.

#### 6. What is the difference between a Symmetric and Asymmetric cryptographic algorithm, and how are they used in HTTPS?
- **Detailed Answer**:
- **Asymmetric Cryptography (Public-Key)**: Uses a public key (to encrypt) and a private key (to decrypt). It is computationally expensive. Used during the TLS handshake to authenticate the server and negotiate a shared secret securely.
- **Symmetric Cryptography (Shared-Key)**: Uses a single shared key to encrypt and decrypt. It is very fast. Once the TLS handshake establishes a shared secret, all application data is encrypted symmetrically using this secret key.
- **Follow-up Questions**: Give examples of each algorithm type used in TLS. (Answer: Asymmetric: RSA, ECDHE. Symmetric: AES-GCM, ChaCha20).
- **Interviewer's Expectations**: Contrast key usage and processing costs, and explain their roles in TLS setup (asymmetric) vs. data transport (symmetric).

#### 7. How does a browser validate a TLS certificate?
- **Detailed Answer**:
1. **Chain Verification**: The browser traces the certificate up to a trusted root certificate pre-installed in the browser/OS store.
2. **Signature Verification**: The browser uses the issuer's public key to decrypt the digital signature on the certificate, verifying it was signed by a trusted CA.
3. **Date Validity**: The browser checks that the current time falls within the certificate's `notBefore` and `notAfter` dates.
4. **Domain Match**: The browser verifies that the domain name in the URL matches the certificate's Common Name (CN) or Subject Alternative Name (SAN).
5. **Revocation Check**: The browser queries the CA via CRL or OCSP to ensure the certificate has not been revoked.
- **Follow-up Questions**: What is a wildcard certificate? (Answer: A certificate that covers a domain and all its subdomains, e.g. `*.example.com`).
- **Interviewer's Expectations**: Detail root trust chains, public key signature validation, expiration checks, host mapping, and revocation lookups.

#### 8. What is a Replay Attack, and how does TLS protect against it?
- **Detailed Answer**: A Replay Attack occurs when an adversary intercepts encrypted packets sent during a valid session and transmits them to the server at a later time to repeat a transaction (e.g. duplicating a payment).
TLS protects against this by:
1. **Cryptographic Nonces**: During the handshake, both client and server exchange random bytes (nonces) that are combined to generate unique session keys.
2. **Sequence Numbers**: Every record packet sent during a TLS session contains an implicit sequence number. If a packet is replayed, the MAC validation fails because the sequence number does not match.
- **Follow-up Questions**: How does 0-RTT session resumption re-introduce replay attack risks? (Answer: Because 0-RTT sends data on the first flight before a new handshake exchange, an attacker can capture and replay this initial packet. Servers must use replay caches or restrict 0-RTT to idempotent requests).
- **Interviewer's Expectations**: Explain interception, session uniqueness (nonces), packet sequencing, and the replay vulnerabilities of 0-RTT.

#### 9. What is SNI (Server Name Indication) and why is it needed?
- **Detailed Answer**: SNI is an extension to the TLS protocol. In virtual hosting, a single server IP hosting multiple websites (e.g., `a.com` and `b.com`) must know which domain the client wants to access in order to serve the correct SSL/TLS certificate.
During the TLS handshake, the browser sends the hostname in plaintext inside the SNI field of the `ClientHello` message. This allows the server to select and return the correct certificate before the encrypted connection is established.
- **Follow-up Questions**: What is Encrypted Client Hello (ECH)? (Answer: An updated standard replacing SNI that encrypts the hostname field during the handshake to prevent eavesdroppers from identifying which site the user is visiting).
- **Interviewer's Expectations**: Explain virtual hosting on single IPs and the necessity of hostname visibility before certificate transmission.

#### 10. Explain the difference between HTTP Keep-Alive and Connection Multiplexing.
- **Detailed Answer**:
- **HTTP Keep-Alive (HTTP/1.1)**: Keeps a TCP connection open after a request completes so it can be reused for subsequent requests. However, requests must still run sequentially: a new request cannot be sent on the connection until the previous response has been fully received.
- **Connection Multiplexing (HTTP/2/3)**: Allows sending multiple requests and receiving responses concurrently over a single connection. The payload is split into frames with stream identifiers, allowing data from different files to be interleaved in transit.
- **Follow-up Questions**: How does multiplexing resolve head-of-line blocking? (Answer: It allows the client to process headers and data from stream B even if stream A is waiting for database processing).
- **Interviewer's Expectations**: Contrast sequential reuse (Keep-Alive) with concurrent interleaved frames (Multiplexing).

---

### Scenario-Based Questions

#### 11. A browser blocks an API request from your frontend web app, logging: "Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource." How do you troubleshoot and fix this?
- **Detailed Answer**:
- **Troubleshooting**: This is a CORS error. The browser blocks the request because the web page origin (`https://myfrontend.com`) does not match the API server origin (`https://myapi.com`), and the server response is missing headers permitting cross-origin access.
- **Fix**:
  1. Add a CORS preflight OPTIONS route handler on the backend.
  2. Configure the server to return headers:
     `Access-Control-Allow-Origin: https://myfrontend.com`
     `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
     `Access-Control-Allow-Headers: Authorization, Content-Type`
  3. Ensure the OPTIONS request returns a `204 No Content` status code immediately, without running database or authentication queries.
- **Follow-up Questions**: Why is it best practice to avoid wildcard `*` origins when credentials are used? (Answer: Browsers reject CORS requests containing cookies or auth headers if the origin is set to `*` for security reasons).
- **Interviewer's Expectations**: Explain origin matching, detail CORS headers, and explain preflight OPTIONS handling.

#### 12. Your API service receives sensitive user data. You want to make sure it is impossible for intermediate routers to read this data. Describe your security configuration.
- **Detailed Answer**:
1. **Enforce HTTPS**: Disable Port 80 (HTTP) or configure a global redirection rule to Port 443 (HTTPS) at the API Gateway.
2. **HSTS Header**: Inject HSTS headers with `preload` to force browsers to use HTTPS for all requests.
3. **Configure Cipher Suites**: Restrict the server to TLS 1.3 only, or TLS 1.2 with secure ciphers (e.g. ECDHE-RSA-AES256-GCM-SHA384), disabling weak ciphers (like RC4, 3DES, or CBC mode).
4. **HSTS Preload Listing**: Add the domain to the Chrome HSTS preload list to secure the user's initial connection.
5. **Secure Cookies**: Set all auth cookies with `Secure`, `HttpOnly`, and `SameSite=Strict`.
- **Follow-up Questions**: Does HTTPS encrypt the query string parameters in the URL? (Answer: Yes, HTTPS encrypts the entire HTTP payload, including query strings, paths, and headers. However, URLs can still be logged in plain text in browser histories, so sensitive data should be sent in the request body).
- **Interviewer's Expectations**: Enforce HTTPS, disable weak ciphers, configure HSTS, and protect auth cookies.

#### 13. Your web page loads slowly because it requests 50 small icon images from your server. Explain how protocol version impacts this loading behavior.
- **Detailed Answer**:
- **Under HTTP/1.1**: The browser can only load 6 images in parallel. The remaining 44 images must wait in a queue. Each connection requires a TCP 3-way handshake and TLS setup, causing high latency.
- **Under HTTP/2**: The browser loads all 50 images concurrently over a single TCP connection using multiplexing, eliminating queue delays and handshake overhead.
- **Under HTTP/3**: Latency is reduced further. If a packet is lost in transit, only the stream containing the lost image is delayed, while the other 49 images render immediately.
- **Follow-up Questions**: How did developers optimize assets under HTTP/1.1? (Answer: They combined images into a single file called a sprite, or merged JS/CSS files to reduce request counts).
- **Interviewer's Expectations**: Compare parallel connections limits, multiplexing performance, and QUIC packet recovery.

#### 14. Your application needs to serve static assets via a CDN. How do you configure HTTP headers to maximize caching efficiency while ensuring users get updates instantly when assets change?
- **Detailed Answer**:
1. **Cache-Control Configuration**: Configure the origin server to return headers for static assets:
   ```text
   Cache-Control: public, max-age=31536000, immutable
   ```
   This allows browsers and CDNs to cache assets for up to a year without checking the server.
2. **Cache Busting**: Append a content hash to the asset filenames (e.g. `main.a8f2c.js` instead of `main.js`).
3. **Updates**: When the asset changes, the build process generates a new file hash (`main.b9e3d.js`). Since it is a new filename, the browser requests the new asset immediately, bypasses the cached version, and updates without delay.
- **Follow-up Questions**: What is the purpose of the `Vary` header? (Answer: It tells caches which request headers to inspect to determine if a cached response can be reused, e.g. `Vary: Accept-Encoding`).
- **Interviewer's Expectations**: Recommend long cache lifetimes combined with filename hashing (cache busting).

#### 15. A client application reports connection failures when calling your API. The client says they are using a custom certificate authority. How do you resolve this?
- **Detailed Answer**:
- **Diagnosis**: The client's system does not trust the certificate chain returned by your server because your certificate was signed by a private or self-signed CA that is not in the client's trusted root store.
- **Resolution**:
  1. The client must import your custom CA's root certificate into their local OS/browser trust store.
  2. In client scripts (like node or python), configure the HTTP library to point to the custom CA certificate file (e.g. using `requests.get(url, verify='/path/to/custom_ca.pem')`).
  3. Ensure your server is returning the full certificate chain (including intermediate certificates), not just the leaf certificate.
- **Follow-up Questions**: Why should you avoid disabling certificate verification (e.g. `verify=False` in Python)? (Answer: Disabling verification disables identity checks, leaving the connection vulnerable to Man-in-the-Middle attacks).
- **Interviewer's Expectations**: Detail certificate chain trust models and recommend importing CAs over disabling verification.

---

### Debugging Questions

#### 16. A client reports receiving a "403 Forbidden" response when calling your secure API. What are your troubleshooting steps?
- **Detailed Answer**:
1. **Verify Authentication**: Ensure the client sent credentials (e.g., `Authorization: Bearer <token>`). If missing, the issue is authentication (though the server should return 401).
2. **Inspect Token Claims**: Decode the JWT or token and verify that the user's role or scopes match the resource requirements (e.g., checking if they have `write:users` access).
3. **Check Resource Ownership**: Verify if the user is attempting to access a resource belonging to another account or tenant.
4. **IP Restrictions / WAF**: Check if the request was blocked by a Web Application Firewall (WAF) or IP whitelist rule at the API Gateway.
- **Follow-up Questions**: How do you inspect JWT contents securely? (Answer: Decode the signature locally without querying the database, but verify the signature using the server's public key).
- **Interviewer's Expectations**: Step through auth verification, scope mapping, tenant isolation checks, and gateway-level blocks.

#### 17. Your website displays a "Mixed Content" warning in the browser. What does this mean and how do you resolve it?
- **Detailed Answer**:
- **Meaning**: The main HTML page was loaded securely over HTTPS, but the page is requesting sub-resources (like images, stylesheets, or scripts) using plain HTTP (e.g. `http://cdn.com/logo.png`). Browsers display warnings because these plaintext requests can be intercepted or tampered with, compromising the page's security.
- **Resolution**:
  1. Change all sub-resource URLs in the code to use HTTPS.
  2. Use relative paths or protocol-relative URLs (e.g., `//cdn.com/logo.png`).
  3. Add the HSTS header to the server configuration.
  4. Use the Content Security Policy (CSP) header to force secure connections:
     ```text
     Content-Security-Policy: upgrade-insecure-requests;
     ```
- **Follow-up Questions**: Will browsers block mixed content? (Answer: Yes, modern browsers block active mixed content like scripts and iframes automatically, while displaying warnings for passive content like images).
- **Interviewer's Expectations**: Explain security boundaries and recommend CSP upgrades.

#### 18. The first request to your API takes 800ms, but subsequent requests take only 30ms. Explain the network causes.
- **Detailed Answer**:
1. **Connection Overhead**: The first request must establish a TCP connection and negotiate a TLS handshake:
   - TCP Handshake (1-RTT).
   - TLS Handshake (1-RTT or 2-RTT).
   - DNS Lookup (up to 1-RTT).
   This adds 3 round trips of latency before any data is sent. Subsequent requests reuse the open TCP connection (using Keep-Alive or Multiplexing), skipping the handshakes.
2. **Cold Starts**: If the backend runs on serverless infrastructure (like AWS Lambda), the first request requires launching the container, causing a cold start delay.
3. **Database Connection Warmup**: The application server may establish database connection pools on the first query.
- **Follow-up Questions**: How do you optimize handshake latency? (Answer: Use a CDN to terminate TLS connections close to the user, and keep backend connections warm).
- **Interviewer's Expectations**: Identify DNS, TCP, and TLS handshakes as connection setup bottlenecks, and mention Keep-Alive reuse.

#### 19. A client reports that cookies are not being saved across requests in their browser. What could be the cause?
- **Detailed Answer**:
1. **Domain/Path Scope Mismatch**: The cookie was set with a restricted domain (e.g., `Domain=app.example.com`) or path (e.g., `Path=/api`), and the subsequent request is outside this scope.
2. **HttpOnly flag confusion**: The client JavaScript is attempting to read the cookie, but it is blocked by the `HttpOnly` flag.
3. **SameSite Restrictions**: The frontend and backend run on different domains, and the cookie is missing the `SameSite=None` or `Secure` attributes, causing the browser to reject it.
4. **Cookie Expiry**: The cookie expired because `Max-Age` or `Expires` was set incorrectly or omitted (making it a session cookie that expires when the browser closes).
- **Follow-up Questions**: How do you inspect cookies in browser dev tools? (Answer: Open the Application tab, navigate to Storage -> Cookies, and check the domain, path, and security flags).
- **Interviewer's Expectations**: Enumerate scope mismatches, SameSite flags, and expiration configurations.

#### 20. Your server's SSL certificate expired, causing service outages. How do you resolve this permanently and prevent future occurrences?
- **Detailed Answer**:
- **Immediate Resolution**: Renew the certificate immediately using a Certificate Authority (like Let's Encrypt or DigiCert) and deploy it to the API gateway or server.
- **Permanent Prevention**:
  1. **Automated Renewal**: Implement ACME protocol clients (like Certbot) to automatically renew certificates (e.g. every 60 days for Let's Encrypt).
  2. **Monitoring & Alerts**: Set up automated monitoring (using tools like Datadog, Prometheus, or uptime checkers) to scan the endpoint daily and alert engineering teams when a certificate is within 14 days of expiration.
  3. **Multi-Domain Certificates**: Use wildcard or SAN certificates to simplify management.
- **Follow-up Questions**: What is a self-signed certificate and when should it be used? (Answer: A certificate signed by the creator rather than a trusted CA. Use it only in isolated development environments).
- **Interviewer's Expectations**: Propose automated ACME setups and automated expiration monitoring.

---

### System Design Questions

#### 21. Design a globally distributed web application that serves users in Asia, Europe, and America with low latency.
- **Detailed Answer**:
- **Global Load Balancing**: Use a Geolocation-based DNS routing service (e.g. AWS Route 53 or Cloudflare) to route users to the nearest edge server.
- **Content Delivery Network (CDN)**: Deploy a CDN (e.g., Cloudflare, Akamai) to cache static assets (HTML, images, JS) at edge locations close to users.
- **Anycast IP Routing**: Route user requests to the nearest edge location using Anycast IPs.
- **Edge TLS Termination**: Terminate TLS connections at the CDN edge. This reduces handshake latency (TTFT) by performing DNS, TCP, and TLS handshakes close to the user, while keeping persistent TCP connections open between the edge and the origin server.
- **Multi-Region Origin**: Deploy backend application instances in three regions (e.g., AWS us-east-1, eu-west-1, ap-southeast-1) with a replicated database (e.g., Aurora Global Database) to handle dynamic API queries locally.
- **Follow-up Questions**: How does terminating TLS at the edge improve performance? (Answer: It reduces the distance the TLS handshake packets must travel, cutting handshake time from 150ms to 10ms for distant users).
- **Interviewer's Expectations**: Detail Geo-routing, CDNs, Edge TLS termination, and multi-region databases.

#### 22. Design a system to serve dynamic data (e.g., stock prices) to millions of clients with sub-second latency.
- **Detailed Answer**:
- **Transport Protocol**: I will use **Server-Sent Events (SSE)** or **WebSockets** running over **HTTP/2 or HTTP/3**.
- **Edge Push Gateways**: Deploy push gateway clusters at edge locations close to users.
- **Pub/Sub Broker**: Use a high-throughput message broker (like Redis Pub/Sub or Kafka) to publish stock price updates from data feeds to the edge gateways.
- **Client Connections**: Clients connect to their nearest edge gateway. The gateway maintains a persistent HTTP connection to the client and broadcasts updates as they arrive.
- **Multiplexing Optimization**: Run the system over HTTP/2 or HTTP/3 to allow clients to stream updates on one channel while making standard API requests on others, without connection overhead.
- **Follow-up Questions**: Why choose SSE over WebSockets for stock tickers? (Answer: Stock tickers only require one-way data updates from server to client. SSE is simpler, runs over standard HTTP, and handles automatic reconnections natively).
- **Interviewer's Expectations**: Detail persistent connection gateways, pub/sub integration, and multiplexing optimizations.

#### 23. Design a secure communication channel between microservices in an enterprise network.
- **Detailed Answer**:
- **Mutual TLS (mTLS)**: Enforce mTLS for all service-to-service communication. Both the client service and server service must present and validate each other's certificates, ensuring mutual authentication and encryption.
- **Service Mesh**: Deploy a service mesh (like Istio or Linkerd) using sidecar proxies (like Envoy) running alongside each microservice container. The sidecars manage the mTLS handshakes, certificate rotation, and encryption automatically, keeping application code clean.
- **Certificate Authority**: Use a private CA (like HashiCorp Vault or AWS Private CA) to automatically issue and rotate short-lived certificates (e.g., valid for 24 hours) for the microservices.
- **Authorization Policies**: Define strict access control policies (e.g., SPIFFE IDs) at the proxy level to restrict which services are allowed to call each other (e.g., allowing Billing Service to call Payment Service, but blocking Frontend Service).
- **Follow-up Questions**: Why are short-lived certificates preferred? (Answer: They minimize security risks if a certificate's private key is compromised, eliminating the need for complex revocation lists).
- **Interviewer's Expectations**: Recommend mTLS, sidecar proxies, automated CA rotation, and identity-based access controls.

---

## 10. Common Mistakes

- **Dynamic Prefix Caching Violations**: Placing changing parameters (like `timestamp`) at the beginning of API queries, causing CDN cache misses and resource waste.
- **Missing Cookie Security Flags**: Setting session cookies without `HttpOnly` and `Secure` attributes, exposing user sessions to XSS theft.
- **GET Requests with Side-Effects**: Designing GET APIs that mutate database states, which can cause unexpected changes if search crawlers index the site.
- **Ignoring CORS Preflight OPTIONS Requirements**: Building backend API services that do not handle preflight `OPTIONS` requests, resulting in browser connection blocks.
- **Hardcoding SSL Certificates**: Hardcoding SSL certificates in mobile applications rather than pinning public key hashes, causing app crashes when certificates are renewed.

---

## 11. Comparison Section: HTTP/1.1 vs. HTTP/2 vs. HTTP/3

| Feature | HTTP/1.1 | HTTP/2 | HTTP/3 |
|---|---|---|---|
| **Transport Protocol** | TCP | TCP | UDP (QUIC) |
| **Connection Handshake** | TCP Handshake (1-RTT) + TLS (1-2 RTT) | TCP Handshake (1-RTT) + TLS (1-2 RTT) | Combined QUIC/TLS 1.3 Handshake (1-RTT) |
| **Multiplexing** | No (sequential pipelining only) | Yes (stream-level multiplexing) | Yes (stream-level multiplexing) |
| **Head-of-Line Blocking** | Yes (at HTTP layer) | Yes (at TCP packet layer if drop occurs) | No (QUIC handles packet recovery per stream) |
| **Header Compression** | None (plain text ASCII) | HPACK (Huffman coding + static tables) | QPACK (optimized for out-of-order delivery) |
| **Connection Migration** | No (IP changes break socket) | No (IP changes break socket) | Yes (identifies sessions via Connection IDs) |
| **Resource Prioritization**| No | Yes (via stream dependency trees) | Yes (via stream priority frames) |
| **Security Configuration** | Optional TLS encryption | Optional (but enforced by browsers) | Enforced natively (QUIC integrates TLS 1.3) |

---

## 12. Practical Project Ideas

### Beginner: Inspecting Headers & Handshakes
Write a command-line script in Python or Node.js that takes a URL, performs a verbose connection scan, and outputs a formatted summary containing: IP address, TLS protocol version, cipher suite used, server certificate issuer, and response headers.

### Intermediate: CORS-Enabled API Gateway Proxy
Build a reverse proxy server (using Node.js or Python) that sits in front of a backend API. Configure the proxy to intercept requests, handle preflight `OPTIONS` calls, validate Origin domains against a whitelist, and inject appropriate CORS headers before forwarding requests.

### Advanced/Resume-worthy: Secure mTLS Service Mesh Simulation
Create a multi-container local service mesh using Docker Compose. Deploy two microservices that communicate using mutual TLS (mTLS). Configure a local CA service (using HashiCorp Vault) to automatically generate, distribute, and rotate certificates for both services. Validate that connections are rejected if certificates are missing or expired.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of HTTP/1.1 vs HTTP/2 differences, status code families, cookie security flags, and the differences between symmetric and asymmetric encryption.
- **What Engineering Teams expect**: Familiarity with browser CORS policies, configuring HTTPS on servers/gateways, and troubleshooting mixed content errors.

---

## 14. Cheat Sheet

- **Handshake Speeds**:
  - TLS 1.2 = 2 round trips.
  - TLS 1.3 = 1 round trip.
- **Cookie Security flags**:
  - `HttpOnly`: Mitigates script reading (XSS protection).
  - `Secure`: Mitigates plain text transmission (HTTPS enforcement).
  - `SameSite=Strict`: Mitigates CSRF.
- **HSTS Header**:
  ```text
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  ```
- **ALPN**: Negotiates protocol versions (e.g. h2) during the TLS handshake, saving round trips.

---

## 15. One-Day Revision Guide

- [ ] Trace a request from typing a URL to page render, detailing DNS, TCP, and TLS steps.
- [ ] Explain how HTTP/2 multiplexing differs from HTTP/1.1 Keep-Alive.
- [ ] Describe how QUIC resolves Head-of-Line blocking in HTTP/3.
- [ ] List the three cookie security flags and explain their purposes.
- [ ] Explain how a browser verifies a server's TLS certificate.
