# 4. C & C++ Programming

## 1. Introduction
### What it is
C is a statically typed, procedural programming language developed in 1972 by Dennis Ritchie at Bell Labs. It provides low-level memory access, direct mapping to hardware instructions, and compiles down to native machine code. C++ was created by Bjarne Stroustrup in 1985 as an extension of C, introducing Object-Oriented Programming (OOP) paradigms, generic templates, type safety, and the Resource Acquisition Is Initialization (RAII) pattern to manage resource lifecycles automatically.

### Why it exists
High-level programming languages (such as Python, Java, or C#) isolate developer code from direct hardware layers using runtime interpreters or virtual machines, which introduces significant runtime latency, non-deterministic Garbage Collection pauses, and memory footprint overhead. C and C++ exist to bypass these abstractions. They give developers absolute control over the target CPU instructions, memory registers, cache alignments, and physical hardware interfaces, enabling maximum possible performance and optimization.

### Problems it solves
- **Execution Overhead**: Eliminates runtime interpreters or virtual machine translations, compiling directly into hardware-specific machine instructions.
- **Resource Constraints**: Allows programs to run inside microcontrollers and embedded devices with minimal RAM (kilobytes) and low clock speeds.
- **Non-Deterministic Pauses**: Replaces automatic garbage collectors with precise, developer-managed memory lifetimes, ensuring real-time response consistency.
- **Hardware Integration**: Provides raw memory pointer manipulation and inline assembly to interact directly with hardware registers and memory-mapped I/O devices.

### Industry Use Cases
- **Operating Systems**: The Linux Kernel is written in C; the Microsoft Windows Kernel is written in a hybrid of C and C++.
- **Game Engine Architecture**: Game engines like Unreal Engine utilize C++ to build graphics pipelines and physics calculations running at high frame rates.
- **Embedded Systems & IoT**: Firmware for automotive ECUs, aerospace guidance systems, and medical devices.
- **High-Frequency Trading (HFT)**: Ultra-low latency execution engines where microseconds determine financial outcomes.
- **Database Internals**: Engines like MySQL, PostgreSQL, and SQLite are written in C/C++ to optimize storage I/O and cache speeds.

### Analogy
If high-level languages are like commercial airlines where you sit back and let the autopilot and crew manage the flight paths, C and C++ are like flying a military fighter jet: you have direct control over every engine valve, wing flap, and fuel nozzle. It offers unmatched speed and maneuverability, but the slightest mistake can cause an unrecoverable system crash.

---

## 2. Core Concepts

### Beginner Concepts
- **Pointers**: Variables that store the physical memory address of another variable. Declared using `*` (e.g., `int* ptr`), they allow indirect access and modification of memory.
- **References**: Bound aliases to existing variables, declared using `&` (e.g., `int& ref = x`). Unlike pointers, they cannot be null, must be initialized upon declaration, and cannot be reassigned to refer to another variable.
- **Stack Allocation**: Automatic, fast memory allocation managed by the CPU call stack. Local variables are pushed to the stack when a function is entered and popped off when the function exits scope.
- **Heap Allocation**: Dynamic, manual memory allocation. Managed using `malloc`/`free` in C or `new`/`delete` in C++, heap objects persist across scope boundaries until explicitly deallocated.
- **Function Call Stack Frames**: The memory structure pushed onto the stack containing a function's parameters, local variables, and return address.

### Intermediate Concepts
- **RAII (Resource Acquisition Is Initialization)**: A core C++ design pattern where resource acquisition (memory, file handles, sockets, locks) is tied to object lifetime. The constructor acquires the resource, and the destructor releases it automatically when the object goes out of scope.
- **Smart Pointers (Modern C++)**:
  - `std::unique_ptr`: Enforces single, exclusive ownership of a heap resource. It cannot be copied, only moved.
  - `std::shared_ptr`: Implements reference-counted ownership. Multiple pointers can share the resource, which is freed when the count drops to zero.
  - `std::weak_ptr`: A non-owning observer of a `shared_ptr` resource, preventing cyclic reference memory leaks.
- **The Standard Template Library (STL)**: A library of container classes (e.g., `std::vector`, `std::map`), algorithms (e.g., `std::sort`), and iterators that abstract data manipulation.
- **Virtual Functions & Polymorphism**: Mechanism allowing derived classes to override base class behaviors. Resolved at runtime using a virtual table (vtable).

### Advanced Concepts
- **Move Semantics & Rvalues**: Introduced in C++11 to eliminate expensive deep copies. Rvalue references (`&&`) allow taking ownership of temporary objects' resources (e.g., stealing pointer arrays) using `std::move`.
- **Template Metaprogramming (TMP)**: Writing code templates that execute at compile-time, generating optimized type-specific instructions and executing checks before runtime.
- **Undefined Behavior (UB)**: Code constructs for which the C/C++ language standards impose no requirements, allowing the compiler to optimize under the assumption that they never occur (e.g., null pointer dereferencing, buffer overflows, signed integer wrapping).
- **Custom Memory Allocators**: Overriding standard `new`/`delete` operators or implementing custom Arena and Pool allocators to bypass OS allocation latencies.
- **Volatile and Strict Aliasing**: Rules regarding compiler optimizations. `volatile` prevents the compiler from optimizing away reads/writes, while strict aliasing governs pointer type conversions.

---

## 3. Internal Working

### Memory Layout, Compilation Stages, and Allocator Internals
A C/C++ program goes through a multi-stage compilation pipeline to transform human-readable code into an executable file:

```text
+-----------------------+
|    C++ Source (.cpp)  |
+-----------------------+
            | (Preprocessor: Resolves macros, expands #include)
            v
+-----------------------+
|  Expanded Source      |
+-----------------------+
            | (Compiler: Parses syntax, performs optimizations)
            v
+-----------------------+
|  Assembly Code (.s)   |
+-----------------------+
            | (Assembler: Translates instructions to binary)
            v
+-----------------------+
|   Object File (.o)    |
+-----------------------+
            | (Linker: Resolves symbols, merges static libraries)
            v
+-----------------------+
|  Native Executable    |
+-----------------------+
```

When the OS executes this binary, it maps the executable's virtual address space into the physical RAM, layout out memory segments as follows:

```text
+------------------------+ High Address (Kernel Space Mapping)
|      Stack Segment     | (Grows downwards, stores function local frames)
|           |            |
|           v            |
+------------------------+
|           ^            |
|           |            |
|      Heap Segment      | (Grows upwards, dynamic allocations via new/malloc)
+------------------------+
|      BSS Segment       | (Stores uninitialized global and static variables)
+------------------------+
|      Data Segment      | (Stores initialized global and static variables)
+------------------------+
|      Text Segment      | (Compiled read-only machine instructions)
+------------------------+ Low Address
```

#### Dynamic Allocator Internals (e.g., glibc ptmalloc)
When calling `malloc(size)` or `new`:
1. The memory allocator tries to satisfy the request from thread-local memory caches (e.g., thread-local arenas) to avoid lock contention.
2. It categorizes allocation requests by size into "bins" (e.g., fastbins, unsorted bins, small bins, large bins).
3. If no matching free block is found, it makes a system call: `brk()` to expand the heap data segment, or `mmap()` to allocate a separate virtual memory page for large requests ($\ge 128$ KB).
4. When `free()` is called, the block is returned to the bins and coalesced with neighboring free blocks to prevent memory fragmentation.

---

## 4. Important Terminology
- **Pointer**: A variable holding a virtual memory address.
- **Reference**: A compiler-enforced alias to an existing variable.
- **RAII**: Resource Acquisition Is Initialization, tying resource lifetime to stack object scopes.
- **Memory Leak**: Allocating heap memory and losing all pointers to it without deallocating.
- **Dangling Pointer**: A pointer that references a memory location that has already been deallocated.
- **Undefined Behavior (UB)**: Code constructs with no guaranteed execution path in the language standard.
- **vtable (Virtual Table)**: A table of function pointers generated by the compiler to resolve virtual method overrides at runtime.
- **RTTI (Run-Time Type Information)**: A mechanism to identify the type of an object at runtime (e.g., `dynamic_cast`).
- **Translation Unit**: The single source file after preprocessor expansions, ready for compiler parsing.
- **Strict Aliasing**: Rules preventing two pointers of different types from pointing to the same memory location, aiding optimizations.

---

## 5. Beginner Examples

### Example 1: Pointer Arithmetic and Array Traversal
```c
#include <stdio.h>

int main() {
    int arr[5] = {10, 20, 30, 40, 50};
    int *ptr = arr; // ptr points to arr[0] (address of 10)
    
    printf("Initial Value: %d\n", *ptr); // Output: 10
    
    // Increment pointer by 1 index block (moves 4 bytes forward for int)
    ptr++; 
    printf("Second Value: %d\n", *ptr); // Output: 20
    
    // Accessing elements using pointer offsets
    for (int i = 0; i < 3; i++) {
        printf("Offset %d: %d\n", i, *(arr + i)); 
    }
    return 0;
}
```

### Example 2: Passing Parameters in C++ (Value, Pointer, and Reference)
```cpp
#include <iostream>

// Pass by Value: Copies the argument, original variable remains unchanged
void modifyByValue(int val) {
    val = 100;
}

// Pass by Pointer: Receives address, dereferences to modify original variable
void modifyByPointer(int *ptr) {
    if (ptr) {
        *ptr = 200;
    }
}

// Pass by Reference: Receives alias, modifies original variable directly
void modifyByReference(int &ref) {
    ref = 300;
}

int main() {
    int number = 50;
    
    modifyByValue(number);
    std::cout << "After modifyByValue: " << number << std::endl; // Output: 50
    
    modifyByPointer(&number);
    std::cout << "After modifyByPointer: " << number << std::endl; // Output: 200
    
    modifyByReference(number);
    std::cout << "After modifyByReference: " << number << std::endl; // Output: 300
    
    return 0;
}
```

---

## 6. Intermediate Examples

### Example 1: Implementing a Thread-Safe RAII Mutex Lock
```cpp
#include <iostream>
#include <thread>
#include <mutex>
#include <vector>

class ThreadSafeCounter {
private:
    std::mutex mtx;
    int count = 0;
public:
    void increment() {
        // RAII Lock Guard: Acquires lock in constructor, releases in destructor
        std::lock_guard<std::mutex> lock(mtx);
        count++;
        // lock goes out of scope here; mutex is unlocked automatically
    }

    int getCount() {
        std::lock_guard<std::mutex> lock(mtx);
        return count;
    }
};

void runWorker(ThreadSafeCounter &counter) {
    for (int i = 0; i < 1000; ++i) {
        counter.increment();
    }
}

int main() {
    ThreadSafeCounter counter;
    std::thread t1(runWorker, std::ref(counter));
    std::thread t2(runWorker, std::ref(counter));
    
    t1.join();
    t2.join();
    
    std::cout << "Final Count: " << counter.getCount() << std::endl; // Output: 2000
    return 0;
}
```

### Example 2: Implementing a Custom Vector Class with RAII
```cpp
#include <iostream>
#include <algorithm>
#include <stdexcept>

template <typename T>
class MyVector {
private:
    T* data;
    size_t capacity;
    size_t length;

    void resize() {
        capacity = capacity == 0 ? 1 : capacity * 2;
        T* newData = new T[capacity];
        for (size_t i = 0; i < length; ++i) {
            newData[i] = std::move(data[i]);
        }
        delete[] data;
        data = newData;
    }

public:
    MyVector() : data(nullptr), capacity(0), length(0) {}

    // Destructor: Automatically releases heap allocation (RAII)
    ~MyVector() {
        delete[] data;
    }

    // Copy Constructor: Implements Deep Copy
    MyVector(const MyVector& other) : capacity(other.capacity), length(other.length) {
        data = new T[capacity];
        std::copy(other.data, other.data + other.length, data);
    }

    // Move Constructor: Implements Shallow Copy & Pointer Stealing
    MyVector(MyVector&& other) noexcept 
        : data(other.data), capacity(other.capacity), length(other.length) {
        other.data = nullptr;
        other.capacity = 0;
        other.length = 0;
    }

    void push_back(const T& value) {
        if (length == capacity) {
            resize();
        }
        data[length++] = value;
    }

    T& operator[](size_t index) {
        if (index >= length) throw std::out_of_range("Index out of bounds");
        return data[index];
    }

    size_t size() const { return length; }
};
```

---

## 7. Advanced Concepts

### Template Metaprogramming and SFINAE (Substitution Failure Is Not An Error)
Template Metaprogramming allows compile-time logic processing. SFINAE is used to enable or disable function overrides based on type properties evaluated by the compiler:

```cpp
#include <iostream>
#include <type_traits>

// Enable this function only for integral types (int, long, char)
template <typename T>
typename std::enable_if<std::is_integral<T>::value, void>::type
processValue(T val) {
    std::cout << "Processing Integral Type: " << val << std::endl;
}

// Enable this function only for floating-point types (float, double)
template <typename T>
typename std::enable_if<std::is_floating_point<T>::value, void>::type
processValue(T val) {
    std::cout << "Processing Floating-Point Type: " << val << std::endl;
}

int main() {
    processValue(42);       // Resolves to integral overload
    processValue(3.14159);  // Resolves to floating-point overload
    // processValue("hello"); // Compile-time Error: SFINAE template substitution fails
    return 0;
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for deep understanding of CPU-memory mapping and memory safety. They evaluate your ability to avoid Undefined Behavior, write exception-safe RAII structures, and debug low-level hardware issues.

### Red Flags
- returning raw references/pointers to variables defined on the local stack.
- Deallocating memory with `free` when it was allocated with `new`, or vice versa.
- Neglecting constructor Rule of Five (Destructor, Copy Constructor, Copy Assignment, Move Constructor, Move Assignment) when classes manage raw pointer allocations.
- Believing smart pointers solve concurrency races (they prevent leaks, not data races).

### Green Flags
- Writing code marked with `const` correctness on read-only methods and parameters.
- Using `std::make_unique` and `std::make_shared` over raw `new` operators.
- Marking move constructors with the `noexcept` keyword so STL containers can utilize fast moves safely.

### Answers Matrix
| Level | Question: "What is the difference between a pointer and a reference?" |
|---|---|
| **Rejected** | "They are basically the same but reference is modern syntax." |
| **Shortlisted** | "Pointers store memory addresses and can be NULL. References are aliases to existing variables and cannot be NULL." |
| **Selected** | "A pointer is a distinct object in memory that stores a virtual memory address. It can be set to null, reassigned, and manipulated via pointer arithmetic. A reference is a compiler-enforced alias. It has no identity separate from the object it binds to, must be initialized on creation, cannot be null, cannot be reassigned, and doesn't require explicit dereferencing operators." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the difference between stack and heap memory allocation.
- **Detailed Answer**: Stack allocation is handled automatically by the CPU. When a function is called, a stack frame is pushed, storing parameters and local variables. Stack allocations are sequential, have O(1) complexity, are extremely fast, and automatically clean up when leaving scope. Heap allocation is manual, handled by system libraries and the OS. Memory is requested dynamically via `malloc` or `new`. It is slower because the allocator must search for free memory blocks, requires explicit deallocation, and is prone to memory fragmentation.
- **Follow-up Questions**: What is a stack overflow? (Answer: Exhaustion of stack memory, typically caused by infinite recursion or allocating huge arrays on the stack).
- **Interviewer's Expectations**: Contrast automatic scope cleanup with manual lifetimes, and highlight performance profiles.

#### 2. What is RAII, and how does it guarantee resource safety?
- **Detailed Answer**: Resource Acquisition Is Initialization (RAII) is a C++ paradigm that ties resource management to the lifespan of stack-allocated objects. The resource (such as a database connection, mutex lock, or heap memory) is acquired in the class constructor. When the object goes out of scope, the compiler automatically triggers its destructor, which releases the resource. This ensures resources are cleaned up even if exceptions occur, avoiding leaks.
- **Follow-up Questions**: How does RAII react during stack unwinding? (Answer: During exception propagation, all local stack objects constructed up to that point have their destructors executed automatically, freeing resources).
- **Interviewer's Expectations**: Describe the constructor-destructor relationship and reference exception safety.

#### 3. Explain the difference between unique_ptr, shared_ptr, and weak_ptr.
- **Detailed Answer**:
  - `std::unique_ptr` represents exclusive ownership of a heap resource. It cannot be copied, only moved. The resource is destroyed when the unique_ptr goes out of scope.
  - `std::shared_ptr` represents shared ownership. It uses a control block containing a reference count. When a shared_ptr is copied, the count increases. The resource is deleted only when the last shared_ptr is destroyed.
  - `std::weak_ptr` is a non-owning observer. It references an object managed by shared_ptr but does not increment the reference count. It prevents cyclic reference leaks.
- **Follow-up Questions**: What is the overhead of a `shared_ptr`? (Answer: Atomic operations to increment/decrement reference counts, plus an extra heap allocation for the control block unless `std::make_shared` is used).
- **Interviewer's Expectations**: Explain ownership models, copy capability, and the reference counting control block.

#### 4. Why must base class destructors be declared as virtual?
- **Detailed Answer**: If a base class destructor is not marked as `virtual`, deleting a derived class object through a base class pointer results in Undefined Behavior. In practice, the compiler will only invoke the base class destructor, failing to call the derived class destructor and leaking any resources managed exclusively by the derived class. Declaring it `virtual` ensures the derived destructor runs first, followed by the base class destructor.
- **Follow-up Questions**: When should you *not* declare a virtual destructor? (Answer: When a class is not intended to be inherited, as adding virtual functions introduces a vtable pointer (vptr) which increases the object's memory size).
- **Interviewer's Expectations**: Detail object destruction sequence and vtable dispatching.

#### 5. What are rvalue references (&&) and move semantics?
- **Detailed Answer**: An rvalue reference (`&&`) binds to temporary objects (rvalues) that are about to be destroyed. Move semantics allow C++ to transfer ownership of resources (e.g. heap pointers) from a temporary object directly to a new object, instead of performing an expensive deep copy. The temporary object's pointers are set to null, allowing it to be destroyed safely.
- **Follow-up Questions**: What is the difference between `std::move` and actual moving? (Answer: `std::move` does not move anything; it performs a static cast of an lvalue to an rvalue reference to enable the compiler to select the move constructor).
- **Interviewer's Expectations**: Contrast deep copy costs with shallow pointer swapping.

#### 6. What is the difference between malloc/free and new/delete?
- **Detailed Answer**:
  - `malloc` and `free` are standard C library functions. They allocate raw byte chunks from the heap but do not execute class constructors or destructors. They return a `void*` and require manual type casting.
  - `new` and `delete` are C++ operators. `new` allocates memory, executes object constructors, and returns a type-safe pointer. `delete` runs object destructors before deallocating memory.
- **Follow-up Questions**: Can you call `free` on a pointer allocated with `new`? (Answer: No, mixing allocation types causes undefined behavior).
- **Interviewer's Expectations**: Distinguish constructor execution and type safety.

#### 7. How does dynamic dispatch work via vtables in C++?
- **Detailed Answer**: Dynamic dispatch is the mechanism used to resolve virtual function calls at runtime. If a class declares a virtual function, the compiler inserts a virtual table pointer (`vptr`) into the object's layout. This `vptr` points to a static table (vtable) generated for that class, which contains function pointers pointing to the class's method implementations. When calling a virtual function, the runtime dereferences the `vptr`, looks up the function pointer in the vtable, and jumps to the resolved implementation.
- **Follow-up Questions**: What is the cost of virtual functions? (Answer: Cache miss overhead from double dereferencing, and the inability of compilers to inline virtual functions).
- **Interviewer's Expectations**: Explain `vptr` injection and runtime lookup steps.

#### 8. What is object slicing in C++?
- **Detailed Answer**: Object slicing occurs when a derived class object is assigned by value to a base class object. Because the base class object only has enough memory layout to store base data members, the derived class's additional variables and virtual overrides are sliced away.
- **Follow-up Questions**: How do you prevent object slicing? (Answer: Pass objects by reference or pointer instead of value).
- **Interviewer's Expectations**: Identify value assignment limits and dynamic casting alternatives.

#### 9. What is const-correctness?
- **Detailed Answer**: Const-correctness is the practice of using the `const` keyword to prevent variables and class properties from being mutated. It includes declaring const variables, passing parameters by const reference (`const T&`), and marking member functions as `const` to guarantee they do not modify the object's internal state.
- **Follow-up Questions**: How do you modify a member variable inside a const member function? (Answer: Declare the member variable as `mutable`).
- **Interviewer's Expectations**: Explain read-only guarantees and parameter passing constraints.

#### 10. Explain template instantiation and compilation.
- **Detailed Answer**: Templates in C++ are blueprints, not compilable code. When a template is used (e.g. `std::vector<int>`), the compiler performs template instantiation, generating actual class or function code for that specific type at compile-time. Because of this, template definitions are usually kept in header files rather than compiled source files.
- **Follow-up Questions**: What is template specialization? (Answer: Providing a custom implementation of a template for a specific type to optimize performance or handle special behaviors).
- **Interviewer's Expectations**: Detail compile-time code generation and header-only compiler requirements.

#### 11. Explain Undefined Behavior (UB) and give three examples.
- **Detailed Answer**: Undefined Behavior is code execution for which the C++ standard defines no behavior. The compiler assumes the developer will not write UB, and uses this assumption to optimize code. If UB occurs, the program can crash, produce corrupted data, or execute arbitrary pathways. Examples include dereferencing a null pointer, index out-of-bounds array access, and signed integer overflow.
- **Follow-up Questions**: How does signed integer overflow differ from unsigned integer overflow? (Answer: Unsigned overflow is defined to wrap modulo $2^n$. Signed overflow is undefined behavior).
- **Interviewer's Expectations**: Define UB and explain how the compiler exploits it for optimizations.

#### 12. Explain the Rule of Three, Five, and Zero.
- **Detailed Answer**:
  - **Rule of Three**: If a class manages raw resources and defines a destructor, copy constructor, or copy assignment operator, it must define all three to manage deep copies.
  - **Rule of Five**: Adds move constructor and move assignment operator to optimize temporary resource transfers.
  - **Rule of Zero**: Write classes that delegate resource management to STL containers or smart pointers, requiring no custom copy/move constructors or destructors.
- **Follow-up Questions**: What happens if you violate the Rule of Three? (Answer: Default shallow copies copy raw pointers, leading to double-free crashes when objects exit scope).
- **Interviewer's Expectations**: Contrast deep copy management with resource wrapper delegation.

#### 13. What is the difference between static_cast, dynamic_cast, const_cast, and reinterpret_cast?
- **Detailed Answer**:
  - `static_cast`: Performs compile-time type conversions (e.g., int to float, or up/down casting in hierarchies without runtime checks).
  - `dynamic_cast`: Performs runtime checked downcasts in polymorphic hierarchies. Returns `nullptr` or throws on failure. Requires RTTI.
  - `const_cast`: Adds or removes `const` volatile qualifiers from variables.
  - `reinterpret_cast`: Performs low-level, binary reinterpretation of pointers (unsafe, platform-dependent).
- **Follow-up Questions**: Which cast is slowest? (Answer: `dynamic_cast`, due to runtime traversal of the inheritance hierarchy).
- **Interviewer's Expectations**: Differentiate cast enforcement levels and performance costs.

### Scenario-Based Questions

#### 14. Implement a thread-safe singleton pattern in C++11 (Magic Statics).
- **Detailed Answer**: C++11 guarantees that local static variables are initialized in a thread-safe manner, making singleton implementation clean:
  ```cpp
  class Singleton {
  public:
      static Singleton& getInstance() {
          static Singleton instance; // Thread-safe initialization
          return instance;
      }
      Singleton(const Singleton&) = delete;
      void operator=(const Singleton&) = delete;
  private:
      Singleton() {}
  };
  ```
- **Follow-up Questions**: Why delete copy and assignment? (Answer: To prevent copying or duplicating the single instance).
- **Interviewer's Expectations**: Show static block initialization thread safety.

#### 15. Design a custom Arena Allocator for latency-critical processing.
- **Detailed Answer**: An Arena Allocator pre-allocates a contiguous block of memory and satisfies allocations by incrementing an offset pointer:
  ```cpp
  class Arena {
  private:
      char* buffer;
      size_t size;
      size_t offset;
  public:
      Arena(size_t s) : size(s), offset(0) { buffer = new char[s]; }
      ~Arena() { delete[] buffer; }
      void* allocate(size_t bytes) {
          if (offset + bytes > size) throw std::bad_alloc();
          void* ptr = &buffer[offset];
          offset += bytes;
          return ptr;
      }
      void reset() { offset = 0; } // Instant reclaim
  };
  ```
- **Follow-up Questions**: How does this handle individual deallocations? (Answer: It does not; all objects are deallocated at once when the arena is reset).
- **Interviewer's Expectations**: Implement pointer arithmetic offset updates.

#### 16. You have a memory leak in a large C++ application. How do you find it?
- **Detailed Answer**: Compile the binary with debug symbols enabled (`-g`) and run it under **Valgrind**'s Memcheck tool: `valgrind --leak-check=full ./my_app`. Alternatively, compile with **AddressSanitizer** enabled via compiler flags: `-fsanitize=address`. These tools track allocations and report the exact stack trace of unfreed memory blocks.
- **Follow-up Questions**: Can smart pointers still leak? (Answer: Yes, when circular references are created using `std::shared_ptr`).
- **Interviewer's Expectations**: Mention AddressSanitizer and Valgrind workflows.

#### 17. How do you resolve a reference cycle when using shared_ptrs?
- **Detailed Answer**: Break the cycle by converting one of the shared references (usually the child pointer pointing back to the parent) into a `std::weak_ptr`. The weak reference does not increment the reference count, allowing the parent object to be destroyed when its outer reference is dropped.
- **Follow-up Questions**: How does weak_ptr check if the parent is alive? (Answer: Call `.lock()`, which returns an active `std::shared_ptr` if the object still exists).
- **Interviewer's Expectations**: Diagram cyclic references and demonstrate weak_ptr lock checking.

#### 18. How do you prevent memory leaks when working with legacy C APIs that return raw pointers?
- **Detailed Answer**: Wrap the raw pointer returned by the legacy API in a `std::unique_ptr` with a custom deleter. The custom deleter will automatically call the legacy API's cleanup function (e.g. `fclose` or `free_device`) when the smart pointer exits scope:
  ```cpp
  std::unique_ptr<FILE, int(*)(FILE*)> ptr(fopen("data.bin", "rb"), fclose);
  ```
- **Follow-up Questions**: Does using a custom deleter increase the size of `std::unique_ptr`? (Answer: Only if the deleter holds state; stateless function pointer wrappers maintain the same size as a raw pointer).
- **Interviewer's Expectations**: Recommend `std::unique_ptr` custom deleter bounds.

### Debugging Questions

#### 19. Debug the crash in the code below:
```cpp
class Widget {
public:
    Widget() { data = new int[10]; }
    ~Widget() { delete[] data; }
private:
    int *data;
};
void run() {
    Widget w1;
    Widget w2 = w1; // Crash occurs on scope exit
}
```
- **Detailed Answer**: The crash occurs because of a Rule of Three violation. The compiler generates a default copy constructor which performs a shallow copy of `w1`, setting `w2.data` to point to the same memory address as `w1.data`. When `w2` exits scope, its destructor deallocates the memory. When `w1` exits scope, its destructor tries to delete the same memory address, causing a **double free** crash.
- **Fix**: Implement a custom copy constructor (deep copy) or delete the copy operations.
- **Follow-up Questions**: What is a double free error? (Answer: An allocator security error caused by deleting the same memory block twice).
- **Interviewer's Expectations**: Spot raw pointer copy crashes.

#### 20. Debug this dangling reference:
```cpp
const std::string& getUsername() {
    std::string user = "admin";
    return user;
}
```
- **Detailed Answer**: The function returns a reference to the local variable `user`. Because `user` is allocated on the stack frame of `getUsername()`, it is destroyed when the function returns. The returned reference points to deallocated stack memory, causing undefined behavior when accessed.
- **Fix**: Return by value (`std::string`), letting the compiler use return value optimization (RVO).
- **Follow-up Questions**: What is Return Value Optimization? (Answer: A compiler optimization that constructs the return value directly in the caller's target variable, skipping copies).
- **Interviewer's Expectations**: Spot stack variable lifetimes.

#### 21. Why does the following template function fail to link?
```cpp
// math.h
template <typename T>
T add(T a, T b);

// math.cpp
#include "math.h"
template <typename T>
T add(T a, T b) { return a + b; }

// main.cpp
#include "math.h"
int main() { return add(5, 10); } // Linker Error: Unresolved symbol
```
- **Detailed Answer**: Templates are instantiated at compile-time. When compiling `main.cpp`, the compiler sees the declaration of `add<int>` but not its implementation, so it leaves a placeholder for the linker. When compiling `math.cpp`, the compiler does not see `add` being called with `int`, so it doesn't generate the machine code for `add<int>`. The linker fails because the instantiated symbol is missing.
- **Fix**: Put the template implementation directly in the header file `math.h`.
- **Follow-up Questions**: How can you keep implementations in `.cpp` files? (Answer: By explicitly instantiating the template in `math.cpp` for the expected types, e.g. `template int add<int>(int, int);`).
- **Interviewer's Expectations**: Explain compile-time template code generation limits.

#### 22. Fix this concurrency race condition:
```cpp
int counter = 0;
void increment() {
    for (int i = 0; i < 100000; ++i) {
        counter++;
    }
}
```
- **Detailed Answer**: The operation `counter++` is not atomic; it consists of three instructions: read memory, increment register, write memory. When multiple threads call `increment` concurrently, they overwrite each other's changes.
- **Fix**: Use `std::atomic<int>` for the counter, or protect the critical section with `std::lock_guard` and `std::mutex`.
- **Follow-up Questions**: What is lock-free programming? (Answer: Programming that utilizes atomic hardware instructions to modify shared state without using blocking locks).
- **Interviewer's Expectations**: Identify read-modify-write concurrency risks.

#### 23. Debug this out-of-bounds pointer increment:
```cpp
void clearArray(int *arr, size_t size) {
    for (size_t i = 0; i <= size; ++i) {
        arr[i] = 0; // Buffer overflow
    }
}
```
- **Detailed Answer**: The loop condition `i <= size` causes the loop to run `size + 1` times. On the final iteration, it accesses `arr[size]`, which is one element past the end of the array, corrupting memory.
- **Fix**: Change the loop condition to `i < size`.
- **Follow-up Questions**: How do you avoid raw array indexing issues in modern C++? (Answer: Use `std::array` or `std::vector` and use iterators, range-based for loops, or `.at()` for bounds-checked access).
- **Interviewer's Expectations**: Spot off-by-one bounds check errors.\n\n#### 24. Explain the difference between std::map and std::unordered_map in C++.
- **Detailed Answer**: `std::map` is implemented as a self-balancing binary search tree (typically a Red-Black Tree). Keys are stored in sorted order. Search, insertion, and deletion operations have logarithmic complexity ($O(\log n)$). `std::unordered_map` is implemented using a hash table. Keys are not stored in any sorted order. Average time complexity for lookup, insertion, and deletion is constant ($O(1)$), though worst-case is linear ($O(n)$) if many hash collisions occur.
- **Follow-up Questions**: When would you choose `std::map` over `std::unordered_map`? (Answer: When you need elements sorted, need to perform range queries, or require guaranteed $O(\log n)$ worst-case performance limits).
- **Interviewer's Expectations**: Highlight underlying data structures, order guarantees, and time complexities.

#### 25. What is the static keyword in C/C++?
- **Detailed Answer**: The `static` keyword has different meanings depending on context:
  - **Local Static Variable**: Stored in the data segment, initialized only once, and retains its value between function calls.
  - **Global Static Variable/Function**: Scopes the visibility of the variable/function to the translation unit (.cpp file) in which it is declared, preventing naming collisions.
  - **Static Class Member**: Shared by all instances of the class. Static methods can be called without instantiating the class and can only access static members.
- **Follow-up Questions**: Where are static variables stored in memory? (Answer: In the Data segment if initialized, or the BSS segment if uninitialized).
- **Interviewer's Expectations**: Distinguish local, global, and class scopes.

#### 26. How do you implement dynamic casting without dynamic_cast or RTTI?
- **Detailed Answer**: To implement dynamic casting without standard compiler RTTI, you must manually implement a type tagging system. Add a virtual method like `getType()` or `isType(Type t)` to the base class, and implement overrides in derived classes returning enum tags. The client queries the tag and performs a `static_cast` if the tag matches.
- **Follow-up Questions**: What is a downside of this manual approach? (Answer: Tight coupling, as the base class must know about the enum tags of all derived types, violating the Open-Closed Principle).
- **Interviewer's Expectations**: Propose enum type tags combined with static casts.

#### 27. Explain the volatile keyword and its usage in embedded systems.
- **Detailed Answer**: The `volatile` keyword tells the compiler that a variable can be modified by hardware or external threads outside the program's control. It prevents the compiler from optimizing away reads or writes to the variable, forcing it to reload the value from memory every time it is accessed. It is used for memory-mapped I/O registers, interrupt service routine flags, and global variables shared across threads.
- **Follow-up Questions**: Does `volatile` guarantee thread safety? (Answer: No, it only prevents compiler optimizations. It does not provide atomic operations or memory barriers).
- **Interviewer's Expectations**: Emphasize hardware registers and explain that it does not provide concurrency safety.

#### 28. What is strict aliasing, and how can violating it lead to compiler optimization issues?
- **Detailed Answer**: Strict aliasing is a compiler rule stating that two pointers of different types cannot point to the same memory location, with exceptions like `char*`. The compiler assumes that modifying data through one pointer type will not affect data accessed through another pointer type, enabling aggressive optimizations. Violating this rule (e.g. casting an `int*` to a `float*` and dereferencing) triggers undefined behavior, as the compiler may reorder or omit reads, leading to corrupted values.
- **Follow-up Questions**: How do you bypass strict aliasing safely? (Answer: Use `memcpy` or a union to copy bytes between types).
- **Interviewer's Expectations**: Detail pointer types assumptions and warning signs.

#### 29. Explain inline functions and their relation to macro expansions.
- **Detailed Answer**: Inline functions (`inline` keyword) are directives suggesting that the compiler replace the function call directly with the function's code block, eliminating function call overhead. Unlike macros, inline functions are type-safe, respect scope boundaries, evaluate arguments only once, and are processed by the compiler rather than the preprocessor.
- **Follow-up Questions**: Does the compiler always inline functions marked as `inline`? (Answer: No, it is only a suggestion. Compilers will ignore it for complex, recursive, or large functions).
- **Interviewer's Expectations**: Contrast type-safe compiler inlining with text-replacement macros.

#### 30. What is SFINAE, and how does it differ from concepts in C++20?
- **Detailed Answer**: SFINAE (Substitution Failure Is Not An Error) states that if a template substitution results in an invalid type or expression during overload resolution, the compiler discards that overload instead of throwing a compilation error. C++20 Concepts replace this by providing named compile-time constraints using the `requires` keyword, yielding clean compiler error messages.
- **Follow-up Questions**: Give a common use case of SFINAE. (Answer: Selecting different functions depending on whether a type has a specific method or is a pointer).
- **Interviewer's Expectations**: Explain overload resolution rules and contrast SFINAE with modern Concepts.

#### 31. How do you construct and use a placement new in C++?
- **Detailed Answer**: Placement `new` allows you to construct an object in a pre-allocated memory buffer instead of allocating new heap memory. It is called by passing the buffer address to the `new` operator: `new (buffer) MyClass()`. Since the memory is not allocated on the heap, you must not use `delete`. Instead, call the destructor explicitly: `ptr->~MyClass()`.
- **Follow-up Questions**: Why use placement new? (Answer: For custom allocators or real-time systems to avoid heap allocation latency and memory fragmentation).
- **Interviewer's Expectations**: Show buffer arguments, warn against `delete`, and show explicit destructor calls.

#### 32. What is the difference between static and dynamic linking?
- **Detailed Answer**: Static linking copies the binary code of all library dependencies directly into the final executable at compile-time. Dynamic linking resolves library references at runtime, loading shared library files (.so or .dll) into memory. Static binaries are larger and self-contained; dynamic binaries are smaller but require the shared libraries to be present on the target host.
- **Follow-up Questions**: What is DLL Hell? (Answer: Runtime crashes caused by incompatible versions of dynamic shared libraries installed on the host).
- **Interviewer's Expectations**: Contrast compile-time copying with runtime resolution.

#### 33. How does name mangling work in C++, and how do you prevent it using extern "C"?
- **Detailed Answer**: Name mangling is the process where the C++ compiler encodes function signatures (including namespaces and parameter types) into unique symbol names in the object binary, supporting function overloading. Because C does not support overloading, C compilers do not mangle names. Declaring `extern "C"` forces the C++ compiler to output clean C-style symbol names, allowing C++ code to link with C libraries.
- **Follow-up Questions**: Can you declare overloaded functions inside `extern "C"`? (Answer: No, because C does not support overloading and symbols will collide).
- **Interviewer's Expectations**: Explain symbol table differences and link resolutions.

#### 34. What is a memory barrier (fence) in multi-threaded C++?
- **Detailed Answer**: A memory barrier (or fence) is an instruction that prevents the CPU or compiler from reordering read and write instructions across the barrier. This ensures memory visibility guarantees when writing lock-free algorithms, preventing threads from reading stale or out-of-order data.
- **Follow-up Questions**: What are the common memory order models in C++? (Answer: `memory_order_seq_cst` (sequential consistency), `memory_order_acquire`, `memory_order_release`, and `memory_order_relaxed`).
- **Interviewer's Expectations**: Detail CPU reordering behaviors and instruction boundaries.

#### 35. Explain the difference between copy elision and move semantics.
- **Detailed Answer**: Copy elision is a compiler optimization where copy and move operations are skipped completely. The compiler constructs the return value directly in the target variable (e.g. Return Value Optimization). Move semantics is a language feature that swaps pointers of temporary objects when copy elision is not possible. Copy elision is preferred because it has zero cost.
- **Follow-up Questions**: Is copy elision guaranteed? (Answer: Since C++17, copy elision is guaranteed by the standard for return values of temporary objects, even if copy/move constructors are deleted).
- **Interviewer's Expectations**: Contrast compiler-driven omissions with language-level pointer swaps.

#### 36. What are the rules for alignment and padding in C structs?
- **Detailed Answer**: CPUs read memory in chunks (word sizes, e.g., 4 or 8 bytes). To optimize reads, variables must be aligned to memory addresses that are multiples of their size. The compiler inserts padding bytes inside structs to enforce this alignment. Struct size is padded to be a multiple of the largest member's size.
- **Follow-up Questions**: How do you minimize padding? (Answer: Reorder struct members from largest to smallest, or use compiler directives like `#pragma pack(1)`).
- **Interviewer's Expectations**: Detail memory address alignments and member ordering optimizations.

#### 37. What is placement new and when should it be used?
- **Detailed Answer**: Placement `new` is a version of the `new` operator that accepts a memory pointer as a parameter and constructs an object in that specific address. It is used in custom memory allocators (like Pool or Arena allocators) where memory is pre-allocated once, bypassing runtime allocator latency.
- **Follow-up Questions**: How do you release placement new objects? (Answer: Destructor must be invoked explicitly: `obj->~MyClass()`, then the memory buffer is reclaimed).
- **Interviewer's Expectations**: Point out memory offset allocations and explicit destructor requirements.

#### 38. Explain the difference between std::thread and std::async.
- **Detailed Answer**: `std::thread` is a low-level abstraction that maps directly to an OS thread. It requires manual joining or detaching and doesn't return value easily. `std::async` is a high-level task runner that returns a `std::future`. By default, it runs the task on a thread pool or defers execution lazily.
- **Follow-up Questions**: What happens if you don't store the return value of `std::async`? (Answer: The temporary future's destructor blocks execution, running the task synchronously).
- **Interviewer's Expectations**: Contrast thread mappings with task futures.

