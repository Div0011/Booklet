# 1. Python (Core Programming)

## 1. Introduction

### What it is
Python is a high-level, interpreted, dynamically typed, garbage-collected programming language supporting object-oriented, functional, and procedural paradigms. It compiles to bytecode at import time and executes within the Python Virtual Machine (PVM), which translates bytecode to machine instructions at runtime.

### Why it exists
Created by Guido van Rossum in the late 1980s, Python prioritizes code readability, developer productivity, and clean syntax. It bridges readable scripting and high-performance C/C++ libraries. Python was born from frustration with shell scripting complexity and C's verbosity.

### Problems it solves
- **Syntax Bloat**: Eliminates boilerplate from C++/Java (no static types, no semicolons). A 200-line Java program becomes 30 lines in Python.
- **Manual Memory Management**: Automated GC prevents segfaults and dangling pointers.
- **Prototyping Bottlenecks**: Rapid development with batteries-included stdlib (json, re, datetime, collections, itertools, functools).
- **Cross-platform Consistency**: Code runs on Linux, macOS, Windows without recompilation.
- **Integration with C/C++**: NumPy, PyTorch, TensorFlow are thin Python wrappers around C libraries, enabling fast computation.

### Industry Use Cases
- **AI/ML**: TensorFlow, PyTorch, scikit-learn are Python-first. Most ML research defaults to Python.
- **Backend**: FastAPI, Django, Flask used by Netflix, Spotify, Dropbox.
- **Automation**: ETL pipelines (Airflow, Luigi), DevOps (Ansible), cloud infrastructure (boto3).
- **Finance**: Algorithmic trading backtesting, risk analytics, portfolio optimization (cvxpy).
- **Scientific Computing**: Simulation physics, signal processing, bioinformatics, spatial analysis.
- **Data Science**: Jupyter notebooks, pandas, matplotlib make data exploration interactive.

### Analogy
Think of Python as a **project manager** translating high-level business requirements into detailed worker instructions. Managers stay at 10,000-foot view (your readable Python code), delegating low-level work to warehouse workers (C/C++ libraries). Python orchestrates; C libraries compute at scale.

---

## 2. Core Concepts

### Beginner Concepts

#### Predefined Keywords
Python has a set of predefined keywords (such as `def`, `class`, `yield`, `await`, `async`, `global`, `nonlocal`, `lambda`, `pass`, etc.) that hold special meanings and cannot be used as identifiers (variable or function names).
- `global`: Declares that a variable inside a function is at the module level.
- `nonlocal`: Used inside nested functions to rebind a variable in the nearest outer enclosing scope (excluding global scope).
- `pass`: A null statement used as a placeholder where syntactically a statement is required but no action is needed.

#### Operators & Type Casting
- **Operators**: Python supports:
  - *Arithmetic*: `+`, `-`, `*`, `/`, `%`, `**` (exponentiation), `//` (floor division).
  - *Comparison*: `==`, `!=`, `>`, `<`, `>=`, `<=`.
  - *Logical*: `and`, `or`, `not`.
  - *Bitwise*: `&` (AND), `|` (OR), `^` (XOR), `~` (NOT), `<<` (left shift), `>>` (right shift).
- **Type Casting**:
  - *Implicit*: Python automatically coerces types when safe (e.g., `3 + 4.5` results in a float `7.5`).
  - *Explicit*: Manual conversion using constructors like `int()`, `float()`, `str()`, `list()`, `set()`, `dict()`.

#### Conditionals & Loops
- **Conditionals**: `if`, `elif`, and `else` blocks handle branching logic based on boolean evaluations.
- **Loops**:
  - `for`: Iterates over a sequence. Supports an optional `else` block which runs if the loop completes without hitting a `break`.
  - `while`: Repeatedly executes as long as a condition is true. Also supports `else`.
  - **Loop Control**: `break` exits the loop immediately; `continue` skips the rest of the current iteration and goes to the next.

#### Data Structures & Core Types
- **Strings**: Immutable sequences of Unicode characters. Supports format engines (`f-strings`, `.format()`, `%`), slicing (`[start:stop:step]`), and operations like `.split()`, `.join()`.
- **Lists**: Mutable dynamic arrays with amortized $O(1)$ insertions.
- **Tuples & Sets**: Tuples are immutable arrays (hashable if their elements are hashable). Sets are mutable, unordered collections of unique elements backed by a hash table.
- **Dictionaries**: Store key-value pairs. Dictionaries resolve hash collisions using **open addressing** (specifically, pseudo-random probing) rather than chaining.

