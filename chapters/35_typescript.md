# 35. TypeScript (Typed JavaScript)

## 1. Introduction

### What it is
TypeScript is an open-source, statically typed superset of JavaScript developed by Microsoft. It layers a static type system over JavaScript's dynamic runtime behavior. Every valid JavaScript program is syntactically valid TypeScript, but TypeScript introduces static compile-time checking to catch errors before code is run. Once compiled via the TypeScript compiler (`tsc`), all type annotations, interfaces, and generic declarations are stripped away (type erasure), producing plain, standard JavaScript compatible with any browser or Node.js runtime.

### Why it exists
JavaScript is dynamically typed, meaning variables can hold any value type, and types are resolved at runtime. While this allows for rapid prototyping, it becomes difficult to maintain in large codebases. Typos in property names, passing invalid arguments to functions, or calling methods on `undefined` values can only be detected when the code is executed. TypeScript exists to address these problems by introducing static type checking, bringing compiler-level validation to JavaScript development.

### Problems it solves
- **Catching bugs early**: Detects type mismatches, missing parameters, and typos during compilation.
- **API documentation**: Function signatures and object layouts serve as self-documenting code contracts.
- **Safe refactoring**: Renaming properties or modifying function signatures automatically updates or flags all references across the codebase.
- **Null and Undefined protection**: Prevents the common "Cannot read properties of undefined" error when strict checking is enabled.
- **Enhanced developer tooling**: Enables autocomplete, parameter info, and code navigation in modern IDEs.

### Industry Use Cases
- **Enterprise Applications**: Powering large-scale React, Angular, and Next.js frontend codebases.
- **Server-Side APIs**: Building structured backend services using Nest.js or Express with TypeORM/Prisma.
- **Component and SDK Libraries**: Developing open-source packages where developers need accurate type definitions.
- **Monorepos**: Maintaining shared type definitions across frontend applications and backend APIs.

### Analogy
JavaScript is like driving a car on an open road without lanes or signposts—you can go anywhere quickly, but you are more likely to run into unexpected obstacles. TypeScript is like adding lane markers, traffic signs, and GPS navigation to that road. It doesn't change how the car drives, but it guides you safely to your destination.

---

## 2. Core Concepts

### Beginner Concepts
- **Type Annotations**: Explicitly declaring variable types using the colon syntax (e.g., `let count: number = 0`).
- **Primitive Types**: Basic JavaScript types mapped to TypeScript types: `string`, `number`, `boolean`, `null`, `undefined`, `symbol`, and `bigint`.
- **Objects and Arrays**: Defining structures for arrays (`number[]` or `Array<number>`) and objects using type aliases or interfaces.
- **Tuples**: Fixed-length arrays where each element has a predefined type (e.g., `[string, number]`).
- **Union Types**: Allowing a value to be one of several types (e.g., `string | number`).
- **Type Inference**: The compiler automatically infers types based on initialization values when explicit types are omitted.

### Intermediate Concepts
- **Interfaces vs. Type Aliases**: Both define object shapes, but interfaces support declaration merging (appending properties to existing interfaces) and extending other shapes, while type aliases can define unions, intersections, and primitives.
- **Generics**: Reusable, parameterized types that allow functions, classes, and interfaces to adapt dynamically to different types while preserving type safety (e.g., `function identity<T>(arg: T): T`).
- **Utility Types**: Built-in helper types to transform existing types, such as `Partial<T>`, `Required<T>`, `Readonly<T>`, `Pick<T, K>`, `Omit<T, K>`, and `Record<K, T>`.
- **Type Guards and Narrowing**: Using runtime checks like `typeof`, `instanceof`, the `in` operator, or custom type predicate functions (`value is Type`) to narrow down union types.
- **Discriminated Unions**: Creating a union of object types that share a literal property (the discriminator) used to safely distinguish between them.
- **Enums**: Numeric or string enums to define a set of named constants.

### Advanced Concepts
- **Conditional Types**: Defining types conditionally based on type relationships using a ternary structure (e.g., `T extends U ? X : Y`).
- **Mapped Types**: Creating new types by iterating over properties of an existing type (e.g., `{ [K in keyof T]: T[K] }`).
- **Template Literal Types**: Combining type-level string union values to construct new string types dynamically.
- **The `satisfies` Operator**: Validates that an object matches a specific type without widening its type inference, preserving precise literal property definitions.
- **`infer` Keyword**: Extracting types inside conditional type constraints (e.g., extracting the return type of a function).
- **Declaration Files (`.d.ts`)**: Files that contain only type declarations, used to provide typings for raw JavaScript libraries.

---

## 3. Internal Working

### The Compilation and Type Checking Pipeline
TypeScript uses a separate parser and type checker:

```text
.ts Source Code ---> AST Parser ---> Abstract Syntax Tree (AST)
                                              |
                                              v
Compilation JS Output <--- Emitter <--- Type Checker (Structural)
```

1. **AST Parsing**: The compiler parses the `.ts` source file into an Abstract Syntax Tree.
2. **Type Checking**: The Type Checker analyzes the AST, checking variable declarations and function calls against typing rules using structural assignment rules.
3. **Diagnostics**: If any typing rules are violated, compile errors are reported.
4. **Code Generation**: The Emitter strips out all type annotations, interfaces, and generics, outputting standard, plain JavaScript code. Types are completely removed and do not exist at runtime.

### Nominal vs. Structural Typing
Unlike languages like Java or C# which use nominal typing (where types are matched by their class names), TypeScript uses **Structural Typing** (often compared to static duck typing). Two types are considered compatible if they share the same structure, regardless of their declared names:

```typescript
class Point2D {
  x: number = 0;
  y: number = 0;
}

class Vector2D {
  x: number = 0;
  y: number = 0;
}

// Allowed because Point2D and Vector2D share the same properties (structure)
const pt: Point2D = new Vector2D();
```

If the target type requires properties `x` and `y`, any object that has those properties with compatible types is accepted.

---

## 4. Important Terminology

