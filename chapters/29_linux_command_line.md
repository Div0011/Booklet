# 29. Linux Command Line (Dev & Data Engineering Essentials)

## 1. Introduction

### What it is
Linux is the dominant open-source kernel and operating system family that powers modern cloud infrastructure, supercomputers, database clusters, and AI/ML model training fleets. The Linux Command Line Interface (CLI) is a text-based user interface that interacts directly with the operating system shell, providing a programmable environment to manage resources, processes, storage, and networking.

### Why it exists
Graphical User Interfaces (GUIs) are heavy, difficult to automate, and consume valuable server RAM and CPU cycles. Headless servers (servers running without a monitor or GUI) require a lightweight, high-bandwidth method of remote administration. The Linux CLI utilizes the Unix philosophy: "Write programs that do one thing and do it well. Write programs to work together. Write programs to handle text streams, because that is a universal interface."

### Problems it solves
- **Remote Administration**: Managing servers located in distant data centers over low-bandwidth connections using Secure Shell (SSH).
- **Automation and Scripting**: Writing shell scripts (Bash/Zsh) to automate software installation, database backups, and log parsing.
- **Process and Memory Debugging**: Inspecting system health, tracking memory leaks, and profiling performance bottlenecks directly from the console.
- **Reproducible Environments**: Standardizing server setup via configuration scripts, forming the foundation of DevOps and infrastructure-as-code (IaC) patterns.

### Industry Use Cases
- **Cloud Infrastructure Management**: Provisioning and configuring virtual machines, Kubernetes nodes, and network gateways.
- **Data Engineering Pipelines**: Automating ETL (Extract, Transform, Load) tasks, running cron jobs, and parsing gigabytes of raw logs.
- **Machine Learning Operations (MLOps)**: Running GPU training scripts, installing deep learning dependencies, and managing environment parameters.
- **CI/CD Build Automation**: Automating compilation, linting, testing, and deployment steps inside runner containers (e.g. GitHub Actions, GitLab CI).

### Analogy
The Linux CLI is like an automated assembly line. Every command (worker) takes raw material (text inputs), performs one transformation, and passes the result down a conveyor belt (a pipe `|`) to the next worker. Instead of moving items by hand (using a mouse to click GUI menus), you build a pipeline script that processes materials continuously and automatically.

---

## 2. Core Concepts

### Beginner Concepts
- **The Shell**: A command interpreter program that accepts text input, parses it, and invokes corresponding kernel system calls. Popular shells include `bash` (Bourne Again Shell, the Linux standard) and `zsh` (standard on macOS).
- **POSIX Filesystem Hierarchy**:
  - `/`: The root directory containing the entire directory tree.
  - `/etc`: Holds system configuration files (e.g. network parameters, user groups).
  - `/var`: Contains variable data that changes during system operation (e.g. logs in `/var/log`, mail spools).
  - `/tmp`: Temporary storage cleared on system reboots.
  - `/home`: User home directories.
  - `/bin` & `/sbin`: Core user and system administrator binaries (commands).
- **Standard File Permissions**: Every file and directory has 3 sets of permissions: Owner (User), Group, and Others. Permissions consist of: Read (`r` = 4), Write (`w` = 2), and Execute (`x` = 1). Octal representation combines these values (e.g. `755` = `rwxr-xr-x`).
- **Standard Streams & Redirection**:
  - `stdin` (File Descriptor 0): Standard input stream (default is keyboard).
  - `stdout` (File Descriptor 1): Standard output stream (default is terminal console).
  - `stderr` (File Descriptor 2): Standard error stream for logs and errors.
  - Redirection: `>` overwrites stdout to a file, `>>` appends stdout, `<` redirects input from a file, `2>` redirects errors, and `2>&1` merges stderr into stdout.

### Intermediate Concepts
- **Process Management**:
  - `PID` (Process ID): Every running process has a unique ID.
  - `ps`: Lists currently running processes. `ps aux` shows all processes running on the system with user details.
  - Signals: Control commands sent to processes (e.g. `SIGTERM` requests a graceful shutdown, `SIGKILL` forces termination).
  - Foreground vs. Background: Appending `&` to a command runs it in the background, freeing the shell.
- **Package Managers**: System utilities that automate installation, configuration, and removal of software libraries (e.g. `apt` for Debian/Ubuntu, `yum/dnf` for RHEL/CentOS, and language-specific tools like `pip` or `npm`).
- **Text Slicing and Processing**: Core utilities designed to filter and manipulate text files without loading them into memory:
  - `grep`: Searches text using regular expressions.
  - `awk`: A pattern scanning and processing language, highly effective for extracting tabular column data.
  - `sed`: Stream editor used to perform text search-and-replace mutations inline.
- **Disk and Filesystem Inspection**:
  - `df`: Shows total disk space usage across mounted filesystems.
  - `du`: Computes directory-level disk usage.
- **Networking Diagnostics**:
  - `curl` & `wget`: Utilities to download files or query API endpoints over HTTP/HTTPS/FTP.
  - `netstat` / `ss`: Displays active network sockets, routing tables, and port listeners.
  - `ssh` & `scp`: Securely connects to remote consoles and copies files over encrypted connections.

### Advanced Concepts
- **Bash Strict Mode**: A set of configuration options (`set -euo pipefail`) placed at the start of scripts to force them to exit immediately if any command returns a non-zero exit code or attempts to use an uninitialized variable, preventing silent failures.
- **Systemd and Init Systems**: Systemd is the default initialization system (PID 1) that boots the operating system and manages system services (daemons), restart policies, environment files, and system logging (`journalctl`).
- **Cron and Timers**: Schedules recurring jobs (e.g., executing a database backup script every night at 2:00 AM) using cron tab notation (`0 2 * * * /backup.sh`).
- **System Tracing (`strace`)**: A debugging utility that logs all kernel system calls (e.g., file opens, network socket writes) made by a running process, allowing developers to debug permission errors and connection drops without source code access.
- **Tmux / Screen (Terminal Multiplexers)**: Allows launching a terminal session, detaching from it to log out of the server, and re-attaching later without interrupting background jobs running in the session.