#### Dynamic Typing
Variables bind to values at runtime, not declaration. Contrast with Java's `int x = 5`:
```python
x = 5; x = "hello"; x = [1, 2, 3]  # Rebind; old reference GC'd
```
**Benefit**: Generic code without type declarations. **Drawback**: Typos surface at runtime. **Solution**: Type hints + mypy.

#### Mutable vs Immutable
- **Mutable**: `list`, `dict`, `set`, `bytearray` — id() unchanged when contents change.
- **Immutable**: `int`, `float`, `str`, `tuple`, `frozenset`, `bytes` — "modification" creates new object.

```python
lst = [1, 2]; lst.append(3)  # Same id()
s = "hello"; s = s + " world"  # New string created
```
**Why it matters**: Immutable objects hashable (safe dict keys). Mutable can't be hashed. Immutable avoids synchronization in multithreading.
- *Mutable Defaults Trap*: Defining a function with a mutable default argument like `def foo(val=[])` binds `val` to a single list object created at definition time. Subsequent calls append to this same shared list instance. Fix this by using `def foo(val=None): if val is None: val = []`.

#### LEGB Rule
Variable lookup: **Local → Enclosing → Global → Builtin**

#### Duck Typing
Objects judged by behavior (methods/attributes), not type. "If it walks like a duck and quacks like a duck, it's a duck."

### Intermediate Concepts

#### Generators & Iterators
- **Iterator**: `__iter__()` returns self; `__next__()` returns next item.
- **Generator**: Function with `yield`, returns generator iterator. State preserved.

```python
def count_up(n):
    i = 0
    while i < n:
        yield i
        i += 1

gen = count_up(3)
next(gen)  # 0; pauses here
next(gen)  # 1; resumes
```
**Memory O(1) regardless of n.**

#### Decorators
Functions wrapping callables. Use `functools.wraps` to preserve metadata.

```python
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.4f}s")
        return result
    return wrapper
```

#### Comprehensions
List/dict/set comprehensions. Faster than `.append()` loops.

```python
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
word_len = {w: len(w) for w in ["apple", "pie"]}
unique_lens = {len(w) for w in ["a", "bb", "ccc"]}
```

#### Context Managers
`with` protocol ensures cleanup via `__enter__` / `__exit__`. Prevents resource leaks.

```python
with open("data.txt") as f:
    content = f.read()  # Guaranteed f.close() even if exception
```

#### Properties
`@property` lets getters/setters behave like attributes.

```python
class Circle:
    def __init__(self, r):
        self._r = r
    
    @property
    def radius(self):
        return self._r
    
    @radius.setter
    def radius(self, value):
        if value <= 0: raise ValueError("Positive only")
        self._r = value
```

#### Parameter Passing in Functions
Python parameters are passed using **call-by-sharing** (pass-by-object-reference). When you call a function, the arguments are bound to the parameter names in the local scope:
- If you pass an immutable object (e.g. integer or string), rebinding it inside the function does not affect the caller.
- If you pass a mutable object (e.g. a list or dictionary), modifying it in-place affects the caller, but rebinding the variable to a new object does not.

#### Functional Programming Utilities
- **Lambdas**: Anonymous one-line functions: `lambda x, y: x + y`.
- **Map, Filter, & Reduce**:
  - `map(func, iterable)`: Applies a function to all items in an input list.
  - `filter(func, iterable)`: Filters items based on a boolean-returning function.
  - `reduce(func, iterable)`: Applies a rolling computation to sequential pairs of values (imported from `functools`).

#### OOP Mechanics: Inheritance & Methods
- **Inheritance Types**: Supports multiple and multilevel inheritance. Multiple inheritance is resolved via the MRO algorithm.
- **Class Methods vs. Static Methods**:
  - `@classmethod`: Accepts the class `cls` as the first argument. Can access/modify class state. Used for alternative constructor factory functions.
  - `@staticmethod`: Receives no class or instance argument. Behaves like a regular function placed inside the class namespace.
- **Abstract Classes**: Enforces child class implementations using the `abc` module:
  ```python
  from abc import ABC, abstractmethod
  class Worker(ABC):
      @abstractmethod
      def do_work(self): pass
  ```
- **Dunder Methods**: Double underscore methods customize built-in operator behaviors:
  - `__new__` vs `__init__`: `__new__` is the constructor (allocates memory and returns a new instance), while `__init__` is the initializer (populates attributes on the returned instance).
  - `__str__` vs `__repr__`: `__str__` defines user-friendly string representations; `__repr__` defines unambiguous representations for developers (eval-able where possible).
  - `__call__`: Allows instances to be invoked like regular functions.

