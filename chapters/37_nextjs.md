# 37. Next.js (Server Rendering & Static Web Architecture)

## 1. Introduction

### What it is
Next.js is a production-ready React framework created by Vercel. It provides additional structure, configuration configurations, and optimizations for building hybrid, search-engine-friendly, and high-performance web applications.

### Why it exists
Standard React applications are Client-Side Rendered (CSR). The server sends an empty HTML template containing a heavy JavaScript bundle to the browser. The browser then executes the JavaScript to build the DOM. This causes:
1. **Poor SEO**: Search engine crawlers receive empty HTML files, making indexing content difficult.
2. **Slow Initial Page Load (LCP)**: Users see a blank page while downloading and parsing the JavaScript.
Next.js was built to solve these issues by providing hybrid server-side rendering (SSR), static site generation (SSG), and incremental page caching.

### Problems it solves
- **Client-Side Sizing Latency**: Moves compilation workloads to the server, reducing the amount of JavaScript sent to client browsers.
- **Complex Routing Configuration**: Replaces React Router configurations with a file-based routing system.
- **Uncached Content**: Offers Incremental Static Regeneration (ISR) to cache static pages and update them in the background.

### Industry Use Cases
- **E-Commerce Applications**: Target and category catalog pages are generated statically (SSG) for SEO speed and cached at edge CDN nodes.
- **Publishing & Blogs**: Content pages are rendered via ISR to load instantly while incorporating CMS updates in the background.
- **Enterprise SaaS Web Apps**: Secure client portals leverage Server-Side Rendering (SSR) to render private dashboard components on demand.

---

## 2. Core Concepts

### Beginner Concepts
- **File-Based Routing (App Router)**: Sourced inside the `app/` folder. Sub-folders represent URL paths, and `page.js` files define the UI.
  - `app/page.js` mapping to `/`.
  - `app/dashboard/page.js` mapping to `/dashboard`.
- **Layouts and Pages**:
  - `layout.js`: Defines shared UI layout structures (e.g. headers, sidebars) that persist during route transitions.
  - `page.js`: The unique UI content of a route.
- **SEO Metadata**: Static or dynamic definitions declared directly inside page configurations:
  ```javascript
  export const metadata = {
      title: "Pricing Plans - SaaS App",
      description: "Secure pricing plans for all user scales."
  };
  ```

### Intermediate Concepts
- **Hybrid Rendering Strategies**:
  - **Static Site Generation (SSG)**: Pages are compiled once at build time. High performance, ideal for public marketing pages.
  - **Server-Side Rendering (SSR)**: Pages are rendered to HTML on the server on *every* request. Best for user-specific dashboards.
  - **Incremental Static Regeneration (ISR)**: Statically generates pages, but regenerates them in the background after a specified cache validation delay.
  - **Client-Side Rendering (CSR)**: Standard React behavior where layouts render in the browser (marked with `'use client'`).
- **Next.js Data Fetching**: Employs extended `fetch` syntax to manage server-side caching directly:
  ```javascript
  // Fetch with cache revalidation after 1 hour (ISR)
  fetch('https://api.example.com/products', { next: { revalidate: 3600 } });
  ```

### Advanced Concepts
- **React Server Components (RSC) vs. Client Components**:
  - **Server Components (Default)**: Execute entirely on the server. They have direct access to database modules, do not ship JavaScript to the browser, and cannot use client hooks (like `useState` or `useEffect`).
  - **Client Components**: Marked with `'use client'` at the top of the file. Hydrated in the browser to support interactive elements.
- **Suspense and Streaming**: Allows streaming HTML layout blocks from the server as they finish rendering, letting components load incrementally instead of waiting for the entire page to compile.
- **Next.js Middleware**: Code that runs *before* a request is completed, enabling redirects, rewrites, and header validation (e.g., verifying user JWTs).

---

## 3. Internal Working

### Server Hydration and React Server Components (RSC) Architecture

Next.js optimizes client loads by splitting rendering between server-side compilation and client-side hydration:

```text
[ Client Page Request ] -> Hits Server
                               |
  +------------------ Next.js Server Rendering Phase --------------------+
  |                                                                      |
  |  1. Executes React Server Components (RSC) directly.                 |
  |  2. Compiles HTML layout string containing static data.              |
  |  3. Streams HTML to browser + serializes RSC JSON Payload data.      |
  +----------------------------------------------------------------------+
                               |
                               v
[ Browser receives initial page ] -> User sees text layouts immediately (Fast LCP)
                               |
  +------------------ Client Hydration Phase ----------------------------+
  |                                                                      |
  |  1. Browser parses lightweight JS script bundle.                     |
  |  2. React matches virtual nodes with server-rendered HTML nodes.     |
  |  3. Attaches event listeners dynamically without flashing layout.    |
  +----------------------------------------------------------------------+
                               |
                               v
[ Fully Interactive Page ] ---> User can click elements, trigger hooks
```

1. **The Hydration Process**:
   - The server renders components into a static HTML string. The browser receives this HTML, allowing text and layouts to appear instantly (reducing First Contentful Paint).
   - The browser then downloads the JavaScript bundle.
   - **Hydration**: React traverses the DOM tree, matching client-side virtual components with the server-rendered HTML nodes, and attaches event listeners (like `onClick`) to make the page interactive.
2. **React Server Components (RSC) Execution**:
   - Unlike SSR (which renders all React components to HTML on the server and runs them again on the client), RSCs execute **only** on the server.
   - The compiled output is streamed to the browser as a serialized JSON-like structure (RSC Payload).
   - This payload contains the instructions needed to update the DOM, eliminating the need to send heavy dependencies (like markdown parsers or date utilities used in RSCs) to the browser.
3. **Automatic Code Splitting and Prefetching**:
   - Next.js splits JavaScript bundles by route. Moving to a page only downloads the code needed for that page.
   - The `<Link>` component detects when it enters the browser viewport and automatically prefetches the target page's code in the background, making route transitions feel instant.

---

## 4. Important Terminology

- **Hydration**: The process of attaching event listeners to server-rendered HTML in the browser.
- **React Server Components (RSC)**: React components that execute exclusively on the server, reducing client-side JavaScript bundle sizes.
- **Incremental Static Regeneration (ISR)**: An optimization strategy that updates static pages in the background after they have been built and cached.
- **Hydration Mismatch**: A runtime error that occurs when the HTML generated on the server does not match the HTML rendered in the browser on initial load.
- **Edge Runtime**: A lightweight execution environment that runs middleware code closer to the user on global CDN nodes.

---

## 5. Beginner Examples

### Example 1: App Router Layout and Page Setup
This example demonstrates setting up a shared layout and a static page with SEO metadata in the App Router.

```javascript
// 1. app/layout.js (Root Layout)
export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>
                <header>
                    <nav>Logo | Home | Products</nav>
                </header>
                <main>{children}</main>
                <footer>© 2026 Booklet Corp</footer>
            </body>
        </html>
    );
}

// 2. app/products/page.js (Static Product Page)
export const metadata = {
    title: "Our Products",
    description: "Explore our catalog of data science tools."
};

export default function ProductsPage() {
    return (
        <section>
            <h1>Products Catalog</h1>
            <p>Select a product to view its details.</p>
        </section>
    );
}
```

---

## 6. Intermediate Examples

### Example 1: Incremental Static Regeneration (ISR) Product Loader
This example fetches dynamic catalog data from a backend database and caches the static output, updating it automatically in the background.

```javascript
// app/catalog/page.js (Server Component)

async function getCatalogData() {
    // Fetch from API, caching the result with a 60-second revalidation window
    const res = await fetch("https://api.example.com/products", {
        next: { revalidate: 60 } // Revalidate static page at most once every 60 seconds
    });
    
    if (!res.ok) throw new Error("Failed to load catalog data");
    return res.json();
}

export default async function CatalogPage() {
    const products = await getCatalogData();

    return (
        <div>
            <h1>Store Catalog</h1>
            <ul>
                {products.map((product) => (
                    <li key={product.id}>
                        {product.name} - ${product.price}
                    </li>
                ))}
            </ul>
        </div>
    );
}
```