---

## 3. Internal Working

### Shell Execution Model (Fork-Exec)
When a user executes a command (e.g., `ls -l`), the shell does not run the program within its own process space. It performs a **Fork-Exec** cycle:

```text
+------------------+
|   Parent Shell   | (PID 1022 - e.g. bash)
+------------------+
         |
         | fork() System Call
         v
+------------------+
|   Child Process  | (PID 1023 - Duplicate memory space of parent shell)
+------------------+
         |
         | execve("/bin/ls", ["-l"], envp) System Call
         v
+------------------+
|    ls Program    | (Memory overwritten with 'ls' binary code; executes task)
+------------------+
         |
         | exit(0) System Call
         v
+------------------+
|  Parent Shell    | (Reaped child status via waitpid(); returns exit code $?)
+------------------+
```

1. **Fork**: The shell calls the `fork()` system call, creating a child process that is an exact duplicate of the shell's memory space.
2. **Setup File Descriptors**: If redirections (like `>` or `|`) are defined, the child process uses the `dup2()` system call to map its file descriptors (0, 1, 2) to the target files or pipe sockets.
3. **Exec**: The child process calls `execve()`, passing the path to the executable binary. The kernel discards the duplicate shell memory space and loads the binary executable into the child's process space, running the program.
4. **Wait**: The parent shell runs `waitpid()`, pausing execution until the child process terminates, capturing its exit status code (accessible in the `$?` variable).

### Filesystem Metadata (Inodes and Pointers)
Linux systems decouple a file's name from its contents on disk using **inodes** (index nodes).

```text
Directory Entry Table
+-------------+---------+
| File Name   | Inode # |
+-------------+---------+
| report.csv  | 891220  | ---> Inode 891220 Metadata Block
+-------------+---------+      +-----------------------------------------+
                               | - Owner UID: 1001                       |
                               | - Permissions: 644 (rw-r--r--)          |
                               | - File Size: 120 KB                     |
                               | - Hard Link Count: 1                    |
                               | - Data Block Pointers:                  |
                               |   [Block 502, Block 503, Block 509...]  |
                               +-----------------------------------------+
                                                |
                                                v
                                       +------------------+
                                       | Disk Data Blocks |
                                       | (Raw File Bytes) |
                                       +------------------+
```

An **Inode** is a data structure storing file metadata: owner ID, permissions, file size, timestamps, and pointers to the physical data blocks on disk. The directory is a simple lookup table mapping file names to inode numbers.
- **Hard Links**: Multiple directory filenames can point to the same inode number. The file data is only deleted from disk when the inode's "hard link count" drops to 0.
- **Soft (Symbolic) Links**: A special file containing a text string pointing to another filename path, similar to a shortcut. If the target file is deleted, the symlink breaks.

### Process States and Signals
A process moves through various execution states managed by the kernel scheduler:
- **Running/Runnable (`R`)**: The process is actively executing on a CPU core or waiting in the run queue.
- **Interruptible Sleep (`S`)**: The process is waiting for an event (like a database query response or keyboard input). It can respond to signals.
- **Uninterruptible Sleep (`D`)**: Typically waiting for direct hardware I/O (like a disk read). It cannot respond to signals, including `SIGKILL`.
- **Stopped (`T`)**: The process has been paused (e.g. by pressing Ctrl+Z or sending `SIGSTOP`).
- **Zombie (`Z`)**: The process has finished execution but its parent has not yet read its exit status code. It consumes no memory but occupies an entry in the system process table.

**Standard Signals Matrix**:
| Signal | Value | Keyboard | Default Action | Purpose | Can be Caught/Ignored? |
|---|---|---|---|---|---|
| **SIGHUP** | 1 | | Terminate | Terminal hangup; reload configs. | Yes |
| **SIGINT** | 2 | Ctrl+C | Terminate | Terminal interrupt (stop current task).| Yes |
| **SIGQUIT**| 3 | Ctrl+\ | Core Dump | Terminal quit with diagnostic dump. | Yes |
| **SIGKILL**| 9 | | Terminate | Force terminate process immediately. | **No** |
| **SIGTERM**| 15 | | Terminate | Request graceful shutdown (default). | Yes |
| **SIGSTOP**| 19 | Ctrl+Z | Stop | Pause process execution. | **No** |

---

## 4. Important Terminology

- **Shell**: A program that acts as the command interpreter (e.g. bash).
- **Kernel**: The core of the operating system managing hardware, memory, and CPU access.
- **PID (Process ID)**: Unique numeric identifier assigned to a running process.
- **PPID (Parent Process ID)**: The PID of the process that spawned the child.
- **Inode**: Database block on disk storing metadata for a file.
- **File Descriptor**: An integer index pointing to a file or network stream in the process table.
- **Pipe (`|`)**: IPC mechanism passing the stdout of one command to the stdin of another.
- **Redirection**: Mapping standard streams to files using operators like `>`, `>>`, `<`.
- **Exit Code**: Integer value (0-255) returned by a process on termination (0 indicates success).
- **Zombie Process**: A terminated process whose exit status has not been read by its parent.
- **Orphan Process**: A running process whose parent has terminated; it is adopted by PID 1 (systemd).
- **Daemon**: A background process running continuously to handle system services.
- **Umask**: A user-specific mask determining default permissions for newly created files.
- **Bash Strict Mode**: Shell options (`set -euo pipefail`) enforcing strict error handling in scripts.
- **SUID (Set Owner User ID)**: Permission bit executing a file with the permissions of the file owner.
- **SGID (Set Group ID)**: Permission bit executing a file with the permissions of the file group.
- **Sticky Bit**: Directory permission bit restricting file deletion to the file owner.
- **Hard Link**: A directory entry pointing directly to an existing inode.
- **Soft Link (Symlink)**: A reference file containing a path pointer to another file.
- **systemd**: System and service manager responsible for booting and controlling daemons.
- **journalctl**: Systemd utility used to query and inspect system and service logs.
- **xargs**: Command builder converting standard input lines into arguments for other commands.