### Advanced Concepts

#### Global Interpreter Lock (GIL)
CPython mutex allowing one thread to execute bytecode at a time. Protects refcnt corruption.

```python
# CPU-bound threads don't scale
import threading, time

def cpu_work():
    return sum(range(100_000_000))

start = time.perf_counter()
t1, t2 = threading.Thread(target=cpu_work), threading.Thread(target=cpu_work)
t1.start(); t2.start(); t1.join(); t2.join()
# Takes ~2x single thread (GIL serializes)
```

**Solution**: `multiprocessing` (separate processes, no GIL) or Cython/C extensions releasing GIL.

#### Garbage Collection
Python uses **reference counting** + **cyclic GC**.

```python
import gc

class Node:
    def __init__(self, name):
        self.name = name
        self.ref = None

a = Node("A"); b = Node("B")
a.ref = b; b.ref = a  # Cycle
del a, b  # Refcounts drop but cycle alive

gc.collect()  # Detects and frees cycles
```

#### Method Resolution Order (MRO)
C3 linearization for multiple inheritance.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.__mro__)  # (D, B, C, A, object)
# Diamond: A searched once, not twice
```

#### Metaclasses
Classes that create classes. `type` is default metaclass.

```python
class Meta(type):
    def __new__(cls, name, bases, namespace):
        if name != "Base" and "validate" not in namespace:
            raise TypeError(f"{name} must have validate()")
        return super().__new__(cls, name, bases, namespace)

class Base(metaclass=Meta):
    pass
```

#### Descriptor Protocol
Objects defining `__get__`, `__set__`, `__delete__` control attribute access.

```python
class Typed:
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type
    
    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name) if obj else self
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError()
        obj.__dict__[self.name] = value
```

#### `__slots__` Memory Optimization
Removes `__dict__`, stores attributes in fixed array. Saves ~60% per instance.

```python
import sys

class WithDict:
    def __init__(self, x, y):
        self.x = x; self.y = y

class WithSlots:
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x; self.y = y

d = WithDict(1, 2); s = WithSlots(1, 2)
# d uses 240+MB; s uses 56MB for 1M objects
```

#### Bytecode and Optimization
Python compiles to bytecode. Compiler performs peephole optimization.

```python
import dis

def constant_folding():
    return 2 + 3  # Compiler folds to 5

dis.dis(constant_folding)
# Output: LOAD_CONST(5); RETURN_VALUE
```

#### File Handling, Exceptions, & Logging
- **File Handling**: Opening files using the `with` context manager guarantees file closure, preventing file descriptor leaks. Supports reading (`r`), writing (`w`), appending (`a`), and binary modes (`b`).
- **Exceptions**: Exception hierarchy runs inside `try-except-else-finally` blocks. `else` executes only if no exception occurred; `finally` runs unconditionally, executing cleanup operations. Custom exceptions inherit from `Exception` (or `BaseException` for system-level overrides).
- **Logging**: Configured via the `logging` module to track application events. Supports log levels: `DEBUG` $\to$ `INFO` $\to$ `WARNING` $\to$ `ERROR` $\to$ `CRITICAL`. Loggers can direct output to handlers (StreamHandler, FileHandler) and format messages structurally.

#### Concurrency: Multithreading vs. Multiprocessing
- **Multithreading**: Lightweight, shared memory execution. Because of CPython's **Global Interpreter Lock (GIL)**, multiple threads cannot execute bytecode in parallel on multiple cores. Multithreading is highly effective for I/O-bound tasks (network calls, database operations, file reads), as the GIL is released during blocking system calls. Threads can use locks (`threading.Lock`) to prevent race conditions.
- **Multiprocessing**: Spawns multiple independent OS processes, each with its own memory space and Python interpreter instance. This bypasses the GIL entirely, enabling true parallel execution on multi-core systems. Spawning processes is computationally heavier and requires Inter-Process Communication (IPC) objects like `multiprocessing.Queue`, `Pipe`, or `SharedMemory` to exchange data.

---

## 3. Internal Working

### Compilation and Execution Pipeline
```
Source.py → Lexer/Tokenizer → Parser → AST → Compiler → Bytecode.pyc
                                                             ↓
                                                        PVM Loop
                                                             ↓
                                        C Functions/GIL/CPython Heap
