# 32. HTML5 (Modern Web Markup)

## 1. Introduction

### What it is
HTML5 is the fifth and current major version of the Hypertext Markup Language (HTML), the standard XML-compliant markup language used to structure web content. HTML5 is more than a markup language; it represents a unified application platform that combines semantic syntax with browser-level API standards for graphics, storage, background processing, and media streaming.

### Why it exists
Historically, HTML4 was designed primarily for static document structures. When the web transitioned to dynamic applications, browsers lacked native support for video streaming, local databases, complex animations, and vector graphics. Developers relied on proprietary browser plugins (e.g. Adobe Flash, Microsoft Silverlight) to fill these gaps. These plugins were prone to security exploits, caused system instability, and were incompatible with mobile devices. HTML5 was developed to eliminate plugin dependencies by introducing native browser APIs for multimedia, storage, and graphics.

### Problems it solves
- **Plugin Dependencies**: Replaces Flash with native `<video>` and `<audio>` tags.
- **Div Soup Layouts**: Replaces generic `<div>` hierarchies with semantic tags (like `<article>`, `<main>`), improving machine readability, SEO, and accessibility.
- **No Native Client Storage**: Replaces limited 4KB cookies with 5MB+ Web Storage (LocalStorage/SessionStorage) and transactional client-side databases (IndexedDB).
- **Single-Threaded Bottlenecks**: Allows running long-running operations in background threads using **Web Workers**, preventing scripts from locking the browser's UI thread.
- **Lack of Real-time communication**: Replaces expensive polling with native bidirectional protocols like WebSockets.

### Industry Use Cases
- **Progressive Web Applications (PWAs)**: Using Service Workers to cache resources and allow applications to run offline.
- **Media Streaming Players**: Platforms like YouTube and Netflix use HTML5 media structures (MSE - Media Source Extensions) to stream adaptive HD video.
- **Browser-based Gaming**: Using the `<canvas>` API and WebGL to render 2D and 3D graphics at 60 FPS without plugins.
- **Accessible Enterprise Dashboards**: Enforcing Web Content Accessibility Guidelines (WCAG) using semantic layout landmarks and ARIA roles for screen readers.

### Analogy
HTML4 was like a static notice board: you could pin paper documents, text, and images, but if you wanted to play video or run interactive programs, you had to install separate projection systems (plugins) next to the board. HTML5 is an interactive digital screen workstation. The screen plays video natively, renders drawings, saves user data, runs background processes, and connects to sensors without needing external plugins.

---

## 2. Core Concepts

### Beginner Concepts
- **Document Structure**: Every HTML5 document begins with the `<!DOCTYPE html>` declaration, which forces the browser to run in Standards Mode. The document is nested inside `<html>`, divided into `<head>` (metadata, CSS/JS links) and `<body>` (rendered content).
- **Semantic Layout Landmarks**:
  - `<header>`: Contains introductory content, logos, or site navigation.
  - `<nav>`: Holds navigation link blocks.
  - `<main>`: Encloses the unique, central content of the document.
  - `<article>`: Represents self-contained, reusable content (e.g., blog posts, cards).
  - `<section>`: Groups related content elements.
  - `<aside>`: Holds secondary, sidebar-style content.
  - `<footer>`: Contains author, copyright, and contact details.
- **Inline vs. Block Elements**:
  - **Block Elements** (e.g., `<div>`, `<p>`, `<main>`) start on a new line and stretch to occupy the full width of their parent container.
  - **Inline Elements** (e.g., `<span>`, `<a>`, `<strong>`) do not start on a new line and occupy only the width of their content.

### Intermediate Concepts
- **Constraint validation forms**: Native HTML5 inputs (e.g., `<input type="email">`, `<input type="number" min="10" max="100">`) enforce input validation rules directly in the browser, reducing the need for custom JavaScript validation scripts.
- **Canvas 2D API**: A programmatic drawing canvas (`<canvas>`) exposed via JavaScript, used to draw shapes, paths, text, images, and compile animations pixel-by-pixel.
- **SVG (Scalable Vector Graphics)**: XML-based vector graphic definitions embedded directly in the HTML DOM, enabling lossless resolution scaling and styling via CSS.
- **Web Storage (LocalStorage & SessionStorage)**: Key-value storage. LocalStorage persists data permanently across browser restarts; SessionStorage keeps data active only for the duration of the browser tab session.
- **History API**: Allows modifying the browser URL and history stack programmatically (`history.pushState()`) without triggering full page reloads, serving as the foundation of Single-Page Application (SPA) routers.
- **Web Accessibility (A11y) & ARIA**: Structuring markup so assistive technologies can read it. Enforced using `aria-*` attributes (e.g. `aria-label`, `aria-describedby`) and landmark roles to map DOM elements to accessibility APIs.

### Advanced Concepts
- **Web Workers**: Independent background JavaScript execution threads running in a separate OS thread, allowing calculations to execute without blocking the main UI thread.
- **Service Workers**: Event-driven network proxy scripts registered in the browser. They intercept network requests, manage cache storage, and enable offline execution and push notifications.
- **WebSockets**: A protocol providing persistent, full-duplex communication channels over a single TCP connection, replacing HTTP polling for real-time applications.
- **Web Components**: A suite of technologies allowing developers to create reusable, custom HTML tags:
  - **Custom Elements**: Defining custom elements (e.g. `<user-card>`) and their lifecycles.
  - **Shadow DOM**: Encapsulating component styles and structures, preventing CSS styles from leaking out.
  - **HTML Templates**: Storing reusable chunks of markup (`<template>`) that are not rendered until instantiated by JavaScript.
- **Intersection Observer API**: An API that monitors when a target element enters or exits the browser viewport, used to implement lazy loading for images or trigger scroll animations.

---

## 3. Internal Working

### The Critical Rendering Path (CRP)
The Critical Rendering Path is the sequence of steps the browser takes to convert raw HTML, CSS, and JavaScript bytes into physical pixels on the user's screen.

```text
+-------------------+
|  HTML Bytes Received |
+-------------------+
         |
         v Parsing / Tokenization
+-------------------+      +-------------------+
|     DOM Tree      |      |    CSSOM Tree     |
+-------------------+      +-------------------+
         |                           |
         +-------------+-------------+
                       | Combine Trees
                       v
               +---------------+
               |  Render Tree  | (Contains visible nodes only)
               +---------------+
                       |
                       v Layout / Reflow (Compute geometry)
               +---------------+
               |    Layout     |
               +---------------+
                       |
                       v Paint (Fill pixels)
               +---------------+
               |     Paint     |
               +---------------+
                       |
                       v Compositing (Combine GPU layers)
               +---------------+
               |  Compositing  |
               +---------------+
```