---

## 5. Beginner Examples

### Example 1: Creating Directories and Managing Permissions
Setting up project structures and adjusting access permissions for group collaboration.
```bash
# Create directory structure with nested child folders
mkdir -p workspace/project/{src,data,logs}

# Create a sample file
touch workspace/project/src/app.py

# Set permissions: Read-Write-Execute for Owner, Read-Execute for Group, None for Others
chmod 750 workspace/project/src/app.py

# Verify permissions details (l = list, a = all, h = human readable)
ls -lah workspace/project/src/app.py
```
*Expected Output:*
```text
-rwxr-x--- 1 developer dev_group 0 Jun 11 15:20 workspace/project/src/app.py
```

### Example 2: Searching and Filtering Text Streams
Finding specific patterns inside logs and slicing text outputs.
```bash
# Append mock errors to a log file
echo "2026-06-11 15:21:00 [ERROR] Database connection failed." >> workspace/project/logs/app.log
echo "2026-06-11 15:21:05 [INFO] Retrying connection..." >> workspace/project/logs/app.log
echo "2026-06-11 15:21:10 [ERROR] Database query timeout." >> workspace/project/logs/app.log

# Search for ERROR entries recursively (-r) and show matching line numbers (-n)
grep -rn "ERROR" workspace/project/logs/
```
*Expected Output:*
```text
workspace/project/logs/app.log:1:2026-06-11 15:21:00 [ERROR] Database connection failed.
workspace/project/logs/app.log:3:2026-06-11 15:21:10 [ERROR] Database query timeout.
```

### Example 3: Querying Web APIs and Parsing Payloads
Querying endpoints and parsing JSON payloads using curl.
```bash
# Fetch HTTP headers and body from a mock API
curl -i -s https://httpbin.org/json -o workspace/project/data/response.json

# Extract and display the first 5 lines of the response
head -n 5 workspace/project/data/response.json
```

---

## 6. Intermediate Examples

### Example 1: Process Management & Job Control
Executing a training script in the background, redirecting logs, and monitoring its execution.

```bash
# 1. Run a script in the background, merging stderr (2) into stdout (1)
nohup python3 -c "import time; [print(f'Step {i}') or time.sleep(1) for i in range(60)]" > workspace/project/logs/job.log 2>&1 &

# Save the background PID
JOB_PID=$!
print "Job launched with PID: $JOB_PID"

# 2. Check process status in the system table
ps -p $JOB_PID -f

# 3. Monitor log outputs in real-time
tail -n 5 workspace/project/logs/job.log

# 4. Gracefully terminate the process using SIGTERM
kill -15 $JOB_PID
```

### Example 2: Text Slicing and Log Frequency Calculation
Analyzing access logs to identify the top 5 most active IP addresses.

```bash
# Create a mock web server log file
cat << 'EOF' > workspace/project/logs/access.log
192.168.1.5 - - [11/Jun/2026] "GET /index.html" 200
192.168.1.10 - - [11/Jun/2026] "POST /login" 401
192.168.1.5 - - [11/Jun/2026] "GET /styles.css" 200
192.168.1.12 - - [11/Jun/2026] "GET /index.html" 200
192.168.1.5 - - [11/Jun/2026] "GET /logo.png" 200
192.168.1.10 - - [11/Jun/2026] "GET /index.html" 200
EOF

# Pipeline explanation:
# 1. awk prints the first space-separated column (IP address).
# 2. sort groups identical IPs together.
# 3. uniq -c counts consecutive duplicates.
# 4. sort -rn sorts the counts numerically in reverse order.
# 5. head -n 5 displays the top 5 records.
awk '{print $1}' workspace/project/logs/access.log | sort | uniq -c | sort -rn | head -n 5
```
*Expected Output:*
```text
   3 192.168.1.5
   2 192.168.1.10
   1 192.168.1.12
```

### Example 3: Disk and Inode Usage Auditing
Finding the largest files and auditing inode counts to prevent system locks.

```bash
# 1. Audit human-readable disk use across filesystems
df -h

# 2. Audit inode usage (if inodes run out, files cannot be created even with free space)
df -i

# 3. Find files larger than 10MB in the home directory, logging errors to /dev/null
# print out sizes and paths
find ~ -type f -size +10M -exec ls -lh {} \; 2>/dev/null | awk '{print $5, $9}' | head -n 5
```

---

## 7. Advanced Concepts & Examples

### Example 1: Bash Scripting with Strict Mode
A robust pipeline automation script that checks exit codes, validates variables, and traps cleanup tasks.

```bash
#!/usr/bin/env bash

# Enable Bash Strict Mode
# -e: Exit immediately if a command returns a non-zero exit code
# -u: Exit immediately if an uninitialized variable is used
# -o pipefail: Pipeline exit status is that of the last command to fail
set -euo pipefail

# Configure Internal Field Separator to handle newlines and tabs, preventing spaces from breaking loops
IFS=$'\n\t'

# Setup temp directory cleanup trap
cleanup() {
    echo "Running cleanup task: removing temporary files..."
    rm -rf "${TEMP_DIR:-/tmp/invalid_path}"
}
# Execute cleanup function on script exit (normal or error)
trap cleanup EXIT

# Initialize variables
TEMP_DIR=$(mktemp -d)
DATA_SOURCE="https://httpbin.org/stream/5"
OUTPUT_FILE="workspace/project/data/parsed_stream.json"

echo "Temporary workspace created at: ${TEMP_DIR}"

# Download stream with timeout
curl -s -f --max-time 10 "${DATA_SOURCE}" -o "${TEMP_DIR}/raw_data.json"

# Process stream and write output
# If grep fails (no records found), strict mode -e would kill the script.
# We append '|| true' to bypass exit checks safely for expected empty matches.
grep -i "id" "${TEMP_DIR}/raw_data.json" > "${OUTPUT_FILE}" || true

# Check if output file has contents
if [ -s "${OUTPUT_FILE}" ]; then
    echo "Task Succeeded. Output lines: $(wc -l < "${OUTPUT_FILE}")"
else
    echo "Task completed: Output file is empty."
fi
```