- **Type Erasure**: The compilation step where TypeScript-specific syntax (types, interfaces) is stripped out, leaving only JavaScript code.
- **Structural Typing**: A typing system where type compatibility is determined by the shape and properties of the type, rather than its name.
- **Discriminated Union**: A union of objects that each contain a common, literal discriminator property used to narrow down the union.
- **Type Guard**: An expression or helper function that performs runtime validation to narrow down a union type to a specific type.
- **Type Widening**: The process where the compiler assigns a broader type (like `string`) to a literal value (like `"hello"`) to allow for future reassignments.
- **Utility Type**: A pre-configured type mapper provided by TypeScript to transform types.
- **tsconfig.json**: The configuration file that defines compiler flags, module systems, source folders, and type safety rules.

---

## 5. Beginner Examples

### Example 1: Basic Types, Interfaces, and Functions
```typescript
interface UserProfile {
  readonly id: string; // Cannot be modified after initialization
  username: string;
  email: string;
  avatarUrl?: string; // Optional property
}

function formatUserProfile(user: UserProfile): string {
  const avatar = user.avatarUrl ?? "default-avatar.png";
  return `User: ${user.username} (${user.email}) - Avatar: ${avatar}`;
}

const activeUser: UserProfile = {
  id: "usr_902",
  username: "code_ninja",
  email: "ninja@dev.io"
};

// activeUser.id = "new_id"; // Error: Cannot assign to 'id' because it is a read-only property
```

### Example 2: Union Types and Type Narrowing
Using `typeof` and `instanceof` to safely narrow down union types.

```typescript
type Identifier = string | number;

function printId(id: Identifier) {
  if (typeof id === "string") {
    // Narrowed to string type; string methods are safe to call
    console.log(`String ID: ${id.toUpperCase()}`);
  } else {
    // Narrowed to number type; number methods are safe to call
    console.log(`Numeric ID: ${id.toFixed(0)}`);
  }
}

class ErrorReporter {
  report() { return "System error detected"; }
}

function processInput(input: string | ErrorReporter) {
  if (input instanceof ErrorReporter) {
    // Narrowed to ErrorReporter instance
    console.log(input.report());
  } else {
    // Narrowed to string
    console.log(input.trim());
  }
}
```

### Example 3: Type Aliases vs. Interfaces
```typescript
// Type Alias: Can define unions, intersections, and primitives
type Status = "idle" | "loading" | "success" | "error";
type Position = { x: number; y: number };
type UniqueID = string;

// Interface: Defines object shapes and supports declaration merging
interface WindowSettings {
  width: number;
}
interface WindowSettings {
  height: number; // Declaration merging: appends height to the WindowSettings interface
}

const windowConfig: WindowSettings = {
  width: 800,
  height: 600
};
```

---

## 6. Intermediate Examples

### Example 1: Generics for Type-Safe Containers
Generics let you write reusable containers that preserve type information.

```typescript
class APIResponseWrapper<T> {
  data: T;
  status: number;
  timestamp: Date;

  constructor(data: T, status: number) {
    this.data = data;
    this.status = status;
    this.timestamp = new Date();
  }
}

interface User {
  id: number;
  name: string;
}

// Data is typed as User
const userResponse = new APIResponseWrapper<User>({ id: 1, name: "Alice" }, 200);
console.log(userResponse.data.name); // Type-safe: Alice

// Data is typed as string[]
const tagsResponse = new APIResponseWrapper<string[]>(["typescript", "programming"], 200);
console.log(tagsResponse.data.map(t => t.toUpperCase()));
```

### Example 2: Discriminated Unions for State Management
Using discriminated unions to manage async operation states safely.

```typescript
interface FetchIdleState {
  status: "idle";
}

interface FetchLoadingState {
  status: "loading";
}

interface FetchSuccessState {
  status: "success";
  payload: string[];
}

interface FetchErrorState {
  status: "error";
  errorMessage: string;
}

type FetchState = FetchIdleState | FetchLoadingState | FetchSuccessState | FetchErrorState;

function renderUI(state: FetchState): string {
  switch (state.status) {
    case "idle":
      return "Ready to load data.";
    case "loading":
      return "Loading components...";
    case "success":
      // Safe to access payload; inferred as string[]
      return `Loaded ${state.payload.length} items successfully.`;
    case "error":
      // Safe to access errorMessage
      return `Failed to fetch: ${state.errorMessage}`;
    default:
      // Exhaustiveness check: ensures all states are handled in the switch
      const _exhaustiveCheck: never = state;
      return _exhaustiveCheck;
  }
}
```

### Example 3: Transforming Shapes using Utility Types
```typescript
interface Task {
  id: string;
  title: string;
  completed: boolean;
  priority: "low" | "high";
}

// 1. Partial: Makes all properties optional
type TaskUpdatePayload = Partial<Task>;

// 2. Pick: Selects specific properties
type TaskSummary = Pick<Task, "title" | "completed">;

// 3. Omit: Removes specific properties
type UnidentifiedTask = Omit<Task, "id">;

// 4. Record: Defines a dictionary structure
type ProjectBacklog = Record<string, Task[]>;
```

---

## 7. Advanced Concepts

### Mapped and Conditional Types
Creating dynamic, type-safe structures by iterating over property keys and evaluating conditions.

```typescript
// Mapped Type: Transforms all properties to be read-only and nullable
type NullableReadonly<T> = {
  readonly [K in keyof T]: T[K] | null;
};

interface Profile {
  name: string;
  age: number;
}

type CustomProfile = NullableReadonly<Profile>;
// Equivalent to:
// type CustomProfile = {
//   readonly name: string | null;
//   readonly age: number | null;
// }

// Conditional Type: Evaluates type relationships
type IsString<T> = T extends string ? true : false;
type A = IsString<string>; // true
type B = IsString<number>; // false

// extracting function return types using conditional infer
type UnpackPromise<T> = T extends Promise<infer U> ? U : T;
type ResolvedData = UnpackPromise<Promise<string>>; // string
```

### Type-Safe Mapped String Events
Using template literal types to build dynamic, type-safe event handler interfaces.

```typescript
type UIEventName = "click" | "hover" | "submit";
type UIEventHandlerName = `on${Capitalize<UIEventName>}`; // "onClick" | "onHover" | "onSubmit"

type EventListeners = {
  [K in UIEventHandlerName]: (eventData: any) => void;
};

const pageListeners: EventListeners = {
  onClick: (e) => console.log("Clicked", e),
  onHover: (e) => console.log("Hovered", e),
  onSubmit: (e) => console.log("Submitted", e)
};
```

### Type Assertions and the `satisfies` Operator
The `satisfies` operator validates that an object matches a type while preserving the object's precise literal property types.

