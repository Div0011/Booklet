# 44. GATE 2027 Engineering Mathematics (CS & DA Syllabi)

## 1. Introduction

### What it is
Engineering Mathematics for GATE 2027 encompasses the mathematical foundations required for Computer Science (CS) and Data Analytics (DA) disciplines. This chapter unifies **Discrete Mathematics**, **Linear Algebra**, **Calculus**, and **Probability & Statistics**—the four pillars tested in GATE. The CS syllabus emphasizes logic, algebraic structures, and graph theory, while the DA syllabus extends into statistical inference, hypothesis testing, and multivariate distributions. Mastery of these topics is essential: they constitute approximately 15 marks in GATE CS and form the backbone of DA paper sections.

### Why it exists
Mathematical maturity distinguishes exceptional engineers from average ones. GATE tests engineering mathematics because algorithms, machine learning, cryptography, and system design all rest on these foundations. Linear algebra powers neural networks and graph algorithms; probability enables Bayesian reasoning and statistical learning; discrete mathematics underpins database theory and formal verification; calculus drives optimization and numerical methods. Without rigorous mathematical training, candidates cannot analyze algorithm correctness, prove system properties, or derive statistical guarantees.

### Problems it solves
- **Algorithm Analysis**: Recurrence relations and asymptotic notation determine whether an algorithm scales.
- **Machine Learning Theory**: Gradient descent, SVMs, and PCA require linear algebra and multivariate calculus.
- **Probabilistic Reasoning**: Bayesian networks, HMMs, and randomized algorithms demand probability fluency.
- **System Verification**: Formal logic and proof techniques verify hardware and protocol correctness.
- **Statistical Inference**: Hypothesis testing and confidence intervals validate experimental results in data science.
- **Optimization**: Calculus-based methods find optimal solutions in operations research and ML.

### Industry Use Cases
- **Tech Interviews**: FAANG companies test DSA (discrete math) and probability puzzles routinely.
- **Machine Learning Engineering**: Backpropagation (calculus), SVD/PCA (linear algebra), loss functions (optimization).
- **Quantitative Finance**: Stochastic calculus, portfolio optimization (quadratic forms), risk modeling (distributions).
- **Cryptography**: Group theory (Elliptic Curve Cryptography), number theory (RSA), finite fields.
- **Database Systems**: Relational algebra (set theory), query optimization (combinatorics).
- **Computer Graphics**: Matrix transformations, projections (linear algebra), ray tracing (calculus).

### Analogy
Engineering mathematics is the grammar of computing. Just as grammar gives structure to language, mathematics gives rigor to code. Discrete math is the syntax (rules of logic), linear algebra is the vocabulary (vectors and spaces), calculus is the semantics (change and meaning), and probability is the pragmatics (handling ambiguity). A programmer without math is like a writer without grammar—functional but limited in expressing complex ideas.

---

## 2. Core Concepts

### Beginner Concepts

#### Propositional Logic
Propositional logic deals with declarative sentences that are either true (T) or false (F).

- **Logical Connectives**:
  - Negation ($\neg p$): "Not p"
  - Conjunction ($p \land q$): "p and q"
  - Disjunction ($p \lor q$): "p or q" (inclusive)
  - Implication ($p \to q$): "If p then q" (false only when p=T, q=F)
  - Biconditional ($p \leftrightarrow q$): "p if and only if q"

- **Truth Tables**: Enumerate all $2^n$ assignments for $n$ propositional variables.

- **Tautology**: Always true (e.g., $p \lor \neg p$).
- **Contradiction**: Always false (e.g., $p \land \neg p$).
- **Contingency**: Neither tautology nor contradiction.

- **Logical Equivalences**:
  - De Morgan's Laws: $\neg(p \land q) \equiv \neg p \lor \neg q$, $\neg(p \lor q) \equiv \neg p \land \neg q$
  - Distributive: $p \land (q \lor r) \equiv (p \land q) \lor (p \land r)$
  - Implication: $p \to q \equiv \neg p \lor q$
  - Contrapositive: $p \to q \equiv \neg q \to \neg p$

- **Normal Forms**:
  - **CNF (Conjunctive Normal Form)**: Conjunction of clauses (disjunctions of literals). $(p \lor q) \land (\neg p \lor r)$
  - **DNF (Disjunctive Normal Form)**: Disjunction of terms (conjunctions of literals). $(p \land q) \lor (\neg p \land r)$

#### First-Order Logic (Predicate Logic)
Extends propositional logic with quantifiers and predicates.

- **Predicates**: $P(x)$: "x is prime" — truth value depends on x.
- **Quantifiers**:
  - Universal ($\forall x$): "For all x"
  - Existential ($\exists x$): "There exists x"
- **Negation Rules**:
  - $\neg(\forall x \, P(x)) \equiv \exists x \, \neg P(x)$
  - $\neg(\exists x \, P(x)) \equiv \forall x \, \neg P(x)$
- **Nested Quantifiers**: Order matters. $\forall x \exists y \, P(x,y) \not\equiv \exists y \forall x \, P(x,y)$
- **Validity**: A formula is valid if true in all interpretations; satisfiable if true in at least one.

#### Sets, Relations, and Functions

