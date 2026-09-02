# 52. GATE 2027: High-Yield Formula Sheet & Master Reference (CS & DA)

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Time & Space Complexity Master Matrix](#2-time--space-complexity-master-matrix)
- [3. Formal Languages & Chomsky Decidability Reference](#3-formal-languages--chomsky-decidability-reference)
- [4. Engineering Mathematics Formulas](#4-engineering-mathematics-formulas)
- [5. Digital Logic & Computer Architecture Formulas](#5-digital-logic--computer-architecture-formulas)
- [6. Operating Systems & Memory Management Formulas](#6-operating-systems--memory-management-formulas)
- [7. Databases, Normalization & Relational Theory](#7-databases-normalization--relational-theory)
- [8. Computer Networks & Protocol Calculations](#8-computer-networks--protocol-calculations)
- [9. Machine Learning & AI Reference Formulas](#9-machine-learning--ai-reference-formulas)
- [10. Common Numerical Traps in GATE](#10-common-numerical-traps-in-gate)
- [11. Master Formula Comparison Tables](#11-master-formula-comparison-tables)
- [12. Quick Revision Cards](#12-quick-revision-cards)
- [13. Top 30 High-Yield Numerical Formulas](#13-top-30-high-yield-numerical-formulas)
- [14. Quick Cheat Sheet](#14-quick-cheat-sheet)
- [15. Final Exam Day Checklist](#15-final-exam-day-checklist)

---

## 1. Introduction
This master reference chapter consolidates every high-yield mathematical formula, complexity boundary, decidability result, and architectural equation across all 14 subjects of the GATE 2027 Computer Science (CS) and Data Science & AI (DA) syllabi.

---

## 2. Time & Space Complexity Master Matrix

| Data Structure / Algorithm | Access | Search | Insertion | Deletion | Space |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Array** | $O(1)$ | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| **Singly Linked List** | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| **Binary Search Tree (BST)**| $O(h)$ | $O(h)$ | $O(h)$ | $O(h)$ | $O(n)$ |
| **AVL Tree / Red-Black Tree**| $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **B-Tree / B+ Tree** | $O(\log_B n)$ | $O(\log_B n)$ | $O(\log_B n)$ | $O(\log_B n)$ | $O(n)$ |
| **Hash Table** | - | $O(1)$ avg / $O(n)$ | $O(1)$ avg / $O(n)$ | $O(1)$ avg / $O(n)$ | $O(n)$ |
| **Binary Heap** | $O(1)$ min/max| $O(n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

### Sorting Algorithms Complexity
| Algorithm | Best Time | Average Time | Worst Time | Space | Stable? |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bubble Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| **Insertion Sort** | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes |
| **Selection Sort** | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No |
| **Merge Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes |
| **Quick Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No |
| **Heap Sort** | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | No |
| **Counting Sort** | $O(n+k)$ | $O(n+k)$ | $O(n+k)$ | $O(k)$ | Yes |

---

## 3. Formal Languages & Chomsky Decidability Reference

### Closure Properties Matrix
| Operation | Regular | DCFL | CFL | CSL | Recursive | RE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Union** | Yes | No | Yes | Yes | Yes | Yes |
| **Intersection** | Yes | No | No | Yes | Yes | Yes |
| **Complement** | Yes | Yes | No | Yes | Yes | No |
| **Concatenation**| Yes | No | Yes | Yes | Yes | Yes |
| **Kleene Star** | Yes | No | Yes | Yes | Yes | Yes |
| **Intersection with Regular** | Yes | Yes | Yes | Yes | Yes | Yes |

### Decidability Decision Table
| Question / Problem | Regular | DCFL | CFL | CSL | REC | RE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Membership ($w \in L$)** | Decidable | Decidable | Decidable | Decidable | Decidable | Semi-Decidable |
| **Emptiness ($L = \emptyset$)** | Decidable | Decidable | Decidable | Undecidable| Undecidable| Undecidable |
| **Finiteness ($|L| < \infty$)**| Decidable | Decidable | Decidable | Undecidable| Undecidable| Undecidable |
| **Equivalence ($L_1 = L_2$)** | Decidable | Decidable | Undecidable| Undecidable| Undecidable| Undecidable |
| **Totality ($L = \Sigma^*$)** | Decidable | Decidable | Undecidable| Undecidable| Undecidable| Undecidable |
| **Ambiguity of Grammar** | Decidable | - | Undecidable| Undecidable| Undecidable| Undecidable |

---

## 4. Engineering Mathematics Formulas

### Linear Algebra
- $	ext{Rank}(A) + 	ext{Nullity}(A) = n$ (Number of columns).
- $\det(A) = \prod_{i=1}^n \lambda_i$, $	ext{Trace}(A) = \sum_{i=1}^n \lambda_i$.
- Eigenvalues of $A^k$ are $\lambda_i^k$; Eigenvalues of $A^{-1}$ are $rac{1}{\lambda_i}$.
- Cayley-Hamilton Theorem: Every square matrix satisfies its own characteristic equation $p(A) = 0$.

### Calculus & Optimization
- **Taylor Series:** $f(x) = \sum_{n=0}^\infty rac{f^{(n)}(a)}{n!} (x-a)^n$.
- **Stationary Points:** $
abla f(x) = 0$.
- **Second Derivative Test:** Hessian matrix $H$. If $H \succ 0$ (positive definite) $\implies$ Local Minimum; if $H \prec 0$ (negative definite) $\implies$ Local Maximum; if indefinite $\implies$ Saddle point.

### Probability & Statistics
- **Bayes' Rule:** $P(A \mid B) = rac{P(B \mid A) P(A)}{P(B)}$.
- **Variance:** $	ext{Var}(X) = E[X^2] - (E[X])^2$.
- **Covariance:** $	ext{Cov}(X, Y) = E[XY] - E[X]E[Y]$.
- **Chebyshev's Inequality:** $P(|X - \mu| \ge k\sigma) \le rac{1}{k^2}$.

---

## 5. Digital Logic & Computer Architecture Formulas

### Pipelining & Cache Math
- **Pipeline Speedup:**
  $$S = rac{	ext{Execution Time (Non-Pipelined)}}{	ext{Execution Time (Pipelined)}} = rac{n \cdot k}{(k + n - 1) + 	ext{Stalls}}$$
  $$	ext{Ideal Speedup (as } n ightarrow \infty) = k$$
- **Effective Memory Access Time (EMAT):**
  $$	ext{EMAT} = h_1 \cdot t_1 + (1 - h_1) \cdot [h_2 \cdot (t_1 + t_2) + (1 - h_2) \cdot (t_1 + t_2 + t_{MEM})]$$
- **Cache Tag Bits (Direct Mapped):**
  $$	ext{Physical Address Bits} = 	ext{Tag Bits} + 	ext{Line/Index Bits} + 	ext{Block/Byte Offset Bits}$$
- **Cache Tag Bits ($k$-Way Set Associative):**
  $$	ext{Set Index Bits} = \log_2(	ext{Number of Sets}) = \log_2\left(rac{	ext{Total Cache Lines}}{k}ight)$$

---

## 6. Operating Systems & Memory Management Formulas

- **Turnaround Time:** $TAT = CT - AT$.
- **Waiting Time:** $WT = TAT - BT$.
- **Paging Effective Access Time (EMAT with TLB):**
  $$	ext{EMAT} = h \cdot (t_{TLB} + t_{MEM}) + (1 - h) \cdot (t_{TLB} + (n+1) \cdot t_{MEM})$$
- **Inverted Page Table Size:**
  $$	ext{Size} = 	ext{Number of Physical Frames} 	imes 	ext{Size of Frame Entry}$$

---

## 7. Databases, Normalization & Relational Theory

- **1NF:** All attribute values are atomic.
- **2NF:** 1NF + No partial dependency (no non-prime attribute depends on a proper subset of candidate key).
- **3NF:** 2NF + No transitive dependency ($X ightarrow Y \implies X$ is superkey OR $Y$ is prime attribute).
- **BCNF:** For every non-trivial FD $X ightarrow Y$, $X$ must be a superkey.
- **Maximum B+ Tree Keys:** Order $p \implies$ Max keys in internal node $= p - 1$, Min keys in non-root internal node $= \lceil p/2 ceil - 1$.

---

## 8. Computer Networks & Protocol Calculations

- **Transmission Delay:** $T_t = rac{L}{B}$ (Length of packet / Bandwidth).
- **Propagation Delay:** $T_p = rac{d}{v}$ (Distance / Propagation Speed).
- **Round Trip Time:** $RTT = 2 \cdot T_p$.
- **Stop-and-Wait Efficiency:**
  $$\eta = rac{T_t}{T_t + 2 T_p} = rac{1}{1 + 2a} \quad 	ext{where } a = rac{T_p}{T_t}$$
- **Optimal Window Size ($W$):** $W = 1 + 2a$.
- **Sliding Window Efficiency:**
  - **Go-Back-N:** $\eta = \min\left(1, rac{N}{1 + 2a}ight)$ with sequence number space $\ge N + 1$.
  - **Selective Repeat:** $\eta = \min\left(1, rac{N}{1 + 2a}ight)$ with sequence number space $\ge 2N$.
- **CSMA/CD Minimum Frame Size:**
  $$L_{min} = 2 \cdot T_p 	imes B$$

---

## 9. Machine Learning & AI Reference Formulas

- **K-Means Objective:** $J = \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$.
- **$A^*$ Search Evaluation:** $f(n) = g(n) + h(n)$.
- **Singular Value Decomposition:** $A = U \Sigma V^T$.
- **PCA Covariance Matrix:** $\Sigma = rac{1}{N} X^T X$ (for zero-mean data).
- **Bayesian Network Joint Probability:** $P(X_1, \dots, X_n) = \prod_{i=1}^n P(X_i \mid 	ext{Parents}(X_i))$.

---

## 10. Common Numerical Traps in GATE

1. **Byte vs Bit units in Networks:** Bandwidth is given in bits/sec ($1	ext{ Mbps} = 10^6	ext{ bps}$), file size is given in Bytes ($1	ext{ KB} = 2^{10}	ext{ Bytes}$ or $10^3	ext{ Bytes}$).
2. **LR(0) vs SLR(1) reduction rows:** In LR(0), reduce actions fill all terminal columns; in SLR(1), reduce actions only appear in $FOLLOW(A)$ columns.
3. **Pipelining Clock Cycle Time:** Non-pipelined delay $T = \sum t_i$; Pipelined cycle $	au = \max(t_i) + t_{register}$.

---

## 11. Master Formula Comparison Tables

| Topic | Equation / Rule | Key Caveat |
| :--- | :--- | :--- |
| **Pipeline Speedup** | $S = rac{n \cdot k}{k + n - 1 + 	ext{stalls}}$ | Check whether register delay is added to stage time |
| **Cache EMAT** | $h \cdot t_c + (1-h)(t_c + t_m)$ | Check if cache access is simultaneous or hierarchical |
| **CSMA/CD Frame Size** | $L \ge 2 \cdot T_p 	imes B$ | Factor of 2 accounts for worst-case collision detection RTT |
| **Stop & Wait Efficiency** | $rac{1}{1 + 2a}$ | $a = T_p / T_t$; acknowledgment transmission time assumed negligible |

---

## 12. Quick Revision Cards

- **Rank-Nullity Theorem:** $	ext{Rank} + 	ext{Nullity} = n$.
- **Eigenvalue Properties:** Sum of eigenvalues = Trace; Product of eigenvalues = Determinant.
- **Master Theorem:** $T(n) = a T(n/b) + \Theta(n^k \log^p n)$. Compare $a$ with $b^k$.
- **Banker's Condition:** Allocate if $Need \le Available$.
- **Rice's Theorem:** Non-trivial semantic property of RE language is Undecidable.
- **B+ Tree Leaf Node:** All data records/pointers reside solely at leaf level; leaves connected via linked list.

---

## 13. Top 30 High-Yield Numerical Formulas

1. $a = rac{T_p}{T_t} = rac{d \cdot B}{v \cdot L}$.
2. $L_{min} = 2 \cdot rac{d}{v} \cdot B$.
3. $	ext{Efficiency}_{	ext{Stop-Wait}} = rac{1}{1 + 2a}$.
4. $	ext{Efficiency}_{	ext{GBN}} = rac{W}{1 + 2a}$ (where $W \le 2^k - 1$).
5. $	ext{Efficiency}_{	ext{SR}} = rac{W}{1 + 2a}$ (where $W \le 2^{k-1}$).
6. $	ext{Speedup} = rac{k}{1 + 	ext{Stalls per instruction}}$.
7. $	ext{CPI}_{	ext{pipelined}} = 1 + 	ext{Stalls per instruction}$.
8. $	ext{EMAT} = t_{TLB} + t_{MEM} + (1-h) \cdot n \cdot t_{MEM}$.
9. $	ext{Block Offset Bits} = \log_2(	ext{Block Size in Bytes})$.
10. $	ext{Index Bits} = \log_2(	ext{Number of Sets})$.
11. $	ext{Tag Bits} = 	ext{Address Bits} - 	ext{Index Bits} - 	ext{Offset Bits}$.
12. $	ext{Max Keys in B-Tree node of order } p = p - 1$.
13. $	ext{Min Keys in non-root B-Tree node of order } p = \lceil p/2 ceil - 1$.
14. $TAT = CT - AT$.
15. $WT = TAT - BT$.
16. $	ext{Chebyshev: } P(|X-\mu| \ge k\sigma) \le rac{1}{k^2}$.
17. $	ext{Variance: } 	ext{Var}(X) = E[X^2] - (E[X])^2$.
18. $	ext{Poisson: } P(X=k) = rac{\lambda^k e^{-\lambda}}{k!}$.
19. $	ext{Exponential: } P(X \le x) = 1 - e^{-\lambda x}$.
20. $	ext{Trace}(A) = \sum \lambda_i = \sum A_{ii}$.
21. $\det(A) = \prod \lambda_i$.
22. $	ext{Rank}(A) + 	ext{Nullity}(A) = n$.
23. $A^*$ heuristic admissibility: $0 \le h(n) \le h^*(n)$.
24. $A^*$ heuristic consistency: $h(n) \le c(n, a, n') + h(n')$.
25. $	ext{Alpha-Beta best case time: } O(b^{d/2})$.
26. $	ext{K-Means WCSS: } J = \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$.
27. $	ext{Bayesian Joint Factorization: } P(X_1 \dots X_n) = \prod P(X_i \mid 	ext{Parents}(X_i))$.
28. $	ext{Number of states in minimal DFA for string ending in pattern of length } k = k + 1$.
29. $	ext{Arden's Theorem: } R = Q + RP \implies R = QP^*$.
30. $	ext{Hamming Distance for detecting } d 	ext{ errors: } d + 1$; for correcting $d$ errors: $2d + 1$.

---

## 14. Quick Cheat Sheet

- **Language Hierarchy:** Regular $\subset$ DCFL $\subset$ CFL $\subset$ CSL $\subset$ REC $\subset$ RE.
- **Scheduling:** SJF/SRTF gives minimal average waiting time.
- **Virtual Memory:** LRU and Optimal are stack algorithms (no Belady's anomaly). FIFO has Belady's anomaly.
- **Relational:** BCNF removes all functional redundancy. 3NF allows prime attribute on right side.
- **TCP:** Congestion window doubles each RTT during Slow Start; increases by 1 MSS each RTT during Congestion Avoidance.

---

## 15. Final Exam Day Checklist

- [ ] Check units for every network calculation (bits vs bytes, ms vs seconds).
- [ ] Review Master Theorem conditions ($a \ge 1, b > 1$).
- [ ] Verify eigenvalues sum = trace, product = determinant on scratch sheet.
- [ ] For LR parsing, verify whether question specifies LR(0), SLR(1), LALR(1), or CLR(1).
- [ ] For pipelining speedup, verify if operand forwarding is enabled.
- [ ] For virtual memory, verify single-level vs multi-level page table access count.
