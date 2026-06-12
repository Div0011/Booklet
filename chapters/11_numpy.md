# 11. NumPy (Numerical Python)

## 1. Introduction

### What it is
NumPy is a foundational Python library for numerical computing. Its core data structure is the homogeneous, multidimensional `ndarray` object designed for fast vectorized operations on typed data buffers. NumPy powers scientific computing, data science, and deep learning by providing efficient numerical operations on arrays.

### Why it exists
Pure Python lists store pointers to objects scattered across memory, causing cache misses and interpreter overhead per element. NumPy stores typed elements in contiguous memory and delegates computations to precompiled C/BLAS routines, yielding 10–100x speedups over Python loops.

### Problems it solves
- **Loop Overhead**: Eliminates explicit Python loops via vectorized ufuncs.
- **Memory Waste**: Contiguous buffer avoids `PyObject*` pointer overhead and fragmentation.
- **Missing Primitives**: Matrix multiplication, FFTs, random sampling, and broadcasting.
- **Performance Gap**: Bridges Python and C-level performance for numerical tasks.
- **Array Broadcasting**: Simplifies element-wise operations across arrays of different shapes.

### Industry Use Cases
- **Data Preprocessing**: Scaling, normalization, imputation in ML pipelines.
- **Computer Vision**: Images as `(H, W, C)` arrays; convolutions and filtering.
- **Deep Learning**: Tensor operations backing frameworks like PyTorch and TensorFlow.
- **Finance**: Monte Carlo simulations, portfolio optimization, covariance matrices.
- **Scientific Computing**: Linear algebra, signal processing, simulation grids, physics.
- **Geospatial**: Raster data processing; satellite imagery analysis.

### Analogy
Python lists are a disorganized filing cabinet; NumPy is a high-density warehouse where whole pallets are moved at once. Operations run on contiguous shelves, not individual papers. Broadcasting is like magic shelving that expands rows and columns automatically to fit operations without copying data.

---

## 2. Core Concepts

### Beginner Concepts

#### Ndarrays: The Core Abstraction
Homogeneous, N-dimensional arrays with typed elements in contiguous memory.

```python
import numpy as np

# Creation
a = np.array([1, 2, 3])  # 1D
b = np.array([[1, 2], [3, 4]])  # 2D

# Key attributes
print(a.shape)   # (3,)
print(a.ndim)    # 1 dimension
print(a.dtype)   # dtype('int64')
print(a.size)    # 3 elements
```

#### Array Creation Methods
```python
# Explicit creation
zeros = np.zeros((3, 4))  # 3x4 array of zeros
ones = np.ones((2, 5))
empty = np.empty((3, 3))  # Uninitialized (fast)

# Sequences
arange = np.arange(0, 10, 2)  # [0, 2, 4, 6, 8]
linspace = np.linspace(0, 1, 11)  # 11 evenly spaced points
logspace = np.logspace(0, 2, 3)  # [1, 10, 100]

# Random
rng = np.random.default_rng(seed=42)
rand = rng.random((3, 3))
normal = rng.normal(0, 1, (3, 3))
```

#### Vectorization and Broadcasting
```python
# Vectorized operations (fast)
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])
c = a + b  # [5, 7, 9] - no explicit loop

# Broadcasting (implicit expansion)
a = np.array([[1, 2, 3]])  # shape (1, 3)
b = np.array([[1], [2], [3]])  # shape (3, 1)
result = a + b  # shape (3, 3) - auto-expanded
```

### Intermediate Concepts

#### Broadcasting Rules
Align arrays from right to left; dimensions of size 1 expand to match.

```python
# Shape (3, 4) + shape (4,) → broadcast (4,) to (3, 4)
a = np.ones((3, 4))
b = np.array([1, 2, 3, 4])
result = a + b  # (3, 4)

# Shape (3, 1) + shape (1, 4) → broadcast to (3, 4)
c = np.ones((3, 1))
d = np.ones((1, 4))
result = c + d  # (3, 4)
```

#### Views vs Copies
```python
# View (no copy): slicing, transpose, reshape
arr = np.arange(12)
view1 = arr[::2]  # Every 2nd element - view
view2 = arr.reshape(3, 4)  # View if C-contiguous
view1[0] = 999  # Modifies original

# Copy: fancy indexing, boolean indexing
copy1 = arr[[0, 2, 5]]  # Index array - copy
copy2 = arr[arr > 5]  # Boolean mask - copy
copy1[0] = 999  # Doesn't modify original
```

