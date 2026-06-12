# 34. JavaScript (Dynamic Web Programming)

## 1. Introduction

### What it is
JavaScript is a high-level, single-threaded, dynamically typed, garbage-collected, and prototype-based scripting language. As the core behavior engine of the web, it operates as an interpreted language that is compiled just-in-time (JIT) to machine code. While historically confined to the browser, JavaScript has evolved into a general-purpose language powering backend architectures (Node.js, Deno, Bun), desktop environments (Electron), mobile platforms (React Native), and edge computing services.

### Why it exists
While HTML defines document structure and CSS governs visual layouts, they cannot react dynamically to user actions, perform mathematical calculations, or retrieve external data from a server without a full page refresh. JavaScript was created to add behavioral logic to the web page, turning static documents into interactive applications by enabling direct manipulation of the Document Object Model (DOM).

### Problems it solves
- **Client-Side Interactivity**: Handles client-side actions such as button clicks, modal states, input validation, and drop-down layouts.
- **Asynchronous Data Transfers**: Fetches data dynamically from servers using AJAX and the Fetch API, avoiding the need for full page reloads.
- **Single Threaded Event Concurrency**: Manages concurrent tasks (like timer tracking or HTTP requests) using an asynchronous event loop without the complexity of multi-threaded race conditions or deadlocks.
- **Dynamic Type Adaptability**: Allows rapid prototyping and development without requiring strict static type definitions.
- **Platform Portability**: Executes identically in any modern browser using standard ECMAScript runtimes.

### Industry Use Cases
- **Single Page Applications (SPAs)**: Powering reactive web frameworks (React, Vue, Svelte, Angular).
- **Backend APIs and Microservices**: Running high-throughput applications with Node.js, Express, or Fastify.
- **Client-Side Storage**: Syncing user preferences, caching data, and enabling offline support via LocalStorage, IndexedDB, and Cache Storage APIs.
- **Build and Dev Tooling**: Orchestrating compiler and bundling configurations with Vite, Rollup, webpack, and ESLint.

### Analogy
If a web page is a theater production, HTML is the physical set structure (the walls and stage floor), CSS is the lighting and costumes (the colors and atmosphere), and JavaScript is the script and the actors' movements, managing timing, scene transitions, and direct responses to the audience's reactions.

---

## 2. Core Concepts

### Beginner Concepts
- **Variable Scope**: Variable declarations have different scoping rules: `var` (function-scoped or globally scoped, subject to hoisting), `let` (block-scoped, not accessible before declaration), and `const` (block-scoped, cannot be reassigned).
- **Primitive Types**: Raw data types stored directly on the stack: `string`, `number` (64-bit float), `boolean`, `undefined` (unassigned value), `null` (intentional absence of value), `bigint` (arbitrary-precision integer), and `symbol` (unique identifier).
- **Control Flow**: Directing logical execution via conditional statements (`if/else`, `switch`) and iteration blocks (`for`, `while`, `for...of` for arrays, `for...in` for object keys).
- **Functions**: Blocks of reusable code written as declarations, expressions, or arrow functions. Arrow functions do not bind their own `this`, `arguments`, or `super` keywords.
- **Standard Operators**: Operators for arithmetic, comparisons (`===` vs `==`), logical evaluation (`&&`, `||`, `!`), optional chaining (`?.`), and the nullish coalescing operator (`??`) which checks for `null` or `undefined`.

### Intermediate Concepts
- **Closures**: The mechanism where an inner function retains access to the variables of its outer enclosing scope, even after the outer function has finished executing.
- **Lexical Scoping**: The scope of a variable is determined by its physical position within the source code during compilation, rather than at runtime.
- **Prototype Chain**: The inheritance model where objects inherit properties and methods from their prototype object via the internal `[[Prototype]]` link.
- **`this` Binding**: The value of the `this` keyword, resolved at runtime based on how a function is called: default (global object or `undefined` in strict mode), implicit (the calling object), explicit (`call`, `apply`, `bind`), or lexical (inheriting from parent arrow function scope).
- **ES6+ Syntax**: Standard features like object/array destructuring, rest and spread operators (`...`), default function parameters, template literals, and ES Modules (`import`/`export`).
- **Asynchronous Execution**: Handling asynchronous tasks using callback functions, Promises, and `async/await` syntax.

### Advanced Concepts
- **Event Loop & Concurrency**: The mechanism that manages the execution of multiple tasks, using a call stack, a microtask queue (Promises), and a macrotask queue (timers, I/O).
- **V8 Engine Heap & Stack**: How memory is allocated: variables and execution contexts go on the stack, while objects and closures are allocated on the heap.
- **Garbage Collection Mechanics**: Automatic memory recovery using a generational garbage collector that splits the heap into young and old generations and uses mark-sweep-compact algorithms.
- **Proxies & Reflect**: Intercepting and defining custom behavior for fundamental object operations (like property lookups, assignments, and function invocations) using `new Proxy(target, handler)`.
- **Generators & Iterators**: Custom iteration behaviors using functions that can yield control mid-execution (`function*` and `yield`) and objects that implement the Iterator protocol.
- **Web Workers**: Running heavy computations on background threads to prevent blocking the main browser thread.

---

## 3. Internal Working