- **Sets**: Unordered collections. Operations: union ($\cup$), intersection ($\cap$), complement ($A'$), difference ($-$), symmetric difference ($\Delta$).
  - $|A \cup B| = |A| + |B| - |A \cap B|$ (Inclusion-Exclusion)
  - Power set $\mathcal{P}(A)$: Set of all subsets; $|\mathcal{P}(A)| = 2^{|A|}$
  - Cartesian product: $A \times B = \{(a,b) : a \in A, b \in B\}$

- **Relations**: Subset of $A \times B$. Properties:
  - Reflexive: $(a,a) \in R$ for all $a$
  - Symmetric: $(a,b) \in R \to (b,a) \in R$
  - Antisymmetric: $(a,b), (b,a) \in R \to a = b$
  - Transitive: $(a,b), (b,c) \in R \to (a,c) \in R$

- **Equivalence Relation**: Reflexive + Symmetric + Transitive. Partitions set into equivalence classes.
- **Partial Order**: Reflexive + Antisymmetric + Transitive. Denoted $(S, \le)$.
  - **Poset**: Partially ordered set.
  - **Chain**: Totally ordered subset.
  - **Hasse Diagram**: Visual representation of poset (omit reflexive and transitive edges).
  - **Maximal/Greatest Element**: No element greater than it / greater than all elements.
  - **Lattice**: Poset where every pair has a least upper bound (join, $\vee$) and greatest lower bound (meet, $\wedge$).

- **Functions**: $f: A \to B$ is a relation where each $a \in A$ maps to exactly one $b \in B$.
  - **Injective (One-to-One)**: $f(a_1) = f(a_2) \to a_1 = a_2$
  - **Surjective (Onto)**: For every $b \in B$, exists $a \in A$ with $f(a) = b$
  - **Bijective**: Both injective and surjective (invertible)
  - **Composition**: $(f \circ g)(x) = f(g(x))$
  - **Inverse**: $f^{-1}(f(x)) = x$ (exists iff bijective)

#### Groups and Algebraic Structures

- **Group** $(G, \cdot)$: Set with binary operation satisfying:
  1. **Closure**: $a, b \in G \to a \cdot b \in G$
  2. **Associativity**: $(a \cdot b) \cdot c = a \cdot (b \cdot c)$
  3. **Identity**: $\exists e \in G : a \cdot e = e \cdot a = a$
  4. **Inverse**: $\forall a \in G, \exists a^{-1} : a \cdot a^{-1} = e$

- **Abelian Group**: Commutative: $a \cdot b = b \cdot a$
- **Monoid**: Group without inverse requirement (associativity + identity).
- **Semi-group**: Closure + associativity only (no identity).
- **Ring**: Abelian group under addition, monoid under multiplication, with distributivity.
- **Field**: Ring where non-zero elements form an abelian group under multiplication ($\mathbb{Q}$, $\mathbb{R}$, $\mathbb{Z}_p$ for prime $p$).

- **Subgroup Test**: $H \subseteq G$ is subgroup iff $a, b \in H \to ab^{-1} \in H$.
- **Order of Element**: Smallest $n > 0$ such that $a^n = e$. If no such $n$, order is infinite.
- **Lagrange's Theorem**: For finite group $G$ and subgroup $H$, $|H|$ divides $|G|$.
- **Cyclic Group**: Generated by single element: $G = \langle a \rangle = \{a^n : n \in \mathbb{Z}\}$.

#### Graph Theory Basics

- **Graph** $G = (V, E)$: Vertices $V$, Edges $E \subseteq V \times V$.
  - **Undirected**: Edges are unordered pairs.
  - **Directed (Digraph)**: Edges are ordered pairs.
  - **Weighted**: Edges have numerical labels.
  - **Simple**: No loops or multiple edges.

- **Key Terms**:
  - **Degree** $\deg(v)$: Number of edges incident to $v$.
  - **Handshaking Lemma**: $\sum_{v \in V} \deg(v) = 2|E|$.
  - **Walk/Trail/Path/Cycle**: Sequence of vertices; trail has no repeated edges; path has no repeated vertices; cycle is closed path.

- **Connectivity**:
  - **Connected**: Path between every pair of vertices.
  - **Connected Component**: Maximal connected subgraph.
  - **Cut Vertex (Articulation Point)**: Removal disconnects the graph.
  - **Bridge**: Edge whose removal disconnects the graph.
  - **Biconnected**: No articulation points.

- **Special Graphs**:
  - **Complete** $K_n$: All pairs adjacent; $|E| = \binom{n}{2}$.
  - **Bipartite**: Vertices partitionable into $V_1, V_2$ with edges only between sets.
  - **Complete Bipartite** $K_{m,n}$: Every vertex in $V_1$ adjacent to every vertex in $V_2$.
  - **Regular**: All vertices have same degree.

- **Planar Graphs**: Can be drawn without edge crossings.
  - **Euler's Formula**: $V - E + F = 2$ (for connected planar graph).
  - **Kuratowski's Theorem**: Planar iff no subgraph homeomorphic to $K_5$ or $K_{3,3}$.
  - **Maximum Edges**: $E \le 3V - 6$ (for $V \ge 3$).

#### Combinatorics: Counting Principles

- **Sum Rule**: If tasks $A$ and $B$ are mutually exclusive, ways = $|A| + |B|$.
- **Product Rule**: If task 1 has $m$ ways and task 2 has $n$ ways, combined = $m \cdot n$.
- **Permutations**: Arrangements of $r$ from $n$ distinct items: $P(n,r) = \frac{n!}{(n-r)!}$.
- **Combinations**: Selections of $r$ from $n$: $\binom{n}{r} = \frac{n!}{r!(n-r)!}$.
- **Circular Permutations**: $(n-1)!$ arrangements around a circle.

- **Binomial Theorem**:
$$(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$$

- **Multinomial Coefficient**: Ways to divide $n$ items into groups of sizes $n_1, n_2, \ldots, n_k$:
$$\binom{n}{n_1, n_2, \ldots, n_k} = \frac{n!}{n_1! \, n_2! \, \cdots \, n_k!}$$

- **Inclusion-Exclusion**:
$$|A_1 \cup A_2 \cup \cdots \cup A_n| = \sum_{i} |A_i| - \sum_{i<j} |A_i \cap A_j| + \sum_{i<j<k} |A_i \cap A_j \cap A_k| - \cdots + (-1)^{n+1}|A_1 \cap \cdots \cap A_n|$$

- **Pigeonhole Principle**: If $n$ items placed in $m$ containers with $n > m$, at least one container has $\lceil n/m \rceil$ items.

### Intermediate Concepts

#### Recurrence Relations

A recurrence relation expresses $a_n$ in terms of previous terms $a_{n-1}, a_{n-2}, \ldots$.

- **Linear Recurrence with Constant Coefficients**:
$$a_n = c_1 a_{n-1} + c_2 a_{n-2} + \cdots + c_k a_{n-k} + f(n)$$

- **Homogeneous**: $f(n) = 0$.
- **Characteristic Equation**: $r^k - c_1 r^{k-1} - \cdots - c_k = 0$.
  - **Distinct Roots** $r_1, \ldots, r_k$: $a_n = \alpha_1 r_1^n + \cdots + \alpha_k r_k^n$.
  - **Repeated Root** $r$ with multiplicity $m$: $(A_0 + A_1 n + \cdots + A_{m-1} n^{m-1}) r^n$.

- **Non-homogeneous**: Particular solution depends on form of $f(n)$.
  - $f(n) = d \cdot r^n$: Try $A \cdot r^n$ (if $r$ not a root) or $A \cdot n^m r^n$ (if $r$ is root with multiplicity $m$).
  - $f(n) = \text{polynomial}$: Try polynomial of same degree.

- **Master Theorem** (for divide-and-conquer):
$$T(n) = aT\left(\frac{n}{b}\right) + f(n)$$
Compare $f(n)$ with $n^{\log_b a}$:
  - **Case 1**: $f(n) = O(n^c)$, $c < \log_b a \implies T(n) = \Theta(n^{\log_b a})$.
  - **Case 2**: $f(n) = \Theta(n^{\log_b a} \log^k n) \implies T(n) = \Theta(n^{\log_b a} \log^{k+1} n)$.
  - **Case 3**: $f(n) = \Omega(n^c)$, $c > \log_b a$, with regularity condition $\implies T(n) = \Theta(f(n))$.

- **Substitution Method**: Guess the bound, prove by induction.
- **Recursion Tree Method**: Sum costs at each level.

#### Generating Functions

A generating function encodes a sequence $\{a_n\}$ as a power series.

- **Ordinary Generating Function (OGF)**:
$$A(x) = \sum_{n=0}^{\infty} a_n x^n$$

- **Exponential Generating Function (EGF)**:
$$A(x) = \sum_{n=0}^{\infty} a_n \frac{x^n}{n!}$$

- **Common OGFs**:
  - $a_n = 1$: $\frac{1}{1-x}$
  - $a_n = r^n$: $\frac{1}{1-rx}$
  - $a_n = \binom{n+k-1}{k-1}$: $\frac{1}{(1-x)^k}$ (stars and bars)
  - Fibonacci: $\frac{x}{1-x-x^2}$

- **Operations**:
  - Addition: $\{a_n\} + \{b_n\} \to A(x) + B(x)$
  - Convolution: $\{a_n\} \cdot \{b_n\} \to A(x) \cdot B(x)$
  - Shift: $\{a_{n-k}\} \to x^k A(x)$

- **Solving Recurrences**: Multiply recurrence by $x^n$, sum over $n$, solve for $A(x)$, extract coefficient.

#### Graph: Matching and Coloring

- **Matching**: Set of edges without common vertices.
  - **Perfect Matching**: Covers all vertices (requires even $|V|$).
  - **Maximum Matching**: Largest possible matching.
  - **Bipartite Matching**: Matching in bipartite graphs.
  - **Hall's Marriage Theorem**: Bipartite graph $G = (X \cup Y, E)$ has matching covering $X$ iff for all $S \subseteq X$, $|N(S)| \ge |S|$.

- **Vertex Coloring**: Assign colors to vertices so adjacent vertices differ.
  - **Chromatic Number** $\chi(G)$: Minimum colors needed.
  - **Bounds**: $\omega(G) \le \chi(G) \le \Delta(G) + 1$ (where $\omega$ is clique number, $\Delta$ is max degree).
  - **Brooks' Theorem**: $\chi(G) \le \Delta(G)$ for connected graphs that aren't complete or odd cycles.
  - **Bipartite Graphs**: $\chi(G) = 2$ (iff no odd cycle).

- **Edge Coloring**: $\chi'(G)$: Minimum colors for edges.
  - **Vizing's Theorem**: $\Delta(G) \le \chi'(G) \le \Delta(G) + 1$.
  - **König's Theorem**: For bipartite graphs, $\chi'(G) = \Delta(G)$.

#### Linear Algebra: Matrices and Determinants

- **Matrix Operations**:
  - Addition, scalar multiplication, matrix multiplication.
  - **Transpose** $A^T$: $(A^T)_{ij} = A_{ji}$.
  - **Trace**: $\text{tr}(A) = \sum_i A_{ii}$.
  - **Conjugate Transpose** $A^*$: $(A^*)_{ij} = \overline{A_{ji}}$.

- **Special Matrices**:
  - **Symmetric**: $A = A^T$.
  - **Skew-symmetric**: $A = -A^T$ (diagonal entries zero).
  - **Orthogonal**: $A^T A = I$ (columns orthonormal).
  - **Hermitian**: $A = A^*$.
  - **Unitary**: $A^* A = I$.
  - **Idempotent**: $A^2 = A$.
  - **Involutory**: $A^2 = I$.
  - **Nilpotent**: $A^k = 0$ for some $k$.

- **Determinant**: Scalar value defined recursively.
  - $\det(A) = \sum_{j=1}^{n} (-1)^{i+j} a_{ij} \det(M_{ij})$ (cofactor expansion along row $i$).
  - **Properties**:
    - $\det(AB) = \det(A)\det(B)$
    - $\det(A^T) = \det(A)$
    - $\det(cA) = c^n \det(A)$
    - Row operations: swap multiplies by $-1$; scale multiplies by $c$; adding multiple of row to another leaves unchanged.
    - $\det(A^{-1}) = 1/\det(A)$ (if invertible).
  - **Cramer's Rule**: For $Ax = b$, $x_i = \det(A_i)/\det(A)$ where $A_i$ replaces column $i$ with $b$.

- **Inverse**:
  - $A^{-1} = \frac{1}{\det(A)} \text{adj}(A)$, where $\text{adj}(A)$ is adjugate (transpose of cofactor matrix).
  - **Gauss-Jordan**: Row reduce $[A | I] \to [I | A^{-1}]$.

#### Systems of Linear Equations

- **Form**: $Ax = b$ where $A$ is $m \times n$, $x$ is $n \times 1$, $b$ is $m \times 1$.

- **Consistency**: System is consistent iff $\text{rank}(A) = \text{rank}([A|b])$.

- **Solutions**:
  - **Unique**: $\text{rank}(A) = \text{rank}([A|b]) = n$ (full column rank).
  - **Infinite**: $\text{rank}(A) = \text{rank}([A|b]) < n$ (free variables = $n - \text{rank}$).
  - **No Solution**: $\text{rank}(A) < \text{rank}([A|b])$.

- **Gaussian Elimination**: Row reduce augmented matrix to row echelon form (REF) or reduced row echelon form (RREF).
  - **Pivot**: First non-zero entry in a row.
  - **REF**: All entries below pivots are zero; each pivot is right of the one above.
  - **RREF**: Pivots are 1; all other entries in pivot column are zero.

- **Homogeneous Systems** ($b = 0$):
  - Always consistent (trivial solution $x = 0$).
  - Non-trivial solutions iff $\text{rank}(A) < n$.

#### Eigenvalues and Eigenvectors

- **Definition**: For square matrix $A$, if $Av = \lambda v$ for non-zero vector $v$, then $\lambda$ is eigenvalue, $v$ is eigenvector.

- **Characteristic Polynomial**:
$$p(\lambda) = \det(A - \lambda I) = 0$$

- **Finding Eigenvalues**: Solve $\det(A - \lambda I) = 0$.
- **Finding Eigenvectors**: For each $\lambda$, solve $(A - \lambda I)v = 0$.

- **Properties**:
  - Sum of eigenvalues = trace: $\sum \lambda_i = \sum a_{ii}$
  - Product of eigenvalues = determinant: $\prod \lambda_i = \det(A)$
  - Eigenvalues of $A^{-1}$ are $1/\lambda_i$.
  - Eigenvalues of $A^k$ are $\lambda_i^k$.
  - Eigenvalues of $A + cI$ are $\lambda_i + c$.
  - Similar matrices have same eigenvalues.

- **Diagonalization**: $A = PDP^{-1}$ where $D$ is diagonal of eigenvalues, $P$ has eigenvectors as columns.
  - **Diagonalizable** iff $A$ has $n$ linearly independent eigenvectors.
  - **Symmetric matrices** are always diagonalizable with orthogonal eigenvectors (Spectral Theorem).

- **Cayley-Hamilton Theorem**: Every matrix satisfies its own characteristic equation. $p(A) = 0$.

#### Calculus: Limits and Continuity

- **Limit**: $\lim_{x \to a} f(x) = L$ if for every $\epsilon > 0$, exists $\delta > 0$ such that $0 < |x - a| < \delta \implies |f(x) - L| < \epsilon$.

- **One-sided Limits**: $\lim_{x \to a^-}$ (left), $\lim_{x \to a^+}$ (right). Two-sided limit exists iff both one-sided exist and are equal.

- **Limit Laws**: Sum, product, quotient (if denominator limit $\ne 0$), squeeze theorem.

- **L'Hôpital's Rule**: If $\lim f(x)/g(x)$ is $0/0$ or $\infty/\infty$, then $\lim f(x)/g(x) = \lim f'(x)/g'(x)$ (if latter exists).

- **Continuity at $a$**: $\lim_{x \to a} f(x) = f(a)$.
  - Requires: (1) $f(a)$ defined, (2) $\lim_{x \to a} f(x)$ exists, (3) limit equals value.
  - **Continuous on interval**: Continuous at every point in interval.
  - **Intermediate Value Theorem**: If $f$ continuous on $[a,b]$ and $k$ between $f(a)$ and $f(b)$, exists $c \in (a,b)$ with $f(c) = k$.

#### Calculus: Differentiation

- **Derivative**: $f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}$.

- **Differentiability implies continuity** (converse false).

- **Rules**:
  - Product: $(fg)' = f'g + fg'$
  - Quotient: $(f/g)' = (f'g - fg')/g^2$
  - Chain: $(f(g(x)))' = f'(g(x)) \cdot g'(x)$

- **Rolle's Theorem**: If $f$ continuous on $[a,b]$, differentiable on $(a,b)$, and $f(a) = f(b)$, then exists $c \in (a,b)$ with $f'(c) = 0$.

- **Mean Value Theorem (MVT)**: If $f$ continuous on $[a,b]$ and differentiable on $(a,b)$, then exists $c \in (a,b)$ with:
$$f'(c) = \frac{f(b) - f(a)}{b - a}$$

- **Taylor's Theorem**: If $f$ has $n+1$ continuous derivatives near $a$:
$$f(x) = \sum_{k=0}^{n} \frac{f^{(k)}(a)}{k!}(x-a)^k + R_n(x)$$
where $R_n(x) = \frac{f^{(n+1)}(\xi)}{(n+1)!}(x-a)^{n+1}$ (Lagrange form of remainder).

- **Maxima and Minima**:
  - **Critical Points**: Where $f'(x) = 0$ or undefined.
  - **Second Derivative Test**: $f''(x_0) > 0 \implies$ local min; $f''(x_0) < 0 \implies$ local max; $f''(x_0) = 0 \implies$ inconclusive.
  - **First Derivative Test**: Sign change of $f'$ around critical point.

- **Integration**:
  - **Indefinite**: $\int f(x)\,dx = F(x) + C$ where $F' = f$.
  - **Definite**: $\int_a^b f(x)\,dx = F(b) - F(a)$ (Fundamental Theorem of Calculus).
  - **Techniques**: Substitution, integration by parts ($\int u\,dv = uv - \int v\,du$), partial fractions.
  - **Improper Integrals**: Limits of integration or integrand unbounded.

### Advanced Concepts

#### Vector Spaces and Subspaces

- **Vector Space** $(\mathbb{V}, +, \cdot)$ over field $\mathbb{F}$: Set with vector addition and scalar multiplication satisfying 8 axioms (associativity, commutativity, identity, inverse for addition; associativity, identity for multiplication; distributivity).

- **Subspace**: Non-empty subset $W \subseteq \mathbb{V}$ closed under addition and scalar multiplication.
  - **Test**: $\forall u, v \in W, \forall c \in \mathbb{F}: u + v \in W$ and $cu \in W$.

- **Span**: $\text{span}(S) = \{\sum c_i v_i : v_i \in S, c_i \in \mathbb{F}\}$ — smallest subspace containing $S$.
- **Linear Independence**: Vectors $\{v_1, \ldots, v_n\}$ are linearly independent iff $\sum c_i v_i = 0$ implies all $c_i = 0$.
- **Basis**: Linearly independent spanning set. Every basis has same cardinality.
- **Dimension**: $\dim(\mathbb{V})$ = size of any basis.

- **Rank-Nullity Theorem**: For linear transformation $T: \mathbb{V} \to \mathbb{W}$:
$$\dim(\text{ker}(T)) + \dim(\text{im}(T)) = \dim(\mathbb{V})$$
For matrix $A$: $\text{nullity}(A) + \text{rank}(A) = n$ (number of columns).

- **Row Space, Column Space, Null Space**:
  - $\text{Col}(A)$: Span of columns; $\dim = \text{rank}(A)$.
  - $\text{Row}(A)$: Span of rows; $\dim = \text{rank}(A)$.
  - $\text{Null}(A) = \{x : Ax = 0\}$; dimension = $n - \text{rank}(A)$.
  - $\text{Col}(A)^\perp = \text{Null}(A^T)$ (fundamental theorem of linear algebra).

#### Matrix Decompositions

- **LU Decomposition**: $A = LU$ where $L$ is lower triangular, $U$ is upper triangular.
  - **Purpose**: Solve $Ax = b$ efficiently by forward/back substitution.
  - **Existence**: If no row exchanges needed during Gaussian elimination.
  - **With Pivoting**: $PA = LU$ (permutation matrix $P$).
  - **Complexity**: $O(n^3)$ for decomposition, $O(n^2)$ per right-hand side.

- **QR Decomposition**: $A = QR$ where $Q$ is orthogonal, $R$ is upper triangular.
  - **Gram-Schmidt**: Columns of $Q$ are orthonormal basis for column space.
  - **Applications**: Least squares, eigenvalue algorithms.

- **Singular Value Decomposition (SVD)**:
$$A = U \Sigma V^T$$
  - $U$: $m \times m$ orthogonal (left singular vectors)
  - $\Sigma$: $m \times n$ diagonal with singular values $\sigma_1 \ge \sigma_2 \ge \cdots \ge 0$
  - $V$: $n \times n$ orthogonal (right singular vectors)
  - **Relation to Eigendecomposition**: Columns of $U$ are eigenvectors of $AA^T$; columns of $V$ are eigenvectors of $A^T A$; singular values are $\sqrt{\lambda_i(AA^T)}$.
  - **Properties**: $\text{rank}(A)$ = number of non-zero singular values.
  - **Applications**: PCA, low-rank approximation, pseudoinverse, image compression.

- **Eigendecomposition** (Symmetric matrices): $A = Q \Lambda Q^T$ where $Q$ orthogonal, $\Lambda$ diagonal.

- **Cholesky Decomposition**: For positive definite $A$, $A = LL^T$ where $L$ is lower triangular with positive diagonal entries.

#### Quadratic Forms

- **Quadratic Form**: $Q(x) = x^T A x$ where $A$ is symmetric.

- **Classification** (based on eigenvalues $\lambda_i$):
  - **Positive Definite**: All $\lambda_i > 0$; $Q(x) > 0$ for all $x \ne 0$.
  - **Positive Semi-definite**: All $\lambda_i \ge 0$.
  - **Negative Definite**: All $\lambda_i < 0$.
  - **Indefinite**: Mix of positive and negative eigenvalues.

- **Sylvester's Criterion**: $A$ is positive definite iff all leading principal minors are positive.

- **Applications**: Optimization (Hessian matrix determines nature of critical point), covariance matrices.

#### Projections and Special Matrices

- **Projection Matrix**: $P$ satisfying $P^2 = P$ (idempotent). Projects onto $\text{Col}(P)$ along $\text{Null}(P)$.
  - **Orthogonal Projection** onto subspace with orthonormal basis $\{u_1, \ldots, u_k\}$:
$$P = \sum_{i=1}^{k} u_i u_i^T = U(U^T U)^{-1} U^T$$
  - Properties: $P = P^T$ (symmetric), eigenvalues are 0 or 1.

- **Idempotent Matrix**: $A^2 = A$. Eigenvalues are 0 or 1. $\text{tr}(A) = \text{rank}(A)$.

- **Partitioned Matrices**:
$$\begin{pmatrix} A & B \\ C & D \end{pmatrix}$$
  - Block inversion formula when $A$ invertible.
  - Schur complement: $D - CA^{-1}B$.

#### Probability: Foundations

- **Sample Space** $\Omega$: Set of all possible outcomes.
- **Event**: Subset of $\Omega$.
- **Probability Measure** $P$ satisfying Kolmogorov axioms:
  1. $P(E) \ge 0$ for all events $E$.
  2. $P(\Omega) = 1$.
  3. For mutually exclusive $E_1, E_2, \ldots$: $P(\bigcup_i E_i) = \sum_i P(E_i)$ (countable additivity).

- **Properties**:
  - $P(E^c) = 1 - P(E)$
  - $P(\emptyset) = 0$
  - If $E \subseteq F$, then $P(E) \le P(F)$
  - $P(E \cup F) = P(E) + P(F) - P(E \cap F)$
  - **Boole's Inequality**: $P(\bigcup_i E_i) \le \sum_i P(E_i)$

- **Conditional Probability**:
$$P(A | B) = \frac{P(A \cap B)}{P(B)} \quad \text{(for } P(B) > 0\text{)}$$

- **Independence**: $A$ and $B$ independent iff $P(A \cap B) = P(A)P(B)$.
  - Equivalent: $P(A|B) = P(A)$ (if $P(B) > 0$).

- **Mutually Exclusive vs Independent**:
  - Mutually exclusive: $P(A \cap B) = 0$.
  - Independent: $P(A \cap B) = P(A)P(B)$.
  - Events with positive probability cannot be both.

- **Bayes' Theorem**:
$$P(A_i | B) = \frac{P(B | A_i) P(A_i)}{\sum_j P(B | A_j) P(A_j)}$$

  - **Prior**: $P(A_i)$
  - **Likelihood**: $P(B | A_i)$
  - **Posterior**: $P(A_i | B)$
  - **Evidence**: $P(B) = \sum_j P(B | A_j) P(A_j)$

- **Law of Total Probability**: If $A_1, \ldots, A_n$ partition $\Omega$:
$$P(B) = \sum_{i=1}^{n} P(B | A_i) P(A_i)$$

#### Random Variables and Distributions

- **Random Variable (RV)**: Function $X: \Omega \to \mathbb{R}$.

- **Cumulative Distribution Function (CDF)**: $F_X(x) = P(X \le x)$.
  - Properties: Non-decreasing, right-continuous, $\lim_{x \to -\infty} F(x) = 0$, $\lim_{x \to \infty} F(x) = 1$.

- **Discrete RV**: Takes countable values.
  - **PMF (Probability Mass Function)**: $p_X(x) = P(X = x)$.
  - $\sum_x p_X(x) = 1$.
  - $F(x) = \sum_{t \le x} p_X(t)$.

- **Continuous RV**: Takes uncountable values.
  - **PDF (Probability Density Function)**: $f_X(x)$ such that $F(x) = \int_{-\infty}^x f(t)\,dt$.
  - $\int_{-\infty}^{\infty} f_X(x)\,dx = 1$.
  - $P(a \le X \le b) = \int_a^b f_X(x)\,dx = F(b) - F(a)$.
  - $f_X(x) = F'(x)$ (where derivative exists).
  - Note: $P(X = a) = 0$ for continuous RVs.

- **Key Distributions**:

| Distribution | PMF/PDF | Mean | Variance |
|-------------|---------|------|----------|
| **Bernoulli**($p$) | $p^k(1-p)^{1-k}$ for $k \in \{0,1\}$ | $p$ | $p(1-p)$ |
| **Binomial**($n,p$) | $\binom{n}{k}p^k(1-p)^{n-k}$ | $np$ | $np(1-p)$ |
| **Geometric**($p$) | $(1-p)^{k-1}p$ for $k \ge 1$ | $1/p$ | $(1-p)/p^2$ |
| **Poisson**($\lambda$) | $e^{-\lambda}\lambda^k/k!$ | $\lambda$ | $\lambda$ |
| **Uniform**($a,b$) | $1/(b-a)$ for $x \in [a,b]$ | $(a+b)/2$ | $(b-a)^2/12$ |
| **Exponential**($\lambda$) | $\lambda e^{-\lambda x}$ for $x \ge 0$ | $1/\lambda$ | $1/\lambda^2$ |
| **Normal**($\mu,\sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/(2\sigma^2)}$ | $\mu$ | $\sigma^2$ |

- **Relationships**:
  - Binomial($n$,$p$) $\approx$ Poisson($np$) when $n$ large, $p$ small.
  - Binomial($n$,$p$) $\approx$ Normal($np$, $np(1-p)$) when $np \ge 5$ and $n(1-p) \ge 5$.
  - Exponential($\lambda$): Time between Poisson events (memoryless property).
  - Geometric: Discrete analog of exponential.

- **Memoryless Property**:
  - Exponential: $P(X > s+t | X > s) = P(X > t)$.
  - Geometric: $P(X > m+n | X > m) = P(X > n)$.

#### Expectation and Moments

- **Expectation**: $E[X] = \sum_x x \cdot p_X(x)$ (discrete) or $\int x f_X(x)\,dx$ (continuous).

- **Properties**:
  - $E[aX + b] = aE[X] + b$
  - $E[X + Y] = E[X] + E[Y]$
  - If $X, Y$ independent: $E[XY] = E[X]E[Y]$

- **Variance**: $\text{Var}(X) = E[(X - \mu)^2] = E[X^2] - (E[X])^2$.
  - $\text{Var}(aX + b) = a^2 \text{Var}(X)$
  - If $X, Y$ independent: $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y)$

