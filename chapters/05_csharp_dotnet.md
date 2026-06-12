# 5. C# & .NET

## 1. Introduction
### What it is
C# (C-Sharp) is a modern, statically typed, object-oriented programming language developed by Microsoft in 2000, led by Anders Hejlsberg. It runs on the .NET framework, a cross-platform software development platform providing a Common Language Runtime (CLR), a standard class library, and compiler tooling. C# integrates structural, component-oriented, functional, and generic programming paradigms.

### Why it exists
Historically, developers had to choose between high-performance systems languages like C++ (which require complex manual memory management and compile separately for each platform) and rapid application development languages (which were slower and lacked static type safety). C# and the .NET runtime were created to resolve this dichotomy, delivering execution speeds matching compiled native programs while ensuring memory safety, rapid development cycles, and multi-platform portability.

### Problems it solves
- **Memory Management**: Eliminates manual memory management bugs (such as double-frees and memory leaks) using automatic Garbage Collection (GC).
- **Type Safety**: Enforces compile-time and runtime type checks, preventing buffer overflows and illegal type casts.
- **Asynchronous Stalls**: Resolves thread-blocking latency during I/O operations (database calls, web queries) via the `async`/`await` pattern.
- **Platform Portability**: Compiles source code into Intermediate Language (IL) bytecode, which runs on any operating system (Windows, macOS, Linux) equipped with the .NET runtime.

### Industry Use Cases
- **Enterprise Web Backends**: High-performance API engines built with ASP.NET Core, running in Docker containers on Linux.
- **Game Development**: The primary language powering the Unity Game Engine for 2D, 3D, and VR games.
- **Cloud-Native Services**: Microservices, worker queues, and serverless functions deployed to Azure, AWS, or GCP.
- **Desktop Software**: Enterprise desktop tools constructed using WPF, WinForms, or cross-platform .NET MAUI.
- **Database Access Layers**: Fast database object-relational mapping using Entity Framework Core (EF Core).

### Analogy
If C++ is a manual racing motorcycle where the driver must manually shift gears, balance weight, and manage tires, C# on .NET is an automatic luxury sedan: it has automatic transmission, traction control, and collision warnings. You can still drive it at high speeds, but the vehicle automatically manages the engine timings and braking dynamics for you.

---

## 2. Core Concepts

### Beginner Concepts
- **Common Language Runtime (CLR)**: The execution engine of .NET that compiles Intermediate Language (IL) bytecode into CPU-specific native machine instructions using a Just-In-Time (JIT) compiler.
- **Value Types vs. Reference Types**:
  - **Value Types** (e.g., `struct`, `int`, `double`, `bool`) store data directly on the stack frame. Releasing or copying values duplicates the data.
  - **Reference Types** (e.g., `class`, `interface`, `string`, `object`) store a memory pointer on the stack, while the actual object data resides on the managed heap.
- **Encapsulation & Properties**: Hiding object state using private variables and exposing them safely through compiler-generated Properties (`get; set;`).
- **Interfaces**: Contracts defining methods, properties, and events that implementing classes must satisfy, enabling loose coupling.

### Intermediate Concepts
- **LINQ (Language Integrated Query)**: A declarative syntax allowing developers to query collections, databases, and XML streams using sql-like operations.
- **Generics**: Type-safe templates (e.g., `List<T>`) that allow classes and methods to operate on any type without the performance penalty of boxing.
- **Asynchronous Programming**: Structuring non-blocking, concurrent workflows using `async`, `await`, and `Task` signatures.
- **Delegates and Events**: Type-safe function pointers allowing class subscription models and decoupling event publishers from subscribers.
- **Exception Handling**: Standardized error management using `try-catch-finally` blocks to ensure resource cleanup.

### Advanced Concepts
- **Generational Garbage Collection**: The managed heap is divided into Generation 0 (short-lived temporary variables), Generation 1 (buffer zone), and Generation 2 (long-lived state). This structure optimizes memory sweeps.
- **Span<T> and Memory<T>**: Allocation-free representations of contiguous memory blocks, allowing slicing of strings and arrays without creating new heap objects.
- **Boxing and Unboxing**:
  - **Boxing**: Implicitly wrapping a stack value type into an `object` reference instance on the heap.
  - **Unboxing**: Explicitly casting the heap object reference back into a stack value type.
- **Reflection**: Inspecting assembly metadata, type schemas, and invoking classes dynamically at runtime.
- **ValueTask**: A performance-optimized version of `Task` that avoids heap allocations when an async method completes synchronously.

---

## 3. Internal Working

### CLR Execution Model and Heap Architecture
The C# compilation and execution flow is split into compile-time and runtime phases:

```text
+-----------------------+
|   C# Code Files       |
+-----------------------+
            | (C# Compiler - CSC)
            v
+-----------------------+
|  IL Bytecode (.dll)   | (Platform-independent bytecode + Metadata)
+-----------------------+
            |
            v  (CLR Execution Phase)
+-----------------------+
|  JIT Compiler (RyuJIT)| (Compiles IL into native machine instructions)
+-----------------------+
            |
            v
+-----------------------+
|  Native Machine Code  |
+-----------------------+
```

#### The .NET Managed Heap Layout
The CLR allocates dynamic memory into two primary managed heaps:
1. **Small Object Heap (SOH)**: Handles allocations smaller than 85,000 bytes. It is subdivided into three generations:
   - **Generation 0 (Gen 0)**: Newest allocations. Swept frequently in milliseconds.
   - **Generation 1 (Gen 1)**: The buffer zone. Objects that survive Gen 0 sweep are promoted here.
   - **Generation 2 (Gen 2)**: Long-lived objects (e.g., statics, singletons) and Large Objects. Collected rarely due to CPU cost.
2. **Large Object Heap (LOH)**: Handles allocations $\ge$ 85,000 bytes. Objects are allocated directly in Gen 2 and collected during Gen 2 passes. LOH is not compacted by default because moving large memory blocks is expensive, making it prone to memory fragmentation.

```text
Managed Heap:
+-----------------------------------------------------------------+
|  Small Object Heap (SOH)                                        |
|  [ Gen 0 (Fast Sweeps) ] -> [ Gen 1 (Buffer) ] -> [ Gen 2 ]     |
+-----------------------------------------------------------------+
|  Large Object Heap (LOH)                                        |
|  [ Allocations >= 85KB (Gen 2, No Compaction by default) ]      |
+-----------------------------------------------------------------+
```

---

## 4. Important Terminology
- **CLR**: Common Language Runtime, the execution virtual engine of .NET.
- **IL**: Intermediate Language, platform-independent bytecode generated from C# compile.
- **JIT**: Just-In-Time Compiler, translates IL to native code at execution time.
- **Boxing**: Wrapping a value type inside a heap reference object.
- **Unboxing**: Extracting the value type from the heap object.
- **SOH**: Small Object Heap, stores objects under 85,000 bytes in generations.
- **LOH**: Large Object Heap, stores objects $\ge$ 85k bytes without compaction.
- **IDisposable**: Interface requiring the release of unmanaged resources.
- **GC (Garbage Collector)**: The automated engine reclaiming heap memory.
- **Task**: Class representing an asynchronous execution operation.