### Browser Engine Runtime Architecture
A JavaScript engine (like Chrome/Node's V8) uses a compiler pipeline to run code:

```text
Source Code ---> Parser ---> AST (Abstract Syntax Tree) ---> Interpreter (Ignition) 
                                                                |         ^
                                                                v         | (Deoptimization)
                                                         Compiler (TurboFan) 
                                                                |
                                                                v
                                                           Machine Code
```

1. **Parser & AST**: The engine parses source code into an Abstract Syntax Tree (AST).
2. **Interpreter (Ignition)**: Generates intermediate bytecode from the AST for quick startup times.
3. **Compiler (TurboFan)**: A JIT compiler that monitors execution hot-spots and compiles them directly into optimized machine code. If a type changes unexpectedly, it deoptimizes back to bytecode.

### The Event Loop Pipeline
The event loop coordinates synchronous and asynchronous execution:

```text
[ Call Stack ]  <--- executes synchronous code
      |
      +---> [ Web APIs / Node C++ APIs ] (runs setTimeout, Fetch, Event listeners)
                  |
                  v
       [ Microtask Queue ]   --- (Promise.then, queueMicrotask, MutationObserver)
       [ Macrotask Queue ]   --- (setTimeout, setInterval, setImmediate, I/O)
```

**Execution Order Rules**:
1. Run all synchronous code on the **Call Stack** until it is empty.
2. Check the **Microtask Queue**. Run all microtasks until the queue is completely empty. If a microtask adds another microtask, run that one too before proceeding.
3. If needed, perform a browser paint and style recalculation.
4. Take the oldest task from the **Macrotask Queue** and push it onto the Call Stack to execute.
5. Repeat the cycle.

### Prototype Chain Mechanics
When you look up a property on an object, JavaScript checks the object itself. If not found, it traverses up the prototype chain:

```text
[ instance: student ]
       |
       +---> __proto__ ---> [ Student.prototype ]
                                    |
                                    +---> __proto__ ---> [ Object.prototype ]
                                                                 |
                                                                 +---> __proto__ ---> null
```

If the property is not found anywhere in the chain, it returns `undefined`.

---

## 4. Important Terminology

- **Execution Context**: The environment in which JavaScript code is evaluated and executed. It contains the Variable Object, Scope Chain, and `this` value.
- **Hoisting**: The behavior where variable and function declarations are moved to the top of their containing scope during compilation.
- **Temporal Dead Zone (TDZ)**: The period between block entry and variable declaration where accessing `let` or `const` variables throws a `ReferenceError`.
- **Memory Leak**: Allocated memory that is no longer needed by the application but has not been returned to the operating system by the garbage collector.
- **Microtask**: A small task executed immediately after the current script finishes and before the browser yields control back to the event loop.
- **Macrotask**: A heavier, standalone task queued for execution on the next event loop iteration.
- **Event Delegation**: A pattern where you attach a single event listener to a parent element to handle events bubbles up from its children.
- **Garbage Collection (GC)**: The automated process of identifying and releasing unused memory across the heap.

---

## 5. Beginner Examples

### Example 1: Scopes, Hoisting, and the Temporal Dead Zone
```javascript
// Function hoisting: allowed because function declarations are fully hoisted
greet(); 

function greet() {
  console.log("Hello!");
}

// var hoisting: variable is hoisted but initialized as undefined
console.log(oldVar); // undefined
var oldVar = 5;

// let/const TDZ: throws ReferenceError because let/const are in the TDZ until declared
try {
  console.log(newLet);
} catch (error) {
  console.error(error.message); // Cannot access 'newLet' before initialization
}
let newLet = 10;
```

### Example 2: Array Transformations
```javascript
const inventory = [
  { id: 101, name: "Laptop", category: "Electronics", price: 1200, stock: 15 },
  { id: 102, name: "Chair", category: "Furniture", price: 150, stock: 8 },
  { id: 103, name: "Headphones", category: "Electronics", price: 200, stock: 0 },
  { id: 104, name: "Desk", category: "Furniture", price: 450, stock: 4 }
];

// 1. Filter: Get in-stock electronics
const inStockElectronics = inventory.filter(item => item.category === "Electronics" && item.stock > 0);

// 2. Map: Format names and prices
const formattedItems = inStockElectronics.map(item => `${item.name} ($${item.price})`);

// 3. Reduce: Calculate total value of in-stock furniture items
const totalFurnitureValue = inventory
  .filter(item => item.category === "Furniture")
  .reduce((total, item) => total + (item.price * item.stock), 0);

console.log(formattedItems); // ["Laptop ($1200)"]
console.log(totalFurnitureValue); // (150*8) + (450*4) = 1200 + 1800 = 3000
```

### Example 3: Basic Async/Await Fetch Wrapper
```javascript
async function fetchUserData(userId) {
  const url = `https://jsonplaceholder.typicode.com/users/${userId}`;
  
  try {
    const response = await fetch(url);
    
    // Check if HTTP status indicates success (status in the range 200-299)
    if (!response.ok) {
      throw new Error(`Failed to fetch user. Status: ${response.status}`);
    }
    
    const data = await response.json();
    return { success: true, user: data };
  } catch (error) {
    console.error("fetchUserData encountered an error:", error.message);
    return { success: false, error: error.message };
  }
}
```

---

## 6. Intermediate Examples

### Example 1: Closure for Data Encapsulation
A closure creates private variable scopes that cannot be accessed or modified from the outside.

```javascript
function createBankAccount(ownerName, initialBalance) {
  // Private variables nested inside the outer function's execution scope
  let balance = initialBalance;
  const ledger = [{ type: "Opening", amount: initialBalance, date: new Date() }];

  return {
    deposit(amount) {
      if (amount <= 0) throw new Error("Deposit amount must be positive");
      balance += amount;
      ledger.push({ type: "Deposit", amount, date: new Date() });
      return balance;
    },
    withdraw(amount) {
      if (amount > balance) throw new Error("Insufficient funds");
      balance -= amount;
      ledger.push({ type: "Withdrawal", amount, date: new Date() });
      return balance;
    },
    getBalance() {
      // Returns a read-only copy of the private balance value
      return balance;
    },
    getStatement() {
      // Return a copy to prevent mutation of the internal ledger array
      return [...ledger];
    }
  };
}

const myAccount = createBankAccount("John Doe", 500);
myAccount.deposit(250);
myAccount.withdraw(100);
console.log(myAccount.getBalance()); // 650
// console.log(myAccount.balance); // undefined (cannot access private scope directly)
```

### Example 2: Custom Debounce and Throttle Helpers
```javascript
// Debounce delays function execution until a specified idle period has passed
function debounce(fn, waitMs = 300) {
  let timerId = null;
  
  return function (...args) {
    const context = this;
    
    if (timerId) clearTimeout(timerId);
    
    timerId = setTimeout(() => {
      fn.apply(context, args);
    }, waitMs);
  };
}

// Throttle guarantees a function runs at most once in a specified time window
function throttle(fn, limitMs = 300) {
  let inThrottle = false;
  
  return function (...args) {
    const context = this;
    
    if (!inThrottle) {
      fn.apply(context, args);
      inThrottle = true;
      setTimeout(() => {
        inThrottle = false;
      }, limitMs);
    }
  };
}
```

### Example 3: Asynchronous API Request Concurrency Controller
Managing high-volume API requests by limiting maximum concurrency.

```javascript
async function limitConcurrency(taskFns, limit) {
  const results = [];
  const executing = new Set();
  
  for (const fn of taskFns) {
    const promise = Promise.resolve().then(() => fn());
    results.push(promise);
    
    if (limit <= taskFns.length) {
      executing.add(promise);
      
      const clean = () => executing.delete(promise);
      promise.then(clean, clean);
      
      if (executing.size >= limit) {
        // Wait for the first running task in the set to complete
        await Promise.race(executing);
      }
    }
  }
  
  return Promise.all(results);
}
```

---

## 7. Advanced Concepts

### Identifying and Fixing Memory Leaks
Memory leaks often happen when variables remain referenced in memory after they are no longer needed, preventing garbage collection.

```javascript
// 1. Accidental global variable leak
function leakGlobal() {
  leakedVar = new Array(1000000); // Missing var/let/const attaches variable to window
}

// 2. Uncleared Timer leak
function runTimer() {
  const largeObject = { data: new Array(1000000) };
  setInterval(() => {
    // Closes over largeObject, preventing it from being garbage collected
    console.log(largeObject.data.length);
  }, 1000);
}

// 3. Detached DOM Nodes leak
let detachedNode;
function createAndRemoveElement() {
  detachedNode = document.createElement("div");
  detachedNode.id = "leak";
  document.body.appendChild(detachedNode);
  document.body.removeChild(detachedNode);
  // detachedNode still references the element, keeping it in memory
}

// Fix: Clean up references and use WeakMaps
const cache = new WeakMap();