```

### Object Header and Reference Counting
Every Python object has C-level header:
```c
typedef struct {
    Py_ssize_t ob_refcnt;     // Reference count
    PyTypeObject *ob_type;    // Pointer to type
    // ... object data
} PyObject;
```

**Reference counting example**:
```python
import sys
x = []           # refcnt = 1
y = x            # refcnt = 2
z = [x]          # refcnt = 3
del y            # refcnt = 2
# refcnt = 0 → deallocate immediately
```

### Memory Layout of a List
```
PyListObject:
  ob_refcnt | ob_type → PyList_Type
  allocated | ob_size
  +---------+
  | ob_item[] (array of PyObject* pointers)
  |
  +→ [PyObject*] → int 10
  |  [PyObject*] → str "hello"
  |  [PyObject*] → list [1, 2]
```

When appending: if ob_size < allocated, add pointer. Else reallocate with growth factor ~1.125.

### Package Import System
```
import numpy
  ↓
Is 'numpy' in sys.modules?
  ├─ YES → Return cached (no re-execution)
  └─ NO  → Find in sys.path
          → Load numpy/__init__.py
          → Compile to bytecode
          → Execute __init__.py
          → Create module object
          → Store in sys.modules
          → Bind local name
```

**Circular import problem**:
```python
# a.py: from b import x  → b.from a import y  (a in sys.modules but __init__ not finished)
# Result: NameError
```

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Bytecode** | `.pyc` intermediate instructions executed by PVM |
| **PVM** | Python Virtual Machine; stack-based interpreter |
| **GIL** | Global Interpreter Lock; mutex in CPython |
| **MRO** | Method Resolution Order via C3 linearization |
| **Duck Typing** | Judge by behavior, not type |
| **LEGB** | Local→Enclosing→Global→Builtin lookup |
| **`__slots__`** | Pre-allocated attributes; removes `__dict__` |
| **Descriptor** | `__get__`, `__set__`, `__delete__` protocol |
| **Monkey Patching** | Dynamic code modification at runtime |
| **Mixin** | Class providing methods via inheritance |
| **Coroutine** | Object from `async def`; executed by event loop |
| **Pickling** | Object serialization via `pickle` module |
| **Refcnt** | Reference count; 0 → deallocation |
| **Cyclic GC** | Detects/frees cycles reference counting misses |

---

## 5. Beginner Examples

### Example 1: Generators vs Lists Memory
```python
import sys

huge_list = [x for x in range(1_000_000)]
print(f"List: {sys.getsizeof(huge_list):,} bytes")  # ~8.8MB

huge_gen = (x for x in range(1_000_000))
print(f"Gen: {sys.getsizeof(huge_gen)} bytes")  # ~128 bytes

# Generator: process chunks without loading all
def read_file(path, chunk_size=8192):
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            yield chunk

for chunk in read_file("huge_file.bin"):
    process(chunk)
```

### Example 2: Context Manager Guarantees Cleanup
```python
# Bad: leak on exception
f = open("data.txt", "r")
try:
    content = f.read()
    x = content.split("\n")[999]
except IndexError:
    pass  # File handle leaked!

# Good: guaranteed cleanup
with open("data.txt", "r") as f:
    content = f.read()
    # __exit__ called even if exception
```

### Example 3: Duck Typing
```python
class Dog:
    def speak(self): return "Woof!"

class Cat:
    def speak(self): return "Meow!"

def announce(creature):
    return creature.speak()

announce(Dog())   # Woof!
announce(Cat())   # Meow!
# No inheritance; only .speak() matters
```

### Example 4: LEGB Scope
```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        nonlocal x
        x = "inner"
    inner()
    print(x)  # "inner"

outer()
print(x)      # "global"
```

### Example 5: Mutable Default Trap
```python
# Bad
def register(user, history=[]):
    history.append(user)
    return history

register("Alice")    # ["Alice"]
register("Bob")      # ["Alice", "Bob"] — leaked state!

# Good
def register(user, history=None):
    if history is None:
        history = []
    history.append(user)
    return history
```

---

## 6. Intermediate Examples

### Example 1: Retry Decorator
```python
import time, functools

def retry(max_attempts=3, delay=1.0, backoff=2.0):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def flaky_api_call():
    import random
    if random.random() < 0.7:
        raise ConnectionError()
    return "Success"
```

### Example 2: Custom Iterator
```python
class Fibonacci:
    def __init__(self, limit):
        self.limit = limit
        self.a, self.b, self.count = 0, 1, 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return val

for fib in Fibonacci(5):
    print(fib, end=" ")  # 0 1 1 2 3
```

### Example 3: LRU Cache
```python
from collections import OrderedDict

class LRU:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
```

### Example 4: Property with Validation
```python
class BankAccount:
    def __init__(self, owner, balance):
        self._owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, amount):
        if amount < 0:
            raise ValueError("Negative balance")
        self._balance = amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