### Example 2: Systemd Service Unit File Configuration
Running a Python backend application as a background service with auto-restart and environment configurations.

**File: `/etc/systemd/system/data_parser.service`**
```ini
[Unit]
Description=ML Log Ingestion and Processing Daemon
After=network.target

[Service]
Type=simple
User=app_worker
Group=app_workers
WorkingDirectory=/opt/log_processor
# Path to virtual environment binary
ExecStart=/opt/log_processor/venv/bin/python3 main.py
# Environment variables
Environment=PORT=8080
Environment=REDIS_URL=redis://localhost:6379/0
# Restart Policies
Restart=on-failure
RestartSec=5s
# Resource Limits
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

**Commands to register and run the service:**
```bash
# Reload systemd manager configuration
sudo systemctl daemon-reload

# Enable the service to launch automatically on system boot
sudo systemctl enable data_parser.service

# Start the service immediately
sudo systemctl start data_parser.service

# Check service logs in real-time
sudo journalctl -u data_parser.service -f -n 50
```

### Example 3: SSH Port Forwarding and Tunneling
Securing database access and exposing development servers using SSH tunnels.

```bash
# 1. Local Port Forwarding:
# Access a PostgreSQL database running on remote server port 5432 via localhost:8000
ssh -L 8000:localhost:5432 gateway_user@remote_server_ip -Nf
# -N: Do not execute a remote command (port forwarding only)
# -f: Fork SSH process into the background

# 2. Remote (Reverse) Port Forwarding:
# Expose a web app running on local port 3000 to remote server port 9000
ssh -R 9000:localhost:3000 gateway_user@remote_server_ip -Nf

# 3. Dynamic Port Forwarding (SOCKS Proxy):
# Routes all local traffic through the remote server to bypass network firewalls
ssh -D 1080 gateway_user@remote_server_ip -Nf
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate command line competence to verify candidates can operate efficiently in Linux environments common to production systems, data pipelines, and cloud servers. They look for comfort with standard streams, signal behaviors, permissionsOctals, and tracing logs under pressure.

### Red Flags
- **Arbitrary `rm -rf` usage**: Recommending file removals without verifying target paths, or using unquoted variables (e.g. `rm -rf $DIR/` which evaluates to `rm -rf /` if `$DIR` is empty).
- **Ignoring `$?` (Exit Codes)**: Designing automation scripts that ignore exit codes, allowing a pipeline to continue executing even if a download fails.
- **Root Abuse (`sudo` by default)**: Running every command with `sudo` prefix without understanding the security risks of root privilege escalation.
- **Pipe Memory Ignorance**: Loading entire gigabyte-sized files into memory using commands like `cat file | grep` instead of streaming with `grep file`.

### Green Flags
- **Strict Mode adoption**: Proactively using `set -euo pipefail` in shell scripting.
- **Composing Pipeline commands**: Using pipes, redirections, and text processors (`awk`, `xargs`) to solve complex search tasks.
- **Graceful Termination knowledge**: Knowing the difference between `SIGTERM` (graceful cleanup) and `SIGKILL` (immediate crash).
- **Disk state awareness**: Knowing that deleted files can remain open by processes, preventing disk space recovery.

### Answers Matrix
| Level | Question: "You deleted a 50GB log file but 'df -h' still shows the disk is 100% full. Why, and how do you fix it?" |
|---|---|
| **Rejected** | "The filesystem cache is delayed. You must restart the server to update it." |
| **Shortlisted** | "A process still has the file open. You need to stop the application that was writing to the log file." |
| **Selected** | "In Linux, a file is only removed from disk when its link count drops to 0 and all file descriptors pointing to it are closed. If a running process (e.g. Nginx) has the log file open, the directory link is removed, but the kernel keeps the data blocks active. To find the process holding the file, run `lsof | grep deleted`. To release the space without restarting the service, truncate the file descriptor by running `echo > /proc/<PID>/fd/<FD_NUM>` or reload the service to force it to reopen a new log file." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the difference between a Hard Link and a Soft (Symbolic) Link.
- **Detailed Answer**:
- **Hard Link**:
  - A directory entry that points directly to an existing file's **inode**.
  - Shares the same inode number as the source file.
  - Cannot span across different filesystems (partitions) and cannot link directories.
  - If the original filename is deleted, the file content remains accessible via the hard link until the inode link count drops to 0.
- **Soft Link (Symlink)**:
  - A separate file that contains a text path string pointing to another file.
  - Has its own unique inode number.
  - Can span across filesystems and can link directories.
  - If the original file is deleted, the symlink remains but becomes a "broken link," pointing to a non-existent path.
- **Follow-up Questions**: How do you create each link? (Answer: Hard link: `ln file link`. Soft link: `ln -s file link`).
- **Interviewer's Expectations**: Explain target pointers, inode allocation, cross-filesystem limits, and deletion behavior.

#### 2. What are the three standard stream file descriptors in Linux and how do you redirect them?
- **Detailed Answer**:
- `stdin` (File Descriptor 0): Receives input data. Redirect with `<` (e.g. `cmd < file.txt`).
- `stdout` (File Descriptor 1): Outputs normal messages. Redirect with `>` (overwrite) or `>>` (append).
- `stderr` (File Descriptor 2): Outputs error logs. Redirect with `2>` or `2>>`.
- To merge stderr into stdout, use `2>&1`. To discard errors entirely, redirect stderr to the null device: `2> /dev/null`.
- **Follow-up Questions**: What is `/dev/null`? (Answer: A special virtual device file that discards all data written to it, returning an end-of-file (EOF) character on read).
- **Interviewer's Expectations**: List all three streams, specify their numeric file descriptors, and show redirection syntax.