1. **DOM Construction**: The browser parses HTML bytes, translates them to characters, tokens, and nodes, building the **Document Object Model (DOM)** tree.
2. **CSSOM Construction**: The browser parses CSS stylesheets to build the **CSS Object Model (CSSOM)** tree.
3. **Render Tree**: The DOM and CSSOM are combined into a **Render Tree**. The Render Tree includes only visible elements (nodes set to `display: none` are omitted).
4. **Layout (Reflow)**: The browser calculates the exact geometry, position, and dimensions of each visible node on the screen.
5. **Paint**: The browser fills in pixels (colors, text, images, borders) across visual layers.
6. **Compositing**: The browser sends the independent layers to the GPU to be combined and rendered on the screen, ensuring smooth scrolling and animations.

### HTML5 Tokenization and Parsing
The HTML5 parser is error-tolerant, designed to parse malformed markup consistently across all browsers without crashing.
- **Tokenizer**: A state machine that reads characters and emits tokens (StartTag, EndTag, Character, Comment).
- **Tree Construction**: The parser reads tokens and builds the DOM tree. If it encounters malformed HTML (e.g. `<div><p>Hello</div></p>`), the parser uses spec-defined error correction rules to close the `<p>` tag automatically when it reaches `</div>`, preventing layout rendering failure.

### Script Loading: Default vs. Async vs. Defer
When the HTML parser encounters a `<script>` tag, its behavior varies based on the attributes declared:

```text
Default:
Parsing HTML   |=========[Block Parser]===================>
Script Down    |---------[Download]
Script Exec    |                   [Exec]

Async:
Parsing HTML   |=========[Block Exec]=====================>
Script Down    |---------[Download]
Script Exec    |                   [Exec]

Defer:
Parsing HTML   |==========================================>
Script Down    |---------[Download]
Script Exec    |                                          [Exec]
```

- **Default (`<script src="...">`)**: The parser halts HTML parsing, downloads the script, executes it, and then resumes parsing. This blocks page rendering.
- **Async (`<script async src="...">`)**: The browser downloads the script in the background while the HTML parser continues. Once the script is downloaded, the parser pauses to execute the script immediately. It is ideal for independent scripts (e.g. analytics).
- **Defer (`<script defer src="...">`)**: The browser downloads the script in the background while the HTML parser continues. The script is executed only after the HTML parser completes. It is ideal for scripts that manipulate the DOM and depend on other files.

---

## 4. Important Terminology

- **HTML5**: Standard markup language for structuring web applications.
- **DOM (Document Object Model)**: The programmatic interface representing HTML documents as a tree of nodes.
- **CSSOM (CSS Object Model)**: The tree structure representing CSS rules and styles.
- **Semantic HTML**: Using tags that describe their content's purpose (e.g., `<article>`) instead of generic wrappers.
- **ARIA (Accessible Rich Internet Applications)**: Specification defining attributes to make web content accessible.
- **WCAG (Web Content Accessibility Guidelines)**: Standard guidelines for web accessibility.
- **Landmark Roles**: ARIA roles identifying structural page regions (e.g., `role="navigation"`).
- **Constraint Validation**: Browser-native form validation using input attributes.
- **Canvas API**: Procedural 2D graphics rendering interface.
- **SVG (Scalable Vector Graphics)**: XML-based vector image format integrated into the DOM.
- **Web Worker**: Background thread running complex calculations without blocking the main UI thread.
- **Service Worker**: Event-driven network proxy enabling offline caching and push notifications.
- **Web Components**: Standard suite for creating encapsulated, custom HTML tags.
- **Shadow DOM**: Encapsulated DOM subtree isolated from main document styling.
- **Intersection Observer**: API tracking when elements enter or exit the viewport.
- **Quirks Mode**: Browser compatibility mode mimicking legacy IE rendering behavior.
- **Standards Mode**: Default HTML5 rendering mode adhering to modern web standards.
- **Critical Rendering Path (CRP)**: Sequence of steps translating code into pixels on screen.
- **Reflow**: Recalculating the layout geometry of DOM elements.
- **Repaint**: Re-drawing pixels on screen after layout changes.
- **WebSockets**: Persistent, bidirectional TCP protocol for real-time web communication.
- **WebRTC**: Real-time communication protocol for peer-to-peer audio and video streaming.
- **IndexedDB**: Transactional, client-side Object database for storing large datasets.

---

## 5. Beginner Examples

### Example 1: Full Semantic Page Layout
A search engine-optimized page layout implementing semantic tags and accessibility guidelines.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <!-- Critical for responsive mobile view scaling -->
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Corporate Customer Portal</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>

  <!-- Site-wide header landmark -->
  <header>
    <h1>Enterprise Systems</h1>
    <nav aria-label="Primary Navigation">
      <ul>
        <li><a href="/dashboard">Dashboard</a></li>
        <li><a href="/profile">Profile</a></li>
      </ul>
    </nav>
  </header>

  <!-- Unique page content landmark -->
  <main id="main-content">
    <article>
      <header>
        <h2>Quarterly Performance Review</h2>
        <p>Published on: <time datetime="2026-06-11">June 11, 2026</time></p>
      </header>
      <p>Our operational throughput increased by 15% due to optimized database indexing.</p>
    </article>

    <!-- Sidebar landmark containing related references -->
    <aside aria-label="Reference Links">
      <h3>Quick Links</h3>
      <ul>
        <li><a href="/kb/database-tuning">Database Tuning Guide</a></li>
      </ul>
    </aside>
  </main>

  <!-- Site-wide footer landmark -->
  <footer>
    <p>&copy; 2026 Enterprise Systems. All rights reserved.</p>
  </footer>

</body>
</html>
```

### Example 2: Accessible Form with Native Constraint Validation
Using native HTML5 validators to secure input layouts before JavaScript processing.

```html
<!-- novalidate can be set if custom JS validation is desired instead -->
<form action="/api/v1/users" method="POST" id="registration-form">
  
  <!-- Associated label ensures screen reader accessibility -->
  <div class="form-group">
    <label for="user-email">Email Address (Required):</label>
    <input 
      type="email" 
      id="user-email" 
      name="email" 
      required 
      placeholder="user@domain.com"
      aria-required="true"
    >
  </div>

  <div class="form-group">
    <label for="username">Username (5-12 alphanumeric characters):</label>
    <input 
      type="text" 
      id="username" 
      name="username" 
      required
      pattern="^[a-zA-Z0-9]{5,12}$"
      title="Username must be 5 to 12 alphanumeric characters."
    >
  </div>

  <div class="form-group">
    <label for="user-age">Age (Must be at least 18):</label>
    <input 
      type="number" 
      id="user-age" 
      name="age" 
      min="18" 
      max="120"
    >
  </div>

  <button type="submit">Submit Registration</button>