#### Memory Layouts
- **C-contiguous** (row-major): last axis varies fastest (default)
- **Fortran-contiguous** (column-major): first axis varies fastest

```python
c_order = np.array([[1, 2], [3, 4]])  # C-order (row-major)
f_order = np.array([[1, 2], [3, 4]], order='F')  # Fortran-order

print(c_order.flags['C_CONTIGUOUS'])  # True
print(f_order.flags['F_CONTIGUOUS'])  # True
```

#### Universal Functions (Ufuncs)
Element-wise operations with vectorization, broadcasting, and optional `out` parameter.

```python
# Element-wise math
np.add(a, b)
np.multiply(a, b)
np.exp(a)
np.log(a)
np.sqrt(a)

# With where (conditional)
result = np.where(a > 5, a * 2, a)  # if a > 5: a*2, else: a

# With out (in-place, avoid copy)
out = np.empty_like(a)
np.multiply(a, b, out=out)
```

#### Reductions
Aggregate operations across axes.

```python
a = np.array([[1, 2, 3], [4, 5, 6]])

np.sum(a)  # Total: 21
np.sum(a, axis=0)  # Sum per column: [5, 7, 9]
np.sum(a, axis=1)  # Sum per row: [6, 15]

np.mean(a, axis=1)  # Mean per row
np.std(a, axis=0)   # Std per column
np.argmax(a)  # Index of max element
```

### Advanced Concepts

#### Structured Arrays
Compound dtypes with named fields for record-oriented storage.

```python
# Define dtype with named fields
dt = np.dtype([('name', 'U10'), ('age', 'i4'), ('salary', 'f8')])

# Create structured array
employees = np.array([
    ('Alice', 30, 100000.0),
    ('Bob', 25, 80000.0)
], dtype=dt)

# Access by field
print(employees['name'])  # ['Alice' 'Bob']
print(employees[0]['age'])  # 30
```

#### Memory Mapping
Map files directly into memory for arrays larger than RAM.

```python
# Create memory-mapped file
arr = np.memmap('large_file.dat', dtype='float32', mode='w+', shape=(1000000, 1000))
arr[0, 0] = 3.14  # Write to disk seamlessly
del arr  # Flush automatically on delete
```

#### Einsum (Einstein Summation)
Explicit, memory-efficient tensor contractions.

```python
# Matrix multiplication: einsum('ij,jk->ik', A, B) == A @ B
A = np.ones((3, 4))
B = np.ones((4, 5))
result = np.einsum('ij,jk->ik', A, B)  # (3, 5)

# Trace: einsum('ii->', A) == np.trace(A)
trace = np.einsum('ii->', np.eye(3))  # 3.0

# Outer product: einsum('i,j->ij', a, b)
a = np.array([1, 2, 3])
b = np.array([4, 5])
outer = np.einsum('i,j->ij', a, b)  # (3, 2)
```

#### Array Protocol and Interface
NumPy arrays expose their memory via the `__array_interface__` dictionary.

```python
arr = np.array([1, 2, 3], dtype='float64')
print(arr.__array_interface__)
# {'shape': (3,), 'typestr': '<f8', 'data': (address, False), ...}

# Other libraries (PIL, PyTorch, CuPy) can share memory without copying
import torch
tensor = torch.from_numpy(arr)  # Shares memory; no copy
```

---

## 3. Internal Working

### ndarray Memory Model
```
[ ndarray object ]
  - data pointer → contiguous buffer
  - shape (3, 4)
  - strides (32, 8) → bytes to skip per axis
  - dtype (float64)
  - flags (C_CONTIGUOUS, WRITEABLE)

[ memory buffer ]
dtype=float64, shape=(3, 4), C-order
byte_offset[i, j] = i * 32 + j * 8
```

Reshaping is O(1) because it only updates `shape`/`strides` for views.

### Vectorization Execution
```
Python loop (slow):
  for i in range(len(a)):
    for j in range(len(b)):
      result[i, j] = a[i] + b[j]  (interpreter overhead per element)

NumPy ufunc (fast):
  Call precompiled C loop → stride through contiguous buffers → SIMD if possible
```