function processElement(element) {
  // Storing metadata associated with a DOM element
  // When the element is removed from the DOM, it can be garbage collected
  cache.set(element, { processed: true });
}
```

### Advanced Reactive State Tracking using Proxy
A mini reactive engine that detects property mutations and runs side effects automatically.

```javascript
const effectsQueue = new Set();
let activeEffect = null;

function observe(fn) {
  activeEffect = fn;
  fn();
  activeEffect = null;
}

function reactive(target) {
  const dependencyMap = new Map();
  
  return new Proxy(target, {
    get(obj, key, receiver) {
      const value = Reflect.get(obj, key, receiver);
      
      if (activeEffect) {
        let deps = dependencyMap.get(key);
        if (!deps) {
          deps = new Set();
          dependencyMap.set(key, deps);
        }
        deps.add(activeEffect);
      }
      return value;
    },
    set(obj, key, value, receiver) {
      const success = Reflect.set(obj, key, value, receiver);
      const deps = dependencyMap.get(key);
      if (deps) {
        deps.forEach(effect => effect());
      }
      return success;
    }
  });
}

// Usage
const state = reactive({ count: 0 });
observe(() => {
  console.log(`State count changed: ${state.count}`);
});
state.count = 5; // Triggers effect console output automatically
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look beyond framework-specific APIs to test your fundamental understanding of the browser runtime. They want to see if you can write non-blocking asynchronous code, manage scope, prevent memory leaks, and understand prototype mechanics.

### Red Flags
- **Accidental globals**: Declaring variables without keyword qualifiers.
- **Synchronous loops**: Writing blocks that block the event loop instead of using chunking or Web Workers.
- **Ignoring rejections**: Writing promises or fetch requests without `.catch()` blocks or `try/catch` wrappers.
- **Confusing arrow function scope**: Using arrow functions for object methods and wondering why `this` returns `undefined` (because it inherits lexically).

### Green Flags
- **Event loop mastery**: Accurately tracing task and microtask execution orders.
- **Clean closures**: Using closures intentionally for data encapsulation or scoping.
- **Correct prototype usage**: Implementing inheritance pattern structures without relying exclusively on class syntax.
- **Memory awareness**: Cleaning up event listeners and intervals when they are no longer needed.

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What are the differences between `var`, `let`, and `const`? Explain scope, hoisting, and the Temporal Dead Zone (TDZ).
- **Detailed Answer**:
  - **Scope**: `var` is function-scoped. If declared outside a function, it attaches to the global object. `let` and `const` are block-scoped, meaning they are restricted to the containing curly braces `{}` (such as loops, conditionals, or functions).
  - **Hoisting & TDZ**: All three declarations are hoisted to the top of their scope during compilation. However:
    * `var` is hoisted and initialized as `undefined`. You can access it before its line declaration without throwing an error.
    * `let` and `const` are hoisted but remain uninitialized in the **Temporal Dead Zone (TDZ)**. Accessing them before their declaration throws a `ReferenceError`.
  - **Reassignment**: `var` and `let` allow reassignment. `const` creates a read-only reference that cannot be reassigned (though if the value is an object or array, its properties can still be mutated).
- **Follow-up Questions**:
  - Does `const` make objects immutable? (No, use `Object.freeze()` to prevent property mutation).
  - How does hoisting behave in block scopes? (`let` and `const` are hoisted to the top of their block scope, not the function scope).
- **Interviewer's Expectations**:
  - Explaining block scope vs. function scope.
  - Explaining the TDZ and how it prevents runtime errors.
  - Demonstrating clear hoisting mechanics.

#### 2. What is a closure? How does the JavaScript engine manage memory for variables enclosed within closures?
- **Detailed Answer**: A closure is formed when a nested function is defined inside an outer function, allowing the inner function to retain access to variables in the outer function's scope (its lexical environment), even after the outer function has finished executing.
  
  **Memory Management**: Normally, when a function finishes executing, its local execution context stack frame is popped off, and its variables are marked for garbage collection. However, if an inner function is returned or remains referenced elsewhere, the JavaScript engine detects that the inner function references variables in the outer function's scope. The engine moves these variables from the stack to the **Heap**, keeping them alive as long as the inner function remains referenced.
- **Follow-up Questions**:
  - Can closures cause memory leaks? (Yes, if the inner function is stored globally or inside long-lived event listeners without being cleared).
  - How do you destroy a closure? (By setting the reference to the inner function to `null`).
- **Interviewer's Expectations**:
  - A clear definition of closures and lexical environments.
  - Explaining that variables are kept on the heap rather than the stack.
  - Discussing the memory implications of closures.

#### 3. Explain the resolution rules of the `this` keyword. How do arrow functions change these rules?
- **Detailed Answer**: The value of the `this` keyword is resolved at runtime based on the function's call site and execution context:
  1. **Default Binding**: In a standalone function call, `this` refers to the global object (`window` in browsers, `global` in Node.js) or is `undefined` in strict mode.
  2. **Implicit Binding**: When a function is called as a method on an object (e.g., `obj.method()`), `this` refers to the object before the dot (`obj`).
  3. **Explicit Binding**: Using `call`, `apply`, or `bind` allows you to explicitly set the value of `this`.
  4. **New Binding**: When calling a constructor function with the `new` keyword, `this` refers to the newly created instance object.
  
  **Arrow Functions**: Arrow functions do not have their own `this` binding. Instead, they inherit `this` **lexically** from their enclosing parent scope at the time they are defined. Their `this` value cannot be changed, even when using `call`, `apply`, or `bind`.
- **Follow-up Questions**:
  - What happens when you pass an object method as a callback? (It loses its implicit binding, and `this` falls back to default binding. You can fix this by binding it or using an arrow function).
  - What is the difference between `call` and `apply`? (`call` accepts arguments individually: `fn.call(ctx, arg1, arg2)`. `apply` accepts them as an array: `fn.apply(ctx, [arg1, arg2])`).
- **Interviewer's Expectations**:
  - Listing the four binding rules in order of priority.
  - Explaining the difference between runtime dynamic binding and compile-time lexical binding.
  - Writing code showing how implicit binding can be lost.

#### 4. How does prototype inheritance work in JavaScript? Contrast it with class-based inheritance.
- **Detailed Answer**:
  - **Prototype Inheritance**: Every JavaScript object has an internal link (historically accessed via `__proto__`, standardly queried via `Object.getPrototypeOf`) pointing to another object called its prototype. When you access a property on an object, the engine searches the object itself. If not found, it searches the prototype, and continues up the prototype chain until it reaches `Object.prototype` (and eventually `null`).
  - **Class Syntax**: Introduced in ES6, the `class` keyword is syntactic sugar over prototype-based inheritance. It does not introduce a new object model; under the hood, classes still use constructor functions and prototypes.
  
  *Comparison*:
  * Class-based languages instantiate objects by copying layouts defined in class blueprints.
  * JavaScript objects are linked dynamically to their prototype object. If you add a method to a prototype at runtime, all instances instantly gain access to it.