#### 39. What is a union, and how does it differ from a struct?
- **Detailed Answer**: A `struct` allocates separate memory locations for each member, so all members can be read concurrently. A `union` allocates a single memory segment shared by all members, and its size is equal to its largest member. Only one member of a union can be stored at a time.
- **Follow-up Questions**: What is a tagged union? (Answer: A struct containing a union alongside an enum member representing which union field is currently active).
- **Interviewer's Expectations**: Contrast shared memory allocations with separate member locations.

#### 40. Explain lock-free programming primitives (compare-and-swap).
- **Detailed Answer**: Lock-free programming utilizes atomic CPU instructions to update shared variables without using blocking locks (mutexes). The core primitive is **Compare-And-Swap (CAS)**. CAS compares the current variable value to an expected value; if they match, it updates the variable to a new value atomically. If they don't, it fails, and the loop retries.
- **Follow-up Questions**: What is the ABA problem? (Answer: A concurrency issue where a variable is changed from A to B and back to A, causing a CAS check to succeed even though the state changed).
- **Interviewer's Expectations**: Detail CPU-level atomic checks and retry loops.\n\n\n\n#### 41. What are pointer-to-member operators (.* and ->*) in C++?
- **Detailed Answer**: Pointer-to-member operators allow you to reference and invoke class member variables or functions indirectly. `.*` is used when operating directly on an object instance, while `->*` is used when operating on a pointer to an object instance. They are essential for callback systems and function-routing engines.
- **Follow-up Questions**: How do you declare a pointer to a member function? (Answer: `void (MyClass::*funcPtr)() = &MyClass::myMethod;`).
- **Interviewer's Expectations**: Show pointer-to-member syntax and explain indirect method invocation.

