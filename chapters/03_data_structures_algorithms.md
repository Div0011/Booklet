# 3. Data Structures and Algorithms (Core Patterns & Complexity)

## 1. Introduction

### What it is
Data Structures are programmatic methods for organizing, storing, and accessing data in computer memory. Algorithms are precise, step-by-step computational procedures that take input parameters, perform logical transformations, and yield outputs. Together, they form the core foundation of computational efficiency, determining how software performs as data loads scale.

### Why it exists
Computer hardware has physical limitations: finite processor speeds, CPU cache sizes, memory bandwidth, and RAM limits. An inefficient algorithm can cause execution times to spike exponentially as input datasets grow, rendering applications unusable. DSA exists to provide a structured, mathematical framework for evaluating and optimizing execution speeds (Time Complexity) and memory consumption (Space Complexity).

### Problems it solves
- **Algorithmic Scale Collapse**: Prevents applications from slowing to a crawl ($O(N^2)$ or $O(2^N)$ runtime) when processing enterprise-scale datasets.
- **Search Latency**: Avoids scanning millions of rows sequentially by using indexed layouts (like B-Trees or Hash tables).
- **Network Optimization**: Finds the shortest routing path through complex networks, minimizing data transfer delays.
- **Resource Constraints**: Fits large datasets into limited system memory by using compact encodings.

### Industry Use Cases
- **Database Query Engines**: Databases use B+ Trees to accelerate range queries, and LSM-Trees (Log-Structured Merge-Trees) to handle high-frequency writes.
- **GPS Navigation and Routing**: Google Maps runs variations of Dijkstra's and A* search algorithms to calculate real-time driving routes.
- **Search Engine Autocomplete**: Search inputs use Trie structures (prefix trees) to return instant word completions as users type.
- **High-Performance Caching**: Web frameworks implement Least Recently Used (LRU) caches using HashMaps and Doubly Linked Lists to fetch hot objects in constant $O(1)$ time.

### Analogy
Data structures are the layout systems in a shipping warehouse (shelves, zones, indexing tags). Algorithms are the pickup routes and sorting instructions used by warehouse workers. If you store items randomly in a pile (unsorted array), workers must inspect every item to find a match (linear search). If you index items on ordered shelves (Binary Search Tree) and provide workers with optimized pick paths (binary search), they can locate any item in seconds.

---

## 2. Core Concepts

### Beginner Concepts
- **Big-O Notation**: A mathematical framework used to describe the asymptotic upper bound of an algorithm's worst-case runtime as a function of the input size $N$.
  - $O(1)$ (Constant): Runtime is independent of input size (e.g. HashMap read).
  - $O(\log N)$ (Logarithmic): Input size halves on each step (e.g. Binary Search).
  - $O(N)$ (Linear): Runtime scales proportionally with input size (e.g. Single loop).
  - $O(N \log N)$ (Linearithmic): Divide-and-conquer operations (e.g. Merge Sort).
  - $O(N^2)$ (Quadratic): Nested loops over the input (e.g. Bubble Sort).
- **Linear Data Structures**:
  - **Array**: Contiguous memory blocks storing elements of the same type. Fast random access ($O(1)$) but slow insertions ($O(N)$) due to element shifting.
  - **Linked List**: Nodes containing data and pointers to the next node. Fast insertions ($O(1)$ at ends) but slow random access ($O(N)$).
  - **Stack**: LIFO (Last-In, First-Out) structure (push/pop).
  - **Queue**: FIFO (First-In, First-Out) structure (enqueue/dequeue).
- **Recursion**: A programming technique where a function calls itself to solve smaller instances of the same problem, requiring a base case to prevent stack overflow.

### Intermediate Concepts
- **Non-Linear Data Structures**:
  - **Trees**: Hierarchical nodes where each parent can have child nodes.
    - **Binary Search Tree (BST)**: A binary tree where the left child is smaller than the parent, and the right child is larger.
  - **Heaps (Priority Queues)**: Binary trees maintaining the heap property (Max-Heap: parent $\ge$ children; Min-Heap: parent $\le$ children).
  - **Graphs**: Nodes (vertices) connected by edges. Represented via Adjacency Lists (best for sparse graphs) or Adjacency Matrices (best for dense graphs).
- **Sorting Algorithms**:
  - **Merge Sort**: Stable, divide-and-conquer sort with $O(N \log N)$ runtime.
  - **Quick Sort**: Unstable, in-place sort with $O(N \log N)$ average runtime.
- **Hashing and Collisions**: Using a hash function to map keys to bucket indices. Collisions occur when different keys hash to the same bucket index. Resolved via **Chaining** (linked lists in buckets) or **Open Addressing** (finding empty buckets via probing).

### Advanced Concepts
- **Dynamic Programming (DP)**: An optimization technique for problems with overlapping subproblems and optimal substructures. Solved via:
  - **Memoization (Top-Down)**: Storing recursive results in a cache.
  - **Tabulation (Bottom-Up)**: Building a table iteratively to construct the final solution.
- **Disjoint Set Union (DSU)**: A structure tracking partitioned elements into disjoint subsets. Optimized using **Path Compression** and **Union by Rank** to achieve near-constant $O(\alpha(N))$ amortized runtime.
- **Trie (Prefix Tree)**: A search tree used to store associative arrays where keys are strings, enabling fast prefix lookups.
- **Advanced Graph Algorithms**:
  - **Dijkstra's Algorithm**: Calculates the shortest path on a weighted graph with non-negative edge weights using a Min-Heap.
  - **Bellman-Ford**: Calculates shortest paths while handling negative edge weights and detecting negative cycles.
- **Segment Trees & Fenwick Trees**: Trees optimized to perform range queries and element updates on arrays in logarithmic $O(\log N)$ time.

---

## 3. Internal Working

### Mathematical Complexity Framework
Formal definition of Big-O: An algorithm has a runtime complexity $f(N) = O(g(N))$ if there exist positive constants $c$ and $N_0$ such that:

$$|f(N)| \le c \cdot |g(N)| \quad \text{for all } N \ge N_0$$