```typescript
type RGBColor = [number, number, number];
type ColorValue = string | RGBColor;

const palette = {
  primary: "#3b82f6",
  secondary: [239, 68, 68] as RGBColor,
  accent: "purple"
} satisfies Record<string, ColorValue>;

// Without satisfies, checking palette.primary.toUpperCase() would throw a type error
// because palette.primary would be widened to the union type string | RGBColor.
// satisfies keeps the specific type, allowing you to use string methods directly:
console.log(palette.primary.toUpperCase()); // #3B82F6
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers want to see if you understand how to use types to make code safer and more maintainable, rather than just using TypeScript to silence compiler warnings. They evaluate if you write clean abstractions, choose union types over enums, avoid using `any`, and understand how TypeScript compiles down to JavaScript.

### Red Flags
- **`any` variables**: Using `any` everywhere to bypass type checking, which defeats the purpose of using TypeScript.
- **Ignoring compilation errors**: Using `// @ts-ignore` or `as any` type assertions to bypass compiler errors instead of fixing the root typing issues.
- **Confusing runtime vs. compile-time**: Expecting interfaces to exist at runtime (e.g., using `instanceof myInterface`, which throws an error because interfaces are stripped during compilation).
- **Overusing enums**: Using standard numeric enums when simple union types (`"success" | "error"`) are cleaner and compile to less JavaScript code.

### Green Flags
- **Strict configuration enabled**: Ensuring `strict: true` and `noImplicitAny: true` are enabled in `tsconfig.json`.
- **Exhaustiveness checking**: Using the `never` type to ensure all cases in a discriminated union switch block are handled.
- **Correct type guards**: Using user-defined type predicates (`value is Type`) to narrow down complex types.
- **Read-only protection**: Using `readonly` properties to enforce immutability rules.

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What are the primary differences between TypeScript and JavaScript?
- **Detailed Answer**:
  - **Type Checking**: JavaScript is dynamically typed, checking and resolving types at runtime. TypeScript is statically typed, analyzing and validating types at compile time.
  - **Compilation Step**: JavaScript runs directly in browsers or Node.js without compiling. TypeScript must be compiled using `tsc` to strip out type declarations and output standard JavaScript.
  - **Tooling Support**: TypeScript provides better IDE support (autocomplete, refactoring tools, syntax validation) because it explicitly defines type structures.
  - **Runtime Execution**: At runtime, TypeScript compiles down to standard JavaScript, so it has no performance impact and executes identically to plain JS.
- **Follow-up Questions**:
  - Can you run TypeScript files directly? (Yes, in developmental environments using tools like `ts-node` or runtimes like Deno/Bun, though they still handle compilation under the hood).
  - Does TypeScript protect against runtime type errors from API payloads? (No, TypeScript only provides compile-time safety. To validate runtime payloads, you must use validation libraries like Zod).
- **Interviewer's Expectations**:
  - Distinguishing between compile-time static checks and runtime dynamic execution.
  - Explaining the compilation and type-erasure process.
  - Noting that TypeScript has no runtime performance overhead.

#### 2. What is the difference between an `interface` and a `type` alias? When do you choose each?
- **Detailed Answer**:
  - **Declaration Merging**: Interfaces support declaration merging. If you declare two interfaces with the same name in the same scope, the compiler automatically merges their properties. Type aliases do not support merging and throw a duplicate identifier error.
  - **Extending Shapes**: Interfaces extend other interfaces using the `extends` keyword (e.g., `interface B extends A {}`). Type aliases extend other shapes using intersection types (e.g., `type B = A & { newProp: string }`).
  - **Capability Scope**: Type aliases can define primitives, unions, tuples, and mapped types:
    ```typescript
    type StringOrNumber = string | number; // Not possible with interfaces
    ```
  - **Recommendation**: Use `interface` to define object structures, especially for public APIs, libraries, or components where consumers might need to extend them. Use `type` aliases for complex types, unions, intersections, utility types, or tuples.
- **Follow-up Questions**:
  - How does the compiler performance compare between the two? (Interfaces can be checked slightly faster because the compiler caches their shape lookups, whereas intersection types must be computed).
  - Can a class implement a type alias? (Yes, a class can implement a type alias if it represents an object shape, but it cannot implement a union type).
- **Interviewer's Expectations**:
  - Highlighting declaration merging as the key difference.
  - Explaining when to use each (e.g., interfaces for object structures, type aliases for unions/intersections).
  - Comparing how they extend other types.

#### 3. Compare the types `any`, `unknown`, `never`, and `void`. When should you use each?
- **Detailed Answer**:
  - **`any`**: Turns off type checking. A variable typed as `any` can be assigned to anything, and you can access any property or method on it without compiler checks. Avoid using it in production code.
  - **`unknown`**: A type-safe counterpart to `any`. You can assign any value to an `unknown` variable, but you cannot access its properties or methods, nor assign it to other types, without first performing type narrowing (e.g., using `typeof` or type guards):
    ```typescript
    let val: unknown = "hello";
    // val.toUpperCase(); // Error: Object is of type 'unknown'
    if (typeof val === "string") val.toUpperCase(); // Allowed after narrowing
    ```
  - **`void`**: Used as a function return type to indicate that the function executes but returns no value (returns `undefined`).
  - **`never`**: Represents values that should never occur. Typically used for functions that throw errors, run infinite loops, or as a fallback case to ensure exhaustive checks in switch blocks.
- **Follow-up Questions**:
  - Why is `unknown` preferred over `any` for raw API responses? (It forces developers to validate the data structure before using it, preventing runtime errors).
  - Can you assign a value to a variable of type `never`? (No, not even `any` can be assigned to `never`).
- **Interviewer's Expectations**:
  - Accurate distinction between the un-checked `any` and the type-safe `unknown`.
  - Explaining the difference between no return value (`void`) and code that never returns (`never`).
  - Providing practical use cases for each type.

#### 4. What are union and intersection types? How do you merge object structures with them?
- **Detailed Answer**:
  - **Union Types (`|`)**: Allows a variable to hold one of several types. The compiler only allows you to access properties that are shared by all types in the union, unless you use type narrowing:
    ```typescript
    type Shape = Circle | Square;
    ```
  - **Intersection Types (`&`)**: Combines multiple types into a single type containing all properties from the intersected shapes:
    ```typescript
    type AdminUser = User & Permissions;
    ```
  
  When intersecting objects, properties with different names are merged. If the same property name exists in both types with conflicting types (e.g., `id: string` and `id: number`), that property is resolved as `never`, making the overall object impossible to instantiate.
