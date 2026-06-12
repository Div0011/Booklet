# 36. React (Component Architecture & Virtual DOM)

## 1. Introduction

### What it is
React is an open-source, component-based frontend JavaScript library used for building dynamic user interfaces. It focuses on the view layer of web applications, utilizing a declarative programming model to describe how user interfaces should look based on application state.

### Why it exists
In early web design, developers used direct JavaScript commands (like `document.getElementById` or jQuery) to manipulate the DOM tree. When applications scaled, keeping the user interface in sync with application data led to complex codebases. Manual DOM manipulation is also slow, triggering page-wide layout recalculations (Reflows). Facebook created React in 2013 to introduce a Virtual DOM, component encapsulation, and automated interface updates.

### Problems it solves
- **Performance Overhead**: Minimizes direct DOM manipulations by diffing changes in memory first.
- **Complex UI States**: Automates rendering updates. Developers update the data state, and React handles rendering the layout.
- **Monolithic Layouts**: Breaks complex interfaces into small, self-contained, and reusable **Components**.

### Industry Use Cases
- **Single Page Applications (SPAs)**: Building dynamic interfaces for platforms like Facebook, Netflix, and Airbnb.
- **SaaS Dashboards**: Creating interactive data dashboards that update layout modules in real-time.
- **Cross-Platform Mobile Apps**: Using React Native to compile React components into native iOS and Android modules.

---

## 2. Core Concepts

### Beginner Concepts
- **Declarative Components**: Instead of writing instructions to modify elements, developers declare how the UI should look for a given state:
  ```jsx
  const UserGreeting = ({ name }) => <h1>Hello, {name}!</h1>;
  ```
- **JSX (JavaScript XML)**: A syntax extension that allows writing HTML-like markup directly inside JavaScript files. Transpiled to standard `React.createElement()` calls.
- **Props vs. State**:
  - **Props**: Read-only configuration inputs passed down from parent to child components. Immutable within the child.
  - **State**: Mutable local memory owned and managed internally by the component. Updating state triggers a component re-render.

### Intermediate Concepts
- **React Hooks**: Functions that allow functional components to access state and lifecycle features:
  - `useState`: Declares a state variable and setter.
  - `useEffect`: Manages side-effects (fetching data, setting timers, manual DOM updates). Runs after layout rendering.
  - `useRef`: Creates a persistent reference object. Its `.current` property stays mutable across renders without triggering a re-render.
- **Lists and Keys**: When rendering array items, React requires a unique `key` prop for each item. This helps React identify which items changed, were added, or were removed, optimizing list rendering.

### Advanced Concepts
- **Context API**: Provides a way to share state variables globally across the component tree, avoiding the need to pass props through intermediate levels (Prop Drilling).
- **Custom Hooks**: Functions that extract and package stateful hook logic, allowing it to be reused across different components:
  ```javascript
  function useWindowWidth() {
      const [width, setWidth] = useState(window.innerWidth);
      useEffect(() => {
          const handleResize = () => setWidth(window.innerWidth);
          window.addEventListener('resize', handleResize);
          return () => window.removeEventListener('resize', handleResize);
      }, []);
      return width;
  }
  ```
- **Performance Optimization Hooks**:
  - `useMemo`: Caches (memoizes) the computed result of an expensive calculation.
  - `useCallback`: Caches a function definition instance, preventing unnecessary child re-renders when passed as a prop.

---

## 3. Internal Working

### Virtual DOM, Reconciliation, and the Fiber Engine

React keeps the browser responsive by managing updates inside a virtual representation of the DOM:

```text
[ State/Props Update ] -> Trigger Re-render -> [ Generate New Virtual DOM Tree ]
                                                      |
  +------------------ Reconciliation Phase -----------v--------------------+
  |                                                                        |
  |  Compare New Virtual DOM with Old Virtual DOM (Diffing Algorithm)      |
  |  Rules:                                                                |
  |    1. Elements of different types generate completely new subtrees.    |
  |    2. Elements with matching keys are matched and updated in place.    |
  |                                                                        |
  |  Fiber Reconciler: Splits diffing work into small incremental fibers   |
  |                    that yield back execution to main browser thread    |
  +------------------------------------------------------------------------+
                                       |
                                       v
[ Commit Phase ] -> Batch updates -> Write changes to Real DOM (Paint pixels)
```

1. **The Virtual DOM (VDOM)**:
   - A lightweight JavaScript object representation of the real DOM tree.
   - When a component's state updates, a new VDOM tree is generated.
