# 39. Angular Enterprise Development

## 1. Introduction
### What it is
Angular is an open-source, component-based, opinionated web application framework developed and maintained by Google in 2016. It is built entirely on TypeScript and provides a comprehensive suite of development tools, including routing, form management, dependency injection, and HTTP client modules, designed to compile high-performance, structured enterprise-grade web applications.

### Why it exists
Building large-scale client-side applications using unstructured, ad-hoc JavaScript libraries often leads to architectural fragmentation, testing difficulties, and poor scalability. Angular exists to enforce an architecture-first design. It provides a standardized framework out of the box, ensuring that multi-team enterprise groups can write maintainable, testable, and highly consistent web applications.

### Problems it solves
- **Architecture Fragmentation**: Standardizes code modularity using standalone components, services, pipes, and directives.
- **Change Detection Latency**: Optimizes UI rendering by migrating from global zone-based checking to modern, fine-grained reactivity via Angular Signals.
- **Dependency Management**: Decouples services from components and simplifies unit test mocking through hierarchical Dependency Injection.
- **Form Verification Boilerplate**: Delivers robust, type-safe validation and asynchronous status updates via Reactive Forms.

### Industry Use Cases
- **Enterprise Dashboards**: Administrative portals managing complex state and multi-role operations.
- **Financial Software**: Secure banking platforms requiring strict data binding and automated form validations.
- **E-Commerce Portals**: High-performance consumer storefronts utilizing Server-Side Rendering (SSR).
- **SaaS Control Panels**: Web interfaces managing real-time data feeds and multi-step configuration wizard steps.

### Analogy
If React is a toolbox of custom parts where you must pick your own router, state manager, and build tools, Angular is a fully assembled luxury SUV: it comes pre-equipped with high-end navigation, automatic climate control, and standard safety systems, ensuring a consistent ride across any terrain.

---

## 2. Core Concepts

### Beginner Concepts
- **Standalone Components**: Modular, self-contained view definitions that import their own dependencies, bypassing the need for legacy `NgModule` declarations.
- **Directives**: Classes that add custom behavior to elements in the DOM. Divided into:
  - **Structural Directives**: Alter the DOM layout by adding or removing elements (e.g. `*ngIf`, `*ngFor` or the new `@if`, `@for` syntax).
  - **Attribute Directives**: Alter the appearance or behavior of an existing element (e.g. `ngClass`, `ngStyle`).
- **Pipes**: Template helpers used to format data before rendering (e.g. `currency`, `date`).
- **Data Binding**: Enforcing state propagation via Interpolation (`{{val}}`), Property Binding (`[property]`), and Event Binding (`(event)`).

### Intermediate Concepts
- **Angular Signals**: A fine-grained reactive model (`signal()`, `computed()`, `effect()`) that tracks dependencies dynamically and notifies the DOM when values change.
- **Dependency Injection (DI)**: Design pattern where dependencies are provided to constructors by injectors rather than instantiated inside classes.
- **RxJS Observables**: Stream-based async programming structures used to manage event listeners, HTTP queries, and reactive pipelines.
- **Reactive Forms**: Model-driven form management offering type-safe inputs, dynamic fields, and custom validations.

### Advanced Concepts
- **Zone.js vs. Zoneless Change Detection**: Migrating from micro-task interception (Zone.js checking everything) to fine-grained Signals tracking.
- **Hierarchical Injectors**: Resolution pathways across Platform, Root, Environment, and Component injector trees.
- **Content Projection**: Dynamically injecting custom HTML layouts using the `<ng-content>` directive.
- **Route Guards & Resolvers**: Middleware interfaces regulating route access permissions and pre-fetching page data.

---

## 3. Internal Working

### Change Detection, Signals, and the Ivy Compiler
Angular checks for model updates and propagates changes to the DOM using a directional tree scan.

#### The Ivy Compilation Pipeline
The Ivy Compiler compiles component templates into highly optimized, tree-shakeable JavaScript code. During compilation, Ivy converts HTML templates into incremental DOM instruction blocks:

```text
+-----------------------+
|  HTML Template        | (e.g., <div>{{ title }}</div>)
+-----------------------+
            | (Ivy Compiler Compilation)
            v
+-----------------------+
| Incremental DOM JS    | (Outputs template functions: ɵɵelementStart, ɵɵtext)
+-----------------------+
            |
            v
+-----------------------+
| Browser View Rendering| (Executes instructions directly on DOM node)
+-----------------------+
```

When change detection runs, Angular executes these compiled template functions directly against the DOM node structure.

#### Traditional Change Detection (Zone.js)
1. **Zone.js** patches browser APIs (clicks, setTimeout, HTTP requests) to detect when async tasks complete.
2. It triggers change detection for the entire component tree from top to bottom.
3. Every component is checked unless marked with the `OnPush` strategy (which only checks when input properties change).

#### Signal-Based Reactivity (Zoneless)
Signals bypass Zone.js entirely. A signal maintains an internal list of consumers. When a signal changes, Angular schedules rendering only for the specific components reading that signal, eliminating global tree sweeps.

---

## 4. Important Terminology
- **Standalone Component**: A component that imports its own dependencies without needing an `NgModule`.
- **Signal**: A reactive wrapper value that notifies consumers when its contents change.
- **RxJS**: A reactive programming library based on Observables.
- **Dependency Injection (DI)**: A pattern for passing services into dependent components.
- **Zone.js**: A library that patches browser APIs to trigger global change detection.
- **OnPush Change Detection**: Strategy checking components only when their input values change.
- **Directive**: A class that manipulates DOM elements.
- **Pipe**: A template pipe formatting raw data values.
- **Ivy Compiler**: Angular's compilation engine that outputs tree-shakeable code.

---

## 5. Beginner Examples

### Example 1: Standalone Component with Event Binding
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-counter',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 1rem;">
      <h3>Count: {{ count }}</h3>
      <button (click)="increment()">Increment</button>
    </div>
  `
})
export class CounterComponent {
  public count: number = 0;

  public increment(): void {
    this.count++;
  }
}
```