This represents the asymptotic limit, ignoring constant factors and lower-order terms.

**Master Theorem for Divide-and-Conquer Recurrences**:
If an algorithm's runtime is defined by the recurrence:
$$T(N) = aT\left(\frac{N}{b}\right) + f(N)$$
where $a \ge 1$ and $b > 1$, the asymptotic complexity is evaluated by comparing $f(N)$ to $N^{\log_b a}$:
- **Case 1**: If $f(N) = O(N^c)$ where $c < \log_b a$, then $T(N) = \Theta(N^{\log_b a})$.
- **Case 2**: If $f(N) = \Theta(N^{\log_b a} \log^k N)$, then $T(N) = \Theta(N^{\log_b a} \log^{k+1} N)$. (For Merge Sort, $a=2, b=2, k=0 \to T(N) = \Theta(N \log N)$).
- **Case 3**: If $f(N) = \Omega(N^c)$ where $c > \log_b a$, then $T(N) = \Theta(f(N))$.

### LRU Cache Internals
An LRU (Least Recently Used) cache must execute `get()` and `put()` operations in constant $O(1)$ time. This requires combining two distinct data structures:

```text
HashMap Lookup Table (Key -> Node Pointer)
+------------+-------------------------+
| Key "user" | Pointer to Node("Alice")|
+------------+-------------------------+
                     |
                     v
Doubly Linked List (Ordering by Recency)
+------------+     +-----------------------+     +-----------------------+     +------------+
| Dummy Head | <-> | Node: Key="user"      | <-> | Node: Key="theme"     | <-> | Dummy Tail |
|            |     | Value="Alice"         |     | Value="dark"          |     |            |
+------------+     +-----------------------+     +-----------------------+     +------------+
                   (Most Recently Used)          (Least Recently Used)
```

1. **HashMap**: Stores key-to-node pointers, providing $O(1)$ time complexity for value lookups.
2. **Doubly Linked List**: Stores cached values in order of recency.
   - When a key is accessed (`get`), the HashMap locates the node in $O(1)$ time. The node is unlinked from its current position in the list and moved to the head, marking it as Most Recently Used.
   - When a new key is added (`put`), a new node is inserted at the head. If the cache exceeds capacity, the node at the tail (Least Recently Used) is evicted from both the list and the HashMap.

### Graph Traversals (BFS vs. DFS Mechanics)
- **Breadth-First Search (BFS)**: Explores a graph layer-by-layer. It uses a **Queue** (FIFO) to track neighbor nodes. BFS guarantees finding the shortest path on unweighted graphs because it visits nodes in order of their distance from the source.
- **Depth-First Search (DFS)**: Explores a branch as deeply as possible before backtracking. It uses a **Stack** (LIFO, either via the system recursion stack or an explicit stack structure). Best for topological sorting and cycle detection.

---

## 4. Important Terminology

- **Big-O**: Asymptotic upper bound of runtime complexity.
- **Amortized Complexity**: The average cost of an operation over a sequence of operations (e.g. array resizing).
- **Recursion**: Function calling itself to solve smaller subproblems.
- **Memoization**: Storing recursive subproblem results in a lookup table (Top-Down DP).
- **Tabulation**: Building a table iteratively from base cases up (Bottom-Up DP).
- **BST (Binary Search Tree)**: Sorted binary tree where left < parent < right.
- **Heap**: Complete binary tree maintaining parent-child order limits.
- **Trie**: Prefix tree used to store and look up strings efficiently.
- **DSU (Disjoint Set Union)**: Structure tracking partitions of disjoint elements.
- **Segment Tree**: Tree structure optimized for range queries and updates.
- **Dijkstra's Algorithm**: Shortest path algorithm for non-negative weighted graphs.
- **BFS (Breadth-First Search)**: Queue-based graph traversal visiting nodes level-by-level.
- **DFS (Depth-First Search)**: Stack-based graph traversal exploring branches deeply.
- **Topological Sort**: Linear ordering of vertices in a directed acyclic graph (DAG) based on dependencies.
- **Stable Sort**: Sorting algorithm that preserves the relative order of equal elements.
- **In-Place Sort**: Sorting algorithm requiring $O(1)$ auxiliary memory.
- **Divide and Conquer**: Breaking a problem into independent subproblems, solving them, and merging results.
- **Hash Collision**: When different keys hash to the same bucket index in a hash table.
- **Chaining**: Handling hash collisions by storing elements in a linked list at the bucket index.
- **Open Addressing**: Handling hash collisions by probing for the next empty bucket.
- **Load Factor**: The ratio of stored items to hash table capacity, triggering resize operations.
- **Adjacency List**: Array of linked lists representing graph edges, efficient for sparse graphs.
- **Adjacency Matrix**: 2D array representing graph edges, efficient for dense graphs.

---

## 5. Beginner Examples

### Example 1: Binary Search (Iterative and Recursive)
Searching a sorted array for a target value in $O(\log N)$ time. Includes the mid-calculation overflow fix.

```python
def binary_search_iterative(arr: list[int], target: int) -> int:
    lo, hi = 0, len(arr) - 1
    
    while lo <= hi:
        # Prevent integer overflow: (lo + hi) // 2 can exceed boundary limits in static languages
        mid = lo + (hi - lo) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
            
    return -1

# Recursive implementation
def binary_search_recursive(arr: list[int], target: int, lo: int, hi: int) -> int:
    if lo > hi:
        return -1
        
    mid = lo + (hi - lo) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    else:
        return binary_search_recursive(arr, target, lo, mid - 1)
```

### Example 2: Two Sum using Hash Map
Locating two numbers in an array that add up to a target value in $O(N)$ time.

```python
def find_two_sum(nums: list[int], target: int) -> list[int]:
    # Stores: Value -> Index
    seen = {}
    
    for current_index, current_val in enumerate(nums):
        complement = target - current_val
        
        # Check if the complement has been seen
        if complement in seen:
            return [seen[complement], current_index]
            
        # Record current value and index
        seen[current_val] = current_index
        
    return [] # Return empty list if no pair matches
```