#### 3. What does `chmod 755` mean? Explain the permission octal format.
- **Detailed Answer**: `chmod 755` sets the file permissions. The three numbers correspond to the three user classes: Owner, Group, and Others.
The permissions are computed using octal values:
- Read (`r`) = 4
- Write (`w`) = 2
- Execute (`x`) = 1
- **7** (Owner): $4 + 2 + 1 = 7$ (Read, Write, and Execute: `rwx`).
- **5** (Group): $4 + 0 + 1 = 5$ (Read and Execute: `r-x`).
- **5** (Others): $4 + 0 + 1 = 5$ (Read and Execute: `r-x`).
- **Follow-up Questions**: What does `chmod +x` do? (Answer: Adds execute permission for all classes: Owner, Group, and Others).
- **Interviewer's Expectations**: Break down octal mathematics, map numbers to class groups, and translate permissions to character notation (`rwxr-xr-x`).

#### 4. How does the shell search for executable binaries when you run a command?
- **Detailed Answer**: When you enter a command (e.g. `python`), the shell first checks if it is a built-in function or alias. If not, it parses the **`$PATH` environment variable**, which contains a colon-separated list of directory paths (e.g., `/usr/bin:/bin:/usr/sbin`).
The shell scans these directories sequentially from left to right, looking for an executable file matching the command name. The first match found is executed. If no match is found, it returns `command not found`.
- **Follow-up Questions**: How do you see the path of the binary being executed? (Answer: Run the `which` or `type` command, e.g., `which python`).
- **Interviewer's Expectations**: Describe the role of the `$PATH` variable and the sequential lookup process.

#### 5. Explain the difference between `SIGTERM` (15) and `SIGKILL` (9).
- **Detailed Answer**:
- **`SIGTERM` (Signal 15)**: The default signal sent to terminate a process. It is a **request** for termination. The process can catch this signal, run cleanup tasks (e.g., closing database connections, flushing log buffers, deleting temp files), and exit gracefully.
- **`SIGKILL` (Signal 9)**: An **immediate termination command** executed at the kernel level. The process cannot catch, block, or ignore this signal. The kernel halts the process immediately, which can result in database corruption or orphaned child processes.
- **Follow-up Questions**: When should you use `SIGKILL`? (Answer: Only as a last resort when a process is unresponsive and ignores `SIGTERM` requests).
- **Interviewer's Expectations**: Contrast graceful shutdown requests (SIGTERM) with kernel-level termination commands (SIGKILL).

#### 6. What is a Zombie Process, and how do you resolve it?
- **Detailed Answer**: A Zombie Process is a process that has completed execution but still has an entry in the system process table. This occurs when a child process exits, but its parent process has not yet called the `wait()` system call to read the child's exit status.
- **Resolution**: Since zombies are already dead, you cannot terminate them using `kill -9`.
  1. Send `SIGHUP` or `SIGTERM` to the parent process to prompt it to read the child's status.
  2. If the parent remains unresponsive, terminate the parent process. Once the parent dies, the zombie children are adopted by `init` / `systemd` (PID 1), which automatically reaps their exit status and clears them from the process table.
- **Follow-up Questions**: Do zombie processes consume memory or CPU? (Answer: No, they consume no RAM or CPU, but they consume an entry in the process table, which can lock the system if the PID limit is reached).
- **Interviewer's Expectations**: Explain the parent-child wait model and detail parent-level resolution steps.

#### 7. How does the pipe operator `|` function internally?
- **Detailed Answer**: The pipe operator `|` is an Inter-Process Communication (IPC) mechanism. When you run `cmd1 | cmd2`:
1. The shell calls the `pipe()` system call, which returns two file descriptors pointing to a unidirectional data buffer managed in kernel memory.
2. The shell forks two child processes, one for `cmd1` and one for `cmd2`.
3. In the child process for `cmd1`, the shell redirects its standard output (fd 1) to the write end of the pipe.
4. In the child process for `cmd2`, the shell redirects its standard input (fd 0) to the read end of the pipe.
5. Both commands run in parallel. The kernel handles synchronization: if `cmd1` writes data faster than `cmd2` reads it, the kernel pauses `cmd1` once the buffer is full until `cmd2` reads data, avoiding memory exhaustion.
- **Follow-up Questions**: What is the size of the kernel pipe buffer? (Answer: Typically 64KB on modern Linux systems).
- **Interviewer's Expectations**: Explain kernel buffers, file descriptor duplication, and concurrent stream execution.

#### 8. What is the difference between `top` and `htop`?
- **Detailed Answer**:
- **`top`**: The standard built-in utility for real-time system process monitoring. It displays CPU use, memory usage, load averages, and process lists. It has a basic, text-based interface.
- **`htop`**: An interactive, user-friendly process viewer that requires separate installation. It displays CPU core utilization using color-coded bars, supports mouse interaction, and allows filtering, sorting, and terminating processes without typing PIDs.
- **Follow-up Questions**: What is "Load Average" in top output? (Answer: The average number of processes in a runnable or uninterruptible state over the last 1, 5, and 15 minutes).
- **Interviewer's Expectations**: Contrast the interface, interactivity, and usability of both tools.

#### 9. Explain umask and how default permissions are calculated.
- **Detailed Answer**: `umask` (User Mask) is a system parameter that determines default permissions for newly created files and directories. It acts as a bitwise filter that strips permissions.
- Default permissions for a new file are `666` (read/write).
- Default permissions for a new directory are `777` (read/write/execute).
- **Calculation**: Subtract the umask from the default permissions.
  - If umask is `022`, a new file receives permissions: `666 - 022 = 644` (`rw-r--r--`).
  - A new directory receives permissions: `777 - 022 = 755` (`rwxr-xr-x`).