- **Standard Deviation**: $\sigma_X = \sqrt{\text{Var}(X)}$.

- **Conditional Expectation**:
  - $E[X | Y = y] = \sum_x x \cdot p_{X|Y}(x|y)$ (discrete).
  - **Law of Total Expectation**: $E[X] = E[E[X | Y]]$.
  - $E[X | Y]$ is a function of $Y$ (random variable).

- **Conditional Variance**:
  - $\text{Var}(X | Y) = E[X^2 | Y] - (E[X | Y])^2$.
  - **Law of Total Variance**: $\text{Var}(X) = E[\text{Var}(X | Y)] + \text{Var}(E[X | Y])$.

- **Moment Generating Function (MGF)**: $M_X(t) = E[e^{tX}]$.
  - $E[X^n] = M_X^{(n)}(0)$ (nth derivative at 0).
  - If $X, Y$ independent: $M_{X+Y}(t) = M_X(t) M_Y(t)$.
  - **Characteristic Function**: $\phi_X(t) = E[e^{itX}]$ (always exists).

#### Joint Distributions and Multivariate Analysis

- **Joint CDF**: $F_{X,Y}(x,y) = P(X \le x, Y \le y)$.
- **Joint PMF/PDF**: $p_{X,Y}(x,y)$ or $f_{X,Y}(x,y)$.
- **Marginal Distributions**: $p_X(x) = \sum_y p_{X,Y}(x,y)$ or $f_X(x) = \int f_{X,Y}(x,y)\,dy$.
- **Conditional Distributions**: $p_{Y|X}(y|x) = p_{X,Y}(x,y) / p_X(x)$.