### Example 3: Stack for Valid Parentheses
Validating balanced opening and closing brackets.
```python
def is_parentheses_balanced(expression: str) -> bool:
    stack = []
    brackets_map = {")": "(", "}": "{", "]": "["}
    
    for char in expression:
        if char in "({[":
            stack.append(char)
        elif char in brackets_map:
            # If stack is empty or top element doesn't match, brackets are unbalanced
            if not stack or stack.pop() != brackets_map[char]:
                return False
                
    # Balanced only if stack is empty
    return len(stack) == 0
```

---

## 6. Intermediate Examples

### Example 1: LRU Cache Implementation from Scratch
A complete, custom LRU Cache implementing a Doubly Linked List and HashMap in Python without using standard libraries.

```python
class Node:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {} # Map key -> Node
        
        # Initialize sentinel dummy head and tail nodes to simplify unlinking
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node):
        """Unlink node from its current position in the list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node):
        """Insert node immediately after the dummy head."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node) # Mark as most recently used
            return node.val
        return -1

    def put(self, key: int, value: int):
        if key in self.cache:
            # Update existing value and move to head
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_head(node)
        else:
            # Create new entry
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            
            # Check capacity limits
            if len(self.cache) > self.capacity:
                # Evict least recently used (node before dummy tail)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
```

### Example 2: Merge Sort
A divide-and-conquer sorting algorithm that guarantees $O(N \log N)$ runtime.

```python
def merge_sort(arr: list[int]) -> list[int]:
    # Base case: array of size 1 is already sorted
    if len(arr) <= 1:
        return arr
        
    # Divide array into halves
    mid = len(arr) // 2
    left_half = merge_sort(arr[:mid])
    right_half = merge_sort(arr[mid:])
    
    # Merge sorted halves
    return merge_halves(left_half, right_half)

def merge_halves(left: list[int], right: list[int]) -> list[int]:
    merged = []
    i = j = 0
    
    # Merge elements in sorted order
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
            
    # Append any remaining elements
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
```

### Example 3: Topological Sort (Kahn's Algorithm)
A dependency scheduling algorithm utilizing in-degrees and BFS to sort a Directed Acyclic Graph (DAG), detecting cycles if present.

```python
from collections import deque

def find_topological_sort(num_courses: int, prerequisites: list[list[int]]) -> list[int]:
    # 1. Build adjacency list and calculate node in-degrees
    adj_list = {i: [] for i in range(num_courses)}
    in_degree = [0] * num_courses
    
    for dest, src in prerequisites:
        adj_list[src].append(dest)
        in_degree[dest] += 1
        
    # 2. Queue nodes with 0 in-degree (no prerequisites)
    queue = deque([i for i in range(num_courses) if in_degree[i] == 0])
    ordered_list = []
    
    # 3. Process nodes
    while queue:
        node = queue.popleft()
        ordered_list.append(node)
        
        # Decrement in-degree for all neighbor nodes
        for neighbor in adj_list[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                
    # 4. Check for cycles
    if len(ordered_list) != num_courses:
        return [] # Cycle detected, topological sort is impossible
        
    return ordered_list
```

---

## 7. Advanced Concepts & Examples

### Example 1: Dynamic Programming - Coin Change Problem
Finding the minimum number of coins needed to make up a target amount.

```python
def get_min_coins(coins: list[int], amount: int) -> int:
    # dp[i] stores the minimum coins needed to make amount i
    # Initialize table with infinity, except base case dp[0] = 0
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    # Iterate through all target amounts
    for i in range(1, amount + 1):
        for coin in coins:
            if i - coin >= 0:
                # Recurrence: dp[i] = min(dp[i], dp[i - coin] + 1)
                dp[i] = min(dp[i], dp[i - coin] + 1)
                
    # Return -1 if amount cannot be reached
    return dp[amount] if dp[amount] != float('inf') else -1
```
- **State Definition**: `dp[i]` represents the minimum number of coins required to build the value `i`.
- **Recurrence Relation**:
  $$dp[i] = \min_{c \in \text{coins}} (dp[i - c] + 1)$$
- **Space Optimization**: Complexity is $O(A \cdot C)$ time and $O(A)$ space, where $A$ is the target amount and $C$ is the coin set size.

### Example 2: Disjoint Set Union (DSU) and Kruskal's MST Algorithm
Implementing DSU with Path Compression and Union by Rank to find the Minimum Spanning Tree of a weighted graph.

```python
class DisjointSetUnion:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size

    def find(self, x: int) -> int:
        """Find root parent with Path Compression."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Union by Rank. Returns True if a merge occurred, False if already in same set."""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False
            
        # Merge lower rank tree under higher rank tree
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
            
        return True

def find_minimum_spanning_tree(num_vertices: int, edges: list[tuple[int, int, int]]) -> int:
    """
    Kruskal's Algorithm:
    Edges list format: (weight, u, v)
    """
    # 1. Sort edges by weight in ascending order
    edges.sort()
    
    dsu = DisjointSetUnion(num_vertices)
    mst_weight = 0
    edges_added = 0
    
    for weight, u, v in edges:
        # Try to connect vertices
        if dsu.union(u, v):
            mst_weight += weight
            edges_added += 1
            if edges_added == num_vertices - 1:
                break
                
    return mst_weight
```

### Example 3: Dijkstra's Shortest Path Algorithm
Calculating the shortest path on a weighted graph with non-negative edge weights using a Min-Heap.