- **Follow-up Questions**:
  - What happens when you intersect a primitive type with an object type? (It resolves to `never`, as a value cannot be both a primitive and an object).
  - How do you resolve property conflicts in intersections? (By using helper utility types to omit the conflicting property from one of the types before intersecting).
- **Interviewer's Expectations**:
  - Explaining logical OR (`|`) vs. logical AND (`&`) type calculations.
  - Describing how type checking behaves on union and intersection properties.
  - Spotting property type conflict issues.

#### 5. Explain Generics. How do you implement constraints using the `extends` keyword?
- **Detailed Answer**: Generics act as type parameters, allowing you to write reusable code that maintains type safety across different data structures. Instead of using `any` or hardcoding types, you use a type variable (like `<T>`) that is resolved when the function is called.
  
  You can restrict the types that a generic parameter accepts by using the `extends` keyword to define a constraint:
  ```typescript
  interface Identifiable {
    id: string;
  }
  
  // T is constrained: it must be an object that contains at least an 'id' property
  function getRecordId<T extends Identifiable>(record: T): string {
    return record.id;
  }
  
  getRecordId({ id: "rec_1", name: "Laptop" }); // Allowed
  // getRecordId({ name: "Laptop" }); // Error: Property 'id' is missing
  ```
- **Follow-up Questions**:
  - What is the default value of a generic parameter? (You can provide a default type using the `=` operator, e.g., `<T = string>`).
  - How does `keyof` work with generics? (It allows you to constrain a generic parameter to the keys of another object type, e.g., `<K extends keyof T>`).
- **Interviewer's Expectations**:
  - Explaining how generics preserve type safety across different types.
  - Using the `extends` keyword to write type constraints.
  - Demonstrating generic constraints in code.

#### 6. What is type widening and narrowing? Use examples.
- **Detailed Answer**:
  - **Type Widening**: The process where the compiler infers a broader type for a mutable variable initialized with a specific value. This allows you to reassign the variable to other values of that broader type later:
    ```typescript
    let userRole = "admin"; // Inferred as 'string' (widened from '"admin"'), allowing reassignment
    userRole = "editor"; // Allowed
    
    const fixedRole = "admin"; // Inferred as '"admin"' (literal type, not widened because it is a const)
    ```
  - **Type Narrowing**: The process of refining a broad type (like a union type) to a more specific type within a block of code using runtime checks (type guards):
    ```typescript
    function processInput(val: string | number) {
      if (typeof val === "string") {
        // Inferred as string; type is narrowed inside this block
        console.log(val.length);
      }
    }
    ```
- **Follow-up Questions**:
  - How do you prevent type widening on mutable object properties? (By appending `as const` to the object declaration).
  - Can you narrow types using the `in` operator? (Yes, e.g., `if ("radius" in shape)` narrows the type to an object that contains the `radius` property).
- **Interviewer's Expectations**:
  - Defining the difference between widening (broadening type scope) and narrowing (restricting type scope).
  - Explaining how the compiler uses runtime checks to narrow types.
  - Providing code examples for both concepts.

#### 7. How does enabling `strictNullChecks` affect your codebase?
- **Detailed Answer**: When `strictNullChecks` is disabled (the default in older versions), `null` and `undefined` are assignable to any type (e.g., you can assign `null` to a `string` variable). This can lead to runtime errors like "Cannot read properties of null".
  
  Enabling `strictNullChecks` treats `null` and `undefined` as distinct, independent types. You must explicitly declare them in union types if a variable can hold them:
  ```typescript
  let name: string;
  // name = null; // Error: Type 'null' is not assignable to type 'string'
  
  let nullableName: string | null;
  nullableName = null; // Allowed
  ```
  This forces you to check for `null` and `undefined` values (using optional chaining `?.` or type guards) before accessing properties or methods on the variable, protecting against runtime crashes.
- **Follow-up Questions**:
  - What is the non-null assertion operator? (The `!` operator, which tells the compiler to assume a value is not null or undefined, e.g., `user!.name`. Use it cautiously, as it bypasses compile-time checks and can crash at runtime).
  - How does `strictNullChecks` relate to optional properties? (Optional properties automatically append `| undefined` to their type).
- **Interviewer's Expectations**:
  - Explaining how strict checks treat `null` and `undefined` as independent types.
  - Discussing how it protects against runtime crashes.
  - Using optional chaining and guard blocks to handle nullable values.

#### 8. Compare Abstract Classes and Interfaces. When do you use each?
- **Detailed Answer**:
  - **Interfaces**: Purely compile-time structures. They define API contracts and object shapes but generate zero code in the compiled JavaScript output. A class implements an interface using the `implements` keyword.
  - **Abstract Classes**: Runtime structures that can define both abstract method signatures (to be implemented by subclasses) and fully implemented methods, properties, and constructor logic. They compile to standard JavaScript classes. A subclass extends an abstract class using the `extends` keyword.
  
  *Recommendation*: Use an `interface` to define light contracts, object shapes, or when working in frontend frameworks like React. Use an `abstract class` when you want to share common implementation details, default methods, or constructor logic across multiple subclasses.
- **Follow-up Questions**:
  - Can a class implement multiple interfaces? (Yes, classes can implement multiple interfaces but can only extend a single parent class).
  - Do abstract classes exist in the compiled JavaScript output? (Yes, they compile to standard JavaScript classes, whereas interfaces are completely removed).
- **Interviewer's Expectations**:
  - Distinguishing between pure compile-time contracts (interfaces) and runtime classes with partial implementations (abstract classes).
  - Explaining compilation output differences.
  - Providing criteria for choosing between them.

#### 9. What is the difference between `readonly` properties and `const` declarations?
- **Detailed Answer**:
  - **`const`**: Applies to variable declarations. It prevents the variable reference from being reassigned to a new value. It does not prevent properties of an object or elements of an array assigned to the variable from being mutated.
  - **`readonly`**: Applies to class properties, interface properties, or type definitions. It prevents individual properties of an object from being mutated after initialization:
    ```typescript
    const user = { name: "Alice" };
    user.name = "Bob"; // Allowed (const reference is preserved, object is mutated)
    
    interface SecureUser {
      readonly name: string;
    }
    const secureUser: SecureUser = { name: "Alice" };
    // secureUser.name = "Bob"; // Error: Cannot assign to 'name' because it is a read-only property
    ```