### Example 2: Pipe Formatting
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-date-viewer',
  standalone: true,
  imports: [CommonModule],
  template: `
    <p>Today is: {{ today | date:'fullDate' | uppercase }}</p>
  `
})
export class DateViewerComponent {
  public today: Date = new Date();
}
```

---

## 6. Intermediate Examples

### Example 1: Modern Signals Counter
```typescript
import { Component, signal, computed, effect } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signals-counter',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div style="padding: 1rem;">
      <p>Value: {{ value() }}</p>
      <p>Double: {{ doubleValue() }}</p>
      <button (click)="add()">Add</button>
    </div>
  `
})
export class SignalsCounterComponent {
  public value = signal<number>(0);
  
  // Computed signal (cached, re-evaluates only when value() changes)
  public doubleValue = computed(() => this.value() * 2);

  constructor() {
    // Effect triggers whenever internal signals update
    effect(() => {
      console.log(`Current counter value is: ${this.value()}`);
    });
  }

  public add(): void {
    this.value.update(val => val + 1);
  }
}
```

### Example 2: Reactive Form with Custom Domain Validation
```typescript
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators, AbstractControl, ValidationErrors } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <form [formGroup]="registerForm" (ngSubmit)="onSubmit()">
      <input formControlName="email" placeholder="Email">
      <div *ngIf="registerForm.get('email')?.errors?.['email']">Invalid Email</div>
      <button type="submit" [disabled]="registerForm.invalid">Register</button>
    </form>
  `
})
export class RegisterComponent {
  public registerForm: FormGroup;

  constructor(private fb: FormBuilder) {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email, this.domainValidator]]
    });
  }

  // Custom Domain Validator
  private domainValidator(control: AbstractControl): ValidationErrors | null {
    const email = control.value as string;
    if (email && !email.endsWith('@company.com')) {
      return { invalidDomain: true };
    }
    return null;
  }

  public onSubmit(): void {
    if (this.registerForm.valid) {
      console.log("Registered data: ", this.registerForm.value);
    }
  }
}
```

---

## 7. Advanced Concepts

### RxJS Stream Composition with SwitchMap
When handling search inputs, we want to discard previous HTTP requests if the user types a new character. We compose these operations using RxJS pipe operators:

```typescript
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { debounceTime, distinctUntilChanged, switchMap, Observable } from 'rxjs';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  template: `
    <input [formControl]="searchControl" placeholder="Search...">
    <ul>
      <li *ngFor="let item of results$ | async">{{ item }}</li>
    </ul>
  `
})
export class SearchComponent implements OnInit {
  public searchControl = new FormControl('');
  public results$!: Observable<any>;

  constructor(private http: HttpClient) {}

  public ngOnInit(): void {
    this.results$ = this.searchControl.valueChanges.pipe(
      debounceTime(300), // Wait 300ms for pause in typing
      distinctUntilChanged(), // Trigger only if input changed
      switchMap(query => this.fetchResults(query)) // Cancel previous request
    );
  }