```python
import heapq

def calculate_shortest_paths(num_vertices: int, graph_adj: dict, source: int) -> dict:
    """
    graph_adj format: {u: [(v, weight), ...]}
    """
    # Initialize distances to all vertices as infinity, source as 0
    distances = {i: float('inf') for i in range(num_vertices)}
    distances[source] = 0
    
    # Min-Heap stores tuples: (distance, vertex)
    min_heap = [(0, source)]
    
    # Set to track visited nodes
    visited = set()
    
    while min_heap:
        current_distance, u = heapq.heappop(min_heap)
        
        # Skip processing if the node has already been visited
        if u in visited:
            continue
        visited.add(u)
        
        # Traverse neighbors
        for neighbor, weight in graph_adj.get(u, []):
            if neighbor in visited:
                continue
                
            distance_through_u = current_distance + weight
            
            # Relaxation step
            if distance_through_u < distances[neighbor]:
                distances[neighbor] = distance_through_u
                heapq.heappush(min_heap, (distance_through_u, neighbor))
                
    return distances
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate problem-solving ability by testing how candidates design, explain, and optimize algorithms. They look for candidates who clarify constraints before writing code, start with a brute-force approach and optimize systematically, write clean variable names, and calculate Time and Space complexity accurately.

### Red Flags
- **Jumping Straight to Coding**: Coding before verifying input constraints, edge cases (e.g. empty lists, negative values), or expected outputs.
- **Complexity Calculation Errors**: Confusing $O(N)$ and $O(\log N)$ or omitting stack space overhead when calculating recursive space complexity.
- **Mismatching Traversals**: Recommending DFS when the task requires finding the shortest path on an unweighted graph (which requires BFS).
- **Infinite Loop Oversights**: Writing binary search loops without updates to `lo` or `hi` pointers, causing infinite loops.

### Green Flags
- **PECS Application**: Demonstrating knowledge of pointer constraints and memory layouts.
- **Mental Dry Runs**: Tracing the code step-by-step with a small example inputs before declaring it complete.
- **Space-Efficient DP**: Implementing space optimization (e.g., keeping only the previous two states in Fibonacci instead of a complete array).
- **Proactive Constraint Checking**: Handling null objects, empty arrays, and potential overflow bounds gracefully.

### Answers Matrix
| Level | Question: "When would you use a Min-Heap instead of sorting an array?" |
|---|---|
| **Rejected** | "Heaps are always faster than sorting arrays." |
| **Shortlisted** | "Use a heap when you need to continuously retrieve the minimum element from a dynamic dataset, as heap push/pop takes $O(\log N)$ time, while sorting takes $O(N \log N)$." |
| **Selected** | "Use a **Min-Heap (Priority Queue)** when processing a dynamic stream of data where elements are added continuously, and you need to retrieve the minimum element frequently. A Heap maintains the heap property in $O(\log N)$ time for insertions and deletions. Sorting the array takes $O(N \log N)$ time for each update. However, if the dataset is static and you only need to sort it once, standard sorting algorithms (like Timsort) are preferred because they have better cache locality and run faster in practice." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Compare Arrays and Linked Lists.
- **Detailed Answer**:
- **Array**: Contiguous block of memory.
  - *Time Complexity*: Access: $O(1)$ (using index offset math). Search: $O(N)$. Insert/Delete: $O(N)$ (requires shifting elements).
  - *Memory*: Contiguous allocation; suffers from resizing overhead but benefits from CPU cache locality.
- **Linked List**: Scattered nodes connected via pointers.
  - *Time Complexity*: Access: $O(N)$. Search: $O(N)$. Insert/Delete: $O(1)$ if the pointer is already located.
  - *Memory*: Dynamic allocation; node pointers consume extra memory overhead and cause CPU cache misses.
- **Follow-up Questions**: Why is ArrayList resizing slow? (Answer: Because when the capacity limit is reached, a new larger array must be allocated in memory, and all existing elements must be copied over, an $O(N)$ operation).
- **Interviewer's Expectations**: Compare time complexities (access vs insertion), memory layouts, and CPU cache performance.

#### 2. How do HashMaps resolve collisions internally?
- **Detailed Answer**: HashMaps resolve hash collisions (where two different keys generate the same bucket index) using two main strategies:
1. **Separate Chaining**: Each bucket contains a linked list (or red-black tree) of entries. When a collision occurs, the new entry is appended to the list. If list sizes exceed a threshold (e.g., 8 in Java), the list is converted to a red-black tree to improve lookup speed from $O(N)$ to $O(\log N)$.
2. **Open Addressing**: If a collision occurs, the map probes for the next empty bucket index using algorithms like Linear Probing (checking sequential indices), Quadratic Probing, or Double Hashing.
- **Follow-up Questions**: What is the "Load Factor"? (Answer: The ratio of elements to bucket capacity (typically 0.75). When reached, the map allocates a larger bucket array and rehashes all elements to prevent collision performance degradation).
- **Interviewer's Expectations**: Detail chaining, tree conversions (red-black trees), open addressing, and load factor thresholds.

#### 3. What is the difference between a Binary Search Tree (BST) and a Heap?
- **Detailed Answer**:
- **BST**: An ordered, binary tree structure where for every node: left child < parent < right child.
  - *Use Case*: Fast search, insertion, and deletion of sorted elements in $O(\log N)$ average time.
- **Heap**: A complete binary tree maintaining the heap property: parent $\le$ children (Min-Heap) or parent $\ge$ children (Max-Heap). There is no left-to-right order sorting.
  - *Use Case*: Fast retrieval of the minimum or maximum element in $O(1)$ time, and updating in $O(\log N)$ time.
- **Follow-up Questions**: What is the worst-case search complexity in an unbalanced BST? (Answer: $O(N)$ if the tree degenerates into a linear linked list; self-balancing trees like AVL or Red-Black trees resolve this by maintaining $O(\log N)$ bounds).
- **Interviewer's Expectations**: Compare ordering rules (sorted vs heap property), completeness constraints, and search complexities.

#### 4. What is the difference between BFS and DFS? When do you choose each?
- **Detailed Answer**:
- **Breadth-First Search (BFS)**:
  - Explores nodes level-by-level, using a **Queue** (FIFO).
  - *When to choose*: Best for finding the **shortest path on unweighted graphs**, as it guarantees visiting nodes in order of their distance from the source.
- **Depth-First Search (DFS)**:
  - Explores paths as deeply as possible, using a **Stack** (LIFO) or recursion.
  - *When to choose*: Best for finding topological sorting, cycle detection, or path connectivity where shortest distance is not required.
- **Follow-up Questions**: How does memory usage compare? (Answer: BFS memory scales with the width of the graph (storing queue layers). DFS memory scales with the depth of the graph (storing recursion stack frames)).
- **Interviewer's Expectations**: Compare tracking structures (Queue vs Stack), path finding capabilities, and memory footprints.

#### 5. Explain the difference between Dynamic Programming (DP) and Greedy algorithms.
- **Detailed Answer**:
- **Dynamic Programming**: Solves problems with overlapping subproblems and optimal substructures. It evaluates *all* possible subpaths to find the global optimum, saving intermediate results to avoid redundant calculations.
- **Greedy Algorithms**: Makes the locally optimal choice at each step, hoping it leads to a global optimum. It never backtracks or evaluates other paths.
- **Follow-up Questions**: How do you prove a greedy algorithm is correct? (Answer: Using proof techniques like structural induction or exchange arguments to show that the greedy choice always yields an optimal solution).
- **Interviewer's Expectations**: Contrast local optimization (Greedy) with global evaluation (DP), and explain subproblem memoization.

#### 6. What is amortized time complexity? Give an example.
- **Detailed Answer**: Amortized Time Complexity is the average cost of an operation over a long sequence of operations. Even if a single operation is expensive, it is amortized if it occurs infrequently.
- *Example*: Adding an element to an `ArrayList`. Most insertions take $O(1)$ constant time. However, when the array capacity is full, the array must resize. This requires allocating a new array and copying all $N$ elements over, which takes $O(N)$ time. Since this resize occurs infrequently (e.g. doubling capacity), the average cost per insertion remains $O(1)$.
- **Follow-up Questions**: How does this differ from average-case complexity? (Answer: Average-case depends on random inputs. Amortized complexity guarantees the average cost of a sequence of operations in the worst case).
- **Interviewer's Expectations**: Define sequential averages and explain array resizing mechanics.

#### 7. Compare Merge Sort, Quick Sort, and Heap Sort.
- **Detailed Answer**:
- **Merge Sort**: Divide-and-conquer. Time: $O(N \log N)$ (best/average/worst). Space: $O(N)$ auxiliary space. It is **stable** (preserves equal element order).
- **Quick Sort**: Partition-based. Time: $O(N \log N)$ average, but degrades to $O(N^2)$ in the worst case (if pivots are chosen poorly). Space: $O(\log N)$ recursion stack space. It is **unstable** but runs fast due to good cache locality.
- **Heap Sort**: Heap-based. Time: $O(N \log N)$ (best/average/worst). Space: $O(1)$ auxiliary space. It is **unstable**.
- **Follow-up Questions**: Why is Quick Sort preferred over Merge Sort for arrays? (Answer: Quick Sort is in-place ($O(1)$ extra space) and has better cache locality than Merge Sort, which requires allocating a temporary array).
- **Interviewer's Expectations**: Compare time complexities (average vs worst case), auxiliary space requirements, and stability.

#### 8. What is the difference between a Trie and a Hash Map?
- **Detailed Answer**:
- **Hash Map**: Maps complete keys directly to values.
  - *Complexity*: $O(1)$ average lookup, but degrades if hash collisions occur.
  - *Cons*: Cannot perform prefix searches or retrieve alphabetical order easily.
- **Trie (Prefix Tree)**: Stores strings character-by-character along path branches.
  - *Complexity*: $O(L)$ lookup where $L$ is the length of the string, independent of dataset size.
  - *Pros*: Supports prefix searches (e.g., find all words starting with "app"), autocomplete lookup, and saves space for shared prefixes.
- **Follow-up Questions**: How does a Trie save space? (Answer: By sharing common prefixes; words like "cart", "car", and "card" share the same initial prefix path node).
- **Interviewer's Expectations**: Compare lookup complexities, detail prefix search features, and explain node sharing.

#### 9. What is a Disjoint Set Union (DSU) structure and how is it optimized?
- **Detailed Answer**: DSU (or Union-Find) is a data structure tracking partitioned elements into disjoint subsets. It supports two operations: `find(x)` (locate the subset representative) and `union(x, y)` (merge two subsets).
**Optimizations**:
1. **Path Compression**: During `find(x)`, update parent pointers of all traversed nodes to point directly to the root representative, shortening future searches.
2. **Union by Rank**: During `union(x, y)`, attach the tree with smaller depth (rank) under the tree with larger depth, keeping the tree balanced.
- These optimizations reduce the time complexity of DSU operations to near-constant $O(\alpha(N))$ amortized time (where $\alpha$ is the Inverse Ackermann function).
- **Follow-up Questions**: What is the value of $\alpha(N)$ in practice? (Answer: For all practical inputs, $\alpha(N) < 5$, making it virtually $O(1)$).
- **Interviewer's Expectations**: Describe find/union operations, explain path compression and union by rank, and mention the Inverse Ackermann complexity.

#### 10. Explain B-Trees and B+ Trees. Why are they used in databases?
- **Detailed Answer**:
- **B-Trees**: Balanced search trees designed for external storage. Unlike binary trees, each node can contain multiple keys and child pointers, reducing tree height.
- **B+ Trees**: A variation where:
  - All actual data records are stored in the leaf nodes.
  - Internal nodes store only index keys.
  - Leaf nodes are linked sequentially, enabling fast range scans.
- **Why used in databases**: Reading from disk is slow. By storing multiple keys per node, the tree height is reduced (typically 3-4 levels for millions of records). This minimizes disk I/O reads.
- **Follow-up Questions**: Why does storing keys in internal nodes improve B+ Tree performance? (Answer: It allows internal nodes to hold more pointers per page, increasing the fan-out ratio and reducing tree height).
- **Interviewer's Expectations**: Explain node key capacity, leaf node chaining, and the reduction of disk page reads.

---

### Scenario-Based Questions

#### 11. Design a system to find the top 100 most frequent search terms in a real-time stream of millions of queries.
- **Detailed Answer**: I will use a **Frequency Map** combined with a **Min-Heap**:
1. **Count Frequencies**: Use a HashMap to count query occurrences in real-time. Or use a Count-Min Sketch (probabilistic data structure) if memory is restricted.
2. **Track Top 100**: Maintain a Min-Heap of size 100 storing tuples: `(frequency, query)`.
3. **Update Logic**:
   - For each query, update its frequency in the map.
   - If the query is already in the heap, update its value and heapify.
   - If not in the heap, check if its frequency is higher than the minimum frequency in the heap (the root). If yes, pop the root and insert the new query.
- This maintains the top 100 queries in $O(\log 100)$ time per update, using minimal memory.
- **Follow-up Questions**: How do you scale this to run across multiple distributed servers? (Answer: Route queries to partition nodes using consistent hashing, and merge their local top 100 lists on a coordinator node).
- **Interviewer's Expectations**: Propose hash maps for counting, min-heaps for top-K limits, and explain update logic complexities.

#### 12. Design an autocomplete suggestions system.
- **Detailed Answer**:
- **Data Structure**: I will use a **Trie (Prefix Tree)**.
- **Trie Node Structure**:
  - Each node contains a map of characters to child nodes, a boolean indicating the end of a word, and a list of the top 3 most popular words starting with that prefix.
- **Workflow**:
  1. As the user types "ap", traverse the Trie nodes: `a -> p`.
  2. At node `p`, return the pre-compiled list of the top 3 popular words stored on the node.
  3. This ensures lookup is $O(L)$ where $L$ is the input prefix length, avoiding the need to traverse the entire subtree at runtime.
- **Follow-up Questions**: How do you update search frequencies in the Trie? (Answer: Run a daily background job that recalculates query frequencies from search logs and updates the pre-compiled lists on the Trie nodes).
- **Interviewer's Expectations**: Recommend Tries, suggest storing pre-compiled top suggestions on nodes, and analyze prefix search complexities.

#### 13. You have a list of tasks with dependency rules (e.g. Task A must run before Task B). Write a design to detect circular dependencies.
- **Detailed Answer**:
- **Graph Modeling**: Model the tasks as a Directed Graph where vertices are tasks and directed edges represent dependencies ($A \to B$).
- **Cycle Detection Design**:
  - Implement **Kahn's Algorithm (Topological Sort)**.
  - Calculate the in-degrees of all task nodes.
  - Queue nodes with 0 in-degree and process them (decrementing neighbor in-degrees).
  - Count processed nodes. If the count of processed nodes does not match the total number of tasks, a circular dependency exists.
- **Alternative**: Run DFS with a recursion stack tracker (three-color marking: unvisited, visiting, visited). If DFS encounters a node currently in the `visiting` state, a cycle exists.
- **Follow-up Questions**: What is the time complexity of cycle detection? (Answer: $O(V + E)$ where $V$ is tasks and $E$ is dependency rules, as each node and edge is processed once).
- **Interviewer's Expectations**: Model dependencies as a directed graph and recommend cycle detection using Kahn's or DFS coloring.

#### 14. Design an in-memory filesystem.
- **Detailed Answer**:
- **Data Structure**: A **Trie-like Tree structure** representing directories and files.
- **Node Structure**:
  ```python
  class FileNode:
      def __init__(self, name: str, is_file: bool = False):
          self.name = name
          self.is_file = is_file
          self.content = ""             # Empty if directory
          self.children = {}            # Map: Name -> FileNode (Empty if file)
  ```
- **Operations**:
  - `mkdir(path)`: Split the path string by `/` and traverse the node tree, creating child nodes if they do not exist.
  - `write_file(path, content)`: Navigate to the target path node, set `is_file = True`, and append content.
  - `read_file(path)`: Navigate to the node and return the content string.
- **Follow-up Questions**: What is the complexity of locating a file? (Answer: $O(D \cdot L)$ where $D$ is the depth of the directory structure and $L$ is the average name length).
- **Interviewer's Expectations**: Propose tree-structured nodes with maps for children and trace path split traversals.

#### 15. You need to build a rate limiter that checks if a client IP made more than 100 calls in a rolling 60-second window.
- **Detailed Answer**: I will use a **Sliding Window Log** algorithm stored in memory:
- **Structure**: Maintain a HashMap where keys are client IPs and values are double-ended queues (deques) containing request timestamps.
- **Checking Logic**:
  1. When a request arrives, get current time $T$.
  2. Retrieve the deque of timestamps for the client IP.
  3. Prune timestamps older than $T - 60$ seconds from the front of the deque.
  4. Check the size of the deque:
     - If size < 100: Append $T$ to the deque and allow the request.
     - If size $\ge$ 100: Deny the request.
- **Follow-up Questions**: What is the space complexity of this design? (Answer: $O(U \cdot W)$ where $U$ is active users and $W$ is the limit (100), as we store at most 100 timestamps per client).
- **Interviewer's Expectations**: Recommend Sliding Window Log, detail queue prunings, and calculate time/space complexities.

---

### Debugging Questions

#### 16. A binary search implementation runs into an infinite loop during testing. What is the most likely cause?
- **Detailed Answer**:
1. **Incorrect pointer updates**: The pointers are not updated correctly, for example, setting `lo = mid` or `hi = mid` instead of `lo = mid + 1` and `hi = mid - 1`. If the array has two elements and the target is at the end, `mid` remains equal to `lo` in integer division, causing `lo` to never update.
2. **Loop condition mismatch**: Using `while lo < hi` but returning `-1` inside, which misses the target when `lo == hi`.
- **Correction**: Always update pointers past the checked midpoint: `lo = mid + 1` and `hi = mid - 1`.
- **Follow-up Questions**: How do you fix mid-point calculations to prevent integer overflow? (Answer: Use `mid = lo + (hi - lo) // 2` instead of `(lo + hi) // 2`).
- **Interviewer's Expectations**: Spot incorrect mid-pointer assignments and recommend pointer updates past `mid`.