</form>
```

### Example 3: Video Element with Multi-Source Fallbacks
Embedding native media players with fallbacks for unsupported legacy browsers.

```html
<video width="640" height="360" controls poster="images/poster_preview.jpg">
  <!-- Browser plays the first compatible file format -->
  <source src="media/promo_video.webm" type="video/webm">
  <source src="media/promo_video.mp4" type="video/mp4">
  
  <!-- Fallback message displayed only if browser lacks native support -->
  <p>
    Your browser does not support native HTML5 video. 
    Please download the file: <a href="media/promo_video.mp4">Download MP4</a>.
  </p>
</video>
```

---

## 6. Intermediate Examples

### Example 1: Canvas Drawing Application
Rendering a dynamic bar chart using the HTML5 Canvas 2D API and JavaScript.

```html
<canvas id="metrics-chart" width="400" height="200" style="border:1px solid #ddd;"></canvas>

<script>
  const canvas = document.getElementById("metrics-chart");
  const ctx = canvas.getContext("2d");

  // Chart data representation
  const chartData = [120, 80, 160, 90, 140];
  const barWidth = 40;
  const barSpacing = 20;
  const startX = 50;

  // Clear canvas background
  ctx.fillStyle = "#f9f9f9";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Draw chart bars
  chartData.forEach((value, index) => {
      // Set bar color based on value thresholds
      ctx.fillStyle = value > 100 ? "#2563eb" : "#93c5fd";
      
      const x = startX + index * (barWidth + barSpacing);
      // Invert Y coordinate since Canvas origin (0,0) starts at top-left
      const y = canvas.height - value;
      
      ctx.fillRect(x, y, barWidth, value);
      
      // Draw text label on top of each bar
      ctx.fillStyle = "#1e293b";
      ctx.font = "12px Arial";
      ctx.fillText(value.toString(), x + 10, y - 5);
  });
</script>
```

### Example 2: Client-side SPA Router utilizing the History API
Updating URLs and browser states without triggering full-page server requests.

```html
<nav id="spa-nav">
  <a href="/home" data-route="home">Home</a> | 
  <a href="/dashboard" data-route="dashboard">Dashboard</a>
</nav>

<div id="app-view"><h2>Home View</h2></div>

<script>
  const appView = document.getElementById("app-view");
  
  // Map routes to display content
  const viewMap = {
      home: "<h2>Home View</h2><p>Welcome to our main single page app.</p>",
      dashboard: "<h2>Dashboard View</h2><p>Here are your operations metrics.</p>"
  };

  document.getElementById("spa-nav").addEventListener("click", (e) => {
      if (e.target.tagName === "A") {
          e.preventDefault();
          const route = e.target.getAttribute("data-route");
          const targetUrl = e.target.getAttribute("href");
          
          // Update the browser's URL and history stack programmatically
          history.pushState({ view: route }, "", targetUrl);
          
          // Render the new view content dynamically
          renderView(route);
      }
  });

  // Handle browser back and forward button clicks
  window.addEventListener("popstate", (e) => {
      const route = e.state ? e.state.view : "home";
      renderView(route);
  });

  function renderView(viewName) {
      appView.innerHTML = viewMap[viewName] || "<h2>404 View Not Found</h2>";
  }
</script>
```

### Example 3: Client-side storage using IndexedDB
An in-browser database wrapper for storing structured objects.

```javascript
// Open database connection
const dbRequest = indexedDB.open("InventoryDB", 1);
let database = null;

dbRequest.onupgradeneeded = (e) => {
    database = e.target.result;
    // Create an object store with auto-incrementing IDs
    database.createObjectStore("items", { keyPath: "id", autoIncrement: true });
};

dbRequest.onsuccess = (e) => {
    database = e.target.result;
    console.log("Database opened successfully.");
};

function addItemToDatabase(name, quantity) {
    // Start a readwrite transaction
    const transaction = database.transaction(["items"], "readwrite");
    const store = transaction.objectStore("items");
    
    const itemRecord = { name, quantity, timestamp: Date.now() };
    const addRequest = store.add(itemRecord);
    
    addRequest.onsuccess = () => {
        console.log("Item saved successfully. ID:", addRequest.result);
    };
}
```

---

## 7. Advanced Examples & Concepts

### Example 1: Service Worker for Offline-First Caching
A complete script registering and executing a Service Worker to intercept network requests and cache static assets for offline execution.

**File: `app.js` (Main Thread registration)**
```javascript
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js")
            .then(reg => console.log("Service Worker registered. Scope:", reg.scope))
            .catch(err => console.error("Service Worker registration failed:", err));
    });
}
```

**File: `sw.js` (Service Worker file)**
```javascript
const CACHE_NAME = "assets-cache-v1";
const STATIC_ASSETS = [
    "/",
    "/index.html",
    "/styles.css",
    "/app.js",
    "/images/fallback_logo.png"
];

// 1. Install event: Cache static assets
self.addEventListener("install", (e) => {
    e.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log("Pre-caching application assets...");
                return cache.addAll(STATIC_ASSETS);
            })
            .then(() => self.skipWaiting()) // Force active state immediately
    );
});