#### 42. Explain the difference between std::shared_ptr thread-safety and the thread-safety of the underlying object.
- **Detailed Answer**: `std::shared_ptr` provides thread-safety for its control block (incrementing/decrementing reference counts is atomic). However, the underlying object is not thread-safe. Multiple threads writing to the same object wrapped in `shared_ptr` concurrently will cause data races, requiring external synchronization locks.
- **Follow-up Questions**: What happens if you modify the `shared_ptr` pointer itself across threads concurrently? (Answer: It is a data race; you must use `std::atomic` overloads for shared_ptr).
- **Interviewer's Expectations**: Distinguish control block atomicity from object-level data safety.

#### 43. What is the difference between static and dynamic polymorphism?
- **Detailed Answer**: Static polymorphism resolves method calls at compile-time (using Templates and Function Overloading), avoiding runtime virtual table lookup overhead. Dynamic polymorphism resolves method calls at runtime (using Virtual Functions and Inheritance), which allows dynamic runtime behavior changes but introduces vtable lookup latency.
- **Follow-up Questions**: What is the CRTP pattern? (Answer: Curiously Recurring Template Pattern, a C++ idiom implementing static polymorphism using templates).
- **Interviewer's Expectations**: Contrast compile-time code generation with runtime vtable lookups.

#### 44. What are type traits and how do they work in template metaprogramming?
- **Detailed Answer**: Type traits are templates that provide information about types at compile-time (e.g. `std::is_integral<T>::value` or `std::is_pointer<T>::value`). They allow the compiler to query type properties and alter code generation dynamically.
- **Follow-up Questions**: How are type traits implemented? (Answer: Through template specialization, defining a base template returning false and specializations for specific types returning true).
- **Interviewer's Expectations**: Explain template specialization mechanics.