#### 17. A recursive DFS function throws a `StackOverflowError` on a graph with 20,000 nodes. Explain the cause and fix.
- **Detailed Answer**:
- **Cause**: The depth of the graph exceeds the execution stack limits of the thread. Each recursive call pushes a stack frame. If the graph is a long, linear chain of 20,000 nodes, recursion will go 20,000 frames deep, exceeding typical stack limits (which support ~1,000-5,000 frames).
- **Fix**: Convert the recursive DFS implementation into an **Iterative DFS** using an explicit, heap-allocated Stack collection:
  ```python
  def iterative_dfs(graph, start):
      visited = set()
      stack = [start]
      while stack:
          u = stack.pop()
          if u not in visited:
              visited.add(u)
              # Push unvisited neighbors to stack
              for v in graph.get(u, []):
                  if v not in visited:
                      stack.append(v)
  ```
- **Follow-up Questions**: Does this iterative approach consume less memory? (Answer: It consumes a similar amount of memory, but it stores nodes in heap memory, which is much larger than stack memory, avoiding overflow crashes).
- **Interviewer's Expectations**: Identify recursive depth limits and convert the algorithm to use an iterative stack.

#### 18. You implement a hash table, but notice that as elements are added, retrieval times slow down to $O(N)$ linear scans. What is the cause?
- **Detailed Answer**:
1. **Bad Hash Function**: The hash function maps keys to the same bucket index (hash collisions), causing all entries to be stored in a single bucket's linked list.
2. **Missing Resize Logic**: The hash table does not resize when its load factor threshold (e.g. 0.75) is exceeded. As keys increase, the average bucket list size grows linearly.
- **Fix**:
  - Implement a hash function that distributes keys uniformly across buckets (e.g., using prime numbers).
  - Implement table resizing: when the load factor threshold is reached, double the bucket array size and rehash all keys to the new bucket indices.