// 2. Activate event: Clean up old caches
self.addEventListener("activate", (e) => {
    e.waitUntil(
        caches.keys().then(keys => {
            return Promise.all(
                keys.map(key => {
                    if (key !== CACHE_NAME) {
                        console.log("Clearing outdated cache: ", key);
                        return caches.delete(key);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// 3. Fetch event: Intercept network requests (Cache-first with network fallback)
self.addEventListener("fetch", (e) => {
    e.respondWith(
        caches.match(e.request).then(cachedResponse => {
            // Return cached response if present, otherwise fetch from network
            return cachedResponse || fetch(e.request).then(networkResponse => {
                // Return network response
                return networkResponse;
            });
        }).catch(() => {
            // Return fallback asset if offline and network request fails
            if (e.request.destination === "image") {
                return caches.match("/images/fallback_logo.png");
            }
        })
    );
});
```

### Example 2: Web Worker for Background CPU Calculations
Running heavy computational processes in a background thread to prevent UI lag.

**File: `main.js` (Main Thread)**
```javascript
const calculatorWorker = new Worker("worker.js");

// Trigger calculation
document.getElementById("calc-btn").addEventListener("click", () => {
    console.log("Triggering calculation in background worker...");
    calculatorWorker.postMessage({ limit: 10000000 });
});

// Listen for results
calculatorWorker.onmessage = (e) => {
    console.log("Calculation complete. Prime count: " + e.data.result);
};
```

**File: `worker.js` (Background Thread)**
```javascript
self.onmessage = (e) => {
    const limit = e.data.limit;
    let primeCount = 0;
    
    // Slow CPU calculation loop
    for (let i = 2; i <= limit; i++) {
        let isPrime = true;
        for (let j = 2; j * j <= i; j++) {
            if (i % j === 0) {
                isPrime = false;
                break;
            }
        }
        if (isPrime) primeCount++;
    }
    
    // Post result back to main thread
    self.postMessage({ result: primeCount });
};
```

### Example 3: Intersection Observer for Lazy Loading Images
Improving page loading speeds by loading images only as they approach the user's viewport.

```html
<!-- Images use data-src instead of src to prevent immediate browser downloads -->
<img class="lazy-load" data-src="images/high_res_photo_1.jpg" src="placeholder.gif" alt="Corporate Event">
<img class="lazy-load" data-src="images/high_res_photo_2.jpg" src="placeholder.gif" alt="Awards Ceremony">

<script>
  const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
          if (entry.isIntersecting) {
              const image = entry.target;
              
              // Swap placeholder with real source path
              image.src = image.getAttribute("data-src");
              image.classList.remove("lazy-load");
              
              // Stop observing the image once loaded
              observer.unobserve(image);
              console.log("Loaded lazy image:", image.src);
          }
      });
  }, {
      // Trigger load when the image is within 100px of the viewport
      rootMargin: "0px 0px 100px 0px",
      threshold: 0.01
  });

  // Register elements to observer
  document.querySelectorAll("img.lazy-load").forEach(img => imageObserver.observe(img));
</script>
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate web engineering skills by testing how candidates use HTML5 as an application runtime rather than a simple document layout. They look for clean, accessible markup, awareness of Critical Rendering Path optimizations (like async vs. defer), proper storage choices (IndexedDB vs. LocalStorage), and understanding of progressive enhancement patterns.

### Red Flags
- **Div-Soup Layouts**: Building application structures using nested `<div>` wrappers instead of semantic landmarks (like `<header>`, `<main>`), breaking accessibility.
- **Unlabeled Forms**: Creating input forms without associated `<label>` elements or `aria-label` tags, making inputs unreadable for screen readers.
- **Missing Viewport Meta Tag**: Omitting `<meta name="viewport" content="...">`, which prevents responsive mobile scaling.
- **Unverified storage assumptions**: Proposing `localStorage` to store large datasets (e.g. 50MB of user offline documents) without understanding quota limits (often capped at 5MB).

### Green Flags
- **Defer/Async Script optimization**: Using `defer` or `async` tags on scripts to optimize the Critical Rendering Path and reduce render-blocking times.
- **Phishing-resistant layouts**: Adding `rel="noopener noreferrer"` attributes to external links (`target="_blank"`) to prevent target window hijacking.
- **Semantic layout landmarks**: Designing layouts using semantic landmarks to enable keyboard and screen reader navigation.
- **Progressive Web App awareness**: Proposing Service Worker caching and IndexedDB storage for offline-first application designs.

### Answers Matrix
| Level | Question: "Where should you store sensitive session tokens (JWTs) in the browser?" |
|---|---|
| **Rejected** | "In `localStorage` so it persists across page refreshes." |
| **Shortlisted** | "In `sessionStorage` or in-memory React state, using a refresh token in an HttpOnly cookie to get new tokens." |
| **Selected** | "Sensitive tokens like JWTs must never be stored in `localStorage` or `sessionStorage` because they are vulnerable to theft via Cross-Site Scripting (XSS) attacks. Any script running on the page can read Web Storage. The most secure browser storage is an **`HttpOnly` cookie** with `Secure` and `SameSite=Strict` flags. This blocks JavaScript read access. Alternatively, store the token in-memory (JavaScript state) and route requests through a **Backend-For-Frontend (BFF) proxy** that manages session states securely." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What are the benefits of Semantic HTML over generic `<div>` layouts?
- **Detailed Answer**:
1. **Accessibility (A11y)**: Screen readers use semantic landmarks (e.g., `<main>`, `<nav>`) to build page structures, allowing visually impaired users to skip navigation and jump directly to content.
2. **SEO (Search Engine Optimization)**: Search engine crawlers index semantic content higher (e.g., placing more weight on headers inside `<article>` than a nested `<div>`).
3. **Code Maintainability**: Clean, standardized structure makes layouts easier for developers to read and debug.
4. **Performance**: Reduces DOM depth and nesting levels.
- **Follow-up Questions**: When should you still use a `<div>`? (Answer: Only when grouping elements for visual styling or layout grids, where no semantic meaning is required).
- **Interviewer's Expectations**: Discuss accessibility, SEO indexing, code clarity, and contrast with div soup.

#### 2. Explain the differences between `async` and `defer` script loading.
- **Detailed Answer**:
- **Default (`<script>`)**: Parser stops HTML parsing, downloads the script, executes it, and resumes parsing. Blocks page rendering.
- **`async`**: Downloads the script in the background while parsing continues. Once downloaded, it pauses the HTML parser to execute the script immediately. It is asynchronous and does not guarantee execution order. Best for independent scripts (e.g., Google Analytics).
- **`defer`**: Downloads the script in the background while parsing continues. Execution is deferred until the HTML parser completes, running in the order declared in document markup. Best for scripts that depend on the complete DOM structure.
- **Follow-up Questions**: What happens if an `async` script completes download before the DOM is built? (Answer: The parser pauses immediately to run the script, which can throw errors if the script attempts to reference DOM elements that have not been parsed yet).
- **Interviewer's Expectations**: Explain parser blocking, download behaviors, execution timings, and identify use cases for both attributes.

#### 3. Compare `localStorage`, `sessionStorage`, and Cookies.
- **Detailed Answer**:
- **`localStorage`**:
  - *Capacity*: ~5MB per origin.
  - *Persistence*: Permanent until deleted manually by the user or code.
  - *Transmission*: Stored locally; not sent with HTTP requests.
- **`sessionStorage`**:
  - *Capacity*: ~5MB per origin.
  - *Persistence*: Temporary; cleared when the browser tab session is closed.
  - *Transmission*: Stored locally; not sent with HTTP requests.
- **Cookies**:
  - *Capacity*: 4KB.
  - *Persistence*: Configured via expiration dates.
  - *Transmission*: Automatically sent to the server with every HTTP request, consuming bandwidth.
- **Follow-up Questions**: Which storage is best for offline-first documents? (Answer: Neither. `IndexedDB` is preferred for large datasets because it supports indexing, transactions, and has a much larger storage quota (often 50%+ of free disk space)).
- **Interviewer's Expectations**: Compare capacity limits, persistence scopes, network overheads, and security risks.

#### 4. How does the browser render a page? Explain the Critical Rendering Path (CRP).
- **Detailed Answer**:
1. **DOM Tree Creation**: The browser parses HTML bytes to construct the Document Object Model (DOM) tree.
2. **CSSOM Tree Creation**: The browser parses CSS stylesheets to construct the CSS Object Model (CSSOM) tree.
3. **Render Tree Creation**: DOM and CSSOM trees are combined into the Render Tree, containing only visible nodes.
4. **Layout (Reflow)**: The browser calculates the position, geometry, and dimensions of each visible node relative to the viewport.
5. **Painting**: The browser draws pixels (backgrounds, borders, text, colors) onto layers.
6. **Compositing**: The browser combines the layers and outputs them to the GPU to be rendered on the screen.
- **Follow-up Questions**: How does JavaScript block this path? (Answer: JavaScript can modify both the DOM and CSSOM, so when the parser encounters a script tag, it pauses HTML parsing until the script downloads and executes, blocking rendering).
- **Interviewer's Expectations**: Enumerate all CRP steps, explain the relationship between DOM/CSSOM, and outline the layout and paint operations.

#### 5. What are ARIA attributes and when should they be used?
- **Detailed Answer**: ARIA (Accessible Rich Internet Applications) is a set of attributes (e.g. `aria-label`, `role="dialog"`) that extend HTML to make web applications accessible. They provide metadata to screen readers when native HTML tags cannot.
- **First Rule of ARIA**: "If you can use a native HTML element with the semantics and behavior you require, do so instead of using ARIA." For example, use `<button>` instead of `<div role="button">`.
- Use ARIA only when creating custom interactive widgets (like accordion menus or tab structures) that native HTML does not support, ensuring you also manage keyboard focus states.
- **Follow-up Questions**: What does `aria-live="polite"` do? (Answer: Instructs screen readers to read out dynamic content changes (like notification alerts) as soon as the user is idle, without interrupting their current action).
- **Interviewer's Expectations**: Explain the purpose of ARIA, state the "first rule of ARIA," and provide examples of role mappings and state attributes.

#### 6. What is the difference between `<canvas>` and `<svg>`?
- **Detailed Answer**:
- **`<canvas>`**:
  - *Type*: Raster-based (pixel grid).
  - *Rendering*: Procedural drawing via JavaScript commands.
  - *Performance*: Fast for large numbers of elements or complex pixel-level animations (like games).
  - *Cons*: Resolution-dependent (becomes pixelated when zoomed); no DOM elements inside (harder to attach event handlers to individual shapes).
- **`<svg>`**:
  - *Type*: Vector-based (XML).
  - *Rendering*: Declarative markup. Each shape is a node in the DOM.
  - *Performance*: Slow if there are thousands of elements on screen due to DOM rendering overhead.
  - *Pros*: Resolution-independent (scales without loss of quality); supports CSS styling and direct DOM event handlers (e.g., clicking a specific path).
- **Follow-up Questions**: Which is better for displaying a interactive map with clickable regions? (Answer: SVG, because each region can be a separate DOM element with its own click event handlers).
- **Interviewer's Expectations**: Compare raster vs. vector, JavaScript drawing vs. DOM nodes, scaling behaviors, and interaction models.

#### 7. How does a Service Worker function and what is its lifecycle?
- **Detailed Answer**: A Service Worker is an event-driven background proxy script. It intercepts network requests, manages caches, and handles offline behaviors, running independently of the main browser window.
**Lifecycle**:
1. **Registration**: The client page registers the worker using `navigator.serviceWorker.register()`.
2. **Installation**: The browser downloads and compiles the script. The `install` event is triggered, commonly used to pre-cache static assets (JS, CSS, HTML).
3. **Activation**: The worker is activated, triggering the `activate` event. Used to clean up old caches.
4. **Active/Execution**: The worker intercepts fetch requests or listens for push messages.
- **Follow-up Questions**: Can a Service Worker access the DOM? (Answer: No, it runs in a separate thread. To communicate with the main page, it must use the `postMessage()` API).
- **Interviewer's Expectations**: Explain background threading, trace installation and activation steps, and explain cache management features.

#### 8. What is the Shadow DOM and how is it used in Web Components?
- **Detailed Answer**: The Shadow DOM is a web standard that allows developers to attach an encapsulated DOM subtree to an element. This subtree (the shadow tree) is rendered separately from the main document DOM.
- **Encapsulation**: Styles declared inside the Shadow DOM do not leak out to the main document, and styles in the main document do not affect the elements in the Shadow DOM. This enables building isolated, self-contained components (like widgets) that do not conflict with site-wide CSS.
- **Follow-up Questions**: What is the difference between open and closed mode in Shadow DOM? (Answer: In `open` mode, JavaScript in the main document can access the shadow root using `element.shadowRoot`. In `closed` mode, the shadow root is inaccessible from external scripts).
- **Interviewer's Expectations**: Explain DOM isolation, style encapsulation, and how it is implemented in custom components.

#### 9. What is the Intersection Observer API and when is it preferred over scroll listeners?
- **Detailed Answer**: The Intersection Observer API monitors when a target element intersects with the browser viewport or a parent container.
- **Why preferred**: Traditional lazy-loading techniques relied on listening to window `scroll` or `resize` events and calling `getBoundingClientRect()` on elements. This runs on the browser's main thread and triggers constant layouts/reflows, causing lag.
- The Intersection Observer runs asynchronously at the browser level, notifying the application only when threshold crossings occur, which reduces CPU load and rendering delays.
- **Follow-up Questions**: What is the `threshold` option? (Answer: A list of numbers between 0.0 and 1.0 indicating at what percentage of target visibility the observer's callback should execute).
- **Interviewer's Expectations**: Explain async scroll monitoring, contrast it with the performance overhead of scroll listeners, and detail use cases (lazy loading).

#### 10. What is Quirks Mode in browsers, and how do you prevent it?
- **Detailed Answer**:
- **Quirks Mode**: A compatibility rendering mode where the browser mimics the bugs and layout behaviors of legacy browsers (like Internet Explorer 5) to render older web pages correctly. For example, it alters the CSS box model calculation rules.
- **Standards Mode**: The modern rendering mode where the browser adheres to HTML5 and CSS standards.
- **Prevention**: Always include the correct doctype declaration at the very first line of the HTML document: `<!DOCTYPE html>`. This instructs the browser to parse the document in Standards Mode.
- **Follow-up Questions**: What happens if there is whitespace before the `<!DOCTYPE html>` tag? (Answer: Some older browsers may fail to parse it and default to Quirks Mode).
- **Interviewer's Expectations**: Define quirks mode, contrast it with standard rendering, and provide the doctype remedy.

---

### Scenario-Based Questions

#### 11. You need to build a photo gallery containing thousands of high-resolution images. How do you design the markup and script to ensure fast loading times?
- **Detailed Answer**:
1. **Lazy Loading**: Use the native `loading="lazy"` attribute on `<img>` tags, or use the `IntersectionObserver` API to swap `data-src` placeholders with real URLs as images approach the viewport.
2. **Responsive Images**: Use the `srcset` and `sizes` attributes to serve appropriately sized images based on the user's screen resolution, preventing mobile devices from downloading 4K images:
   ```html
   <img 
     src="image-800.jpg" 
     srcset="image-400.jpg 400w, image-800.jpg 800w, image-1200.jpg 1200w"
     sizes="(max-width: 600px) 400px, 800px"
     alt="Gallery Photo"
   >
   ```
3. **Modern Image Formats**: Serve images in modern formats (like WebP or AVIF) using the `<picture>` tag:
   ```html
   <picture>
     <source srcset="image.avif" type="image/avif">
     <source srcset="image.webp" type="image/webp">
     <img src="image.jpg" alt="Gallery Photo">
   </picture>
   ```
- **Follow-up Questions**: Why is the `<picture>` tag preferred over standard `<img>` for format fallback? (Answer: It allows specifying different image source files based on browser compatibility, defaulting to standard formats if WebP/AVIF are unsupported).
- **Interviewer's Expectations**: Recommend lazy loading, responsive formats (`srcset`), modern codecs (WebP/AVIF), and `<picture>` fallback tags.

#### 12. Design an offline-first task tracker web application using HTML5 APIs.
- **Detailed Answer**:
- **Service Worker**: Register a Service Worker to intercept network requests. Cache all static assets (HTML, CSS, JS) on first install using the Cache API.
- **Offline Data Storage**: Use **IndexedDB** to store user tasks locally. IndexedDB runs asynchronously and has a large storage quota.
- **Synchronization Pipeline**:
  - When the user adds a task while offline, write it to IndexedDB and mark its status as `pending_sync`.
  - Use the **Background Sync API** to register a sync event. The browser will fire this event in the background as soon as network connectivity is restored.
  - The Service Worker intercepts the sync event, reads pending tasks from IndexedDB, and uploads them to the backend server.
- **Follow-up Questions**: Why not use `localStorage` for offline tasks? (Answer: `localStorage` is synchronous, blocks the main thread, and is capped at 5MB, which can fail if users attach photos or notes to tasks).
- **Interviewer's Expectations**: Detail Service Worker caching, recommend IndexedDB for local data, and outline background synchronization flows.

#### 13. You are designing a custom form wizard with five steps. How do you implement the accessibility markup to ensure screen reader users can navigate it?
- **Detailed Answer**:
1. **Dynamic Navigation**: Wrap each step in a `<section>` container with `aria-live="polite"` so screen readers read out step changes.
2. **Header Focus**: When a user clicks "Next Step", shift focus programmatically to the header of the new section (e.g. using `tabindex="-1"` and calling `.focus()` in JS).
3. **Form Association**: Ensure every form input has an associated `<label>` using `for` and `id` attributes.
4. **Errors**: If validation fails, display error messages linked to inputs using `aria-describedby` and mark fields with `aria-invalid="true"`.
5. **Progress indicator**: Use `<progress>` or a progress bar with `role="progressbar"`, `aria-valuenow="2"`, and `aria-valuemax="5"` to announce progress status.
- **Follow-up Questions**: What does `tabindex="-1"` do? (Answer: Allows an element (like a heading) to receive programmatic focus via JavaScript, without placing it in the standard keyboard tab order).
- **Interviewer's Expectations**: Recommend step markers, focus management, label associations, `aria-describedby` for errors, and progress bars.

#### 14. Your Single Page Application (SPA) needs to support deep linking and browser back/forward buttons. How do you implement this?
- **Detailed Answer**:
- I will implement a client-side router utilizing the **History API**:
  1. Intercept all link clicks inside the app. Call `e.preventDefault()`.
  2. Extract the destination path (e.g., `/dashboard`).
  3. Call **`history.pushState({ path: '/dashboard' }, "", "/dashboard")`** to update the URL in the browser address bar without triggering a server request.
  4. Listen for the **`popstate` window event**. This event fires when the user clicks the browser's back or forward buttons.
  5. In the `popstate` handler, retrieve the route state and render the corresponding page component.
  6. Configure the backend server to redirect all fallback routes to `index.html` so that deep links resolve correctly on page refreshes.
- **Follow-up Questions**: What is the difference between `pushState` and `replaceState`? (Answer: `pushState` adds a new entry to the browser history stack, while `replaceState` overwrites the current history entry without adding a new step).
- **Interviewer's Expectations**: Intercept clicks, explain `pushState` and `popstate` events, and discuss backend fallback configurations.

#### 15. Design a real-time multiplayer drawing application.
- **Detailed Answer**:
- **Graphics layer**: Use the **`<canvas>`** API. Since it is raster-based and runs fast, it can render hundreds of brush strokes at 60 FPS.
- **Communication layer**: Use **WebSockets** (or WebRTC data channels for low-latency peer-to-peer connection).
- **Drawing Loop**:
  - Track mouse/touch coordinates relative to the canvas.
  - Draw paths on the local canvas: `ctx.lineTo(x, y); ctx.stroke();`.
  - Package coordinates as a JSON string and send them over the WebSocket connection: `ws.send(JSON.stringify({ x, y, color }))`.
  - The server broadcasts coordinates to all other connected clients.
  - Other clients receive coordinates and draw them on their local canvases.
- **Follow-up Questions**: How do you prevent drawings from becoming blurry on high-DPI screens (Retina displays)? (Answer: Scale the canvas's internal bitmap size by the device pixel ratio (`window.devicePixelRatio`) while maintaining its CSS layout size).
- **Interviewer's Expectations**: Recommend Canvas for rendering, WebSockets for communication, and outline coordinate sharing.

---

### Debugging Questions

#### 16. A form containing invalid inputs submits to the server, bypassing your HTML5 validation attributes (like `required` or `pattern`). How do you debug?
- **Detailed Answer**:
1. Check the `<form>` tag for the **`novalidate` attribute**. If present, it disables native browser validation, letting the form submit unchecked.
2. Check the submit action in JavaScript. If a script intercepts the submit event (`form.submit()`), it bypasses native browser validation checks. Use `form.reportValidity()` to trigger validation checks manually before programmatically submitting.
3. Ensure input elements have valid `name` attributes; some older engines fail to validate inputs without names.
- **Follow-up Questions**: Why should you never rely solely on client-side HTML5 validation? (Answer: Client-side validation can be bypassed by disabling JavaScript, modifying DOM attributes, or sending POST requests directly. Always run validation checks on the server).
- **Interviewer's Expectations**: Identify `novalidate` tags, distinguish CLI-triggered submits, and recommend server-side validation.

#### 17. Your application's local storage calls fail, throwing `QuotaExceededError`. How do you resolve this?
- **Detailed Answer**:
- **Cause**: The application has exceeded the browser's storage limit for LocalStorage (typically capped at 5MB per origin).
- **Resolution**:
  1. Optimize data storage: Stringify and compress large JSON payloads.
  2. Implement cleanup routines: Delete expired caches or stale data.
  3. **Migrate to IndexedDB**: For applications requiring larger storage (e.g. offline document cache), migrate from LocalStorage to IndexedDB, which has a much larger quota (often 50% of the host's free disk space).
- **Follow-up Questions**: Is LocalStorage synchronous? (Answer: Yes, LocalStorage reads and writes are synchronous and block the browser's main UI thread, whereas IndexedDB runs asynchronously).
- **Interviewer's Expectations**: Identify storage limits, recommend cleanup routines, and suggest migrating to IndexedDB.

#### 18. You register a Service Worker and update your app's CSS, but users report still seeing the old style. How do you fix this caching issue?
- **Detailed Answer**:
- **Cause**: The Service Worker's fetch event is serving the old cached CSS file instead of fetching the updated version from the network.
- **Resolution**:
  1. **Update the Cache Name**: Increment the cache version number in the Service Worker (e.g., changing `CACHE_NAME = 'v1'` to `'v2'`). This triggers the `activate` event, which should delete the old cache.
  2. **Cache Busting**: Append a content hash to the asset filenames (e.g., `styles.a8f2c.css`). When you update the styles, the build tool generates a new filename. The Service Worker detects it as a new request, fetches it from the network, and caches it.
- **Follow-up Questions**: How does a browser detect updates to the Service Worker file itself? (Answer: The browser checks the `sw.js` file for updates on every page load. If the file has changed by even 1 byte, it installs the new worker).
- **Interviewer's Expectations**: Recommend cache name rotations, activate events, and filename cache busting.

#### 19. A div styled to behave like a button is focusable via keyboard, but pressing the spacebar does not trigger its click action. How do you resolve this?
- **Detailed Answer**:
- **Cause**: Unlike native `<button>` elements, a `<div>` styled with `role="button"` and `tabindex="0"` does not inherit native button behaviors. Browsers do not automatically trigger click events on divs when the Enter or Space keys are pressed.
- **Resolution**: Add an event listener to the element to handle key presses manually:
```javascript
const myDivButton = document.getElementById("div-btn");

myDivButton.addEventListener("keydown", (e) => {
    // Check if Enter (13) or Space (32) was pressed
    if (e.key === "Enter" || e.key === " ") {
        e.preventDefault(); // Prevent page scroll on Space key
        triggerAction();
    }
});
```
- **Follow-up Questions**: Why is it still preferred to use a native `<button>`? (Answer: Because native buttons handle focus, click events, and keyboard behaviors out of the box, without requiring custom JS listeners).
- **Interviewer's Expectations**: Explain missing keyboard mappings on non-native elements, and show how to handle keydown events manually.

#### 20. Your site's images fail to load on mobile devices. Inspecting the DOM shows that the `srcset` attribute is configured. How do you troubleshoot?
- **Detailed Answer**:
1. Check the image paths inside `srcset`. Verify they are correct and return `200 OK` status codes.
2. Check the `sizes` attribute. If missing, the browser defaults to `100vw` (full screen width), which can cause it to request the largest image in the list, causing timeout failures on slow mobile networks.
3. Verify if the mobile browser supports the image format (e.g., if you are serving AVIF images, verify the browser is compatible; otherwise provide JPEG/PNG fallbacks).
- **Follow-up Questions**: What does the `w` descriptor mean in `srcset` (e.g., `image-400.jpg 400w`)? (Answer: It specifies the actual pixel width of the source image file, allowing the browser to choose the best matching image based on screen resolution).
- **Interviewer's Expectations**: Check image paths, verify the `sizes` configuration, and check format compatibility.

---

### System Design Questions

#### 21. Design the architecture of an offline-first Progressive Web Application (PWA).
- **Detailed Answer**:
- **Application Shell**: Cache the App Shell (HTML, CSS, core JS, logos) in the browser's Cache API during the Service Worker's `install` event. Serve the cached App Shell immediately on page requests to ensure fast load times.
- **Client Data Storage**: Use **IndexedDB** as the primary database for dynamic user content, using libraries like Dexie.js to manage transactions.
- **Synchronization Layer**:
  - The client writes changes to IndexedDB and registers a background sync event.
  - The Service Worker listens for the sync event, reads pending data from IndexedDB, and sends it to the API Gateway.
- **Conflict Resolution**:
  - If a synchronization conflict occurs (e.g., data was modified on another device), the backend resolves it using last-write-wins or returns a merge prompt.
- **Follow-up Questions**: What is the purpose of the web app manifest file? (Answer: A JSON file detailing metadata (app name, icons, start URL) needed to allow users to install the web app to their mobile home screen).
- **Interviewer's Expectations**: Detail App Shell caching, IndexedDB integration, sync channels, and conflict resolution rules.

#### 22. Design an accessible corporate UI component library.
- **Detailed Answer**:
- **Standard Guidelines**: Enforce WCAG 2.1 Level AA conformance criteria (contrast, resizing, focus).
- **Semantic Foundation**: Use native semantic HTML elements by default (e.g., `<dialog>` for modals, `<button>` for actions).
- **ARIA Integration**: For custom widgets, apply appropriate ARIA roles and states (e.g., `aria-expanded="true/false"` on accordion triggers).
- **Keyboard Navigation**:
  - Manage focus traps in modal overlays (pressing Tab should cycle focus only within the modal, and pressing Escape should close it).
  - Support standard keyboard controls (arrows, home, end) inside tabs and menu components.
- **Automated Testing**: Integrate accessibility testing tools (like Axe-core) into the CI/CD pipeline to scan components for contrast and structure violations on every commit.
- **Follow-up Questions**: How do you implement a focus trap in vanilla JS? (Answer: Listen for the Tab key inside the modal, check if the active element is the first or last focusable element, and wrap the focus path).
- **Interviewer's Expectations**: Enforce WCAG conformance, recommend native elements, detail keyboard focus traps, and propose automated pipeline audits (Axe).

#### 23. Design a real-time collaborative document editing system (similar to Google Docs) at the DOM level.
- **Detailed Answer**:
- **DOM Representation**: Use a single container div with the `contenteditable="true"` attribute.
- **Synchronization Protocol**:
  - Use **OT (Operational Transformation)** or **CRDTs (Conflict-free Replicated Data Types)** to manage concurrent edits.
  - Represent edits as operations: `Insert(position, character)` or `Delete(position, length)`.
- **Communication Layer**: Use a persistent WebSocket connection to send and receive edit operations.
- **Client Synchronization**:
  - The client listens for input events on the DOM.
  - Translate edits into CRDT operations and transmit them over the WebSocket.
  - When receiving operations from other clients, apply them to the local DOM using range markers (`window.getSelection()`) to prevent shifting the user's active cursor position.
- **Follow-up Questions**: Why is direct HTML string swapping (like `innerHTML = newHTML`) unsuitable for collaborative editors? (Answer: It resets the editor state, destroying user selections, cursor positions, and causes page flickering).
- **Interviewer's Expectations**: Recommend contenteditable containers, propose CRDT/OT operation models, and use WebSocket channels for real-time updates.

---

## 10. Common Mistakes

- **Div-Soup Layouts**: Building application structures using nested `<div>` wrappers instead of semantic landmarks (like `<header>`, `<main>`), breaking accessibility.
- **Unlabeled Forms**: Creating input forms without associated `<label>` elements or `aria-label` tags, making inputs unreadable for screen readers.
- **Missing Viewport Meta Tag**: Omitting `<meta name="viewport" content="...">`, which prevents responsive mobile scaling.
- **Unsecured target="_blank" Links**: Opening external links in new tabs without adding `rel="noopener noreferrer"`, exposing the page to security vulnerabilities (window hijacking).
- **Storing sensitive data in LocalStorage**: Storing authorization tokens or private user details in LocalStorage, exposing them to theft via XSS attacks.

---

## 11. Comparison Section: Web Graphics & Client Storage

### Web Graphics comparison
| Feature | Canvas | SVG | WebGL |
|---|---|---|---|
| **Type** | Raster-based (pixels) | Vector-based (XML) | 3D raster-based |
| **Scaling** | Resolution-dependent | Resolution-independent | Resolution-dependent |
| **DOM Integration** | Single canvas element node | Each shape is a DOM node | Single canvas element node |
| **Event Handling** | Manual (track coordinates) | Direct (attach listeners to nodes)| Manual (raycasting) |
| **Best For** | 2D games, pixel filters, charts. | Icons, UI drawings, maps. | 3D graphics, heavy simulations.|

### Client Storage comparison
| Feature | LocalStorage | SessionStorage | Cookies | IndexedDB |
|---|---|---|---|---|
| **Capacity** | ~5MB | ~5MB | 4KB | 50%+ of free disk |
| **Persistence** | Permanent | Session duration | Configurable expiry | Permanent |
| **API** | Sync Key-Value | Sync Key-Value | Header string | Async Transactional |
| **Network Overhead** | None | None | Sent on every request | None |
| **Use Cases** | User settings. | Transient filters. | Auth session keys. | Offline documents. |

---

## 12. Practical Project Ideas

### Beginner: Accessible Portfolio Page
Build a personal portfolio page using semantic HTML5 tags (`<header>`, `<nav>`, `<main>`, `<section>`, `<footer>`). Ensure all images have alt attributes, the page gets standards rendering mode, and form inputs are associated with labels.

### Intermediate: Autocomplete Input with Keyboard Navigation
Build a custom search input box. As the user types, query a mock API and render a list of suggestions. Manage keyboard navigation: pressing the Down Arrow should highlight suggestions, Enter should select, and Escape should close the list.

### Advanced/Resume-worthy: Offline-Capable PWA Task Manager
Create a task tracker application. Implement a Service Worker to pre-cache application assets and serve them offline. Use IndexedDB to save tasks locally, and implement background sync functionality to upload tasks when network connectivity returns.

---

## 13. Internship Preparation Notes

- **What Recruiters look for**: Flawless explanation of block vs inline elements, semantic landmarks, client storage options, and the purpose of the doctype tag.
- **What Engineering Teams expect**: Familiarity with web accessibility (ARIA, alt tags), configuring script load tags (async/defer), and understanding DOM rendering stages.

---

## 14. Cheat Sheet

- **Doctype**: `<!DOCTYPE html>` (forces Standards Mode).
- **Script parameters**:
  - `async`: Download in background, run immediately (non-ordered).
  - `defer`: Download in background, run after parsing (ordered).
- **Storage options**:
  - `localStorage` = Permanent user settings.
  - `sessionStorage` = Temporary tab states.
  - `IndexedDB` = Large offline datasets.
- **Links**: Use `rel="noopener noreferrer"` for `target="_blank"` links.

---

## 15. One-Day Revision Guide

- [ ] Write a semantic page skeleton with headers, nav, main, and footers.
- [ ] Contrast the loading behavior of async vs defer scripts.
- [ ] Explain how the Critical Rendering Path translates HTML bytes to pixels.
- [ ] Choose appropriate client storage options based on capacity and persistence.
- [ ] Write a basic Intersection Observer setup to lazy load images.
- [ ] State the first rule of ARIA.
