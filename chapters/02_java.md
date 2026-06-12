# 2. Java (Core Language & Ecosystem)

## 1. Introduction

### What it is
Java is a class-based, statically typed, multi-threaded, object-oriented programming language designed to have as few implementation dependencies as possible. Java source code (`.java`) compiles into intermediate **bytecode** (`.class`), which is interpreted and compiled at runtime by the **Java Virtual Machine (JVM)**. This enables its core design tenet: "Write Once, Run Anywhere" (WORA).

### Why it exists
Java was created by James Gosling at Sun Microsystems in 1995. Prior to Java, the dominant system languages were C and C++. Writing large applications in C/C++ required manual memory management, creating risks of memory leaks and pointer corruption. Furthermore, C/C++ code had to be recompiled for each target operating system and hardware architecture. Java was designed to automate memory management (Garbage Collection), remove explicit pointer arithmetic, and introduce a virtual execution layer (the JVM) to isolate software from host hardware variations.

### Problems it solves
- **Manual Memory Allocation errors**: Replaces manual memory allocation and deallocation (`malloc`/`free` or `new`/`delete`) with automated garbage collection.
- **Platform Lock-In**: Decouples executable code from the host OS and CPU architecture. The JVM translates bytecode into host-specific machine code at runtime.
- **Type Insecurity**: Enforces compile-time type checking and runtime validation, preventing arbitrary memory access.
- **Concurrency Complexity**: Provides built-in keywords (`synchronized`, `volatile`) and structured libraries (`java.util.concurrent`) to make multi-threaded application design manageable.

### Industry Use Cases
- **Enterprise Web Backends**: Running core systems for banking, retail, and insurance platforms (frequently utilizing frameworks like Spring Boot or Jakarta EE).
- **Android Mobile App Ecosystem**: Google's Android runtime uses Java API libraries and bytecode-like Dalvik/ART execution layers.
- **Big Data Infrastructures**: Powers core systems of Apache Hadoop, Apache Spark, Apache Fargate, and Apache Kafka.
- **High-Frequency Trading Platforms**: Low-latency, tuned JVM systems executing financial transactions in microseconds.

### Analogy
Java is like a container shipping logistics network. The source code is the cargo. Instead of designing a custom boat for each type of cargo and each destination port (compiling C++ for every OS/CPU combination), you pack the cargo into standardized containers (bytecode `.class` files). Every port in the world is equipped with a standardized container terminal (the JVM). As long as the port has a container terminal, the cargo lands and unloads identically, regardless of the underlying terrain (Windows, Linux, or macOS).

---

## 2. Core Concepts

### Beginner Concepts
- **JDK vs. JRE vs. JVM**:
  - **JVM (Java Virtual Machine)**: The execution engine that runs bytecode.
  - **JRE (Java Runtime Environment)**: The package that runs applications. It contains the JVM along with Java core class libraries and binaries.
  - **JDK (Java Development Kit)**: The full SDK for developers. It includes the JRE, JVM, and compilation tools (e.g. `javac`, debugger).
- **Static vs. Instance Scope**:
  - `static` members (fields/methods) belong directly to the **Class**. They are loaded into memory once and shared among all object instances.
  - Instance members belong to the individual **Object**. They are allocated memory dynamically on the heap when an object is instantiated using `new`.
- **Primitives vs. Wrapper Types**:
  - Primitives (`int`, `char`, `double`, `boolean`) store raw values directly on the stack. They are fast and memory-efficient.
  - Wrapper classes (`Integer`, `Character`, `Double`, `Boolean`) are objects that wrap primitives, allowing them to be stored in Collections and used in generic methods.
  - **Autoboxing/Unboxing**: The compiler automatically converts primitives to wrappers (autoboxing) and vice-versa (unboxing).

### Intermediate Concepts
- **Four Pillars of OOP**:
  - **Encapsulation**: Hiding internal object state by making fields `private` and exposing access via public getters and setters.
  - **Inheritance**: Allowing one class (subclass) to acquire the properties and methods of another (superclass) using the `extends` keyword.
  - **Polymorphism**: The ability of an object to take on many forms. Demonstrated via **Method Overloading** (same method name, different signatures; resolved at compile-time) and **Method Overriding** (subclass redefines parent method; resolved at runtime).
  - **Abstraction**: Hiding implementation details and exposing only essential interfaces. Achieved using `abstract` classes and interfaces.
- **Interface vs. Abstract Class**:
  - **Interface**: A contract. Can have `default` and `static` methods (since Java 8) and private methods (since Java 9). A class can implement multiple interfaces.
  - **Abstract Class**: A partial blueprint. Can have instance variables, non-public methods, and constructors. A class can extend only one abstract class.
- **Generics & Type Erasure**: Generics enforce type safety at compile-time (e.g., `List<String>`). However, to maintain backward compatibility with older Java versions, the compiler replaces all generic types with `Object` (or their bounds) in the compiled bytecode. This is **Type Erasure**.
- **Java Collections Framework**:
  - `List`: Ordered collection allowing duplicates (`ArrayList` backed by array, `LinkedList` backed by nodes).
  - `Set`: Unordered collection preventing duplicates (`HashSet` backed by HashMap, `TreeSet` sorted using red-black trees).
  - `Map`: Key-value pair mapping (`HashMap` using hashing and bucket chaining, `TreeMap` sorted keys).
- **Exceptions Hierarchy**:
  - `Throwable` is the root class.
  - `Error`: Represents serious system-level failures (e.g., `OutOfMemoryError`) that applications should not attempt to catch.
  - `Exception`: Represents application errors.
    - **Checked Exceptions**: Subclasses of `Exception` (excluding `RuntimeException`). Must be declared in the method signature (`throws`) or handled in a `try-catch` block (e.g. `IOException`).
    - **Unchecked Exceptions**: Subclasses of `RuntimeException`. Checked at runtime (e.g. `NullPointerException`, `IndexOutOfBoundsException`).

### Advanced Concepts
- **JVM Runtime Memory Areas**:
  - **Heap**: Shared memory area storing all instantiated objects, arrays, and the string constant pool. Managed by the Garbage Collector.
  - **Stack**: Thread-private memory. Stores stack frames containing local variables, parameters, and partial results for each active method call.
  - **Metaspace**: Stores class metadata, runtime constant pools, and method bytecodes. Allocated from native host memory.