- **Covariance**:
$$\text{Cov}(X, Y) = E[(X - \mu_X)(Y - \mu_Y)] = E[XY] - E[X]E[Y]$$

  - $\text{Cov}(X, X) = \text{Var}(X)$
  - If $X, Y$ independent: $\text{Cov}(X, Y) = 0$ (converse false).
  - $\text{Var}(X + Y) = \text{Var}(X) + \text{Var}(Y) + 2\text{Cov}(X, Y)$.

- **Correlation Coefficient**:
$$\rho_{X,Y} = \frac{\text{Cov}(X, Y)}{\sigma_X \sigma_Y}$$

  - $-1 \le \rho \le 1$.
  - $\rho = \pm 1$ iff $Y = aX + b$ (linear relationship).

- **Properties of Covariance**:
  - $\text{Cov}(aX + b, cY + d) = ac \, \text{Cov}(X, Y)$
  - $\text{Cov}(X, Y + Z) = \text{Cov}(X, Y) + \text{Cov}(X, Z)$

- **Multivariate Normal**: $(X_1, \ldots, X_n) \sim \mathcal{N}(\mu, \Sigma)$ where $\mu$ is mean vector, $\Sigma$ is covariance matrix.

#### Special Distributions for Hypothesis Testing

- **Standard Normal** $Z \sim \mathcal{N}(0,1)$: $\Phi(z) = P(Z \le z)$.
  - $Z = (X - \mu)/\sigma$ (standardization).
  - $\Phi(-z) = 1 - \Phi(z)$.

- **Chi-Square Distribution** $\chi^2_k$: Sum of $k$ independent squared standard normals.
  - If $Z_i \sim \mathcal{N}(0,1)$ iid, then $\sum_{i=1}^k Z_i^2 \sim \chi^2_k$.
  - Mean = $k$, Variance = $2k$.
  - Used in: goodness-of-fit tests, tests of independence, confidence intervals for variance.

- **Student's t-Distribution** $t_k$: $T = \frac{Z}{\sqrt{V/k}}$ where $Z \sim \mathcal{N}(0,1)$, $V \sim \chi^2_k$, independent.
  - Heavier tails than normal; approaches $\mathcal{N}(0,1)$ as $k \to \infty$.
  - Mean = 0 (for $k > 1$), Variance = $k/(k-2)$ (for $k > 2$).
  - Used in: small sample mean tests.

- **F-Distribution** $F_{d_1, d_2}$: Ratio of independent chi-squares divided by degrees of freedom.
  - $F = \frac{U_1/d_1}{U_2/d_2}$ where $U_i \sim \chi^2_{d_i}$.
  - Used in: ANOVA, comparing variances.

#### Central Limit Theorem and Sampling

- **Central Limit Theorem (CLT)**: Let $X_1, X_2, \ldots, X_n$ be iid random variables with mean $\mu$ and variance $\sigma^2$. Define $\bar{X}_n = \frac{1}{n}\sum_{i=1}^n X_i$. Then:
$$Z_n = \frac{\bar{X}_n - \mu}{\sigma/\sqrt{n}} \xrightarrow{d} \mathcal{N}(0,1) \quad \text{as } n \to \infty$$

  - In practice: For $n \ge 30$, $\bar{X}_n$ is approximately normal.
  - **Standard Error**: $\text{SE} = \sigma/\sqrt{n}$ (estimate with $s/\sqrt{n}$ if $\sigma$ unknown).

- **Confidence Interval**: Range of values likely containing the true parameter.
  - **For mean** ($\sigma$ known): $\bar{x} \pm z_{\alpha/2} \cdot \frac{\sigma}{\sqrt{n}}$
  - **For mean** ($\sigma$ unknown): $\bar{x} \pm t_{\alpha/2, n-1} \cdot \frac{s}{\sqrt{n}}$
  - **For proportion**: $\hat{p} \pm z_{\alpha/2} \sqrt{\frac{\hat{p}(1-\hat{p})}{n}}$
  - **For variance**: $\left(\frac{(n-1)s^2}{\chi^2_{\alpha/2}}, \frac{(n-1)s^2}{\chi^2_{1-\alpha/2}}\right)$

- **Interpretation**: 95% CI means if we repeated sampling infinitely, 95% of intervals would contain true parameter.

#### Hypothesis Testing

- **Null Hypothesis** $H_0$: Default assumption (status quo).
- **Alternative Hypothesis** $H_1$: What we want to prove.
- **Test Statistic**: Function of sample data used to decide.
- **Rejection Region**: Values of test statistic that lead to rejecting $H_0$.
- **Critical Value**: Boundary of rejection region.
- **p-value**: Probability of observing test statistic as extreme as (or more extreme than) observed, assuming $H_0$ true.

- **Decision Rule**: Reject $H_0$ if p-value $\le \alpha$.

- **Errors**:
  - **Type I ($\alpha$)**: Reject true $H_0$ (False Positive). $P(\text{Type I}) = \alpha$.
  - **Type II ($\beta$)**: Fail to reject false $H_0$ (False Negative).
  - **Power**: $1 - \beta$ = probability of correctly rejecting false $H_0$.

- **Common Tests**:

| Test | Statistic | Distribution | Use Case |
|------|-----------|--------------|----------|
| **Z-test** | $Z = \frac{\bar{x} - \mu_0}{\sigma/\sqrt{n}}$ | $\mathcal{N}(0,1)$ | Mean test, $\sigma$ known, large $n$ |
| **One-sample t-test** | $T = \frac{\bar{x} - \mu_0}{s/\sqrt{n}}$ | $t_{n-1}$ | Mean test, $\sigma$ unknown |
| **Two-sample t-test** | $T = \frac{\bar{x}_1 - \bar{x}_2}{s_p\sqrt{1/n_1 + 1/n_2}}$ | $t_{n_1+n_2-2}$ | Compare two means |
| **Paired t-test** | $T = \frac{\bar{d}}{s_d/\sqrt{n}}$ | $t_{n-1}$ | Before-after comparisons |
| **Chi-square goodness-of-fit** | $\chi^2 = \sum \frac{(O_i - E_i)^2}{E_i}$ | $\chi^2_{k-1}$ | Distribution fit |
| **Chi-square independence** | $\chi^2 = \sum \frac{(O_{ij} - E_{ij})^2}{E_{ij}}$ | $\chi^2_{(r-1)(c-1)}$ | Association between categorical variables |
| **F-test** | $F = s_1^2/s_2^2$ | $F_{n_1-1, n_2-1}$ | Compare two variances |

- **ANOVA** (Analysis of Variance):
  - Tests if 3+ group means are equal.
  - **$H_0$**: $\mu_1 = \mu_2 = \cdots = \mu_k$.
  - Partition total variance: $SS_{\text{Total}} = SS_{\text{Between}} + SS_{\text{Within}}$.
  - **F-statistic**: $F = \frac{MS_{\text{Between}}}{MS_{\text{Within}}} = \frac{SS_{\text{Between}}/(k-1)}{SS_{\text{Within}}/(N-k)}$.
  - Reject $H_0$ if $F > F_{\alpha, k-1, N-k}$.

- **p-value Computation**:
  - For two-tailed z-test: $p = 2(1 - \Phi(|z|))$.
  - For one-tailed: $p = 1 - \Phi(z)$ (right) or $\Phi(z)$ (left).

---

## 3. Internal Working

### How Gaussian Elimination Solves Linear Systems
```
Input: Augmented matrix [A|b] of size m×(n+1)

For each column j from 1 to n:
    1. Find pivot: row i ≥ j with max |A[i,j]| (partial pivoting)
    2. Swap row i with row j (if needed)
    3. For each row k below j:
        factor = A[k,j] / A[j,j]
        Row_k ← Row_k - factor × Row_j
    
Result: Upper triangular matrix (Row Echelon Form)

Back substitution:
    For i from n down to 1:
        x_i = (b_i - Σ_{j>i} A[i,j]×x_j) / A[i,i]
```

**Numerical Stability**: Partial pivoting (selecting largest magnitude pivot) prevents division by small numbers that amplify floating-point errors.

### How Eigenvalue Computation Works (QR Algorithm)
```
Input: Matrix A
Repeat until convergence:
    1. QR decompose: A = QR
    2. Recombine: A ← RQ
    3. A converges to upper triangular (eigenvalues on diagonal)
    
For symmetric matrices, A converges to diagonal matrix.
```