- **Follow-up Questions**:
  - What does `new` do behind the scenes? (Creates an empty object, links its prototype to the constructor's prototype, binds `this` to the new object, and returns it).
  - How do you create an object with no prototype? (Using `Object.create(null)`).
- **Interviewer's Expectations**:
  - Explaining the prototype chain lookup mechanism.
  - Clarifying that class syntax is syntactic sugar.
  - Explaining the dynamic nature of prototype updates.

#### 5. Walk through the Event Loop, including the Call Stack, Microtask Queue, and Macrotask Queue.
- **Detailed Answer**: The JavaScript runtime is single-threaded, meaning it can only execute one statement at a time using its Call Stack. To handle asynchronous operations without blocking execution, the engine uses the **Event Loop**:
  1. **Synchronous Execution**: The engine pushes synchronous statements onto the Call Stack and executes them.
  2. **Asynchronous Hand-off**: When an async API is called (e.g., `setTimeout`, `fetch`), the task is handed off to the browser's Web APIs (or Node's C++ threads), and execution continues.
  3. **Queueing**: Once the async task completes, its callback is placed into one of two queues:
     * **Microtask Queue**: For high-priority tasks like Promise resolutions (`.then`/`catch`/`finally`), `queueMicrotask`, and `MutationObserver` callbacks.
     * **Macrotask Queue** (or Task Queue): For timers (`setTimeout`, `setInterval`), I/O operations, and user interactions (clicks, keyboard input).
  4. **The Event Loop Cycle**: The event loop continuously checks if the Call Stack is empty. When it is:
     * It runs all callbacks in the Microtask Queue one by one until the queue is completely empty.
     * If there are rendering updates, it paints the screen.
     * It runs the oldest task from the Macrotask Queue, executes it, and repeats the cycle.
- **Follow-up Questions**:
  - What happens if a microtask queues another microtask infinitely? (It starves the event loop, blocking user interactions and freezing the page).
  - Trace this output:
    ```javascript
    console.log(1);
    setTimeout(() => console.log(2), 0);
    Promise.resolve().then(() => console.log(3));
    console.log(4);
    ```
    (Output: `1, 4, 3, 2`. Synchronous: `1, 4`. Microtask: `3`. Macrotask: `2`).
- **Interviewer's Expectations**:
  - Accurately explaining the roles of the Call Stack, Microtask Queue, and Macrotask Queue.
  - Explaining that the Microtask Queue is completely drained before processing the next macrotask.
  - Tracing execution ordering examples.

#### 6. What is the difference between different Promise orchestration methods: `Promise.all`, `Promise.allSettled`, `Promise.race`, and `Promise.any`?
- **Detailed Answer**:
  - **`Promise.all`**: Runs promises concurrently. It resolves when all input promises have resolved, returning an array of results. If *any* promise rejects, the entire operation rejects immediately with that error.
    *Use case*: Fetching multiple independent endpoints where all data is required for the page.
  - **`Promise.allSettled`**: Runs promises concurrently. It waits for all input promises to settle (either resolve or reject) and returns an array of outcome objects containing their status and value/reason. It never rejects.
    *Use case*: Running independent batch operations where you want to know which ones succeeded and which ones failed.
  - **`Promise.race`**: Settles as soon as the *first* promise in the input array settles (either resolves or rejects).
    *Use case*: Implementing request timeouts by racing a fetch call against a timer promise.
  - **`Promise.any`**: Resolves as soon as the *first* promise resolves. If all promises reject, it rejects with an AggregateError containing all the errors.
    *Use case*: Fetching the same resource from mirror servers and using the fastest successful response.
- **Follow-up Questions**:
  - How do you handle individual errors in `Promise.all` without rejecting the whole operation? (By attaching a `.catch()` block to each individual promise before passing it to `Promise.all`).
  - Does `Promise.all` run promises in parallel? (No, JavaScript is single-threaded, so it coordinates them concurrently, not in parallel).
- **Interviewer's Expectations**:
  - Clear distinction between early-rejection behavior (`all`), non-rejecting aggregation (`allSettled`), fastest settling (`race`), and fastest resolution (`any`).
  - Providing practical use cases for each method.

#### 7. How does `async/await` work under the hood? How does it compile down to older Promise chains?
- **Detailed Answer**: `async/await` is syntactic sugar over Promises and Generators. When a function is marked as `async`, it is compiled to return a Promise. When the engine encounters an `await` statement, it pauses the execution of the async function, yields control back to the call stack, and resumes execution once the awaited Promise resolves.
  
  Under the hood, the compiler transforms `async/await` syntax into a generator function wrapped in a recursive promise-resolving runner (often called a co-routine):
  
  *Original Code*:
  ```javascript
  async function getData() {
    const r1 = await fetch('/api1');
    const data = await r1.json();
    return data;
  }
  ```
  
  *Equivalent Generator Transformation*:
  ```javascript
  function getData() {
    return spawn(function* () {
      const r1 = yield fetch('/api1');
      const data = yield r1.json();
      return data;
    });
  }
  
  // Recursive runner wrapper
  function spawn(genF) {
    return new Promise((resolve, reject) => {
      const gen = genF();
      function step(nextF) {
        let next;
        try { next = nextF(); } catch(e) { return reject(e); }
        if (next.done) return resolve(next.value);
        Promise.resolve(next.value).then(
          v => step(() => gen.next(v)),
          e => step(() => gen.throw(e))
        );
      }
      step(() => gen.next());
    });
  }
  ```
- **Follow-up Questions**:
  - What happens if you forget to `await` a promise? (The code execution continues immediately, and the variable stores the pending Promise object instead of the resolved value).
  - Can you use `await` outside of an async function? (Yes, in environments that support top-level await in ES Modules).
- **Interviewer's Expectations**:
  - Explaining the relationship between async/await, generators, and promises.
  - Showing how yielding works using generator functions.
  - Explaining the role of the recursive runner.

#### 8. What is the difference between shallow copying and deep copying? How do you implement each in JavaScript?
- **Detailed Answer**:
  - **Shallow Copy**: Copies only the top-level properties of an object or array. Nested objects or arrays are not cloned; instead, their references are copied, meaning changes to nested properties will affect both the original and the copy.
    *Implementation*: Spread operator `{...obj}`, `Object.assign({}, obj)`, or `Array.prototype.slice()` for arrays.
  - **Deep Copy**: Recursively clones the entire object structure, creating new references for all nested objects and arrays. Changes to the copy have no effect on the original.
    *Implementation*:
    1. **`structuredClone(obj)`**: The modern, native Web API that handles nested structures, circular references, and diverse built-in types (Dates, RegExps, TypedArrays).
    2. **`JSON.parse(JSON.stringify(obj))`**: A common fallback, but it fails on `undefined`, functions, symbols, and circular references.
    3. **Custom Recursive Function**: Using recursion to deep copy custom object structures.
- **Follow-up Questions**:
  - Why does `JSON.stringify` fail on Map or Set? (JSON does not support Map or Set structures, so they are serialized as empty objects `{}`).
  - What happens if you run `structuredClone` on an object containing a function? (It throws a `DataCloneError`, as functions cannot be serialized across structured clone boundaries).