#### 45. Explain how the C++ compiler implements lambda closures.
- **Detailed Answer**: The compiler converts a lambda expression into a unique, unnamed functor struct. The capture list defines the struct's member variables (storing copies or references), the lambda parameters become arguments of the overloaded `operator()`, and the lambda body becomes the operator method body.
- **Follow-up Questions**: What is the size of a lambda that captures nothing? (Answer: 1 byte, equivalent to an empty struct in C++).
- **Interviewer's Expectations**: Describe functor struct translations and capture storage.

#### 46. What is the difference between const and constexpr in C++?
- **Detailed Answer**: `const` declares that a variable is read-only after initialization, but the initialization can happen at runtime. `constexpr` declares that a variable or function must be evaluated at compile-time, allowing it to be used where compile-time constants are required (like array sizes).
- **Follow-up Questions**: Can a `constexpr` function run at runtime? (Answer: Yes, if its parameters are not compile-time constants, it falls back to runtime execution).
- **Interviewer's Expectations**: Contrast read-only runtime variables with compile-time constants.

#### 47. What is memory-mapped file access (mmap) and how is it used in C++?
- **Detailed Answer**: `mmap` is a system call that maps a file's contents directly into the process's virtual address space. This allows the application to read and write file data using pointer offsets, bypassing standard file I/O system call overheads and caching data in OS page pools.
- **Follow-up Questions**: How do you sync changes back to disk? (Answer: Call the `msync` system call).
- **Interviewer's Expectations**: Detail virtual address mapping benefits over file read/write buffers.