- **Follow-up Questions**:
  - How do you create an array that cannot be mutated? (Using `ReadonlyArray<T>` or `readonly number[]`).
  - Does `readonly` exist in the compiled JavaScript output? (No, it is a compile-time check and does not prevent mutations in raw JavaScript at runtime).
- **Interviewer's Expectations**:
  - Distinguishing between variable references (`const`) and object properties (`readonly`).
  - Describing compile-time check limitations.
  - Explaining how to enforce immutability on arrays.

#### 10. What is declaration merging? Explain its use cases and risks.
- **Detailed Answer**: Declaration merging is the behavior where the TypeScript compiler automatically merges multiple declarations sharing the same name in the same namespace or scope.
  
  *Supported Merges*:
  - **Interfaces**: Properties from duplicate interface declarations are merged:
    ```typescript
    interface User { name: string; }
    interface User { age: number; }
    // User is merged to contain both 'name' and 'age'
    ```
  - **Namespaces**: Merges declarations across namespaces.
  - **Classes & Namespaces**: Merges namespace functions or values onto a class.
  
  *Use Case*: Extending third-party library types or globally defined variables (such as appending custom properties to the Express request object or the global window object).
  
  *Risk*: If duplicate declarations define the same property name with conflicting types, compilation fails. It can also make code harder to debug because type declarations are split across different files.
- **Follow-up Questions**:
  - Can you merge two type aliases? (No, declaring two type aliases with the same name throws a duplicate identifier error).
  - How do you augment a globally defined interface? (Wrap the duplicate interface inside a `declare global {}` block).
- **Interviewer's Expectations**:
  - Explaining the definition and behavior of declaration merging.
  - Describing use cases like augmenting third-party types.
  - Highlighting risks like split type declarations and naming conflicts.

---

### Scenario-Based Questions

#### 11. Model an API request state that can represent Idle, Loading, Success (with data), and Error (with an error message) states using type safety.
- **Detailed Answer**:
  We can model this using a discriminated union type:
  ```typescript
  type APIState<T> =
    | { status: "idle" }
    | { status: "loading" }
    | { status: "success"; data: T; fetchedAt: Date }
    | { status: "error"; error: Error };
  
  // Usage
  interface Product {
    id: string;
    title: string;
  }
  
  function renderProducts(state: APIState<Product[]>) {
    switch (state.status) {
      case "idle":
        return "Click search to load products.";
      case "loading":
        return "Fetching products...";
      case "success":
        // Safe to access data
        return `Loaded ${state.data.length} products.`;
      case "error":
        // Safe to access error
        return `Failed to fetch: ${state.error.message}`;
    }
  }
  ```
- **Follow-up Questions**:
  - Why is a discriminated union better than a single object with optional fields (e.g., `{ loading: boolean, data?: T, error?: Error }`)? (Discriminated unions prevent invalid states, such as having both data and an error present simultaneously).
  - How do you ensure the switch statement handles all states? (Use an exhaustiveness check with the `never` type in the `default` block).
- **Interviewer's Expectations**:
  - Using a discriminated union with a shared discriminator property (`status`).
  - Parameterizing the state type using generics.
  - Preventing invalid state combinations.

#### 12. Design a type-safe Event Emitter class that restricts registered events and callbacks to a predefined schema.
- **Detailed Answer**:
  We can use generics and mapped types to build a type-safe event emitter:
  ```typescript
  type EventSchema = Record<string, any[]>;
  
  class TypedEventEmitter<TEvents extends EventSchema> {
    private listeners: { [K in keyof TEvents]?: Function[] } = {};
  
    on<K extends keyof TEvents>(event: K, callback: (...args: TEvents[K]) => void) {
      if (!this.listeners[event]) {
        this.listeners[event] = [];
      }
      this.listeners[event]!.push(callback);
    }
  
    emit<K extends keyof TEvents>(event: K, ...args: TEvents[K]) {
      const callbacks = this.listeners[event];
      if (callbacks) {
        callbacks.forEach(cb => cb(...args));
      }
    }
  }
  
  // Usage
  interface UserEvents extends EventSchema {
    login: [userId: string, timestamp: Date];
    logout: [userId: string];
  }
  
  const emitter = new TypedEventEmitter<UserEvents>();
  emitter.on("login", (id, date) => console.log(id, date)); // Typed parameters
  // emitter.emit("login", "usr_1"); // Error: Expected 2 arguments, got 1
  ```
- **Follow-up Questions**:
  - How do you allow optional arguments in events? (Define them as optional elements in the tuple, e.g., `login: [userId: string, timestamp?: Date]`).
  - How would you implement an unsubscribe function? (Return a function from `on` that removes the registered callback from the listeners array).
- **Interviewer's Expectations**:
  - Using generics to define the event schema.
  - Constraining event names to the schema's keys (`keyof TEvents`).
  - Typing callback parameters using tuple mapping (`TEvents[K]`).

#### 13. Design a type-safe form validation utility using mapped types and generics.
- **Detailed Answer**:
  ```typescript
  type ValidatorFn<T> = (value: T) => string | null;
  
  type FormValidators<TForm> = {
    [K in keyof TForm]?: ValidatorFn<TForm[K]>[];
  };
  
  type FormErrors<TForm> = {
    [K in keyof TForm]?: string[];
  };
  
  class FormValidator<TForm extends Record<string, any>> {
    constructor(private validators: FormValidators<TForm>) {}
  
    validate(data: TForm): FormErrors<TForm> {
      const errors: FormErrors<TForm> = {};
      
      for (const key in this.validators) {
        const valFns = this.validators[key];
        if (valFns) {
          const fieldErrors = valFns
            .map(fn => fn(data[key]))
            .filter((err): err is string => err !== null);
            
          if (fieldErrors.length > 0) {
            errors[key] = fieldErrors;
          }
        }
      }
      return errors;
    }
  }
  ```
- **Follow-up Questions**:
  - How do you handle validation for nested object properties? (Use recursive mapped types to validate nested structures).
  - Can you write validation schemas without class syntax? (Yes, you can write pure functions that accept schemas and datasets).