2. **Reconciliation and the Diffing Algorithm**:
   - React compares the new VDOM tree with the previous VDOM tree using a heuristic diffing algorithm that runs in $\mathcal{O}(N)$ time based on two assumptions:
     - **Different element types**: If elements have different types (e.g. changing `<div>` to `<span>`), React tears down the old tree and builds a new one from scratch.
     - **Keys for matching lists**: Keys allow React to match children in the original tree with children in the new tree. If an array is sorted, React matches elements by key and moves them, rather than re-rendering every item.
3. **The React Fiber Engine**:
   - Older versions of React (before version 16) used a synchronous stack reconciler that processed updates in a single block, blocking the browser's main thread during heavy updates.
   - **Fiber** introduced incremental rendering. It breaks reconciliation work into small units of work called "fibers".
   - It schedules updates based on priority. High-priority tasks (like user typing or animations) can pause lower-priority reconciliations (like rendering a list in the background), keeping the interface responsive.
4. **Render and Commit Phases**:
   - **Render Phase**: Runs calculations to diff the virtual trees. This phase can be paused and restarted by the Fiber engine.
   - **Commit Phase**: Writes the computed changes directly to the real DOM. This phase runs synchronously to prevent visual inconsistencies.

---

## 4. Important Terminology

- **Virtual DOM**: An in-memory JavaScript representation of the real DOM.
- **Reconciliation**: The process of diffing two virtual DOM trees and updating only the differences in the real DOM.
- **Fiber**: React's core reconciliation engine that enables incremental, priority-based updates.
- **Prop Drilling**: Passing props down through multiple layers of components to reach a deeply nested child component.
- **Stale Closure**: A behavior where a hook captures variables from its parent scope at render time, remaining locked into outdated values if dependencies are missing.

---

## 5. Beginner Examples

### Example 1: Count Component with State Lifecycle
This example demonstrates state management, batching updates, and hook triggers.

```jsx
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    const handleIncrement = () => {
        // State updates are batched:
        setCount(count + 1);
        setCount(count + 1);
        // Both calls reference the same 'count' value in this render,
        // resulting in incrementing by 1, not 2.
        
        // Correct way to queue updates based on prior state:
        // setCount(prevCount => prevCount + 1);
    };

    return (
        <div class="counter-box">
            <p>Current Count: {count}</p>
            <button onClick={handleIncrement}>Increment</button>
        </div>
    );
}
```

---

## 6. Intermediate Examples

### Example 1: Custom Hooks to Fetch Async API Data
This example implements a reusable `useFetch` hook to fetch data asynchronously, including loading and error states.

```javascript
import { useState, useEffect } from 'react';

function useFetch(url) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        let isMounted = true; // Prevents updating state if component unmounts
        setLoading(true);

        fetch(url)
            .then(res => {
                if (!res.ok) throw new Error("Network request failed");
                return res.json();
            })
            .then(json => {
                if (isMounted) {
                    setData(json);
                    setLoading(false);
                }
            })
            .catch(err => {
                if (isMounted) {
                    setError(err.message);
                    setLoading(false);
                }
            });

        // Cleanup function runs when component unmounts or URL changes
        return () => {
            isMounted = false;
        };
    }, [url]); // Dependency array: Runs fetch only when URL updates

    return { data, loading, error };
}
```

---

## 7. Advanced Concepts

### Deep Hook Lifecycle Analysis and State Staleness

#### Stale Closures in `useEffect`
A stale closure occurs when a hook closure references state variables from an older render cycle.

```jsx
import React, { useState, useEffect } from 'react';

function Timer() {
    const [count, setCount] = useState(0);

    useEffect(() => {
        const interval = setInterval(() => {
            // BUG: 'count' is captured once when the effect runs.
            // Since the dependency array is empty, the interval callback
            // always references count as 0, logging 'Interval count: 1' every second.
            console.log("Interval count:", count + 1);
            setCount(count + 1);
        }, 1000);

        return () => clearInterval(interval);
    }, []); // Missing 'count' dependency

    // FIX 1: Add [count] to dependencies (resets the interval on every increment).
    // FIX 2: Use functional updates: setCount(prev => prev + 1) (recommended).

    return <h1>Timer Count: {count}</h1>;
}
```

#### Optimizing Re-renders with `React.memo` and `useCallback`
By default, when a parent component updates its state, all of its child components re-render, even if their props have not changed. We can optimize this behavior:

```jsx
import React, { useState, useCallback } from 'react';

// Wrap child component in React.memo to skip re-renders if props are identical
const ListButton = React.memo(({ onClick }) => {
    console.log("ListButton rendered");
    return <button onClick={onClick}>Click me</button>;
});

function ParentContainer() {
    const [count, setCount] = useState(0);
    const [text, setText] = useState("");

    // useCallback prevents re-instantiating the function on every render,
    // keeping the prop reference stable for ListButton.
    const handleButtonClick = useCallback(() => {
        setCount(prev => prev + 1);
    }, []); // Empty dependencies: Function instance is cached permanently

    return (
        <div>
            <input value={text} onChange={(e) => setText(e.target.value)} />
            <p>Count: {count}</p>
            <ListButton onClick={handleButtonClick} />
        </div>
    );
}
```

### React 19 Architecture and API Additions
React 19 introduces major upgrades to data flow, async states, rendering optimizations, and resource loading.

* **The React Compiler (React Forget)**: A build-time compiler that automatically memoizes components, props, and dependency arrays. It eliminates the need for manual `useMemo` and `useCallback` optimization boilerplate by analyzing code and injecting memoization caches where safe.
* **Server Actions**: Native support for invoking server-side functions directly from client components during form submissions or events, abstracting network request boilerplate.
* **`useActionState` Hook**: Replaces `useFormStatus` and manual pending states. It tracks the status of async form submissions, returning the form's state (data/errors) and a `isPending` flag.
* **`useOptimistic` Hook**: Enables optimistic UI updates, rendering the expected final state immediately during async operations and automatically rolling back if the operation fails.
* **`use` API**: A new runtime API that allows reading Promises or Context inline within rendering loops, conditional blocks, and loops (unlike standard hooks).

#### Code Example: React 19 Form Submission with Async States
This example demonstrates a client form using Server Actions, `useActionState` for pending states, `useOptimistic` for instant list updates, and the `use` API to read profile context.