#### 48. What is the difference between typedef and using in modern C++?
- **Detailed Answer**: Both define type aliases. `typedef` is the legacy C syntax (e.g. `typedef int my_int;`). `using` is the modern C++11 syntax (e.g. `using my_int = int;`). `using` is preferred because it is easier to read and supports templates (creating template aliases), which `typedef` does not support.
- **Follow-up Questions**: Write a template alias using `using`. (Answer: `template <typename T> using MyList = std::vector<T>;`).
- **Interviewer's Expectations**: Detail template alias capabilities.

#### 49. Explain the Curiously Recurring Template Pattern (CRTP).
- **Detailed Answer**: CRTP is a C++ design pattern where a class inherits from a template class, passing itself as a template parameter: `class Derived : public Base<Derived>`. This allows the base class to cast itself to the derived class at compile-time, enabling static polymorphism without vtables.
- **Follow-up Questions**: What is a benefit of CRTP? (Answer: Zero-overhead polymorphic interfaces and compiler inlining optimizations).
- **Interviewer's Expectations**: Show template parameter passing and static casts.

#### 50. What is data structure alignment and how does alignas work?
- **Detailed Answer**: Alignment dictates that variables must be allocated at memory addresses that are multiples of their size. The `alignas` specifier allows developers to force custom alignment rules (e.g. aligning a struct to a cache line boundary of 64 bytes) to optimize CPU cache reads.
- **Follow-up Questions**: What is a cache line? (Answer: The basic unit of data transfer between CPU cache and main memory, typically 64 bytes).
- **Interviewer's Expectations**: Explain memory alignments and cache boundaries.