- **Follow-up Questions**: Why do files not get execute permissions by default? (Answer: Security; new files should not be executable by default to prevent accidental running of untrusted code).
- **Interviewer's Expectations**: Explain umask subtraction and calculate default permission outcomes.

#### 10. What is an inode depletion error?
- **Detailed Answer**: An Inode Depletion Error occurs when a filesystem runs out of free inodes, even if there is ample disk space available. Every file and directory requires one inode to store its metadata.
If an application creates millions of tiny files (e.g. session files, temp cache keys), all available inodes on the partition can be consumed. Once depleted, any attempt to write new data or create files returns `No space left on device`, even if `df -h` shows gigabytes of free disk space.
- **Follow-up Questions**: How do you inspect inode usage? (Answer: Run `df -i`).
- **Interviewer's Expectations**: Identify inode limits separate from storage space and explain how to diagnose this error using `df -i`.

---

### Scenario-Based Questions

#### 11. A production service is running slowly. How do you identify which process is causing the bottleneck?
- **Detailed Answer**:
1. Run `top` or `htop` to identify CPU-bound processes. Look at the `%CPU` and `%MEM` columns.
2. Check the CPU state metrics:
   - If `%us` (user space) is high: The application code is executing intensive calculations.
   - If `%sy` (system space) is high: The kernel is busy handling system calls or network interrupts.
   - If `%wa` (I/O wait) is high: The system is blocked waiting for disk or network read/write operations.
3. Use `iostat -xz 1` to check disk read/write throughput and latency.
4. Run `vmstat 1` to check memory paging and context switching counts.
5. Once the process PID is identified, use `strace -p <PID> -c` to profile system call counts and locate bottlenecks.
- **Follow-up Questions**: How do you sort top outputs by memory usage? (Answer: Press `M` inside top, or configure sort columns in htop).
- **Interviewer's Expectations**: Detail CPU states, I/O wait times, context switching, and tracing tools.

#### 12. Find all CSV files in `/data` larger than 500MB that were modified more than 30 days ago.
- **Detailed Answer**: I will use the `find` command with file size and time parameters:
```bash
find /data -type f -name "*.csv" -size +500M -mtime +30
```
- **Explanation**:
  - `-type f`: Searches only for files, ignoring directories.
  - `-name "*.csv"`: Filters files matching the CSV extension.
  - `-size +500M`: Matches files larger than 500 Megabytes.
  - `-mtime +30`: Matches files whose content was modified more than 30 days ago.
- **Follow-up Questions**: How do you automatically delete these files? (Answer: Append `-delete` to the command, or pipe to xargs: `find ... | xargs rm`).
- **Interviewer's Expectations**: Show command flags for size, type, pattern name, and modification dates.

#### 13. Write a shell script snippet to check if a process with PID 2045 is running. If not, print a message and exit with code 1.
- **Detailed Answer**:
```bash
if kill -0 2045 2>/dev/null; then
    echo "Process 2045 is active."
else
    echo "Process 2045 is terminated." >&2
    exit 1
fi
```
- **Explanation**: `kill -0 <PID>` does not send a termination signal. It performs error checking, validating that the target PID exists and that the calling user has permission to send signals to it. If the process is dead, the command returns a non-zero exit status, triggering the `else` block.
- **Follow-up Questions**: What is the exit status code of a successful check? (Answer: `0`).
- **Interviewer's Expectations**: Propose efficient check methods (`kill -0` or `ps -p`) rather than parsing text outputs with grep.

#### 14. Your automation script fails occasionally because a download command hangs. How do you resolve this?
- **Detailed Answer**:
1. Configure timeouts in the download tool:
   - For `curl`: Use `--max-time 30` (overall execution limit) and `--connect-timeout 10` (connection limit).
   - For `wget`: Use `--timeout=30` and `--tries=3`.
2. Wrap the download step in a retry loop using exponential backoff:
   ```bash
   for i in {1..3}; do
       if curl -f --max-time 30 "$URL" -o file.zip; then
           break
       else
           sleep $((i * 5))
       fi
   done
   ```
- **Follow-up Questions**: Why use `--max-time` instead of just relying on default timeouts? (Answer: Default curl connection timeout is infinite, which can hang CI/CD runners indefinitely).
- **Interviewer's Expectations**: Recommend command-level timeouts and retry loops.

#### 15. You need to tail a log file in real-time, but you only want to see lines containing the word "critical" (case-insensitive) and ignore lines containing "debug".
- **Detailed Answer**: I will combine `tail -f` with pipelined `grep` commands:
```bash
tail -F /var/log/app.log | grep -i --line-buffered "critical" | grep -v --line-buffered "debug"
```
- **Explanation**:
  - `tail -F`: Follows the file, automatically reconnecting if the file is rotated or replaced.
  - `grep -i "critical"`: Performs a case-insensitive search for "critical".
  - `grep -v "debug"`: Inverts the match, filtering out lines containing "debug".
  - `--line-buffered`: Forces grep to output lines immediately instead of caching them, ensuring real-time display.
- **Follow-up Questions**: Why is `--line-buffered` important? (Answer: Without it, grep buffers output in 4KB blocks, causing updates to appear delayed).
- **Interviewer's Expectations**: Explain follow-mode, keyword filters, inverse filters, and buffer management.

---

### Debugging Questions

#### 16. A bash script fails with the message `script.sh: Permission denied`. What are your steps to resolve this?
- **Detailed Answer**:
1. Check the file permissions using `ls -l script.sh`. Verify if the execution bit (`x`) is missing.
2. Add execute permissions for the owner: `chmod u+x script.sh`.
3. Check the filesystem mounting flags. If the script is stored on a partition mounted with the `noexec` flag (e.g. `/tmp` on secured systems), the kernel blocks execution regardless of permissions. Run it explicitly via shell: `bash script.sh`.
4. Ensure the script has a correct shebang line (e.g. `#!/usr/bin/env bash`) at the first line.
- **Follow-up Questions**: What is the purpose of the shebang? (Answer: It instructs the kernel's `execve` call which interpreter to launch to execute the script's commands).
- **Interviewer's Expectations**: Check permission flags, shebang formats, and filesystem mounting limits.