- **Garbage Collection Algorithms**:
  - **Generational GC**: Divides the heap into Young Generation (Eden, S0, S1) and Old Generation, leveraging the hypothesis that most objects die young.
  - **G1 (Garbage First) GC**: Divides the heap into equal-sized regions, prioritizing regions with the most garbage to meet target pause times.
  - **ZGC (Z Garbage Collector)**: A scalable, low-latency collector designed to handle multi-terabyte heaps with pauses under 1 millisecond.
- **Concurrency & Memory Visibility**:
  - `synchronized`: Enforces mutual exclusion (only one thread can execute a block of code at a time).
  - `volatile`: Guarantees memory visibility. Reads/writes of a volatile variable go directly to main memory, bypassing CPU L1/L2 caches.
  - `java.util.concurrent`: High-level concurrency utilities (e.g. `ExecutorService`, `ConcurrentHashMap`, `Locks`).
- **Java Streams & Lambdas (Java 8+)**: Enables declarative, functional-style transformations over collections (e.g. `map`, `filter`, `reduce`), supporting automatic parallelization.

---

## 3. Internal Working

### JVM Architecture and Memory Layout
The JVM runtime data areas manage memory allocation dynamically during execution:

```text
+--------------------------------------------------------------------------------+
| JVM Runtime Data Areas                                                         |
|                                                                                |
|  [ Thread-Private Memory ]                       [ Shared Memory ]             |
|  +-----------------------+                      +----------------------------+ |
|  | Thread 1 Stack        |                      | Heap                       | |
|  | [Frame 2: methodB]    |                      | +------------------------+ | |
|  | [Frame 1: methodA]    |                      | | Young Gen (Eden, S0,S1)| | |
|  |                       |                      | +------------------------+ | |
|  +-----------------------+                      | | Old Gen / Tenured      | | |
|  | PC Register           |                      | +------------------------+ | |
|  +-----------------------+                      | | String Constant Pool   | | |
|  | Native Method Stack   |                      | +------------------------+ | |
|  +-----------------------+                      +----------------------------+ |
|                                                 | Metaspace (Native RAM)     | |
|                                                 | (Class structures, methods)| |
|                                                 +----------------------------+ |
+--------------------------------------------------------------------------------+
```

1. **Method Stack Frames**:
   Each thread has a private stack. When a method is called, a **Stack Frame** is pushed. The frame contains:
   - **Local Variable Table (LVT)**: Stores primitive values and references to objects on the heap.
   - **Operand Stack**: Workspace for performing bytecode operations.
   - **Frame Data**: References to the runtime constant pool and exception handlers.
2. **Just-In-Time (JIT) Compilation**:
   The JVM starts by interpreting bytecode. When it detects "hot spots" (methods executed frequently), the JIT compiler compiles the bytecode directly into native machine code. It uses two compilers:
   - **C1 (Client Compiler)**: Focuses on fast compilation with basic optimization.
   - **C2 (Server Compiler)**: Performs deep optimizations (inlining, escape analysis, loop unrolling), resulting in highly optimized machine code.

### Generational Garbage Collection Mechanics
The generational hypothesis states that most objects survive for only a short period. The heap is divided into:
1. **Young Generation**:
   - **Eden Space**: Newly allocated objects are created here.
   - **Survivor Spaces (S0 and S1)**: When Eden fills up, a **Minor GC** occurs. Live objects are copied to one of the survivor spaces, and their age counter increments. On subsequent collections, live objects are copied between S0 and S1, incrementing their age.
2. **Old Generation (Tenured)**:
   - If an object survives enough minor GC cycles (defined by `-XX:MaxTenuringThreshold`, default 15), it is promoted to the Old Generation.
   - **Major GC / Full GC**: Cleans the Old Generation, which takes longer and can cause longer "Stop-the-World" (STW) pauses.

```text
Eden Allocation ---> Minor GC ---> Copy to S0/S1 (Age +1) ---> Age >= 15 ---> Promote to Old Gen
```

### String Constant Pool and Immutability
In Java, `String` objects are immutable.
- **Why**: Security (usernames, file paths, and database connection strings cannot be changed after validation), thread safety (no synchronization required), and caching.
- **String Pool**: A dedicated hashtable located in the heap. When you declare a literal: `String s1 = "hello"`, the JVM checks the pool. If "hello" exists, s1 points to the existing object. If you declare `String s2 = new String("hello")`, the JVM is forced to bypass the pool and create a new object on the heap, wasting memory.
- **Interning**: Calling `s2.intern()` returns the canonical representation from the string pool, adding it if not present.

---

## 4. Important Terminology

- **JVM (Java Virtual Machine)**: Platform-dependent runtime executing compiled bytecode.
- **Bytecode**: Platform-independent intermediate instruction set generated from Java source.
- **JIT Compiler**: Compilation engine translating bytecode to machine code at runtime.
- **Garbage Collection (GC)**: Automatic reclamation of memory allocated to unreachable objects.
- **Metaspace**: Native memory region storing class definitions and metadata.
- **Stack Frame**: Memory block pushed onto a thread stack representing a method call.
- **Eden Space**: The entry-level heap allocation region for new objects.
- **Survivor Space (S0/S1)**: Temporary areas holding objects that survived minor GCs.
- **Old Gen (Tenured)**: Heap region holding long-lived objects promoted from survivor spaces.
- **String Constant Pool**: Memory cache in the heap storing unique string literals.
- **Classloader**: JVM component responsible for loading, linking, and initializing classes dynamically.
- **Type Erasure**: Compilation step removing generic type information before bytecode generation.
- **Checked Exception**: Exception class validated at compile-time, requiring try-catch or declaration.
- **Unchecked Exception**: Exception validated at runtime (e.g. RuntimeException).
- **Volatile**: Variable modifier ensuring reads/writes bypass CPU cache to main memory.
- **Synchronized**: Access control lock enforcing single-thread execution on blocks or methods.
- **Happens-Before Relationship**: Memory model rule ensuring changes made by one thread are visible to another.
- **CompletableFuture**: Concurrency class representing asynchronous execution pipelines.
- **JPMS (Java Platform Module System)**: Modular system enforcing strong encapsulation (since Java 9).
- **PECS (Producer Extends, Consumer Super)**: Generics rule for using wildcards to make APIs flexible.
- **Autoboxing**: Automatic conversion from primitives to matching wrapper objects.
- **Autocloseable**: Interface allowing resources to close automatically in try-with-resources.

---

## 5. Beginner Examples

### Example 1: Static vs. Instance Variables and Context
Understanding how static fields are shared class-wide, whereas instance variables are bound to individual objects on the heap.