- **Follow-up Questions**: What is the collision complexity in Java 8+ HashMap? (Answer: Java 8+ converts bucket lists to red-black trees when collisions exceed 8, keeping worst-case lookup at $O(\log N)$).
- **Interviewer's Expectations**: Identify poor hash distributions and missing table resizing as causes of linear degradation.

#### 19. A sorting algorithm works correctly during local testing but crashes with memory limit exceptions on large datasets. What is the cause?
- **Detailed Answer**:
- **Cause**: The sorting algorithm is likely creating temporary array copies during execution (e.g., naive Merge Sort allocating new slice arrays at each recursion step). For large datasets, these allocations consume significant memory ($O(N \log N)$ total space if slices are not cleaned up), causing memory limits to be exceeded.
- **Fix**:
  1. Optimize Merge Sort to reuse a single temporary array across all recursive steps.
  2. Or switch to an **In-place sorting algorithm** (like Heap Sort or Quick Sort) that mutates the array elements directly within the original memory space, using $O(1)$ or $O(\log N)$ auxiliary space.
- **Follow-up Questions**: Is Quick Sort space complexity $O(1)$? (Answer: No. Quick Sort operates in-place but requires $O(\log N)$ stack space on average to store recursion calls).
- **Interviewer's Expectations**: Identify duplicate memory allocations in sort routines and recommend in-place sorting algorithms.