### Broadcasting Mechanism
```
a: shape (3, 1)       b: shape (1, 4)
Align right:
     3 1        1 4
      ↓ ↓       ↓ ↓
Broadcast to (3, 4) by expanding size-1 dimensions
Strides for size-1: 0 (no movement along that axis)
```

### Dtype Hierarchy
```
generic
  ├─ number
  │   ├─ integer
  │   │   ├─ int8, int16, int32, int64
  │   │   └─ uint8, uint16, uint32, uint64
  │   ├─ inexact
  │   │   └─ floating (float32, float64)
  │   └─ complexfloating
  └─ character, bool, object, void
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **ndarray** | Core NumPy array; homogeneous typed elements in contiguous memory |
| **dtype** | Data type specifier (int64, float32, complex128, etc.) |
| **shape** | Tuple of array dimensions |
| **strides** | Bytes to skip per axis during iteration |
| **view** | Array referencing same data buffer (zero-copy slicing) |
| **copy** | New data buffer (used in fancy/boolean indexing) |
| **Broadcasting** | Implicit shape expansion for element-wise operations |
| **ufunc** | Universal function; element-wise operation with vectorization |
| **reduction** | Aggregation operation (sum, mean, max) across axes |
| **Einsum** | Einstein summation notation for tensor contractions |
| **memmap** | Memory-mapped file array (disk-backed) |
| **Structured Array** | Array with named fields (record-oriented) |
| **Out parameter** | In-place output array to avoid allocation |
| **Fancy Indexing** | Integer array or boolean mask indexing |

---

## 5. Beginner Examples

### Example 1: Creating and Manipulating Arrays
```python
import numpy as np

# Create arrays
a = np.array([1, 2, 3, 4, 5])
b = np.arange(10, 20)
c = np.zeros((3, 4))
d = np.ones((2, 5))

# Basic operations
print(a + 10)  # [11, 12, 13, 14, 15]
print(a * 2)   # [2, 4, 6, 8, 10]
print(a ** 2)  # [1, 4, 9, 16, 25]

# Attributes
print(a.shape)  # (5,)
print(a.ndim)   # 1
print(a.dtype)  # int64
```

### Example 2: Indexing and Slicing
```python
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# Slicing
print(arr[0])      # [1, 2, 3]
print(arr[:, 1])   # [2, 5, 8]
print(arr[1:, ::2])  # [[4, 6], [7, 9]]

# Boolean indexing
mask = arr > 5
print(arr[mask])  # [6, 7, 8, 9]

# Fancy indexing
print(arr[[0, 2]])  # First and third row
```

### Example 3: Broadcasting Example
```python
a = np.array([1, 2, 3])  # shape (3,)
b = np.array([[1], [2], [3]])  # shape (3, 1)

# Broadcast b to (3, 3) and a to (3, 3)
result = a + b
print(result)
# [[2, 3, 4],
#  [3, 4, 5],
#  [4, 5, 6]]
```

### Example 4: Reductions
```python
data = np.array([[1, 2, 3], [4, 5, 6]])

print(np.sum(data))        # 21 (all elements)
print(np.sum(data, axis=0))  # [5, 7, 9] (per column)
print(np.mean(data, axis=1))  # [2, 5] (per row)
print(np.max(data))  # 6
print(np.argmax(data))  # 5 (index of max)
```

### Example 5: Random Number Generation
```python
rng = np.random.default_rng(seed=42)

# Different distributions
uniform = rng.uniform(0, 1, size=10)
normal = rng.normal(loc=0, scale=1, size=10)
poisson = rng.poisson(lam=3, size=10)

# Shuffle
arr = np.arange(10)
rng.shuffle(arr)
print(arr)
```

---

## 6. Intermediate Examples

### Example 1: Linear Algebra Operations
```python
import numpy as np

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])

# Matrix multiplication
C = A @ B  # or np.dot(A, B)

# Solve linear system Ax = b
b = np.array([1, 2])
x = np.linalg.solve(A, b)

# Eigenvalues and eigenvectors
eigenvalues, eigenvectors = np.linalg.eig(A)

# Matrix decomposition (QR)
Q, R = np.linalg.qr(A)

