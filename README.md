# Technical Interview Preparation Booklet
### Data Science, Generative AI, AI/ML, and Software Engineering Roles

Welcome to your comprehensive technical interview handbook. This booklet has been structured to teach you concepts from first principles up to expert interview-ready implementation and theory.

---

## Table of Contents & Syllabus

The handbook is divided into five core sections, each containing dedicated chapters for deep-dive technical mastery:

### 1. Core Web
* **Chapter 01: HTML5** - Semantic structure, DOM tree, browser APIs, storage, accessibility (A11y).
* **Chapter 02: CSS3** - Box model, layouts (Flexbox/Grid), transitions/animations, performance, architecture.
* **Chapter 03: JavaScript (ES6+)** - V8 runtime, execution context, closures, event loop, asynchronous JS, promises.
* **Chapter 04: TypeScript** - Type system, generics, interfaces vs. types, compiler mechanics, advanced typing.

### 2. Frontend
* **Chapter 05: React.js** - Virtual DOM, fiber architecture, hooks, rendering optimization, state management, synthetic events.
* **Chapter 06: Next.js** - Server-side rendering (SSR), Static generation (SSG), routing (App Router), server components, caching.

### 3. Backend
* **Chapter 07: Node.js** - Event-driven architecture, non-blocking I/O, event loop internals, streams, clustering, buffer.
* **Chapter 08: Express.js** - Middleware pattern, routing lifecycle, error handling, security, scalability.

### 4. Databases
* **Chapter 09: SQL & Relational Databases** - Relational theory, ACID, normalization, joins, indexing strategies.
* **Chapter 10: PostgreSQL** - Advanced querying, JSONB, window functions, MVCC, performance optimization.
* **Chapter 11: MySQL** - InnoDB vs. MyISAM, locking mechanisms, replication patterns, indexing.
* **Chapter 12: MongoDB** - NoSQL patterns, BSON document structure, aggregation pipelines, sharding, replication.

### 5. Programming & Version Control
* **Chapter 13: Python** - Memory management, GIL, generators/iterators, decorators, OOP, async.
* **Chapter 14: Java** - JVM architecture, GC, multithreading, collections framework, DSA patterns.
* **Chapter 15: Git & GitHub** - VCS internals, merge vs. rebase, branching strategies, internal state objects (blobs/commits).
* **Chapter 16: REST APIs & JSON** - HTTP-based contract design, status codes, serialization, payload design.
* **Chapter 17: HTTP/HTTPS** - Connection lifecycles, TCP handshakes, TLS/SSL, HTTP/2 & HTTP/3.
* **Chapter 18: Authentication & Authorization** - Sessions vs JWTs, OAuth2/OIDC protocols, security policies (CORS, CSRF).

### 6. Data Science & AI/GenAI
* **Chapter 19: NumPy** - Vectorization, ndarray memory layouts, broadcasting mechanics, linear algebra.
* **Chapter 20: Pandas** - DataFrames, Series, alignment, grouping, merging, performance tuning (vectorized methods).
* **Chapter 21: Matplotlib & Seaborn** - Graphics syntax, canvas rendering, styling, advanced statistical charts.
* **Chapter 22: Scikit-Learn** - Classical ML modeling, data pipelines, regression, classification, clustering, validation.
* **Chapter 23: TensorFlow & PyTorch** - Dynamic vs. static computation graphs, autograd, layer mechanics, custom pipelines.
* **Chapter 24: LangChain** - LLM orchestrations, chains, memory patterns, agents, expression language (LCEL).
* **Chapter 25: RAG & Vector Databases** - Information retrieval, vector indexing (HNSW, IVF), search metrics (cosine similarity).
* **Chapter 26: Embeddings** - Vector representations, model architectures (BERT, OpenAI), dimensionalities.
* **Chapter 27: LLM, Prompt Engineering & GenAI** - Attention mechanism, Transformers, decoding (temperature, top-p), prompt techniques.

---

## How to Read the Booklet

### 1. Interactive Reader (`reader.html`)
For the best reading and study experience, open the included `reader.html` in your browser. 
* **If running a local HTTP server** (e.g., via `python3 -m http.server 8000` or VS Code Live Server): Open `http://localhost:8000/reader.html`. The reader will scan and load the chapters automatically.
* **If opening via `file://` directly**: Open the file in your browser, drag and drop this `booklet` project folder, or click **Browse Folders** to select this folder. The app uses the HTML5 Folder API to read the markdown files locally without requiring a local server!

#### Key Features in Reader:
- **Practice Mode**: Extracts Section 8 from any chapter and builds an interactive flashcard interface where you can review questions, test yourself, and toggle details.
- **Search**: Fast search across titles.
- **Tab Layouts**: Easily switch between standard study chapters and interactive practice tools.
- **Glassmorphic Theme**: A premium dark theme designed to be easy on the eyes.

### 2. Compile into a Single File (`compile.py`)
To merge all individual chapters into a single markdown handbook (`booklet.md`), run the compilation script:

```bash
python3 compile.py
```

This merges the chapters chronologically, creates a master Table of Contents, and inserts print page-breaks so you can convert `booklet.md` to a clean PDF.