#### 17. A server's network is unresponsive. You cannot access external APIs. How do you troubleshoot the network interfaces?
- **Detailed Answer**:
1. Check connection status: `ping 8.8.8.8` (checks IP routing) and `ping google.com` (checks DNS resolution).
2. Check network interface states: Run `ip addr` or `ifconfig` to verify interfaces are UP and have assigned IP addresses.
3. Check DNS configurations: Inspect `/etc/resolv.conf` to check active name servers. Run `dig google.com` or `nslookup google.com` to test DNS queries.
4. Check routing tables: Run `ip route` or `netstat -rn` to verify default gateway configurations.
5. Check ports: Run `ss -tulpn` to check active listening ports and routing filters.
- **Follow-up Questions**: What does `traceroute` do? (Answer: Logs the path and hop count that packets take to reach a destination host, helping isolate upstream connection failures).
- **Interviewer's Expectations**: Enumerate route checks, interface lookups, DNS resolutions, and port audits.

#### 18. A cron job fails to execute in production, although the script runs successfully when run manually in the terminal. Why, and how do you resolve it?
- **Detailed Answer**:
- **Why it happens**: Cron runs jobs in an isolated environment with a minimal set of environment variables. The `$PATH` variable in cron is restricted (often just `/usr/bin:/bin`). If the script references commands (like node, python, or custom scripts) located in `/usr/local/bin` or user home directories, cron cannot locate them and fails with `command not found`.
- **How to resolve**:
  1. Use absolute paths for all commands inside the script (e.g. `/usr/bin/python3` instead of `python3`).
  2. Declare the shell path and environment variables at the top of the crontab:
     ```text
     SHELL=/bin/bash
     PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
     * * * * * /path/to/script.sh
     ```
- **Follow-up Questions**: How do you capture cron error logs? (Answer: Redirect stdout and stderr to a file in the crontab definition: `* * * * * /script.sh > /tmp/cron.log 2>&1`).
- **Interviewer's Expectations**: Identify environment variables mismatch (PATH) and recommend absolute paths.

#### 19. A database service fails to start, logging: "No space left on device." But `df -h` shows 50GB of free space. How do you debug?
- **Detailed Answer**:
1. Check Inode Usage: Run `df -i`. If the inode count is at 100%, the filesystem cannot write new metadata, blocking file creation despite free storage space. Find directories containing high file counts and delete temporary files.
2. Check Deleted Files held by processes: If log files were deleted using `rm`, but the database process still holds the file descriptors open, the disk space is not released. Run `lsof +L1` or `lsof | grep deleted` to find open deleted files. Restart the corresponding process to free up disk space.
- **Follow-up Questions**: How do you safely clear file contents without deleting the file descriptor link? (Answer: Truncate the file using redirect: `> file.log`).
- **Interviewer's Expectations**: Detail inode exhaustion checks and process file descriptor holds.

#### 20. Your shell script exits immediately because of a minor command warning. How do you debug and resolve it?
- **Detailed Answer**:
- **Cause**: The script likely has Bash strict mode enabled (`set -e`), which forces the script to exit if any command returns a non-zero exit status. Even a warning or search failure (e.g., `grep` finding no matches returns exit code 1) is treated as an error, causing the script to exit.
- **Resolution**:
  1. Append `|| true` to the warning-prone command to force a successful exit status: `grep "error" app.log || true`.
  2. Temporarily disable error checks around the command:
     ```bash
     set +e
     command_with_warning
     set -e
     ```
- **Follow-up Questions**: What does `set -u` do? (Answer: Forces the shell to exit if it encounters an undeclared or uninitialized variable).
- **Interviewer's Expectations**: Identify `set -e` as the cause and show how to bypass it safely using `|| true` or `set +e`.

---

### System Design Questions

#### 21. Design an automated log rotation and storage architecture for a production web server.
- **Detailed Answer**:
- **Log Collection**: Web applications write logs to `/var/log/app/app.log`.
- **Logrotate Configuration**: Configure the standard `logrotate` daemon to manage logs:
  - **Rotation Frequency**: Rotate daily.
  - **Retention**: Keep 14 days of logs on disk.
  - **Compression**: Compress older logs using gzip (`compress`).
  - **Post-rotation**: Send a `SIGHUP` signal to the web server daemon to reopen log descriptors.
- **Off-loader Pipeline**: A cron job runs daily, compressing rotated logs and uploading them to secure object storage (e.g. AWS S3 Glacier) for long-term audit storage.
- **Monitoring**: Set up Prometheus node-exporter to track disk utilization on `/var/log` and trigger alerts when space exceeds 80%.
- **Follow-up Questions**: Why is compressing rotated logs important? (Answer: Text logs compress up to 90%, saving significant storage space).
- **Interviewer's Expectations**: Detail logrotate configurations, post-rotate signalling, off-loader storage, and space monitoring.

#### 22. Design a system monitor and alerting pipeline to track CPU, memory, and disk health across 500 Linux servers.
- **Detailed Answer**:
- **Server Agent**: Install a monitoring agent (like Prometheus Node Exporter or Datadog Agent) on every server. The agent gathers system metrics (CPU core states, disk space, IO wait times) and exposes them on a port.
- **Centralized Metrics Collector**: A centralized Prometheus server queries (scrapes) metrics from the 500 nodes periodically.
- **Alerting Engine**: Configure Prometheus Alertmanager with threshold rules:
  - Alert if `node_memory_Active_bytes / node_memory_MemTotal_bytes > 0.9` for 5 minutes (Memory exhaustion).
  - Alert if `node_filesystem_free_bytes / node_filesystem_size_bytes < 0.1` (Disk space under 10%).