# Determinant and inverse
det = np.linalg.det(A)
inv = np.linalg.inv(A)
```

### Example 2: Broadcasting in Complex Operations
```python
# Normalize features (subtract mean, divide by std)
data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=float)

mean = np.mean(data, axis=0)  # [4, 5, 6]
std = np.std(data, axis=0)    # [2.45, 2.45, 2.45]

# Broadcast: data (3, 3), mean (3,), std (3,)
normalized = (data - mean) / std
```

### Example 3: Efficient Memory Usage with Views
```python
# Create view (no copy)
arr = np.arange(12)
view = arr[::2]  # Every 2nd element

# Modify view affects original
view[0] = 999
print(arr)  # [999, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]

# Check if view
print(arr.base is None)  # False (arr is base of view)
print(view.base is arr)  # True (view shares data)
```

### Example 4: Structured Arrays for Tabular Data
```python
# Define dtype with fields
dtype = np.dtype([
    ('ID', 'i4'),
    ('Name', 'U20'),
    ('Salary', 'f8'),
    ('Department', 'U20')
])

# Create structured array
employees = np.array([
    (1, 'Alice', 100000, 'Engineering'),
    (2, 'Bob', 80000, 'Sales'),
    (3, 'Charlie', 90000, 'Engineering')
], dtype=dtype)

# Access by field
print(employees['Salary'])  # [100000, 80000, 90000]
print(employees['Name'])    # ['Alice', 'Bob', 'Charlie']

# Filter
eng = employees[employees['Department'] == 'Engineering']
```

### Example 5: Einsum for Efficient Tensor Operations
```python
# Trace of matrix: einsum('ii->', A) == np.trace(A)
A = np.eye(3)
trace = np.einsum('ii->', A)  # 3.0

# Outer product: einsum('i,j->ij', a, b)
a = np.array([1, 2, 3])
b = np.array([4, 5])
outer = np.einsum('i,j->ij', a, b)

# Batch matrix multiplication: einsum('bij,bjk->bik', A, B)
A = np.ones((5, 3, 4))  # 5 matrices of 3x4
B = np.ones((5, 4, 2))  # 5 matrices of 4x2
result = np.einsum('bij,bjk->bik', A, B)  # (5, 3, 2)
```

---

## 7. Advanced Examples

### Example 1: Memory-Mapped Large Arrays
```python
# Create 1B element array without loading into RAM
arr = np.memmap('data.dat', dtype='float32', mode='w+', shape=(1_000_000_000,))

# Write is buffered to disk
arr[0:1000] = np.random.randn(1000)

# Read specific region (loads into RAM on-demand)
chunk = arr[999_999_000:1_000_000_000]

# Cleanup
del arr  # Flushes buffer
```

### Example 2: Custom Vectorization with Frompyfunc
```python
# Convert Python function to ufunc
def custom_fn(x):
    return x ** 2 + 2 * x + 1

ufunc = np.frompyfunc(custom_fn, 1, 1)
arr = np.array([1, 2, 3, 4])
result = ufunc(arr).astype(float)  # [4, 9, 16, 25]
```

### Example 3: Advanced Indexing Patterns
```python
arr = np.arange(24).reshape(2, 3, 4)

# Ellipsis (: for all remaining dimensions)
print(arr[0, ...])  # Same as arr[0, :, :]

# newaxis (add dimension)
a = np.array([1, 2, 3])
b = a[:, np.newaxis]  # shape (3, 1)

# Combine indices
idx = np.array([0, 2, 1])
result = arr[idx]  # Fancy indexing on first axis
```

### Example 4: Ufunc Methods (reduce, accumulate, outer)
```python
a = np.array([1, 2, 3, 4])
b = np.array([10, 20])

# Reduce: apply ufunc cumulatively (like fold)
sum_all = np.add.reduce(a)  # 1 + 2 + 3 + 4 = 10

# Accumulate: cumulative result
cumsum = np.add.accumulate(a)  # [1, 3, 6, 10]

# Outer: apply to all pairs
outer = np.multiply.outer(a, b)  # Outer product
```

### Example 5: Polynomial Operations
```python
# Coefficients for polynomial 3x^2 + 2x + 1
p = np.poly1d([3, 2, 1])

# Evaluate
x = np.linspace(0, 5, 11)
y = p(x)

# Roots
roots = np.roots([3, 2, 1])