- **Interviewer's Expectations**:
  - Explaining reference copying vs. recursive value copying.
  - Pointing out the limitations of the `JSON` serialization hack.
  - Recommending `structuredClone` as the modern standard.

#### 9. Compare ES Modules (ESM) and CommonJS (CJS). What are the execution and loading differences?
- **Detailed Answer**:
  - **CommonJS (CJS)**:
    * Syntax: Uses `require()` and `module.exports`.
    * Resolution: Synchronous and blocking. Modules are loaded, parsed, and executed sequentially at runtime.
    * Mutability: Exports are copied values. Once imported, they are not updated if the exporting module changes them.
    * Context: CommonJS files are executed within a wrapper function that provides variables like `__dirname` and `__filename`.
  - **ES Modules (ESM)**:
    * Syntax: Uses `import` and `export`.
    * Resolution: Asynchronous. Loading and parsing happen during static analysis before code execution. This allows compile-time optimizations like tree-shaking (removing unused code).
    * Mutability: Exports are live read-only bindings. If the exporting module updates a value, the importing module sees the change.
    * Context: Strict mode is active by default. Global variables like `__dirname` do not exist (you must use `import.meta.url`).
- **Follow-up Questions**:
  - Can you import CommonJS modules into ES Modules? (Yes, you can import them, but you cannot use named exports; you must import the default object).
  - Can you use dynamic imports in CommonJS? (Yes, using the asynchronous `import()` function).
- **Interviewer's Expectations**:
  - Distinguishing between runtime synchronous loading (CJS) and static asynchronous resolution (ESM).
  - Explaining the difference between copied values and live bindings.
  - Describing compile-time optimization benefits like tree-shaking.

#### 10. What are generators and iterators? How do they enable custom iteration behaviors?
- **Detailed Answer**:
  - **Iterators**: An object is an iterator if it implements a `.next()` method that returns an object containing two properties: `value` (the next value in the sequence) and `done` (a boolean indicating if the iteration is complete).
  - **Iterable Protocol**: An object is iterable if it defines a method with the key `Symbol.iterator` that returns an iterator object.
  - **Generators**: A generator function (`function*`) simplifies writing iterators. Calling a generator returns a Generator Object that conforms to both the iterator and iterable protocols. The function execution can be paused using the `yield` keyword and resumed by calling `.next()` on the generator object.
  
  *Custom Iterator Example*:
  ```javascript
  const fibonacciSequence = {
    [Symbol.iterator]() {
      let fn1 = 0, fn2 = 1;
      return {
        next() {
          const current = fn1;
          fn1 = fn2;
          fn2 = current + fn1;
          return { value: current, done: current > 50 };
        }
      };
    }
  };
  
  for (const num of fibonacciSequence) {
    console.log(num); // Prints Fibonacci numbers up to 50
  }
  ```
- **Follow-up Questions**:
  - Can you pass values back into a generator? (Yes, calling `.next(value)` sends that value back into the generator function as the result of the paused `yield` expression).
  - What is the difference between `yield` and `yield*`? (`yield` returns a single value; `yield*` delegates iteration to another iterable object, yielding all its values).
- **Interviewer's Expectations**:
  - Explaining the iterator and iterable protocols.
  - Describing the role of the `Symbol.iterator` property.
  - Demonstrating how generators simplify custom iteration.

---

### Scenario-Based Questions

#### 11. Implement custom debounce and throttle functions from scratch.
- **Detailed Answer**:
  ```javascript
  // Debounce delays function execution until a specified idle period has passed
  function debounce(fn, waitMs = 300) {
    let timerId = null;
    
    return function (...args) {
      const context = this;
      
      if (timerId) {
        clearTimeout(timerId);
      }
      
      timerId = setTimeout(() => {
        fn.apply(context, args);
      }, waitMs);
    };
  }
  
  // Throttle guarantees a function runs at most once in a specified time window
  function throttle(fn, limitMs = 300) {
    let inThrottle = false;
    
    return function (...args) {
      const context = this;
      
      if (!inThrottle) {
        fn.apply(context, args);
        inThrottle = true;
        
        setTimeout(() => {
          inThrottle = false;
        }, limitMs);
      }
    };
  }
  ```
- **Follow-up Questions**:
  - How do you add a `cancel` method to a debounced function? (By attaching a `.cancel` function to the returned wrapper function that calls `clearTimeout(timerId)`).
  - What happens to arguments passed to debounced calls during the delay? (Only the arguments from the last call are used when the function eventually runs).
- **Interviewer's Expectations**:
  - Using closures to preserve timer states.
  - Preserving the calling context (`this`) and arguments.
  - Explaining the difference between delaying execution (debounce) and limiting execution frequency (throttle).

#### 12. Write a function that fetches data from multiple URLs concurrently but limits active requests to a maximum concurrency limit.
- **Detailed Answer**:
  We can implement a concurrency pool using a helper that executes tasks and returns their results once all complete.
  ```javascript
  async function fetchWithConcurrencyLimit(urls, maxConcurrency) {
    const results = new Array(urls.length);
    let index = 0; // Tracks the next URL to process
  
    async function worker() {
      while (index < urls.length) {
        const currentIndex = index++;
        const url = urls[currentIndex];
        
        try {
          const response = await fetch(url);
          results[currentIndex] = response.ok ? await response.json() : null;
        } catch (error) {
          results[currentIndex] = { error: error.message };
        }
      }
    }
  
    // Create and start worker pool threads
    const pool = Array.from({ length: Math.min(urls.length, maxConcurrency) }, worker);
    await Promise.all(pool);
    return results;
  }
  ```
- **Follow-up Questions**:
  - What happens if the `urls` array is empty? (The worker pool array will be empty, and `Promise.all` will resolve immediately with an empty array).
  - How would you modify this to reject early if a worker encounters a critical failure? (Throw an error in the worker function, which rejects the `Promise.all` wrapper).
- **Interviewer's Expectations**:
  - Managing a shared index pointer across multiple worker promises.
  - Avoiding nesting loops that exceed the concurrency limit.
  - Handling request errors gracefully without halting the remaining tasks.

#### 13. Design an in-memory API response cache helper that supports expiration (Time-to-Live / TTL).
- **Detailed Answer**:
  A class-based cache container can manage storage, retrieval, and automated cleanup of expired responses.
  ```javascript
  class APICache {
    constructor() {
      this.store = new Map();
    }
  
    set(key, val, ttlMs = 60000) {
      const expiresAt = Date.now() + ttlMs;
      this.store.set(key, { val, expiresAt });
    }
  
    get(key) {
      const entry = this.store.get(key);
      if (!entry) return null;
      
      // If the cache entry has expired, delete it and return null
      if (Date.now() > entry.expiresAt) {
        this.store.delete(key);
        return null;
      }
      return entry.val;
    }
  
    delete(key) {
      this.store.delete(key);
    }
  
    clear() {
      this.store.clear();
    }
  }
  ```
- **Follow-up Questions**:
  - Does expired data sit in memory if it is never accessed again? (Yes, to prevent memory leaks, you can run a background interval that sweeps and removes expired entries).
  - Why use a `Map` instead of a plain object? (Maps have better insertion/deletion performance and support any data type as keys).