- **Interviewer's Expectations**:
  - Mapping validation rules to form field keys.
  - Enforcing types on form inputs using generics.
  - Filtering validation results using type guards.

#### 14. How do you add type definitions to an external JavaScript library that lacks types, without modifying its code?
- **Detailed Answer**:
  You can create custom type definitions using declaration files (`.d.ts`) and module augmentation:
  1. **Configure paths**: Ensure your `tsconfig.json` is configured to look for local declaration files:
     ```json
     {
       "compilerOptions": {
         "typeRoots": ["./node_modules/@types", "./types"]
       }
     }
     ```
  2. **Create the declaration file**: Inside the `types` folder, create a file matching the library name, e.g., `types/legacy-logger/index.d.ts`.
  3. **Declare the module**: Declare the module structure using the `declare module` syntax:
     ```typescript
     declare module "legacy-logger" {
       export interface LoggerConfig {
         silent: boolean;
         level: "info" | "error";
       }
       
       export class Logger {
         constructor(config: LoggerConfig);
         log(message: string): void;
       }
     }
     ```
- **Follow-up Questions**:
  - What does `declare` do? (It tells the compiler that a variable, function, or class exists at runtime, preventing compile errors without generating code).
  - How do you augment a class inside an existing typed library? (Import the module, and declare it again in the same namespace to merge your properties onto the existing class or interface).
- **Interviewer's Expectations**:
  - Knowing where to place declaration files.
  - Writing clean library modules using `declare module`.
  - Understanding how the compiler loads type definition roots.

#### 15. Implement recursive utility types for `DeepPartial` and `DeepReadonly` from scratch.
- **Detailed Answer**:
  We can write recursive mapped types that apply modifications to nested object structures:
  ```typescript
  // DeepPartial: Recursively makes all object properties optional
  type DeepPartial<T> = {
    [K in keyof T]?: T[K] extends object
      ? DeepPartial<T[K]>
      : T[K];
  };
  
  // DeepReadonly: Recursively makes all object properties read-only
  type DeepReadonly<T> = {
    readonly [K in keyof T]: T[K] extends object
      ? DeepReadonly<T[K]>
      : T[K];
  };
  
  // Test structures
  interface Project {
    id: string;
    details: {
      name: string;
      tasks: string[];
    };
  }
  
  type EditableProject = DeepPartial<Project>;
  // Equivalent to:
  // type EditableProject = {
  //   id?: string;
  //   details?: {
  //     name?: string;
  //     tasks?: string[];
  //   }
  // }
  ```
- **Follow-up Questions**:
  - Why do we check `extends object`? (To determine if a property is a nested object that needs recursive mapping. If it is a primitive type, we return the type as-is).
  - How does this handle array properties? (If an array is treated as an object, it can lead to type errors. You can handle arrays explicitly using a conditional check like `T[K] extends Array<infer U>`).
- **Interviewer's Expectations**:
  - Designing recursive type mappings.
  - Using conditional checks to identify objects.
  - Preserving primitive types during recursion.

---

### Debugging Questions

#### 16. A destructured object property loses its specific literal type, widening to `string`. How do you debug and fix this?
- **Detailed Answer**:
  *The Cause*: When you declare an object literal, the compiler widens string properties to the general `string` type to allow for future reassignments:
  ```typescript
  const config = {
    env: "production" // Widened to 'string'
  };
  const { env } = config; // env is inferred as 'string'
  ```
  If another function requires a specific literal value like `"production" | "development"`, passing `env` will throw a type error.
  
  *Solutions*:
  1. **Use `as const`**: Appending `as const` to the object literal prevents type widening, freezing the properties as read-only literal types:
     ```typescript
     const config = {
       env: "production"
     } as const;
     const { env } = config; // env is inferred as '"production"'
     ```
  2. **Add Explicit Types**: Annotate the object with an explicit type or interface:
     ```typescript
     interface Config { env: "production" | "development"; }
     const config: Config = { env: "production" };
     ```
- **Follow-up Questions**:
  - What else does `as const` change? (It applies `readonly` recursively to all properties and turns arrays into read-only tuples).
  - Can you use `as const` on variables? (No, `as const` is only used on object and array literals).
- **Interviewer's Expectations**:
  - Identifying type widening as the root cause.
  - Explaining the differences between mutable object inference and literal type inference.
  - Using `as const` to enforce literal types.

#### 17. The compiler throws: "Property 'x' does not exist on type 'T'". How do you debug and resolve it?
- **Detailed Answer**:
  *The Cause*: This error happens when a generic parameter `T` is used without constraints. The compiler must assume that `T` could be any type (including primitives like `number` or objects without the property `x`), so it blocks access to property `x`.
  
  *Debugging and Fix*:
  1. Check where the property `x` is accessed.
  2. Constrain the generic parameter `T` using the `extends` keyword to ensure it only accepts objects that contain property `x`:
     ```typescript
     // Fix: T is constrained to objects that contain property 'x'
     function printX<T extends { x: any }>(obj: T) {
       console.log(obj.x);
     }
     ```
  3. If the property `x` is optional, check if you need to perform type narrowing before accessing it.
- **Follow-up Questions**:
  - Can you use `keyof` to constrain property lookups? (Yes, e.g., `<K extends keyof T>` ensures a key parameter is a valid property key of object `T`).
  - What happens if you pass a type assertion like `(obj as any).x`? (It silences the compiler warning, but bypasses type checking and can lead to runtime crashes).
- **Interviewer's Expectations**:
  - Identifying missing generic constraints as the cause of the error.
  - Constraining generic parameters using the `extends` keyword.
  - Avoiding `any` type assertions to bypass compilation checks.

#### 18. You receive an error: "Type 'unknown' is not assignable to type 'string'". How do you debug it?
- **Detailed Answer**:
  *The Cause*: You are trying to assign a value of type `unknown` to a variable that requires a `string`. The `unknown` type represents any value, so the compiler blocks the assignment because it cannot guarantee the value is actually a string.
  
  *Debugging and Fix*:
  1. **Locate the assignment**: Find where the `unknown` type is assigned to the `string` variable.
  2. **Narrow the type**: Use a type guard (like `typeof` or a type predicate) to verify the value is a string before assigning it:
     ```typescript
     let rawData: unknown = fetchInput();
     if (typeof rawData === "string") {
       let cleanData: string = rawData; // Allowed inside the block after narrowing
     }
     ```
  3. **Assert the type**: If you are certain the value is a string and cannot perform runtime checks, use a type assertion (`rawData as string`):
     ```typescript
     let cleanData: string = rawData as string;
     ```