#### 51. Explain how to detect and resolve cyclic references in smart pointers.
- **Detailed Answer**: Cyclic references occur when shared pointers create loops (e.g. A points to B, B points to A), preventing reference counts from dropping to zero. You resolve them by converting one of the shared references (usually parent references) into `std::weak_ptr`.
- **Follow-up Questions**: How does a `weak_ptr` resolve references? (Answer: It does not increment the strong reference count, allowing parent objects to be destroyed cleanly).
- **Interviewer's Expectations**: Identify loop references and propose weak_ptr solutions.

#### 52. What is the difference between structured binding and tuple unpacking?
- **Detailed Answer**: Structured binding (C++17) allows unpacking tuples, pairs, or structs into separate variables directly: `auto [x, y] = getPair()`. Tuple unpacking in older versions required `std::tie`, which required variables to be declared beforehand.
- **Follow-up Questions**: Can you use structured binding with custom classes? (Answer: Yes, by specializing `std::tuple_size` and `std::tuple_element` for the class).
- **Interviewer's Expectations**: Differentiate structured binding syntax from `std::tie`.

#### 53. Explain the difference between std::vector::reserve and std::vector::resize.
- **Detailed Answer**:
  - `reserve`: Allocates memory capacity without constructing objects, keeping vector size the same.
  - `resize`: Changes the vector size, constructing new objects if size increases or deleting them if size decreases.
