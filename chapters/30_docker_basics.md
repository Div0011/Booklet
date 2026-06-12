# 30. Docker (Containerization & Deployment)

## 1. Introduction

### What it is
Docker is an open-source containerization platform designed to automate the deployment of applications as lightweight, portable, self-contained packages called **containers**. Unlike virtual machines, containers share the host operating system's kernel, virtualizing at the OS level rather than the hardware level.

### Why it exists
Historically, deployment suffered from "works on my machine" syndrome. Environment drift—differences in OS distributions, system libraries, configuration files, and Python/Node runtimes between developer laptops and production servers—caused frequent deployment failures. Docker resolves this by packaging the application binary, configuration files, dependencies, and execution runtimes together into a single, immutable unit that runs identically on any system running Docker.

### Problems it solves
- **Environment Inconsistency**: Eliminates dependency deviations across development, testing, and production.
- **Dependency Collision**: Allows running multiple applications requiring conflicting versions of the same libraries (e.g. Node 16 and Node 20) on the same host without configuration conflicts.
- **Onboarding Latency**: Enables new developers to run a single command (`docker compose up`) to spin up a local environment containing databases, cache brokers, and microservices in seconds.
- **Orchestration Readiness**: Provides standardized, lightweight artifacts that can be managed by orchestration tools like Kubernetes.

### Industry Use Cases
- **Microservice Architectures**: Deploying hundreds of decoupled backend services independently on shared cloud servers.
- **CI/CD Build Runners**: Launching temporary, clean containers to compile, test, and audit application code before shutting down.
- **Machine Learning MLOps**: Packaging model inference APIs alongside CUDA drivers and deep learning libraries (TensorFlow/PyTorch) to guarantee reproducible execution.
- **Serverless Compute Scaling**: Powering platforms like AWS Fargate and Google Cloud Run, which launch client container containers instantly in response to web traffic.

### Analogy
In the shipping industry, cargo was once loaded loose onto ships (requiring custom crates, custom hooks, and manually handling coffee beans, steel bars, and cars). This was slow and error-prone. The **standard steel shipping container** revolutionized transport: any cargo of any shape is packed inside a standard container, and every ship, crane, and truck is designed to carry that exact box. Docker is the standard shipping container for software. The ship is the server, the docker engine is the crane, and the application code is the cargo.

---

## 2. Core Concepts

### Beginner Concepts
- **Image**: A read-only, immutable template containing the application code, libraries, runtime environment, and system files. Built using instructions declared in a Dockerfile.
- **Container**: A running, transient instance of an image. If the image is the class (compiled blueprint), the container is the object instantiated in memory.
- **Dockerfile**: A plain-text configuration file containing a sequential list of instructions (e.g. `FROM`, `RUN`, `COPY`) used by the Docker engine to compile an image.
- **Docker Registry**: A centralized repository system for uploading and downloading images (e.g. Docker Hub, Amazon ECR, Google Container Registry).
- **Volumes vs. Bind Mounts**:
  - **Volume**: A persistent storage directory managed entirely by Docker within a dedicated part of the host filesystem. Best for production databases.
  - **Bind Mount**: Links an arbitrary file or directory on the host machine to a path inside the container. Best for live-reloading code during development.
- **Container Networking**: Isolates containers from the host network, allocating them virtual IPs and enabling communication via virtual bridges.

### Intermediate Concepts
- **Union File Systems (UnionFS)**: Docker images are composed of read-only layers. When an instruction in a Dockerfile creates a layer, it is stacked on top of previous layers. UnionFS merges these layers into a single cohesive filesystem view inside the container.
- **Copy-on-Write (CoW)**: When a container is launched from an image, Docker adds a thin, writable layer (**Container Layer**) on top of the read-only image layers. If the container modifies a file from the image, the file is copied up to the writable layer first, keeping the underlying image layers unchanged.
- **Multi-Stage Builds**: A Dockerfile pattern that uses multiple `FROM` instructions. It allows compiling binaries in a temporary build stage containing compilers and SDKs, then copying only the final compiled artifact to a minimal runtime stage, shrinking the production image size by up to 90%.
- **Docker Compose**: A developer tool used to define and manage multi-container applications (e.g., app, database, and Redis cache) using a single YAML configuration file (`docker-compose.yml`).
- **Resource Constraints**: Capping the maximum CPU share and RAM allocation (e.g. `--memory=512m`) a container is allowed to consume, preventing resource starvation on the host server.

### Advanced Concepts
- **BuildKit**: The modern, highly optimized build engine for Docker. It supports parallel layer compilation, build cache mounts (speeding up package managers like pip/npm), and secure build-time secrets injection without writing secrets to image layers.
- **Rootless Containers**: Running the Docker daemon and containers inside a non-root user account, utilizing user namespaces to prevent container-breakout exploits from gaining root access to the host server.
- **Scratch and Distroless Images**: Minimal base images containing zero OS shell utilities, package managers, or debugging tools (Distroless contains only runtime dependencies; Scratch is completely empty). Using them drastically reduces security vulnerabilities (CVEs) and image sizes.
- **Vulnerability Scanning**: CI/CD security tools (like Trivy or Grype) that scan container image layers for known CVEs before deployment.
- **Network Drivers**:
  - `bridge`: The default driver; allocates private IPs to containers connected to a virtual network bridge on the host.
  - `host`: Disables network isolation; the container shares the host's IP and port space directly.
  - `overlay`: Connects multiple Docker daemons across different hosts, enabling swarm services to communicate securely.

---

## 3. Internal Working

### Docker Architecture
Docker uses a client-server architecture. The CLI client does not manage containers; it communicates with a daemon process via Unix sockets or a REST API.