---

## 5. Beginner Examples

### Example 1: Value Types (Struct) vs. Reference Types (Class)
```csharp
using System;

public struct CoordinatesStruct {
    public int Latitude;
    public int Longitude;
}

public class CoordinatesClass {
    public int Latitude;
    public int Longitude;
}

class Program {
    static void Main() {
        // Structs are allocated on the Stack and copied by value
        CoordinatesStruct s1 = new CoordinatesStruct { Latitude = 45, Longitude = 90 };
        CoordinatesStruct s2 = s1; // Copy of values
        s2.Latitude = 100;
        Console.WriteLine($"s1.Lat: {s1.Latitude}, s2.Lat: {s2.Latitude}"); // Output: s1.Lat: 45, s2.Lat: 100

        // Classes are allocated on the Heap and copied by reference pointer
        CoordinatesClass c1 = new CoordinatesClass { Latitude = 45, Longitude = 90 };
        CoordinatesClass c2 = c1; // Copy of reference pointer
        c2.Latitude = 100;
        Console.WriteLine($"c1.Lat: {c1.Latitude}, c2.Lat: {c2.Latitude}"); // Output: c1.Lat: 100, c2.Lat: 100
    }
}
```

### Example 2: Simple LINQ Filtering and Projection
```csharp
using System;
using System.Linq;
using System.Collections.Generic;

public class Student {
    public string Name { get; set; }
    public int Grade { get; set; }
}

class Program {
    static void Main() {
        List<Student> students = new List<Student> {
            new Student { Name = "Alice", Grade = 85 },
            new Student { Name = "Bob", Grade = 60 },
            new Student { Name = "Charlie", Grade = 90 }
        };

        // Query: Find students with Grade >= 70, order by Name
        var passedStudents = students
            .Where(s => s.Grade >= 70)
            .OrderBy(s => s.Name)
            .Select(s => s.Name)
            .ToList();

        Console.WriteLine(string.Join(", ", passedStudents)); // Output: Alice, Charlie
    }
}
```

---

## 6. Intermediate Examples

### Example 1: Async File I/O with Cancel Tokens
```csharp
using System;
using System.IO;
using System.Threading;
using System.Threading.Tasks;

public class LogProcessor {
    public async Task WriteLogAsync(string path, string message, CancellationToken token) {
        // Non-blocking file open and write
        using (StreamWriter writer = new StreamWriter(path, append: true)) {
            token.ThrowIfCancellationRequested(); // Check cancel request before write
            await writer.WriteLineAsync(message.AsMemory(), token);
            Console.WriteLine("Log written successfully.");
        }
    }
}

class Program {
    static async Task Main() {
        LogProcessor processor = new LogProcessor();
        CancellationTokenSource cts = new CancellationTokenSource();
        
        try {
            await processor.WriteLogAsync("app.log", "System Started.", cts.Token);
        } catch (OperationCanceledException) {
            Console.WriteLine("Operation cancelled.");
        }
    }
}
```

### Example 2: Implementing IDisposable and Finalizer Pattern
```csharp
using System;
using System.IO;

public class UnmanagedResourceWrapper : IDisposable {
    private FileStream _fileStream;
    private bool _disposed = false;

    public UnmanagedResourceWrapper(string filePath) {
        _fileStream = new FileStream(filePath, FileMode.OpenOrCreate);
    }

    // Public dispose: called deterministically by the developer
    public void Dispose() {
        Dispose(true);
        GC.SuppressFinalize(this); // Skip finalizer queue to save GC cycles
    }

    protected virtual void Dispose(bool disposing) {
        if (!_disposed) {
            if (disposing) {
                // Free managed resources
                _fileStream?.Dispose();
            }
            // Free unmanaged resources here (if any exist)
            _disposed = true;
        }
    }

    // Finalizer: fallback safety net called by the GC
    ~UnmanagedResourceWrapper() {
        Dispose(false);
    }
}
```

---

## 7. Advanced Concepts

### Span<T> and Memory<T> Allocation-Free Slicing
`Span<T>` represents a contiguous region of arbitrary memory. It is a ref struct allocated exclusively on the stack, preventing heap allocations during array or string parsing operations:

```csharp
using System;

class Program {
    static void Main() {
        string logLine = "2026-06-12 [INFO] Server Started";
        
        // Substring allocates a new string on the heap:
        // string dateStr = logLine.Substring(0, 10);
        
        // ReadOnlySpan slicing does NOT allocate any heap memory:
        ReadOnlySpan<char> span = logLine.AsSpan();
        ReadOnlySpan<char> dateSpan = span.Slice(0, 10);
        ReadOnlySpan<char> levelSpan = span.Slice(11, 6);
        
        Console.WriteLine($"Date: {dateSpan.ToString()}, Level: {levelSpan.ToString()}");
        // Output: Date: 2026-06-12, Level: [INFO]
    }
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for understanding of the .NET runtime lifecycle. They evaluate your ability to manage memory allocations, avoid blocking threads during async workflows, and optimize garbage collection paths in high-throughput applications.

### Red Flags
- Re-throwing exceptions with `throw ex;` (which destroys the call stack trace) instead of `throw;`.
- Blocking asynchronous code paths using `.Result` or `.Wait()`, risking deadlocks.
- Declaring classes with finalizers without implementing `IDisposable`, degrading GC performance.
- Allocating large byte arrays repeatedly instead of using `ArrayPool<T>` renting.

### Green Flags
- Utilizing `ValueTask` on hot paths where async methods often complete synchronously.
- Disabling change tracking in EF Core queries using `.AsNoTracking()` for read-only actions.
- Enforcing resource safety using `using` declarations and block-scopes.

### Answers Matrix
| Level | Question: "What is boxing and unboxing?" |
|---|---|
| **Rejected** | "It's when you put variables in boxes to make them safe." |
| **Shortlisted** | "Boxing converts value types to reference types on the heap. Unboxing casts it back." |
| **Selected** | "Boxing is the implicit conversion of a value type to an `object` or interface reference type, which allocates a wrapper object on the managed heap. Unboxing is the explicit extraction of the value type from the object. It incurs high performance overhead due to heap allocations and GC pressure, which is resolved using Generics." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is the difference between a class and a struct in C#?
- **Detailed Answer**: A class is a reference type stored on the heap, and its variables hold pointers to the heap address. Structs are value types stored on the stack (unless embedded inside a reference type). Class variables copy reference pointers, while struct variables duplicate the entire value during assignments. Classes support inheritance, while structs do not.
- **Follow-up Questions**: When should you define a struct? (Answer: For small, immutable structures representing single values under 16 bytes).
- **Interviewer's Expectations**: Distinguish stack vs heap allocations, value vs reference passing, and inheritance limitations.

#### 2. How does the .NET Garbage Collector work?
- **Detailed Answer**: The .NET GC manages memory using a generational sweep algorithm. Objects are categorized into Gen 0 (short-lived), Gen 1 (buffer), or Gen 2 (long-lived). The GC starts at roots (static references, stack variables), marks reachable objects, sweeps away dead objects, and compacts remaining memory blocks. Large objects ($\ge$ 85KB) are placed on the Large Object Heap (LOH), which is collected in Gen 2 without compaction to save CPU cycles.
- **Follow-up Questions**: What triggers a collection? (Answer: Low physical memory, allocations exceeding generational thresholds, or calling `GC.Collect()`).
- **Interviewer's Expectations**: Detail generational promotion, SOH/LOH differences, and marking phase roots.

#### 3. What is the difference between IDisposable.Dispose() and finalizers?
- **Detailed Answer**: `Dispose()` is called deterministically by developers to free unmanaged resources immediately. Finalizers (`~ClassName()`) are called nondeterministically by the GC before destroying the object. Implementing `Dispose` allows resources to be freed immediately, while finalizers act as a fallback safety net.
- **Follow-up Questions**: Why use `GC.SuppressFinalize`? (Answer: It tells the GC that resources are already cleaned up, removing the object from the finalization queue and saving GC sweeps).
- **Interviewer's Expectations**: Contrast deterministic and nondeterministic resource cleaning.

#### 4. Explain the async/await model and how it avoids thread blocking.
- **Detailed Answer**: The `async`/`await` model is compiled into a state machine. When an `await` is encountered on a running task, the method yields control, allowing the thread to return to the ThreadPool to execute other tasks. Once the awaited task completes, a thread resumes execution from the saved state. This prevents thread starvation during I/O operations.
- **Follow-up Questions**: What is SynchronizationContext? (Answer: The context that directs execution threads back to a specific environment, like the UI thread).
- **Interviewer's Expectations**: Detail thread yielding and state machine compilation.

#### 5. Explain boxing and unboxing and how to avoid them.
- **Detailed Answer**: Boxing wraps a value type (e.g. `int`) inside an `object` container allocated on the heap. Unboxing casts the object reference back to a value type. This incurs performance costs due to heap allocations and type-cast checks. It is avoided by using generic collections (like `List<T>`) instead of obsolete non-generic collections (like `ArrayList`).
- **Follow-up Questions**: Does boxing occur when using interfaces? (Answer: Yes, if a struct implements an interface and is cast to that interface type, it is boxed).
- **Interviewer's Expectations**: Detail heap allocation penalties and generic collection benefits.

#### 6. What is the difference between string and StringBuilder?
- **Detailed Answer**: Strings are immutable; modifying a string creates a new string object on the heap, leading to memory allocations in loops. `StringBuilder` is mutable; it maintains an internal buffer array to modify text in place, avoiding new heap allocations.
- **Follow-up Questions**: What is the String Intern Pool? (Answer: A table maintained by the CLR storing single copies of literal strings to reduce memory consumption).
- **Interviewer's Expectations**: Contrast immutability vs mutability memory allocations.

#### 7. What are the differences between virtual, override, and new keywords?
- **Detailed Answer**:
  - `virtual` allows a method in a base class to be overridden by subclasses.
  - `override` extends or replaces the base virtual method, supporting polymorphism.
  - `new` hides a base class method without overriding it. Calling the method on a base class pointer executes the base implementation rather than the derived one.
- **Follow-up Questions**: What is object slicing in C#? (Answer: Not directly present since references are pointers, but casting to base changes accessible APIs).
- **Interviewer's Expectations**: Differentiate dynamic dispatch overrides from method hiding.

#### 8. Explain LINQ Deferred Execution vs Eager Execution.
- **Detailed Answer**: LINQ queries use deferred execution by default; they do not execute until the query is iterated (e.g. in a `foreach` loop or calling `ToList()`). Eager execution runs immediately upon invocation (e.g. calling `ToList()`, `ToArray()`, or aggregation functions like `Count()`).
- **Follow-up Questions**: What is the risk of deferred execution in loops? (Answer: Executing queries multiple times if iterated repeatedly, or executing after database contexts are closed).
- **Interviewer's Expectations**: Connect iteration triggers to query execution timing.

#### 9. What is the difference between Task and ValueTask?
- **Detailed Answer**: `Task` is a reference type allocated on the heap, which incurs allocation overhead even if the task completes synchronously. `ValueTask` is a struct type allocated on the stack. If an async method completes synchronously, `ValueTask` executes without heap allocations, reducing GC pressure.
- **Follow-up Questions**: When should you still use `Task`? (Answer: When the operation completes asynchronously most of the time, or when you need to await the task multiple times).
- **Interviewer's Expectations**: Contrast heap reference types with stack value types.

#### 10. Explain compilation in .NET: JIT vs AOT.
- **Detailed Answer**:
  - **JIT (Just-In-Time)** compiles IL bytecode to machine code at runtime as methods are called. This allows CPU-specific optimizations but introduces startup latency.
  - **AOT (Ahead-of-Time)** compiles IL directly to machine code during the build process, eliminating startup latency and reducing runtime footprint.
- **Follow-up Questions**: What is Tiered Compilation? (Answer: A JIT feature that compiles code quickly first, then compiles optimized versions for frequently called methods).
- **Interviewer's Expectations**: Contrast compile timings and startup latency.

#### 11. What is the difference between IEnumerable, IQueryable, and ICollection?
- **Detailed Answer**:
  - `IEnumerable`: Read-only, forward-only iteration over in-memory collections. Operates on client-side memory.
  - `IQueryable`: Represents queries against out-of-memory databases (EF Core), translating LINQ expressions to SQL queries executed on the database server.
  - `ICollection`: Extends `IEnumerable` to support modifications (Add, Remove) and count checks.
- **Follow-up Questions**: What happens if you run `.Where()` on `IEnumerable` vs `IQueryable`? (Answer: `IEnumerable` pulls the entire table into memory and filters on the client. `IQueryable` runs the filter on the database).
- **Interviewer's Expectations**: Differentiate client-side in-memory queries from database-side SQL executions.

#### 12. Explain C# 10/11 records and how they differ from classes.
- **Detailed Answer**: A `record` is a reference type (or value type if declared as `record struct`) optimized for immutable data structures. Unlike classes, records implement value-based equality by default; two record instances are equal if their property values match, even if they occupy different memory addresses.
- **Follow-up Questions**: What is the `with` expression? (Answer: A record feature that creates a copy of the record with specified properties modified).
- **Interviewer's Expectations**: Explain value-based equality and immutability.

#### 13. What is the difference between Thread, ThreadPool, and Task?
- **Detailed Answer**:
  - `Thread`: A heavy, OS-level thread with its own stack memory. Expensive to create and destroy.
  - `ThreadPool`: A pool of pre-allocated threads. Tasks are queued to the pool, avoiding thread creation latency.
  - `Task`: A high-level abstraction representing an asynchronous operation, running on the ThreadPool.
- **Follow-up Questions**: How do you run a task on a new background thread? (Answer: Call `Task.Run()`).
- **Interviewer's Expectations**: Describe the hierarchy of threads and pool worker queues.

### Scenario-Based Questions

#### 14. Implement a thread-safe Singleton pattern using Lazy<T>.
- **Detailed Answer**:
  ```csharp
  public sealed class Singleton {
      private static readonly Lazy<Singleton> _instance = 
          new Lazy<Singleton>(() => new Singleton());

      public static Singleton Instance => _instance.Value;

      private Singleton() { }
  }
  ```
- **Follow-up Questions**: Is this lazy initialization thread-safe? (Answer: Yes, `Lazy<T>` guarantees thread safety and single initialization internally).
- **Interviewer's Expectations**: Show private constructors and lazy instantiation patterns.

#### 15. Design an ASP.NET Core Middleware to log request latency.
- **Detailed Answer**:
  ```csharp
  public class LatencyLoggerMiddleware {
      private readonly RequestDelegate _next;
      public LatencyLoggerMiddleware(RequestDelegate next) => _next = next;

      public async Task InvokeAsync(HttpContext context) {
          var watch = System.Diagnostics.Stopwatch.StartNew();
          await _next(context); // Forward request
          watch.Stop();
          Console.WriteLine($"Request took {watch.ElapsedMilliseconds} ms");
      }
  }
  ```
- **Follow-up Questions**: How do you register this middleware? (Answer: Call `app.UseMiddleware<LatencyLoggerMiddleware>()` in Program.cs).
- **Interviewer's Expectations**: Show downstream forwarding and latency tracking.

#### 16. You have a database connection leak in production. How do you resolve it?
- **Detailed Answer**: Ensure all connection and context allocations use the `using` statement or `using` declaration. This guarantees the `Dispose` or `DisposeAsync` method is called even when exceptions occur, closing raw connection pools:
  ```csharp
  using (var connection = new SqlConnection(connString)) {
      await connection.OpenAsync();
      // Execute DB queries
  } // Automatically closed here
  ```
- **Follow-up Questions**: How does EF Core handle database connection lifetimes? (Answer: DbContext instances manage connection pooling automatically if lifetime-scoped correctly, e.g., Scoped lifetime).
- **Interviewer's Expectations**: Show `using` block compilation translation to `try-finally`.

#### 17. What are the performance implications of using EF Core with tracked entities? How do you optimize?
- **Detailed Answer**: By default, EF Core tracks changes to all queried entities. This stores a copy of the entity in the DbContext tracking graph, causing high memory and CPU overhead during queries. For read-only operations, disable tracking using `.AsNoTracking()` to improve query speeds:
  ```csharp
  var users = await _context.Users.AsNoTracking().ToListAsync();
  ```
- **Follow-up Questions**: Can you configure no-tracking globally? (Answer: Yes, by changing change tracker options on the DbContext initialization configuration).
- **Interviewer's Expectations**: Contrast tracking graph overhead with raw queries.

#### 18. How do you pass data efficiently between threads without memory allocations?
- **Detailed Answer**: Use `System.Threading.Channels` instead of generic thread-safe queues. Channels provide high-performance, asynchronous producer-consumer pipelines with minimal allocations, supporting backpressure configurations.
- **Follow-up Questions**: What is backpressure? (Answer: Restricting producer speeds when consumer queues exceed capacity bounds to prevent out-of-memory errors).
- **Interviewer's Expectations**: Propose Channels over blocking collections.

### Debugging Questions

#### 19. Debug this NullReferenceException:
```csharp
public class UserService {
    private List<User> _users;
    public void AddUser(User u) => _users.Add(u);
}
```
- **Detailed Answer**: The crash occurs because the `_users` list field is declared but never initialized. Calling `.Add(u)` on a null object pointer throws a `NullReferenceException`.
- **Fix**: Initialize the list: `private List<User> _users = new();`.
- **Follow-up Questions**: What is nullable reference types (NRT)? (Answer: A compiler feature that raises warnings when accessing potential null objects unless marked with `?`).
- **Interviewer's Expectations**: Spot unitialized field references.

#### 20. Debug this memory leak:
```csharp
public class InventoryMonitor {
    public InventoryMonitor(StockManager manager) {
        manager.StockChanged += OnStockChanged;
    }
    private void OnStockChanged(object sender, EventArgs e) { /* Update UI */ }
}
```
- **Detailed Answer**: The `InventoryMonitor` subscribes to the `StockManager` event. If the `StockManager` is a long-lived object, it maintains a reference to the `InventoryMonitor` delegate. Even if the monitor goes out of scope, the GC cannot reclaim it because of this reference, causing a memory leak.
- **Fix**: Implement `IDisposable` on `InventoryMonitor` and unsubscribe from the event: `manager.StockChanged -= OnStockChanged;` in `Dispose()`.
- **Follow-up Questions**: How can we avoid manual unsubscribing? (Answer: Use weak event patterns or weak reference handles).
- **Interviewer's Expectations**: Identify event subscription leaks.

#### 21. Why does this async method block the thread pool?
```csharp
public int GetValue() {
    return FetchValueAsync().Result;
}
```
- **Detailed Answer**: Accessing `.Result` (or calling `.Wait()`) blocks the calling thread synchronously until the task completes. If this is run on a UI thread or single-threaded ASP.NET context, it blocks the thread dispatcher. If the awaited task needs that same thread to complete, a deadlock occurs.
- **Fix**: Make the calling method async and await the task: `public async Task<int> GetValueAsync() => await FetchValueAsync();`.
- **Follow-up Questions**: What does `.ConfigureAwait(false)` do? (Answer: Tells the task executor not to marshal the execution context back to the original synchronization context, preventing UI deadlocks).
- **Interviewer's Expectations**: Identify blocking sync over async task execution.

#### 22. Identify the race condition:
```csharp
private int _counter = 0;
public void Increment() {
    _counter++;
}
```
- **Detailed Answer**: The increment operation is not thread-safe. Under the hood, `_counter++` performs three steps: read current value, increment, and write back. In a multi-threaded environment, threads can read the same value concurrently, causing lost updates.
- **Fix**: Use `Interlocked.Increment(ref _counter)` or protect the operation with a `lock` block.
- **Follow-up Questions**: Why is `Interlocked` preferred over `lock`? (Answer: It uses CPU-level atomic instructions without the overhead of thread context switching).
- **Interviewer's Expectations**: Explain non-atomic instructions in variable modification.

#### 23. Debug this incorrect task execution layout:
```csharp
public async Task ProcessData() {
    foreach (var item in items) {
        Task.Run(() => Compute(item));
    }
}
```
- **Detailed Answer**: The loop launches multiple tasks using `Task.Run` but never awaits their completion or stores their handles. The `ProcessData` method returns immediately, and the tasks run in the background unsupervised. Any exception thrown inside `Compute` will be swallowed.
- **Fix**: Store tasks in a collection and await all of them: `await Task.WhenAll(items.Select(item => Task.Run(() => Compute(item))));`.
- **Follow-up Questions**: What happens to exceptions thrown in `Task.WhenAll`? (Answer: They are aggregated and thrown as an `AggregateException`).
- **Interviewer's Expectations**: Recognize fire-and-forget task risks.\n\n#### 24. What is the difference between const and readonly in C#?
- **Detailed Answer**: `const` represents a compile-time constant. Its value is evaluated at compile-time and hardcoded directly into the IL bytecode of assembly consumers. `readonly` is a runtime constant. It is evaluated at runtime and can be assigned inside class constructors.
- **Follow-up Questions**: What is a danger of changing `const` variables in shared libraries? (Answer: Class consumers in other assemblies must be recompiled, otherwise they will continue to use the old hardcoded value).
- **Interviewer's Expectations**: Contrast compile-time evaluation with constructor runtime assignments.

#### 25. Explain the difference between IEnumerable and IEnumerator.
- **Detailed Answer**: `IEnumerable` is a contract that exposes an `GetEnumerator()` method, allowing a collection to be iterated using a `foreach` loop. `IEnumerator` is the iterator object itself, maintaining state coordinates (with properties `Current` and methods `MoveNext()`, `Reset()`).
- **Follow-up Questions**: Is `IEnumerable` thread-safe? (Answer: No, because multiple threads calling `GetEnumerator()` concurrently share the collection index unless synchronized).
- **Interviewer's Expectations**: Differentiate iteration contracts from iterator state drivers.

#### 26. What is the Global Assembly Cache (GAC)?
- **Detailed Answer**: The GAC is a centralized folder structure in Windows used by .NET Framework to store shared assemblies. It allows multiple applications on the computer to share DLL files, requiring assemblies to be signed with a strong name key.
- **Follow-up Questions**: Does .NET Core/Modern .NET use the GAC? (Answer: No, modern .NET uses application-local dependencies or NuGet folders, bypassing GAC DLL versioning conflicts).
- **Interviewer's Expectations**: Mention strong name requirements and modern local dependencies.

#### 27. Explain Covariance and Contravariance in C# generics.
- **Detailed Answer**:
  - **Covariance** (`out` keyword): Allows a method to return a more derived type than specified in the generic parameters (e.g. assigning `IEnumerable<Derived>` to `IEnumerable<Base>`).
  - **Contravariance** (`in` keyword): Allows a method to accept a less derived type (e.g. passing `Action<Base>` where `Action<Derived>` is expected).
- **Follow-up Questions**: Can value types support covariance? (Answer: No, covariance and contravariance apply only to reference types).
- **Interviewer's Expectations**: Contrast input parameter directions (`in`) with output return directions (`out`).

#### 28. What are indexers in C#, and how are they defined?
- **Detailed Answer**: Indexers allow instances of a class to be indexed like arrays using the square brackets syntax. They are defined using the `this` keyword: `public T this[int index] { get; set; }`.
- **Follow-up Questions**: Can indexers be overloaded? (Answer: Yes, by defining indexers with different index parameter types, like indexing by a string key).
- **Interviewer's Expectations**: Show `this` index syntax definitions.

#### 29. Explain dependency injection lifetimes in ASP.NET Core.
- **Detailed Answer**:
  - **Transient**: A new service instance is created every time it is requested from the DI container.
  - **Scoped**: A single service instance is created per HTTP request lifecycle, shared by all classes handling that request.
  - **Singleton**: A single service instance is created once and shared globally across the entire application lifetime.
- **Follow-up Questions**: What is a Captive Dependency? (Answer: A configuration error where a transient or scoped service is injected into a singleton service, extending the scoped resource's lifetime inappropriately).
- **Interviewer's Expectations**: Differentiate lifetimes and identify captive dependency risks.

#### 30. What is the role of yield return in C# iterators?
- **Detailed Answer**: The `yield return` keyword creates an iterator state machine under the hood. When called, the method evaluates the value, returns it to the caller, and pauses its execution state. On the next iteration loop, execution resumes from that exact paused state, enabling lazy O(1) evaluation.
- **Follow-up Questions**: What happens to local variables inside a `yield return` function? (Answer: They are compiled into class fields within the compiler-generated iterator state machine class).
- **Interviewer's Expectations**: Detail compile-time state machine generation and lazy execution.

#### 31. Explain compiled vs interpreted queries in EF Core.
- **Detailed Answer**: By default, EF Core parses and compiles LINQ queries to SQL at runtime when invoked, which adds compilation latency. Compiled queries allow developers to pre-compile the LINQ structure using `EF.CompileAsyncQuery`, skipping compilation on subsequent database calls.
- **Follow-up Questions**: Does EF Core cache compiled SQL statements automatically? (Answer: Yes, EF Core uses an internal query cache to store generated SQL templates, but the LINQ expression parsing still runs).
- **Interviewer's Expectations**: Contrast runtime SQL parses with pre-compiled query declarations.

#### 32. What is the difference between Monitor and Mutex in .NET?
- **Detailed Answer**:
  - `Monitor` (the lock keyword): A lightweight, thread synchronization block limited to the hosting process.
  - `Mutex`: An OS-level kernel synchronization primitive that can synchronize threads across separate processes (inter-process synchronization).
- **Follow-up Questions**: Which is faster? (Answer: `Monitor` is significantly faster because it does not require OS kernel context switches).
- **Interviewer's Expectations**: Contrast in-process synchronization with inter-process kernel locks.

#### 33. How does the dynamic keyword work under the hood in C#?
- **Detailed Answer**: The `dynamic` keyword bypasses compile-time type checking. Under the hood, the compiler translates dynamic calls into expressions utilizing the **DLR (Dynamic Language Runtime)**. The DLR inspects type signatures at runtime and binds methods dynamically, caching the dispatch paths.
- **Follow-up Questions**: How does `dynamic` differ from `object`? (Answer: `object` requires explicit type casts to access properties; `dynamic` resolves properties at runtime without casting).
- **Interviewer's Expectations**: Explain DLR runtime lookups and resolution caches.

#### 34. What is the difference between Thread.Sleep and Task.Delay?
- **Detailed Answer**:
  - `Thread.Sleep`: Blocks the active thread synchronously, preventing it from executing other tasks.
  - `Task.Delay`: An asynchronous operation that schedules a timer and yields the execution thread back to the pool, resuming when the timer completes.
- **Follow-up Questions**: Which should be used in async methods? (Answer: `Task.Delay`, to prevent thread pool starvation).
- **Interviewer's Expectations**: Contrast synchronous thread blocks with asynchronous timer yields.

#### 35. What is structural casting and how does it relate to the as operator?
- **Detailed Answer**: In C#, the `as` operator attempts to cast an object to a reference or nullable type. If the cast fails, it returns `null` instead of throwing an exception, making it safer than direct casts.
- **Follow-up Questions**: Can you use `as` with value types like `int`? (Answer: Only if they are declared as nullable value types like `int?`).
- **Interviewer's Expectations**: Contrast `as` operator null results with direct casting exception risks.

#### 36. Explain garbage collection patterns: Server GC vs Workstation GC.
- **Detailed Answer**:
  - **Workstation GC**: Optimized for desktop apps. Runs on a single background thread to minimize UI interruptions.
  - **Server GC**: Optimized for high-throughput backend apps. Creates a separate GC thread and allocation queue per CPU core, processing sweeps concurrently.
- **Follow-up Questions**: How do you configure Server GC? (Answer: By enabling `System.GC.Server` in the runtime configuration JSON or project file).
- **Interviewer's Expectations**: Contrast thread allocation models based on hosting types.

#### 37. What is type erasure in compiler outputs and does .NET do it?
- **Detailed Answer**: Type erasure is a compiler step (common in Java) where generic type arguments are stripped during compilation and replaced with basic objects, requiring casts at runtime. .NET does not perform type erasure; generics are preserved as first-class metadata in compiled assemblies, allowing the JIT to generate optimal, type-specific native machine code.
- **Follow-up Questions**: What is a benefit of preserving generics? (Answer: Runtime performance optimization and type safety checks during reflection).
- **Interviewer's Expectations**: Contrast Java's type erasure with .NET's generic metadata preservation.

#### 38. Explain class constructors in static vs non-static scopes.
- **Detailed Answer**: Static constructors (`static MyClass()`) initialize static fields and execute exactly once before the class is first instantiated or accessed. They cannot have parameters or access modifiers. Non-static constructors run every time an object instance is created, initializing instance state.
- **Follow-up Questions**: Can you call static constructors manually? (Answer: No, the CLR manages their execution automatically).
- **Interviewer's Expectations**: Detail execution timings and parameter limitations.

#### 39. What are the rules of pattern matching in C#?
- **Detailed Answer**: Pattern matching evaluates expressions against type shapes and structures. It supports declaration checks, type casting, property filters, relational operators, and logical combinations (e.g. `is Student { Grade: >= 70 }`).
- **Follow-up Questions**: How does pattern matching improve readability? (Answer: By replacing nested `if-else` and cast statements with clean, declarative switch expressions).
- **Interviewer's Expectations**: Detail structural and property matching expressions.

#### 40. Explain structural records and equality overrides.
- **Detailed Answer**: In C#, `record` types compile default implementations of `Equals()`, `GetHashCode()`, and comparison operators to evaluate value-based equality. Two record objects are equal if their fields match.
- **Follow-up Questions**: How do records handle inheritance? (Answer: Record classes support inheritance, but record structs do not).
- **Interviewer's Expectations**: Highlight value-based equality over reference address comparison.\n\n\n\n#### 41. What is the difference between is and as in C#?
- **Detailed Answer**: The `is` operator checks if an object is compatible with a given type and returns a boolean, or extracts the cast value directly in modern C# (`if (obj is Student s)`). The `as` operator attempts to cast an object to a reference or nullable type, returning `null` on failure.
- **Follow-up Questions**: Which is preferred in modern C#? (Answer: The `is` operator with pattern matching, as it combines type checking and assignment in one step).
- **Interviewer's Expectations**: Contrast boolean checks with null-result casts.

#### 42. Explain the purpose of the volatile keyword in C#.
- **Detailed Answer**: The `volatile` keyword indicates that a field can be modified by multiple threads concurrently. It prevents the compiler or CPU from optimizing or reordering reads/writes to that field, ensuring that the thread always reads the most up-to-date value.
- **Follow-up Questions**: Does `volatile` make increment operations thread-safe? (Answer: No, it only ensures visibility. Operations like `x++` still require locks or `Interlocked`).
- **Interviewer's Expectations**: Emphasize instruction reordering prevention and visibility.

#### 43. What is the difference between Task.WhenAll and Task.WaitAll?
- **Detailed Answer**:
  - `Task.WhenAll`: An asynchronous method returning a `Task` that can be awaited, yielding the execution thread back to the pool.
  - `Task.WaitAll`: A synchronous blocking method that halts the calling thread until all tasks complete, risking deadlocks in single-threaded contexts.
- **Follow-up Questions**: How are exceptions aggregated? (Answer: Both wrap exceptions in an `AggregateException` container).
- **Interviewer's Expectations**: Contrast asynchronous yields with synchronous thread blocks.

#### 44. Explain the role of the Dynamic Language Runtime (DLR) in C#.
- **Detailed Answer**: The DLR is an execution environment that adds dynamic scripting capabilities to .NET. It sits on top of the CLR, resolving method calls at runtime using a dynamic call site cache.
- **Follow-up Questions**: Which keyword triggers the DLR? (Answer: The `dynamic` keyword).
- **Interviewer's Expectations**: Detail runtime method binding.

#### 45. What are anonymous types in C# and when should they be used?
- **Detailed Answer**: Anonymous types allow you to declare read-only object properties without defining a class explicitly: `var user = new { Name = "Alice", Age = 30 }`. They are used for local data projections in LINQ queries.
- **Follow-up Questions**: What is the scope of anonymous types? (Answer: They are internal to the assembly in which they are declared).
- **Interviewer's Expectations**: Highlight read-only properties and LINQ projection uses.

#### 46. Explain the difference between System.String and System.Text.StringBuilder.
- **Detailed Answer**: `System.String` represents immutable text; modifying a string allocates a new string object on the heap. `StringBuilder` represents a mutable string, modifying characters inside a pre-allocated buffer array to avoid allocations.
- **Follow-up Questions**: What is the default starting capacity of `StringBuilder`? (Answer: 16 characters).
- **Interviewer's Expectations**: Contrast immutability with mutable buffer allocations.

#### 47. What is the difference between GC.Collect() and letting the GC run automatically?
- **Detailed Answer**: The GC runs automatically based on memory allocation metrics. Calling `GC.Collect()` forces a synchronous collection pass across all generations, suspending application threads, which can introduce latency. It should be avoided in production.
- **Follow-up Questions**: When is it acceptable to call `GC.Collect()`? (Answer: In testing environments, or when cleaning up large allocations before entering idle cycles).
- **Interviewer's Expectations**: Explain performance penalties of forced collections.

#### 48. Explain the purpose of the ThreadLocal<T> class.
- **Detailed Answer**: `ThreadLocal<T>` allocates a separate, isolated instance of a variable for each executing thread. Threads read and write their own copy of the variable without locking, preventing concurrency races.
- **Follow-up Questions**: How does this differ from the `[ThreadStatic]` attribute? (Answer: `ThreadLocal<T>` supports lazy initialization and instance-level fields, while `[ThreadStatic]` only supports static fields).
- **Interviewer's Expectations**: Detail thread-local storage and lazy initialization.

#### 49. What is the difference between ConcurrentDictionary and Dictionary with locks?
- **Detailed Answer**: A standard `Dictionary` with locks blocks all read and write operations during modifications, causing lock contention. `ConcurrentDictionary` uses fine-grained locking, locking only the specific hash bucket being modified, allowing concurrent reads without blocking.
- **Follow-up Questions**: Does `ConcurrentDictionary` require locks for reads? (Answer: No, read operations are lock-free).
- **Interviewer's Expectations**: Explain bucket-level locking and lock-free reads.

#### 50. Explain how C# implements events using multicast delegates.
- **Detailed Answer**: Events wrap multicast delegates. When a subscriber registers (`+=`), the compiler combines the delegate instances into an execution list. When the event is raised, the delegates in the list are invoked sequentially.
- **Follow-up Questions**: What happens if a subscriber throws an exception? (Answer: It halts the invocation list, preventing subsequent subscribers from receiving the event).
- **Interviewer's Expectations**: Detail delegate combining and invocation lists.

#### 51. What is the dynamic keyword and how does it differ from object?
- **Detailed Answer**: `dynamic` tells the compiler to bypass compile-time validation, resolving method calls at runtime using the DLR. `object` represents the base type, requiring explicit casting to access members.
- **Follow-up Questions**: Does `dynamic` have a performance cost? (Answer: Yes, due to runtime lookup and compilation overheads).
- **Interviewer's Expectations**: Contrast DLR lookups with type casting.

#### 52. Explain the purpose of Expression<Func<T>> in LINQ.
- **Detailed Answer**: An `Expression<Func<T>>` compiles a lambda expression into an Abstract Syntax Tree (AST) representation instead of executable code. This allows database providers (like EF Core) to parse the tree and translate it into SQL.
- **Follow-up Questions**: How does it differ from a standard `Func<T>` delegate? (Answer: `Func<T>` is compiled directly to IL executable bytecode; it cannot be parsed or translated).
- **Interviewer's Expectations**: Detail AST representation and SQL translations.

#### 53. What is the difference between struct and class memory layouts?
- **Detailed Answer**: Structs are value types allocated on the stack (or inline inside classes), copying values during assignment. Classes are reference types allocated on the managed heap, copying reference pointers during assignment.
- **Follow-up Questions**: What is the default memory layout of a struct? (Answer: `LayoutKind.Sequential`, where members are allocated in order of declaration).
- **Interviewer's Expectations**: Contrast stack allocation with reference pointer copies.

#### 54. Explain the purpose of the Nullable<T> struct.
- **Detailed Answer**: `Nullable<T>` (denoted as `T?`) wraps a value type struct, adding a boolean field `HasValue` and a `Value` property to allow value types to represent null states, commonly used in database bindings.
- **Follow-up Questions**: What is the size of `int?`? (Answer: 5 bytes (4 bytes for int + 1 byte for bool), but rounded to 8 bytes due to alignment padding).
- **Interviewer's Expectations**: Detail the internal representation fields.

#### 55. What is the using statement and how does it compile?
- **Detailed Answer**: The `using` statement (or `using` declaration) guarantees that `Dispose()` is called on an `IDisposable` object when leaving scope. The compiler translates the block into a `try-finally` block, executing `Dispose()` inside the `finally` block.
- **Follow-up Questions**: What if the object is null? (Answer: The compiler-generated code checks for null before calling `Dispose()`).
- **Interviewer's Expectations**: Show `try-finally` compilation translations.

#### 56. Explain the difference between System.Threading.Monitor and Mutex.
- **Detailed Answer**: `Monitor` is a lightweight, in-process synchronization lock. `Mutex` is an OS-level kernel synchronization primitive that can synchronize threads across separate processes (inter-process lock).
- **Follow-up Questions**: Which is faster? (Answer: `Monitor` is much faster because it does not require OS kernel transitions).
- **Interviewer's Expectations**: Contrast in-process and inter-process locking.

#### 57. What is the role of yield return in C# iterators?
- **Detailed Answer**: The `yield return` keyword compiles the method into an iterator state machine class, pausing execution after each return and resuming from the saved state on the next call.
- **Follow-up Questions**: Can you put `yield return` inside a `try-catch` block? (Answer: No, it is disallowed by the compiler because the state machine cannot guarantee exception cleanup across paused states).
- **Interviewer's Expectations**: Detail state machine compilation constraints.

#### 58. Explain compiled vs interpreted queries in EF Core.
- **Detailed Answer**: Interpreted queries parse the LINQ expression tree to generate SQL on every call. Compiled queries pre-compile the LINQ structure using `EF.CompileAsyncQuery`, caching the SQL template to avoid parsing overhead.
- **Follow-up Questions**: Does EF Core cache SQL queries automatically? (Answer: Yes, but the expression parsing phase still runs).
- **Interviewer's Expectations**: Contrast parsing overheads.

#### 59. What is the Global Assembly Cache (GAC)?
- **Detailed Answer**: The GAC is a system-wide folder in Windows used by .NET Framework to store shared assemblies signed with a strong name. It is not used in modern .NET (.NET Core), which relies on application-local dependencies.
- **Follow-up Questions**: Why did modern .NET drop the GAC? (Answer: To prevent versioning conflicts ("DLL Hell") and support cross-platform self-contained deployments).
- **Interviewer's Expectations**: Explain DLL version sharing and modern deployment changes.

#### 60. Explain Covariance and Contravariance in C# generics.
- **Detailed Answer**: Covariance (`out`) allows returning a more derived type. Contravariance (`in`) allows accepting a less derived type. They apply only to interfaces and delegates wrapping reference types.
- **Follow-up Questions**: Give an example of a covariant interface. (Answer: `IEnumerable<out T>`, which allows assigning `IEnumerable<string>` to `IEnumerable<object>`).
- **Interviewer's Expectations**: Explain `in`/`out` generic parameters.\n\n

#### 61. What are Source Generators in C# and how do they differ from reflection?
- **Detailed Answer**: Source Generators (introduced in .NET 5) are a compiler feature that allows developers to inspect user code and generate additional C# source files on-the-fly during compilation. This generated code is added to the compilation context. In contrast to reflection, which inspects metadata at runtime and incurs significant CPU and memory overhead, Source Generators move code generation to compile-time. This enables ahead-of-time (AOT) compilation optimization, zero runtime overhead, and better linker trimming.
- **Follow-up Questions**: How do you debug a source generator? (Answer: By using `Debugger.Launch()` inside the generator or using generator driver unit tests).
- **Interviewer's Expectations**: Highlight compile-time code generation, AOT compilation benefits, and zero runtime performance cost.

#### 62. How does ArrayPool<T> optimize memory allocation in high-performance applications?
- **Detailed Answer**: `ArrayPool<T>` is a high-performance buffer pool for reusing array allocations. Instead of allocating a new array on the managed heap (which triggers Garbage Collection pressure, especially on the Large Object Heap if the array is >= 85KB), you rent an array from the pool: `var array = ArrayPool<byte>.Shared.Rent(minimumLength);`. Once done, you return it: `ArrayPool<byte>.Shared.Return(array);`. This eliminates allocation cycles and reduces memory fragmentation.
- **Follow-up Questions**: What is a risk when returning arrays to the pool? (Answer: If you forget to clear the array or hold a reference to it after returning, it can cause data leaks or concurrency bugs).
- **Interviewer's Expectations**: Describe the benefits of reusing heap buffers and reducing GC overhead.

#### 63. Explain the difference between System.Threading.Lock (C# 13) and traditional object locking.
- **Detailed Answer**: Prior to C# 13, locking was performed on any reference object (`lock (someObj)`), which compiles to `Monitor.Enter` and `Monitor.Exit`. This requires the CLR to allocate a sync block index dynamically in the object header. C# 13 introduces `System.Threading.Lock`, a dedicated class that provides a cleaner, highly-optimized locking mechanism. When using `lock (myLock)` where `myLock` is an instance of `System.Threading.Lock`, the compiler generates calls to the lock's `EnterScope()` method, utilizing a lightweight ref struct scope that is faster and avoids sync block allocation overhead.
- **Follow-up Questions**: Does `System.Threading.Lock` support reentrancy? (Answer: Yes, it supports reentrant locking by the same thread).
- **Interviewer's Expectations**: Show understanding of object sync block headers vs dedicated Lock scopes.

#### 64. How do you implement custom validation using IValidateOptions in .NET Configuration?
- **Detailed Answer**: `IValidateOptions<TOptions>` allows you to enforce validation rules on configuration objects during application startup. You implement the interface and define the `Validate` method:
  ```csharp
  public class ConfigureMySettings : IValidateOptions<MySettings> {
      public ValidateOptionsResult Validate(string name, MySettings options) {
          if (options.Port <= 0) return ValidateOptionsResult.Fail("Port must be positive.");
          return ValidateOptionsResult.Success;
      }
  }
  ```
  This is registered in the DI container using `builder.Services.ConfigureOptions<ConfigureMySettings>();`. You can then call `ValidateOnStart()` to crash the application early if config is invalid.
- **Follow-up Questions**: How does this differ from Data Annotations validation? (Answer: Data Annotations use attributes; `IValidateOptions` allows complex, multi-property, and database-driven validation logic).
- **Interviewer's Expectations**: Demonstrate configuring application startup safety checks.

#### 65. Explain the internals of Dynamic Method Dispatch and virtual method table (vtable) slots in the CLR.
- **Detailed Answer**: When a class defines virtual methods, the compiler creates a Method Table for that type in the CLR metadata. Each virtual method has a dedicated slot in the vtable. When a subclass overrides a virtual method, its vtable slot points to the subclass implementation; if it does not, it points to the base class implementation. During invocation, the CPU executes an indirect call: it resolves the object pointer on the heap, reads the Method Table pointer, offsets to the vtable slot index, and jumps to the address. This adds pointer indirection overhead and prevents inline compiler optimizations.
- **Follow-up Questions**: How does devirtualization optimize this? (Answer: If the compiler can prove the concrete type at compile-time, it bypasses the vtable and performs a direct function call).
- **Interviewer's Expectations**: Explain pointer indirection, Method Tables, and vtable slots.

#### 66. What are primary constructors in C# 12 and how do they differ between classes and structs?
- **Detailed Answer**: C# 12 introduced primary constructors, allowing you to declare parameters directly on the class or struct definition line: `public class UserService(IDatabase db) { ... }`. For classes, primary constructor parameters are not automatically exposed as properties; they are only in scope within the class body. For records, primary constructor parameters automatically generate public, init-only properties.
- **Follow-up Questions**: Can you define multiple constructors when using a primary constructor? (Answer: Yes, but all other constructors must call the primary constructor using `this(...)`).
- **Interviewer's Expectations**: Explain the syntax simplification and the scoping differences between classes, structs, and records.

#### 67. Explain how the CLR handles JIT compilation tiers.
- **Detailed Answer**: Tiered Compilation (enabled by default in modern .NET) allows the JIT compiler to balance application startup time and runtime performance.
  - **Tier 0**: Compiles methods quickly with little or no optimization, ensuring fast startup.
  - **Tier 1**: If a method is called frequently (determined by internal CLR call counters), it is queued for re-compilation on a background thread with full optimizations (loop unrolling, devirtualization, inlining).
- **Follow-up Questions**: Can you disable tiered compilation? (Answer: Yes, using the environment variable `DOTNET_TieredCompilation=0`).
- **Interviewer's Expectations**: Describe startup speed vs steady-state performance optimizations.

---

## 10. Common Mistakes
- **throw ex;**: Erases original stack trace. Use `throw;` instead.
- **Async Void**: Except for event handlers, never use `async void` because exceptions cannot be caught. Use `async Task`.
- **LOH Fragmentation**: Allocating large arrays repeatedly. Use `ArrayPool<T>` to rent and return buffers.
- **Using LINQ on DbContext incorrectly**: Performing `.ToList()` before `.Where()`, which pulls the entire table into memory instead of translating to SQL.
- **Ignoring IDisposable**: Leaving database connections or file streams open.

---

## 11. Comparison Section: C# vs Java vs C++

| Feature | C# | Java | C++ |
|---|---|---|---|
| **Compilation** | JIT/AOT to Native | JIT/AOT to Native | Direct Machine Code |
| **Memory Management** | Automatic Generational GC | Automatic Generational GC | Manual / RAII / Smart Pointers |
| **Value Types** | Yes (`struct`) | Only primitive types | Yes (All objects are value types by default) |
| **Pointers / Direct Access** | Yes (inside `unsafe` blocks) | No | Yes (Default behavior) |
| **Properties** | Built-in syntax | Requires getter/setter boilerplates | Manual implementations |

---

## 12. Practical Project Ideas
- **Beginner**: A command-line JSON analyzer using `StreamReader` and basic string operations.
- **Intermediate**: A task scheduler API using ASP.NET Core, EF Core, SQLite, and custom background workers.
- **Advanced**: A high-frequency stock trading simulator with Redis, using `Channels`, `Span<char>` parsing, and allocation-free serialization pipelines.

---

## 13. Internship Preparation Notes
- **Focus Areas**: Reference vs value types, basic OOP, inheritance, and `async`/`await` tasks.
- **Key Checks**: Explain the difference between stack and heap memory, write basic LINQ queries, and explain how GC reclaims objects.
- **Practical Check**: Write a class implementing `IDisposable` and explain its destructor.

---

## 14. Cheat Sheet
- **Read-only Memory slice**: `ReadOnlySpan<char> span = text.AsSpan();`
- **Clean resource release**:
  ```csharp
  using var stream = new FileStream("path", FileMode.Open);
  ```
- **Thread-safe value increment**: `Interlocked.Increment(ref counter);`
- **Query performance optimization**: `_context.Users.AsNoTracking();`

---

## 15. One-Day Revision Guide
- [ ] Differentiate stack vs heap memory allocations.
- [ ] Differentiate Class vs Struct.
- [ ] Explain GC generations and promotional paths.
- [ ] Write a thread-safe singleton using `Lazy<T>`.
- [ ] Explain why `.ConfigureAwait(false)` prevents UI deadlocks.
- [ ] Differentiate Boxing and Unboxing performance profiles.
- [ ] Contrast `using` block vs garbage collection timelines.