### How LU Decomposition Factors a Matrix
```
For k = 1 to n:
    For i = k+1 to n:
        L[i,k] = A[i,k] / A[k,k]        # Multiplier
        For j = k to n:
            A[i,j] -= L[i,k] × A[k,j]   # Update trailing submatrix
            
L = unit lower triangular (multipliers below diagonal)
U = upper triangular (modified A above diagonal)
```

### How the CLT Emerges
```
Step 1: Sample n iid RVs X₁, X₂, ..., Xₙ with mean μ, variance σ²
Step 2: Form sample mean X̄ = (X₁ + ... + Xₙ)/n
Step 3: Standardize: Z = (X̄ - μ)/(σ/√n) = (ΣXᵢ - nμ)/(σ√n)
Step 4: MGF of Z: M_Z(t) = [M_{Xᵢ}(t/(σ√n))]ⁿ
Step 5: Taylor expand M around 0: M(t) ≈ 1 + μt + (σ²+μ²)t²/2 + ...
Step 6: Take limit as n→∞: M_Z(t) → e^{t²/2} (standard normal MGF)
Step 7: By continuity theorem, Z converges in distribution to N(0,1)
```

### How Hypothesis Testing Makes Decisions
```
Step 1: State H₀ and H₁
Step 2: Choose significance level α (typically 0.05)
Step 3: Compute test statistic from sample data
Step 4: Determine critical value or compute p-value
Step 5: If p-value ≤ α → Reject H₀
         Else → Fail to reject H₀
Step 6: State conclusion in context
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Proposition** | Declarative sentence with definite truth value (T or F) |
| **Tautology** | Formula true under all interpretations |
| **Contradiction** | Formula false under all interpretations |
| **CNF** | Conjunctive Normal Form: AND of ORs of literals |
| **DNF** | Disjunctive Normal Form: OR of ANDs of literals |
| **Equivalence Relation** | Reflexive, symmetric, transitive relation |
| **Partial Order** | Reflexive, antisymmetric, transitive relation |
| **Lattice** | Poset with join and meet for every pair |
| **Group** | Set with associative binary operation, identity, inverses |
| **Field** | Commutative ring where non-zero elements have inverses |
| **Chromatic Number** | Minimum colors for proper vertex coloring |
| **Matching** | Set of edges without common vertices |
| **Recurrence** | Equation defining sequence in terms of previous terms |
| **Generating Function** | Power series encoding a sequence |
| **Eigenvalue** | Scalar λ where Av = λv for nonzero v |
| **Eigenvector** | Nonzero vector v where Av = λv |
| **Rank** | Dimension of column space (or row space) |
| **Nullity** | Dimension of null space; n - rank |
| **Determinant** | Scalar encoding matrix invertibility and volume scaling |
| **LU Decomposition** | Factoring A = LU (lower × upper triangular) |
| **SVD** | A = UΣV^T (orthogonal-diagonal-orthogonal) |
| **Quadratic Form** | Expression x^T A x |
| **Positive Definite** | All eigenvalues > 0; x^T A x > 0 for x ≠ 0 |
| **Random Variable** | Function from sample space to real numbers |
| **PMF** | Probability Mass Function (discrete RVs) |
| **PDF** | Probability Density Function (continuous RVs) |
| **CDF** | Cumulative Distribution Function; F(x) = P(X ≤ x) |
| **Expectation** | Weighted average of possible values |
| **Variance** | E[(X-μ)²]; measure of spread |
| **Covariance** | Measure of linear relationship between two RVs |
| **Correlation** | Normalized covariance; ρ ∈ [-1, 1] |
| **Conditional Probability** | P(A\|B) = P(A∩B)/P(B) |
| **Bayes' Theorem** | Updates prior belief with evidence |
| **Independence** | P(A∩B) = P(A)P(B) |
| **CLT** | Sample means converge to normal as n increases |
| **Confidence Interval** | Range likely containing true parameter |
| **p-value** | Probability of observed result assuming H₀ true |
| **Type I Error** | Rejecting true H₀ (false positive) |
| **Type II Error** | Failing to reject false H₀ (false negative) |

---

## 5. Beginner Examples

### Example 1: Logical Equivalence via Truth Table
Show that $p \to q \equiv \neg p \lor q$.

| $p$ | $q$ | $p \to q$ | $\neg p$ | $\neg p \lor q$ |
|-----|-----|-----------|----------|-----------------|
| T | T | T | F | T |
| T | F | F | F | F |
| F | T | T | T | T |
| F | F | T | T | T |

Since columns 3 and 5 match for all rows, the equivalence holds.

### Example 2: Set Operations
Given $A = \{1, 2, 3, 4\}$, $B = \{3, 4, 5, 6\}$, universal set $U = \{1, 2, 3, 4, 5, 6, 7\}$.

- $A \cup B = \{1, 2, 3, 4, 5, 6\}$
- $A \cap B = \{3, 4\}$
- $A - B = \{1, 2\}$
- $A' = \{5, 6, 7\}$
- $A \Delta B = (A-B) \cup (B-A) = \{1, 2, 5, 6\}$

Power set of $A$: $\mathcal{P}(A) = \{\emptyset, \{1\}, \{2\}, \{3\}, \{4\}, \{1,2\}, \{1,3\}, \ldots, A\}$ has $|\mathcal{P}(A)| = 2^4 = 16$ elements.

### Example 3: Verify Group Properties
Show that $(\mathbb{Z}_5^*, \times)$ where $\mathbb{Z}_5^* = \{1, 2, 3, 4\}$ is an abelian group.

- **Closure**: $2 \times 3 = 6 \equiv 1 \pmod{5} \in \mathbb{Z}_5^*$ ✓
- **Associativity**: Multiplication mod 5 is associative ✓
- **Identity**: $1 \times a = a$ for all $a$ ✓
- **Inverses**: $1^{-1}=1$, $2^{-1}=3$ (since $2\times3=6\equiv1$), $3^{-1}=2$, $4^{-1}=4$ ✓
- **Commutative**: $a \times b = b \times a$ ✓

Hence $(\mathbb{Z}_5^*, \times)$ is an abelian group of order 4.

### Example 4: Eigenvalue Computation
Find eigenvalues of $A = \begin{pmatrix} 4 & 1 \\ 2 & 3 \end{pmatrix}$.

Characteristic equation: $\det(A - \lambda I) = 0$

$$\det\begin{pmatrix} 4-\lambda & 1 \\ 2 & 3-\lambda \end{pmatrix} = (4-\lambda)(3-\lambda) - 2 = \lambda^2 - 7\lambda + 10 = 0$$

$$(\lambda - 5)(\lambda - 2) = 0$$

Eigenvalues: $\lambda_1 = 5$, $\lambda_2 = 2$.

For $\lambda_1 = 5$: Solve $(A - 5I)v = 0$:
$$\begin{pmatrix} -1 & 1 \\ 2 & -2 \end{pmatrix}\begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = 0 \implies v_1 = v_2$$

Eigenvector: $v_1 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$.

For $\lambda_2 = 2$: Solve $(A - 2I)v = 0$:
$$\begin{pmatrix} 2 & 1 \\ 2 & 1 \end{pmatrix}\begin{pmatrix} v_1 \\ v_2 \end{pmatrix} = 0 \implies 2v_1 = -v_2$$

Eigenvector: $v_2 = \begin{pmatrix} 1 \\ -2 \end{pmatrix}$.

### Example 5: Probability Basics
A fair die is rolled. Let $A$ = "even number", $B$ = "number > 3". Find $P(A | B)$.

- $A = \{2, 4, 6\}$, $B = \{4, 5, 6\}$, $A \cap B = \{4, 6\}$
- $P(A) = 3/6 = 1/2$, $P(B) = 3/6 = 1/2$, $P(A \cap B) = 2/6 = 1/3$
- $P(A | B) = P(A \cap B)/P(B) = (1/3)/(1/2) = 2/3$

Check independence: $P(A)P(B) = 1/4 \ne 1/3 = P(A \cap B)$, so not independent.

---

## 6. Intermediate Examples

### Example 1: Solving Linear Recurrence
Solve $a_n = 5a_{n-1} - 6a_{n-2}$ with $a_0 = 1, a_1 = 2$.

**Characteristic equation**: $r^2 - 5r + 6 = 0 \implies (r-2)(r-3) = 0$.

Roots: $r = 2, 3$ (distinct).

General solution: $a_n = \alpha \cdot 2^n + \beta \cdot 3^n$.

Using initial conditions:
- $a_0 = 1$: $\alpha + \beta = 1$
- $a_1 = 2$: $2\alpha + 3\beta = 2$

Solving: $\beta = 0$, $\alpha = 1$.

**Answer**: $a_n = 2^n$.

### Example 2: Generating Function for Combinatorics
Find the number of ways to distribute 10 identical balls into 3 distinct boxes where each box has at least 1 ball.

This equals coefficient of $x^{10}$ in $(x + x^2 + x^3 + \cdots)^3 = x^3(1-x)^{-3}$.

Need coefficient of $x^7$ in $(1-x)^{-3} = \sum_{k=0}^{\infty} \binom{k+2}{2} x^k$.

Coefficient: $\binom{7+2}{2} = \binom{9}{2} = 36$.

**Answer**: 36 ways.

### Example 3: LU Decomposition
Find LU decomposition of $A = \begin{pmatrix} 2 & 1 \\ 4 & 3 \end{pmatrix}$.

Gaussian elimination:
- $R_2 \leftarrow R_2 - 2R_1$: multiplier $l_{21} = 2$

$$U = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}, \quad L = \begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}$$

Verify: $LU = \begin{pmatrix} 1 & 0 \\ 2 & 1 \end{pmatrix}\begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 2 & 1 \\ 4 & 3 \end{pmatrix} = A$ ✓

### Example 4: Hypothesis Test (Z-Test)
A sample of 100 students has mean IQ of 105. Population $\sigma = 15$. Test if mean differs from 100 at $\alpha = 0.05$.

- $H_0: \mu = 100$, $H_1: \mu \ne 100$
- $Z = \frac{105 - 100}{15/\sqrt{100}} = \frac{5}{1.5} = 3.33$
- Critical value: $z_{0.025} = 1.96$
- $|3.33| > 1.96$, so **reject $H_0$**
- p-value: $2(1 - \Phi(3.33)) = 2(1 - 0.9996) = 0.0008$

Conclusion: Significant evidence that mean IQ differs from 100.

### Example 5: Bayes' Theorem Application
A disease affects 1% of population. Test is 99% accurate (sensitivity and specificity). If tested positive, what's the probability of having the disease?

- $P(D) = 0.01$, $P(\neg D) = 0.99$
- $P(+|D) = 0.99$, $P(+|\neg D) = 0.01$
- $P(+) = P(+|D)P(D) + P(+|\neg D)P(\neg D) = 0.99(0.01) + 0.01(0.99) = 0.0198$
- $P(D|+) = \frac{P(+|D)P(D)}{P(+)} = \frac{0.0099}{0.0198} = 0.5$

**Answer**: Only 50% chance despite 99% accurate test (base rate fallacy).

---

## 7. Advanced Examples

### Example 1: Diagonalization and Matrix Powers
Diagonalize $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ and compute $A^{100}$.

**Eigenvalues**: $\det(A - \lambda I) = (2-\lambda)^2 - 1 = 0 \implies \lambda = 1, 3$.

**Eigenvectors**:
- $\lambda = 1$: $(A-I)v = 0 \implies v_1 = \begin{pmatrix} 1 \\ -1 \end{pmatrix}$
- $\lambda = 3$: $(A-3I)v = 0 \implies v_2 = \begin{pmatrix} 1 \\ 1 \end{pmatrix}$

$$P = \begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}, \quad D = \begin{pmatrix} 1 & 0 \\ 0 & 3 \end{pmatrix}$$

$$A^{100} = P D^{100} P^{-1} = \begin{pmatrix} 1 & 1 \\ -1 & 1 \end{pmatrix}\begin{pmatrix} 1 & 0 \\ 0 & 3^{100} \end{pmatrix}\frac{1}{2}\begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix}$$

$$= \frac{1}{2}\begin{pmatrix} 1 + 3^{100} & 3^{100} - 1 \\ 3^{100} - 1 & 1 + 3^{100} \end{pmatrix}$$

### Example 2: SVD and Low-Rank Approximation
Find best rank-1 approximation of $A = \begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}$.

**Step 1**: Compute $A^T A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$.

**Step 2**: Eigenvalues: $\det(A^T A - \lambda I) = (2-\lambda)^2 - 1 = 0 \implies \lambda = 1, 3$.

**Step 3**: Singular values: $\sigma_1 = \sqrt{3}$, $\sigma_2 = 1$.

**Step 4**: Eigenvectors of $A^T A$: for $\lambda = 3$, $v_1 = \frac{1}{\sqrt{2}}\begin{pmatrix} 1 \\ 1 \end{pmatrix}$.

**Step 5**: Best rank-1 approximation: $A_1 = \sigma_1 u_1 v_1^T$ where $u_1 = \frac{1}{\sigma_1}Av_1$.

$$u_1 = \frac{1}{\sqrt{3}} \cdot \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 0 \\ 0 & 1 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} 1 \\ 1 \end{pmatrix} = \frac{1}{\sqrt{6}}\begin{pmatrix} 1 \\ 1 \\ 2 \end{pmatrix}$$

$$A_1 = \sqrt{3} \cdot \frac{1}{\sqrt{6}}\begin{pmatrix} 1 \\ 1 \\ 2 \end{pmatrix} \cdot \frac{1}{\sqrt{2}}\begin{pmatrix} 1 & 1 \end{pmatrix} = \frac{1}{2}\begin{pmatrix} 1 & 1 \\ 1 & 1 \\ 2 & 2 \end{pmatrix}$$

### Example 3: MLE and Exponential Family
Given $X_1, \ldots, X_n \sim \text{Exp}(\lambda)$, find MLE of $\lambda$.

**Likelihood**: $L(\lambda) = \prod_{i=1}^n \lambda e^{-\lambda x_i} = \lambda^n e^{-\lambda \sum x_i}$

**Log-likelihood**: $\ell(\lambda) = n\ln\lambda - \lambda\sum x_i$

**Derivative**: $\frac{d\ell}{d\lambda} = \frac{n}{\lambda} - \sum x_i = 0$

**MLE**: $\hat{\lambda} = \frac{n}{\sum x_i} = \frac{1}{\bar{x}}$

**Second derivative**: $\frac{d^2\ell}{d\lambda^2} = -\frac{n}{\lambda^2} < 0$, confirming maximum.

### Example 4: ANOVA Calculation
Three teaching methods tested on students:

| Method A | Method B | Method C |
|----------|----------|----------|
| 78 | 85 | 92 |
| 82 | 88 | 95 |
| 75 | 82 | 89 |
| 80 | 86 | 94 |

**Means**: $\bar{x}_A = 78.75$, $\bar{x}_B = 85.25$, $\bar{x}_C = 92.5$, Grand mean $\bar{x} = 85.5$

**SSB** (Between): $3[(78.75-85.5)^2 + (85.25-85.5)^2 + (92.5-85.5)^2] = 3[45.5625 + 0.0625 + 49] = 283.875$

**SSW** (Within):
- A: $(78-78.75)^2 + (82-78.75)^2 + (75-78.75)^2 + (80-78.75)^2 = 0.5625 + 10.5625 + 14.0625 + 1.5625 = 26.75$
- B: $(85-85.25)^2 + (88-85.25)^2 + (82-85.25)^2 + (86-85.25)^2 = 0.0625 + 7.5625 + 10.5625 + 0.5625 = 18.75$
- C: $(92-92.5)^2 + (95-92.5)^2 + (89-92.5)^2 + (94-92.5)^2 = 0.25 + 6.25 + 12.25 + 2.25 = 21$

SSW = 26.75 + 18.75 + 21 = 66.5

**F-statistic**: $F = \frac{SSB/(3-1)}{SSW/(12-3)} = \frac{141.9375}{7.389} = 19.21$

Compare to $F_{0.05, 2, 9} = 4.26$. Since $19.21 > 4.26$, reject $H_0$: significant difference between methods.

### Example 5: Markov's and Chebyshev's Inequalities
For RV $X$ with $\mu = 10$, $\sigma^2 = 4$, bound $P(X \ge 16)$.

**Markov** (requires non-negative): $P(X \ge 16) \le E[X]/16 = 10/16 = 0.625$

**Chebyshev**: $P(|X - \mu| \ge k\sigma) \le 1/k^2$

Here $16 = 10 + 6 = 10 + 3\sigma$ (since $\sigma = 2$), so $k = 3$.

$P(|X - 10| \ge 6) \le 1/9 \approx 0.111$

Chebyshev gives tighter bound when variance is known.

---

## 8. How Interviewers Think

### Red Flags
- **Confusing necessary and sufficient conditions**: Saying "if $AB = I$ then $A$ is invertible" without checking $BA = I$ (for non-square matrices).
- **Ignoring edge cases**: Not checking if matrix is invertible before computing inverse.
- **Misapplying independence**: Assuming $P(A|B) = P(A)$ without justification.
- **Forgetting CLT conditions**: Applying CLT with small samples from highly skewed distributions.
- **Sign errors in determinants**: Cofactor expansion mistakes.
- **Confusing correlation with causation**: "High correlation implies X causes Y."
- **Not verifying constraints**: In optimization, ignoring boundary points.
- **Assuming normal distribution**: When problem specifies uniform or other distribution.
- **Rank-nullity confusion**: Thinking rank + nullity = number of rows (it's columns).
- **Bayes' theorem errors**: Swapping prior and likelihood.

### Green Flags
- **Systematic approach**: Breaking complex problems into steps.
- **Verification**: Checking answer by substitution or alternative method.
- **Dimensional analysis**: Verifying matrix multiplication dimensions match.
- **Intuitive checks**: "Does this eigenvalue make sense given the trace?"
- **Clear notation**: Distinguishing between random variables and their values.
- **Stating assumptions**: "Assuming the sample is iid..."
- **Multiple solution paths**: Solving via elimination and verifying with matrix inverse.
- **Connecting concepts**: "This is a Markov chain, so I can use the stationary distribution."
- **Asymptotic thinking**: "As $n \to \infty$, this term dominates."
- **Probabilistic reasoning**: Using symmetry to simplify counting.

### Answer Matrix

| Question Type | Key Insight | Common Trap | Approach |
|--------------|-------------|-------------|----------|
| **Eigenvalue** | Trace = sum, det = product | Forgetting complex eigenvalues exist | Check characteristic polynomial degree |
| **Probability** | Define sample space first | Assuming independence | Use Bayes' or law of total probability |
| **Linear System** | Check rank of augmented matrix | Assuming unique solution | Row reduce to RREF |
| **Graph Coloring** | Bipartite = 2-colorable | Confusing vertex and edge coloring | Check for odd cycles |
| **Hypothesis Test** | State $H_0$ and $H_1$ clearly | Confusing p-value with $P(H_0)$ | Compute test statistic, compare to critical value |
| **Recurrence** | Characteristic equation | Missing particular solution for non-homogeneous | Check form of $f(n)$ |
| **Optimization** | Check critical points AND boundaries | Assuming interior solution | Use second derivative test or bordered Hessian |
| **Matrix Decomposition** | LU requires no row exchanges | Forgetting permutation matrix $P$ | Check if leading principal minors are non-zero |

---

## 9. Frequently Asked Interview Questions (25 Questions)

### Conceptual (1-10)

1. **What is the difference between a monoid and a group?**
   A monoid is a set with an associative binary operation and an identity element. A group additionally requires every element to have an inverse. Example: $(\mathbb{N}, +)$ is a monoid but not a group (no additive inverses for positive integers).

2. **When is a matrix diagonalizable?**
   An $n \times n$ matrix is diagonalizable iff it has $n$ linearly independent eigenvectors. Sufficient conditions: (a) $n$ distinct eigenvalues, (b) matrix is symmetric (or Hermitian). The matrix $A = \begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$ is not diagonalizable (only one eigenvector).

3. **Explain the Central Limit Theorem intuitively.**
   When you average many independent random variables, the distribution of the average becomes approximately normal, regardless of the original distribution. This works because averaging smooths out irregularities. The approximation improves with larger sample sizes ($n \ge 30$ is a rule of thumb).

4. **What is the difference between Type I and Type II errors?**
   Type I: Rejecting a true null hypothesis (false positive). Type II: Failing to reject a false null hypothesis (false negative). Decreasing $\alpha$ (Type I rate) increases $\beta$ (Type II rate) for fixed sample size.

5. **Why do we use $n-1$ in sample variance instead of $n$?**
   Using $n$ gives a biased estimate of population variance. Dividing by $n-1$ (Bessel's correction) makes the estimator unbiased: $E[s^2] = \sigma^2$. The "lost" degree of freedom comes from estimating the sample mean.

6. **What is the rank-nullity theorem?**
   For an $m \times n$ matrix $A$: $\text{rank}(A) + \text{nullity}(A) = n$. The rank is the dimension of the column space; nullity is the dimension of the null space. Together they account for all $n$ columns.

7. **Explain Bayes' theorem with an example.**
   Bayes' theorem updates beliefs given evidence: $P(H|E) = \frac{P(E|H)P(H)}{P(E)}$. Example: Medical testing—even with a 99% accurate test, if disease prevalence is 0.1%, a positive result only gives ~9% probability of having the disease.

8. **What makes a relation an equivalence relation?**
   Three properties: reflexive ($aRa$), symmetric ($aRb \implies bRa$), and transitive ($aRb \land bRc \implies aRc$). Equivalence relations partition sets into disjoint equivalence classes.

9. **What is the significance of eigenvalues in PCA?**
   In PCA, eigenvalues of the covariance matrix represent the variance captured by each principal component. Larger eigenvalue = more variance explained. The corresponding eigenvector gives the direction of maximum variance.

10. **When do you use t-test vs z-test?**
    Use z-test when population variance is known and sample size is large ($n \ge 30$). Use t-test when population variance is unknown (estimated from sample) and/or sample size is small. The t-distribution has heavier tails, accounting for additional uncertainty.

### Scenario-Based (11-18)

11. **You flip a coin 100 times and get 60 heads. Is the coin fair?**
    Test $H_0: p = 0.5$ vs $H_1: p \ne 0.5$. $Z = \frac{0.6 - 0.5}{\sqrt{0.5(0.5)/100}} = 2.0$. p-value = $2(1 - \Phi(2)) = 0.046$. At $\alpha = 0.05$, reject $H_0$: evidence suggests coin is biased.

12. **How would you detect if a graph is bipartite?**
    Use BFS/DFS to 2-color the graph. Start with any vertex, color it red. All neighbors must be blue. If we ever need to assign a conflicting color, the graph is not bipartite (contains odd cycle). Time complexity: $O(V + E)$.

13. **A system $Ax = b$ has no solution. What does this mean geometrically?**
    $b$ is not in the column space of $A$. The columns of $A$ span a subspace, and $b$ lies outside it. We can find the least-squares solution $x^*$ that minimizes $\|Ax - b\|^2$ by solving $A^T A x^* = A^T b$.

14. **You have 10,000 features. How do you reduce dimensionality?**
    Use PCA: compute SVD of data matrix, project onto top $k$ singular vectors where $k$ captures 95% of variance (sum of top $k$ singular values squared / total sum). Alternatively, use feature selection methods.

15. **Two classes have different variances. Which test do you use?**
    Use Welch's t-test (unequal variances t-test): $T = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$. Degrees of freedom approximated by Welch-Satterthwaite equation.

16. **How many edges in a complete bipartite graph $K_{m,n}$?**
    Every vertex in the first partition connects to all $n$ vertices in the second. Total edges: $m \cdot n$.

17. **A matrix has determinant 0. What does this tell you?**
    The matrix is singular (not invertible). Its columns are linearly dependent. The null space is non-trivial (contains non-zero vectors). The transformation collapses space into lower dimension.

18. **You observe 5 events in 2 hours. What's the probability of 0 events in the next hour?**
    Assuming Poisson process: $\lambda = 5/2 = 2.5$ per hour. $P(X = 0) = e^{-2.5} \approx 0.082$.

### Debugging (19-22)

19. **Your eigenvalue computation gives complex values for a real matrix. Is this wrong?**
    Not necessarily. Real matrices can have complex eigenvalues (they come in conjugate pairs). However, real symmetric matrices always have real eigenvalues. Check if your matrix is symmetric.

20. **Your probability calculation gives $P(A) > 1$. What went wrong?**
    Check: (1) Did you double-count overlapping events? (2) Are you using the correct denominator for conditional probability? (3) Did you forget to normalize? Probabilities must be in $[0, 1]$.

21. **Gaussian elimination gives a row of zeros but the system should have a unique solution.**
    Check for: (1) Numerical precision issues (use partial pivoting), (2) Incorrect row operations, (3) The system might actually be singular (verify determinant).

22. **Your hypothesis test rejects $H_0$ but the effect size is tiny. What's happening?**
    With large sample sizes, even trivial effects become statistically significant. Report effect size (Cohen's d) alongside p-value. Statistical significance ≠ practical significance.

### System Design (23-24)

23. **Design a system to estimate $\pi$ using probability.**
    Use Monte Carlo: Generate random points $(x, y)$ in $[0,1]^2$. Count fraction inside quarter circle ($x^2 + y^2 \le 1$). This fraction $\approx \pi/4$, so $\pi \approx 4 \times (\text{fraction})$. Error decreases as $O(1/\sqrt{n})$.

24. **How would you test if a random number generator is uniform?**
    (1) Chi-square goodness-of-fit test comparing observed frequencies to expected uniform frequencies. (2) Kolmogorov-Smirnov test comparing empirical CDF to uniform CDF. (3) Visual inspection with histogram and Q-Q plot.

### Advanced (25)

25. **Prove that $\det(e^A) = e^{\text{tr}(A)}$.**
    Using Jordan form: $A = PJP^{-1}$ where $J$ is Jordan matrix. Then $e^A = Pe^JP^{-1}$, so $\det(e^A) = \det(e^J)$. For Jordan block with eigenvalue $\lambda$, $e^J$ has $e^\lambda$ on diagonal. So $\det(e^J) = \prod e^{\lambda_i} = e^{\sum \lambda_i} = e^{\text{tr}(A)}$.

---

## 10. Common Mistakes

- **Assuming $P(A|B) = P(B|A)$**: These are equal only when $P(A) = P(B)$. Base rate neglect.
- **Forgetting to check invertibility**: Computing $A^{-1}$ without verifying $\det(A) \ne 0$.
- **Confusing $\land$ and $\lor$ in logic**: "AND" requires both true; "OR" requires at least one.
- **Misapplying L'Hôpital's Rule**: Only valid for $0/0$ or $\infty/\infty$ forms.
- **Ignoring boundary conditions in optimization**: Max/min can occur at endpoints.
- **Using $=$ instead of $\equiv$ for logical equivalence**: $\equiv$ denotes equivalence; $=$ is equality.
- **Forgetting the chain rule**: $\frac{d}{dx}f(g(x)) = f'(g(x)) \cdot g'(x)$, not $f'(g(x))$.
- **Assuming normal approximation for small $n$**: CLT requires $n \ge 30$ for non-normal populations.
- **Confusing necessary and sufficient**: "$A$ invertible $\implies \det(A) \ne 0$" but not conversely stated.
- **Not checking linear independence**: Assuming eigenvectors are independent without verification.
- **Sign errors in cofactor expansion**: $(-1)^{i+j}$ alternates in checkerboard pattern.
- **Forgetting Jacobian in transformations**: $f_Y(y) = f_X(g^{-1}(y)) \cdot |\frac{d}{dy}g^{-1}(y)|$.
- **Assuming all symmetric matrices are positive definite**: Only if all eigenvalues > 0.
- **Using population $\sigma$ when sample $s$ should be**: Affects choice of z-test vs t-test.
- **Not stating assumptions**: "Assuming iid samples..." is crucial for validity.

---

## 11. Comparison Tables

### Logic: Propositional vs First-Order

| Aspect | Propositional Logic | First-Order Logic |
|--------|---------------------|-------------------|
| **Basic Unit** | Propositions (atomic) | Predicates with variables |
| **Quantifiers** | None | $\forall$, $\exists$ |
| **Expressiveness** | Limited | Can express "for all", "there exists" |
| **Decidability** | Decidable (truth tables) | Semi-decidable (validity) |
| **Complexity** | NP-complete (SAT) | Undecidable in general |
| **Use Case** | Circuit design, constraints | Mathematics, verification |

### Distributions: Discrete vs Continuous

| Aspect | Discrete | Continuous |
|--------|----------|------------|
| **Function** | PMF $p(x)$ | PDF $f(x)$ |
| **Probability at point** | $P(X = x) = p(x) > 0$ | $P(X = x) = 0$ |
| **Sum vs Integral** | $\sum p(x) = 1$ | $\int f(x)\,dx = 1$ |
| **CDF** | Step function | Continuous function |
| **Examples** | Binomial, Poisson, Geometric | Normal, Exponential, Uniform |

### Matrix Decompositions

| Decomposition | Form | Requirements | Primary Use |
|--------------|------|--------------|-------------|
| **LU** | $A = LU$ | No zero pivots (or use $PA = LU$) | Solving linear systems |
| **QR** | $A = QR$ | Any matrix | Least squares, stability |
| **SVD** | $A = U\Sigma V^T$ | Any matrix | PCA, low-rank approx, pseudoinverse |
| **Eigendecomposition** | $A = PDP^{-1}$ | Diagonalizable | Matrix powers, differential equations |
| **Cholesky** | $A = LL^T$ | Symmetric positive definite | Efficient SPD solving |

### Hypothesis Tests

| Test | When to Use | Assumptions | Test Statistic |
|------|-------------|-------------|----------------|
| **Z-test** | Known $\sigma$, large $n$ | Normal or $n \ge 30$ | $Z = \frac{\bar{x}-\mu_0}{\sigma/\sqrt{n}}$ |
| **t-test** | Unknown $\sigma$, small $n$ | Approximately normal | $T = \frac{\bar{x}-\mu_0}{s/\sqrt{n}}$ |
| **Chi-square** | Categorical data | Expected counts $\ge 5$ | $\chi^2 = \sum \frac{(O-E)^2}{E}$ |
| **F-test** | Compare variances | Normal populations | $F = s_1^2/s_2^2$ |
| **ANOVA** | 3+ group means | Normality, equal variance | $F = \frac{MS_B}{MS_W}$ |

### Graph Types

| Property | Complete $K_n$ | Bipartite $K_{m,n}$ | Tree | Cycle $C_n$ |
|----------|----------------|---------------------|------|-------------|
| **Edges** | $n(n-1)/2$ | $mn$ | $n-1$ | $n$ |
| **Chromatic Number** | $n$ | 2 | 2 | 2 if even, 3 if odd |
| **Planar** | Only $n \le 4$ | Only $m \le 2$ or $n \le 2$ | Yes | Yes |
| **Eulerian** | $n$ odd | $m = n$ (even) | No (unless $n=1$) | $n$ even |
| **Hamiltonian** | Always | $m = n$ | Only path graphs | Always |

### Probability Distributions Comparison

| Distribution | Type | Mean | Variance | MGF | Key Property |
|-------------|------|------|----------|-----|--------------|
| **Bernoulli**($p$) | Discrete | $p$ | $p(1-p)$ | $1-p+pe^t$ | Single trial |
| **Binomial**($n,p$) | Discrete | $np$ | $np(1-p)$ | $(1-p+pe^t)^n$ | Sum of $n$ Bernoulli |
| **Geometric**($p$) | Discrete | $1/p$ | $(1-p)/p^2$ | $\frac{pe^t}{1-(1-p)e^t}$ | Memoryless (discrete) |
| **Poisson**($\lambda$) | Discrete | $\lambda$ | $\lambda$ | $e^{\lambda(e^t-1)}$ | Rare events |
| **Uniform**($a,b$) | Continuous | $(a+b)/2$ | $(b-a)^2/12$ | $\frac{e^{tb}-e^{ta}}{t(b-a)}$ | Constant density |
| **Exponential**($\lambda$) | Continuous | $1/\lambda$ | $1/\lambda^2$ | $\frac{\lambda}{\lambda-t}$ | Memoryless (continuous) |
| **Normal**($\mu,\sigma^2$) | Continuous | $\mu$ | $\sigma^2$ | $e^{\mu t + \sigma^2 t^2/2}$ | CLT limit |

### Convergence Types (for Sequences of RVs)

| Type | Notation | Definition | Strength |
|------|----------|------------|----------|
| **Almost Sure** | $X_n \xrightarrow{a.s.} X$ | $P(\lim X_n = X) = 1$ | Strongest |
| **In Probability** | $X_n \xrightarrow{P} X$ | $\lim P(|X_n - X| > \epsilon) = 0$ | Strong |
| **In Distribution** | $X_n \xrightarrow{d} X$ | $\lim F_{X_n}(x) = F_X(x)$ at continuity points | Weakest |
| **In $L^p$** | $X_n \xrightarrow{L^p} X$ | $\lim E[|X_n - X|^p] = 0$ | Intermediate |

Relationship: Almost sure $\implies$ In probability $\implies$ In distribution.

---

## 12. Practical Projects

### Discrete Mathematics Projects
- **Boolean Satisfiability Solver**: Implement DPLL algorithm for SAT solving.
- **Graph Algorithm Visualizer**: BFS/DFS/Dijkstra with step-by-step visualization.
- **Formal Verification Tool**: Model checker for temporal logic properties.
- **Combinatorial Game Solver**: Use Sprague-Grundy theorem for impartial games.
- **Automata Simulator**: DFA/NFA/PDA simulator with regex conversion.

### Linear Algebra Projects
- **Matrix Library**: Implement LU, QR, SVD from scratch (no libraries).
- **PCA Implementation**: Dimensionality reduction on real datasets.
- **PageRank Algorithm**: Power iteration for eigenvector computation.
- **Image Compression**: SVD-based compression with quality metrics.
- **Neural Network from Scratch**: Backpropagation using only matrix operations.

### Calculus & Optimization Projects
- **Gradient Descent Visualizer**: 2D/3D optimization with trajectory plotting.
- **Newton's Method Solver**: Root finding with convergence analysis.
- **Simulated Annealing**: TSP solver using stochastic optimization.
- **ODE Solver**: Runge-Kutta methods for differential equations.
- **Convex Optimization**: Implement interior point method for LP.

### Probability & Statistics Projects
- **A/B Testing Framework**: Statistical significance calculator with power analysis.
- **Bayesian Inference Engine**: MCMC sampling for posterior estimation.
- **Random Number Generator Suite**: Implement and test various distributions.
- **Hypothesis Testing Calculator**: Automated test selection and p-value computation.
- **Monte Carlo Simulation**: Option pricing, integration, probability estimation.

---

## 13. Internship Preparation

### Must-Know Theorems (Proofs Expected)
- **Lagrange's Theorem** (group theory)
- **Rank-Nullity Theorem** (linear algebra)
- **Cayley-Hamilton Theorem** (matrices)
- **Central Limit Theorem** (probability)
- **Bayes' Theorem** (probability)
- **Euler's Formula** (planar graphs)
- **Handshaking Lemma** (graph theory)

### Must-Solve Problem Types
- **Eigenvalue/Eigenvector**: 2×2 and 3×3 matrices, diagonalization checks.
- **System of Equations**: Consistency, parametric solutions, rank analysis.
- **Probability**: Bayes' theorem, conditional probability, distribution identification.
- **Graph Theory**: Chromatic number, matching, planarity, connectivity.
- **Recurrence Relations**: Solve using characteristic equation or generating functions.
- **Hypothesis Testing**: Identify correct test, compute statistic, make decision.

### Quick Revision Formulas
- $\det(AB) = \det(A)\det(B)$
- $\text{tr}(A+B) = \text{tr}(A) + \text{tr}(B)$
- $A^{-1} = \frac{1}{\det(A)}\text{adj}(A)$
- $E[aX + b] = aE[X] + b$
- $\text{Var}(aX + b) = a^2\text{Var}(X)$
- $P(A|B) = \frac{P(B|A)P(A)}{P(B)}$
- $\binom{n}{r} = \frac{n!}{r!(n-r)!}$
- $\sum_{k=0}^{n} \binom{n}{k} = 2^n$

### Common GATE Question Patterns
- **Assertion-Reason**: "Assertion: Matrix is invertible. Reason: Determinant is non-zero."
- **Numerical Answer**: Compute eigenvalue, probability, or rank.
- **Match the Following**: Match distributions to their properties.
- **Common Data**: Multi-part questions on same matrix/dataset.

### Time Management Strategy
- **Section 1 (Math)**: 15-18 minutes for 1-mark questions.
- **2-mark questions**: 3-4 minutes each.
- **Skip if stuck**: Mark for review, return later.
- **Verification**: Use properties (trace, determinant) to check eigenvalue answers.

---

## 14. Cheat Sheet

### Linear Algebra Quick Reference

| Operation | Formula | Notes |
|-----------|---------|-------|
| **Determinant (2×2)** | $ad - bc$ | For $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$ |
| **Determinant (3×3)** | $a(ei-fh) - b(di-fg) + c(dh-eg)$ | Cofactor expansion |
| **Inverse (2×2)** | $\frac{1}{ad-bc}\begin{pmatrix} d & -b \\ -c & a \end{pmatrix}$ | Swap diagonal, negate off-diagonal |
| **Eigenvalues** | Solve $\det(A-\lambda I) = 0$ | Sum = trace, product = det |
| **Rank** | Number of pivots in RREF | = dim(Col) = dim(Row) |
| **Nullity** | $n - \text{rank}(A)$ | Dimension of null space |

### Probability Quick Reference

| Concept | Formula | When to Use |
|---------|---------|-------------|
| **Bayes' Theorem** | $P(A\|B) = \frac{P(B\|A)P(A)}{P(B)}$ | Reverse conditioning |
| **Total Probability** | $P(B) = \sum P(B\|A_i)P(A_i)$ | Partition of sample space |
| **Independence Test** | $P(A \cap B) = P(A)P(B)$ | Check if events independent |
| **Conditional Expectation** | $E[X\|Y] = \sum x P(X=x\|Y)$ | Expected value given info |
| **Variance** | $E[X^2] - (E[X])^2$ | Computational formula |
| **Covariance** | $E[XY] - E[X]E[Y]$ | Linear relationship |

### Distribution Quick Reference

| Distribution | PMF/PDF | Mean | Variance |
|-------------|---------|------|----------|
| **Bernoulli**($p$) | $p^x(1-p)^{1-x}$ | $p$ | $p(1-p)$ |
| **Binomial**($n,p$) | $\binom{n}{x}p^x(1-p)^{n-x}$ | $np$ | $np(1-p)$ |
| **Poisson**($\lambda$) | $e^{-\lambda}\lambda^x/x!$ | $\lambda$ | $\lambda$ |
| **Uniform**($a,b$) | $1/(b-a)$ | $(a+b)/2$ | $(b-a)^2/12$ |
| **Exponential**($\lambda$) | $\lambda e^{-\lambda x}$ | $1/\lambda$ | $1/\lambda^2$ |
| **Normal**($\mu,\sigma^2$) | $\frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$ | $\mu$ | $\sigma^2$ |

### Hypothesis Testing Decision Tree

```
Is the parameter a mean?
├── Yes → Is σ known?
│   ├── Yes → Z-test
│   └── No → Is n ≥ 30?
│       ├── Yes → Z-test (approximate)
│       └── No → t-test
└── No → Is it a proportion?
    ├── Yes → Z-test for proportion
    └── No → Is it variance?
        ├── Yes → Chi-square test
        └── No → Categorical data?
            ├── Yes → Chi-square test
            └── No → F-test (compare variances)