- **Notification Router**: Alertmanager routes alerts to engineering channels (Slack, PagerDuty).
- **Follow-up Questions**: How do you secure metrics collection? (Answer: Run node exporters within a private network and restrict access using firewalls or mTLS certificates).
- **Interviewer's Expectations**: Propose metric scrapers (Prometheus), alerting rules, and notification integration.

#### 23. Design a zero-downtime deployment script for a backend application.
- **Detailed Answer**:
- **Directory Layout**:
  - `/opt/app/releases/`: Stores individual releases in directories named by release timestamp.
  - `/opt/app/current`: A symbolic link pointing to the active release directory (e.g. `/opt/app/releases/v1.0`).
- **Deployment Script Workflow**:
  1. Pull build code, compile dependencies, and copy to a new directory: `/opt/app/releases/v1.1`.
  2. Configure environment variables in the new directory.
  3. Start the application instance on a temporary port. Run health checks to verify it is active.
  4. Update the symbolic link atomically:
     ```bash
     ln -sfn /opt/app/releases/v1.1 /opt/app/current_temp
     mv -T /opt/app/current_temp /opt/app/current
     ```
     Moving the symbolic link replaces the reference atomically.
  5. Reload the reverse proxy (Nginx) or load balancer config to route traffic to the new instance.
  6. Stop the old application instance.
- **Follow-up Questions**: What is the benefit of using an atomic symlink swap? (Answer: It ensures that at no point is the `/opt/app/current` link missing or broken, avoiding request failures during deployments).
- **Interviewer's Expectations**: Detail release directories, atomic symlink swaps (`ln -sfn`), health validation, and proxy reload steps.

---

## 10. Common Mistakes

- **Unquoted Variables in rm Commands**: Running `rm -rf $TARGET_DIR/` in scripts. If the `$TARGET_DIR` variable is uninitialized, the command expands to `rm -rf /`, deleting the root filesystem. Always quote variables: `rm -rf "$TARGET_DIR/"`.
- **Ignoring Pipefail**: Writing scripts with `set -e` but omitting `set -o pipefail`. If a command inside a pipe fails (e.g., `failed_download | grep "data"`), the script continues because the exit code is set by the final grep command.
- **Arbitrary Shell Execution from Web**: Running random commands downloaded from the internet: `curl https://installer.com/install.sh | sh`. This is a massive security risk. Always download, inspect the script content locally, and execute it using non-root privileges.
- **Neglecting Log Rotation**: Letting applications write to a single log file without rotation until the file consumes all available disk space, locking the system.
- **Deploying Apps as Root**: Running production backend applications using the root user, allowing any remote command execution vulnerability to compromise the entire OS server.

---

## 11. Comparison Section: Bash vs. Python for Scripting Tasks

| Feature | Bash / Shell Scripting | Python Scripting |
|---|---|---|
| **Core Use Case** | Operating system commands, file piping. | Business logic, data parsing, APIs. |
| **Integration with OS utilities**| High (native executable calls). | Moderate (requires calling subprocess). |
| **Text Parsing & Processing** | Good for stream filters (awk/sed/grep). | Excellent (JSON libraries, regex engine). |
| **Code Readability / Structure** | Poor for nested loops and logic. | High (clean indentation, OOP support). |
| **Error Handling** | Basic (checking exit codes and traps). | Advanced (exceptions with try-except blocks). |
| **Ecosystem & Libraries** | Standard Unix utilities. | Massive package repository (PyPI). |
| **Multi-platform Portability** | Low (POSIX-compliant systems only). | High (runs on Windows, Linux, macOS). |

---

## 12. Practical Project Ideas

### Beginner: Automated File Organizer Script
Write a Bash script that scans a download directory, identifies files by extension, creates folders dynamically (e.g., `PDFs/`, `Images/`, `CSV_Data/`), and moves files to their corresponding folders. Log all operations to a log file.

### Intermediate: System Resource Monitoring Daemon
Write a shell script that runs continuously in the background. Check CPU, memory, and disk space usage every 10 seconds. If any metric exceeds 90%, write an alert to `/var/log/system_alerts.log`. Create a systemd service unit to manage the script.

### Advanced/Resume-worthy: Atomic Zero-Downtime Deployment Runner
Build a deployment manager script in Bash. It pulls a Python repository, builds a virtual environment, launches the app on a secondary port, runs health checks, updates symbolic links atomically, reloads Nginx, and implements rollbacks if the health check fails.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of file permission octals, basic stream redirections (`>`, `|`), signal functions (SIGTERM vs SIGKILL), and basic troubleshooting commands (`top`, `df`).
- **What Engineering Teams expect**: Familiarity with navigating remote servers over SSH, writing basic deployment scripts, reading logs with tail, and checking system health.

---

## 14. Cheat Sheet

- **Octal Permissions**:
  - `7` = `rwx` (Read, Write, Execute).
  - `6` = `rw-` (Read, Write).
  - `5` = `r-x` (Read, Execute).
  - `4` = `r--` (Read).
- **Process Signals**:
  - `kill -15 <PID>`: Graceful shutdown (SIGTERM).
  - `kill -9 <PID>`: Immediate termination (SIGKILL).
- **Stream Redirections**:
  - `>`: Overwrite stdout.
  - `>>`: Append stdout.
  - `2>`: Redirect stderr.
  - `2>&1`: Merge stderr into stdout.
- **Pipe**: `cmd1 | cmd2` passes output of cmd1 to input of cmd2.

---

## 15. One-Day Revision Guide

- [ ] Practice navigating directories and setting permissions via octal codes.
- [ ] Write a pipeline command using grep, awk, and sort to find errors in log files.
- [ ] Understand how the shell executes commands using the Fork-Exec model.
- [ ] Review how to create and manage systemd service unit files.
- [ ] Explain how a deleted file can still occupy disk space if held open by a process.
- [ ] Verify you know the difference between SIGTERM and SIGKILL.
