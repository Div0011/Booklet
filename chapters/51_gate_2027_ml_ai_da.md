# 51. GATE 2027: Machine Learning & Artificial Intelligence for Data Science (DA)

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Core Concepts](#2-core-concepts)
  - [2.1 Beginner Level (Unsupervised Clustering & Search Fundamentals)](#21-beginner-level)
  - [2.2 Intermediate Level (Dimensionality Reduction & Adversarial Game Trees)](#22-intermediate-level)
  - [2.3 Advanced Level (Probabilistic Reasoning, Bayesian Networks & NLP)](#23-advanced-level)
- [3. Internal Working](#3-internal-working)
- [4. Important Terminology](#4-important-terminology)
- [5. Beginner Examples](#5-beginner-examples)
- [6. Intermediate Examples](#6-intermediate-examples)
- [7. Advanced Examples](#7-advanced-examples)
- [8. How Interviewers Think](#8-how-interviewers-think)
- [9. FAQs (25 High-Yield GATE DA & Interview Questions)](#9-faqs)
- [10. Common Mistakes](#10-common-mistakes)
- [11. Comparison Tables](#11-comparison-tables)
- [12. Practical Projects](#12-practical-projects)
- [13. Internship Preparation](#13-internship-preparation)
- [14. Cheat Sheet](#14-cheat-sheet)
- [15. One-Day Revision Checklist](#15-one-day-revision-checklist)

---

## 1. Introduction

### What is GATE DA (Data Science & AI)?
The **GATE Data Science & Artificial Intelligence (DA)** syllabus covers foundational mathematical modeling, search strategies, knowledge representation, statistical learning, and unsupervised/supervised machine learning algorithms.

### Why it Exists & Scope
1. **Mathematical AI Rigor:** Tests core mathematical formulation of clustering (K-Means, DBSCAN, Hierarchical), matrix decompositions (PCA, SVD), and search optimality ($A^*$, Minimax, Alpha-Beta pruning).
2. **Probabilistic Reasoning:** Explores exact inference over joint distributions and Directed Acyclic Graph (DAG) structures in Bayesian Networks.

---

## 2. Core Concepts

### 2.1 Beginner Level

#### Unsupervised Learning: Clustering
- **K-Means Clustering:**
  - Objective: Minimize Within-Cluster Sum of Squares (WCSS / Inertia):
    $$J = \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$$
  - Steps: Initialize $K$ centroids $ightarrow$ Assign each point to nearest centroid $ightarrow$ Recompute centroids as cluster means $ightarrow$ Repeat until convergence.
  - Convergence: Guaranteed to reach a local minimum, not necessarily global optimum. Sensitive to initial centroid placement (mitigated by K-Means++).
- **K-Medoids:** Uses actual data points as centers (medoids); robust to outliers. Uses PAM (Partitioning Around Medoids).
- **Hierarchical Clustering:**
  - Agglomerative (bottom-up) vs Divisive (top-down).
  - Linkage criteria: Single Link (minimum distance - chaining effect), Complete Link (maximum distance - compact spheres), Average Link, Ward's Method (minimizes variance increase).
- **DBSCAN (Density-Based Spatial Clustering of Applications with Noise):**
  - Parameters: $\epsilon$ (radius) and $MinPts$ (minimum points in $\epsilon$-neighborhood).
  - Point types: Core Point ($|N_\epsilon(p)| \ge MinPts$), Border Point ($|N_\epsilon(p)| < MinPts$ but in neighborhood of core point), Noise Point (neither).
  - Finds arbitrary-shaped clusters; robust to noise; does NOT require specifying $K$.

#### Uninformed & Informed Search Algorithms
- **Uninformed Search:**
  - **BFS:** Complete, optimal if step costs are identical. Space $O(b^d)$, Time $O(b^d)$.
  - **DFS:** Not complete in infinite spaces, not optimal. Space $O(b \cdot m)$, Time $O(b^m)$.
  - **Uniform Cost Search (UCS / Dijkstra):** Expands node with lowest path cost $g(n)$. Complete and optimal for positive step costs.
  - **Iterative Deepening DFS (IDDFS):** Combines BFS completeness/optimality with DFS linear space $O(b \cdot d)$.
- **Informed (Heuristic) Search:**
  - **Greedy Best-First Search:** Expands node with lowest heuristic $h(n)$. Not optimal, not complete.
  - **$A^*$ Search:** Expands node with lowest $f(n) = g(n) + h(n)$.
  - **Admissibility:** $0 \le h(n) \le h^*(n)$ (never overestimates true cost). Guarantees tree-search $A^*$ optimality.
  - **Consistency (Monotonicity):** $h(n) \le c(n, a, n') + h(n')$. Guarantees graph-search $A^*$ optimality without node reopening.

---

### 2.2 Intermediate Level

#### Dimensionality Reduction: PCA & SVD
- **Principal Component Analysis (PCA):**
  - Unsupervised linear dimensionality reduction maximizing variance / minimizing reconstruction error.
  - Steps: Center data ($X - \mu$) $ightarrow$ Compute sample covariance matrix $\Sigma = rac{1}{N} X^T X$ $ightarrow$ Compute eigenvalues and eigenvectors ($\Sigma v_i = \lambda_i v_i$) $ightarrow$ Sort eigenvectors by decreasing eigenvalues $ightarrow$ Project data onto top $k$ principal eigenvectors.
  - Explained Variance Ratio: $rac{\lambda_i}{\sum_j \lambda_j}$.
- **Singular Value Decomposition (SVD):**
  - Factorizes any real $m 	imes n$ matrix $A$ into:
    $$A = U \Sigma V^T$$
    where $U$ is $m 	imes m$ orthogonal (left singular vectors), $\Sigma$ is $m 	imes n$ diagonal (singular values $\sigma_1 \ge \sigma_2 \ge \dots \ge 0$), and $V^T$ is $n 	imes n$ orthogonal (right singular vectors).
  - Connection to PCA: The columns of $V$ are the principal directions of $X^T X$, and $\sigma_i = \sqrt{\lambda_i (N-1)}$.

#### Adversarial Search: Game Trees
- **Minimax Algorithm:** Optimal decision in 2-player zero-sum perfect information games. MAX node chooses $\max$, MIN node chooses $\min$. Depth $d$, branching factor $b \implies O(b^d)$ time.
- **Alpha-Beta Pruning:**
  - $lpha$: Best value that MAX can guarantee so far (initially $-\infty$).
  - $eta$: Best value that MIN can guarantee so far (initially $+\infty$).
  - Pruning condition: Prune branch if $lpha \ge eta$.
  - Best-case time complexity with perfect move ordering: $O(b^{d/2})$, doubling searchable depth!

---

### 2.3 Advanced Level

#### Knowledge Representation, Resolution & Logic
- **Propositional Resolution:** Refutation completeness. Convert to Conjunctive Normal Form (CNF) $ightarrow$ Negate goal $ightarrow$ Apply resolution rule: $rac{A \lor B, \quad 
eg B \lor C}{A \lor C} ightarrow$ Derive empty clause $\square$ (Contradiction).
- **First-Order Logic (FOL) & Unification:** Most General Unifier (MGU) replaces variables with terms to make literals identical. Skolemization eliminates existential quantifiers.

#### Probabilistic Reasoning & Bayesian Networks
- **Bayesian Network (BN):** Directed Acyclic Graph (DAG) representing conditional dependencies among random variables.
- **Joint Probability Factorization:**
  $$P(X_1, X_2, \ldots, X_n) = \prod_{i=1}^n P(X_i \mid 	ext{Parents}(X_i))$$
- **D-Separation (Conditional Independence):**
  - **Serial (Causal Chain):** $A ightarrow B ightarrow C \implies A \perp C \mid B$. (Blocked if $B$ is observed).
  - **Diverging (Common Cause):** $A \leftarrow B ightarrow C \implies A \perp C \mid B$. (Blocked if $B$ is observed).
  - **Converging (V-Structure / Collider):** $A ightarrow B \leftarrow C \implies A \perp C$ when $B$ is UNKNOWN. (Active/Unblocked if $B$ or its descendant is observed!).

---

## 3. Internal Working

### 3.1 Alpha-Beta Pruning Execution Trace
```
                    [ MAX ]  (root)
                   /                    [ MIN ]       [ MIN ]
            /       \         │
         [3]         [5]     [2] ──► (alpha=3, beta=2 => alpha >= beta => PRUNE sibling!)
```

### 3.2 D-Separation Rules in Bayesian Networks
```
 1. Chain:       A ──► [B] ──► C      => A and C are INDEPENDENT given B
 2. Fork:        A ◄── [B] ──► C      => A and C are INDEPENDENT given B
 3. Collider:    A ──►  B  ◄── C      => A and C are INDEPENDENT when B is UNKNOWN!
                 A ──► [B] ◄── C      => A and C become DEPENDENT when B is OBSERVED!
```

---

## 4. Important Terminology

- **WCSS (Within-Cluster Sum of Squares):** Sum of squared Euclidean distances between points and their assigned cluster centroid.
- **Admissible Heuristic:** Heuristic function that never overestimates the true cost to reach the nearest goal.
- **Consistent (Monotonic) Heuristic:** Heuristic satisfying the triangle inequality $h(n) \le c(n, a, n') + h(n')$.
- **Alpha-Beta Pruning:** Optimization algorithm for minimax game tree search that eliminates branches provably unable to influence the final decision.
- **D-Separation:** Graphical criterion to determine whether a set of variables $X$ is conditionally independent of $Y$ given $Z$ in a Bayesian Network.
- **Collider:** Node in a Bayesian network with two or more incoming directed edges ($A ightarrow B \leftarrow C$).
- **Singular Value Decomposition (SVD):** Matrix factorization $A = U \Sigma V^T$ providing the best low-rank approximation (Eckart-Young theorem).

---

## 5. Beginner Examples

### Example 1: K-Means Clustering Centroid Update
Given points in 1D: $X = [2, 4, 10, 12, 3, 20, 30, 11, 25]$. Initial centroids: $c_1 = 2, c_2 = 10, c_3 = 25$.
- Distance to $c_1, c_2, c_3$:
  - Point 2: assigned to $C_1$
  - Point 3: assigned to $C_1$
  - Point 4: assigned to $C_1$
  - Point 10: assigned to $C_2$
  - Point 11: assigned to $C_2$
  - Point 12: assigned to $C_2$
  - Point 20: assigned to $C_3$
  - Point 25: assigned to $C_3$
  - Point 30: assigned to $C_3$
- Updated Centroids:
  - $c_1' = rac{2+3+4}{3} = 3.0$
  - $c_2' = rac{10+11+12}{3} = 11.0$
  - $c_3' = rac{20+25+30}{3} = 25.0$

---

## 6. Intermediate Examples

### Example 1: Principal Component Analysis Step-by-Step
Given 2D centered data matrix:
$$X = egin{pmatrix} 1 & 2 \ 3 & 6 \ -1 & -2 \ -3 & -6 \end{pmatrix}$$
1. Compute Covariance Matrix $\Sigma = rac{1}{4} X^T X$:
   $$X^T X = egin{pmatrix} 1 & 3 & -1 & -3 \ 2 & 6 & -2 & -6 \end{pmatrix} egin{pmatrix} 1 & 2 \ 3 & 6 \ -1 & -2 \ -3 & -6 \end{pmatrix} = egin{pmatrix} 20 & 40 \ 40 & 80 \end{pmatrix}$$
   $$\Sigma = egin{pmatrix} 5 & 10 \ 10 & 20 \end{pmatrix}$$
2. Characteristic equation: $\det(\Sigma - \lambda I) = (5-\lambda)(20-\lambda) - 100 = \lambda^2 - 25\lambda = 0 \implies \lambda_1 = 25, \lambda_2 = 0$.
3. First Principal Direction: $(\Sigma - 25 I) v_1 = 0 \implies egin{pmatrix} -20 & 10 \ 10 & -5 \end{pmatrix} egin{pmatrix} v_{11} \ v_{12} \end{pmatrix} = 0 \implies 2 v_{11} = v_{12}$.
   Normalized unit eigenvector: $v_1 = rac{1}{\sqrt{5}} egin{pmatrix} 1 \ 2 \end{pmatrix}$.
4. Explained Variance: $rac{25}{25+0} = 100\%$. The data is completely 1-dimensional!

---

## 7. Advanced Examples

### Example 1: Bayesian Network Joint Probability Calculation
Given Network: $A ightarrow B ightarrow C$ and $A ightarrow C$.
$$P(A, B, C) = P(A) \cdot P(B \mid A) \cdot P(C \mid A, B)$$
To compute marginal $P(C=c)$:
$$P(C=c) = \sum_{a \in A} \sum_{b \in B} P(A=a) \cdot P(B=b \mid A=a) \cdot P(C=c \mid A=a, B=b)$$

---

## 8. How Interviewers Think

- **Admissibility vs Consistency:** Remember: Consistency $\implies$ Admissibility, but Admissibility $
ot\implies$ Consistency. For graph search without reopening, consistency is required.
- **Collider Behavior in BNs:** Interviewers test the "Explaining Away" effect: two independent causes become conditionally DEPENDENT given their common effect.
- **K-Means Outlier Sensitivity:** K-Means squares distances, making it highly sensitive to extreme outliers; K-Medoids or DBSCAN should be chosen when noise is prevalent.

---

## 9. FAQs (25 High-Yield GATE DA & Interview Questions)

### Q1: Why does DBSCAN not require the number of clusters $K$ in advance?
**Answer:** DBSCAN discovers clusters as connected components of high-density core points separated by regions of low density. It constructs clusters dynamically based solely on the local radius $\epsilon$ and density threshold $MinPts$.

### Q2: What is the relationship between SVD and PCA?
**Answer:** For a centered data matrix $X$, the right singular vectors $V$ from SVD ($X = U \Sigma V^T$) are exactly the eigenvectors of the sample covariance matrix $X^T X$, and the singular values $\sigma_i$ are related to the eigenvalues by $\lambda_i = rac{\sigma_i^2}{N-1}$.

### Q3: What is the condition for Alpha-Beta pruning to achieve maximum efficiency?
**Answer:** When moves are evaluated in perfect order (best moves searched first), Alpha-Beta pruning reduces the effective branching factor from $b$ to $\sqrt{b}$, cutting time complexity to $O(b^{d/2})$.

---

## 10. Common Mistakes

| Anti-Pattern | Why It Is Wrong | Correct Approach |
| :--- | :--- | :--- |
| Applying PCA without mean centering | Data spread will be measured from arbitrary origin $(0,0)$ rather than data centroid | Always center the dataset ($X - ar{X}$) before computing covariance matrix |
| Assuming non-core points in DBSCAN cannot form clusters | Border points belong to clusters, but they cannot expand clusters | Only Core Points ($|N_\epsilon| \ge MinPts$) expand cluster neighborhoods |

---

## 11. Comparison Tables

### Search Algorithms Comparison
| Algorithm | Complete? | Optimal? | Time Complexity | Space Complexity |
| :--- | :--- | :--- | :--- | :--- |
| **BFS** | Yes | Yes (if uniform cost) | $O(b^d)$ | $O(b^d)$ |
| **DFS** | No (in infinite paths) | No | $O(b^m)$ | $O(b \cdot m)$ |
| **Uniform Cost (UCS)**| Yes | Yes | $O(b^{1 + \lfloor C^*/\epsilon floor})$ | $O(b^{1 + \lfloor C^*/\epsilon floor})$ |
| **$A^*$ (Tree)** | Yes | Yes (if Admissible) | $O(b^d)$ | $O(b^d)$ |
| **$A^*$ (Graph)**| Yes | Yes (if Consistent) | $O(b^d)$ | $O(b^d)$ |

---

## 12. Practical Projects

### Project: Complete K-Means Clustering Implementation from Scratch
```python
import numpy as np

class KMeansScratch:
    def __init__(self, k=3, max_iters=100, tol=1e-4):
        self.k = k
        self.max_iters = max_iters
        self.tol = tol
        self.centroids = None

    def fit(self, X):
        np.random.seed(42)
        # Initialize centroids randomly from data points
        indices = np.random.choice(len(X), self.k, replace=False)
        self.centroids = X[indices].copy()

        for iteration in range(self.max_iters):
            # Compute Euclidean distances to all centroids
            distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
            labels = np.argmin(distances, axis=1)

            # Recompute centroids
            new_centroids = np.array([X[labels == j].mean(axis=0) if len(X[labels == j]) > 0
                                      else self.centroids[j] for j in range(self.k)])

            if np.all(np.abs(new_centroids - self.centroids) < self.tol):
                break
            self.centroids = new_centroids

        return self

    def predict(self, X):
        distances = np.linalg.norm(X[:, np.newaxis] - self.centroids, axis=2)
        return np.argmin(distances, axis=1)

# Test run
X = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])
km = KMeansScratch(k=2).fit(X)
print("Converged Centroids:\n", km.centroids)
print("Cluster Assignments:", km.predict(X))
```

---

## 13. Internship Preparation

1. Implement PCA and K-Means from scratch using NumPy.
2. Be able to trace Alpha-Beta pruning on arbitrary game trees by hand.
3. Master D-separation path checking across chains, forks, and colliders.
4. Understand Singular Value Decomposition rank-$k$ matrix approximation.
5. Review evaluation metrics for classification (ROC-AUC, Precision-Recall) and clustering (Silhouette score).

---

## 14. Cheat Sheet

- **WCSS Objective:** $J = \sum_{k=1}^K \sum_{x \in C_k} \|x - \mu_k\|^2$.
- **$A^*$ Optimality Condition:** $h(n) \le h^*(n)$ (Admissible) for tree search; $h(n) \le c(n, a, n') + h(n')$ (Consistent) for graph search.
- **Covariance Matrix:** $\Sigma = rac{1}{N} X^T X$ (for zero-mean data $X$).
- **SVD Decomposition:** $A = U \Sigma V^T$.
- **Bayesian Factorization:** $P(X_1, \dots, X_n) = \prod_{i=1}^n P(X_i \mid 	ext{Parents}(X_i))$.

---

## 15. One-Day Revision Checklist

- [ ] Execute 1 iteration of K-Means clustering centroid update.
- [ ] Review DBSCAN Core, Border, and Noise classification rules.
- [ ] Trace an Alpha-Beta pruning game tree and label pruned subtrees.
- [ ] Review D-separation rules (Chain, Fork, Collider).
- [ ] Check PCA eigenvalue covariance calculation formula.
- [ ] Review $A^*$ admissibility vs consistency definitions.