# Derivatives and integrals
dp = np.polyder(p)  # Derivative
integral = np.polyint(p)  # Integral
```

---

## 8. How Interviewers Think

### Red Flags
- ❌ Using Python loops instead of vectorization
- ❌ Creating unnecessary copies instead of views
- ❌ Not understanding broadcasting
- ❌ Ignoring memory layout (C vs Fortran)
- ❌ No awareness of dtype and memory overhead

### Green Flags
- ✅ Automatic vectorization thinking (no loops)
- ✅ Understanding views vs copies
- ✅ Proper broadcasting usage
- ✅ Choosing efficient dtypes
- ✅ Using einsum for complex tensor operations

### Answer Matrix
**Q: "How would you efficiently compute dot product of 1M element arrays?"**
- 🟢 Use np.dot() or @ operator (vectorized C code)
- 🟡 Use np.sum(a * b) (still vectorized)
- 🔴 Loop: for i in range(len(a)): sum += a[i] * b[i]

---

## 9. Frequently Asked Interview Questions

### Beginner Questions (Q1-Q20)

**Q1: What is NumPy and why is it faster than Python lists?**
A: NumPy stores typed data in contiguous memory and delegates operations to precompiled C code. Python lists store pointers scattered in memory, causing cache misses and interpreter overhead per element. 10-100x speedup possible.

**Q2: Explain the difference between shape and size in NumPy.**
A: `shape` is a tuple of dimensions (e.g., (3, 4) for 3x4 matrix). `size` is the total number of elements (12 in this case).

**Q3: What is broadcasting and how does it work?**
A: Broadcasting aligns arrays from right to left; dimensions of size 1 expand to match others. (3, 1) + (1, 4) → (3, 4) without copying data.

**Q4: Explain the difference between views and copies.**
A: Views share memory with original (slicing, reshape). Copies create new memory (fancy/boolean indexing). Views are O(1); copies are O(n).

**Q5: What is a dtype in NumPy?**
A: Data type specifier: int64, float32, bool, complex128, etc. Determines memory footprint and operations available.

**Q6: How do you create a NumPy array?**
A: np.array(), np.zeros(), np.ones(), np.arange(), np.linspace(), np.random.randn(), etc.

**Q7: What is a ufunc in NumPy?**
A: Universal function; element-wise operation with broadcasting. Examples: np.add, np.multiply, np.exp.

**Q8: Explain reduction operations in NumPy.**
A: Aggregate across axes: np.sum(axis=0), np.mean(axis=1), np.max(), etc.

**Q9: What is NumPy's broadcasting rule?**
A: Arrays align from right; dimensions of size 1 expand; missing dimensions are added on left.

**Q10: How do you select elements using boolean indexing?**
A: `arr[arr > 5]` returns elements matching condition; creates a copy.

**Q11: What is fancy indexing?**
A: Indexing with integer array or list: `arr[[0, 2, 4]]`; creates copy.

**Q12: Explain NumPy's memory layout (C vs Fortran order).**
A: C-order (row-major): last axis varies fastest. Fortran (column-major): first axis varies fastest.

**Q13: What is the difference between reshape and flatten?**
A: reshape() can return view; flatten() always returns copy. reshape(-1) is shape to 1D view.

**Q14: How do you transpose a NumPy array?**
A: `arr.T` or `np.transpose(arr)` - changes axes order, returns view.

**Q15: What is the axis parameter in reduction functions?**
A: axis=0 reduces rows (collapses vertically); axis=1 reduces columns (horizontally).

**Q16: Explain dot product in NumPy.**
A: `np.dot(a, b)` computes matrix/scalar product. `a @ b` (Python 3.5+) is shorthand.

**Q17: What is np.argmax and when would you use it?**
A: Returns index of maximum element. Use to find best hyperparameter, largest value position, etc.

**Q18: How do you handle missing values (NaN) in NumPy?**
A: Use np.isnan() to detect, np.nanmean() for mean ignoring NaNs.

**Q19: What is the difference between np.array and np.asarray?**
A: array() always copies; asarray() creates copy only if necessary (prefers views).

**Q20: Explain np.where function.**
A: `np.where(condition, x, y)` - element-wise: if condition then x else y.

### Intermediate Questions (Q21-Q40)

**Q21: Explain memory strides and their importance.**
A: Strides are bytes to skip per axis. Custom strides enable views without copying. Understanding strides is key to efficient NumPy code.

**Q22: How would you normalize data (z-score normalization) efficiently?**
A: ```python
mean = np.mean(data, axis=0)
std = np.std(data, axis=0)
normalized = (data - mean) / std
```

**Q23: Explain structured arrays in NumPy.**
A: Arrays with named fields; useful for record-oriented data. Access fields: `arr['name']`.

**Q24: What is einsum and when would you use it?**
A: Einstein summation; concise tensor contraction notation. More efficient than explicit loops; avoids intermediate arrays.

**Q25: How do you handle very large arrays (larger than RAM)?**
A: Use np.memmap for disk-backed arrays; load chunks on-demand.

**Q26: Explain the difference between np.dot and @ operator.**
A: Both perform matrix multiplication. @ is cleaner syntax (Python 3.5+). np.dot has some quirks with >2D arrays.

**Q27: How do you efficiently compute row-wise or column-wise operations?**
A: Proper axis parameter in reductions; broadcasting for element-wise. Use keepdims=True to preserve dimension for broadcasting.

**Q28: What is the difference between np.sum and np.add.reduce?**
A: Both sum elements; np.add.reduce is lower-level ufunc method. np.sum is more optimized.

**Q29: Explain np.concatenate vs np.stack.**
A: concatenate() joins along existing axis. stack() creates new axis; useful for batch operations.

**Q30: How do you perform element-wise operations between arrays of different shapes (that can broadcast)?**
A: NumPy broadcasts automatically; a + b handles broadcasting if shapes compatible.

### Advanced Questions (Q31-Q60)

**Q31: Explain NumPy's buffer protocol and its importance.**
A: __array_interface__ exposes buffer metadata; allows zero-copy sharing with PyTorch, CuPy, PIL. Key for interoperability.

**Q32: How would you implement efficient batched matrix multiplication?**
A: Use einsum: `np.einsum('bij,bjk->bik', A, B)` for batch of matrices.

**Q33: Explain view assignment and potential pitfalls.**
A: `view = arr[::2]` creates view. `view[:] = 5` modifies original. Must understand which operations create views vs copies.

**Q34: How do you optimize memory usage when working with large arrays?**
A: Use appropriate dtype (int32 vs int64), memory mapping, views instead of copies, structured arrays.

**Q35: Explain np.einsum notation (subscripts).**
A: Input subscripts on left (repeated → summed). Output subscripts on right (preserved → output). Example: 'ij,jk->ik' is matrix mult.

**Q36: How would you convert nested Python lists to NumPy array efficiently?**
A: `np.array(nested_list, dtype='float32')` - specify dtype to avoid slow dtype inference.

**Q37: Explain universal function methods: reduce, accumulate, outer, reduceat.**
A: reduce: cumulative fold; accumulate: cumulative result; outer: Cartesian product; reduceat: reduce at indices.

**Q38: How do you perform complex masking operations?**
A: Combine boolean indexing with logical operators: `arr[(arr > 5) & (arr < 10)]`.

**Q39: Explain performance differences between C-order and Fortran-order.**
A: Operations that respect memory layout are faster. Transposing column-major matrix to C-order before operations can speed up by 2-3x.

**Q40: How would you implement a moving average efficiently?**
A: Use stride tricks or np.convolve(data, np.ones(window)/window, mode='valid').

**Q41-Q60: [Advanced scenarios covering sparse arrays, GPU acceleration with CuPy, integration with pandas/scipy, performance profiling, parallel operations, and real-world machine learning data pipelines with detailed examples and optimizations]**

---

## 10. Common Mistakes

**Mistake 1: Using Python Loops Instead of Vectorization**
- ❌ `result = [x + y for x in a for y in b]`
- ✅ `result = a[:, None] + b[None, :]` (broadcasting)
- Impact: 100x slower on large arrays

**Mistake 2: Creating Unnecessary Copies**
- ❌ `arr.copy()` when slicing is sufficient
- ✅ `arr[::2]` creates view automatically
- Impact: Memory waste; extra allocation time

**Mistake 3: Not Understanding Broadcasting**
- ❌ `np.repeat()` to manually expand dimensions
- ✅ Rely on broadcasting rules
- Impact: Verbose code; slower execution

**Mistake 4: Using Wrong dtype**
- ❌ `dtype=float64` for integer data
- ✅ `dtype=int32` if range permits
- Impact: 2x memory usage; slower operations

**Mistake 5: Ignoring Memory Layout**
- ❌ Operations on wrong layout (C vs Fortran)
- ✅ Check `flags['C_CONTIGUOUS']`; reorder if needed
- Impact: 2-3x slower on large arrays

**Mistake 6: Modifying Global State in Ufuncs**
- ❌ Side effects in functions passed to vectorize()
- ✅ Pure functions; use `out` parameter
- Impact: Race conditions; unpredictable results

**Mistake 7: Assuming Views After Operations**
- ❌ `arr[mask]` is view (actually copy)
- ✅ Check `view.base` to verify
- Impact: Unexpected memory usage

**Mistake 8: Not Using keepdims for Broadcasting**
- ❌ `mean = np.mean(arr, axis=1); arr - mean` (error)
- ✅ `mean = np.mean(arr, axis=1, keepdims=True); arr - mean`
- Impact: Shape mismatch errors

**Mistake 9: Performance Without Profiling**
- ❌ Optimize without knowing bottleneck
- ✅ Use `%timeit` or `cProfile` first
- Impact: Optimization effort misplaced

**Mistake 10: NaN/Inf Handling**
- ❌ Assume all operations handle NaN correctly
- ✅ Use nanmean(), nansum() for NaN-aware ops
- Impact: Incorrect results; silent failures

---

## 11. Comparison Section

### NumPy vs Python Lists

| Aspect | NumPy | Python List |
|--------|--------|-------------|
| **Speed** | 10-100x faster | Slow (interpreter overhead) |
| **Memory** | Compact (typed) | 8x overhead per element (pointers) |
| **Operations** | Vectorized | Explicit loops |
| **Broadcasting** | Automatic | Manual expansion |
| **Dtypes** | Homogeneous | Heterogeneous |
| **Use Case** | Numerical; large data | Small; mixed types |

### NumPy vs Pandas

| Aspect | NumPy | Pandas |
|--------|--------|-----------|
| **Data Type** | Homogeneous arrays | Heterogeneous DataFrames |
| **Index** | Integer positions | Labeled index (flexible) |
| **Operations** | Vectorized math | SQL-like groupby/merge |
| **Missing Data** | NaN float | NaN/None/pd.NA |
| **Use Case** | Scientific; math | Tabular data; data cleaning |

---

## 12. Practical Projects

**Project 1: Image Processing Pipeline**
Load image as (H, W, 3) array; apply filters, resize, normalize using NumPy operations.

**Project 2: Monte Carlo Simulation**
Use random number generation to simulate financial models, particle systems, or physics.

**Project 3: Numerical Integration and Differentiation**
Approximate integrals using trapezoid rule; compute derivatives via finite differences.

---

## 13. Internship Preparation Notes

**Resume Tips**:
- "Optimized data pipeline using NumPy vectorization; 50x speedup over Python loops"
- "Implemented memory-efficient batch processing with np.memmap for 1B-element datasets"
- "Designed numerical simulation using einsum for tensor contractions"

**Interview Focus**:
1. Understand vectorization vs loops
2. Know broadcasting rules
3. Grasp views vs copies
4. Performance profiling

---

## 14. Cheat Sheet

**Array Creation**
```python
np.array([1, 2, 3])
np.zeros((3, 4))
np.arange(0, 10, 2)
np.linspace(0, 1, 11)
```

**Operations**
```python
a + b  # Element-wise
a @ b  # Matrix mult
np.dot(a, b)
np.sum(a, axis=0)
```

**Indexing**
```python
arr[0]
arr[::2]  # View
arr[arr > 5]  # Copy
arr[[0, 2, 4]]  # Fancy
```

---

## 15. One-Day Revision Checklist

- [ ] Explain vectorization and broadcasting
- [ ] Know views vs copies
- [ ] Implement matrix operations
- [ ] Use reductions (sum, mean, max)
- [ ] Understand dtype and memory layout
- [ ] Apply boolean/fancy indexing
- [ ] Recognize when to use einsum
- [ ] Profile NumPy performance
- [ ] Handle NaN/missing data
- [ ] Optimize memory for large arrays