```jsx
import { use, useActionState, useOptimistic, useRef } from 'react';
import { ThemeContext } from './ThemeContext';

// Server Action simulation (runs on server, called from client)
async function updateUsernameOnServer(newUsername: string) {
  // Simulate network latency
  await new Promise(resolve => setTimeout(resolve, 1000));
  if (newUsername.toLowerCase() === "admin") {
    throw new Error("Username 'admin' is reserved!");
  }
  return newUsername;
}

export function UsernameForm({ currentUsername }) {
  // 1. Read context dynamically using the 'use' API (can be used inside conditionals)
  const theme = use(ThemeContext); 
  const formRef = useRef(null);

  // 2. Optimistic state management
  const [optimisticName, setOptimisticName] = useOptimistic(
    currentUsername,
    (state, newName) => newName // Instantly update to new value during action execution
  );

  // 3. Form Action State hook for pending status and error tracking
  const [state, formAction, isPending] = useActionState(
    async (prevState, formData) => {
      const newName = formData.get("username");
      
      // Instantly trigger optimistic UI update
      setOptimisticName(newName);
      
      try {
        const savedName = await updateUsernameOnServer(newName);
        formRef.current?.reset();
        return { success: true, username: savedName, error: null };
      } catch (err) {
        // Automatically rolls back optimisticName to currentUsername
        return { success: false, username: prevState.username, error: err.message };
      }
    },
    { success: false, username: currentUsername, error: null }
  );

  return (
    <form ref={formRef} action={formAction} style={{ color: theme.color }}>
      <label>Current: {optimisticName}</label>
      <input type="text" name="username" disabled={isPending} />
      
      <button type="submit" disabled={isPending}>
        {isPending ? "Saving..." : "Update"}
      </button>

      {state.error && <p style={{ color: 'red' }}>{state.error}</p>}
    </form>
  );
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate your mental model of React's rendering flow. They look at how you manage rendering performance, whether you understand state batching and stale closures, and how you resolve prop-drilling without over-engineering layout wrappers.

### Red Flags
- **Mutating State Variables**: Mutating state values directly (e.g. `state.user = "new"`) instead of using setter functions. This prevents React from detecting changes, failing to trigger re-renders.
- **Using Array Indices as Keys**: Defaulting to array indices (`key={index}`) for dynamic lists. If the list is sorted, filtered, or shuffled, this can cause rendering bugs and performance issues.
- **Micro-optimizing with Hooks**: Wrapping simple functions in `useCallback` when they have no impact on child component rendering. This adds memory overhead.

### Green Flags
- **Functional State Updates**: Writing state setters using prior state functions (`setCount(prev => prev + 1)`) to avoid stale state bugs.
- **Cleanup Functions**: Cleaning up event listeners, API requests, and intervals inside effect return blocks.
- **Custom Hook Modularity**: Moving data fetching and logic out of components and into reusable custom hooks.

### Answers Matrix

| Level | Question: "Why shouldn't you call Hooks inside loops or conditions?" |
|---|---|
| **Rejected** | "Because React gets confused if you put hooks inside conditional blocks." |
| **Shortlisted** | "React requires hooks to run in the same order on every render so it can map state values correctly." |
| **Selected** | "React manages component state internally using an array. Every time a hook is called, React stores its state metadata sequentially. During re-renders, React relies on the call order remaining identical to map the states back to their corresponding hooks. If we wrap a hook in a conditional block, the call sequence can shift. This causes subsequent hooks to read incorrect state references, leading to runtime bugs." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is React Reconciliation and how does the diffing algorithm optimize updates?
- **Detailed Answer**: Reconciliation is the algorithm React uses to diff the virtual DOM trees and determine which updates need to be applied to the real DOM.
  - Doing a full tree comparison has an algorithmic complexity of $\mathcal{O}(N^3)$, which is too slow. React uses a heuristic diffing algorithm that runs in $\mathcal{O}(N)$ based on two rules:
    1. **Element types**: If two elements have different types (e.g. changing `<div>` to `<section>`), React destroys the old tree and builds the new one.
    2. **Unique keys**: Using unique `key` props on list elements allows React to track items across renders, avoiding unnecessary re-renders when items are reordered.
- **Follow-up Questions**: What happens if you do not provide a key in a list? (Answer: React defaults to using the index as the key, which can cause state bugs if items are reordered).
- **Interviewer's Expectations**: Explain the $\mathcal{O}(N)$ complexity simplification and the role of element types and keys.

#### 2. What is the difference between `useEffect` and `useLayoutEffect`?
- **Detailed Answer**:
  - **`useEffect`**: Runs asynchronously after the render and commit phases, after the browser has painted the pixels on screen. This prevents blocking page paint operations, making it ideal for standard side effects like data fetching.
  - **`useLayoutEffect`**: Runs synchronously after DOM changes are committed, but before the browser paints the pixels on screen. This allows reading DOM layout geometry (like calculating element heights) and making immediate updates before the user sees them, preventing layout flicker.
- **Follow-up Questions**: Why is `useEffect` preferred for data fetching? (Answer: Because it does not block browser painting, keeping the interface responsive).
- **Interviewer's Expectations**: Differentiate timing behaviors relative to browser paint cycles.

---

### Scenario-Based Questions

#### 3. You are rendering a large list of search results. Typing in the search field causes the input to lag. How do you optimize this?
- **Detailed Answer**:
  - **Virtualization**: Use libraries like React Window to render only the visible items in the viewport, reducing DOM nodes.
  - **Debouncing**: Debounce the input state update so search filtering only runs after the user stops typing.
  - **Interruptible Rendering**: Use React 18's `useTransition` to mark the search list update as a lower priority, keeping the input input responsive.
- **Follow-up Questions**: Why does rendering too many DOM nodes slow down the browser? (Answer: It increases memory footprint and slows down layout calculations).
- **Interviewer's Expectations**: Propose component virtualization, debouncing, or React 18 transition hooks.

#### 4. How do you implement a theme state wrapper using Context API without causing unnecessary re-renders across all child components?
- **Detailed Answer**: We wrap the theme values inside context providers. To optimize re-renders:
  1. Split the context into two: `ThemeStateContext` (stores values) and `ThemeDispatchContext` (stores update functions). This prevents components that only need the update function from re-rendering when the theme state changes.
  2. Memoize the context values using `useMemo`:
     ```jsx
     const themeValue = useMemo(() => ({ theme }), [theme]);
     ```
  3. Wrap child components in `React.memo`.
- **Follow-up Questions**: How does Redux or Zustand prevent the context re-rendering issue? (Answer: They use selector-based subscriptions, notifying components to re-render only when the selected slices of state change).
- **Interviewer's Expectations**: Highlight value memoization and context splitting techniques.

---

### Debugging Questions

#### 5. Debug the following code where state changes are ignored during successive calls:
```jsx
const [user, setUser] = useState({ name: "Alex", role: "Developer" });
const updateRole = () => {
    user.role = "Lead Developer"; // Mutating state directly
    setUser(user);                // Passing same reference pointer
};
```
- **Detailed Answer**: React detects state changes by comparing reference pointers using strict equality (`Object.is`). Because `user.role` was mutated directly, the object reference did not change. Calling `setUser(user)` passes the same object reference, so React assumes no changes occurred and skips re-rendering.
- **Fix**: Clone the object using the spread operator to create a new reference pointer:
  ```javascript
  const updateRole = () => {
      setUser({ ...user, role: "Lead Developer" });
  };
  ```
- **Follow-up Questions**: Why does React use shallow comparison instead of deep checking? (Answer: Deep comparison of nested structures is computationally expensive, slowing down state updates).
- **Interviewer's Expectations**: Explain object reference comparison and how to clone structures.

---

### System Design Questions

#### 6. Design a secure client authentication state wrapper in React.
- **Detailed Answer**:
  - We create an `AuthProvider` containing the user state.
  - The authentication state is stored in memory to prevent XSS attacks. The JSON Web Token (JWT) is stored in a secure, `httpOnly` cookie.
  - We export a custom `useAuth` hook:
    ```javascript
    export const useAuth = () => useContext(AuthContext);
    ```
  - We implement routing guards (e.g. `<ProtectedRoute>`) that redirect unauthenticated users to a login page.
- **Follow-up Questions**: How do you prevent layout shift when checking if a user is logged in on page load? (Answer: Render a loading skeleton until the token validation call resolves).
- **Interviewer's Expectations**: Cover state storage, hook routing guards, and token validation.

---

### Real Interview Questions

#### 7. Why do we write `super(props)` inside React class component constructors?
- **Detailed Answer**: Calling `super(props)` invokes the constructor of the parent class (`React.Component`). This initializes the component and allows accessing `this.props` inside the constructor. If you omit `super(props)`, `this` will be uninitialized, causing a ReferenceError.
- **Follow-up Questions**: Why is this step not necessary in functional components? (Answer: Functional components receive props directly as function arguments instead of utilizing class constructors).
- **Interviewer's Expectations**: Describe class inheritance and parent constructor initialization.

---

## 10. Common Mistakes

- **Storing computed values in state**: Storing values that can be derived from existing state. This forces redundant state management (e.g. storing `fullName` when `firstName` and `lastName` are already in state).
- **Infinite Effect Loops**: Running `useEffect` without specifying dependencies, or updating state inside the effect without omitting it from the dependency array, causing infinite render loops.
- **Index Key Bindings**: Using loop index keys on sorted lists, causing state misalignment across child inputs.

---

## 11. Comparison Section: React Hook Performance Choices

| Hook / Pattern | Purpose | When to use | Performance Overhead |
|---|---|---|---|
| **`useState`** | Manages component state. | For values that trigger layout updates. | Low |
| **`useRef`** | Stores persistent mutable references. | For DOM queries and caching variables without re-renders. | Extremely Low |
| **`useMemo`** | Memoizes computed values. | When recalculating values is expensive (e.g. filtering large lists). | Adds overhead for simple calculations. |
| **`useCallback`** | Memoizes callback functions. | When passing callbacks to memoized child components (`React.memo`). | Adds initialization overhead. |

---

## 12. Practical Project Ideas

### Beginner
- **Dynamic Shopping Cart**: A shopping cart interface where users can add, increment, and remove items, with quantities and total costs calculated dynamically.

### Intermediate
- **Filtered Search Dashboard**: Build a dashboard with search and category filters that queries large datasets, using `useMemo` to optimize searches and custom hooks for API calls.

### Advanced/Resume-worthy
- **Draggable Kanban Board**: Build a Kanban board from scratch without external libraries. Implement custom drag-and-drop events, manage state transitions, and optimize element movement.

---

## 13. Internship Preparation Notes

- **Recruiters focus on**: Component structures, simple hooks (`useState`, `useEffect`), and prop passing.
- **Product Companies Expect**: Deep understanding of rendering lifecycles, custom hook modularity, state immutability, and lists key reconciliations.
- **Key optimizations**: Be ready to explain when *not* to use `useMemo`/`useCallback` (e.g. avoiding unnecessary optimizations).

---

## 14. Cheat Sheet

- **Functional State Update**:
  ```javascript
  setVal(prev => prev + 1);
  ```
- **Cleanup Template**:
  ```javascript
  useEffect(() => {
      const sub = api.subscribe();
      return () => sub.unsubscribe(); // Cleanup callback
  }, []);
  ```
- **Context Creation**:
  ```javascript
  const MyCtx = React.createContext(null);
  ```
- **Reference Binding**: `<div ref={myRef}></div>`

---

## 15. One-Day Revision Guide

- [ ] Explain why mutating state variables directly fails to trigger re-renders.
- [ ] Understand why React requires unique keys on list elements.
- [ ] Describe the rendering stages of the VDOM and the Fiber engine.
- [ ] Debug a stale closure in a useEffect timer hook.
- [ ] Explain when to use `React.memo` to optimize child component rendering.