#### 20. Your binary search on a rotated sorted array fails to find the target on certain inputs. How do you troubleshoot?
- **Detailed Answer**:
- **Cause**: In a rotated sorted array, one half of the array relative to `mid` is always sorted, while the other half contains the rotation pivot. If your search checks values without identifying which half is sorted first, it will search the wrong range.
- **Troubleshooting Steps**:
  1. Verify if `arr[lo] <= arr[mid]` (indicates the left half is sorted).
  2. If left is sorted, check if target lies within the left boundaries (`arr[lo] <= target < arr[mid]`). If yes, search left (`hi = mid - 1`); otherwise search right.
  3. If left is not sorted, the right half must be sorted. Check if target lies within the right boundaries (`arr[mid] < target <= arr[hi]`). If yes, search right (`lo = mid + 1`); otherwise search left.
- **Follow-up Questions**: What happens if the array contains duplicate elements? (Answer: Duplicates make it impossible to determine which half is sorted in $O(1)$ time, degrading the search time complexity to $O(N)$ in the worst case).
- **Interviewer's Expectations**: Identify sorted halves, apply boundary checks, and handle rotation pivots correctly.

---

### System Design Questions

#### 21. Design a memory-efficient spell checker library.
- **Detailed Answer**:
- **Data Structure**: I will use a **Trie** or a **Bloom Filter**.
- **Bloom Filter (Primary Filter)**:
  - An extremely space-efficient probabilistic data structure.
  - Model: A bit array of size $M$ initialized to 0. Use $K$ independent hash functions to map words to bit positions, setting them to 1.
  - *Lookup*: Hash the input word. If any bit position is 0, the word is definitely misspelled. If all are 1, the word is likely correct (low false-positive rate, e.g., 1%).
- **Trie (Backup Suggestion Engine)**:
  - If the Bloom filter flags a misspelling, query a compressed Trie (like a Patricia Trie or Radix Tree) containing correct words to generate spelling suggestions (using Levenshtein edit distance searches).
- **Follow-up Questions**: Why not use a HashSet? (Answer: A HashSet containing 100,000 strings would consume tens of megabytes of RAM. A Bloom filter can achieve a 1% false positive rate using only a few hundred kilobytes).
- **Interviewer's Expectations**: Propose Bloom filters for space-efficient membership checks and Tries for generating corrections.

#### 22. Design a system to schedule and execute millions of tasks with specific execution timestamps in real-time.
- **Detailed Answer**:
- **Task Queue**: Use a **Min-Heap (Priority Queue)** where task keys are sorted by execution timestamp.
- **Data Store**: Store task payloads in a persistent database (e.g. DynamoDB), keeping only the PIDs and timestamps in the in-memory Min-Heap.
- **Scheduler Worker**:
  - Run a scheduler loop.
  - Peek at the root of the Min-Heap.
  - If `root.timestamp <= current_time`, pop the task and assign it to a thread worker pool for execution.
  - If `root.timestamp > current_time`, compute the wait duration: `wait_time = root.timestamp - current_time`. Put the scheduler thread to sleep for the duration using a conditional lock wait, waking up early if a new task with an earlier timestamp is inserted.