```java
public class BankAccount {
    // Instance variable: allocated on the heap per object
    private double balance;
    private final String accountNumber;

    // Static variable: allocated once, shared across all instances
    private static double interestRate = 0.02;

    public BankAccount(String accountNumber, double initialDeposit) {
        this.accountNumber = accountNumber;
        this.balance = initialDeposit;
    }

    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;
        }
    }

    // Static method: can only access static fields directly
    public static void setInterestRate(double newRate) {
        interestRate = newRate;
    }

    public static double getInterestRate() {
        return interestRate;
    }

    public double getBalance() {
        return balance;
    }
}
```

### Example 2: List, Set, and Map Manipulation
Working with the Java Collections framework.

```java
import java.util.*;

public class CollectionBasics {
    public static void main(String[] args) {
        // 1. List: Ordered, permits duplicates
        List<String> list = new ArrayList<>();
        list.add("Apple");
        list.add("Banana");
        list.add("Apple"); // Duplicate
        
        // 2. Set: Unordered, rejects duplicates
        Set<String> set = new HashSet<>(list);
        
        // 3. Map: Key-Value storage
        Map<String, Integer> fruitInventory = new HashMap<>();
        fruitInventory.put("Apple", 50);
        fruitInventory.put("Banana", 30);
        
        System.out.println("List count: " + list.size()); // 3
        System.out.println("Set count (no duplicates): " + set.size()); // 2
        System.out.println("Apple inventory: " + fruitInventory.get("Apple")); // 50
    }
}
```

### Example 3: Try-With-Resources (AutoCloseable)
Opening files and resources safely to prevent resource leaks.

```java
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;

public class FileReadExample {
    public static void printFirstLine(String filePath) {
        // BufferedReader implements AutoCloseable
        // JVM calls close() automatically on exit, even if exceptions occur
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line = reader.readLine();
            System.out.println("First Line: " + line);
        } catch (IOException e) {
            System.err.println("Error reading file: " + e.getMessage());
        }
    }
}
```

---

## 6. Intermediate Examples

### Example 1: Generics Wildcards (PECS Rule)
Making API parameters flexible using wildcards. The PECS rule stands for: **Producer Extends, Consumer Super**.

```java
import java.util.List;

public class GenericsHelper {

    // Producer Extends: The list produces data (we read from it).
    // Accepts List of Double, Integer, etc.
    public static double calculateSum(List<? extends Number> list) {
        double sum = 0.0;
        for (Number number : list) {
            sum += number.doubleValue();
        }
        return sum;
    }

    // Consumer Super: The list consumes data (we write to it).
    // Accepts List of Integer, Number, Object.
    public static void addNumbers(List<? super Integer> list) {
        for (int i = 1; i <= 5; i++) {
            list.add(i);
        }
    }
}
```

### Example 2: Stream API Pipeline
Declarative text filtering, sorting, mapping, and reduction.

```java
import java.util.List;
import java.util.stream.Collectors;

public class StreamProcessor {
    public static List<String> processWords(List<String> rawWords) {
        return rawWords.stream()
            // 1. Filter out words containing null or empty strings
            .filter(word -> word != null && !word.trim().isEmpty())
            // 2. Filter out words with length under 4 characters
            .filter(word -> word.length() >= 4)
            // 3. Map to uppercase
            .map(String::toUpperCase)
            // 4. Sort alphabetically
            .sorted()
            // 5. Collect stream to a List
            .collect(Collectors.toList());
    }
}
```

### Example 3: Comparable vs. Comparator
Sorting custom classes using both natural ordering (Comparable) and custom comparators.

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

// Comparable implements natural sort order (by age)
public class Candidate implements Comparable<Candidate> {
    private final String name;
    private final int age;
    private final double score;

    public Candidate(String name, int age, double score) {
        this.name = name;
        this.age = age;
        this.score = score;
    }

    public int getAge() { return age; }
    public double getScore() { return score; }

    @Override
    public int compareTo(Candidate other) {
        return Integer.compare(this.age, other.age);
    }

    @Override
    public String toString() {
        return name + " (" + age + ", " + score + ")";
    }
}

class SortingDemo {
    public static void main(String[] args) {
        List<Candidate> candidates = new ArrayList<>();
        candidates.add(new Candidate("Alice", 22, 95.5));
        candidates.add(new Candidate("Bob", 20, 98.0));
        
        // 1. Natural Sort (by age using Comparable)
        Collections.sort(candidates);
        System.out.println("Sorted by Age: " + candidates);
        
        // 2. Custom Sort (by score using Comparator lambda)
        candidates.sort(Comparator.comparingDouble(Candidate::getScore).reversed());
        System.out.println("Sorted by Score: " + candidates);
    }
}
```

---

## 7. Advanced Concepts & Examples

### Example 1: Volatile Visibility and Atomic Operations
Demonstrating how volatile enforces thread visibility, while atomic variables handle thread-safe modifications.

```java
import java.util.concurrent.atomic.AtomicInteger;

public class ConcurrencyDemo {
    // volatile guarantees that changes to stopFlag are visible to all threads immediately
    private static volatile boolean stopFlag = false;
    
    // AtomicInteger handles concurrent increments without requiring synchronized blocks
    private static final AtomicInteger atomicCounter = new AtomicInteger(0);

    public static void main(String[] args) throws InterruptedException {
        Thread worker = new Thread(() -> {
            while (!stopFlag) {
                // Perform calculations
                atomicCounter.incrementAndGet();
            }
            System.out.println("Worker thread stopped. Final Count: " + atomicCounter.get());
        });

        worker.start();

        // Let the worker run for 1 second
        Thread.sleep(1000);
        
        // Trigger stop flag
        stopFlag = true;
        
        // Wait for worker thread to terminate
        worker.join();
    }
}
```

### Example 2: HashMap Hash Collisions and Bucket Chaining
Designing a key class with correct hash calculations to ensure HashMap lookup reliability.

```java
import java.util.Objects;

public class EmployeeKey {
    private final int employeeId;
    private final String department;

    public EmployeeKey(int employeeId, String department) {
        this.employeeId = employeeId;
        this.department = department;
    }

    // Hash calculation contract
    @Override
    public int hashCode() {
        // Computes a hash based on fields to distribute keys across buckets
        return Objects.hash(employeeId, department);
    }