account = BankAccount("Alice", 100)
account.withdraw(30)
print(account.balance)  # 70
```

### Example 5: String Interning
```python
# Small integers cached
a, b = 256, 256
print(a is b)  # True

a, b = 257, 257
print(a is b)  # False (not guaranteed)

# String interning
s1 = "hello"; s2 = "hello"
print(s1 is s2)  # True (literal interned)

s3 = "".join(["h", "e", "l", "l", "o"])
print(s1 is s3)  # False (dynamic)

# Lesson: use == for equality
```

---

## 7. Advanced Examples

### Example 1: Metaclass Registry
```python
class PluginMeta(type):
    plugins = {}

    def __new__(cls, name, bases, namespace):
        new_class = super().__new__(cls, name, bases, namespace)
        if name != "Plugin":
            cls.plugins[name] = new_class
        return new_class

class Plugin(metaclass=PluginMeta):
    pass

class PDFParser(Plugin):
    pass

print(PluginMeta.plugins)  # {'PDFParser': <class...>}
```

### Example 2: Type-Safe Descriptor
```python
class Validated:
    def __init__(self, name, expected_type, validator=None):
        self.name = name
        self.expected_type = expected_type
        self.validator = validator

    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name) if obj else self

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError()
        if self.validator and not self.validator(value):
            raise ValueError()
        obj.__dict__[self.name] = value

class User:
    name = Validated("name", str, lambda x: len(x) > 0)
    age = Validated("age", int, lambda x: 0 < x < 150)

u = User()
u.name = "Alice"; u.age = 30
# u.name = ""  # ValueError
```

### Example 3: Memory with `__slots__`
```python
import sys

class RegularPoint:
    def __init__(self, x, y):
        self.x = x; self.y = y

class SlottedPoint:
    __slots__ = ["x", "y"]
    def __init__(self, x, y):
        self.x = x; self.y = y

reg = RegularPoint(1, 2)
slot = SlottedPoint(1, 2)

# For 1M points: regular ~296MB, slotted ~56MB (5x savings)
```

### Example 4: Async Context Manager
```python
import asyncio

class AsyncResource:
    async def __aenter__(self):
        print("Acquiring...")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing...")
        await asyncio.sleep(0.1)

async def main():
    async with AsyncResource():
        print("Using resource...")
        await asyncio.sleep(0.1)

asyncio.run(main())
```

### Example 5: Bytecode Inspection
```python
import dis

def add(a, b):
    return a + b

dis.dis(add)
# LOAD_FAST 0 (a)
# LOAD_FAST 1 (b)
# BINARY_ADD
# RETURN_VALUE
```

---

## 8. How Interviewers Think

Interviewers test whether you understand **why** Python behaves the way it does. They want developers who write idiomatic Python, diagnose issues, and avoid subtle bugs.

### Red Flags
- Mutable default arguments without recognizing it.
- Using `is` for numeric/string equality.
- Not knowing the GIL.
- Writing `for i in range(len(seq))` instead of `enumerate`.
- Bare `except:` catching `KeyboardInterrupt`, `SystemExit`.

### Green Flags
- Suggesting generators for streaming 100GB logs into 2GB RAM.
- Using `functools.wraps` and explaining why.
- Choosing `multiprocessing` for CPU; `asyncio` for I/O.
- Understanding `==` vs `is` distinction.
- Profiling with `cProfile` before optimizing.

### Answer Matrix
| Level | Question: "How does Python handle memory?" |
|-------|------|
| **Rejected** | "Garbage collection takes care of it." |
| **Shortlisted** | "Reference counting and GC." |
| **Selected** | "Private heap, refcounting deallocates when 0. Cyclic GC (Gen0/1/2) frees cycles. Small ints/strings interned. GIL protects refcnt from thread corruption." |

---

## 9. Frequently Asked Interview Questions (60 Questions)

### Conceptual (1-20)

**1. Explain the GIL.**
The Global Interpreter Lock is a mutex in CPython allowing one thread to execute bytecode at a time. Protects refcnt corruption. CPU-bound threads don't parallelize (use `multiprocessing`). I/O-bound releases GIL, enabling concurrency (`asyncio`, `threading`).

**2. Mutable vs immutable objects.**
Mutable (`list`, `dict`, `set`): modify in-place without changing id(). Immutable (`int`, `str`, `tuple`): "modify" creates new object. Immutable objects are hashable; mutable can't be dict keys if contents change.

**3. Implement a decorator.**
```python
import functools

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