```text
+------------------------+
|   Docker CLI Client    | (Commands like 'docker run')
+------------------------+
           |
           v REST API / UNIX Socket
+------------------------+
|   Docker Daemon        | (dockerd - manages volumes, networks, images)
+------------------------+
           |
           v gRPC API
+------------------------+
|   containerd           | (Supervises container lifecycles, pulls images)
+------------------------+
           |
           v fork/exec
+------------------------+
|   containerd-shim      | (Keeps container pipes open if daemon restarts)
+------------------------+
           |
           v runc system call
+------------------------+
|   Linux Kernel         | (Namespaces, Cgroups, chroot)
+------------------------+
```

1. **Client**: The developer writes commands in the CLI (e.g. `docker run`).
2. **Docker Daemon (`dockerd`)**: Coordinates image building, networking, and volumes. Passes execution requests to containerd.
3. **`containerd`**: A CNCF runtime project that supervises the lifecycle of containers (execution, streaming, state updates).
4. **`runc`**: A lightweight, CLI-compliant tool that implements the OCI specification to interact with the Linux kernel, launch namespaces, apply cgroups, and execute the container process.

### Linux Kernel Primitives
Containers are not physical entities; they are standard Linux processes isolated using kernel-level primitives:
1. **Namespaces (Isolation)**: Restricts what a process can *see*.
   - `PID Namespace`: Gives the container its own process tree (the container's main process runs as PID 1 inside the container, but maps to a standard PID on the host).
   - `NET Namespace`: Provides isolated virtual network cards, routing tables, and port allocations.
   - `MNT Namespace`: Isolates file mount points, giving the container its own view of the filesystem.
   - `IPC Namespace`: Restricts inter-process communication resources.
   - `UTS Namespace`: Isolates hostnames and domain names.
   - `USER Namespace`: Maps UIDs and GIDs inside the container to different UIDs/GIDs on the host (e.g., mapping root UID 0 in the container to UID 10001 on the host).
2. **Control Groups / cgroups (Resource Limits)**: Restricts what a process can *use*. cgroups enforce limits on CPU usage, memory consumption, block I/O throughput, and process counts.
3. **chroot / pivot_root**: Changes the root directory of the container process to the path of the extracted image filesystem, preventing it from accessing files on the host's real root filesystem.

### Image Layering and Cache Invalidation
Union filesystems stack read-only layers. Each line in a Dockerfile (like `RUN`, `COPY`) creates a new layer containing the diff of changes made by that command.

```text
Dockerfile Stack:
+-------------------------------------------------+
| Writable Container Layer                        | (Temporary; created on run)
+-------------------------------------------------+
| Layer 3: COPY app.py /app/                      | (Read-Only; app code diff)
+-------------------------------------------------+
| Layer 2: RUN pip install numpy                  | (Read-Only; dependency diff)
+-------------------------------------------------+
| Layer 1: FROM python:3.12-slim                  | (Read-Only; base OS files)
+-------------------------------------------------+
```

- **Cache Invalidation rules**:
  - During `docker build`, Docker checks if previous builds generated the same layer. If yes, it reuses the cached layer, skipping execution.
  - For `RUN` commands, Docker matches the text string of the command.
  - For `COPY` and `ADD` commands, Docker calculates checksums of the files being copied. If a file changed, the cache is invalidated.
  - **Cascading Invalidation**: Once a layer cache is invalidated, *all subsequent layers* are rebuilt from scratch, regardless of their content. Hence, stable steps must be placed at the top, and volatile steps (like copying application code) must be placed at the bottom of the Dockerfile.

---

## 4. Important Terminology

- **Docker Image**: Immutable, read-only template containing the application environment.
- **Docker Container**: A running, isolated instance of an image.
- **Dockerfile**: Blueprint text file detailing steps to build an image.
- **UnionFS / Overlay2**: File system technology merging multiple read-only layers.
- **Copy-on-Write (CoW)**: Optimization copying files to the container's writable layer only when modified.
- **Volume**: Docker-managed persistent storage directory on the host.
- **Bind Mount**: Direct link mapping a host directory to a container path.
- **Docker Compose**: Tool for defining and running multi-container configurations using YAML.
- **BuildKit**: High-performance image build engine supporting cache mounts.
- **Namespace**: Linux kernel primitive isolating process resources (networking, PIDs).
- **Control Group (cgroup)**: Linux kernel primitive limiting resource usage (CPU, RAM).
- **runc**: OCI-compliant runtime that spawns and runs containers.
- **containerd**: Daemon managing container lifecycles and image transfers.
- **OCI (Open Container Initiative)**: Standards body defining container image and runtime specs.
- **Docker Registry**: Repository storage service for managing image uploads.
- **Multi-Stage Build**: Design pattern using multiple FROM lines to build smaller images.
- **Bridge Network**: Default network driver isolating containers on a virtual switch.
- **Host Network**: Driver removing network isolation, sharing the host ports directly.
- **Overlay Network**: Driver linking containers across multiple physical hosts.
- **Distroless Image**: Minimal base image containing only the app and its runtime.
- **Scratch Image**: Empty base image (0 bytes) used for compiling static binaries.
- **Trivy**: Open-source vulnerability scanner for container images.

---

## 5. Beginner Examples

### Example 1: Basic Python API Dockerfile
Containerizing a simple Python application using best practices like virtual environments and cache layer ordering.

```dockerfile
# 1. Use an official, lightweight base image
FROM python:3.12-slim

# 2. Set the working directory inside the container
WORKDIR /usr/src/app

# 3. Copy only the dependencies file first to leverage cache layers
COPY requirements.txt ./

# 4. Install dependencies without writing caching files to disk
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the remaining application source code
COPY . .

# 6. Expose the port the app listens on
EXPOSE 8000

# 7. Define the runtime execution command
CMD ["python3", "main.py"]
```
*To compile and run this Dockerfile:*
```bash
# Compile the image and tag it as 'my-api'
docker build -t my-api:v1.0 .

# Run the container, mapping host port 8080 to container port 8000
docker run -d -p 8080:8000 --name active-api my-api:v1.0
```

### Example 2: Multi-Container Docker Compose Stack
A docker-compose configuration deploying a web service alongside a PostgreSQL database and persistent storage.

```yaml
version: '3.8'

services:
  web_app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8000"
    environment:
      - DATABASE_HOST=db_service
      - DATABASE_NAME=prod_db
      - DATABASE_USER=db_user
      - DATABASE_PASSWORD=secure_pass
    # Delay startup until database port is open
    depends_on:
      - db_service

  db_service:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=prod_db
      - POSTGRES_USER=db_user
      - POSTGRES_PASSWORD=secure_pass
    # Persist database files in a Docker-managed named volume
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```
*Operations commands:*
```bash
# Start all services in the background (detached mode)
docker compose up -d

# Check logs for the web application
docker compose logs -f web_app

# Tear down the stack, preserving data volumes
docker compose down
```

### Example 3: Debugging and Inspection commands
Common CLI commands to inspect container state and clean up resources.
```bash
# 1. List all running and stopped containers
docker ps -a

# 2. Run an interactive shell inside a running container for debugging
docker exec -it active-api /bin/sh

# 3. View resource utilization (CPU, Memory, Network I/O) in real-time
docker stats active-api

# 4. Clean up unused containers, networks, and dangling images
docker system prune -f
```

---

## 6. Intermediate Examples

### Example 1: Multi-Stage Build for a Production Node.js Application
Separating build tooling (like compilers and devDependencies) from the final runtime image to minimize size and security footprint.

```dockerfile
# =========================================================
# STAGE 1: Build Environment
# =========================================================
FROM node:20-alpine AS builder

WORKDIR /usr/src/app

# Copy package configurations
COPY package*.json ./

# Install all dependencies (including devDependencies like TypeScript)
RUN npm ci

# Copy application source files
COPY . .

# Compile TypeScript to JavaScript
RUN npm run build

# Prune devDependencies to keep only production libraries
RUN npm prune --production

# =========================================================
# STAGE 2: Lightweight Runtime Environment
# =========================================================
FROM node:20-alpine

WORKDIR /app

# Copy production dependencies from build stage
COPY --from=builder /usr/src/app/node_modules ./node_modules

# Copy compiled JavaScript code
COPY --from=builder /usr/src/app/dist ./dist

# Create a non-privileged user and switch to it for security
USER node

EXPOSE 3000

ENV NODE_ENV=production

# Run app
CMD ["node", "dist/server.js"]
```

### Example 2: Volume Configurations and Bind Mounts
Configuring data persistence for development and production environments.

```bash
# 1. Production: Use a named volume (Docker-managed, isolated)
# Docker manages the host path automatically; data persists across container restarts
docker run -d --name db_prod -v pg_data:/var/lib/postgresql/data postgres:16-alpine

# 2. Development: Use a Bind Mount
# Maps a host code directory directly to the container, enabling hot-reloading
docker run -d --name dev_app -v "$(pwd)/src:/app/src" -p 3000:3000 my-node-app

# 3. Performance: Use a tmpfs mount
# Stores files in host memory (RAM) instead of disk, ideal for transient session caches
docker run -d --name cache_app --tmpfs /app/sessions my-cache-app
```

### Example 3: Custom Bridge Network Configuration
Configuring DNS-based service discovery between container apps.

```bash
# 1. Create a custom network bridge
docker network create internal_api_net

# 2. Run a database container connected to the network
# It resolves dynamically using its container name '--name pg_db'
docker run -d --name pg_db \
  --network internal_api_net \
  -e POSTGRES_PASSWORD=pass \
  postgres:16-alpine

# 3. Run the application on the same network
# The app can connect to the database using host='pg_db' instead of an IP address
docker run -d --name app_api \
  --network internal_api_net \
  -e DB_HOST=pg_db \
  -p 8080:8000 \
  my-api:v1.0
```

---

## 7. Advanced Examples & Concepts

### Example 1: BuildKit Caching Optimization and Build-Time Secrets
Using modern BuildKit syntax to mount package caches and pass secrets securely during construction without leaving traces in image layers.

```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim

WORKDIR /app

# 1. Use pip cache mount to speed up subsequent rebuilds
# The directory is cached on the host and reused across builds
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

# 2. Access secrets securely at build time
# The secret is mounted in memory during compilation and never committed to the image
RUN --mount=type=secret,id=api_key \
    python3 -c "import os; print('Validating private key token...')" && \
    cat /run/secrets/api_key >> /app/verification.log

COPY . .

CMD ["python3", "main.py"]
```
*To build this image passing the secret:*
```bash
export DOCKER_BUILDKIT=1
docker build --secret id=api_key,src=workspace/project/data/key.txt -t secure-app .
```

### Example 2: Deploying Static Go Binaries on a Scratch Image
Building a Golang binary and running it inside a completely empty `scratch` image (0 bytes), achieving the smallest possible attack surface.

```dockerfile
# =========================================================
# STAGE 1: Build Binary
# =========================================================
FROM golang:1.22-alpine AS builder

WORKDIR /src

COPY . .

# Compile binary statically (no dynamic C library dependencies)
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# =========================================================
# STAGE 2: Empty Scratch Runtime
# =========================================================
FROM scratch

WORKDIR /root/

# Copy the compiled binary from the build stage
COPY --from=builder /src/main .

EXPOSE 8080

CMD ["./main"]
```
*Expected image footprint:* ~10-15MB (only the compiled binary, containing zero shell utilities).

### Example 3: Healthchecks and Resource Constraints in Docker Compose
Configuring resource limits and health checks to prevent a single container from crashing the host system.

```yaml
version: '3.8'

services:
  web_service:
    image: my-app:latest
    deploy:
      resources:
        limits:
          cpus: '0.5'        # Limit CPU usage to 50% of a single core
          memory: 256M       # Limit RAM usage to 256 Megabytes
        reservations:
          memory: 64M
    restart: on-failure:5    # Restart up to 5 times on failure
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s          # Run healthcheck every 30 seconds
      timeout: 10s           # Timeout after 10 seconds
      retries: 3             # Mark container as unhealthy after 3 failed attempts
      start_period: 15s      # Grace period to allow application startup
```

### Example 4: Docker Shield - Hardened Container Runtime Configuration
This example demonstrates a secure Docker runtime execution configuration and Dockerfile design, enforcing non-root user accounts, dropping Linux capabilities, mounting read-only filesystems, and locking down write operations.

#### Hardened Dockerfile
```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-alpine AS builder
WORKDIR /usr/src/app
COPY package*.json ./
RUN npm ci --only=production
COPY . .

# Production stage
FROM alpine:3.19
# Install minimal runtime dependency (no npm, no compiler)
RUN apk add --no-cache nodejs
WORKDIR /app

# 1. Create a dedicated non-system system user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# 2. Copy production files from builder stage
COPY --from=builder /usr/src/app/node_modules ./node_modules
COPY --from=builder /usr/src/app/src ./src

# 3. Ownership update
RUN chown -R appuser:appgroup /app

# 4. Switch to the non-root user
USER appuser

EXPOSE 3000
CMD ["node", "src/index.js"]
```

#### Hardened Run Command (Docker Shield Runtime Configuration)
To run this hardened container in production, run:
```bash
docker run -d \
  --name secure-app-container \
  --read-only \
  --security-opt=no-new-privileges:true \
  --cap-drop=ALL \
  --cap-add=NET_BIND_SERVICE \
  --memory="512m" \
  --memory-swap="512m" \
  --tmpfs /tmp:rw,noexec,nosuid,size=64m \
  secure-app:latest
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate containerization competence by testing how candidates design deployment workflows for production. They check if candidates can write optimized Dockerfiles, manage data persistence, secure container configurations (avoiding root access), and troubleshoot crashed runtimes under pressure.

### Red Flags
- **Running Containers as Root**: Accepting Dockerfiles that do not specify a non-root `USER`, leaving the container vulnerable to host-takeover attacks if a container escape occurs.
- **Secrets committed to Image Layers**: Using `ENV` or `COPY` to bake passwords or API keys directly into images, allowing anyone with pull access to inspect and extract them.
- **Monolithic Image Sizes**: Creating single-stage Dockerfiles that build 2GB images containing build tools, test databases, and temp caches.
- **Incorrect Entrypoint/CMD usage**: Confusing `ENTRYPOINT` and `CMD`, resulting in container startup failures when parameters are overridden.

### Green Flags
- **Multi-Stage Builds**: Using multi-stage designs to create minimal runtime images.
- **Cache-Optimized Layers**: Ordering Dockerfile instructions (dependencies first, code last) to maximize build speed.
- **Robust Health Checks**: Defining explicit `HEALTHCHECK` parameters to allow orchestration engines to detect locked services.
- **Using .dockerignore**: Declaring a `.dockerignore` file to prevent copying `node_modules`, `.git`, or build logs into images.

### Answers Matrix
| Level | Question: "What is the difference between CMD and ENTRYPOINT in a Dockerfile?" |
|---|---|
| **Rejected** | "They both do the same thing and run when the container starts." |
| **Shortlisted** | "ENTRYPOINT defines the command that always runs, while CMD defines the default arguments passed to it. CMD can be overridden when running the container." |
| **Selected** | "ENTRYPOINT defines the core executable run when the container launches. CMD defines the default parameters passed to the entrypoint. When a user runs a container, any arguments passed in the CLI (e.g. `docker run app arg1`) override the default CMD parameters entirely, while the ENTRYPOINT command remains locked. It is best practice to use ENTRYPOINT for the system execution utility (e.g., `["python3"]`) and CMD for default arguments (e.g., `["app.py"]`), allowing developers to override inputs easily." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is the difference between a Virtual Machine (VM) and a Docker Container?
- **Detailed Answer**:
- **Virtual Machines**:
  - Virtualize physical hardware using a **Hypervisor** (Type 1 or Type 2).
  - Each VM contains a complete guest operating system, virtual drivers, and system memory allocations.
  - *Cons*: High resource overhead (gigabytes of RAM), slow boot times (minutes), and large image files.
- **Docker Containers**:
  - Virtualize the host operating system's kernel.
  - Share the host OS kernel and run as isolated processes on the host.
  - *Pros*: Minimal resource overhead (megabytes of RAM), near-instant boot times (seconds), and compact image sizes.
- **Follow-up Questions**: Can you run a Windows container on a Linux host? (Answer: No, because Windows containers require the Windows kernel, which is not available on a Linux host).
- **Interviewer's Expectations**: Compare virtualization levels (hardware vs. OS kernel), memory overheads, boot times, and OS dependencies.

#### 2. How does the Docker layer caching mechanism work?
- **Detailed Answer**: During execution of `docker build`, the engine processes instructions in the Dockerfile sequentially from top to bottom. For each instruction, Docker calculates a hash representation of the input and checks if a matching layer exists in its build cache.
- If a match exists, it reuses the layer (indicated by `---> Using cache`).
- If an instruction changes (e.g., modifying `requirements.txt` before a `COPY` step), the cache is invalidated.
- Once a layer cache is invalidated, **all subsequent layers below it** are rebuilt from scratch, regardless of whether their instructions changed.
- **Follow-up Questions**: How do you optimize layer caching? (Answer: Place stable, slow-changing instructions like dependency installation at the top, and volatile, fast-changing instructions like copying application code at the bottom).
- **Interviewer's Expectations**: Explain sequential evaluation, hash checks, cascading invalidation, and layer optimization.

#### 3. What is the difference between a Volume and a Bind Mount?
- **Detailed Answer**:
- **Volumes**:
  - Managed entirely by Docker and stored in an isolated directory on the host filesystem (e.g. `/var/lib/docker/volumes/`).
  - Isolated from direct host system access.
  - Best for production databases and persistent application data.
- **Bind Mounts**:
  - Maps an arbitrary file or directory path on the host machine directly to a path inside the container.
  - Can be modified by any process on the host.
  - Best for development (e.g., mapping code directories to enable live-reloading).
- **Follow-up Questions**: What happens to files inside a container directory when you mount a volume to it? (Answer: The files from the mounted directory replace the container's native files for the duration of the mount).
- **Interviewer's Expectations**: Compare management layers, host isolation differences, and specify clear use cases for each.

#### 4. Explain the difference between copying files via COPY and ADD.
- **Detailed Answer**:
- `COPY`: Accepts local files on the build host and copies them to the container destination path. It is simple, explicit, and preferred for most operations.
- `ADD`: Supports additional features:
  1. It can retrieve files from remote URL sources.
  2. It can automatically extract compressed tar files (`tar.gz`, `tar.xz`) into the destination directory.
- **Follow-up Questions**: Why is `COPY` preferred over `ADD` for copying local files? (Answer: `COPY` is more secure and predictable; `ADD` can execute unexpected extractions or download unsecured payloads).
- **Interviewer's Expectations**: Distinguish local file transfers (COPY) from URL downloads and archive extractions (ADD).

#### 5. What are Linux Namespaces and Cgroups, and how do they power Docker?
- **Detailed Answer**: Namespaces and Control Groups are the core Linux kernel primitives that enable container virtualization:
- **Namespaces (Isolation)**: Virtualize resources to isolate what a container process can *see*.
  - `PID`: Isolates the process tree.
  - `NET`: Isolates network interfaces.
  - `MNT`: Isolates file mount points.
  - `USER`: Isolates user and group IDs.
- **Cgroups (Control Groups)**: Limit and monitor what a container process can *use*. They restrict CPU time, memory limits, and disk I/O throughput.
- **Follow-up Questions**: Does Docker use a hypervisor? (Answer: No, Docker relies on these kernel features to isolate standard OS processes directly).
- **Interviewer's Expectations**: Define both kernel features and explain how isolation (namespaces) and resource capping (cgroups) create container boundaries.

#### 6. What is a Multi-stage build and why is it used?
- **Detailed Answer**: A Multi-stage build is a Dockerfile design pattern that utilizes multiple `FROM` instructions in a single file. Each `FROM` line begins a new build stage.
- **Why it is used**: It separates the **build-time environment** (requiring compilers, SDKs, and build dependencies) from the **runtime environment** (requiring only compiled binaries or production code).
- Developers copy the compiled artifacts from the build stage to the final stage using `COPY --from=stage_name`, discarding unnecessary build tools and reducing the size and attack surface of the production image.
- **Follow-up Questions**: How does this improve security? (Answer: By removing build tools like compiler tools or package managers from the runtime image, attackers have fewer tools to exploit if they gain access to the container).
- **Interviewer's Expectations**: Explain the multi-FROM pattern, artifact copying, and benefits (reduced image size and improved security).

#### 7. What is the difference between Docker bridge, host, and overlay networks?
- **Detailed Answer**:
- **`bridge`**: The default network driver. It creates a virtual switch on the host. Containers connected to the bridge get private IP addresses and can communicate with each other. They access the internet via NAT (Network Address Translation).
- **`host`**: Disables network isolation entirely. The container shares the host's network interfaces directly (e.g. running a container on port 80 makes it accessible directly on the host's IP port 80).
- **`overlay`**: Connects multiple Docker daemons running on different physical hosts, allowing containers to communicate across nodes without host-level port mapping.
- **Follow-up Questions**: When should you use host networking? (Answer: For high-performance applications where network performance is critical and NAT adds unacceptable overhead).
- **Interviewer's Expectations**: Compare networking isolation boundaries and identify use cases for bridge, host, and overlay drivers.

#### 8. How do you pass secrets securely to a container at runtime?
- **Detailed Answer**:
1. **Never bake secrets into the Dockerfile or image layers** using `ENV` or `COPY`.
2. Pass secrets dynamically at runtime using **environment variables** (e.g. `docker run -e DB_PASSWORD=$DB_PASS`) or using `.env` files that are excluded from Git repository commits.
3. In production orchestration environments (like Kubernetes or Docker Swarm), inject secrets as **in-memory secret mounts** (e.g. mounting files to `/run/secrets/`).
- **Follow-up Questions**: Why is passing secrets via environment variables sometimes considered insecure? (Answer: Because any process with access to the container can read environment variables, and they can be exposed in debug logs or process lists).
- **Interviewer's Expectations**: Reject image-layer secrets, recommend environment variables, and suggest secure secret mounts.

#### 9. What is the purpose of the `.dockerignore` file?
- **Detailed Answer**: The `.dockerignore` file defines a list of file matching patterns (similar to `.gitignore`) that should be excluded from the build context sent to the Docker daemon.
- **Why it matters**: When you run `docker build`, the client first packs all files in the directory and sends them to the daemon. Excluding large folders like `node_modules/`, `.git/`, test databases, or build caches speeds up build times and prevents copying sensitive configurations into image layers.
- **Follow-up Questions**: What happens if you omit `.dockerignore` when copying files? (Answer: Large directories are transferred to the daemon, increasing build times and potentially leaking developer credentials or local test files into the image).
- **Interviewer's Expectations**: Explain build context optimization, build speed improvements, and security leak preventions.

#### 10. What is a "dangling" image and how do you clean it up?
- **Detailed Answer**: A dangling image (indicated by `<none>:<none>` tags) is an image layer that has been orphaned. This occurs when you build an image with the same name and tag as an existing image, causing the older image layers to lose their tags.
- **Cleanup**: Run `docker image prune` or `docker system prune` to delete all dangling images and free up disk space.
- **Follow-up Questions**: What is the difference between `docker rm` and `docker rmi`? (Answer: `docker rm` deletes containers. `docker rmi` deletes images).
- **Interviewer's Expectations**: Define orphaned layers, explain tag replacements, and provide the command-line cleanup tools.

---

### Scenario-Based Questions

#### 11. Your Docker image is 2.5GB. Walk me through the steps you would take to reduce it.
- **Detailed Answer**:
1. **Use a Minimal Base Image**: Switch from standard OS images (like `ubuntu` or `python:3.12`) to lightweight alternatives (like `python:3.12-slim` or `node:20-alpine`).
2. **Implement Multi-Stage Builds**: Compile dependencies in a build stage and copy only the final binary or build directory to the runtime stage.
3. **Minimize Layers**: Combine multiple `RUN` commands into a single statement using logical operators (`&&` and `\`), reducing layer overhead.
4. **Clean Package Caches**: Configure package installers to disable cache storage (e.g., using `pip install --no-cache-dir` or `apt-get clean && rm -rf /var/lib/apt/lists/*`).
5. **Use `.dockerignore`**: Exclude local directories like `node_modules/` or `.git/` from being copied.
- **Follow-up Questions**: How do you inspect layer sizes? (Answer: Run `docker history <image_id>` to see the size contribution of each instruction layer).
- **Interviewer's Expectations**: Recommend minimal base images, multi-stage builds, layer reduction, package cache cleaning, and `.dockerignore` usage.

#### 12. A container crashes immediately on startup. How do you troubleshoot it?
- **Detailed Answer**:
1. Run `docker ps -a` to identify the container status and inspect its exit code.
2. Read the container's standard logs: `docker logs <container_id>`. This displays any unhandled exceptions or startup validation errors.
3. Check the command configuration: Verify if the `CMD` or `ENTRYPOINT` command is invalid or points to a missing file path.
4. Run the container interactively with a shell to bypass the entrypoint:
   ```bash
   docker run -it --entrypoint /bin/sh <image_name>
   ```
   Once inside, manually execute the startup script to identify missing directories or permission errors.
5. Use `docker inspect <container_id>` to inspect environment variables and volume mounts.
- **Follow-up Questions**: What does exit code 137 mean? (Answer: The container was terminated by the host OS because it ran out of memory (Out Of Memory - OOM)).
- **Interviewer's Expectations**: Check exit codes, read logs, override entrypoints for interactive shell runs, and inspect parameters.

#### 13. Write a Dockerfile for a Python application that runs securely as a non-root user.
- **Detailed Answer**:
```dockerfile
FROM python:3.12-slim

# Create a system group and user
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /bin/bash appuser

WORKDIR /home/appuser/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set ownership of the application directory to the non-root user
RUN chown -R appuser:appgroup /home/appuser/app

# Switch to the non-root user
USER appuser

EXPOSE 8000

CMD ["python3", "main.py"]
```
- **Follow-up Questions**: Why is running as root inside a container dangerous? (Answer: If an attacker escapes the container, they gain root privileges on the host system, compromising the entire server).
- **Interviewer's Expectations**: Add user creation steps, adjust directory ownership, and switch users using the `USER` instruction.

#### 14. Design a Docker Compose configuration where a database migrations container runs and finishes before the main application starts.
- **Detailed Answer**: I will use a combination of `depends_on` with condition checks:
```yaml
services:
  web_app:
    build: .
    ports:
      - "8080:8000"
    depends_on:
      db_migrations:
        condition: service_completed_successfully

  db_migrations:
    image: my-migration-tool:latest
    command: ["run", "migrations"]
    depends_on:
      db:
        condition: service_healthy

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_PASSWORD=pass
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5
```
- **Follow-up Questions**: Why is a standard `depends_on` list not enough? (Answer: By default, `depends_on` only waits for the dependent container to start, not for it to complete or be healthy).
- **Interviewer's Expectations**: Recommend healthcheck conditions and completion conditions (`service_completed_successfully`).

#### 15. You want to share files dynamically between two containers on the same host. How do you design this?
- **Detailed Answer**:
- I will use a **Named Volume** shared across both service definitions in Docker Compose:
```yaml
services:
  producer:
    image: writer-app:latest
    volumes:
      - shared_data:/app/output

  consumer:
    image: reader-app:latest
    volumes:
      - shared_data:/app/input

volumes:
  shared_data:
```
Both containers mount the same volume (`shared_data`). When the producer writes files to `/app/output`, they are instantly accessible to the consumer at `/app/input`.
- **Follow-up Questions**: What is the benefit of a named volume over a host bind mount for this? (Answer: Volumes are managed by Docker and are portable across environments, whereas bind mounts rely on specific host directories).
- **Interviewer's Expectations**: Recommend shared named volumes and provide the Docker Compose structure.

---

### Debugging Questions

#### 16. A container works locally but fails in production, logging: "exec user process caused: no such file or directory." How do you debug?
- **Detailed Answer**:
- **Cause**: This error is usually caused by building the image on a Windows machine with CRLF line endings in the entrypoint shell script (e.g. `entrypoint.sh`). When the Linux container attempts to execute the script, it fails because it cannot parse the carriage return `\r` character.
- **Fix**:
  1. Convert the shell script line endings from CRLF to LF using utilities like `dos2unix` or by adjusting Git line ending settings (`git config core.autocrlf false`).
  2. If using a compiled binary (like Go), check if the binary was compiled for a different target architecture (e.g. compiling for Windows/macOS and attempting to execute it in a Linux container). Compile statically: `GOOS=linux GOARCH=amd64 CGO_ENABLED=0 go build`.
- **Follow-up Questions**: How do you inspect a file's line endings? (Answer: Run `file entrypoint.sh` or check inside text editors like Vim using `:set ff?`).
- **Interviewer's Expectations**: Identify CRLF line ending mismatch and architecture compilation conflicts.

#### 17. You run a container with `-p 8080:80`, but when you navigate to `http://localhost:8080`, the request times out. How do you troubleshoot?
- **Detailed Answer**:
1. Check container status: Run `docker ps` to verify the container is active and that the port mapping is configured correctly (`0.0.0.0:8080->80/tcp`).
2. Verify application binding: Ensure the application inside the container is listening on `0.0.0.0` (all interfaces), not `127.0.0.1` (localhost loopback). If it binds to `127.0.0.1`, it will only accept connections from inside the container, causing port forwarding to fail.
3. Check host port usage: Verify if another service on the host is already using port 8080.
4. Check firewalls: Ensure host firewall rules (e.g., ufw, iptables) are not blocking traffic.
- **Follow-up Questions**: How do you test if the container's internal port is open? (Answer: Run a shell inside the container and use `curl http://localhost:80` to test locally).
- **Interviewer's Expectations**: Check process binding (0.0.0.0 vs 127.0.0.1), port mappings, and port usage conflicts.

#### 18. You modify files on your host machine, but the changes do not appear inside the container. You are using a bind mount. Why?
- **Detailed Answer**:
1. **Incorrect Path Mapping**: Check the bind mount paths in `docker run -v` or compose. The path must be absolute (e.g. `$(pwd)/src:/app/src`).
2. **File Invalidation via IDEs**: Some text editors (like Vim or WebStorm) do not modify files directly; they write updates to a temporary file, delete the original, and rename the temp file. This updates the file's **inode number** on the host, breaking the bind mount link inside the container. Disable "safe write" features in the IDE.
3. **Caching**: If using Docker Desktop on macOS or Windows, check if the file sharing permissions do not include the target folder, or if virtual machine synchronization is delayed.
- **Follow-up Questions**: How do you force a file sync? (Answer: Restart the container to recreate the bind mount mapping).
- **Interviewer's Expectations**: Identify path mapping errors, IDE safe-write behaviors (inode swaps), and file sharing configurations.

#### 20. Your host server runs out of disk space. A check shows that Docker is consuming 90% of the storage. How do you resolve this?
- **Detailed Answer**:
- **Diagnosis**: Docker accumulates orphaned images, stopped containers, build caches, and logs over time.
- **Resolution**:
  1. Run **`docker system prune -a --volumes`** to delete all stopped containers, unused networks, volumes, and dangling images.
  2. Limit container log sizes. If container logs are not capped, they can grow indefinitely in `/var/lib/docker/containers/`.
     Add log limits in `/etc/docker/daemon.json`:
     ```json
     {
       "log-driver": "json-file",
       "log-opts": {
         "max-size": "10m",
         "max-file": "3"
       }
     }
     ```
- **Follow-up Questions**: How do you see which Docker resources consume the most space? (Answer: Run `docker system df` to display a breakdown of images, containers, and volumes).
- **Interviewer's Expectations**: Recommend system prune commands, volume deletions, and log rotation caps.

---

### System Design Questions

#### 21. Design a production-grade CI/CD pipeline that compiles, tests, scans, and deploys a Docker application.
- **Detailed Answer**:
- **Source Control**: Developer pushes code to Git.
- **Compilation Stage (CI Runner)**:
  - Trigger build runner.
  - Build the Docker image using BuildKit caching to speed up compilation.
- **Testing Stage**:
  - Launch dependencies (like databases) inside a temporary network.
  - Run integration tests inside the compiled application container.
- **Security Audit Stage**:
  - Run a vulnerability scanner (like **Trivy**) on the compiled image layers.
  - Fail the build if it detects any critical CVEs.
- **Registry Push**:
  - Tag the image with the Git commit SHA (e.g. `app:sha-8812c`).
  - Push the image to a secure registry (like AWS ECR).
- **Deployment**:
  - Trigger a rolling update on the orchestration cluster (ECS/Kubernetes), pulling the new image tag.
- **Follow-up Questions**: Why use the Git commit SHA for tagging instead of `latest`? (Answer: Using `latest` makes rollbacks difficult and can cause deployment confusion; unique SHA tags guarantee reproducible deployments).
- **Interviewer's Expectations**: Detail cache optimizations, integration testing networks, security scanning (Trivy), SHA tagging, and deployment pushes.

#### 22. Design a containerized machine learning inference pipeline that scales dynamically based on request traffic.
- **Detailed Answer**:
- **Base Environment**: Build an image utilizing a base CUDA image (e.g. `nvidia/cuda`) if GPU access is required, bundling model weights, requirements, and an API service (like FastAPI).
- **Model weights separation**: Instead of baking model weights (e.g., 5GB files) into the image, store them in object storage (S3) and download them to a shared volume during container initialization, keeping image sizes small.
- **Load Balancing**: Deploy an API gateway / Load Balancer (like Nginx) to route traffic across container instances.
- **Scaling Orchestrator**: Deploy the containers on an orchestration cluster (like Kubernetes or AWS ECS). Configure horizontal pod autoscaling (HPA) to monitor container CPU usage or request rates, scaling the container count from 1 to 50 dynamically.
- **Follow-up Questions**: How does a container access the host GPU? (Answer: Use the NVIDIA Container Toolkit and pass the `--gpus all` flag to the container runtime).
- **Interviewer's Expectations**: Separate large model assets from images, optimize base layers, and detail load balancing and scaling metrics.

#### 23. Design a multi-tenant container hosting service where clients can upload and run custom Docker containers securely.
- **Detailed Answer**:
- **Host Isolation (Rootless)**: Enforce rootless Docker daemon execution for all client containers. This ensures that even if a container-breakout exploit succeeds, the client gains only non-root user privileges on the host.
- **Virtual Network Isolation**: Create separate virtual bridge networks for each tenant, blocking inter-tenant container communication.
- **Resource Constraints**: Apply strict cgroup resource limits per container (e.g., capping memory at 128MB and CPU at 20%).
- **Filesystem Isolation**: Use read-only filesystems for container runtimes, forcing clients to write temporary data to memory-based `tmpfs` mounts.
- **Hypervisor Isolation**: Instead of standard runc, run client containers using **gVisor** or **Kata Containers**. gVisor intercepts kernel system calls from the container and filters them, providing hypervisor-level isolation on shared kernels.
- **Follow-up Questions**: Why is standard Docker isolation insufficient for multi-tenant hosting? (Answer: Standard Docker shares the host kernel directly. A kernel vulnerability (kernel exploit) can allow a container process to compromise the host kernel and access other containers).
- **Interviewer's Expectations**: Recommend rootless execution, cgroup resource limits, network bridges isolation, and hypervisor-level container runtimes (gVisor).

---

## 10. Common Mistakes

- **Running Containers as Root**: Accepting Dockerfiles without declaring a non-root `USER`, leaving the container vulnerable to host-takeover attacks if a container escape occurs.
- **Secrets committed to Image Layers**: Using `ENV` or `COPY` to bake passwords or API keys directly into images, allowing anyone with pull access to inspect and extract them.
- **Monolithic Image Sizes**: Creating single-stage Dockerfiles that build 2GB images containing build tools, test databases, and temp caches.
- **Dangling volume accumulations**: Removing containers (`docker rm`) without removing associated volumes (`-v` flag), leaving orphaned data directories that consume disk space.
- **Default bridge network service discovery assumptions**: Attempting to resolve containers by name on the default bridge network, which lacks automatic DNS routing. Custom networks must be created.

---

## 11. Comparison Section: Containers vs. VMs vs. Podman

| Feature | Docker | Virtual Machine (VM) | Podman |
|---|---|---|---|
| **Virtualization Boundary** | OS Kernel | Hardware (via Hypervisor) | OS Kernel |
| **Guest Operating System** | None (shares host OS kernel) | Complete OS (Windows/Linux) | None (shares host OS kernel) |
| **Startup Time** | Near-Instant (seconds) | Slow (minutes) | Near-Instant (seconds) |
| **Resource Overhead** | Minimal | High (requires allocated memory) | Minimal |
| **Daemon Process** | Required (`dockerd` must run) | N/A | Daemonless (runs directly) |
| **Rootless by Default** | Optional | Yes | Yes (Default security model) |
| **Orchestration Compatibility**| High (Kubernetes, ECS) | Moderate | High (Kubernetes, ECS) |

---

## 12. Practical Project Ideas

### Beginner: Python API Containerization
Build a simple web server in Python (using FastAPI). Write a Dockerfile to package the application. Configure a `.dockerignore` file, build the image, and run it locally, mapping ports to verify API connectivity from your browser.

### Intermediate: Multi-Container Development Stack
Create a web application that records page views in a PostgreSQL database. Write a `docker-compose.yml` file to deploy the web application, the database, and configure a persistent named volume for the database storage.

### Advanced/Resume-worthy: Secure Multi-Stage Build & CVE Scanning Pipeline
Build a production-grade container pipeline for a React application. Create a multi-stage Dockerfile that compiles the app in a Node environment and serves the static build files via Nginx. Add a local script that runs Trivy scanning on the image, failing if it detects any high or critical vulnerabilities.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of containers vs VMs, multi-stage builds, volume setups (data persistence), and basic commands (`docker run`, `docker compose`).
- **What Engineering Teams expect**: Familiarity with containerizing applications, writing basic compose files, checking logs, and running interactive shells inside containers to troubleshoot issues.

---

## 14. Cheat Sheet

- **Build**: `docker build -t app-name:v1 .`
- **Run**: `docker run -d -p 8080:8000 --name running-app app-name:v1`
- **Compose Commands**:
  - `docker compose up -d` (Start stack in background).
  - `docker compose down` (Tear down stack).
  - `docker compose logs -f` (Follow logs).
- **Cleanup**: `docker system prune -a --volumes` (Delete unused resources).
- **Inspect**: `docker exec -it <container_id> /bin/sh` (Interactive shell).

---

## 15. One-Day Revision Guide

- [ ] Build a Dockerfile using a multi-stage build.
- [ ] Run a container with port mapping and volume mounts.
- [ ] Write a docker-compose.yml file for a web service and a database.
- [ ] Explain how namespaces and cgroups isolate container processes.
- [ ] Review how to scan a local image for vulnerabilities.