- **Interviewer's Expectations**:
  - Using timestamps to calculate expiration.
  - Cleaning up expired entries on access.
  - Describing strategies to handle memory management (e.g., eviction policies).

#### 14. Build a custom EventEmitter (Publisher/Subscriber) class from scratch.
- **Detailed Answer**:
  ```javascript
  class EventEmitter {
    constructor() {
      this.events = {};
    }
  
    on(eventName, callback) {
      if (!this.events[eventName]) {
        this.events[eventName] = [];
      }
      this.events[eventName].push(callback);
      
      // Return a unsubscribe function for convenience
      return () => this.off(eventName, callback);
    }
  
    emit(eventName, ...args) {
      const listeners = this.events[eventName];
      if (!listeners) return;
      
      // Copy the array to prevent mutation issues if a listener unsubscribes mid-emit
      [...listeners].forEach(callback => {
        try {
          callback.apply(null, args);
        } catch (error) {
          console.error(`Error in listener for ${eventName}:`, error);
        }
      });
    }
  
    off(eventName, callback) {
      const listeners = this.events[eventName];
      if (!listeners) return;
      
      this.events[eventName] = listeners.filter(cb => cb !== callback);
    }
  
    once(eventName, callback) {
      const unsubscribe = this.on(eventName, (...args) => {
        unsubscribe();
        callback.apply(null, args);
      });
    }
  }
  ```
- **Follow-up Questions**:
  - Why did we copy the listener list before running it inside `emit`? (To prevent infinite loops or skipped callbacks if a listener unsubscribes itself during execution).
  - Can you pass context to event emitter listeners? (Yes, by passing a context parameter or using arrow functions).
- **Interviewer's Expectations**:
  - Storing events as key-value pairs of arrays.
  - Handling subscription removal (`off`).
  - Correct implementation of one-time listeners (`once`).

#### 15. Implement a state machine to manage transitions inside a multi-step user checkout flow.
- **Detailed Answer**:
  We can define a state machine that enforces valid transition paths between steps:
  ```javascript
  const CheckoutStates = {
    CART: "CART",
    SHIPPING: "SHIPPING",
    PAYMENT: "PAYMENT",
    REVIEW: "REVIEW",
    CONFIRMED: "CONFIRMED"
  };
  
  const ValidTransitions = {
    [CheckoutStates.CART]: [CheckoutStates.SHIPPING],
    [CheckoutStates.SHIPPING]: [CheckoutStates.CART, CheckoutStates.PAYMENT],
    [CheckoutStates.PAYMENT]: [CheckoutStates.SHIPPING, CheckoutStates.REVIEW],
    [CheckoutStates.REVIEW]: [CheckoutStates.PAYMENT, CheckoutStates.CONFIRMED],
    [CheckoutStates.CONFIRMED]: [] // Terminal state
  };
  
  class CheckoutStateMachine {
    constructor() {
      this.currentState = CheckoutStates.CART;
    }
  
    transitionTo(nextState) {
      const allowed = ValidTransitions[this.currentState];
      
      if (!allowed || !allowed.includes(nextState)) {
        throw new Error(`Invalid state transition: ${this.currentState} -> ${nextState}`);
      }
      
      this.currentState = nextState;
      return this.currentState;
    }
  
    getState() {
      return this.currentState;
    }
  }
  ```
- **Follow-up Questions**:
  - How do you integrate side effects when entering a state? (By attaching action callbacks or event listeners that run when `transitionTo` is called).
  - Can a state machine scale to handle complex branching paths? (Yes, by keeping transition conditions dynamic instead of static arrays).
- **Interviewer's Expectations**:
  - Restricting state transitions to explicit allowed paths.
  - Handling illegal transitions gracefully with descriptive errors.
  - Keeping state models clean and predictable.

---

### Debugging Questions

#### 16. How do you troubleshoot the error: `TypeError: Cannot read properties of undefined (reading 'x')`?
- **Detailed Answer**:
  *Debugging strategy*:
  1. **Locate the line**: Look at the stack trace to find the exact file and line number where the error occurred.
  2. **Identify the root cause**: The error indicates that the code is trying to access a property `x` on a variable that evaluates to `undefined` or `null`.
     ```javascript
     const user = undefined;
     console.log(user.x); // Throws TypeError
     ```
  3. **Trace data flow**: Check why the parent object was not initialized. Common causes include failed API fetches, incorrect object destructuring, or asynchronous timing issues.
  4. **Apply safe access practices**:
     * Use **Optional Chaining** (`?.`): `user?.x` returns `undefined` instead of throwing an error.
     * Set **Default Parameters**: `const { x = {} } = user || {};`
     * Add **Type Guards**: `if (user && user.x) { ... }`
- **Follow-up Questions**:
  - What is the difference between optional chaining `?.` and logical AND `&&`? (Optional chaining is shorter and handles intermediate nullish properties cleanly without repeating variables).
  - How do you distinguish between `null` and `undefined`? (`undefined` means a variable has been declared but not yet assigned a value; `null` is an assignment value that represents no value).
- **Interviewer's Expectations**:
  - Explaining the cause of the error.
  - Using debugging tools and stack traces to isolate the issue.
  - Resolving the error using optional chaining, logical guards, or default fallback values.

#### 17. How do you resolve issues where asynchronous callback functions in a loop capture the wrong loop index?
- **Detailed Answer**:
  *The Cause*: This issue typically happens when using `var` declarations in a loop:
  ```javascript
  // Prints "3, 3, 3" instead of "0, 1, 2"
  for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100);
  }
  ```
  Because `var` is function-scoped, there is only a single shared `i` variable instance for the entire loop. By the time the asynchronous `setTimeout` callbacks run, the loop has completed, and the shared variable `i` has been incremented to `3`.
  
  *Solutions*:
  1. **Use `let`**: Changing `var` to `let` creates a new block-scoped variable binding for every loop iteration, preserving the correct index value:
     ```javascript
     for (let i = 0; i < 3; i++) {
       setTimeout(() => console.log(i), 100); // Prints "0, 1, 2"
     }
     ```
  2. **Create a IIFE closure**: If working in older ES5 environments, wrap the asynchronous call inside an Immediately Invoked Function Expression (IIFE) to capture the index:
     ```javascript
     for (var i = 0; i < 3; i++) {
       (function(capturedIndex) {
         setTimeout(() => console.log(capturedIndex), 100);
       })(i);
     }
     ```
- **Follow-up Questions**:
  - How does this work under the hood when using `let`? (The engine creates a new lexical scope container for each loop iteration, saving the variable state).
  - Does this issue happen when using `forEach` loops? (No, `forEach` passes the value as a function parameter, which naturally captures the index inside a closure).
- **Interviewer's Expectations**:
  - Explaining block scoping vs. function scoping.
  - Demonstrating how closures capture variables.
  - Providing solutions using modern `let` keywords or IIFE patterns.