```

### Key Theorems Summary

| Theorem | Statement | Application |
|---------|-----------|-------------|
| **Rank-Nullity** | $\text{rank} + \text{nullity} = n$ | Find nullity from rank |
| **Cayley-Hamilton** | $p(A) = 0$ for characteristic polynomial $p$ | Compute matrix powers |
| **Spectral** | Symmetric matrix has real eigenvalues, orthogonal eigenvectors | PCA, quadratic forms |
| **CLT** | Sample means → Normal | Confidence intervals, hypothesis tests |
| **Bayes** | $P(H\|E) \propto P(E\|H)P(H)$ | Update beliefs |
| **Euler** | $V - E + F = 2$ (planar) | Verify planarity |
| **Hall's** | Bipartite matching exists iff $\|N(S)\| \ge \|S\|$ | Matching problems |

---

## 15. One-Day Revision Checklist

### Discrete Mathematics
- [ ] Construct truth tables for compound propositions
- [ ] Verify logical equivalences using laws (De Morgan, distributive)
- [ ] Convert statements to first-order logic with quantifiers
- [ ] Identify reflexive, symmetric, transitive properties of relations
- [ ] Draw Hasse diagrams for partial orders
- [ ] Verify lattice properties (existence of join and meet)
- [ ] Check group axioms (closure, associativity, identity, inverse)
- [ ] Apply Lagrange's theorem (order of subgroup divides group order)
- [ ] Determine if graph is bipartite (check for odd cycles)
- [ ] Compute chromatic number for simple graphs
- [ ] Apply Hall's marriage theorem for bipartite matching
- [ ] Solve counting problems using permutations and combinations
- [ ] Apply inclusion-exclusion principle
- [ ] Solve linear recurrences using characteristic equation
- [ ] Use generating functions to solve counting problems

### Linear Algebra
- [ ] Compute matrix products and verify dimensions
- [ ] Calculate determinants using cofactor expansion
- [ ] Find matrix inverse using Gauss-Jordan elimination
- [ ] Determine rank by row reduction to RREF
- [ ] Solve systems using Gaussian elimination
- [ ] Check consistency using rank of augmented matrix
- [ ] Find eigenvalues from characteristic polynomial
- [ ] Find eigenvectors for each eigenvalue
- [ ] Verify diagonalization: $A = PDP^{-1}$
- [ ] Perform LU decomposition (with pivoting if needed)
- [ ] Apply Cayley-Hamilton theorem
- [ ] Classify quadratic forms (positive definite, etc.)
- [ ] Use Sylvester's criterion for positive definiteness
- [ ] Compute SVD components conceptually
- [ ] Apply rank-nullity theorem

### Calculus
- [ ] Evaluate limits using algebraic manipulation
- [ ] Apply L'Hôpital's rule for indeterminate forms
- [ ] Check continuity and differentiability at points
- [ ] Compute derivatives using product, quotient, chain rules
- [ ] Apply Mean Value Theorem
- [ ] Find Taylor series expansions
- [ ] Identify critical points for maxima/minima
- [ ] Use second derivative test for nature of critical points
- [ ] Evaluate definite integrals using substitution
- [ ] Apply integration by parts
- [ ] Solve optimization problems with constraints

### Probability & Statistics
- [ ] Compute probabilities using axioms and properties
- [ ] Apply conditional probability formula
- [ ] Check independence of events
- [ ] Apply Bayes' theorem with tree diagrams
- [ ] Use law of total probability
- [ ] Identify appropriate distribution for a scenario
- [ ] Compute mean and variance for standard distributions
- [ ] Apply CLT for sample means
- [ ] Construct confidence intervals for mean and proportion
- [ ] Perform z-test and t-test
- [ ] Compute p-values and make decisions
- [ ] Apply chi-square test for independence
- [ ] Perform ANOVA calculations
- [ ] Compute covariance and correlation
- [ ] Apply law of total expectation and variance

### Final Review
- [ ] Review all comparison tables
- [ ] Memorize key formulas from cheat sheet
- [ ] Practice 2-3 problems from each section
- [ ] Review common mistakes list
- [ ] Verify understanding of theorem statements
- [ ] Check time management strategy
- [ ] Get good sleep before exam!