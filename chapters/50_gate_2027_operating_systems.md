# 50. GATE 2027: Operating Systems & System Architecture

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Core Concepts](#2-core-concepts)
  - [2.1 Beginner Level (Processes, Threads & System Calls)](#21-beginner-level)
  - [2.2 Intermediate Level (CPU Scheduling & Concurrency Synchronization)](#22-intermediate-level)
  - [2.3 Advanced Level (Deadlocks, Virtual Memory & Storage Subsystems)](#23-advanced-level)
- [3. Internal Working](#3-internal-working)
- [4. Important Terminology](#4-important-terminology)
- [5. Beginner Examples](#5-beginner-examples)
- [6. Intermediate Examples](#6-intermediate-examples)
- [7. Advanced Examples](#7-advanced-examples)
- [8. How Interviewers Think](#8-how-interviewers-think)
- [9. FAQs (25 High-Yield GATE & Interview Questions)](#9-faqs)
- [10. Common Mistakes](#10-common-mistakes)
- [11. Comparison Tables](#11-comparison-tables)
- [12. Practical Projects](#12-practical-projects)
- [13. Internship Preparation](#13-internship-preparation)
- [14. Cheat Sheet](#14-cheat-sheet)
- [15. One-Day Revision Checklist](#15-one-day-revision-checklist)

---

## 1. Introduction

### What is an Operating System?
An **Operating System (OS)** is system software that acts as an intermediary between the user applications and computer hardware. It provides an abstract execution environment, manages system resources (CPU, Memory, Storage, I/O devices), and guarantees resource protection, process isolation, and concurrent execution.

### Why it Exists & Problems it Solves
1. **Hardware Abstraction:** Shields application programmers from hardware complexity (e.g., standard POSIX file read/write vs. physical disk sector timings).
2. **Concurrency & Multitasking:** Multiplexes CPU execution across hundreds of processes while preventing data corruption via synchronization primitives.
3. **Memory Virtualization:** Gives each process the illusion of owning a contiguous, isolated, private memory address space through demand paging and TLBs.

---

## 2. Core Concepts

### 2.1 Beginner Level

#### Processes, Threads & System Calls
- **Process Definition:** Program in execution. Contains text (code), data (global variables), heap (dynamic allocation), stack (local variables and activation records), and PCB (Process Control Block).
- **Process State Machine:** New $ightarrow$ Ready $\leftrightarrow$ Running $ightarrow$ Waiting/Blocked $ightarrow$ Terminated.
- **Threads:** Lightweight execution units within a process. Share address space (code, data, files) but have private register sets and stacks. User-level threads vs Kernel-level threads (1:1, M:1, M:N mapping models).
- **System Calls:** Programmatic requests to OS kernel via software interrupts / trap instructions (e.g., `fork()`, `exec()`, `wait()`, `read()`, `write()`). Mode switch from User Mode (Ring 3) to Kernel Mode (Ring 0).

---

### 2.2 Intermediate Level

#### CPU Scheduling Algorithms
- **Performance Metrics:** Arrival Time ($AT$), Burst Time ($BT$), Completion Time ($CT$), Turnaround Time ($TAT = CT - AT$), Waiting Time ($WT = TAT - BT$), Response Time ($RT$).
- **Algorithms:**
  - **FCFS (First-Come First-Served):** Non-preemptive. Suffers from Convoy Effect.
  - **SJF (Shortest Job First):** Optimal for minimizing average waiting time. Non-preemptive. Requires future burst knowledge.
  - **SRTF (Shortest Remaining Time First):** Preemptive SJF. Can starve long CPU-intensive jobs.
  - **Round Robin (RR):** Preemptive with time quantum $q$. If $q ightarrow \infty$, behaves like FCFS; if $q ightarrow 0$, context switch overhead dominates.
  - **Priority Scheduling:** Preemptive / Non-preemptive. Mitigated against starvation via Aging.

#### Process Synchronization & Concurrency
- **Critical Section Problem Requirements:**
  1. **Mutual Exclusion:** Only one process inside critical section at a time.
  2. **Progress:** If CS is empty, only processes wishing to enter participate in decision; cannot be delayed indefinitely.
  3. **Bounded Waiting:** Bound on number of times other processes enter CS before a requesting process is granted access.
- **Software Solutions:** Peterson's Algorithm (2 processes, strictly satisfies all 3 criteria using `flag[2]` and `turn`).
- **Hardware Primitives:** TestAndSet, Swap / CompareAndSwap.
- **Semaphores:** Integer variables accessed via atomic `wait()` (P) and `signal()` (V). Binary (Mutex) vs Counting Semaphores.
- **Classical IPC Problems:** Producer-Consumer (Bounded Buffer), Readers-Writers (Reader priority vs Writer priority), Dining Philosophers (deadlock avoidance via asymmetric pickup or limiting diners).

---

### 2.3 Advanced Level

#### Deadlocks
- **Four Necessary & Sufficient Coffman Conditions:**
  1. Mutual Exclusion
  2. Hold and Wait
  3. No Preemption
  4. Circular Wait
- **Handling Strategies:**
  - **Ignoration (Ostrich Algorithm):** Used by general-purpose OS (Linux, Windows).
  - **Deadlock Prevention:** Invalidate at least one of the 4 Coffman conditions (e.g., resource ordering for Circular Wait).
  - **Deadlock Avoidance:** Banker's Algorithm. System maintains a **Safe State** using vectors `Allocation`, `Max`, `Need = Max - Allocation`, and `Available`.
  - **Deadlock Detection & Recovery:** Resource Allocation Graph (RAG) cycle detection ($O(V+E)$ for single instance; matrix reduction for multi-instance).

#### Memory Management & Virtual Memory
- **Address Translation:** Logical Address divided into Page Number ($p$) and Page Offset ($d$). Physical Address divided into Frame Number ($f$) and Frame Offset ($d$).
- **Multi-Level Paging:** Breaks large page tables into pages. Translation lookaside buffer (TLB) speeds up access:
  $$	ext{Effective Access Time (EAT)} = h \cdot (t_{TLB} + t_{MEM}) + (1 - h) \cdot (t_{TLB} + (n+1) \cdot t_{MEM})$$
- **Inverted Page Table:** One entry per physical frame instead of per virtual page. Saves massive physical memory.
- **Page Replacement Algorithms:**
  - **FIFO:** Suffers from Belady's Anomaly (more frames $\implies$ more page faults).
  - **Optimal (OPT / MIN):** Replaces page not used for longest time in future. Provably minimum page faults.
  - **LRU (Least Recently Used):** Stack algorithm (immune to Belady's anomaly). Approximated via Clock / Second-Chance algorithm.
- **Thrashing:** Excessive page faulting occurring when sum of process Working Sets exceeds available physical memory ($\sum WSS_i > D$).

---

## 3. Internal Working

### 3.1 Paging Translation & TLB Cache Hit/Miss Architecture
```
 Logical Address: [ Page Number (p) | Page Offset (d) ]
                         │
                         ▼
               ┌──────────────────┐
               │    TLB Search    │
               └─────────┬────────┘
                         │
        ┌────────────────┴────────────────┐
     TLB Hit                           TLB Miss
        │                                 │
        ▼                                 ▼
 [ Frame Number (f) ]            [ Page Table Lookup ]
        │                        (Reads from Main Memory)
        │                                 │
        ├─────────────────────────────────┘
        ▼
 Physical Address: [ Frame Number (f) | Offset (d) ]
        │
        ▼
   [ Main Memory RAM Access ]
```

---

## 4. Important Terminology

- **PCB (Process Control Block):** Kernel data structure storing PID, state, registers, memory limits, and open file descriptors.
- **Context Switch:** Switching the CPU from one process to another, saving/loading state registers and flushing/reloading page tables.
- **Peterson's Algorithm:** Software mutual exclusion algorithm for 2 processes guaranteeing mutual exclusion, progress, and bounded waiting.
- **Semaphore:** Synchronization primitive with atomic wait ($P$) and signal ($V$) operations.
- **Belady's Anomaly:** Phenomenon where allocating more physical page frames increases the total number of page faults (occurs in FIFO, not in LRU/Optimal).
- **Thrashing:** System state where the CPU spends more time swapping pages in/out than executing user instructions.
- **TLB (Translation Lookaside Buffer):** Fast hardware associative cache that stores recently used virtual-to-physical page mappings.
- **Banker's Algorithm:** Deadlock avoidance algorithm that simulates resource allocations to ensure the system remains in a safe state.

---

## 5. Beginner Examples

### Example 1: Peterson's Mutual Exclusion Implementation
```c
// Shared variables
int flag[2] = {0, 0};
int turn = 0;

void process_i(int i) {
    int j = 1 - i;
    while (1) {
        // Entry Section
        flag[i] = 1;
        turn = j;
        while (flag[j] && turn == j) {
            // Busy wait
        }

        // Critical Section
        // ... perform concurrent-safe work ...

        // Exit Section
        flag[i] = 0;

        // Remainder Section
    }
}
```

---

## 6. Intermediate Examples

### Example 2: Effective Memory Access Time (EMAT) Calculation
**Given:**
- TLB Hit Ratio $h = 90\% = 0.9$
- TLB Access Time $t_{TLB} = 10	ext{ ns}$
- Main Memory Access Time $t_{MEM} = 100	ext{ ns}$
- 2-Level Page Table ($n=2$)

$$	ext{EAT} = h \cdot (t_{TLB} + t_{MEM}) + (1 - h) \cdot (t_{TLB} + (n+1) \cdot t_{MEM})$$
$$	ext{EAT} = 0.9 \cdot (10 + 100) + 0.1 \cdot (10 + (2+1) \cdot 100)$$
$$	ext{EAT} = 0.9 \cdot (110) + 0.1 \cdot (310) = 99 + 31 = 130	ext{ ns}$$

---

## 7. Advanced Examples

### Example 1: Banker's Deadlock Avoidance Algorithm
**Given State:** 5 Processes ($P_0 - P_4$), 3 Resource Types ($A=10, B=5, C=7$).
`Allocation` and `Max` matrices given:
```
Process | Allocation (A B C) | Max (A B C) | Need = Max - Alloc
   P0   |      0 1 0         |    7 5 3    |      7 4 3
   P1   |      2 0 0         |    3 2 2    |      1 2 2
   P2   |      3 0 2         |    9 0 2    |      6 0 0
   P3   |      2 1 1         |    2 2 2    |      0 1 1
   P4   |      0 0 2         |    4 3 3    |      4 3 1
Available = (3, 3, 2)
```
1. Test $P_1$: $Need_1 (1, 2, 2) \le Available (3, 3, 2)$. Execute $P_1$.
   $Available = (3, 3, 2) + (2, 0, 0) = (5, 3, 2)$.
2. Test $P_3$: $Need_3 (0, 1, 1) \le Available (5, 3, 2)$. Execute $P_3$.
   $Available = (5, 3, 2) + (2, 1, 1) = (7, 4, 3)$.
3. Test $P_0$: $Need_0 (7, 4, 3) \le Available (7, 4, 3)$. Execute $P_0$.
   $Available = (7, 4, 3) + (0, 1, 0) = (7, 5, 3)$.
4. Test $P_2$: $Need_2 (6, 0, 0) \le Available (7, 5, 3)$. Execute $P_2$.
   $Available = (7, 5, 3) + (3, 0, 2) = (10, 5, 5)$.
5. Test $P_4$: $Need_4 (4, 3, 1) \le Available (10, 5, 5)$. Execute $P_4$.
   $Available = (10, 5, 5) + (0, 0, 2) = (10, 5, 7)$.
**Safe Sequence Exists:** $\langle P_1, P_3, P_0, P_2, P_4 angle$. System is in a SAFE STATE.

---

## 8. How Interviewers Think

- **Preemption Traps:** Look out for non-preemptive scheduling vs preemptive variants (e.g., SJF vs SRTF).
- **Belady's Anomaly Triggers:** Only FIFO and FIFO-variant queue algorithms exhibit Belady's anomaly; stack algorithms like LRU and Optimal are provably immune.
- **Counting Semaphore Math:** If initial value is $S=10$, after $6P$ operations and $4V$ operations, final value is $10 - 6 + 4 = 8$.

---

## 9. FAQs (25 High-Yield GATE & Interview Questions)

### Q1: What is the primary difference between a process and a thread?
**Answer:** A process is an independent execution entity with its own dedicated memory space (code, data, heap, page tables). A thread is an execution slice within a process that shares code, heap, and open file descriptors with sibling threads, maintaining only its private stack, program counter, and registers.

### Q2: Why is Peterson's algorithm not used on modern multi-core processors directly?
**Answer:** Modern superscalar CPUs perform out-of-order execution and compiler instruction reordering, which violates the strict sequential memory consistency assumed by Peterson's algorithm without explicit memory barriers (`mfence`).

### Q3: What is the cause of Thrashing and how does the OS resolve it?
**Answer:** Thrashing occurs when high degree of multiprogramming causes the sum of process working set sizes to exceed available physical RAM, leading to constant page faults. The OS resolves it by reducing the degree of multiprogramming (suspending/swapping out entire processes).

---

## 10. Common Mistakes

| Anti-Pattern | Why It Is Wrong | Correct Approach |
| :--- | :--- | :--- |
| Forgetting memory accesses in multi-level paging | A $k$-level page table requires $k$ memory accesses for page table entries + 1 for actual data | On a TLB miss, total accesses = $k+1$. On TLB hit, total accesses = 1 |
| Confusing Deadlock Prevention with Avoidance | Prevention removes necessary conditions statically; Avoidance checks safety dynamically | Avoidance uses Banker's algorithm; Prevention uses protocols like strict resource hierarchy |

---

## 11. Comparison Tables

### Page Replacement Algorithms Comparison
| Algorithm | Belady's Anomaly? | Implementation Complexity | Optimality |
| :--- | :--- | :--- | :--- |
| **FIFO** | Yes | Low ($O(1)$ queue) | Poor |
| **Optimal**| No | Unimplementable (needs future knowledge)| Provably Best |
| **LRU** | No | Medium ($O(1)$ hash map + doubly linked list)| Near Optimal |
| **Clock** | No (Second Chance) | Low (Single circular pointer + use bit) | Good approximation |

---

## 12. Practical Projects

### Project: Simulating Producer-Consumer with POSIX Mutex & Semaphores in C
```c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>

#define BUFFER_SIZE 5
int buffer[BUFFER_SIZE];
int in = 0, out = 0;

sem_t empty_slots;
sem_t full_slots;
pthread_mutex_t mutex;

void* producer(void* arg) {
    for (int i = 0; i < 10; i++) {
        sem_wait(&empty_slots);
        pthread_mutex_lock(&mutex);

        buffer[in] = i;
        printf("Producer produced: %d at index %d\n", i, in);
        in = (in + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&full_slots);
        usleep(50000);
    }
    return NULL;
}

void* consumer(void* arg) {
    for (int i = 0; i < 10; i++) {
        sem_wait(&full_slots);
        pthread_mutex_lock(&mutex);

        int item = buffer[out];
        printf("Consumer consumed: %d from index %d\n", item, out);
        out = (out + 1) % BUFFER_SIZE;

        pthread_mutex_unlock(&mutex);
        sem_post(&empty_slots);
        usleep(80000);
    }
    return NULL;
}
```

---

## 13. Internship Preparation

1. Implement process synchronization using mutexes and condition variables.
2. Master calculations for multi-level page tables, TLB effective access times, and inverted page tables.
3. Be able to calculate Gantt charts for FCFS, SJF, SRTF, and Round Robin without errors.
4. Understand Banker's Algorithm safety checking.
5. Review Unix file system inodes, direct/indirect blocks, and disk scheduling algorithms.

---

## 14. Cheat Sheet

- **Turnaround Time ($TAT$):** $TAT = 	ext{Completion Time} - 	ext{Arrival Time}$.
- **Waiting Time ($WT$):** $WT = TAT - 	ext{Burst Time}$.
- **Effective Access Time ($EAT$):** $h(t_{TLB} + t_{MEM}) + (1-h)(t_{TLB} + (n+1)t_{MEM})$.
- **Maximum File Size via Inodes:**
  $$	ext{Max Size} = (	ext{Direct} + 	ext{Single} \cdot rac{B}{P} + 	ext{Double} \cdot (rac{B}{P})^2 + 	ext{Triple} \cdot (rac{B}{P})^3) 	imes 	ext{Block Size}$$
- **Banker's Condition:** If $Need \le Available$, allocate and release $Allocation$ to $Available$.

---

## 15. One-Day Revision Checklist

- [ ] Draw process lifecycle state diagram and list context switch steps.
- [ ] Solve a 4-process CPU scheduling Gantt chart (SRTF & Round Robin).
- [ ] Verify Peterson's algorithm code and 3 critical section properties.
- [ ] Calculate EMAT for a 2-level paging system with TLB hit and miss.
- [ ] Run Banker's Algorithm on a 5-process allocation table.
- [ ] Review Belady's anomaly counter-example on FIFO (3 vs 4 frames).
