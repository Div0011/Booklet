# 47. GATE 2027: Programming, Data Structures and Algorithms

> **CS Syllabus:** Programming in C. Recursion. Arrays, stacks, queues, linked lists, trees, binary search trees, binary heaps, graphs. Searching, sorting, hashing. Asymptotic worst case time and space complexity. Algorithm design techniques: greedy, dynamic programming and divide‐and‐conquer. Graph traversals, minimum spanning trees, shortest paths.
>
> **DA Syllabus:** Programming in Python, basic data structures: stacks, queues, linked lists, trees, hash tables; Search algorithms: linear search and binary search, basic sorting algorithms: selection sort, bubble sort and insertion sort; divide and conquer: mergesort, quicksort; introduction to graph theory; basic graph algorithms: traversals and shortest path.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Core Concepts](#2-core-concepts)
3. [Internal Working](#3-internal-working)
4. [Important Terminology](#4-important-terminology)
5. [Beginner Examples](#5-beginner-examples)
6. [Intermediate Examples](#6-intermediate-examples)
7. [Advanced Examples](#7-advanced-examples)
8. [How Interviewers Think](#8-how-interviewers-think)
9. [FAQs](#9-faqs)
10. [Common Mistakes](#10-common-mistakes)
11. [Comparison Tables](#11-comparison-tables)
12. [Practical Projects](#12-practical-projects)
13. [Internship Preparation](#13-internship-preparation)
14. [Cheat Sheet](#14-cheat-sheet)
15. [One-Day Revision Checklist](#15-one-day-revision-checklist)

---

## 1. Introduction

### What is Programming, Data Structures and Algorithms (PDSA)?

Programming, Data Structures and Algorithms is the foundational discipline of computer science that deals with:

- **Programming:** Writing instructions (code) to solve computational problems using languages like C or Python.
- **Data Structures:** Organizing and storing data efficiently (arrays, trees, graphs, hash tables).
- **Algorithms:** Step-by-step procedures for solving problems (searching, sorting, optimization).

### Why is PDSA Critical for GATE?

| Aspect | Weightage Insight |
|--------|-------------------|
| **Direct Questions** | 15-20% of GATE CSE paper |
| **Foundation for Other Subjects** | OS, DBMS, COA, Compiler Design all build on PDSA |
| **Problem-Solving Aptitude** | Tests analytical thinking, not just memorization |
| **PSU & Research Opportunities** | Strong PDSA skills essential for interviews and higher studies |

### Problems PDSA Solves

- **Efficiency:** Finding the fastest way to search a database (binary search: $O(\log n)$ vs linear: $O(n)$)
- **Organization:** Storing hierarchical data (file systems → trees)
- **Optimization:** Finding shortest routes (GPS → Dijkstra's algorithm)
- **Resource Management:** Scheduling tasks (OS → queues, priority queues)

### Real-World Use Cases

| Domain | Data Structure / Algorithm |
|--------|---------------------------|
| Google Search | PageRank (graph algorithms) |
| Social Networks | BFS/DFS (friend recommendations) |
| E-commerce | Hash tables (product lookup) |
| Navigation Systems | Dijkstra's, A* (shortest path) |
| Database Indexing | B-Trees, B+ Trees |
| Compiler Design | Stacks (parsing), Hash tables (symbol tables) |
| Machine Learning | Dynamic programming (sequence alignment) |

### Analogy: Building a House

- **Programming Language** = Knowledge of tools (hammer, saw, drill)
- **Data Structures** = Choosing the right material (wood, steel, concrete) for each part
- **Algorithms** = The blueprint/plan for assembling everything efficiently

A skilled engineer (programmer) knows which material to use (data structure) and the best construction sequence (algorithm) to build a strong, efficient house (software).

---

## 2. Core Concepts

### 2.1 Beginner Level

#### C Programming Fundamentals

```c
// Variables, Data Types, Operators
int main() {
    int a = 10;          // 4 bytes (typically)
    float b = 3.14;      // 4 bytes
    char c = 'A';        // 1 byte
    double d = 3.14159;  // 8 bytes
    
    // Operators
    int sum = a + 5;     // Arithmetic
    int *ptr = &a;       // Address-of, pointer
    int val = *ptr;      // Dereference
    
    return 0;
}
```

#### Control Structures

```c
// If-else, Loops, Switch
for (int i = 0; i < n; i++) {      // For loop
    if (i % 2 == 0) {               // If-else
        printf("%d ", i);
    }
}

while (n > 0) {                     // While loop
    n /= 2;
}

do {                                // Do-while loop
    // executes at least once
} while (condition);
```

#### Functions and Scope

```c
// Function definition, call by value vs call by reference
int factorial(int n) {              // Call by value
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

void swap(int *a, int *b) {         // Call by reference
    int temp = *a;
    *a = *b;
    *b = temp;
}
```

#### Arrays (Basic)

```c
// 1D and 2D arrays
int arr[5] = {1, 2, 3, 4, 5};
int matrix[3][3] = {{1,2,3}, {4,5,6}, {7,8,9}};

// Array traversal
for (int i = 0; i < 5; i++) {
    printf("%d ", arr[i]);
}
```

#### Python Basics

```python
# Variables, Lists, Dictionaries
arr = [1, 2, 3, 4, 5]           # List (dynamic array)
stack = []                       # Stack using list
queue = []                       # Queue (use collections.deque)

# Dictionary (hash table)
hash_map = {"key": "value"}

# List comprehension
squares = [x**2 for x in range(10)]

# Functions
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

---

### 2.2 Intermediate Level

#### Pointers and Memory

```c
// Pointer arithmetic, arrays as pointers
int arr[] = {10, 20, 30, 40};
int *p = arr;           // Points to arr[0]

printf("%d", *(p+2));   // 30 (pointer arithmetic)
printf("%d", p[2]);     // 30 (array notation)

// Dynamic memory allocation
int *dynamic = (int*)malloc(n * sizeof(int));
free(dynamic);          // Always free allocated memory

// Double pointers
int x = 10;
int *p = &x;
int **pp = &p;          // Pointer to pointer
```

#### Structures and Unions

```c
// Structure - each member has separate memory
struct Student {
    char name[50];
    int roll;
    float gpa;
};

// Union - all members share same memory
union Data {
    int i;
    float f;
    char str[20];
};                      // Size = size of largest member

// Typedef
typedef struct Node {
    int data;
    struct Node *next;
} Node;
```

#### Recursion

```c
// Tail recursion vs head recursion
void tail(int n) {          // Recursive call is last statement
    if (n == 0) return;
    printf("%d ", n);
    tail(n - 1);
}

void head(int n) {          // Recursive call is first statement
    if (n == 0) return;
    head(n - 1);
    printf("%d ", n);
}

// Fibonacci with memoization
int fib(int n, int *memo) {
    if (n <= 1) return n;
    if (memo[n] != -1) return memo[n];
    return memo[n] = fib(n-1, memo) + fib(n-2, memo);
}
```

#### Linked Lists

```c
// Singly linked list
struct Node {
    int data;
    struct Node *next;
};

// Insert at beginning - O(1)
void push(struct Node **head, int data) {
    struct Node *new = (struct Node*)malloc(sizeof(struct Node));
    new->data = data;
    new->next = *head;
    *head = new;
}

// Traversal - O(n)
void printList(struct Node *head) {
    while (head != NULL) {
        printf("%d -> ", head->data);
        head = head->next;
    }
    printf("NULL\n");
}
```

#### Stacks and Queues

```c
// Stack using array
#define MAX 1000
int stack[MAX], top = -1;

void push(int x) {
    if (top >= MAX-1) { printf("Overflow\n"); return; }
    stack[++top] = x;
}

int pop() {
    if (top < 0) { printf("Underflow\n"); return -1; }
    return stack[top--];
}

// Queue using array (circular)
int queue[MAX], front = -1, rear = -1;

void enqueue(int x) {
    if ((rear + 1) % MAX == front) { printf("Full\n"); return; }
    if (front == -1) front = 0;
    rear = (rear + 1) % MAX;
    queue[rear] = x;
}
```

#### Trees (Binary Trees)

```c
struct TreeNode {
    int data;
    struct TreeNode *left, *right;
};

// Tree traversals
void inorder(struct TreeNode *root) {
    if (root == NULL) return;
    inorder(root->left);
    printf("%d ", root->data);
    inorder(root->right);
}

void preorder(struct TreeNode *root) {
    if (root == NULL) return;
    printf("%d ", root->data);
    preorder(root->left);
    preorder(root->right);
}

void postorder(struct TreeNode *root) {
    if (root == NULL) return;
    postorder(root->left);
    postorder(root->right);
    printf("%d ", root->data);
}
```

---

### 2.3 Advanced Level

#### Binary Search Trees (BST)

```c
// BST: Left < Root < Right
struct TreeNode* insert(struct TreeNode *root, int key) {
    if (root == NULL) {
        struct TreeNode *new = (struct TreeNode*)malloc(sizeof(struct TreeNode));
        new->data = key;
        new->left = new->right = NULL;
        return new;
    }
    if (key < root->data)
        root->left = insert(root->left, key);
    else if (key > root->data)
        root->right = insert(root->right, key);
    return root;
}

// Search - O(h) where h is height
struct TreeNode* search(struct TreeNode *root, int key) {
    if (root == NULL || root->data == key) return root;
    if (key < root->data) return search(root->left, key);
    return search(root->right, key);
}
```

#### Binary Heaps

```c
// Min-Heap: Parent <= Children
// Array representation: parent(i) = (i-1)/2, left(i) = 2i+1, right(i) = 2i+2

void heapify(int arr[], int n, int i) {
    int smallest = i;
    int left = 2*i + 1;
    int right = 2*i + 2;
    
    if (left < n && arr[left] < arr[smallest])
        smallest = left;
    if (right < n && arr[right] < arr[smallest])
        smallest = right;
    
    if (smallest != i) {
        swap(&arr[i], &arr[smallest]);
        heapify(arr, n, smallest);
    }
}

// Build heap - O(n)
void buildHeap(int arr[], int n) {
    for (int i = n/2 - 1; i >= 0; i--)
        heapify(arr, n, i);
}
```

#### Graph Representations

```c
// Adjacency Matrix - O(V^2) space
int graph[V][V];

// Adjacency List - O(V+E) space
struct AdjListNode {
    int dest;
    struct AdjListNode *next;
};

struct AdjList {
    struct AdjListNode *head;
};

struct Graph {
    int V;
    struct AdjList *array;
};
```

#### Asymptotic Analysis

| Notation | Definition | Use |
|----------|-----------|-----|
| $O$ (Big-O) | $f(n) \leq c \cdot g(n)$ for $n \geq n_0$ | Upper bound (worst case) |
| $\Omega$ (Big-Omega) | $f(n) \geq c \cdot g(n)$ for $n \geq n_0$ | Lower bound (best case) |
| $\Theta$ (Big-Theta) | $c_1 g(n) \leq f(n) \leq c_2 g(n)$ | Tight bound |
| $o$ (Little-o) | $f(n) < c \cdot g(n)$ | Strictly upper bound |
| $\omega$ (Little-omega) | $f(n) > c \cdot g(n)$ | Strictly lower bound |

#### Master Theorem

For recurrences of form $T(n) = aT(n/b) + f(n)$ where $a \geq 1$, $b > 1$:

1. If $f(n) = O(n^{\log_b a - \epsilon})$ for $\epsilon > 0$, then $T(n) = \Theta(n^{\log_b a})$
2. If $f(n) = \Theta(n^{\log_b a})$, then $T(n) = \Theta(n^{\log_b a} \log n)$
3. If $f(n) = \Omega(n^{\log_b a + \epsilon})$ for $\epsilon > 0$ AND $af(n/b) \leq cf(n)$ for $c < 1$, then $T(n) = \Theta(f(n))$

**Examples:**
- Merge Sort: $T(n) = 2T(n/2) + O(n)$ → Case 2 → $T(n) = O(n \log n)$
- Binary Search: $T(n) = T(n/2) + O(1)$ → Case 2 → $T(n) = O(\log n)$
- Strassen: $T(n) = 7T(n/2) + O(n^2)$ → Case 1 → $T(n) = O(n^{\log_2 7}) \approx O(n^{2.81})$

#### Greedy Algorithms

```c
// Activity Selection Problem
// Select maximum activities that don't overlap
void activitySelection(int start[], int finish[], int n) {
    // Sort by finish time
    int i = 0;  // First activity always selected
    printf("%d ", i);
    
    for (int j = 1; j < n; j++) {
        if (start[j] >= finish[i]) {
            printf("%d ", j);
            i = j;
        }
    }
}
// Time: O(n log n), Space: O(1)
```

#### Dynamic Programming

```c
// 0/1 Knapsack Problem
int knapsack(int W, int wt[], int val[], int n) {
    int dp[n+1][W+1];
    
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0)
                dp[i][w] = 0;
            else if (wt[i-1] <= w)
                dp[i][w] = max(val[i-1] + dp[i-1][w-wt[i-1]], dp[i-1][w]);
            else
                dp[i][w] = dp[i-1][w];
        }
    }
    return dp[n][W];
}
// Time: O(nW), Space: O(nW)
```

#### Divide and Conquer

```c
// Merge Sort
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1, n2 = r - m;
    int L[n1], R[n2];
    
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
// Time: O(n log n), Space: O(n)
```

#### Graph Algorithms

```c
// BFS - O(V+E)
void BFS(struct Graph *graph, int start) {
    int visited[V] = {0};
    int queue[V], front = 0, rear = 0;
    
    visited[start] = 1;
    queue[rear++] = start;
    
    while (front < rear) {
        int v = queue[front++];
        printf("%d ", v);
        
        struct AdjListNode *temp = graph->array[v].head;
        while (temp) {
            if (!visited[temp->dest]) {
                visited[temp->dest] = 1;
                queue[rear++] = temp->dest;
            }
            temp = temp->next;
        }
    }
}

// DFS - O(V+E)
void DFS(struct Graph *graph, int v, int visited[]) {
    visited[v] = 1;
    printf("%d ", v);
    
    struct AdjListNode *temp = graph->array[v].head;
    while (temp) {
        if (!visited[temp->dest])
            DFS(graph, temp->dest, visited);
        temp = temp->next;
    }
}
```

#### Hashing

```c
// Hash table with chaining
#define TABLE_SIZE 11

struct HashNode {
    int key, value;
    struct HashNode *next;
};

int hash(int key) {
    return key % TABLE_SIZE;
}

void insert(struct HashNode *table[], int key, int value) {
    int index = hash(key);
    struct HashNode *new = malloc(sizeof(struct HashNode));
    new->key = key;
    new->value = value;
    new->next = table[index];
    table[index] = new;
}
```

---

## 3. Internal Working

### 3.1 How Arrays Work Internally

Arrays are **contiguous memory blocks**. For an array `arr` of size $n$ with base address $B$ and element size $s$:

$$\text{Address of } arr[i] = B + i \cdot s$$

**Key Properties:**
- Random access: $O(1)$ via index
- Insertion/Deletion: $O(n)$ (shifting required)
- Cache friendly (spatial locality)

### 3.2 How Pointers Work

A pointer stores a **memory address**. For `int *p = &a`:

```
Variable    Address     Value
a           0x1000      42
p           0x1008      0x1000
```

**Pointer Arithmetic:**
- `p + 1` adds `sizeof(int)` bytes (typically 4)
- `p - q` gives number of elements between pointers

### 3.3 How Recursion Works (Call Stack)

Each recursive call creates a **stack frame** containing:
- Local variables
- Parameters
- Return address

```
factorial(3)
├── factorial(2)
│   ├── factorial(1)
│   │   └── returns 1
│   └── returns 2 * 1 = 2
└── returns 3 * 2 = 6
```

**Stack Overflow:** Occurs when recursion depth exceeds stack size (typically ~8MB on Linux).

### 3.4 How Linked Lists Work

```
Singly Linked List:
[Data|Next] -> [Data|Next] -> [Data|Next] -> NULL
  0x1000       0x1010       0x1020

Doubly Linked List:
NULL <- [Prev|Data|Next] <-> [Prev|Data|Next] -> NULL
```

**Memory:** Nodes scattered in heap, connected by pointers. No cache locality.

### 3.5 How Stacks Work (LIFO)

```
Push 10:  [10]
Push 20:  [10, 20]
Push 30:  [10, 20, 30]
Pop:      [10, 20]     → returns 30
```

**Applications:** Function calls, expression evaluation, undo operations, backtracking.

### 3.6 How Queues Work (FIFO)

```
Enqueue 10:  [10]
Enqueue 20:  [10, 20]
Enqueue 30:  [10, 20, 30]
Dequeue:     [20, 30]    → returns 10
```

**Applications:** BFS, scheduling, buffering, print spooling.

### 3.7 How Trees Work

**Binary Tree Properties:**
- Max nodes at level $l$: $2^l$
- Max nodes in tree of height $h$: $2^{h+1} - 1$
- Height of tree with $n$ nodes: $\lfloor \log_2 n \rfloor$ (balanced) to $n-1$ (skewed)

**BST Property:** For every node $x$:
- All keys in left subtree $< x.key$
- All keys in right subtree $> x.key$

### 3.8 How Heaps Work

**Min-Heap Array Representation:**
```
Index:    0  1  2  3  4  5  6
Value:    1  3  2  7  5  4  6

Tree view:
        1
      /   \
     3     2
    / \   / \
   7   5 4   6

Parent(i) = (i-1)/2
Left(i)   = 2i + 1
Right(i)  = 2i + 2
```

**Heapify:** $O(\log n)$ — bubble down from root to leaf.

### 3.9 How Hash Tables Work

**Hash Function:** Maps keys to indices in $[0, m-1]$.

**Collision Resolution:**
1. **Chaining:** Each bucket is a linked list
2. **Open Addressing:**
   - Linear probing: $h(k, i) = (h'(k) + i) \mod m$
   - Quadratic probing: $h(k, i) = (h'(k) + c_1i + c_2i^2) \mod m$
   - Double hashing: $h(k, i) = (h_1(k) + i \cdot h_2(k)) \mod m$

**Load Factor:** $\alpha = n/m$ where $n$ = elements, $m$ = table size.

### 3.10 How Graphs Work Internally

**Adjacency Matrix:**
```
    0  1  2  3
0 [ 0  1  0  1 ]
1 [ 1  0  1  0 ]
2 [ 0  1  0  1 ]
3 [ 1  0  1  0 ]
```
- Space: $O(V^2)$
- Edge lookup: $O(1)$
- Find all neighbors: $O(V)$

**Adjacency List:**
```
0: [1, 3]
1: [0, 2]
2: [1, 3]
3: [0, 2]
```
- Space: $O(V + E)$
- Edge lookup: $O(\text{degree})$
- Find all neighbors: $O(\text{degree})$

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Algorithm** | Finite sequence of well-defined instructions to solve a problem |
| **Data Structure** | A way of organizing and storing data for efficient access and modification |
| **Abstract Data Type (ADT)** | Mathematical model of data structure (what operations, not how) |
| **Time Complexity** | Growth rate of algorithm's running time with input size |
| **Space Complexity** | Growth rate of algorithm's memory usage with input size |
| **Asymptotic Analysis** | Mathematical framework for analyzing algorithm efficiency |
| **Recursion** | Function calling itself to solve smaller subproblems |
| **Base Case** | Condition that stops recursion |
| **Stack Frame** | Memory block for function call containing local variables |
| **Pointer** | Variable storing memory address |
| **Dynamic Memory** | Heap-allocated memory (malloc, free) |
| **Contiguous Memory** | Adjacent memory locations (arrays) |
| **Node** | Basic unit of linked data structures containing data and pointer(s) |
| **Edge** | Connection between two vertices in a graph |
| **Vertex (Node)** | Fundamental unit of a graph |
| **Degree** | Number of edges incident to a vertex |
| **Path** | Sequence of vertices connected by edges |
| **Cycle** | Path that starts and ends at same vertex |
| **Connected Graph** | Graph with path between every pair of vertices |
| **Tree** | Connected acyclic graph |
| **Binary Tree** | Tree where each node has at most 2 children |
| **BST** | Binary tree with ordering property (left < root < right) |
| **Heap** | Complete binary tree satisfying heap property |
| **Hash Function** | Maps keys to array indices |
| **Collision** | When two keys hash to same index |
| **Load Factor** | Ratio of elements to table size in hash table |
| **Greedy Algorithm** | Makes locally optimal choice at each step |
| **Dynamic Programming** | Breaks problem into overlapping subproblems, stores results |
| **Divide and Conquer** | Divides problem into independent subproblems, combines results |
| **Optimal Substructure** | Optimal solution contains optimal solutions to subproblems |
| **Overlapping Subproblems** | Subproblems recur multiple times |
| **BFS** | Breadth-First Search (level-order traversal) |
| **DFS** | Depth-First Search (go deep before wide) |
| **MST** | Minimum Spanning Tree (minimum weight spanning tree) |
| **Shortest Path** | Path with minimum total weight between vertices |
| **Topological Sort** | Linear ordering of vertices in DAG |
| **AVL Tree** | Self-balancing BST with height difference ≤ 1 |
| **Red-Black Tree** | Self-balancing BST with color properties |
| **B-Tree** | Balanced search tree optimized for disk access |
| **Trie** | Tree for efficient string storage and retrieval |

---

## 5. Beginner Examples

### Example 1: Linear Search (C)

**Problem:** Find position of element `x` in array `arr` of size `n`.

```c
int linearSearch(int arr[], int n, int x) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == x)
            return i;       // Found at index i
    }
    return -1;              // Not found
}
```

**Analysis:**
- Time: $O(n)$ worst case, $O(1)$ best case
- Space: $O(1)$
- Works on unsorted arrays

**GATE Tip:** Linear search is the baseline. Always ask: "Is the array sorted?" If yes, use binary search.

---

### Example 2: Factorial Using Recursion (C)

**Problem:** Compute $n! = n \times (n-1) \times \cdots \times 1$.

```c
int factorial(int n) {
    // Base case
    if (n == 0 || n == 1)
        return 1;
    // Recursive case
    return n * factorial(n - 1);
}
```

**Trace for `factorial(4)`:**
```
factorial(4) = 4 * factorial(3)
             = 4 * 3 * factorial(2)
             = 4 * 3 * 2 * factorial(1)
             = 4 * 3 * 2 * 1
             = 24
```

**Analysis:**
- Time: $O(n)$ — n multiplications
- Space: $O(n)$ — call stack depth

**GATE Tip:** Always identify base case first. Without it → infinite recursion → stack overflow.

---

### Example 3: Stack Using Array (C)

**Problem:** Implement stack with push, pop, peek operations.

```c
#define MAX 100
int stack[MAX], top = -1;

void push(int x) {
    if (top >= MAX - 1) {
        printf("Stack Overflow\n");
        return;
    }
    stack[++top] = x;
}

int pop() {
    if (top < 0) {
        printf("Stack Underflow\n");
        return -1;
    }
    return stack[top--];
}

int peek() {
    if (top < 0) return -1;
    return stack[top];
}

int isEmpty() {
    return top == -1;
}
```

**Analysis:**
- Push: $O(1)$
- Pop: $O(1)$
- Peek: $O(1)$
- Space: $O(MAX)$

**GATE Tip:** Check overflow before push, underflow before pop.

---

### Example 4: Python List Operations

**Problem:** Demonstrate basic Python data structure operations.

```python
# List (Dynamic Array)
arr = [1, 2, 3, 4, 5]
arr.append(6)        # O(1) amortized
arr.insert(0, 0)     # O(n)
arr.pop()            # O(1)
arr.pop(0)           # O(n)

# Stack using list
stack = []
stack.append(10)     # Push
stack.append(20)
top = stack[-1]      # Peek
item = stack.pop()   # Pop

# Queue using deque
from collections import deque
queue = deque()
queue.append(10)     # Enqueue
queue.append(20)
item = queue.popleft()  # Dequeue

# Dictionary (Hash Table)
d = {"a": 1, "b": 2}
d["c"] = 3           # Insert
val = d.get("a")     # Lookup: O(1) average
del d["b"]           # Delete
```

**GATE Tip:** Python lists are dynamic arrays. `append` is $O(1)$ amortized, `insert(0, x)` is $O(n)$.

---

### Example 5: Bubble Sort (C)

**Problem:** Sort array in ascending order using bubble sort.

```c
void bubbleSort(int arr[], int n) {
    for (int i = 0; i < n - 1; i++) {
        int swapped = 0;
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                // Swap adjacent elements
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
                swapped = 1;
            }
        }
        // Optimization: already sorted
        if (!swapped) break;
    }
}
```

**Trace for `[5, 3, 8, 1]`:**
```
Pass 1: [3, 5, 1, 8]
Pass 2: [3, 1, 5, 8]
Pass 3: [1, 3, 5, 8]
```

**Analysis:**
- Time: $O(n^2)$ worst/average, $O(n)$ best (already sorted with optimization)
- Space: $O(1)$
- Stable: Yes (equal elements maintain relative order)

**GATE Tip:** Bubble sort is rarely used in practice but important for understanding sorting concepts.

---

## 6. Intermediate Examples

### Example 1: Binary Search (C)

**Problem:** Find position of `x` in **sorted** array.

```c
// Iterative Binary Search
int binarySearch(int arr[], int n, int x) {
    int low = 0, high = n - 1;
    
    while (low <= high) {
        int mid = low + (high - low) / 2;  // Avoid overflow
        
        if (arr[mid] == x)
            return mid;
        else if (arr[mid] < x)
            low = mid + 1;
        else
            high = mid - 1;
    }
    return -1;
}

// Recursive Binary Search
int binarySearchRec(int arr[], int low, int high, int x) {
    if (low > high) return -1;
    
    int mid = low + (high - low) / 2;
    
    if (arr[mid] == x) return mid;
    if (arr[mid] < x)
        return binarySearchRec(arr, mid + 1, high, x);
    return binarySearchRec(arr, low, mid - 1, x);
}
```

**Analysis:**
- Time: $O(\log n)$
- Space: $O(1)$ iterative, $O(\log n)$ recursive (call stack)
- Requires sorted array

**GATE Tip:** Use `mid = low + (high - low) / 2` instead of `(low + high) / 2` to prevent integer overflow.

---

### Example 2: Linked List Reversal (C)

**Problem:** Reverse a singly linked list.

```c
struct Node* reverse(struct Node *head) {
    struct Node *prev = NULL, *current = head, *next = NULL;
    
    while (current != NULL) {
        next = current->next;    // Store next
        current->next = prev;    // Reverse pointer
        prev = current;          // Move prev forward
        current = next;          // Move current forward
    }
    return prev;  // New head
}
```

**Trace:**
```
Original: 1 -> 2 -> 3 -> 4 -> NULL

Step 1: NULL <- 1    2 -> 3 -> 4 -> NULL
Step 2: NULL <- 1 <- 2    3 -> 4 -> NULL
Step 3: NULL <- 1 <- 2 <- 3    4 -> NULL
Step 4: NULL <- 1 <- 2 <- 3 <- 4

Result: 4 -> 3 -> 2 -> 1 -> NULL
```

**Analysis:**
- Time: $O(n)$
- Space: $O(1)$

**GATE Tip:** Draw the pointers. Always save `next` before modifying `current->next`.

---

### Example 3: Infix to Postfix Conversion (C)

**Problem:** Convert `A + B * C - D` to postfix.

```c
// Using stack
char* infixToPostfix(char *exp) {
    char stack[MAX];
    int top = -1;
    char *postfix = malloc(MAX);
    int j = 0;
    
    for (int i = 0; exp[i]; i++) {
        char c = exp[i];
        
        if (isalnum(c)) {
            postfix[j++] = c;           // Operand → output
        } else if (c == '(') {
            stack[++top] = c;           // Push '('
        } else if (c == ')') {
            while (top >= 0 && stack[top] != '(')
                postfix[j++] = stack[top--];  // Pop until '('
            top--;                       // Discard '('
        } else {                         // Operator
            while (top >= 0 && precedence(stack[top]) >= precedence(c))
                postfix[j++] = stack[top--];
            stack[++top] = c;
        }
    }
    while (top >= 0)
        postfix[j++] = stack[top--];
    postfix[j] = '\0';
    return postfix;
}
```

**Trace for `A + B * C`:**
```
Symbol | Stack | Output
A             |       | A
+             | +     | A
B             | +     | AB
*             | +*    | AB
C             | +*    | ABC
(end)         | +     | ABC*
              |       | ABC*+
```

**Result:** `ABC*+`

**GATE Tip:** Operator precedence: `^` > `*,/` > `+,-`. Associativity matters for `^` (right-to-left).

---

### Example 4: Queue Using Two Stacks (Python)

**Problem:** Implement queue using two stacks.

```python
class QueueUsingStacks:
    def __init__(self):
        self.stack1 = []  # For enqueue
        self.stack2 = []  # For dequeue
    
    def enqueue(self, x):
        self.stack1.append(x)  # O(1)
    
    def dequeue(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        if not self.stack2:
            return None  # Queue empty
        return self.stack2.pop()  # Amortized O(1)
    
    def peek(self):
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        if not self.stack2:
            return None
        return self.stack2[-1]
```

**Analysis:**
- Enqueue: $O(1)$
- Dequeue: Amortized $O(1)$, worst $O(n)$
- Each element moved at most twice (stack1 → stack2 → popped)

**GATE Tip:** Amortized analysis — expensive operations are rare, so average cost is low.

---

### Example 5: Merge Sort (C)

**Problem:** Sort array using merge sort (divide and conquer).

```c
void merge(int arr[], int l, int m, int r) {
    int n1 = m - l + 1, n2 = r - m;
    int L[n1], R[n2];
    
    for (int i = 0; i < n1; i++) L[i] = arr[l + i];
    for (int j = 0; j < n2; j++) R[j] = arr[m + 1 + j];
    
    int i = 0, j = 0, k = l;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) arr[k++] = L[i++];
        else arr[k++] = R[j++];
    }
    while (i < n1) arr[k++] = L[i++];
    while (j < n2) arr[k++] = R[j++];
}

void mergeSort(int arr[], int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}
```

**Recurrence:** $T(n) = 2T(n/2) + O(n)$

**Analysis:**
- Time: $O(n \log n)$ — all cases
- Space: $O(n)$ — auxiliary array
- Stable: Yes

**GATE Tip:** Merge sort is the go-to example for divide-and-conquer. Always mention it's stable and has guaranteed $O(n \log n)$.

---

## 7. Advanced Examples

### Example 1: Dijkstra's Shortest Path Algorithm

**Problem:** Find shortest path from source to all vertices in weighted graph.

```c
#define V 9
#define INF 999999

int minDistance(int dist[], int visited[]) {
    int min = INF, min_index;
    for (int v = 0; v < V; v++)
        if (!visited[v] && dist[v] <= min)
            min = dist[v], min_index = v;
    return min_index;
}

void dijkstra(int graph[V][V], int src) {
    int dist[V], visited[V];
    
    for (int i = 0; i < V; i++)
        dist[i] = INF, visited[i] = 0;
    dist[src] = 0;
    
    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(dist, visited);
        visited[u] = 1;
        
        for (int v = 0; v < V; v++)
            if (!visited[v] && graph[u][v] && dist[u] != INF
                && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }
}
```

**Analysis:**
- Time: $O(V^2)$ with array, $O((V+E) \log V)$ with min-heap
- Space: $O(V)$
- Works only for non-negative weights

**GATE Tip:** Dijkstra fails with negative edges. Use Bellman-Ford for negative weights.

---

### Example 2: 0/1 Knapsack (Dynamic Programming)

**Problem:** Given weights and values, find max value fitting in capacity $W$.

```c
int knapsack(int W, int wt[], int val[], int n) {
    int dp[n + 1][W + 1];
    
    for (int i = 0; i <= n; i++) {
        for (int w = 0; w <= W; w++) {
            if (i == 0 || w == 0)
                dp[i][w] = 0;
            else if (wt[i - 1] <= w)
                dp[i][w] = max(val[i - 1] + dp[i - 1][w - wt[i - 1]],
                                dp[i - 1][w]);
            else
                dp[i][w] = dp[i - 1][w];
        }
    }
    return dp[n][W];
}
```

**DP Table for W=5, wt=[1,2,3], val=[6,10,12]:**
```
      w=0  w=1  w=2  w=3  w=4  w=5
i=0  [  0,   0,   0,   0,   0,   0]
i=1  [  0,   6,   6,   6,   6,   6]
i=2  [  0,   6,  10,  16,  16,  16]
i=3  [  0,   6,  10,  16,  16,  18]
```

**Answer:** 18 (items 1 and 3: weight 1+3=4, value 6+12=18)

**Analysis:**
- Time: $O(nW)$
- Space: $O(nW)$
- Pseudo-polynomial (depends on W, not just n)

**GATE Tip:** 0/1 knapsack is classic DP. Fractional knapsack uses greedy (sort by value/weight ratio).

---

### Example 3: Kruskal's MST Algorithm

**Problem:** Find Minimum Spanning Tree using Kruskal's algorithm.

```c
// Union-Find (Disjoint Set) data structure
int find(int parent[], int i) {
    if (parent[i] == i)
        return i;
    return find(parent, parent[i]);  // Path compression
}

void unionSet(int parent[], int rank[], int x, int y) {
    int xroot = find(parent, x);
    int yroot = find(parent, y);
    
    if (rank[xroot] < rank[yroot])
        parent[xroot] = yroot;
    else if (rank[xroot] > rank[yroot])
        parent[yroot] = xroot;
    else {
        parent[yroot] = xroot;
        rank[xroot]++;
    }
}

// Kruskal's algorithm
void kruskalMST(struct Graph *graph) {
    int V = graph->V;
    struct Edge result[V];
    int e = 0, i = 0;
    
    // Sort edges by weight - O(E log E)
    qsort(graph->edge, graph->E, sizeof(struct Edge), compareEdges);
    
    int parent[V], rank[V];
    for (int v = 0; v < V; v++) {
        parent[v] = v;
        rank[v] = 0;
    }
    
    while (e < V - 1 && i < graph->E) {
        struct Edge next = graph->edge[i++];
        
        int x = find(parent, next.src);
        int y = find(parent, next.dest);
        
        if (x != y) {  // No cycle
            result[e++] = next;
            unionSet(parent, rank, x, y);
        }
    }
}
```

**Analysis:**
- Time: $O(E \log E)$ or $O(E \log V)$ — dominated by sorting
- Space: $O(V)$ for union-find
- Greedy approach: always pick minimum weight edge

**GATE Tip:** Kruskal's uses union-find. Prim's uses priority queue. Both find MST but differently.

---

### Example 4: Longest Common Subsequence (DP)

**Problem:** Find length of longest common subsequence of two strings.

```c
int lcs(char *X, char *Y, int m, int n) {
    int dp[m + 1][n + 1];
    
    for (int i = 0; i <= m; i++) {
        for (int j = 0; j <= n; j++) {
            if (i == 0 || j == 0)
                dp[i][j] = 0;
            else if (X[i - 1] == Y[j - 1])
                dp[i][j] = dp[i - 1][j - 1] + 1;
            else
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
        }
    }
    return dp[m][n];
}
```

**DP Table for X="ABCBDAB", Y="BDCAB":**
```
      ""  B  D  C  A  B
""  [ 0, 0, 0, 0, 0, 0]
A   [ 0, 0, 0, 0, 1, 1]
B   [ 0, 1, 1, 1, 1, 2]
C   [ 0, 1, 1, 2, 2, 2]
B   [ 0, 1, 1, 2, 2, 3]
D   [ 0, 1, 2, 2, 2, 3]
A   [ 0, 1, 2, 2, 3, 3]
B   [ 0, 1, 2, 2, 3, 4]
```

**Answer:** 4 (LCS = "BCAB" or "BDAB")

**Analysis:**
- Time: $O(mn)$
- Space: $O(mn)$, can be optimized to $O(\min(m,n))$

**GATE Tip:** LCS is classic 2D DP. Edit distance is a variation (insert, delete, replace operations).

---

### Example 5: Quick Sort with Partition

**Problem:** Sort array using quick sort (in-place, divide and conquer).

```c
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Last element as pivot
    int i = low - 1;        // Index of smaller element
    
    for (int j = low; j < high; j++) {
        if (arr[j] <= pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}
```

**Trace for `[10, 80, 30, 90, 40, 50, 70]`:**
```
Partition (pivot=70): [10, 30, 40, 50, 70, 90, 80]
                      pi=4
Left:  [10, 30, 40, 50] → sorted: [10, 30, 40, 50]
Right: [90, 80] → sorted: [80, 90]
Result: [10, 30, 40, 50, 70, 80, 90]
```

**Analysis:**
- Time: $O(n \log n)$ average, $O(n^2)$ worst (already sorted with bad pivot)
- Space: $O(log n)$ average (recursion stack)
- Not stable

**GATE Tip:** Randomized quicksort avoids worst-case. Median-of-three pivot selection helps.

---

## 8. How Interviewers Think

### 8.1 Red Flags (What Interviewers Hate)

| Red Flag | Why It's Bad |
|----------|-------------|
| **Jumping to code without clarifying** | Shows poor communication, may solve wrong problem |
| **Ignoring edge cases** | Empty input, single element, duplicates, overflow |
| **Memorized solutions without understanding** | Can't adapt to variations |
| **Not analyzing complexity** | Can't evaluate solution quality |
| **Bad variable names** | `x`, `y`, `temp` everywhere — unreadable code |
| **No test cases** | Can't verify correctness |
| **Giving up too easily** | No problem-solving persistence |
| **Overcomplicating simple solutions** | Using DP when greedy works |

### 8.2 Green Flags (What Interviewers Love)

| Green Flag | Why It's Good |
|------------|--------------|
| **Clarifying questions first** | Shows thoroughness |
| **Starting with brute force** | Establishes baseline, shows thinking |
| **Optimizing step by step** | Demonstrates analytical ability |
| **Discussing trade-offs** | Space vs time, readability vs performance |
| **Writing clean, modular code** | Professional coding practices |
| **Testing with examples** | Verifies correctness |
| **Handling edge cases** | Robust solution |
| **Explaining while coding** | Communication skills |

### 8.3 Answer Matrix: How to Structure Responses

| Phase | What to Do | Time |
|-------|-----------|------|
| **1. Understand** | Clarify input, output, constraints | 1-2 min |
| **2. Examples** | Work through 2-3 examples manually | 2-3 min |
| **3. Brute Force** | State naive solution first | 1-2 min |
| **4. Optimize** | Identify bottlenecks, improve | 3-5 min |
| **5. Code** | Write clean, modular code | 5-10 min |
| **6. Test** | Walk through with examples | 2-3 min |
| **7. Analyze** | State time and space complexity | 1 min |

### 8.4 GATE-Specific Interview Patterns

**Pattern 1: "Find the Output"**
- Given code snippet, predict output
- Focus: operator precedence, short-circuit evaluation, pointer arithmetic

**Pattern 2: "Find the Error"**
- Code has a bug (off-by-one, memory leak, null dereference)
- Focus: boundary conditions, edge cases

**Pattern 3: "What's the Complexity"**
- Given algorithm, find time/space complexity
- Focus: loop analysis, recurrence relations

**Pattern 4: "Complete the Code"**
- Fill in missing function/condition
- Focus: understanding of standard algorithms

---

## 9. FAQs

### Conceptual FAQs (1-20)

**Q1: What's the difference between array and linked list?**
- Array: contiguous memory, $O(1)$ access, $O(n)$ insert/delete
- Linked list: scattered memory, $O(n)$ access, $O(1)$ insert/delete at known position

**Q2: When to use BFS vs DFS?**
- BFS: shortest path in unweighted graph, level-order traversal
- DFS: cycle detection, topological sort, exploring all paths

**Q3: What makes a problem suitable for DP?**
- Optimal substructure + overlapping subproblems
- Can be broken into smaller, reusable subproblems

**Q4: Why is merge sort $O(n \log n)$?**
- Recurrence: $T(n) = 2T(n/2) + O(n)$
- Master Theorem Case 2: $T(n) = O(n \log n)$

**Q5: What's the difference between stack and queue?**
- Stack: LIFO (Last In First Out)
- Queue: FIFO (First In First Out)

**Q6: Why use heaps for priority queues?**
- Insert: $O(\log n)$, Extract-min/max: $O(\log n)$
- More efficient than sorted array for dynamic operations

**Q7: What's the difference between BST and hash table?**
- BST: ordered, $O(\log n)$ operations (balanced), supports range queries
- Hash table: unordered, $O(1)$ average, no ordering

**Q8: What's amortized analysis?**
- Average cost over sequence of operations
- Example: dynamic array resize — expensive but rare

**Q9: Why is quicksort faster than merge sort in practice?**
- Better cache locality, in-place (less memory), smaller constant factors
- Despite same $O(n \log n)$ average complexity

**Q10: What's the difference between greedy and DP?**
- Greedy: makes irrevocable locally optimal choices
- DP: explores all possibilities, stores results

**Q11: What's a collision in hashing?**
- When two keys map to same index
- Resolved by chaining or open addressing

**Q12: What's the difference between tree and graph?**
- Tree: connected, acyclic graph with $n-1$ edges
- Graph: general structure, may have cycles

**Q13: What's the Master Theorem used for?**
- Solving recurrence relations of form $T(n) = aT(n/b) + f(n)$
- Common in divide-and-conquer analysis

**Q14: What's the difference between $O$ and $o$?**
- $O$: upper bound (≤), $o$: strict upper bound (<)
- $f(n) = O(f(n))$ is true, $f(n) = o(f(n))$ is false

**Q15: What's tail recursion?**
- Recursive call is the last operation
- Can be optimized to iteration by compiler

**Q16: What's the difference between Prim's and Kruskal's?**
- Prim's: grows MST from a vertex, uses priority queue
- Kruskal's: adds edges in order of weight, uses union-find

**Q17: What's the difference between BFS and Dijkstra's?**
- BFS: unweighted graphs, uses queue
- Dijkstra's: weighted graphs, uses priority queue

**Q18: What's a spanning tree?**
- Subgraph that's a tree, includes all vertices
- MST: spanning tree with minimum total weight

**Q19: What's the difference between stable and unstable sort?**
- Stable: equal elements maintain relative order
- Unstable: may change order of equal elements

**Q20: What's the difference between heap and BST?**
- Heap: parent-child ordering only, array representation
- BST: left-right ordering, pointer-based

---

### Scenario-Based FAQs (21-40)

**Q21: You need to implement undo functionality. Which data structure?**
- **Stack** — LIFO matches undo behavior (last action undone first)

**Q22: You need to schedule print jobs. Which data structure?**
- **Queue** — FIFO ensures fair scheduling (first request served first)

**Q23: You need to find if a word exists in a dictionary. Which data structure?**
- **Hash table** — $O(1)$ average lookup, or **Trie** for prefix searches

**Q24: You need to find the shortest route between cities. Which algorithm?**
- **Dijkstra's** — single-source shortest path with non-negative weights

**Q25: You need to detect a cycle in a directed graph. Which algorithm?**
- **DFS with recursion stack** — if we revisit a node in current recursion stack, cycle exists

**Q26: You need to sort a nearly sorted array. Which algorithm?**
- **Insertion sort** — $O(n)$ for nearly sorted, adaptive

**Q27: You need to find the median of a stream of numbers. Which data structure?**
- **Two heaps** — max-heap for lower half, min-heap for upper half

**Q28: You need to implement a cache (LRU). Which data structure?**
- **Hash map + doubly linked list** — $O(1)$ lookup and $O(1)$ update

**Q29: You need to find all anagrams in a string. Which technique?**
- **Sliding window + hash map** — compare character frequencies

**Q30: You need to find the majority element (> n/2 occurrences). Which algorithm?**
- **Boyer-Moore Voting** — $O(n)$ time, $O(1)$ space

**Q31: You need to find if two strings are anagrams. Which approach?**
- **Sort and compare** — $O(n \log n)$, or **character count** — $O(n)$

**Q32: You need to find the kth largest element. Which approach?**
- **Min-heap of size k** — $O(n \log k)$, or **Quickselect** — $O(n)$ average

**Q33: You need to implement a browser's back/forward. Which data structure?**
- **Two stacks** — one for back history, one for forward history

**Q34: You need to find the longest palindromic substring. Which approach?**
- **Expand around center** — $O(n^2)$, or **Manacher's algorithm** — $O(n)$

**Q35: You need to find if a linked list has a cycle. Which algorithm?**
- **Floyd's Cycle Detection** — slow/fast pointers, $O(n)$ time, $O(1)$ space

**Q36: You need to evaluate a postfix expression. Which data structure?**
- **Stack** — push operands, pop two when operator encountered

**Q37: You need to find the minimum window substring. Which technique?**
- **Sliding window with two pointers** — expand and contract window

**Q38: You need to serialize/deserialize a binary tree. Which traversal?**
- **Level-order (BFS)** — preserves structure with null markers

**Q39: You need to find the intersection of two sorted arrays. Which approach?**
- **Two pointers** — $O(n + m)$ time, $O(1)$ extra space

**Q40: You need to implement a task scheduler with cooldown. Which approach?**
- **Greedy with priority queue** — schedule most frequent tasks first

---

## 10. Common Mistakes

### 10.1 C Programming Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| `int mid = (low + high) / 2` (overflow) | `int mid = low + (high - low) / 2` |
| Forgetting to free `malloc`'d memory | Always `free` after use |
| Using `=` instead of `==` in conditions | Double-check comparisons |
| Not checking `malloc` return for NULL | Always verify allocation |
| Array index out of bounds | Check `0 <= index < size` |
| Modifying string literal | Use `char[]` not `char*` for mutable strings |
| Uninitialized pointers | Initialize to NULL or valid address |
| Buffer overflow in `strcpy` | Use `strncpy` or check lengths |

### 10.2 Data Structure Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Forgetting to update `head` after deletion | Always reassign `head` if first node removed |
| Not handling empty stack/queue | Check `isEmpty()` before pop/dequeue |
| Off-by-one in linked list traversal | Use `while (current != NULL)` not `while (current->next != NULL)` |
| Forgetting to set `next` to NULL for new nodes | Always initialize pointers |
| Not handling single-node edge cases | Test with n=0, n=1, n=2 |
| Confusing pre-order with post-order | Pre: root first, Post: root last |

### 10.3 Algorithm Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Wrong base case in recursion | Verify with smallest input |
| Not sorting before binary search | Binary search requires sorted array |
| Using Dijkstra with negative weights | Use Bellman-Ford instead |
| Not considering worst-case in quicksort | Mention $O(n^2)$ worst case |
| Forgetting to mark visited in graph | Always mark visited to avoid infinite loops |
| Not handling duplicate elements | Clarify if duplicates allowed |
| Greedy when DP needed | Check if greedy choice property holds |

### 10.4 Complexity Analysis Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Saying binary search is $O(n)$ | It's $O(\log n)$ |
| Ignoring space complexity | Always state both time and space |
| Confusing average and worst case | Specify which you're analyzing |
| Not simplifying $O(2n)$ to $O(n)$ | Drop constants in Big-O |
| Saying $O(n^2)$ is better than $O(n \log n)$ | $O(n \log n)$ is better for large n |

---

## 11. Comparison Tables

### 11.1 Search Algorithms

| Algorithm | Time (Best) | Time (Avg) | Time (Worst) | Space | Requires Sorted |
|-----------|-------------|------------|--------------|-------|-----------------|
| Linear Search | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | No |
| Binary Search | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | Yes |
| Hash Lookup | $O(1)$ | $O(1)$ | $O(n)$ | $O(n)$ | No |
| BST Search | $O(1)$ | $O(\log n)$ | $O(n)$ | $O(1)$ | N/A |

### 11.2 Sorting Algorithms

| Algorithm | Best | Average | Worst | Space | Stable | In-Place |
|-----------|------|---------|-------|-------|--------|----------|
| Bubble Sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| Selection Sort | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Yes |
| Insertion Sort | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| Merge Sort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | Yes | No |
| Quick Sort | $O(n \log n)$ | $O(n \log n)$ | $O(n^2)$ | $O(\log n)$ | No | Yes |
| Heap Sort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ | No | Yes |
| Counting Sort | $O(n+k)$ | $O(n+k)$ | $O(n+k)$ | $O(k)$ | Yes | No |
| Radix Sort | $O(nk)$ | $O(nk)$ | $O(nk)$ | $O(n+k)$ | Yes | No |

### 11.3 Data Structure Operations

| Data Structure | Access | Search | Insert | Delete | Space |
|----------------|--------|--------|--------|--------|-------|
| Array | $O(1)$ | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| Sorted Array | $O(1)$ | $O(\log n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| Stack | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| Queue | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| Singly Linked List | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| Doubly Linked List | $O(n)$ | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| BST | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Balanced BST | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Hash Table | N/A | $O(1)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| Min-Heap | $O(n)$ | $O(n)$ | $O(\log n)$ | $O(\log n)$ | $O(n)$ |

### 11.4 Graph Algorithms

| Algorithm | Problem | Time | Space | Notes |
|-----------|---------|------|-------|-------|
| BFS | Shortest path (unweighted) | $O(V+E)$ | $O(V)$ | Uses queue |
| DFS | Traversal, cycle detection | $O(V+E)$ | $O(V)$ | Uses stack/recursion |
| Dijkstra | Shortest path (weighted) | $O((V+E)\log V)$ | $O(V)$ | Non-negative weights |
| Bellman-Ford | Shortest path (negative) | $O(VE)$ | $O(V)$ | Detects negative cycles |
| Floyd-Warshall | All-pairs shortest path | $O(V^3)$ | $O(V^2)$ | DP approach |
| Kruskal | MST | $O(E \log E)$ | $O(V)$ | Union-find |
| Prim | MST | $O((V+E)\log V)$ | $O(V)$ | Priority queue |
| Topological Sort | Ordering in DAG | $O(V+E)$ | $O(V)$ | DFS or Kahn's |

### 11.5 Algorithm Design Techniques

| Technique | When to Use | Key Property | Example |
|-----------|-------------|--------------|---------|
| Greedy | Local optimal → global optimal | Greedy choice property | Activity selection, Huffman |
| DP | Overlapping subproblems | Optimal substructure | Knapsack, LCS, Edit distance |
| Divide & Conquer | Independent subproblems | Can combine solutions | Merge sort, quick sort |
| Backtracking | Explore all choices | Can prune search tree | N-Queens, Sudoku |
| Branch & Bound | Optimization | Can bound solutions | TSP, 0/1 Knapsack |

---

## 12. Practical Projects

### Project 1: Student Database System (C)

**Concepts:** Structures, arrays, file I/O, sorting, searching

```c
struct Student {
    int roll;
    char name[50];
    float gpa;
};

// Features: Add, delete, search (by roll), sort (by gpa), save to file
```

**Skills Practiced:**
- Structure definition and manipulation
- Array of structures
- Binary search on sorted data
- Bubble/selection sort
- File I/O operations

---

### Project 2: Expression Evaluator (C)

**Concepts:** Stacks, infix/postfix conversion, operator precedence

```c
// Convert infix to postfix, then evaluate postfix
// Handle +, -, *, /, ^, parentheses
```

**Skills Practiced:**
- Stack implementation
- String parsing
- Operator precedence handling
- Two-pass algorithm

---

### Project 3: Social Network Graph (Python)

**Concepts:** Graphs, BFS, DFS, shortest path

```python
class SocialNetwork:
    def add_friend(self, user1, user2): ...
    def shortest_path(self, user1, user2): ...  # BFS
    def mutual_friends(self, user1, user2): ...
    def friend_suggestions(self, user): ...  # Friends of friends
```

**Skills Practiced:**
- Graph representation (adjacency list)
- BFS for shortest path
- Set operations for mutual friends
- Graph traversal

---

### Project 4: LRU Cache (Python)

**Concepts:** Hash map, doubly linked list

```python
class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> node
        self.head = self.tail = None
    
    def get(self, key): ...  # O(1)
    def put(self, key, value): ...  # O(1)
```

**Skills Practiced:**
- Combining data structures
- Hash table for O(1) lookup
- Linked list for O(1) removal
- Cache eviction policy

---

### Project 5: Huffman Coding (C)

**Concepts:** Greedy algorithm, binary trees, priority queue

```c
// Build Huffman tree from character frequencies
// Generate codes for each character
// Encode and decode text
```

**Skills Practiced:**
- Min-heap implementation
- Tree construction
- Greedy algorithm application
- Bit manipulation

---

### Project 6: Maze Solver (Python)

**Concepts:** DFS, BFS, backtracking

```python
def solve_maze_dfs(maze, start, end): ...
def solve_maze_bfs(maze, start, end): ...  # Shortest path
```

**Skills Practiced:**
- Grid representation
- DFS with backtracking
- BFS for shortest path
- Path reconstruction

---

## 13. Internship Preparation

### 13.1 Key Topics to Master

| Priority | Topics | Why Important |
|----------|--------|---------------|
| **High** | Arrays, Strings, Hash Tables | 60% of interview questions |
| **High** | Linked Lists, Stacks, Queues | Fundamental data structures |
| **High** | Trees, BSTs, Recursion | Core problem-solving skills |
| **Medium** | Graphs, BFS, DFS | Many real-world applications |
| **Medium** | Sorting, Searching | Algorithm fundamentals |
| **Medium** | Dynamic Programming | Differentiates strong candidates |
| **Low** | Advanced DS (Tries, Segment Trees) | Specialized problems |

### 13.2 Problem-Solving Framework

1. **Understand** — Restate problem, ask clarifying questions
2. **Examples** — Work through 2-3 examples manually
3. **Approach** — Discuss multiple approaches, pick best
4. **Code** — Write clean, modular code
5. **Test** — Walk through with examples, edge cases
6. **Optimize** — Discuss time/space trade-offs

### 13.3 Common Interview Patterns

| Pattern | Example Problems |
|---------|-----------------|
| **Two Pairs** | Two Sum, Three Sum, Four Sum |
| **Sliding Window** | Longest substring without repeats, minimum window |
| **Fast & Slow Pointers** | Cycle detection, middle of linked list |
| **Merge Intervals** | Meeting rooms, insert interval |
| **BFS/DFS** | Number of islands, word ladder |
| **Top K Elements** | Kth largest, top k frequent |
| **Dynamic Programming** | Climbing stairs, coin change, knapsack |
| **Backtracking** | Permutations, combinations, N-Queens |

### 13.4 Practice Resources

| Resource | Best For |
|----------|----------|
| LeetCode | Pattern-based practice |
| GeeksforGeeks | GATE-specific problems |
| HackerRank | Structured learning paths |
| InterviewBit | Company-specific prep |
| Codeforces | Competitive programming |

### 13.5 30-Day Preparation Plan

| Week | Focus | Daily Target |
|------|-------|--------------|
| Week 1 | Arrays, Strings, Hashing | 3-4 problems/day |
| Week 2 | Linked Lists, Stacks, Queues | 3-4 problems/day |
| Week 3 | Trees, BSTs, Recursion | 2-3 problems/day |
| Week 4 | Graphs, DP, Review | 2-3 problems/day + mock interviews |

---

## 14. Cheat Sheet

### 14.1 Complexity Cheat Sheet

| Operation | Array | Linked List | BST | Hash Table | Heap |
|-----------|-------|-------------|-----|------------|------|
| Access | $O(1)$ | $O(n)$ | $O(\log n)$ | N/A | $O(n)$ |
| Search | $O(n)$ | $O(n)$ | $O(\log n)$ | $O(1)$ | $O(n)$ |
| Insert | $O(n)$ | $O(1)$ | $O(\log n)$ | $O(1)$ | $O(\log n)$ |
| Delete | $O(n)$ | $O(1)$ | $O(\log n)$ | $O(1)$ | $O(\log n)$ |

### 14.2 Sorting Cheat Sheet

| Algorithm | Best For | Avoid When |
|-----------|----------|------------|
| Quick Sort | General purpose, cache-friendly | Stability required |
| Merge Sort | Stable sort, linked lists | Space constrained |
| Heap Sort | Space constrained | Stability required |
| Insertion Sort | Small/nearly sorted data | Large datasets |
| Counting Sort | Small integer range | Large range of values |

### 14.3 Graph Algorithm Selection

| Problem | Algorithm |
|---------|-----------|
| Shortest path (unweighted) | BFS |
| Shortest path (weighted, non-negative) | Dijkstra |
| Shortest path (negative weights) | Bellman-Ford |
| All-pairs shortest path | Floyd-Warshall |
| Minimum spanning tree | Kruskal or Prim |
| Cycle detection (undirected) | Union-Find |
| Cycle detection (directed) | DFS with recursion stack |
| Topological sort | Kahn's or DFS |
| Strongly connected components | Kosaraju's or Tarjan's |

### 14.4 DP Problem Identification

**Signs a problem can be solved with DP:**
1. "Find the maximum/minimum..."
2. "Count the number of ways..."
3. "Can we...?" (yes/no)
4. Problem can be broken into smaller subproblems
5. Subproblems overlap

**DP Implementation Steps:**
1. Define state (what does dp[i] or dp[i][j] represent?)
2. Formulate recurrence relation
3. Determine base cases
4. Decide iteration order (top-down with memo or bottom-up)
5. Optimize space if possible

### 14.5 Recurrence Relations

| Algorithm | Recurrence | Solution |
|-----------|-----------|----------|
| Binary Search | $T(n) = T(n/2) + O(1)$ | $O(\log n)$ |
| Merge Sort | $T(n) = 2T(n/2) + O(n)$ | $O(n \log n)$ |
| Quick Sort (avg) | $T(n) = 2T(n/2) + O(n)$ | $O(n \log n)$ |
| Quick Sort (worst) | $T(n) = T(n-1) + O(n)$ | $O(n^2)$ |
| Strassen | $T(n) = 7T(n/2) + O(n^2)$ | $O(n^{2.81})$ |
| Fibonacci (naive) | $T(n) = T(n-1) + T(n-2)$ | $O(2^n)$ |
| Fibonacci (DP) | Bottom-up | $O(n)$ |

### 14.6 Important Formulas

**Master Theorem:** $T(n) = aT(n/b) + f(n)$
- Case 1: $f(n) = O(n^{\log_b a - \epsilon})$ → $T(n) = \Theta(n^{\log_b a})$
- Case 2: $f(n) = \Theta(n^{\log_b a})$ → $T(n) = \Theta(n^{\log_b a} \log n)$
- Case 3: $f(n) = \Omega(n^{\log_b a + \epsilon})$ → $T(n) = \Theta(f(n))$

**Tree Properties:**
- Height $h$, max nodes: $2^{h+1} - 1$
- $n$ nodes, min height: $\lfloor \log_2 n \rfloor$
- Complete binary tree: $2^h$ to $2^{h+1} - 1$ nodes

**Graph Properties:**
- Sum of degrees = $2E$
- Complete graph: $E = n(n-1)/2$
- Tree: $E = n - 1$

**Heap Properties:**
- Parent of $i$: $\lfloor (i-1)/2 \rfloor$
- Left child of $i$: $2i + 1$
- Right child of $i$: $2i + 2$
- Heapify: $O(\log n)$, Build heap: $O(n)$

---

## 15. One-Day Revision Checklist

### Morning Session (3 hours) — Core Concepts

- [ ] **Arrays:** Traversal, insertion, deletion, searching
- [ ] **Pointers:** Declaration, dereferencing, pointer arithmetic, double pointers
- [ ] **Structures & Unions:** Definition, typedef, memory layout
- [ ] **Dynamic Memory:** malloc, calloc, realloc, free
- [ ] **Recursion:** Base case, recursive case, tail recursion, stack frames
- [ ] **Time Complexity:** Big-O, Big-Omega, Big-Theta definitions
- [ ] **Master Theorem:** Three cases, practice 5 recurrences

### Mid-Day Session (3 hours) — Data Structures

- [ ] **Linked Lists:** Singly, doubly, circular — insert, delete, reverse
- [ ] **Stacks:** Array vs linked list implementation, applications
- [ ] **Queues:** Simple, circular, priority — operations
- [ ] **Trees:** Binary tree traversals (inorder, preorder, postorder)
- [ ] **BST:** Insert, delete, search — balanced vs unbalanced
- [ ] **Heaps:** Min-heap, max-heap, heapify, heap sort
- [ ] **Hash Tables:** Hash functions, collision resolution, load factor
- [ ] **Graphs:** Adjacency matrix vs list, representations

### Afternoon Session (3 hours) — Algorithms

- [ ] **Searching:** Linear search, binary search (iterative & recursive)
- [ ] **Sorting:** Bubble, selection, insertion — trace through examples
- [ ] **Advanced Sorting:** Merge sort, quick sort — partition, recurrence
- [ ] **Greedy:** Activity selection, Huffman coding
- [ ] **DP:** Knapsack, LCS, edit distance — fill DP tables
- [ ] **Divide & Conquer:** Merge sort, quick sort, binary search
- [ ] **Graph Traversals:** BFS, DFS — order of visitation
- [ ] **Shortest Path:** Dijkstra, Bellman-Ford — trace through examples
- [ ] **MST:** Kruskal, Prim — union-find operations

### Evening Session (2 hours) — Practice & Review

- [ ] **Solve 5 GATE previous year questions** (mix of topics)
- [ ] **Review all comparison tables** (sorting, DS operations, graph algorithms)
- [ ] **Memorize complexity table** for all standard algorithms
- [ ] **Practice tracing:** Binary search, quicksort partition, heapify
- [ ] **Review common mistakes** section
- [ ] **Quick scan of FAQs** — especially scenario-based questions

### Quick Reference Cards (Keep Handy)

**Card 1: Sorting Complexities**
```
Bubble: O(n²) avg, O(n) best, stable
Selection: O(n²) all, not stable
Insertion: O(n²) avg, O(n) best, stable
Merge: O(n log n) all, stable, O(n) space
Quick: O(n log n) avg, O(n²) worst, not stable
Heap: O(n log n) all, not stable, O(1) space
```

**Card 2: Tree Traversals**
```
Inorder: Left → Root → Right (gives sorted order in BST)
Preorder: Root → Left → Right (copy tree)
Postorder: Left → Right → Root (delete tree)
Level-order: BFS, use queue
```

**Card 3: Graph Algorithms**
```
BFS: Queue, shortest path (unweighted), O(V+E)
DFS: Stack/Recursion, cycle detection, O(V+E)
Dijkstra: Priority queue, non-negative weights, O((V+E)log V)
Kruskal: Sort edges, union-find, O(E log E)
Prim: Priority queue, grow from vertex, O((V+E)log V)
```

**Card 4: DP Patterns**
```
1D DP: Fibonacci, climbing stairs, house robber
2D DP: LCS, edit distance, knapsack
Interval DP: Matrix chain multiplication
Tree DP: Diameter, max path sum
State machine DP: Stock problems
```

### Final Tips for Exam Day

1. **Read questions carefully** — "worst case" vs "average case"
2. **Draw diagrams** for trees, graphs, linked lists
3. **Trace algorithms** on small examples (n=3, n=4)
4. **Check boundary conditions** — empty input, single element
5. **Verify complexity** — don't guess, analyze loops
6. **For numerical answers** — substitute small values to verify
7. **Time management** — don't spend >5 min on single question
8. **Mark and revisit** — come back to difficult questions

---

## GATE 2027: Key Formulas at a Glance

### Complexity Classes (Fastest to Slowest)
$$O(1) < O(\log n) < O(\sqrt{n}) < O(n) < O(n \log n) < O(n^2) < O(n^3) < O(2^n) < O(n!)$$

### Stirling's Approximation
$$n! \approx \sqrt{2\pi n} \left(\frac{n}{e}\right)^n$$

### Harmonic Series
$$H_n = 1 + \frac{1}{2} + \frac{1}{3} + \cdots + \frac{1}{n} \approx \ln n + \gamma$$

### Geometric Series
$$\sum_{i=0}^{n} ar^i = a\frac{r^{n+1} - 1}{r - 1}$$

### Logarithm Properties
$$\log_a(xy) = \log_a x + \log_a y$$
$$\log_a(x^n) = n \log_a x$$
$$\log_a b = \frac{\log_c b}{\log_c a}$$

### Summation Formulas
$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$
$$\sum_{i=1}^{n} i^2 = \frac{n(n+1)(2n+1)}{6}$$
$$\sum_{i=1}^{n} i^3 = \left(\frac{n(n+1)}{2}\right)^2$$

---

**End of Chapter — GATE 2027: Programming, Data Structures and Algorithms**

*Good luck with your preparation!