---

## 7. Advanced Concepts

### React Server Components (RSC) and Server Actions

#### Component Type Boundaries
To optimize performance, place client interactive elements in leaf nodes to keep parent components as Server Components.

```jsx
// 1. app/dashboard/SearchInput.js (Client Component)
'use client'; // Marks this file as client-side code

import { useState } from 'react';

export default function SearchInput({ onSearch }) {
    const [query, setQuery] = useState("");
    return (
        <input 
            value={query} 
            onChange={(e) => { setQuery(e.target.value); onSearch(e.target.value); }} 
            placeholder="Type filter..." 
        />
    );
}

// 2. app/dashboard/page.js (Server Component)
import SearchInput from './SearchInput'; // Imports client node
import { db } from '@/lib/db';         // Direct database query (server-only)

export default async function DashboardPage() {
    const rawData = await db.query("SELECT * FROM metrics"); // Direct server query

    async function handleSearchAction(term) {
        'use server'; // Defines a Server Action
        console.log("Searching database for:", term);
        // Server Actions allow executing database queries directly from client triggers
    }

    return (
        <div>
            <h1>System Metrics Dashboard</h1>
            {/* Server component imports client component and passes action parameters */}
            <SearchInput onSearch={handleSearchAction} />
            <pre>{JSON.stringify(rawData, null, 2)}</pre>
        </div>
    );
}
```

### Next.js 16 Rendering & Cache Architecture
Next.js 16 (built on React 19) optimizes streaming layouts and build times using Turbopack and modern compilation modes.

* **Partial Prerendering (PPR)**: A rendering model that combines static shell layouts with dynamic components on the same page. The shell (e.g. navbar, sidebar) is compiled to static HTML at build time, while dynamic components wrapped in React `<Suspense>` are streamed from the server as they compile, eliminating the SSR wait time.
* **Turbopack Integration**: A Rust-based compiler replacement for Webpack, speeding up local development server starts and hot module replacement (HMR) times by up to 10x.
* **Server Component Caching Hierarchy**: Manages client-side Router Cache, server-side Request Memoization, Data Cache, and Full Route Cache to optimize data delivery.

#### Code Example: Partial Prerendering (PPR) with Dynamic Streaming
This page demonstrates a static layout shell containing an asynchronous, dynamically rendered component wrapped in a `<Suspense>` boundary, allowing PPR.