- **Follow-up Questions**:
  - Why is `unknown` preferred over `any`? (Because `unknown` forces you to perform type checks before using the value, whereas `any` bypasses type checking entirely).
  - Can you assign `unknown` to another `unknown` variable? (Yes, `unknown` is assignable to `unknown` or `any`).
- **Interviewer's Expectations**:
  - Explaining the type-safety behavior of `unknown`.
  - Narrowing union and unknown types using runtime type guards.
  - Using type assertions correctly when runtime checks are not possible.

#### 19. The compiler throws: "Type alias 'X' circularly references itself". How do you resolve this?
- **Detailed Answer**:
  *The Cause*: This error happens when a type alias references itself directly in its definition without an exit condition or property mapping:
  ```typescript
  type Node = Node; // Circular reference error
  ```
  Circular references are common when modeling recursive data structures like trees or nested JSON objects.
  
  *Solutions*:
  1. **Wrap in an Interface**: Interfaces resolve circular dependencies because they defer property lookup to runtime. You can wrap the recursive reference inside an interface property:
     ```typescript
     interface TreeNode {
       value: string;
       children: TreeNode[]; // Allowed in interfaces
     }
     ```
  2. **Use Lazy Mapped Types**: If using type aliases, ensure the self-reference is nested inside an array or an optional object property, allowing the compiler to resolve it lazily:
     ```typescript
     type JSONValue =
       | string
       | number
       | boolean
       | null
       | { [key: string]: JSONValue } // Nested inside an object mapping
       | JSONValue[]; // Nested inside an array
     ```
- **Follow-up Questions**:
  - Can a type alias refer to itself inside a generic? (Yes, as long as the recursive reference is nested and can be resolved lazily).
  - How do you model a JSON schema type safely? (Use recursive type aliases nested inside arrays and object dictionaries).
- **Interviewer's Expectations**:
  - Explaining how the compiler checks circular type references.
  - Using interfaces to resolve circular type definitions.
  - Designing recursive tree and nested JSON structures safely.

#### 20. Module augmentation type changes are not applying in other files. How do you resolve this?
- **Detailed Answer**:
  *Debugging strategy*:
  1. **Verify file imports**: Ensure that the file containing your module augmentation is loaded by the compiler. Check if it is listed in the `include` files array in your `tsconfig.json`.
  2. **Check the file structure**: A declaration file must be treated as a module (it must contain at least one `import` or `export` statement, even an empty `export {}`). Without this, the compiler treats the file as a global script instead of a module augmentation:
     ```typescript
     // types/express.d.ts
     import { Request } from "express"; // Forces the file to be treated as a module
     
     declare module "express" {
       interface Request {
         currentUser?: { id: string; role: string };
       }
     }
     ```
  3. **Check naming matches**: Verify that the module name in `declare module "name"` matches the target library name exactly.
- **Follow-up Questions**:
  - What happens if a `.d.ts` file has no imports or exports? (The compiler treats all declarations inside it as global types instead of augmenting specific modules).
  - Can you use module augmentation on default exports? (Yes, but you must augment the exported interface name directly rather than the default export alias).
- **Interviewer's Expectations**:
  - Understanding how the compiler loads module scopes.
  - Creating module-scoped files using `import` or `export` statements.
  - Augmenting module interfaces correctly.

---

### System Design Questions

#### 21. Design a type-safe plugin architecture for a core application.
- **Detailed Answer**:
  A typed plugin architecture uses generic interfaces to define how plugins hook into the core application:
  ```typescript
  interface AppContext {
    config: Record<string, any>;
    log: (msg: string) => void;
  }
  
  // Define the plugin contract
  interface AppPlugin<TOptions = any, TExports = any> {
    name: string;
    initialize: (ctx: AppContext, options: TOptions) => TExports;
  }
  
  class AppEngine {
    private plugins = new Map<string, AppPlugin>();
    private exports: Record<string, any> = {};
  
    constructor(private context: AppContext) {}
  
    register<TOptions, TExports>(plugin: AppPlugin<TOptions, TExports>, options: TOptions): TExports {
      const result = plugin.initialize(this.context, options);
      this.plugins.set(plugin.name, plugin);
      this.exports[plugin.name] = result;
      return result;
    }
  
    getPluginExports<TPlugin extends AppPlugin>(pluginName: TPlugin["name"]): ReturnType<TPlugin["initialize"]> {
      return this.exports[pluginName];
    }
  }
  ```
- **Follow-up Questions**:
  - How do you allow plugins to extend the core context type? (Use generic type parameters on the `AppEngine` class that plugins can extend using intersection types).
  - How do you prevent plugins from registering under duplicate names? (Check if the plugin name already exists in the `plugins` map during registration and throw an error).
- **Interviewer's Expectations**:
  - Using generics to define customizable plugin options and export signatures.
  - Constraining plugin names to avoid registry issues.
  - Restricting plugin access to the application context.

#### 22. Design a type sharing system between a Node.js backend and a React frontend in a monorepo.
- **Detailed Answer**:
  To share types between a backend and a frontend in a monorepo:
  
  *System Architecture*:
  1. **Shared Package**: Create a shared NPM workspace package (e.g., `@project/shared-types`) in the monorepo root:
     ```text
     monorepo/
       packages/
         frontend/ (React)
         backend/  (Node.js)
         shared/   (Common DTO types)
     ```
  2. **API Data Contracts**: Define data models (Data Transfer Objects / DTOs) in the shared package:
     ```typescript
     // packages/shared/src/dto/user.ts
     export interface UserDTO {
       id: string;
       username: string;
       email: string;
     }
     ```
  3. **Configure Dependencies**: Add `@project/shared-types` to the dependencies list in the frontend and backend `package.json` files.
  4. **Dynamic Validation**: Combine TypeScript types with runtime validation schemas (using Zod) in the shared package to validate API payloads at runtime on the server and client:
     ```typescript
     import { z } from "zod";
     
     export const UserSchema = z.object({
       id: z.string(),
       username: z.string(),
       email: z.string().email()
     });
     
     export type UserDTO = z.infer<typeof UserSchema>;
     ```