- **Follow-up Questions**: Why use `reserve`? (Answer: To prevent multiple array reallocations and copies when adding many elements).
- **Interviewer's Expectations**: Contrast memory allocation capacity with object construction size.

#### 54. What is a conversion operator and what are the dangers of implicit conversions?
- **Detailed Answer**: A conversion operator allows a class to be implicitly cast to another type: `operator int() const { return value; }`. Implicit conversions can cause bugs by allowing unexpected compiler-driven casts (e.g., passing a class object to a function expecting an integer). To prevent this, mark conversion operators as `explicit`.
- **Follow-up Questions**: What does `explicit` do? (Answer: Forces the developer to use explicit casts, preventing the compiler from performing implicit type conversions).
- **Interviewer's Expectations**: Recommend `explicit` to prevent implicit cast bugs.

#### 55. Explain the purpose of std::decay in template metaprogramming.
- **Detailed Answer**: `std::decay` is a type trait that applies standard type conversions: removing references, const/volatile qualifiers, and converting arrays/functions to pointers, matching the type signature passed to function parameters by value.
- **Follow-up Questions**: When is `std::decay` used? (Answer: In generic forwarding and tuple storage structures to store clean, decay-converted types).
- **Interviewer's Expectations**: Detail array-to-pointer conversions and qualifiers removal.