  private fetchResults(query: string | null): Observable<any> {
    return this.http.get(`https://api.example.com/search?q=${query || ''}`);
  }
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for understanding of enterprise scaling patterns. They evaluate your ability to manage RxJS memory streams, optimize change detection configurations, and build secure routing architectures.

### Red Flags
- Subscribing to observables inside components and forgetting to unsubscribe (causing memory leaks).
- Mutating inputs inside `OnPush` components directly instead of passing new object references.
- Writing heavy logic inside template functions (which execute on every change detection loop).
- Failing to explain the difference between `switchMap`, `mergeMap`, and `concatMap`.

### Green Flags
- Utilizing signals to bypass Zone.js and reduce performance overheads.
- Relying on the `async` pipe to manage stream subscriptions and unsubscriptions automatically.
- Designing custom structural directives to encapsulate rendering logic.

### Answers Matrix
| Level | Question: "What is the difference between switchMap and mergeMap?" |
|---|---|
| **Rejected** | "They are RxJS things used to fetch API data." |
| **Shortlisted** | "SwitchMap cancels the previous HTTP request when a new one comes in. MergeMap lets multiple run in parallel." |
| **Selected** | "SwitchMap cancels the previous inner observable subscription when a new value is emitted by the source, preventing race conditions during rapid events. MergeMap executes all inner subscriptions concurrently, maintaining active streams without cancelling." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What are Standalone Components, and what problems do they solve?
- **Detailed Answer**: Standalone components are components that manage their own template imports directly, without needing to be declared inside an `NgModule`. This reduces boilerplate configuration, resolves circular module dependency errors, and makes components easier to reuse, lazy-load, and unit test.
- **Follow-up Questions**: How do you configure routing for standalone components? (Answer: Use `loadComponent` in routing configurations to lazy-load the component dynamically).
- **Interviewer's Expectations**: Point out the reduction of NgModule boilerplate and describe lazy-loading.

#### 2. Explain the change detection strategies Default vs OnPush.
- **Detailed Answer**: Default change detection checks the component and its children on every change detection cycle (e.g. click, scroll). `OnPush` change detection restricts checks. It only triggers when an `@Input()` reference changes, an event originates from within the component, or change detection is triggered manually via `ChangeDetectorRef.markForCheck()`.
- **Follow-up Questions**: How does changing an object property affect `OnPush`? (Answer: It does not trigger change detection because the object reference remains the same. You must pass a new object reference).
- **Interviewer's Expectations**: Describe input reference checks and the performance benefits of `OnPush`.

#### 3. What are Angular Signals, and how do they differ from RxJS Observables?
- **Detailed Answer**: Signals represent state. They are synchronous, always hold a value, and track dependencies automatically when read in computed fields or templates. RxJS Observables represent asynchronous streams of events over time. Observables are not necessarily synchronous and require manual subscriptions or pipe operators to combine.
- **Follow-up Questions**: Can you combine Signals and RxJS? (Answer: Yes, using `toSignal()` to read observables as signals, and `toObservable()` to emit signal updates as streams).
- **Interviewer's Expectations**: Contrast synchronous state representations with async event streams.

#### 4. How does Dependency Injection (DI) resolve service instances in Angular?
- **Detailed Answer**: Angular uses hierarchical injectors. When a component requests a dependency, Angular searches the **Component Injector Tree** first. If not found, it traverses upwards through parent injectors, Environment Injectors (configured in routing), and finally the Root/Platform Injectors.
- **Follow-up Questions**: What is the difference between `@Injectable({ providedIn: 'root' })` and adding a service to a component's `providers` array? (Answer: `providedIn: 'root'` registers a single global instance. Adding it to `providers` creates a new instance scoped to that component and its children).
- **Interviewer's Expectations**: Detail the hierarchical lookup steps.

#### 5. Explain the difference between switchMap, mergeMap, concatMap, and exhaustMap.
- **Detailed Answer**:
  - `switchMap`: Cancels the current active inner observable when a new value is emitted by the source.
  - `mergeMap`: Executes all inner observables concurrently without waiting or cancelling.
  - `concatMap`: Queues incoming values and runs inner observables sequentially one after another.
  - `exhaustMap`: Ignores new incoming source values while the current inner observable is still executing.
- **Follow-up Questions**: Which operator is best for a search typeahead? (Answer: `switchMap`, to discard obsolete search requests).
- **Interviewer's Expectations**: Detail concurrency, cancellation, queuing, and drop behaviors.

#### 6. What is the async pipe, and why is it preferred over manual subscriptions?
- **Detailed Answer**: The `async` pipe (`{{ stream$ | async }}`) automatically subscribes to an observable in the HTML template, updates the view when new values are emitted, and unsubscribes when the component is destroyed. This prevents memory leaks from forgotten manual subscriptions.
- **Follow-up Questions**: Does the `async` pipe trigger change detection in `OnPush` components? (Answer: Yes, it calls `markForCheck()` internally when a new value is emitted).
- **Interviewer's Expectations**: Emphasize automated unsubscription and OnPush integration.

#### 7. How does Zone.js work, and what does Zoneless Angular mean?
- **Detailed Answer**: Zone.js intercepts browser asynchronous tasks (clicks, HTTP responses) and notifies Angular when they finish to trigger change detection. Zoneless Angular uses Signals to notify the framework exactly which values have changed, updating only the affected DOM nodes directly without Zone.js interception.
- **Follow-up Questions**: How do you enable Zoneless mode? (Answer: Call `provideExperimentalZonelessChangeDetection()` in the application configuration).
- **Interviewer's Expectations**: Contrast micro-task interception with fine-grained reactive updates.

#### 8. What is the difference between Reactive Forms and Template-Driven Forms?
- **Detailed Answer**: Reactive Forms are model-driven; the form structure and validators are configured in TypeScript using `FormGroup` and `FormControl`. They are type-safe and support synchronous testing. Template-driven forms rely on directive bindings in the HTML (using `ngModel`), are asynchronous, and are harder to test.
- **Follow-up Questions**: How do you handle conditional validation in Reactive Forms? (Answer: Call `setValidators()` and `updateValueAndValidity()` on the FormControl dynamically).
- **Interviewer's Expectations**: Focus on type-safety, testability, and model locations.

#### 9. What are Angular Route Guards, and how do they operate?
- **Detailed Answer**: Route Guards are interfaces used to control access to routes. They can prevent navigation to a route (`CanActivate`, `CanMatch`), check if a user can leave a route (`CanDeactivate`), or handle lazy-loading permissions (`CanLoad`). Modern guards are defined as functional expressions.
- **Follow-up Questions**: Can a route guard execute async operations? (Answer: Yes, they can return `Observable<boolean>`, `Promise<boolean>`, or plain `boolean`).
- **Interviewer's Expectations**: Detail access controls and asynchronous return types.

#### 10. Explain compilation in Angular: JIT vs AOT.
- **Detailed Answer**: JIT compiles templates in the browser at runtime; it is used for local development but results in slow startup times. Ahead-Of-Time (AOT) compiles templates to JavaScript during the build phase, catching template errors early and reducing the browser bundle size.
- **Follow-up Questions**: What is the Ivy compiler? (Answer: Angular's modern compilation engine that outputs highly optimized, tree-shakeable JavaScript code).
- **Interviewer's Expectations**: Contrast compile timings and bundle size impacts.

#### 11. Explain content projection in Angular.
- **Detailed Answer**: Content projection is a pattern where you insert custom HTML content into a child component template. This is done using the `<ng-content>` tag, which acts as a placeholder. You can project content based on CSS selectors using the `select` attribute.
- **Follow-up Questions**: What lifecycle hook targets projected content? (Answer: `ngAfterContentInit` and `ngAfterContentChecked`).
- **Interviewer's Expectations**: Detail projection placeholders and lifecycle coordinates.

#### 12. What are ViewChild and ContentChild?
- **Detailed Answer**:
  - `ViewChild`: Used to query and reference a DOM element or child component defined directly within the component's own template.
  - `ContentChild`: Used to query and reference an element or child component projected into the template via `<ng-content>`.
- **Follow-up Questions**: When do they become available? (Answer: ViewChild in `ngAfterViewInit`; ContentChild in `ngAfterContentInit`).
- **Interviewer's Expectations**: Differentiate template containment scopes.

#### 13. What is the purpose of NgZone?
- **Detailed Answer**: `NgZone` is a service that wraps Zone.js executions. It allows developers to run code outside Angular's change detection boundaries using `runOutsideAngular()`, preventing expensive redraws for tasks like continuous animation loops.
- **Follow-up Questions**: How do you re-enter Angular's change detection? (Answer: Call `run()` inside the NgZone instance).
- **Interviewer's Expectations**: Focus on performance optimizations for paint/draw tasks.

### Scenario-Based Questions

#### 14. Implement a custom structural directive to display content based on permissions.
- **Detailed Answer**: Use `ViewContainerRef` and `TemplateRef` to manipulate rendering dynamically:
  ```typescript
  @Directive({ selector: '[appHasRole]', standalone: true })
  export class HasRoleDirective {
      @Input() set appHasRole(role: string) {
          if (this.authService.hasRole(role)) {
              this.viewContainer.createEmbeddedView(this.templateRef);
          } else {
              this.viewContainer.clear();
          }
      }
      constructor(
          private templateRef: TemplateRef<any>,
          private viewContainer: ViewContainerRef,
          private authService: AuthService
      ) {}
  }
  ```
- **Follow-up Questions**: Why is it called a structural directive? (Answer: Because it alters the DOM layout directly, denoted by the `*` prefix in templates).
- **Interviewer's Expectations**: Show DI usage of `TemplateRef` and `ViewContainerRef`.

#### 15. Design an HTTP interceptor to append JWT authorization headers and handle 401 unauthorized errors.
- **Detailed Answer**:
  ```typescript
  export const authInterceptor: HttpInterceptorFn = (req, next) => {
      const authService = inject(AuthService);
      const router = inject(Router);
      const token = authService.getToken();
      
      const authReq = token ? req.clone({
          setHeaders: { Authorization: `Bearer ${token}` }
      }) : req;

      return next(authReq).pipe(
          catchError((err: HttpErrorResponse) => {
              if (err.status === 401) {
                  authService.logout();
                  router.navigate(['/login']);
              }
              return throwError(() => err);
          })
      );
  };
  ```
- **Follow-up Questions**: How is this interceptor registered? (Answer: By adding it to `provideHttpClient(withInterceptors([authInterceptor]))` in application bootstrapping).
- **Interviewer's Expectations**: Clone requests and handle errors using RxJS pipes.

#### 16. You have a performance lag on a page with a list of 1,000 complex items. How do you resolve it?
- **Detailed Answer**:
  - Implement **Virtual Scroll** using Angular CDK (`CdkVirtualScrollViewport`) to render only the items currently visible in the viewport.
  - Set `changeDetection: ChangeDetectionStrategy.OnPush` on component templates.
  - Use `trackBy` in structural iteration directives to prevent rendering items that have not changed.
- **Follow-up Questions**: What is the purpose of `trackBy`? (Answer: Tells Angular how to uniquely identify items in a list, preventing complete DOM reconstructions when elements are added or reordered).
- **Interviewer's Expectations**: Propose virtual scrolling and change detection optimizations.

#### 17. What happens if you modify a component property during change detection? How do you fix it?
- **Detailed Answer**: This throws the error `ExpressionChangedAfterItHasBeenCheckedError`. It occurs in dev mode when a property is updated *after* its containing view has been checked, violating the single-pass change detection rule. To fix it, move the state update out of lifecycle hooks like `ngAfterViewInit` to `ngOnInit`, or wrap the update in a micro-task using `Promise.resolve().then()` or `setTimeout()`.
- **Follow-up Questions**: Why does this error only happen in development mode? (Answer: Because Angular runs a second validation check in development mode to detect unstable state changes).
- **Interviewer's Expectations**: Explain the double-pass validation model and offer timing fixes.

#### 18. How do you share state across independent components in a modern zoneless Angular app?
- **Detailed Answer**: Create a singleton service containing writable signals. Components inject this service and read or update the signals:
  ```typescript
  @Injectable({ providedIn: 'root' })
  export class StoreService {
      private _state = signal<AppState>(initialState);
      public state = this._state.asReadonly();
      public updateState(updater: (state: AppState) => AppState) {
          this._state.update(updater);
      }
  }
  ```
- **Follow-up Questions**: Why use `asReadonly()`? (Answer: To prevent consumer components from mutating the internal signal state directly, forcing unidirectional updates).
- **Interviewer's Expectations**: Implement signal-based stores with unidirectional updates.

### Debugging Questions

#### 19. Debug the following component code where changes do not display in the view:
```typescript
@Component({
  selector: 'app-user',
  changeDetection: ChangeDetectionStrategy.OnPush,
  template: `<p>{{ user.name }}</p>`
})
export class UserComponent {
  @Input() user!: { name: string };
  updateName(newName: string) {
    this.user.name = newName; // UI does not update
  }
}
```
- **Detailed Answer**: The component uses `OnPush` change detection. Modifying a property of the `user` object in-place does not change the object's reference, so Angular does not run change detection.
- **Fix**: Assign a new object reference: `this.user = { ...this.user, name: newName };`.
- **Follow-up Questions**: Can we trigger change detection manually? (Answer: Yes, by injecting `ChangeDetectorRef` and calling `detectChanges()`).
- **Interviewer's Expectations**: Recognize reference mutation limits in `OnPush`.

#### 20. Debug this memory leak:
```typescript
export class LiveDataComponent implements OnInit {
  ngOnInit() {
    this.dataService.getStream().subscribe(val => {
      this.localData = val;
    });
  }
}
```
- **Detailed Answer**: The subscription to `getStream()` is opened when the component is initialized, but it is never closed. When the component is destroyed, the subscription reference remains active, leaking memory.
- **Fix**: Store the subscription and unsubscribe in `ngOnDestroy`:
  ```typescript
  private sub = new Subscription();
  ngOnInit() {
      this.sub.add(this.dataService.getStream().subscribe(val => this.localData = val));
  }
  ngOnDestroy() { this.sub.unsubscribe(); }
  ```
  Or use the RxJS `takeUntil` operator or the `async` pipe.
- **Follow-up Questions**: How can we handle this in modern Angular without lifecycle hooks? (Answer: Use `takeUntilDestroyed()` from `@angular/core/rxjs-interop`).
- **Interviewer's Expectations**: Identify subscription leaks and offer cleanup strategies.

#### 21. Why is this computed signal throwing a circular dependency error?
```typescript
val = signal(1);
comp = computed(() => {
    this.val.set(this.val() + 1); // Exception thrown
    return this.val() * 2;
});
```
- **Detailed Answer**: Computed signals must be pure read-only functions. Writing to or setting a signal inside a `computed` evaluation context triggers a circular dependency exception because it modifies the dependencies during evaluation.
- **Fix**: Remove mutators from `computed` fields; use `effect()` or standard methods instead.
- **Follow-up Questions**: Can you write to signals inside an `effect`? (Answer: By default no, unless `allowSignalWrites` is explicitly set to true in the effect configuration).
- **Interviewer's Expectations**: Enforce read-only rules for computed signals.

#### 22. Why does my custom structural directive crash during SSR builds?
```typescript
constructor(private element: ElementRef) {
    this.element.nativeElement.style.color = 'red'; // SSR crash
}
```
- **Detailed Answer**: During Server-Side Rendering (SSR), there is no real browser DOM. Accessing `nativeElement` properties directly throws exceptions because `nativeElement` is a mock structure on the server.
- **Fix**: Inject and use the `Renderer2` service instead:
  ```typescript
  constructor(private renderer: Renderer2, private element: ElementRef) {
      this.renderer.setStyle(this.element.nativeElement, 'color', 'red');
  }
  ```
- **Follow-up Questions**: What is the benefits of using Renderer2? (Answer: It abstracts DOM operations, allowing code to run safely on both server platforms and web workers).
- **Interviewer's Expectations**: Show SSR safety awareness using `Renderer2`.

#### 23. Debug why this form control validator is not updating its state:
```typescript
this.form.controls['username'].clearValidators();
// control validity remains unchanged in UI
```
- **Detailed Answer**: Calling `clearValidators()` removes the validator functions from the control, but does not re-evaluate the control's status. The control remains in its previous valid/invalid state.
- **Fix**: Call `updateValueAndValidity()` immediately after modifying validators.
- **Follow-up Questions**: Can you add validators dynamically? (Answer: Yes, using `setValidators()` followed by `updateValueAndValidity()`).
- **Interviewer's Expectations**: Call status re-evaluations after validator modifications.\n\n#### 24. What are Standalone Components and what problems do they solve?
- **Detailed Answer**: Standalone components are components that manage their own template imports directly, without needing to be declared inside an `NgModule`. This reduces boilerplate configuration, resolves circular module dependency errors, and makes components easier to reuse, lazy-load, and unit test.
- **Follow-up Questions**: How do you configure routing for standalone components? (Answer: Use `loadComponent` in routing configurations to lazy-load the component dynamically).
- **Interviewer's Expectations**: Point out the reduction of NgModule boilerplate and describe lazy-loading.

#### 25. Explain change detection strategies: Default vs OnPush.
- **Detailed Answer**: Default change detection checks the component and its children on every change detection cycle (e.g. click, scroll). `OnPush` change detection restricts checks. It only triggers when an `@Input()` reference changes, an event originates from within the component, or change detection is triggered manually via `ChangeDetectorRef.markForCheck()`.
- **Follow-up Questions**: How does changing an object property affect `OnPush`? (Answer: It does not trigger change detection because the object reference remains the same. You must pass a new object reference).
- **Interviewer's Expectations**: Describe input reference checks and the performance benefits of `OnPush`.

#### 26. What are Angular Signals and how do they differ from RxJS Observables?
- **Detailed Answer**: Signals represent state. They are synchronous, always hold a value, and track dependencies automatically when read in computed fields or templates. RxJS Observables represent asynchronous streams of events over time. Observables are not necessarily synchronous and require manual subscriptions or pipe operators to combine.
- **Follow-up Questions**: Can you combine Signals and RxJS? (Answer: Yes, using `toSignal()` to read observables as signals, and `toObservable()` to emit signal updates as streams).
- **Interviewer's Expectations**: Contrast synchronous state representations with async event streams.

#### 27. How does Dependency Injection (DI) resolve service instances?
- **Detailed Answer**: Angular uses hierarchical injectors. When a component requests a dependency, Angular searches the **Component Injector Tree** first. If not found, it traverses upwards through parent injectors, Environment Injectors (configured in routing), and finally the Root/Platform Injectors.
- **Follow-up Questions**: What is the difference between `@Injectable({ providedIn: 'root' })` and adding a service to a component's `providers` array? (Answer: `providedIn: 'root'` registers a single global instance. Adding it to `providers` creates a new instance scoped to that component and its children).
- **Interviewer's Expectations**: Detail the hierarchical lookup steps.

#### 28. Explain the difference between switchMap, mergeMap, concatMap, and exhaustMap.
- **Detailed Answer**:
  - `switchMap`: Cancels the current active inner observable when a new value is emitted by the source.
  - `mergeMap`: Executes all inner observables concurrently without waiting or cancelling.
  - `concatMap`: Queues incoming values and runs inner observables sequentially one after another.
  - `exhaustMap`: Ignores new incoming source values while the current inner observable is still executing.
- **Follow-up Questions**: Which operator is best for a search typeahead? (Answer: `switchMap`, to discard obsolete search requests).
- **Interviewer's Expectations**: Detail concurrency, cancellation, queuing, and drop behaviors.

#### 29. What is the async pipe and why is it preferred?
- **Detailed Answer**: The `async` pipe (`{{ stream$ | async }}`) automatically subscribes to an observable in the HTML template, updates the view when new values are emitted, and unsubscribes when the component is destroyed. This prevents memory leaks from forgotten manual subscriptions.
- **Follow-up Questions**: Does the `async` pipe trigger change detection in `OnPush` components? (Answer: Yes, it calls `markForCheck()` internally when a new value is emitted).
- **Interviewer's Expectations**: Emphasize automated unsubscription and OnPush integration.

#### 30. How does Zone.js work and what is Zoneless change detection?
- **Detailed Answer**: Zone.js intercepts browser asynchronous tasks (clicks, HTTP responses) and notifies Angular when they finish to trigger change detection. Zoneless Angular uses Signals to notify the framework exactly which values have changed, updating only the affected DOM nodes directly without Zone.js interception.
- **Follow-up Questions**: How do you enable Zoneless mode? (Answer: Call `provideExperimentalZonelessChangeDetection()` in the application configuration).
- **Interviewer's Expectations**: Contrast micro-task interception with fine-grained reactive updates.

#### 31. What is the difference between Reactive Forms and Template-Driven Forms?
- **Detailed Answer**: Reactive Forms are model-driven; the form structure and validators are configured in TypeScript using `FormGroup` and `FormControl`. They are type-safe and support synchronous testing. Template-driven forms rely on directive bindings in the HTML (using `ngModel`), are asynchronous, and are harder to test.
- **Follow-up Questions**: How do you handle conditional validation in Reactive Forms? (Answer: Call `setValidators()` and `updateValueAndValidity()` on the FormControl dynamically).
- **Interviewer's Expectations**: Focus on type-safety, testability, and model locations.

#### 32. What are Route Guards and how do they operate?
- **Detailed Answer**: Route Guards are interfaces used to control access to routes. They can prevent navigation to a route (`CanActivate`, `CanMatch`), check if a user can leave a route (`CanDeactivate`), or handle lazy-loading permissions (`CanLoad`). Modern guards are defined as functional expressions.
- **Follow-up Questions**: Can a route guard execute async operations? (Answer: Yes, they can return `Observable<boolean>`, `Promise<boolean>`, or plain `boolean`).
- **Interviewer's Expectations**: Detail access controls and asynchronous return types.

#### 33. Explain compilation in Angular: JIT vs AOT.
- **Detailed Answer**: JIT compiles templates in the browser at runtime; it is used for local development but results in slow startup times. Ahead-Of-Time (AOT) compiles templates to JavaScript during the build phase, catching template errors early and reducing the browser bundle size.
- **Follow-up Questions**: What is the Ivy compiler? (Answer: Angular's modern compilation engine that outputs highly optimized, tree-shakeable JavaScript code).
- **Interviewer's Expectations**: Contrast compile timings and bundle size impacts.

#### 34. What is Content Projection and how does it work?
- **Detailed Answer**: Content projection is a pattern where you insert custom HTML content into a child component template. This is done using the `<ng-content>` tag, which acts as a placeholder. You can project content based on CSS selectors using the `select` attribute.
- **Follow-up Questions**: What lifecycle hook targets projected content? (Answer: `ngAfterContentInit` and `ngAfterContentChecked`).
- **Interviewer's Expectations**: Detail projection placeholders and lifecycle coordinates.

#### 35. Explain the difference between ViewChild and ContentChild.
- **Detailed Answer**:
  - `ViewChild`: Used to query and reference a DOM element or child component defined directly within the component's own template.
  - `ContentChild`: Used to query and reference an element or child component projected into the template via `<ng-content>`.
- **Follow-up Questions**: When do they become available? (Answer: ViewChild in `ngAfterViewInit`; ContentChild in `ngAfterContentInit`).
- **Interviewer's Expectations**: Differentiate template containment scopes.

#### 36. What is the purpose of NgZone and running code outside Angular?
- **Detailed Answer**: `NgZone` is a service that wraps Zone.js executions. It allows developers to run code outside Angular's change detection boundaries using `runOutsideAngular()`, preventing expensive redraws for tasks like continuous animation loops.
- **Follow-up Questions**: How do you re-enter Angular's change detection? (Answer: Call `run()` inside the NgZone instance).
- **Interviewer's Expectations**: Focus on performance optimizations for paint/draw tasks.

#### 37. What is Ivy compilation and how does it compile templates?
- **Detailed Answer**: Ivy compiles HTML templates into incremental DOM instruction functions (like `ɵɵelementStart`, `ɵɵtext`). During runtime change detection, Angular executes these functions directly against the DOM nodes, skipping virtual DOM diffing.
- **Follow-up Questions**: What is the main benefit of Ivy? (Answer: Extremely small, tree-shakeable bundle sizes because unused rendering instructions are excluded from build outputs).
- **Interviewer's Expectations**: Detail compilation steps and tree-shaking benefits.

#### 38. Explain how to implement a custom structural directive.
- **Detailed Answer**: Create a class decorated with `@Directive` and inject `TemplateRef` and `ViewContainerRef`. Use inputs to control the rendering logic, calling `createEmbeddedView()` or `clear()` on the container.
- **Follow-up Questions**: What does the asterisk (`*`) prefix signify in HTML templates? (Answer: It is syntactic sugar that wraps the element in an `<ng-template>` container).
- **Interviewer's Expectations**: Show DI usage of `TemplateRef` and `ViewContainerRef`.

#### 39. How do you secure templates during SSR builds?
- **Detailed Answer**: Avoid direct accesses to DOM variables (like `window` or `document`) since they do not exist on the server. Inject and use the `Renderer2` abstraction class, or wrap browser-specific statements inside `isPlatformBrowser` checks.
- **Follow-up Questions**: What service identifies the platform? (Answer: Inject the `PLATFORM_ID` token).
- **Interviewer's Expectations**: Highlight platform check utilities.

#### 40. What is a dynamic modal service design in Angular?
- **Detailed Answer**: Create a singleton service that dynamically instantiates components at runtime. Use `ViewContainerRef.createComponent()` to create the component, insert it into the root overlay DOM, and return a reference containing close handles.
- **Follow-up Questions**: How do you pass data? (Answer: Create custom injectors passing data tokens during instantiation).
- **Interviewer's Expectations**: Detail component creation via containers.\n\n\n\n#### 41. What are Standalone Components and what problems do they solve?
- **Detailed Answer**: Standalone components manage their own template imports directly, without needing to be declared inside an `NgModule`. This reduces boilerplate configuration, resolves circular module dependency errors, and makes components easier to reuse, lazy-load, and unit test.
- **Follow-up Questions**: How do you configure routing for standalone components? (Answer: Use `loadComponent` in routing configurations to lazy-load the component dynamically).
- **Interviewer's Expectations**: Point out the reduction of NgModule boilerplate and describe lazy-loading.

#### 42. Explain change detection strategies: Default vs OnPush.
- **Detailed Answer**: Default change detection checks the component and its children on every change detection cycle. `OnPush` change detection restricts checks, triggering only when an `@Input()` reference changes, an event originates from within the component, or change detection is triggered manually.
- **Follow-up Questions**: How does changing an object property affect `OnPush`? (Answer: It does not trigger change detection because the object reference remains the same. You must pass a new object reference).
- **Interviewer's Expectations**: Describe input reference checks and the performance benefits of `OnPush`.

#### 43. What are Angular Signals and how do they differ from RxJS Observables?
- **Detailed Answer**: Signals represent state. They are synchronous, always hold a value, and track dependencies automatically when read in computed fields or templates. RxJS Observables represent asynchronous streams of events over time. Observables are not necessarily synchronous and require manual subscriptions or pipe operators to combine.
- **Follow-up Questions**: Can you combine Signals and RxJS? (Answer: Yes, using `toSignal()` to read observables as signals, and `toObservable()` to emit signal updates as streams).
- **Interviewer's Expectations**: Contrast synchronous state representations with async event streams.

#### 44. How does Dependency Injection (DI) resolve service instances?
- **Detailed Answer**: Angular uses hierarchical injectors. When a component requests a dependency, Angular searches the Component Injector Tree first. If not found, it traverses upwards through parent injectors, Environment Injectors (configured in routing), and finally the Root/Platform Injectors.
- **Follow-up Questions**: What is the difference between `@Injectable({ providedIn: 'root' })` and adding a service to a component's `providers` array? (Answer: `providedIn: 'root'` registers a single global instance. Adding it to `providers` creates a new instance scoped to that component and its children).
- **Interviewer's Expectations**: Detail the hierarchical lookup steps.

#### 45. Explain the difference between switchMap, mergeMap, concatMap, and exhaustMap.
- **Detailed Answer**:
  - `switchMap`: Cancels the current active inner observable when a new value is emitted by the source.
  - `mergeMap`: Executes all inner observables concurrently without waiting or cancelling.
  - `concatMap`: Queues incoming values and runs inner observables sequentially one after another.
  - `exhaustMap`: Ignores new incoming source values while the current inner observable is still executing.
- **Follow-up Questions**: Which operator is best for a search typeahead? (Answer: `switchMap`, to discard obsolete search requests).
- **Interviewer's Expectations**: Detail concurrency, cancellation, queuing, and drop behaviors.

#### 46. What is the async pipe and why is it preferred?
- **Detailed Answer**: The `async` pipe (`{{ stream$ | async }}`) automatically subscribes to an observable in the HTML template, updates the view when new values are emitted, and unsubscribes when the component is destroyed. This prevents memory leaks from forgotten manual subscriptions.
- **Follow-up Questions**: Does the `async` pipe trigger change detection in `OnPush` components? (Answer: Yes, it calls `markForCheck()` internally when a new value is emitted).
- **Interviewer's Expectations**: Emphasize automated unsubscription and OnPush integration.

#### 47. How does Zone.js work and what is Zoneless change detection?
- **Detailed Answer**: Zone.js intercepts browser asynchronous tasks (clicks, HTTP responses) and notifies Angular when they finish to trigger change detection. Zoneless Angular uses Signals to notify the framework exactly which values have changed, updating only the affected DOM nodes directly without Zone.js interception.
- **Follow-up Questions**: How do you enable Zoneless mode? (Answer: Call `provideExperimentalZonelessChangeDetection()` in the application configuration).
- **Interviewer's Expectations**: Contrast micro-task interception with fine-grained reactive updates.

#### 48. What is the difference between Reactive Forms and Template-Driven Forms?
- **Detailed Answer**: Reactive Forms are model-driven; the form structure and validators are configured in TypeScript using `FormGroup` and `FormControl`. They are type-safe and support synchronous testing. Template-driven forms rely on directive bindings in the HTML (using `ngModel`), are asynchronous, and are harder to test.
- **Follow-up Questions**: How do you handle conditional validation in Reactive Forms? (Answer: Call `setValidators()` and `updateValueAndValidity()` on the FormControl dynamically).
- **Interviewer's Expectations**: Focus on type-safety, testability, and model locations.

#### 49. What are Route Guards and how do they operate?
- **Detailed Answer**: Route Guards are interfaces used to control access to routes. They can prevent navigation to a route (`CanActivate`, `CanMatch`), check if a user can leave a route (`CanDeactivate`), or handle lazy-loading permissions (`CanLoad`). Modern guards are defined as functional expressions.
- **Follow-up Questions**: Can a route guard execute async operations? (Answer: Yes, they can return `Observable<boolean>`, `Promise<boolean>`, or plain `boolean`).
- **Interviewer's Expectations**: Detail access controls and asynchronous return types.

#### 50. Explain compilation in Angular: JIT vs AOT.
- **Detailed Answer**: JIT compiles templates in the browser at runtime; it is used for local development but results in slow startup times. Ahead-Of-Time (AOT) compiles templates to JavaScript during the build phase, catching template errors early and reducing the browser bundle size.
- **Follow-up Questions**: What is the Ivy compiler? (Answer: Angular's modern compilation engine that outputs highly optimized, tree-shakeable JavaScript code).
- **Interviewer's Expectations**: Contrast compile timings and bundle size impacts.

#### 51. What is Content Projection and how does it work?
- **Detailed Answer**: Content projection is a pattern where you insert custom HTML content into a child component template. This is done using the `<ng-content>` tag, which acts as a placeholder. You can project content based on CSS selectors using the `select` attribute.
- **Follow-up Questions**: What lifecycle hook targets projected content? (Answer: `ngAfterContentInit` and `ngAfterContentChecked`).
- **Interviewer's Expectations**: Detail projection placeholders and lifecycle coordinates.

#### 52. Explain the difference between ViewChild and ContentChild.
- **Detailed Answer**:
  - `ViewChild`: Used to query and reference a DOM element or child component defined directly within the component's own template.
  - `ContentChild`: Used to query and reference an element or child component projected into the template via `<ng-content>`.
- **Follow-up Questions**: When do they become available? (Answer: ViewChild in `ngAfterViewInit`; ContentChild in `ngAfterContentInit`).
- **Interviewer's Expectations**: Differentiate template containment scopes.

#### 53. What is the purpose of NgZone and running code outside Angular?
- **Detailed Answer**: `NgZone` is a service that wraps Zone.js executions. It allows developers to run code outside Angular's change detection boundaries using `runOutsideAngular()`, preventing expensive redraws for tasks like continuous animation loops.
- **Follow-up Questions**: How do you re-enter Angular's change detection? (Answer: Call `run()` inside the NgZone instance).
- **Interviewer's Expectations**: Focus on performance optimizations for paint/draw tasks.

#### 54. What is Ivy compilation and how does it compile templates?
- **Detailed Answer**: Ivy compiles HTML templates into incremental DOM instruction functions (like `ɵɵelementStart`, `ɵɵtext`). During runtime change detection, Angular executes these functions directly against the DOM nodes, skipping virtual DOM diffing.
- **Follow-up Questions**: What is the main benefit of Ivy? (Answer: Extremely small, tree-shakeable bundle sizes because unused rendering instructions are excluded from build outputs).
- **Interviewer's Expectations**: Detail compilation steps and tree-shaking benefits.

#### 55. Explain how to implement a custom structural directive.
- **Detailed Answer**: Create a class decorated with `@Directive` and inject `TemplateRef` and `ViewContainerRef`. Use inputs to control the rendering logic, calling `createEmbeddedView()` or `clear()` on the container.
- **Follow-up Questions**: What does the asterisk (`*`) prefix signify in HTML templates? (Answer: It is syntactic sugar that wraps the element in an `<ng-template>` container).
- **Interviewer's Expectations**: Show DI usage of `TemplateRef` and `ViewContainerRef`.

#### 56. How do you secure templates during SSR builds?
- **Detailed Answer**: Avoid direct accesses to DOM variables (like `window` or `document`) since they do not exist on the server. Inject and use the `Renderer2` abstraction class, or wrap browser-specific statements inside `isPlatformBrowser` checks.
- **Follow-up Questions**: What service identifies the platform? (Answer: Inject the `PLATFORM_ID` token).
- **Interviewer's Expectations**: Highlight platform check utilities.

#### 57. What is a dynamic modal service design in Angular?
- **Detailed Answer**: Create a singleton service that dynamically instantiates components at runtime. Use `ViewContainerRef.createComponent()` to create the component, insert it into the root overlay DOM, and return a reference containing close handles.
- **Follow-up Questions**: How do you pass data? (Answer: Create custom injectors passing data tokens during instantiation).
- **Interviewer's Expectations**: Detail component creation via containers.

#### 58. Explain the difference between NgModules and Standalone Components.
- **Detailed Answer**: NgModules bundle components, directives, and pipes together in a logical namespace, which must be imported as a whole. Standalone components declare their own dependencies individually, bypassing NgModules entirely.
- **Follow-up Questions**: Can you mix standalone components in legacy modules? (Answer: Yes, standalone components can be imported into the `imports` array of an `NgModule`).
- **Interviewer's Expectations**: Contrast namespace modularity with individual dependency declarations.

#### 59. What are template variables, and how are they referenced?
- **Detailed Answer**: Template variables (denoted by the hash symbol, e.g., `#myInput`) allow referencing a DOM element or child component instance directly inside the HTML template or querying it from the TypeScript file using `@ViewChild`.
- **Follow-up Questions**: How do you read the value of a template variable? (Answer: Access it directly in the template: `myInput.value`).
- **Interviewer's Expectations**: Detail template reference syntax and TypeScript queries.

#### 60. How does Angular handle router preloading strategies?
- **Detailed Answer**: Preloading strategies allow Angular to load lazy-routed component bundles in the background after the initial page renders, preventing navigation delays. Built-in strategies include `PreloadAllModules` or custom strategies based on network latency.
- **Follow-up Questions**: Write a basic preload configuration. (Answer: Pass `withPreloading(PreloadAllModules)` to the `provideRouter` application configuration).
- **Interviewer's Expectations**: Explain lazy-loading enhancements and background module fetches.\n\n

#### 61. What are Angular Signals and how do they differ from RxJS Observables?
- **Detailed Answer**: Angular Signals (introduced in Angular 16) are a reactive primitive representing a value that notifies consumers when it changes. Signals are synchronous and track dependencies automatically using runtime read executions. RxJS Observables are asynchronous streams that require explicit subscription registrations and tear-down logic. Signals are optimized for synchronous state tracking and UI rendering, while Observables remain preferred for asynchronous event handling and HTTP streams.
- **Follow-up Questions**: How do you read a Signal? (Answer: By calling it as a function: `mySignal()`).
- **Interviewer's Expectations**: Contrast synchronous reactivity with asynchronous streams, and explain dependency tracking.

#### 62. Explain Angular's Change Detection zones and the performance impact of runOutsideAngular.
- **Detailed Answer**: Angular uses Zone.js to intercept asynchronous operations (timers, HTTP requests, clicks). When an async task completes, Zone.js triggers change detection across the entire component tree, updating the UI. For performance-intensive calculations (like canvas animations or mouse movement listeners), this constant UI checking causes rendering lag. You optimize this by executing tasks using `NgZone.runOutsideAngular(() => { ... })`, which runs the code without triggering change detection passes.
- **Follow-up Questions**: How do you trigger change detection manually after running code outside the zone? (Answer: Inject `ChangeDetectorRef` and call `detectChanges()`).
- **Interviewer's Expectations**: Detail Zone.js interceptions, tree traversals, and runOutsideAngular use cases.

#### 63. How does Angular's Router execute Resolvers and Guards during page transition cycles?
- **Detailed Answer**: When a user navigates to a route, Angular's Router executes checks in a strict sequence:
  1. **Guards (CanMatch, CanActivate)**: Verify if the user is authorized to access the route. If a guard returns false, navigation is canceled.
  2. **Resolvers**: Fetch required data asynchronously before the component is instantiated. The router waits for the resolver's observable to complete, passing the data as route data, preventing page flashes.
- **Follow-up Questions**: What is the difference between `CanActivate` and `CanActivateChild`? (Answer: `CanActivate` runs on the parent route; `CanActivateChild` runs on all nested child routes).
- **Interviewer's Expectations**: Detail the execution sequence and explain data-binding benefits of resolvers.

#### 64. Explain the difference between ComponentProvider and ModuleProvider scoping rules in Angular.
- **Detailed Answer**: Angular uses a hierarchical Dependency Injection system:
  - **ModuleProvider (or root provider)**: Registered in `@Injectable({ providedIn: 'root' })` or module declarations. It creates a single service instance shared globally across all components.
  - **ComponentProvider**: Registered in a component's `@Component({ providers: [...] })` metadata. It scopes the service instance to that specific component and its child instances, creating a new instance every time the component is mounted.
- **Follow-up Questions**: What happens if a component provider shares a name with a module provider? (Answer: The component-level provider overrides the module provider for that component branch (shadowing)).
- **Interviewer's Expectations**: Explain injector hierarchies, instantiation scopes, and provider overrides.

#### 65. What is Angular's deferrable views (@defer) and how does it optimize bundle sizes?
- **Detailed Answer**: Deferrable views (introduced in Angular 17) allow developers to lazy-load components, directives, and pipes inside template files using the `@defer` syntax. When a defer block is triggered (e.g. `@defer (on viewport)`), Angular fetches the component's bundle over the network and renders it dynamically. This splits the code into separate chunks, decreasing initial bundle sizes and improving page load speeds.
- **Follow-up Questions**: What are the sub-blocks of a `@defer` block? (Answer: `@loading` (placeholder shown while fetching), `@placeholder` (shown before trigger), and `@error` (shown if loading fails)).
- **Interviewer's Expectations**: Show trigger options and describe code-splitting mechanics.

---

## 10. Common Mistakes
- **Direct DOM Manipulation**: Bypassing Angular templates to mutate element structures directly.
- **Heavy functions in HTML templates**: Executing complex logic inside `{{ heavyFunction() }}` bindings.
- **Observable Memory Leaks**: Forgetting to clean up open subscriptions in components.
- **Nested subscriptions**: Subscribing to an observable inside another subscription instead of using pipe operators like `switchMap`.
- **Forgetting trackBy**: Causing complete list rerenders during pagination changes.

---

## 11. Comparison Section: Angular vs React vs Vue

| Feature | Angular | React | Vue |
|---|---|---|---|
| **Architecture** | Opinionated Framework | Library (View-only) | Hybrid / Progressive Framework |
| **Language** | TypeScript (Required) | JavaScript / JSX | HTML / JavaScript / Single File Components |
| **Reactivity** | Signals & RxJS | Virtual DOM diffing | Reactive proxy bindings |
| **Forms & Routing** | Built-in out of the box | Requires external packages | Third-party standard packages |
| **Change Detection** | Directional tree search | Explicit State triggers | Proxy mutations |

---

## 12. Practical Project Ideas
- **Beginner**: A dynamic weather widget displaying forecasts using Pipes and API services.
- **Intermediate**: A task management board with drag-and-drop lists, standalone routing, and Reactive Forms.
- **Advanced**: A multi-user chat shell utilizing WebSockets, RxJS message buffering, offline IndexedDB storage, and Signals.

---

## 13. Internship Preparation Notes
- **Focus Areas**: Standalone Components, data binding syntax, Reactive Forms, and RxJS Observables.
- **Key Check**: Explain how inputs (`@Input()`) and outputs (`@Output()`) pass data between components.
- **Practical Check**: Write a basic service fetching mock data from an API.

---

## 14. Cheat Sheet
- **Signal Definition**: `val = signal(0);`
- **Signal Modification**: `val.update(n => n + 1);`
- **Computed Value**: `comp = computed(() => val() * 2);`
- **Router guard registration**: `canActivate: [authGuard]`

---

## 15. One-Day Revision Guide
- [ ] Differentiate default vs `OnPush` change detection.
- [ ] Write a basic standalone component.
- [ ] Explain how Signals trace dependencies automatically.
- [ ] Differentiate `switchMap` and `mergeMap`.
- [ ] Explain how to resolve `ExpressionChangedAfterItHasBeenCheckedError`.
- [ ] Detail Angular route guard lifecycles.
- [ ] Compare Angular and React architecture.