#### 18. How do you identify memory leaks in a single-page application using Chrome DevTools?
- **Detailed Answer**:
  *Troubleshooting Process*:
  1. **Identify the leak**: Open Chrome DevTools and navigate to the **Performance** tab. Check the Memory checkbox, record a session, and perform interactions (e.g., opening and closing modals). Look for a "sawtooth" memory graph that climbs upwards without dropping back down to its initial baseline, indicating that memory is not being released.
  2. **Take Heap Snapshots**: Switch to the **Memory** tab and select **Heap snapshot**:
     * Take snapshot 1 (baseline state).
     * Perform the interaction several times (e.g., opening and closing a view).
     * Take snapshot 2 (suspected leak state).
     * Compare the two snapshots using the **Comparison** view.
  3. **Find the cause**: Sort by **Delta** or **Retainer size** to find objects that were allocated but not released. Look for common leak sources like detached DOM elements, active event listeners, or uncleared timers.
  4. **Trace references**: Inspect the retaining tree at the bottom of the screen to identify which variable or closure reference is keeping the object from being garbage collected.
- **Follow-up Questions**:
  - What are detached DOM elements? (Elements that have been removed from the visible page markup but are still referenced by a JavaScript variable, preventing them from being garbage collected).
  - What is the difference between shallow size and retained size? (Shallow size is the memory held by the object itself; retained size is the total memory released if the object and its dependent references are deleted).
- **Interviewer's Expectations**:
  - Describing the Chrome DevTools Memory profiling workflow.
  - Explaining how to compare heap snapshots to find leaks.
  - Understanding retainer graphs and garbage collection behavior.

#### 19. An asynchronous promise-based function is hung, never resolving or rejecting. How do you debug it?
- **Detailed Answer**:
  *Debugging strategy*:
  1. **Identify the hang**: Look for network requests that remain pending indefinitely, or functions that never trigger their `.then()`, `.catch()`, or `await` resolution blocks.
  2. **Check the Promise executor**: Ensure that the Promise executor function actually calls either the `resolve` or `reject` callback. A common mistake is forgetting to call these in certain logical paths (such as inside `try/catch` blocks):
     ```javascript
     // Hung Promise example
     new Promise((resolve, reject) => {
       database.query((err, res) => {
         if (err) return; // Forgets to call reject(err), hanging the promise on error
         resolve(res);
       });
     });
     ```
  3. **Implement a race timeout**: If you cannot guarantee a third-party dependency will resolve, use `Promise.race` to enforce a timeout limit:
     ```javascript
     function timeout(ms) {
       return new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout")), ms));
     }
     
     // Race the hung task against the timeout timer
     await Promise.race([hungTask(), timeout(5000)]);
     ```
- **Follow-up Questions**:
  - Does a hung promise consume memory? (Yes, the promise holds references to its callbacks and execution context, which can lead to memory leaks if left unresolved).
  - Can you cancel a running promise? (No, promises are not cancelable by default. You can use an `AbortController` to abort the underlying task).
- **Interviewer's Expectations**:
  - Explaining the role of the `resolve` and `reject` callbacks.
  - Spotting missing execution branches in Promise definitions.
  - Implementing timeouts using `Promise.race`.

#### 20. The `this` keyword returns `undefined` inside a callback method. How do you fix it?
- **Detailed Answer**:
  *The Cause*: This error happens because object methods passed as callbacks lose their implicit binding. They are executed as standalone functions, which causes `this` to fall back to the default binding (`undefined` in strict mode):
  ```javascript
  class ButtonHandler {
    constructor() {
      this.clickCount = 0;
    }
    handleClick() {
      this.clickCount++; // Throws TypeError: Cannot read properties of undefined
    }
  }
  
  const handler = new ButtonHandler();
  //handleClick is passed as a callback, losing its connection to the handler instance
  document.getElementById("btn").addEventListener("click", handler.handleClick);
  ```
  
  *Solutions*:
  1. **Use Arrow Functions**: Arrow functions do not bind `this`; they inherit it lexically from their enclosing scope. You can write the method as an arrow function:
     ```javascript
     handleClick = () => {
       this.clickCount++;
     };
     ```
  2. **Bind the method in the constructor**: Explicitly bind `this` to the instance in the constructor:
     ```javascript
     constructor() {
       this.clickCount = 0;
       this.handleClick = this.handleClick.bind(this);
     }
     ```
  3. **Wrap in an inline arrow function**: Pass an inline arrow function to the listener:
     ```javascript
     element.addEventListener("click", () => handler.handleClick());
     ```
- **Follow-up Questions**:
  - What is the performance impact of binding methods in the constructor vs. using arrow functions? (Binding in the constructor is slightly more memory-efficient because the method is shared on the prototype, whereas arrow functions are recreated as instance properties for every new object).
  - Can you rebind a method that has already been bound? (No, calling `.bind()` on an already bound function has no effect).
- **Interviewer's Expectations**:
  - Identifying how passing callbacks causes implicit binding loss.
  - Explaining the difference between lexical arrow functions and explicit binding.
  - Discussing performance and structure tradeoffs of each solution.

---

### System Design Questions

#### 21. Design a client-side state management architecture for a highly interactive Single Page Application.
- **Detailed Answer**:
  A scalable state management architecture uses a unidirectional data flow to keep state updates predictable:
  
  ```text
  View Layer (React) ---> Triggers Action ---> Dispatched to Reducer ---> Mutates Store ---> Notifies View
  ```
  
  *Key design components*:
  1. **Single Source of Truth**: Store all shared state in a centralized, read-only store object.
  2. **Unidirectional Data Flow**: Views trigger actions (objects containing type and payload). Actions are dispatched to pure reducer functions that return a new state object instead of mutating the existing state directly.
  3. **Reactivity & Selectors**: Views subscribe to specific parts of the store using selector functions. This prevents unnecessary re-renders when unrelated parts of the state change.
  4. **Side Effect Middleware**: Use middleware (like Redux Thunk or custom asynchronous handlers) to intercept actions, make API calls, and dispatch secondary actions with the payload.
- **Follow-up Questions**:
  - When should you use local state instead of global state? (Use local state for UI-only states like toggles or inputs; use global state for shared domain data like user authentication or cart contents).
  - How do you optimize store selector performance? (Use memoized selectors to prevent recalculating values unless their input state changes).
- **Interviewer's Expectations**:
  - Designing a unidirectional data flow architecture.
  - Explaining how to prevent unnecessary re-renders.
  - Separating synchronous state mutations from asynchronous side effects.

#### 22. Design the client-side logic for a real-time messaging application.
- **Detailed Answer**:
  A real-time messaging client must manage connection state, message queues, and offline synchronization:
  
  *Key Architectural Components*:
  1. **Connection Manager**: Wraps the native `WebSocket` API to handle connection state, heartbeats to keep the connection alive, and automatic backoff reconnection:
     ```javascript
     class SocketClient {
       connect(url, attempt = 1) {
         this.ws = new WebSocket(url);
         this.ws.onclose = () => {
           // Exponential backoff reconnect
           const delay = Math.min(1000 * Math.pow(2, attempt), 30000);
           setTimeout(() => this.connect(url, attempt + 1), delay);
         };
       }
     }
     ```
  2. **Message Outbox & Queue**: Store outgoing messages in an in-memory queue or persistent storage (like IndexedDB). Send them sequentially and mark them as delivered when the server sends an acknowledgment.
  3. **Incoming Router**: Parses incoming socket messages and routes them to the correct local database updates or UI notifications based on their message type.
  4. **State Sync**: When reconnecting, send the timestamp of the last received message to request missing back-log messages from the server.