#### 56. What is the difference between std::move and std::forward?
- **Detailed Answer**:
  - `std::move` performs an unconditional static cast of an lvalue to an rvalue reference, enabling resource moves.
  - `std::forward` performs a conditional cast, preserving rvalues as rvalues and lvalues as lvalues, enabling perfect forwarding.
- **Follow-up Questions**: What is perfect forwarding? (Answer: Preserving the reference type (lvalue or rvalue) of arguments when forwarding them to another function).
- **Interviewer's Expectations**: Contrast unconditional casting with conditional forwarding.

#### 57. Explain how the compiler implements exception handling and its performance costs.
- **Detailed Answer**: Exception handling is implemented using search tables. When an exception is thrown, the runtime performs stack unwinding, scanning table indexes to locate matching catch blocks. This adds zero overhead to normal code execution (zero-cost exceptions) but introduces latency when an exception is thrown.
- **Follow-up Questions**: What does `noexcept` do? (Answer: Informs the compiler that a function will not throw, enabling optimizations like vector reallocations using fast moves).
- **Interviewer's Expectations**: Detail stack unwinding tables and the benefits of `noexcept`.

#### 58. What is strict aliasing and how is it checked?
- **Detailed Answer**: Strict aliasing rules state that pointers of different types cannot refer to the same memory. Compilers assume no aliasing to reorder and optimize reads. You check for strict aliasing violations using compiler warnings (`-Wstrict-aliasing`).
- **Follow-up Questions**: Can you use `char*` to alias other types? (Answer: Yes, the standard explicitly permits `char*` and `unsigned char*` to alias any type).
- **Interviewer's Expectations**: Identify pointer type conversions rules.

#### 59. What are inline namespaces and why are they used in versioning?
- **Detailed Answer**: An `inline` namespace allows members of a nested namespace to be accessed as if they were members of the parent namespace. They are used in library versioning to define default active versions while preserving old signatures.
- **Follow-up Questions**: Write an inline namespace declaration. (Answer: `inline namespace V2 { void func(); }`).
- **Interviewer's Expectations**: Detail namespace versioning controls.

#### 60. Explain raw string literals and their use cases.
- **Detailed Answer**: Raw string literals (`R"(text)"`) ignore escape sequences (like `\n` or `\t`), treating backslashes as raw characters. They are used to write clean regex strings, JSON payloads, or file paths without double-escaping.
- **Follow-up Questions**: How do you include parentheses inside a raw string? (Answer: Use a custom delimiter, e.g. `R"custom(text(with)parentheses)custom"`).
- **Interviewer's Expectations**: Explain escape sequence bypasses.\n\n---

## 10. Common Mistakes
- **Returning Stack References**: Returning references to local variables on the stack.
- **Memory Leaks**: Not pairing `new` with `delete` (always prefer smart pointers).
- **Double Freeing**: Copying objects containing raw pointers without custom copy constructors.
- **Non-virtual destructors**: Missing `virtual` destructors in inherited base classes.
- **Unsigned overflow loops**: Writing `for (unsigned int i = 10; i >= 0; --i)` which loops infinitely because unsigned types cannot be negative.

---

## 11. Comparison Section: C vs C++

| Feature | C | C++ |
|---|---|---|
| **Programming Paradigm** | Procedural / Functional | Multi-paradigm (Procedural, OOP, Generic) |
| **Resource Management** | Manual (`malloc`/`free`) | RAII, Smart Pointers (`unique_ptr`, `shared_ptr`) |
| **Object Orientation** | No (structs only) | Yes (classes, inheritance, polymorphism) |
| **Generics** | No | Yes (Templates) |
| **Exception Handling** | Return codes / `setjmp`/`longjmp` | `try`/`catch` blocks |
| **Standard Library** | Minimal (`libc`) | Rich (`STL` containers, algorithms) |

---

## 12. Practical Project Ideas
- **Beginner**: A command-line program parsing custom text logs using pointer arithmetic.
- **Intermediate**: A custom string class implementing dynamic memory expansion, copy/move constructors, and string splicing.
- **Advanced**: A high-performance Key-Value storage engine utilizing memory-mapped files (`mmap`), page block caching, and custom arena allocations.

---

## 13. Internship Preparation Notes
- **Key Focus**: Pointers, pointers-to-pointers, stack vs heap allocations, and reference parameter passing.
- **Recruiting expectations**: Explain basic differences between C and C++, and show ability to write simple classes implementing virtual destructors.
- **Coding Rounds**: Be prepared to reverse a linked list or implement a binary search tree in C++.

---

## 14. Cheat Sheet
- **Smart Pointer instantiation**:
  ```cpp
  auto uptr = std::make_unique<Type>();
  auto sptr = std::make_shared<Type>();
  ```
- **Virtual Destructor**: `virtual ~Base() = default;`
- **Move static cast**: `std::move(variable)`
- **Pass by reference**: `void modify(int &ref);`

---

## 15. One-Day Revision Guide
- [ ] Differentiate stack vs heap memory scopes.
- [ ] Write a class implementing copy constructor and move constructor.
- [ ] Explain why base class destructors must be virtual.
- [ ] Differentiate `unique_ptr` and `shared_ptr`.
- [ ] Describe how vtables resolve virtual overrides at runtime.
- [ ] Detail Rule of Three, Five, and Zero.
- [ ] Identify signed vs unsigned overflow rules.