    // Equals lookup contract
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        EmployeeKey other = (EmployeeKey) obj;
        return this.employeeId == other.employeeId && 
               Objects.equals(this.department, other.department);
    }
}
```
*Why this contract matters*:
If two keys return the same hash code (a hash collision), they map to the same bucket index. The HashMap stores the keys in a linked list (or red-black tree if collisions exceed 8). When retrieving, the map scans the bucket and uses the `equals()` method to locate the correct key. If `hashCode()` is overridden but `equals()` is omitted (or vice-versa), key retrieval fails, returning `null`.

### Example 3: CompletableFuture Asynchronous Pipeline
Executing non-blocking tasks asynchronously and handling exceptions.

```java
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class AsyncPipelineDemo {
    public static void main(String[] args) throws Exception {
        ExecutorService customExecutor = Executors.newFixedThreadPool(4);

        CompletableFuture<String> pipeline = CompletableFuture.supplyAsync(() -> {
            // Step 1: Fetch data (runs asynchronously in thread pool)
            System.out.println("Fetching data in thread: " + Thread.currentThread().getName());
            return "user_data_payload";
        }, customExecutor)
        // Step 2: Transform data
        .thenApply(rawData -> {
            System.out.println("Transforming data in thread: " + Thread.currentThread().getName());
            return rawData.toUpperCase();
        })
        // Step 3: Handle errors
        .exceptionally(ex -> {
            System.err.println("Pipeline failed: " + ex.getMessage());
            return "FALLBACK_DATA";
        });

        // Block and print result (simulated main thread wait)
        String finalResult = pipeline.get();
        System.out.println("Final Pipeline Result: " + finalResult);
        
        customExecutor.shutdown();
    }
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate Java candidates by testing their understanding of JVM internals, memory management, and class design contracts. They look for awareness of JVM runtime memory areas, Generational Garbage Collection thresholds, type erasure limitations, and proper implementation of the `equals()` and `hashCode()` contracts.

### Red Flags
- **`==` for String comparisons**: Comparing String contents using `==` (which checks reference addresses) instead of `equals()` (which checks content values).
- **Broken Hash contracts**: Overriding `equals()` but omitting `hashCode()` (or vice-versa), breaking HashMap collections.
- **NPE prone chains**: Writing long, unvalidated method chains (e.g. `user.getAddress().getCity().toLowerCase()`) without null checks or `Optional` structures.
- **Generic Exception Catching**: Catching `Throwable` or `Exception` globally without handling specific cases or logging stack traces.

### Green Flags
- **Memory structure awareness**: Explaining the difference between Stack allocations (references, primitives) and Heap allocations (objects).
- **Stream optimization**: Using Stream pipelines efficiently while avoiding side-effects.
- **Checked vs Unchecked clarity**: Understanding when to use Checked exceptions (recoverable actions) vs Unchecked exceptions (programmer bugs).
- **Thread Safety competence**: Correctly using volatile flags and lock-free atomic variables instead of relying on slow synchronized blocks.

### Answers Matrix
| Level | Question: "What is the difference between ArrayList and LinkedList?" |
|---|---|
| **Rejected** | "ArrayList is faster and LinkedList is slower." |
| **Shortlisted** | "ArrayList is backed by an array, providing $O(1)$ random access but $O(N)$ insertion/deletion times. LinkedList is backed by a doubly linked list, providing $O(1)$ insertions but $O(N)$ lookup times." |
| **Selected** | "ArrayList is backed by a dynamically resizing array. It provides $O(1)$ time complexity for random access (`get(index)`), but insertions or deletions in the middle require shifting elements ($O(N)$). LinkedList is a doubly-linked list of node objects. It provides $O(1)$ time complexity for insertions and deletions at the ends, but lookup requires traversing the nodes from the head/tail ($O(N)$). In modern architectures, **ArrayList is almost always preferred** because its contiguous memory layout leverages CPU cache lines, whereas LinkedList's scattered node pointers cause frequent CPU cache misses, making it slower in practice." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the JVM memory areas: Heap, Stack, and Metaspace.
- **Detailed Answer**:
- **Heap**: A shared memory area created at JVM startup. It stores all object instances and arrays. It is managed by the Garbage Collector and divided into Young and Old generations.
- **Stack**: Thread-private memory. Each thread has its own stack. When a method is called, a **Stack Frame** is pushed. The frame stores local variables (primitives and object references), method parameters, and partial results. Frames are popped when the method returns.
- **Metaspace**: Stores class metadata, method definitions, runtime constant pools, and static variables. It is allocated from native system memory (outside the JVM heap), sizing dynamically.
- **Follow-up Questions**: What causes a `StackOverflowError` vs an `OutOfMemoryError`? (Answer: `StackOverflowError` occurs when the method stack grows too deep, e.g., infinite recursion. `OutOfMemoryError` occurs when the heap runs out of memory for new object allocations).
- **Interviewer's Expectations**: Distinguish thread-private (Stack) from shared memory (Heap, Metaspace), and explain local variables storage vs. heap references.

#### 2. What are Checked and Unchecked Exceptions in Java?
- **Detailed Answer**:
- **Checked Exceptions**:
  - Subclasses of `Exception` (excluding `RuntimeException`).
  - Checked by the compiler at compile-time.
  - The compiler forces the developer to handle them in a `try-catch` block or declare them in the method signature using the `throws` keyword.
  - Used for recoverable errors (e.g. `FileNotFoundException`, `SQLException`).
- **Unchecked Exceptions**:
  - Subclasses of `RuntimeException`.
  - Not checked at compile-time.
  - Usually indicate programming errors (bugs) that cannot be recovered from (e.g. `NullPointerException`, `ArithmeticException`).
- **Follow-up Questions**: Why is catching `Throwable` considered an anti-pattern? (Answer: Because `Throwable` includes `Error` subclasses (like `OutOfMemoryError`), which are fatal JVM failures that applications should not try to handle).
- **Interviewer's Expectations**: Differentiate compiler enforcement, identify their positions in the class hierarchy, and provide use cases for both.

#### 3. What is the contract between `equals()` and `hashCode()`?
- **Detailed Answer**: The contract states:
1. **Consistency**: If two objects are equal according to the `equals(Object)` method, calling `hashCode()` on both objects must produce the same integer result.
2. **Unequal hash codes**: If two objects are unequal according to `equals()`, their `hashCode()` values do not have to be different (hash collision), but generating unique hashes improves the performance of collections (like HashMap).
- *If you override `equals()`, you must override `hashCode()`* to ensure objects behave correctly in hashed collections.
- **Follow-up Questions**: What happens in a HashMap if you override equals but not hashCode? (Answer: The map may place duplicate keys in different buckets because they generate different hash codes, making the duplicates impossible to retrieve).
- **Interviewer's Expectations**: State the contract rules and explain the performance impact of hash collisions in HashMap lookups.

#### 4. What is Type Erasure in Java Generics?
- **Detailed Answer**: Java introduced Generics in Java 5 to enforce type safety at compile-time. To maintain backward compatibility with older JVM versions that only support raw types, the compiler applies **Type Erasure**:
1. Replaces generic type parameters (like `T` in `List<T>`) with their bound (`Object` or the specified class boundary, e.g. `Number`).
2. Inserts explicit type casts in the generated bytecode where generic values are returned.
3. Generates bridge methods to preserve polymorphism in inherited classes.
- *At runtime, the JVM has no knowledge of generic type parameters.*
- **Follow-up Questions**: How does type erasure impact runtime reflection? (Answer: You cannot determine the generic type of a class instance at runtime, e.g., checking `obj instanceof List<String>` is illegal due to erasure).
- **Interviewer's Expectations**: Explain the compilation step, backward compatibility constraints, and the removal of generic parameters from compiled bytecode.

#### 5. Explain the difference between `String`, `StringBuilder`, and `StringBuffer`.
- **Detailed Answer**:
- **`String`**: Immutable. Any modification (concatenation, replacement) creates a new String object on the heap, which can cause memory churn in loops.
- **`StringBuilder`**: Mutable. Modifies the internal character array directly without creating new objects. It is **not thread-safe** (methods are not synchronized), making it fast. Best for single-threaded string manipulations.
- **`StringBuffer`**: Mutable and **thread-safe**. All public methods are `synchronized`, ensuring thread safety at the cost of synchronization overhead.
- **Follow-up Questions**: How does the compiler optimize string concatenations like `s1 + s2`? (Answer: In modern Java versions, it compiles the concatenation to use `StringBuilder` or invokedynamic calls under the hood).
- **Interviewer's Expectations**: Compare mutability, thread safety, and performance overheads.

#### 6. What is the difference between `final`, `finally`, and `finalize`?
- **Detailed Answer**:
- **`final`**: A keyword modifier.
  - For a variable: Makes it constant (cannot be reassigned).
  - For a class: Prevents inheritance (cannot be extended, e.g. String).
  - For a method: Prevents overriding in subclasses.
- **`finally`**: A block associated with `try-catch` statements. It is guaranteed to execute after the try and catch blocks finish, regardless of whether an exception was thrown or caught. Used to release system resources.
- **`finalize`**: A method in the `Object` class called by the Garbage Collector before reclaiming an object's memory. It is deprecated and unreliable; applications should use `AutoCloseable` instead.
- **Follow-up Questions**: Does the `finally` block execute if the JVM exits via `System.exit(0)`? (Answer: No, because `System.exit()` halts the JVM process immediately).
- **Interviewer's Expectations**: Differentiate keywords, syntax structures, and object lifecycle methods.

#### 7. How does the JVM handle Method Overriding dynamically (Polymorphism)?
- **Detailed Answer**: Method overriding is resolved at runtime using **Dynamic Method Dispatch**.
When a method is called on an object reference (e.g. `parentRef.execute()`), the JVM looks at the actual object type on the heap, not the reference type.
The JVM uses a **Virtual Method Table (vtable)** associated with each class in the method area. The vtable contains pointers to the executable code for each method. If a subclass overrides a method, its vtable entry points to the subclass version of the code. The JVM performs a vtable lookup at runtime to locate the correct method.
- **Follow-up Questions**: Is method overloading resolved dynamically? (Answer: No, method overloading is resolved statically at compile-time based on the method signature and argument types).
- **Interviewer's Expectations**: Explain runtime resolution, reference vs. heap types, and the role of the virtual method table (vtable).

#### 8. What is the difference between Abstract Classes and Interfaces in Java 8+?
- **Detailed Answer**:
- **Abstract Class**:
  - Can have instance variables (state), constructors, and non-public methods.
  - A class can extend only one abstract class (single inheritance).
- **Interface**:
  - Cannot store instance variables (fields are implicitly `public static final`).
  - A class can implement multiple interfaces.
  - Can contain `default` and `static` methods (with implementations) and private helper methods.
- **Follow-up Questions**: When should you choose an abstract class over an interface? (Answer: Choose abstract classes when you need to share state or define non-public methods. Choose interfaces to define contracts that can be implemented by unrelated classes).
- **Interviewer's Expectations**: Compare variable storage, inheritance limits, and interface enhancements (default methods).

#### 9. What is a Memory Leak in Java, and how can it occur despite Garbage Collection?
- **Detailed Answer**: A Memory Leak in Java occurs when objects that are no longer needed by the application are kept alive because they are still referenced by active (reachable) objects. Since they are reachable, the Garbage Collector cannot reclaim their memory.
**Causes**:
1. **Static Collections**: Storing objects in static collections (like a static List or Map) that are never cleared.
2. **Unclosed Resources**: Leaving database connections or file streams open.
3. **Improper equals/hashCode in cache keys**: Storing keys in HashMaps that do not implement equals/hashCode, preventing them from being retrieved or removed.
4. **ThreadLocal variables**: Leaving values in `ThreadLocal` variables after the thread is returned to a thread pool.
- **Follow-up Questions**: How do you detect memory leaks? (Answer: Use profiling tools like Eclipse Memory Analyzer (MAT) or JProfiler to take heap dumps and identify growing object counts).
- **Interviewer's Expectations**: Define reference reachability and explain how unreleased references block garbage collection.

#### 10. Explain how the Java memory model ensures Thread Safety.
- **Detailed Answer**: The Java Memory Model (JMM) defines the behavior of threads and memory synchronization. It addresses:
1. **Visibility**: Ensuring changes made to a variable by one thread are visible to others. Enforced by `volatile` (forcing reads/writes to main memory) or `synchronized` blocks.
2. **Ordering**: Preventing the compiler or CPU from reordering instructions for optimization. Enforced by happens-before relationships.
3. **Atomicity**: Ensuring operations execute as a single unit. Enforced by `synchronized` locks or atomic classes (`AtomicInteger`).
- **Follow-up Questions**: What does the "Happens-Before" rule state? (Answer: A set of rules guaranteeing that memory writes made by statement A are visible to statement B (e.g. unlocking a monitor happens-before acquiring the lock)).
- **Interviewer's Expectations**: Explain memory visibility (volatile), mutual exclusion (synchronized), instruction reordering, and happens-before guarantees.

---

### Scenario-Based Questions

#### 11. Write a Java Stream pipeline that processes a list of employees, filters for department "IT", extracts their salaries, and calculates the average salary.
- **Detailed Answer**:
```java
import java.util.List;
import java.util.OptionalDouble;

public class CompanyAnalytics {
    public static double calculateITAverageSalary(List<Employee> employees) {
        if (employees == null || employees.isEmpty()) {
            return 0.0;
        }
        
        OptionalDouble average = employees.stream()
            // 1. Filter out null employee records
            .filter(emp -> emp != null)
            // 2. Filter for IT department (case-insensitive)
            .filter(emp -> "IT".equalsIgnoreCase(emp.getDepartment()))
            // 3. Map to double salary stream
            .mapToDouble(Employee::getSalary)
            // 4. Calculate average
            .average();
            
        // Return average if present, otherwise default to 0.0
        return average.orElse(0.0);
    }
}
```
- **Follow-up Questions**: Why use `mapToDouble` instead of standard `map`? (Answer: `mapToDouble` returns a primitive `DoubleStream`, avoiding the overhead of object boxing and exposing specialized terminal operations like `average()` and `sum()`).
- **Interviewer's Expectations**: Show correct filter mapping, handle null values, use primitive streams (`DoubleStream`), and handle empty results using `OptionalDouble`.

#### 12. Design a thread-safe counter class in Java without using the `synchronized` keyword.
- **Detailed Answer**: I will use `java.util.concurrent.atomic.AtomicInteger`, which utilizes CPU-level **Compare-And-Swap (CAS)** operations to perform lock-free thread-safe updates.
```java
import java.util.concurrent.atomic.AtomicInteger;

public class LockFreeCounter {
    private final AtomicInteger counter = new AtomicInteger(0);

    public void increment() {
        // Atomic increment using loop CAS checks under the hood
        counter.incrementAndGet();
    }

    public int getValue() {
        return counter.get();
    }
}
```
- **Follow-up Questions**: How does Compare-And-Swap (CAS) work? (Answer: CAS is a CPU instruction that updates a memory location only if its current value matches an expected value, returning true/false. If false, the thread retries in a loop, avoiding thread suspension overhead).
- **Interviewer's Expectations**: Recommend `AtomicInteger` and explain lock-free CAS operations over lock synchronization.

#### 13. Write a Java method to read a large 10GB text file line by line without running out of memory.
- **Detailed Answer**: Loading a 10GB file into memory (e.g. using `Files.readAllLines`) will trigger an `OutOfMemoryError`. I will use `Files.lines()`, which streams lines lazily from the disk without loading the entire file into RAM.
```java
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.stream.Stream;

public class LargeFileReader {
    public static void printLines(String fileLoc) {
        Path path = Paths.get(fileLoc);
        
        // try-with-resources ensures the stream closes, releasing file handles
        try (Stream<String> lines = Files.lines(path)) {
            lines.forEach(line -> {
                // Process line (only small chunk is in memory at a time)
                if (line.contains("ERROR")) {
                    System.out.println(line);
                }
            });
        } catch (IOException e) {
            System.err.println("File read error: " + e.getMessage());
        }
    }
}
```
- **Follow-up Questions**: How does `Files.lines` compare to `BufferedReader.readLine()`? (Answer: Under the hood, `Files.lines` wraps a `BufferedReader`, exposing the data as a Java 8 Stream).
- **Interviewer's Expectations**: Avoid full-file reads, recommend streams (`Files.lines`), and use try-with-resources to release file descriptors.

#### 14. You are designing a custom key class for a HashMap. How do you implement the class to ensure it works correctly?
- **Detailed Answer**:
1. Make the class **immutable**: Declare all fields as `private final` and omit setter methods. This prevents changes to key fields after insertion, which would alter the hash code and make the entry impossible to retrieve.
2. Override `equals(Object)`: Define what makes two keys logically equivalent (comparing all key fields).
3. Override `hashCode()`: Ensure equal objects return the same integer hash code using `Objects.hash()`.
```java
import java.util.Objects;

public final class CustomerKey {
    private final int id;
    private final String countryCode;

    public CustomerKey(int id, String countryCode) {
        this.id = id;
        this.countryCode = countryCode;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        CustomerKey that = (CustomerKey) o;
        return this.id == that.id && Objects.equals(this.countryCode, that.countryCode);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, countryCode);
    }
}
```
- **Follow-up Questions**: What happens if the key hash changes while stored in the map? (Answer: The map searches the wrong bucket, failing to find the key and leading to memory leaks).
- **Interviewer's Expectations**: Enforce immutability (`final`), and override both `equals()` and `hashCode()` consistently.

#### 15. You need to download data from 10 external APIs in parallel and merge the results. How do you design this?
- **Detailed Answer**: I will use **`CompletableFuture`** combined with a custom thread pool to avoid blocking the common fork-join pool:
```java
import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;

public class ParallelDataFetcher {
    public static List<String> fetchParallel(List<String> apiUrls) {
        // 1. Create a custom thread pool
        ExecutorService executor = Executors.newFixedThreadPool(Math.min(apiUrls.size(), 10));
        
        try {
            // 2. Launch async requests for each URL
            List<CompletableFuture<String>> futures = apiUrls.stream()
                .map(url -> CompletableFuture.supplyAsync(() -> mockDownload(url), executor))
                .collect(Collectors.toList());
                
            // 3. Wait for all requests to complete
            CompletableFuture<Void> allDone = CompletableFuture.allOf(
                futures.toArray(new CompletableFuture[0])
            );
            
            // Block and wait, then collect results
            return allDone.thenApply(v -> 
                futures.stream()
                    .map(CompletableFuture::join)
                    .collect(Collectors.toList())
            ).join();
            
        } finally {
            executor.shutdown();
        }
    }
    
    private static String mockDownload(String url) {
        // Mock download logic
        return "data_from_" + url;
    }
}
```
- **Follow-up Questions**: Why is a custom executor preferred over the default `ForkJoinPool.commonPool()`? (Answer: The common pool is designed for CPU-bound tasks. I/O-bound tasks (like API calls) can block threads, starving other parts of the application).
- **Interviewer's Expectations**: Recommend `CompletableFuture`, use custom thread executors, and collect results asynchronously.

---

### Debugging Questions

#### 16. A client logs show `java.util.ConcurrentModificationException` during list iteration. Explain the cause and fix.
- **Detailed Answer**:
- **Cause**: This exception occurs when a thread attempts to modify a Collection (adding or removing elements) while iterating over it using an Iterator (including implicit `for-each` loops), violating the collection's structure expectations.
- **Fix**:
  1. Use the explicit Iterator's `remove()` method:
     ```java
     Iterator<String> it = list.iterator();
     while(it.hasNext()) {
         if (it.next().equals("remove_me")) {
             it.remove(); // Safe modification
         }
     }
     ```
  2. Use Java 8's `removeIf()` method:
     ```java
     list.removeIf(item -> item.equals("remove_me"));
     ```
  3. Copy the elements to a concurrent collection (like `CopyOnWriteArrayList`) if multi-threaded modifications are occurring.
- **Follow-up Questions**: Why does the enhanced for-loop trigger this? (Answer: The compiler translates the enhanced for-loop into an Iterator structure. Modifying the list directly bypasses the Iterator, triggering the fail-fast check).
- **Interviewer's Expectations**: Identify modification checks, explain Iterator fail-fast mechanisms, and recommend `removeIf` or Iterator removal.

#### 17. Your application's memory usage grows continuously until it crashes with `OutOfMemoryError: Java heap space`. How do you troubleshoot this memory leak?
- **Detailed Answer**:
1. **Analyze logs**: Look for stack traces indicating where the heap run out of memory.
2. **Generate a Heap Dump**: Configure JVM flags to dump memory on crash: `-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/dumps/heap.hprof`. Or generate a dump manually using `jmap -dump:format=b,file=heap.hprof <PID>`.
3. **Inspect the Heap Dump**: Load the `.hprof` file into a memory profiler (like Eclipse MAT or VisualVM).
   - Use the **Histogram** view to identify which classes are consuming the most memory.
   - Use the **Leak Suspects** report to trace references from roots (GC Roots) to locating the objects preventing garbage collection (e.g. unclosed connections, static maps).
- **Follow-up Questions**: What is a "GC Root"? (Answer: Objects that are always reachable by the JVM, such as active thread stacks, local variables, or static variables).
- **Interviewer's Expectations**: Propose heap dump creation flags (`jmap`), analyze tool configurations (MAT), and detail GC Root tracking.

#### 18. A multi-threaded Java application hangs. Threads appear blocked. How do you diagnose a deadlock?
- **Detailed Answer**:
1. **Generate a Thread Dump**: Run the JVM tool `jstack <PID> > dump.txt` to capture the stack traces of all running threads.
2. **Inspect the Thread Dump**: Open the dump file. The JVM automatically runs deadlock detection, printing a summary at the bottom if a deadlock is found:
   ```text
   Found one Java-level deadlock:
   =============================
   "Thread-1": waiting to lock Monitor A, which is held by "Thread-2"
   "Thread-2": waiting to lock Monitor B, which is held by "Thread-1"
   ```
3. Run `jconsole` or `VisualVM` for real-time visual thread tracking.
- **Follow-up Questions**: How do you prevent deadlocks in code? (Answer: Always acquire locks in a consistent order across threads, or use timeout-based locks like `ReentrantLock.tryLock()`).
- **Interviewer's Expectations**: Propose thread dump utilities (`jstack`) and explain lock acquisition cycles.

#### 19. A database query fails because of a `NullPointerException` on a nested chain. How do you resolve this using `Optional`?
- **Detailed Answer**:
- **Problem**: `user.getProfile().getAddress().getCity().toLowerCase()` throws NPE if `Profile` or `Address` is null.
- **Resolution**: Refactor the getters to return `Optional` and chain them safely using `flatMap` and `map`:
```java
import java.util.Optional;

public class OptionalDemo {
    public static String getUserCity(User user) {
        return Optional.ofNullable(user)
            .flatMap(User::getProfile)
            .flatMap(Profile::getAddress)
            .map(Address::getCity)
            .map(String::toLowerCase)
            .orElse("unknown_city");
    }
}
```
- **Follow-up Questions**: Why should you avoid using `Optional` as method arguments or class fields? (Answer: `Optional` is not serializable and adds object wrapping overhead. Use it primarily as return types for methods that may return empty results).
- **Interviewer's Expectations**: Recommend `Optional.ofNullable`, chain using `flatMap` (for Optional returns) and `map` (for standard objects), and define a fallback.

#### 20. Your application is running slowly. Profiling shows that most time is spent in garbage collection pauses. How do you optimize?
- **Detailed Answer**:
1. **Reduce Object Allocation**: Avoid creating short-lived objects inside loops. Reuse objects or use primitives where possible.
2. **Tune Heap Sizes**: Adjust initial heap (`-Xms`) and max heap (`-Xmx`) to prevent the JVM from constantly resizing the heap.
3. **Configure Garbage Collectors**: If heap is large, switch to the G1 collector (`-XX:+UseG1GC`) or ZGC (`-XX:+UseZGC`) to reduce pause times.
4. **Tune Generations**: Increase the Young Generation size (`-XX:NewRatio`) to allow short-lived objects to be collected in minor GCs, preventing promotion to the Old Generation.
- **Follow-up Questions**: How do you monitor GC activity? (Answer: Enable GC logging using `-Xlog:gc*` to log GC execution details and pause times).
- **Interviewer's Expectations**: Identify heap sizing, garbage collector configurations, generation tuning, and object allocation reduction as tuning strategies.

---

### System Design Questions

#### 21. Design a thread-safe, in-memory cache in Java with Time-To-Live (TTL) eviction.
- **Detailed Answer**:
- **Storage**: Use `ConcurrentHashMap<K, CacheEntry<V>>` to handle concurrent reads and writes safely.
- **Entry Structure**: Wrap the cached value along with its expiration timestamp:
  ```java
  public class CacheEntry<V> {
      private final V value;
      private final long expiryTime;
      public CacheEntry(V value, long ttlMs) {
          this.value = value;
          this.expiryTime = System.currentTimeMillis() + ttlMs;
      }
      public boolean isExpired() { return System.currentTimeMillis() > expiryTime; }
  }
  ```
- **Eviction Strategy**:
  - **Passive Eviction**: When a key is requested (`get()`), check `isExpired()`. If true, remove the key from the map and return `null`.
  - **Active Eviction**: Run a background thread using `ScheduledExecutorService` every 60 seconds to scan the map, locate expired keys, and remove them to prevent memory growth.
- **Follow-up Questions**: How does `ConcurrentHashMap` achieve thread safety without locking the entire map? (Answer: It uses segment-level locking or CAS operations on bucket nodes, allowing threads to write to different buckets concurrently).
- **Interviewer's Expectations**: Propose `ConcurrentHashMap`, entry structures with timestamps, passive eviction checks, and background scheduler cleanups.

#### 22. Design a custom Thread Pool Executor in Java.
- **Detailed Answer**:
- **Core Components**:
  1. **Work Queue**: A thread-safe queue (`BlockingQueue<Runnable>`) to hold tasks waiting for execution.
  2. **Worker Thread Cluster**: A set of worker threads running in a loop, fetching tasks from the queue and executing them.
  3. **Core Pool Size**: The minimum number of active threads to keep alive.
  4. **Max Pool Size**: The maximum number of threads allowed.
- **Execution Loop**:
  ```java
  public class Worker extends Thread {
      public void run() {
          while (isRunning) {
              try {
                  // blocks if queue is empty
                  Runnable task = workQueue.take();
                  task.run();
              } catch (InterruptedException e) {
                  // handle shutdown
              }
          }
      }
  }
  ```
- **Submission logic**: When a task is submitted (`execute(task)`):
  - If active threads < core pool size: spawn a new worker thread.
  - If active threads >= core: add the task to the work queue.
  - If the queue is full and active threads < max: spawn a new worker thread.
  - If threads == max: trigger a rejection policy (e.g. abort policy).
- **Follow-up Questions**: Why use `BlockingQueue.take()` instead of a standard queue? (Answer: `take()` blocks the thread when the queue is empty, preventing busy-waiting loops that waste CPU cycles).
- **Interviewer's Expectations**: Detail queue selections (`BlockingQueue`), worker thread loops, pool limit thresholds, and rejection policies.

#### 23. Design a Rate Limiter library in Java using the Token Bucket algorithm.
- **Detailed Answer**:
- **Storage**: Maintain a map linking client IDs to bucket configurations.
- **Bucket Structure**:
  ```java
  public class TokenBucket {
      private final long capacity;
      private final double refillRatePerMs;
      private double tokens;
      private long lastRefillTimestamp;
      
      public synchronized boolean tryConsume() {
          refill();
          if (tokens >= 1.0) {
              tokens -= 1.0;
              return true;
          }
          return false;
      }
      
      private void refill() {
          long now = System.currentTimeMillis();
          long timePassed = now - lastRefillTimestamp;
          double tokensToAdd = timePassed * refillRatePerMs;
          tokens = Math.min(capacity, tokens + tokensToAdd);
          lastRefillTimestamp = now;
      }
  }
  ```
- **Synchronization**: Use synchronized blocks on the bucket instance to ensure thread safety during token checks and updates.
- **Follow-up Questions**: How do you scale this rate limiter across multiple application servers? (Answer: Move the token bucket state to a centralized Redis cache, using Lua scripts to perform atomic decrement and refill checks).
- **Interviewer's Expectations**: Implement token calculation formulas, handle thread synchronization, and discuss distributed scaling (Redis).

---

## 10. Common Mistakes

- **String Comparison using `==`**: Writing `if (name == "admin")` instead of `if ("admin".equals(name))`. `==` checks if the references point to the same memory address, which fails for strings created at runtime.
- **Broken Hash Contract**: Overriding `equals()` but omitting `hashCode()`. This prevents HashMap from locating keys, causing duplicate key insertions and memory leaks.
- **Catching Throwable**: Catching `Throwable` globally, which intercepts system-level errors (like `OutOfMemoryError`) that the application cannot recover from, hiding system failures.
- **Ignoring Resource Cleanup**: Opening files, sockets, or database connections without using `try-with-resources`, resulting in resource leaks that can crash the server.
- **Using LinkedList for Random Access**: Choosing `LinkedList` over `ArrayList` for collections where elements are retrieved by index, leading to slow $O(N)$ lookup times.

---

## 11. Comparison Section: Java vs. Kotlin vs. C++

| Feature | Java | Kotlin | C++ |
|---|---|---|---|
| **Compilation Model** | Bytecode (interpreted/JIT) | Bytecode (interpreted/JIT) | Native Machine Code (compiled) |
| **Memory Management** | Automatic (Garbage Collector) | Automatic (Garbage Collector) | Manual (`new`/`delete`, smart pointers) |
| **Null Safety** | Manual (`Optional`, annotations) | Inherent (Nullable `?` vs Non-Null)| Manual checks |
| **Concurrency Model** | Threads, ExecutorService, Virtual Threads | Coroutines (lightweight green threads) | Threads, mutexes, locks |
| **Platform Portability** | High (any JVM host) | High (JVM, Native, JS) | Low (must recompile per OS/CPU) |
| **Code Verbosity** | High (boilerplate required) | Low (concise syntax) | High |
| **Best Use Cases** | Enterprise backends, Big Data, Android | Android, Spring Boot microservices | Game engines, operating systems, finance |

---

## 12. Practical Project Ideas

### Beginner: Class-based Bank Account Simulation
Build a console application that defines `Account` and `Customer` classes. Implement methods to handle deposits, withdrawals, and interest rate calculations. Run transaction validations and throw custom exceptions for invalid operations.

### Intermediate: In-Memory Cache with TTL Eviction
Build an in-memory caching utility using `ConcurrentHashMap`. Store objects with a configurable Time-To-Live (TTL). Run a background scheduler using `ScheduledExecutorService` to automatically clean up expired keys. Write concurrent unit tests to verify thread safety.

### Advanced/Resume-worthy: Multi-threaded Web Crawler and Link Indexer
Create an asynchronous web crawler. Use a custom `ExecutorService` thread pool to fetch web pages in parallel. Parse pages using JSoup, extract links, and index them in a thread-safe collection. Evaluate performance across different thread pool configurations.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of JDK vs JRE vs JVM, basic inheritance structures, checked vs unchecked exceptions, and String comparison rules.
- **What Engineering Teams expect**: Familiarity with Java Collections (ArrayList vs HashMap), writing stream pipelines, implementing proper equals/hashCode contracts, and using try-with-resources.

---

## 14. Cheat Sheet

- **Collection Speeds**:
  - `ArrayList`: $O(1)$ read, $O(N)$ write.
  - `LinkedList`: $O(N)$ read, $O(1)$ write (ends).
  - `HashMap`: $O(1)$ read/write (assuming low collisions).
- **String appending**: Use `StringBuilder` inside loops instead of `+` concatenation.
- **Thread Safety**: Use `AtomicInteger` or `ConcurrentHashMap` for lock-free thread safety.
- **Signature Exception rules**: Checked exceptions must be declared (`throws`) or handled. Unchecked exceptions can be omitted.

---

## 15. One-Day Revision Guide

- [ ] Draw and explain the JVM runtime memory areas (Heap vs Stack vs Metaspace).
- [ ] Implement a class that overrides both `equals()` and `hashCode()` correctly.
- [ ] Write a Java Stream pipeline using filter, map, and collect.
- [ ] Describe the difference between checked and unchecked exceptions.
- [ ] Explain how type erasure affects generic types at runtime.
- [ ] Contrast the G1 and ZGC garbage collection algorithms.