**4. `is` vs `==`.**
`==` checks equality via `__eq__`. `is` checks identity (id()). Use `==` for values; `is` for `None`, singletons.

**5. What is MRO?**
Method Resolution Order via C3 linearization. Diamond inheritance: `class D(B, C)` where B, C inherit from A searches D→B→C→A (A once, not twice).

**6. `*args` and `**kwargs`.**
`*args` collects extra positional into tuple. `**kwargs` collects extra keyword into dict. Used for flexible signatures, decorator forwarding.

**7. Context managers.**
`with EXPR as VAR:` calls `__enter__()`, runs block, calls `__exit__()` (guaranteed cleanup). Prevents resource leaks.

**8. What does `yield` do?**
Pauses function, returning generator iterator. Local state preserved. Enables lazy O(1) memory evaluation.

**9. Shallow vs deep copy.**
`copy.copy()` duplicates container; nested objects shared. `copy.deepcopy()` recursively duplicates all.

**10. Monkey patching.**
Dynamically modifying code at runtime. Powerful but breaks debugging; use cautiously.

**11. Exception handling.**
`try/except/finally/else`. Specific before generic. Avoid bare `except:`. `finally` always runs.

**12. Lambda functions.**
Anonymous single-expression. Avoid complex logic; use named `def` for readability.

**13. `with` statement internals.**
Calls `__enter__()`, runs block, calls `__exit__()` in finally block (guaranteed even on exception).

**14. Pass-by-assignment.**
Arguments passed by object reference. Mutable objects modified in-place; immutable rebindings local only.

**15. `if __name__ == "__main__"`.**
Allows module to detect direct execution vs import. Prevents side effects on import.

**16. Package vs module.**
Module: single `.py` file. Package: directory with `__init__.py` allowing hierarchical organization, relative imports.

**17. `super()` vs parent calls.**
`super()` follows MRO in multiple inheritance. Direct parent calls break diamond inheritance.

**18. Function annotations.**
PEP 3107: `def f(x: int) -> str:`. Tools like `mypy` check; Python ignores at runtime unless inspected.

**19. List slicing `[::-1]` and `[::2]`.**
`seq[start:stop:step]`. `[::-1]` reverses. `[::2]` every other. Creates shallow copies.

**20. `enumerate` vs index loops.**
`enumerate` yields (index, value) tuples. Faster, more Pythonic than `for i in range(len(seq))`.

### Scenario-Based (21-40)

**21. Process 20 GB CSV in 4 GB RAM.**
Use chunked reading: `pd.read_csv(path, chunksize=50_000)`. Process, write, discard each chunk.

**22. Share state across multiprocessing.**
Direct sharing impossible. Use `Queue`, `Pipe`, `Manager().dict/list`, `shared_memory`.

**23. Design LRU cache.**
`OrderedDict`. `get()`: if key exists, move_to_end(), return. `put()`: update or add, evict oldest if over capacity. O(1) operations.

**24. Debug: class variable shared.**
```python
class Counter:
    count = 0  # Shared

# Fix: instance variable in __init__
self.count = 0
```

**25. Thread-safe singleton.**
```python
class Singleton:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
```

**26. Build stack.**
```python
class Stack:
    def __init__(self): self._data = []
    def push(self, x): self._data.append(x)
    def pop(self): return self._data.pop()
    def peek(self): return self._data[-1]
```

**27. Profile slow function.**
`python -m cProfile script.py`. Inspect cumulative time. Typical wins: NumPy vectorization, caching.

**28. Design rate limiter.**
```python
class RateLimiter:
    def __init__(self, calls, period):
        self.calls = calls
        self.period = period
        self.timestamps = []
    
    def allow(self):
        now = time.time()
        self.timestamps = [t for t in self.timestamps if now - t < self.period]
        if len(self.timestamps) < self.calls:
            self.timestamps.append(now)
            return True
        return False
```

**29. Data pipeline with generators.**
```python
def read_lines(path):
    with open(path) as f:
        for line in f:
            yield line.strip()

pipeline = parse(filter_empty(read_lines("file.txt")))
# Memory constant regardless of file size
```

**30. Why `timeit` over `time.time()`?**
`timeit` disables GC, uses precise timer, repeats statistically. `time.time()` affected by OS scheduling, CPU scaling.

### Debugging (31-45)

**31. Mutable default trap.**
```python
def register(user, history=None):
    if history is None:
        history = []
    history.append(user)
    return history
```

**32. `is` vs `==` issues.**
Use `==` for values. `is` unreliable for ints/strings due to interning.