- **Follow-up Questions**:
  - Why are runtime checkers (like Zod) required alongside TypeScript? (Because TypeScript types are compiled away and do not exist at runtime, leaving the application vulnerable to invalid API payloads).
  - How do you compile the shared package? (Use `tsc` to output declarations (`.d.ts` files) alongside compiled JS files).
- **Interviewer's Expectations**:
  - Designing a shared package directory structure in a monorepo.
  - Using runtime validation (Zod) to validate external payloads.
  - Sharing type-safe DTOs across the backend and frontend.

#### 23. Design a type-safe router system that maps URLs to parameters and page components.
- **Detailed Answer**:
  We can use mapped types and string interpolation to validate route URLs and parameters:
  ```typescript
  // Define route paths with parameters
  type ExtractRouteParams<T extends string> =
    T extends `${string}/:${infer Param}/${infer Rest}`
      ? { [K in Param | keyof ExtractRouteParams<`/${Rest}`>]: string }
      : T extends `${string}/:${infer Param}`
        ? { [K in Param]: string }
        : {};
  
  interface RouteDefinition<TPath extends string> {
    path: TPath;
    component: (params: ExtractRouteParams<TPath>) => string;
  }
  
  class Router {
    private routes: RouteDefinition<any>[] = [];
  
    addRoute<TPath extends string>(route: RouteDefinition<TPath>) {
      this.routes.push(route);
    }
  
    navigate<TPath extends string>(path: TPath, params: ExtractRouteParams<TPath>) {
      // Logic to parse URL parameters and render component
    }
  }
  
  // Usage
  const appRouter = new Router();
  appRouter.addRoute({
    path: "/user/:id/posts/:postId",
    component: (params) => `User: ${params.id} - Post: ${params.postId}` // Typed parameters
  });
  ```
- **Follow-up Questions**:
  - What happens if a route has no parameters? (The type resolves to an empty object `{}`).
  - How do you handle optional query parameters? (You can define a separate type for query strings and merge it with the route parameters).
- **Interviewer's Expectations**:
  - Parsing route parameters from URL strings using template literals and the `infer` keyword.
  - Binding parsed parameters to component properties.
  - Enforcing types on route navigation.

---

## 10. Common Mistakes

- **Using `any` to silence type warnings**: Bypasses the type checker and defeats the purpose of using TypeScript. Use `unknown` or write proper type guards instead.
- **Confusing compile-time types with runtime code**: Trying to run runtime checks like `instanceof` on interfaces (which are compiled away). Use class interfaces or discriminated unions instead.
- **Using non-null assertions (`!`) too frequently**: Tells the compiler to ignore `null` and `undefined` checks, which can lead to runtime crashes if the value is missing.
- **Forgetting to enable strict flags in `tsconfig.json`**: Disabling flags like `strict: true` or `strictNullChecks: true` makes the type checker much weaker.
- **Overusing enums**: Using standard numeric enums instead of clean, simple string union types (`"idle" | "loading"`).

---

## 11. Comparison Section: TypeScript vs. JSDoc Typing

| Feature | TypeScript (`.ts`) | JSDoc with JS (`.js`) |
|---|---|---|
| **Compilation Step** | Required (tsc must compile files) | None (Runs directly in standard engines) |
| **Type Definitions** | Inline type annotations | JSDoc comment blocks (`/** @type {number} */`) |
| **Ecosystem Support** | Native standard for modern web libraries | Good for light projects and Node.js utilities |
| **Code Readability** | Cleaner syntax for complex structures | Can become cluttered with large JSDoc blocks |
| **Feature Richness** | Full support for advanced types and generics | Limited support for complex conditional structures |

---

## 12. Practical Project Ideas

### Beginner Project: Type-Safe Memory Cache
Build an in-memory cache class using TypeScript generics. The class must allow users to store keys and values of a specified type, support optional TTL parameters, and automatically clear expired entries.

### Intermediate Project: Monorepo Type Sharing
Set up a monorepo workspace containing a Nest.js API and a Next.js frontend. Create a shared package containing common Zod schemas and TypeScript interface types (DTOs), and use them to validate data transfers between the client and server.

### Advanced Project: Type-Safe State Machine
Design a state machine library using generics and discriminated unions. The library must accept a state configuration schema and validate that state transitions are valid at compile time, warning users if they attempt to transition to an illegal state.

---

## 13. Internship Preparation Notes

- **Practice writing custom type guards**: Be prepared to write type guard functions (using `value is Type`) to narrow down complex types in coding interviews.
- **Whiteboard generic constraints**: Practice writing generic functions that accept key-value objects and constrain parameters using `extends keyof`.
- **Familiarize yourself with utility types**: Know how and when to use `Pick`, `Omit`, `Partial`, and `Record` to avoid duplicate type definitions.
- **Understand the tsconfig configuration**: Be prepared to explain compiler flags like `strictNullChecks`, `noImplicitAny`, and `target` in technical interviews.

---

## 14. Cheat Sheet

```typescript
/* Discriminator Union Structure */
interface Circle { kind: "circle"; radius: number; }
interface Square { kind: "square"; side: number; }
type Shape = Circle | Square;

/* User-defined Type Guard Predicate */
function isCircle(shape: Shape): shape is Circle {
  return shape.kind === "circle";
}

/* Extracting Keys with keyof */
interface User { id: string; name: string; }
type UserKeys = keyof User; // "id" | "name"

/* Constrained Generics */
function getProp<T, K extends keyof T>(obj: T, key: K): T[K] {
  return obj[key];
}

/* satisfies Operator (Validates without type widening) */
const settings = {
  theme: "dark",
  timeout: 5000
} satisfies Record<string, string | number>;
// settings.theme is still inferred as '"dark"', allowing string method checks
```

---

## 15. One-Day Revision Guide

- [ ] Explain the difference between nominal and structural typing.
- [ ] Differentiate the types `any`, `unknown`, and `never`.
- [ ] Write a generic function that accepts an object and a key and returns the property value.
- [ ] Design a discriminated union to represent the states of an API request.
- [ ] Augment an interface in an external module using declaration merging.
- [ ] Explain how the `satisfies` operator compares to type assertions (`as`).