```jsx
// app/dashboard/page.js (Server Component)
import { Suspense } from 'react';

// Static Shell component (loads instantly via PPR static shell)
function DashboardShell({ children }) {
  return (
    <div className="dashboard-container">
      <header className="navbar">System Monitoring Shell</header>
      <main className="content">{children}</main>
    </div>
  );
}

// Dynamic Component (rendered asynchronously on request, streamed via Suspense)
async function DynamicSystemMetrics() {
  // Disable data cache to force request-time evaluation (Dynamic SSR)
  const res = await fetch("https://api.example.com/system/metrics", {
    cache: "no-store"
  });
  const data = await res.json();

  return (
    <div className="metrics-card">
      <h3>Live CPU Load: {data.cpu}%</h3>
      <p>Disk Usage: {data.disk}%</p>
    </div>
  );
}

// Loading Skeleton placeholder shown while metrics load
function MetricsSkeleton() {
  return (
    <div className="skeleton-card animate-pulse">
      <div className="h-6 w-3/4 bg-gray-200 rounded"></div>
      <div className="h-4 w-1/2 bg-gray-200 rounded mt-2"></div>
    </div>
  );
}

export default function DashboardPage() {
  return (
    <DashboardShell>
      <h2>System Reports</h2>
      {/* 
        PPR renders the page shell statically, while placing the dynamic 
        component inside a Suspense boundary to stream it once resolved.
      */}
      <Suspense fallback={<MetricsSkeleton />}>
        <DynamicSystemMetrics />
      </Suspense>
    </DashboardShell>
  );
}
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers evaluate your understanding of web performance, rendering architectures, and state boundaries. They want to see if you can select the correct rendering strategy (e.g. SSG vs SSR vs ISR), solve hydration mismatch errors, and explain how React Server Components (RSC) optimize client bundle sizes.

### Red Flags
- **`'use client'` Abuse**: Adding `'use client'` to the top of every component, turning Next.js back into a standard client-side SPA.
- **Database Calls in Client Components**: Importing database drivers, filesystems, or secure environment keys inside files marked with `'use client'`.
- **Failing to clean cache options**: Fetching volatile user data (like account details) using cached queries instead of disabling caches (`cache: "no-store"`).

### Green Flags
- **RSC Composition**: Keeping the majority of component trees on the server, importing interactive client elements at leaf nodes.
- **ISR Optimization**: Choosing Incremental Static Regeneration for catalog structures to reduce server load.
- **Handling Hydration Conflicts**: Correctly explaining how hydration mismatches occur and resolving them using client checks.

### Answers Matrix

| Level | Question: "What is the difference between Server Components and Client Components?" |
|---|---|
| **Rejected** | "Server components render on the backend and client components render in the browser." |
| **Shortlisted** | "Server components are static, run on the server, and do not ship JavaScript to the browser. Client components are interactive, run in the browser, and support React hooks like `useState`." |
| **Selected** | "React Server Components (RSC) run exclusively on the server. They can query databases directly and import server-only modules without shipping JavaScript code to the browser, reducing bundle sizes. However, they cannot use React hooks (like `useState` or `useEffect`) or interact with browser APIs. Client components (marked with `'use client'`) are hydrated in the browser. They support interactive features, event listeners, and hooks. The best practice is to use Server Components by default and import Client Components only at leaf nodes where interactivity is required." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. Explain the differences between SSG, SSR, ISR, and CSR in Next.js.
- **Detailed Answer**:
  - **Static Site Generation (SSG)**: Pages are compiled to HTML at build time. They load instantly from a CDN, making them ideal for static content like landing pages.
  - **Server-Side Rendering (SSR)**: Pages are rendered to HTML on the server on *every* request. Best for dynamic, user-specific data that must always be up-to-date.
  - **Incremental Static Regeneration (ISR)**: Static pages are regenerated in the background after a specified revalidation delay. This combines the performance of SSG with the dynamic updates of SSR.
  - **Client-Side Rendering (CSR)**: Standard React rendering. The server sends a shell page, and the browser compiles the UI using JavaScript.
- **Follow-up Questions**: How do you disable caching for a specific API fetch? (Answer: Set `cache: 'no-store'` in the fetch options).
- **Interviewer's Expectations**: Describe the build-time, request-time, background-time, and client-time execution differences of each strategy.

#### 2. What is a Hydration Mismatch error, and how do you resolve it?
- **Detailed Answer**: A hydration mismatch occurs when the server-rendered HTML structure does not match the initial HTML rendered by the client-side JavaScript on load.
  - Common causes include rendering dynamic values (like `new Date()`, `Math.random()`, or window width) that differ between the server execution and client load, or writing invalid HTML structure (like nesting a `<div>` inside a `<p>` tag).
  - **Resolutions**:
    1. Fix invalid HTML nesting.
    2. Move dynamic values to `useEffect` so they are evaluated only after the component mounts on the client.
    3. Disable SSR for specific components using dynamic imports with `ssr: false`.
- **Follow-up Questions**: Why does React throw a hydration mismatch error instead of ignoring the difference? (Answer: To prevent layout shifts, styling bugs, and broken event listeners).
- **Interviewer's Expectations**: Identify dynamic data rendering as the primary cause of hydration errors and provide resolutions.

---

### Scenario-Based Questions

#### 3. You are building a news article page. The content is updated by a CMS. Page speed is critical, and articles can update at any time. Which rendering strategy do you select?
- **Detailed Answer**: **Incremental Static Regeneration (ISR)** is the ideal strategy.
  - We fetch the article content on the server and configure revalidation:
    ```javascript
    fetch(`https://cms.api/article/${id}`, { next: { revalidate: 60 } });
    ```
  - This statically compiles the page. When a user requests the article, it loads instantly from cache.
  - If a change is made in the CMS, the page is regenerated in the background when requests arrive after the 60-second revalidation window, updating the cache without slowing down the site.
- **Follow-up Questions**: How do you trigger an instant revalidation when an editor publishes a change? (Answer: Use On-Demand Revalidation by calling `revalidatePath` or `revalidateTag` in an API route).
- **Interviewer's Expectations**: Recommend ISR and explain background revalidation logic.

#### 4. How do you implement a route guard in Next.js to redirect unauthenticated users away from `/dashboard` paths before the page renders?
- **Detailed Answer**: We use **Next.js Middleware**. Middleware runs before the request reaches the page renderer, allowing us to inspect cookies and redirect users:
  ```javascript
  // middleware.js
  import { NextResponse } from 'next/server';

  export function middleware(request) {
      const token = request.cookies.get('session-token');
      if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
          return NextResponse.redirect(new URL('/login', request.url));
      }
      return NextResponse.next();
  }
  ```
- **Follow-up Questions**: Can middleware query database layers directly? (Answer: No. Middleware runs in the Edge Runtime, which has access only to a subset of Node APIs to keep executions fast. Database queries should be handled via fetch requests or in Server Components).
- **Interviewer's Expectations**: Implement the middleware code and specify match routing path boundaries.

---

### Debugging Questions

#### 5. Debug the following code which throws a hydration mismatch error on initial page load:
```jsx
// app/status/page.js
'use client';
import { useState } from 'react';