- **Follow-up Questions**: How do you prevent loss of tasks if the scheduler server crashes? (Answer: Write tasks to a persistent database before adding them to the heap. On reboot, reload tasks with pending timestamps back into the heap).
- **Interviewer's Expectations**: Recommend Min-Heaps for sorting tasks by execution time, and explain thread sleep-wake scheduling logic.

#### 23. Design an IP address routing table lookup engine that matches packets to routes in $O(1)$ or $O(L)$ time.
- **Detailed Answer**: IP routing requires finding the **Longest Prefix Match** (e.g. routing IP `192.168.1.5` to route `192.168.1.0/24` instead of `192.168.0.0/16`).
- **Data Structure**: A **Trie** structure where nodes represent bits of the IP address (0 or 1).
- **Lookup Process**:
  - Convert the target IP address to binary bits.
  - Traverse the Trie matching bits (0 or 1) sequentially.
  - Keep track of the last traversed node that matches a valid routing rule.
  - Once a mismatch occurs, return the routing rule associated with that node.
  - This guarantees finding the longest prefix match in $O(L)$ time where $L$ is the address bit length (32 bits for IPv4, 128 bits for IPv6), independent of the routing table size.
- **Follow-up Questions**: How does this compare to matching in a HashMap? (Answer: HashMap requires exact matches, so it cannot resolve prefix matches easily).
- **Interviewer's Expectations**: Recommend binary Tries for longest prefix matching and detail the bit-by-bit traversal logic.

---

## 10. Common Mistakes

- **Integer Overflow in Midpoint Calculations**: Writing `mid = (lo + hi) // 2` in binary search, which can cause integer overflow in static languages (like Java/C++) if `lo + hi` exceeds the maximum integer limit. Use `mid = lo + (hi - lo) // 2`.
- **Ignoring Recursion Stack Space**: Calculating the space complexity of recursive algorithms as $O(1)$ because they do not allocate new variables, ignoring the memory consumed by recursive stack frames ($O(D)$ space, where $D$ is the recursion depth).
- **Confusing BFS and DFS implementations**: Using a Queue for DFS or a Stack for BFS, resulting in incorrect graph traversal behavior.
- **Choosing LinkedList for Random Access**: Using a `LinkedList` for tasks requiring random index access, which degrades access times from $O(1)$ to $O(N)$ linear scans.
- **Omitting Base Cases in Recursion**: Forgetting to define a base case in recursive functions, resulting in infinite loops and stack overflow crashes.

---

## 11. Comparison Section: Data Structures & Sorting

### Data Structure Time Complexities
| Structure | Access | Search | Insertion | Deletion | Best Use Case |
|---|---|---|---|---|---|
| **Array** | $O(1)$ | $O(N)$ | $O(N)$ | $O(N)$ | Contiguous records, lookup by index. |
| **LinkedList** | $O(N)$ | $O(N)$ | $O(1)$ | $O(1)$ | Queue buffers, frequent inserts/deletes at ends. |
| **HashMap** | N/A | $O(1)$ | $O(1)$ | $O(1)$ | Key-value indexing, fast caching. |
| **BST** | $O(\log N)$ | $O(\log N)$ | $O(\log N)$ | $O(\log N)$| Sorted records, range queries. |
| **Trie** | $O(L)$ | $O(L)$ | $O(L)$ | $O(L)$ | Autocomplete engines, IP prefix lookups. |
| **Min-Heap** | $O(1)$ (min) | $O(N)$ | $O(\log N)$ | $O(\log N)$| Priority queues, task schedulers. |

### Sorting Algorithm Resource Profiles
| Algorithm | Best Case | Average Case | Worst Case | Space Complexity | Stable? | In-Place? |
|---|---|---|---|---|---|---|
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Yes | No |
| **Quick Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ (stack) | No | Yes |
| **Heap Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(1)$ | No | Yes |
| **Bubble Sort**| $O(N)$ | $O(N^2)$ | $O(N^2)$ | $O(1)$ | Yes | Yes |

---

## 12. Practical Project Ideas

### Beginner: Standard Stack and Queue Implementations
Build custom Stack and Queue classes in Python without using list manipulation helpers (like `.pop(0)` or `.insert()`). Use a raw array of fixed size and manage pointers (`head`, `tail`) manually, handling boundary overflow checks.

### Intermediate: In-Memory LRU Cache from Scratch
Write an in-memory cache class in Python. Combine a custom Doubly Linked List class and a HashMap. Write unit tests simulating concurrent reads, writes, and verify that elements are evicted correctly in least-recently-used order when cache limits are reached.

### Advanced/Resume-worthy: Trie-based Autocomplete Engine with Prefix Search
Build a web autocomplete API. Index 100,000 search terms from a CSV file into a Trie. Configure nodes to store pre-compiled top suggestions. Expose a `/search` endpoint that returns matching suggestions in under 5 milliseconds.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless execution of binary search, understanding Big-O notation time/space differences, and identifying when to use HashMaps vs Arrays.
- **What Engineering Teams expect**: Familiarity with classic LeetCode patterns (two pointers, sliding window, DFS/BFS graph traversals, and dynamic programming), and ability to write clean code handling edge cases.

---

## 14. Cheat Sheet

- **Midpoint calculation**: `mid = lo + (hi - lo) // 2` (prevents integer overflow).
- **BFS vs. DFS**:
  - BFS uses a Queue (FIFO). Best for shortest paths.
  - DFS uses a Stack (LIFO) or recursion. Best for cycle detection.
- **Heap updates**:
  - Peek Min: $O(1)$.
  - Push/Pop: $O(\log N)$.
- **DSU Operations**: Path compression + Union by rank yields near-constant $O(\alpha(N))$ amortized time.

---

## 15. One-Day Revision Guide

- [ ] Implement iterative and recursive binary search from memory.
- [ ] Write a stack-based parentheses validator.
- [ ] Detail the internal workings of an LRU Cache.
- [ ] Compare the resource trade-offs of Merge Sort and Quick Sort.
- [ ] Trace a BFS graph search on paper, detailing queue changes.
- [ ] Write the recurrence relation and code for the Coin Change DP problem.