- **Follow-up Questions**:
  - How do you handle network connectivity drops? (Use the browser's `navigator.onLine` API and listen to `online` and `offline` events to trigger state changes).
  - How do you prevent blocking the main thread when processing a large batch of incoming history messages? (Offload JSON parsing and database storage tasks to a Web Worker).
- **Interviewer's Expectations**:
  - Implementing reconnect strategies (exponential backoff).
  - Using local message queues to handle temporary network drops.
  - Routing messages cleanly and managing client-server state synchronization.

#### 23. Design an offline-first synchronization strategy for a Progressive Web App (PWA).
- **Detailed Answer**:
  An offline-first PWA uses service workers and local storage to remain functional when disconnected and sync changes once reconnected:
  
  *Architecture Components*:
  1. **Service Worker Caching**: Intercepts fetch requests and implements cache-first or network-first strategies using the Cache Storage API:
     ```javascript
     self.addEventListener("fetch", event => {
       event.respondWith(
         caches.match(event.request).then(cachedResponse => {
           // Return cached asset, falling back to network fetch
           return cachedResponse || fetch(event.request);
         })
       );
     });
     ```
  2. **Local Database (IndexedDB)**: Store user mutations (like editing a task) locally in IndexedDB when offline.
  3. **Background Sync API**: Register a sync tag with the Service Worker to defer tasks until the user has a stable network connection:
     ```javascript
     navigator.serviceWorker.ready.then(reg => {
       return reg.sync.register("sync-outbox");
     });
     ```
  4. **Conflict Resolution**: When syncing back to the server, resolve conflicts using timestamps (e.g., last-write-wins) or prompt the user if there are overlapping changes.
- **Follow-up Questions**:
  - What is the storage limit for IndexedDB? (It varies by browser, but generally up to 50% of the user's free disk space).
  - How do you update a Service Worker? (Register the new script; it installs in the background and transitions to active once all tabs running the old version are closed, or you call `self.skipWaiting()`).
- **Interviewer's Expectations**:
  - Explaining the lifecycle and request interception model of Service Workers.
  - Using IndexedDB for local data storage.
  - Synchronizing offline changes using the Background Sync API.

---

## 10. Common Mistakes

- **Using global variable declarations**: Writing `value = 10` instead of `let value = 10` pollutes the global scope and leads to hard-to-debug side effects.
- **Forgetting to clear event listeners and intervals**: Leading to memory leaks in Single Page Applications when elements are removed from the DOM but their listeners remain in memory.
- **Using loose equality (`==`) instead of strict equality (`===`)**: Leading to unexpected type coercion bugs:
  ```javascript
  0 == ''; // true (unexpected coercion)
  0 === ''; // false (correct strict check)
  ```
- **Confusing arrow function `this`**: Declaring object methods as arrow functions and finding that `this` refers to the global window object instead of the instance.
- **Blocking the main thread**: Running heavy, long-running CPU calculations synchronously instead of breaking them into asynchronous chunks or using Web Workers.

---

## 11. Comparison Section: CommonJS vs. ES Modules

| Feature | CommonJS (CJS) | ES Modules (ESM) |
|---|---|---|
| **Syntax** | `require()` and `module.exports` | `import` and `export` |
| **Loading Mode** | Synchronous (Blocking runtime loads) | Asynchronous (Static compile-time analysis) |
| **Tree-Shaking Support** | Poor (Hard to optimize dynamic imports) | Excellent (Enables compile-time optimizations) |
| **Live Bindings** | No (Exports copied values) | Yes (Exports read-only live references) |
| **Runtime Context** | Includes variables like `__dirname`, `__filename` | Needs `import.meta.url` to calculate paths |
| **Platform Defaults** | Node.js (Legacy default configuration) | Modern Browsers and modern Node.js configurations |

---

## 12. Practical Project Ideas

### Beginner Project: Collaborative Board with Event Delegation
Build a canvas board application where users can place and edit interactive stickers. Must use a single event listener on the board container (Event Delegation) to handle clicks on individual stickers, and persist the layout state using LocalStorage.

### Intermediate Project: Debounced Autocomplete Input Search
Build a search input component that makes API requests as the user types. Must include debouncing to limit API requests, an `AbortController` to cancel pending requests if a new query is typed, and an in-memory cache with expiration (TTL) to store and reuse previous search results.

### Advanced Project: Asynchronous Task Runner with Concurrency Limits
Design a command-line script runner that executes a queue of asynchronous tasks (e.g., file downloads or API calls). The runner must accept a configuration parameter limiting the maximum number of tasks that can run concurrently, and generate a final report detailing the execution time and outcome of each task.

---

## 13. Internship Preparation Notes

- **Trace event loop exercises**: Practice tracing the exact output order of complex mixtures of synchronous code, promises (`microtasks`), and timers (`macrotasks`).
- **Implement utility functions from scratch**: Be prepared to write functions like `debounce`, `throttle`, `deepClone`, and promise wrappers on whiteboards without third-party libraries.
- **DOM performance optimization**: Understand the difference between reflows and repaints, and practice using event delegation and `DocumentFragment` to batch DOM updates.
- **Memory profiling practice**: Practice using Chrome DevTools to take heap snapshots, find detached DOM elements, and diagnose memory leaks.

---

## 14. Cheat Sheet

```javascript
/* Standard Specificity Order for 'this' Resolution */
// 1. New Binding: constructor instance
// 2. Explicit Binding: call/apply/bind
// 3. Implicit Binding: parent object context
// 4. Default Binding: window / undefined (strict)

/* Standard Microtask vs Macrotask Event Loop Order */
// Call Stack Empty -> Run All Microtasks -> Render UI -> Run One Macrotask

/* Quick Promise Orchestration Reference */
Promise.all([p1, p2]);       // Fails early if ANY reject
Promise.allSettled([p1, p2]);// Returns results and statuses for all (never rejects)
Promise.race([p1, p2]);      // Settles as soon as the FIRST promise settles
Promise.any([p1, p2]);       // Resolves as soon as the FIRST promise resolves

/* Cancel Fetch requests using AbortController */
const controller = new AbortController();
fetch(url, { signal: controller.signal });
controller.abort(); // Cancels the request immediately
```

---

## 15. One-Day Revision Guide

- [ ] Explain the differences in scope and hosting between `var`, `let`, and `const`.
- [ ] Trace the event loop execution order for a code sample containing `setTimeout` and `Promise.resolve().then()`.
- [ ] Write a custom debounce helper function from scratch.
- [ ] Implement prototype inheritance between two constructor functions.
- [ ] Demonstrate how to identify detached DOM nodes and memory leaks using Chrome DevTools.
- [ ] Describe the differences in loading and parsing between CommonJS and ES Modules.