**33. Generator exhaustion.**
Generators consumed once. Recreate or materialize with `list()`.

**34. Exception swallowing.**
Log exceptions: `logging.exception(e)` or re-raise after cleanup.

**35. `__slots__` inheritance.**
If base lacks `__slots__`, subclass gets `__dict__` automatically.

**36. Circular imports.**
Modules in `sys.modules` before `__init__` finishes. Restructure: move imports inside functions or reorganize module layout.

**37. Forgetting `super().__init__()`.**
Parent `__init__` skipped; attributes not initialized.

**38. Wrong exception catching.**
Catch specific exceptions, not `Exception`. Use `except ValueError:` not bare `except:`.

**39. Modifying list while iterating.**
Changes indices. Iterate copy: `for x in lst[:]`.

**40. Deep recursion limit.**
Use iteration or increase `sys.setrecursionlimit()`.

### System Design (41-55)

**41. Multiple inheritance example.**
```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass
# MRO: D, B, C, A, object
```

**42. Deepcopy recursive behavior.**
Copies every object reachable from source. Prevents shared references.

**43. `__new__` vs `__init__`.**
`__new__` allocates instance. `__init__` initializes. Override `__new__` for immutables, singletons.

**44. List vs tuple.**
List: mutable, slower iteration. Tuple: immutable, hashable, slightly faster.

**45. `nonlocal` keyword.**
Rebinds variable in enclosing (non-global) scope. Required for nested functions to modify closure variables.

### Advanced (46-60)

**46. Generator expressions vs comprehensions.**
Generator: `(x**2 for x in range(5))` lazy, O(1) memory. Comprehension: `[x**2 for x in range(5)]` eager, O(n) memory.

**47. Magic methods.**
`__init__`, `__str__`, `__repr__`, `__len__`, `__getitem__`, `__call__`. Hook into Python operations.

**48. `__getitem__` enables slicing.**
`obj[start:stop:step]` creates `slice(start, stop, step)` passed as key to `__getitem__`.

**49. `sys.getrefcount` limitation.**
Returns refcnt but includes temporary reference from call (off by one). Can't see C-level refs.

**50. `asyncio` vs `threading`.**
`asyncio`: single-threaded event loop, cooperative multitasking, scales to 10K+ concurrent. `threading`: OS pre-emption, GIL-limited, fewer concurrent tasks.

**51. `functools.lru_cache`.**
Decorator caching results (default 128). Uses ordered dict. Great for pure/idempotent functions.

**52. Descriptor protocol.**
`__get__`, `__set__`, `__delete__` control attribute access. Powers `@property`, ORMs.

**53. Coroutine.**
Function defined with `async def`. Returns coroutine object executed by event loop.

**54. `__all__`.**
List of public names exported by `from module import *`. Without it, all non-underscore names exported.

**55. C extension.**
C/C++ module compiled to shared library. Releases GIL in compute loops. Runs at native speed.

**56. Pickle security.**
Unsafe to unpickle untrusted data; arbitrary code can execute during reconstruction.

**57. Global namespace.**
Top-level module scope. Each module has own namespace. `globals()` returns it.

**58. Closure.**
Nested function capturing enclosing scope variables. Captured vars persist between calls.

**59. Indentation for blocks.**
PEP 8: indentation groups statements into suites. Cleaner than braces.

**60. Unpacking assignment.**
`a, b = [1, 2]`. Extended: `a, *rest, z = [1, 2, 3, 4, 5]` → `a=1, rest=[2,3,4], z=5`.

---

#### 61. Explain how mutable default arguments behave in Python and how to avoid side effects.
- **Detailed Answer**: In Python, default parameter values are evaluated exactly once when the function is defined, not when it is called. If a mutable object (like a list or dictionary) is used as a default, that single object is instantiated at compile-time and shared across all subsequent invocations. Any in-place updates to that argument will persist across calls, causing unintended side effects.
  To avoid this, use a `None` sentinel as the default value and instantiate a new mutable object inside the function body if the argument is `None`:
  ```python
  def append_to(element, target=None):
      if target is None:
          target = []
      target.append(element)
      return target
  ```
- **Follow-up Questions**: Why does Python evaluate defaults at definition time? (Answer: To optimize performance by avoiding repetitive evaluations, and because default values themselves are attributes of the function object stored in `__defaults__`).
- **Interviewer's Expectations**: Point out that defaults are evaluated once at definition time, describe the persistent shared object, and demonstrate the `None` sentinel fix.

---