export default function StatusPage() {
    const isMobile = typeof window !== 'undefined' && window.innerWidth < 768;
    return (
        <div>
            <h1>Device Status</h1>
            <p>You are viewing on: {isMobile ? "Mobile" : "Desktop"}</p>
        </div>
    );
}
```
- **Detailed Answer**: During server-side rendering, `window` is undefined, so `isMobile` evaluates to `false`, rendering "Desktop". When the browser loads the page, `window` is defined. If the user's viewport is smaller than 768px, `isMobile` evaluates to `true`, rendering "Mobile". This difference between the server and client HTML causes a hydration mismatch error.
- **Fix**: Move the window measurement logic into `useEffect` so it runs only after the component mounts on the client:
  ```jsx
  import { useState, useEffect } from 'react';

  export default function StatusPage() {
      const [isMobile, setIsMobile] = useState(false);

      useEffect(() => {
          setIsMobile(window.innerWidth < 768);
      }, []); // Empty dependencies: Evaluates once on mount

      return (
          <div>
              <h1>Device Status</h1>
              <p>You are viewing on: {isMobile ? "Mobile" : "Desktop"}</p>
          </div>
      );
  }
  ```
- **Follow-up Questions**: Why is it safer to initialize `isMobile` as false? (Answer: To prevent layout layout shifts. Alternatively, render a loading state until the check completes).
- **Interviewer's Expectations**: Explain server vs client execution differences and use `useEffect` to resolve the mismatch.

---

### System Design Questions

#### 6. Design an e-commerce platform architecture using Next.js.
- **Detailed Answer**:
  - **Homepage and Landing Pages**: Pre-rendered using Static Site Generation (SSG) and cached on a CDN to ensure fast load times.
  - **Product Catalog Pages**: Rendered using Incremental Static Regeneration (ISR) with a revalidation window of 5 minutes to keep pricing and stock data relatively up-to-date.
  - **Checkout and Cart Flow**: Handled completely on the client side using Client Components (`'use client'`) since they contain highly interactive, user-specific forms.
  - **Order Confirmation**: Rendered dynamically using Server-Side Rendering (SSR) to display real-time database details.
  - **Routing Security**: Next.js Middleware inspects JWT session tokens for authentication.
- **Follow-up Questions**: Where do you implement analytics tracking scripts? (Answer: Using Next.js `Script` component with `strategy="lazyOnload"` to avoid blocking page paint).
- **Interviewer's Expectations**: Match rendering strategies to e-commerce page types and justify your choices.

---

### Real Interview Questions

#### 7. What does the `'use client'` directive do in Next.js?
- **Detailed Answer**: The `'use client'` directive marks the boundary between Server Components and Client Components. It tells Next.js to package the component and its imports into a JavaScript bundle to be sent to the browser for hydration. It does *not* mean the component only runs on the client; it is still pre-rendered to HTML on the server before being hydrated in the browser.
- **Follow-up Questions**: If a Server Component imports a Client Component, does the parent become a Client Component? (Answer: No. A Server Component can import Client Components, and they are treated as leaf nodes in the render tree).
- **Interviewer's Expectations**: Define the client-server boundary and explain that client components still pre-render on the server.

---

## 10. Common Mistakes

- **Adding `'use client'` to every file**: Reverts the application back to a client-side SPA, negating the SEO and bundle size benefits of Next.js.
- **Accessing browser APIs in Server Components**: Attempting to read `window`, `document`, or `localStorage` in Server Components, which throws runtime errors on the server.
- **Confusing SSR with SSG**: Assuming pages rendered via SSR are cached on CDNs by default. SSR pages are compiled on demand for every request.

---

## 11. Comparison Section: Next.js Routing and Rendering Choice

| Feature / Strategy | App Router | Pages Router | Server Component (RSC) | Client Component (CSR) |
|---|---|---|---|---|
| **Routing Model** | Folder-based (`app/`) | File-based (`pages/`) | N/A | N/A |
| **Component Caching** | Yes (cached on server) | No | Yes (cached on server) | No (computed in browser) |
| **Bundle Size Impact** | Low (code remains on server) | High | Zero JavaScript shipped | Ships component JS to browser |
| **Supports Hooks?** | No | Yes | No | Yes |

---

## 12. Practical Project Ideas

### Beginner
- **Static Portfolio with Blog**: Create a personal portfolio page using static layout routing, utilizing App Router layouts to share header configurations.

### Intermediate
- **Recipe Directory with Dynamic Pages**: Build a recipe website that fetches data using Next.js ISR, showing recipe pages with custom revalidation times.

### Advanced/Resume-worthy
- **Markdown-to-HTML Blog Platform**: Develop a blogging engine where articles are written in markdown. Render markdown parsing logic entirely inside Server Components to keep client-side JavaScript bundles minimal, and use dynamic path revalidation on article updates.

---

## 13. Internship Preparation Notes

- **Recruiters Focus on**: Basic page layout configurations, directory routing structures, and the difference between Next.js and standard React.
- **Product Companies Expect**: High proficiency in React Server Components, hydration pipelines, rendering choices, and Next.js middleware.
- **Data Engineering Integration**: Understand how Next.js handles server-side API data caching.

---

## 14. Cheat Sheet

- **Client Component Directive**: `'use client'`
- **Revalidation Fetch Option**:
  ```javascript
  fetch(url, { next: { revalidate: 60 } });
  ```
- **Dynamic Routing Directory naming**: `app/blog/[id]/page.js` (accessed via `params.id`).
- **Disable Caching**: `fetch(url, { cache: 'no-store' });`

---

## 15. One-Day Revision Guide

- [ ] Explain the difference between React Server Components (RSC) and Client Components.
- [ ] List the differences between SSG, SSR, ISR, and CSR.
- [ ] Debug a hydration mismatch error caused by rendering dynamic date strings.
- [ ] Write a Next.js middleware file that redirects user requests.
- [ ] Explain how Next.js `<Link>` component pre-loads routes in the background.