#### 62. Contrast Python's multithreading and multiprocessing in terms of GIL, memory sharing, and suitability.
- **Detailed Answer**:
  - **Multithreading**: Uses lightweight threads within a single process. Since CPython's Global Interpreter Lock (GIL) restricts execution to one thread at a time, threads cannot run CPU-bound bytecode in parallel. However, threads share the same memory space, making communication simple, and they release the GIL during blocking I/O calls, making multithreading ideal for network/database tasks.
  - **Multiprocessing**: Spawns independent OS processes, each with its own memory space and Python interpreter instance. This bypasses the GIL entirely, enabling true parallel execution on multi-core systems, making it ideal for CPU-bound tasks. The drawback is that processes do not share memory; exchanging data requires serialization (pickling) and IPC mechanisms (queues, pipes, or managers).
- **Follow-up Questions**: How does memory overhead compare? (Answer: Multiprocessing has a much higher memory overhead since each process has to load the entire Python runtime and its own heap, whereas multithreading shares a single process heap).
- **Interviewer's Expectations**: Contrast GIL impact, compare memory spaces (shared vs isolated), identify suitability (I/O-bound vs CPU-bound), and mention serialization overhead.

---

## 10. Common Mistakes

- **Mutable defaults**: Evaluate once. Fix with `None` sentinel.
- **Modifying while iterating**: Changes indices. Iterate copy.
- **Bare `except:`**: Swallows `KeyboardInterrupt`. Use explicit types.
- **`is` for equality**: Use `==`. `is` for identity.
- **Not closing resources**: Always use `with`.
- **Deep recursion**: Use iteration or increase limit.
- **Confusing concepts**: `==` (equality), `is` (identity), `hash()` (independent).
- **Bytes vs strings**: Python 3 distinguishes.
- **Ignoring exception types**: Use explicit classes.
- **Circular imports**: Restructure; import inside functions.

---

## 11. Comparison: Python vs Java vs C++

| Feature | Python | Java | C++ |
|---------|--------|------|-----|
| **Typing** | Dynamic | Static | Static |
| **Compilation** | Bytecode (PVM) | Bytecode (JVM) | Machine code |
| **GC** | Refcnt + cyclic | Generational | Manual/RAII |
| **Concurrency** | GIL limits threads | Native threads | Native threads |
| **Startup** | ~100ms | ~500ms | ~1ms |
| **Speed** | 1x | 5-10x | 50-100x |
| **Verbosity** | Minimal | Moderate | High |
| **Memory** | High per-object | JVM overhead | Lower |
| **Use Case** | Prototyping, AI | Enterprise | Systems, games |

---

## 12. Practical Projects

- **Beginner**: CLI todo list with JSON persistence, `argparse`, `pathlib`.
- **Intermediate**: Async web scraper with `aiohttp`, retries, rate limiting, CSV export.
- **Advanced**: Python interpreter subset (lexer, parser, AST, bytecode interpreter).

---

## 13. Internship Preparation

- **Resume**: Highlight automation saving time/errors.
- **Startups**: Edge cases, clean functions, Git proficiency.
- **AI startups**: NumPy/Pandas, reproducible notebooks, type hints.
- **Interview focus**: Decorators, generators, GIL, memory optimization.
- **Coding rounds**: Pythonic solutions (comprehensions, `collections`, `itertools`).

---

## 14. Cheat Sheet

| Concept | Key |
|---------|-----|
| **LEGB** | Local → Enclosing → Global → Builtin |
| **Mutability** | lists/dicts mutable; ints/strs immutable |
| **`==` vs `is`** | Equality vs identity |
| **Decorator** | `@functools.wraps` preserves metadata |
| **Generator** | `yield` lazy O(1) iteration |
| **GIL** | `multiprocessing` CPU; `asyncio` I/O |
| **Context** | `with` ensures cleanup |
| **`__slots__`** | Remove `__dict__`, save 60% memory |
| **Metaclass** | `type` controls class creation |
| **MRO** | C3 linearization for inheritance |

---

## 15. One-Day Revision Checklist

- [ ] Explain GIL and `multiprocessing` vs `threading`.
- [ ] Implement decorator with `@wraps`.
- [ ] Mutable vs immutable examples and implications.
- [ ] Describe MRO and C3 linearization.
- [ ] Debug mutable default (< 2 min).
- [ ] List comprehension to generator.
- [ ] 3 reasons for `with open(...)`.
- [ ] Object lifecycle: creation, refcnt, GC.
- [ ] Compare Python/Java in 60 seconds.
- [ ] Demonstrate `__slots__` memory savings.
- [ ] Solve one HackerRank problem (< 10 min).
- [ ] Explain duck typing with analogy.
