# 23. RAG (Retrieval-Augmented Generation)

## 1. Introduction

### What it is
Retrieval-Augmented Generation (RAG) is an architectural framework that enhances the accuracy, reliability, and factual grounding of Large Language Model (LLM) outputs. It does this by dynamically retrieving relevant external knowledge from authoritative data sources at query time and injecting this context directly into the model's prompt. Instead of relying solely on the model's pre-trained parametric memory (the weights learned during training), RAG grounds the model's generation in retrieved documents.

### Why it exists
While LLMs display impressive linguistic capabilities, they suffer from three fundamental limitations in production environments:
1. **Hallucinations**: LLMs generate grammatically correct but factually incorrect assertions when their training data lacks the answer.
2. **Knowledge Cutoffs**: An LLM's knowledge is static, frozen at the moment pre-training finished. Re-training or fine-tuning models to update knowledge is slow and expensive.
3. **Lack of Private Data Access**: LLMs have no access to private enterprise repositories, local codebases, or real-time user-specific profiles.

RAG bridges this gap by decoupling the model's reasoning capabilities (linguistics, synthesis) from its knowledge base, turning the LLM into a real-time processor over retrieved context.

### Problems it solves
- **Factuality & Hallucinations**: Constrains model responses to the facts contained within retrieved context documents.
- **Dynamic Knowledge Updates**: Bypasses the need for expensive model retraining; updating the system's knowledge is as simple as adding or updating document vectors in a database.
- **Data Security & Authorization**: Allows applying role-based access control (RBAC) at the retrieval stage, ensuring users only retrieve context they are authorized to view.
- **Traceability and Citations**: Enables models to cite exact source documents and line ranges for their assertions, making verification simple for users.

### Industry Use Cases
- **Enterprise Semantic Search**: Allowing employees to query internal wikis, policy documents, and HR databases using natural language.
- **Customer Support Automation**: Powering conversational bots that answer questions based on the latest product specifications and returns policies.
- **Automated Code Assistants**: Injecting local repository context, active file lines, and library documentation to generate accurate code recommendations.
- **Medical & Legal Document Analysis**: Extracting terms, clause histories, or patient records to assist specialists, backed by direct source citations.

### Analogy
If an LLM is a **brilliant student taking a closed-book exam** (relying only on what they memorized during study months ago), RAG is giving that student **access to a search engine and an open library** during the exam. The student doesn't need to memorize every fact; they just need to find the correct book, read the relevant paragraphs, and write a synthesized response citing their sources.

---

## 2. Core Concepts

### Beginner Concepts

#### The Retrieval-Generation Loop
The RAG pipeline operates as a two-stage process:
1. **Retrieval**: The system queries a vector or keyword database using the user's input to find the most relevant document chunks.
2. **Generation**: The retrieved chunks are formatted into a prompt template along with the user's query, and the LLM synthesizes the final response based on this context.

```text
User Query ──> [ Retrieval System ] ──> Fetches Context Chunks ──┐
                                                                 v
User Query + Context Chunks ──> [ LLM Generation ] ──> Grounded Answer
```

#### Chunking
The process of breaking down long documents (like 50-page PDFs) into smaller, coherent text segments (chunks) before indexing. This is necessary because:
- LLMs have finite context windows.
- Retrieval is more precise when searching small, focused text segments rather than entire books.

#### Chunk Overlap
The number of characters or tokens shared between consecutive chunks. An overlap of 10-25% prevents losing context for information that falls on a chunk boundary.

### Intermediate Concepts

#### Chunking Strategies
- **Fixed-Size Chunking**: Splits text into a fixed number of tokens/characters with a set overlap (e.g. 500 characters with a 50-character overlap). Simple but can split sentences mid-thought.
- **Recursive Character Splitting**: Splitting text based on a hierarchy of separators (e.g., paragraphs `\n\n`, then sentences `\n`, then spaces ` `) to keep sentences and paragraphs whole.
- **Semantic Chunking**: Computes embeddings for consecutive sentences and splits the document when the similarity score drops below a threshold, ensuring each chunk is semantically coherent.

#### Hybrid Search and Reciprocal Rank Fusion (RRF)
Combines the strengths of:
- **Dense Retrieval (Embeddings)**: Captures semantic meaning, synonyms, and intent.
- **Sparse Retrieval (BM25/TF-IDF)**: Matches exact keywords, codes, names, or serial numbers.

The results are merged using **Reciprocal Rank Fusion (RRF)**, which scores each document based on its ranks in both searches, prioritizing documents that rank high in both:
$$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

#### Reranking
A two-stage retrieval pipeline. First, a fast Bi-Encoder retrieves the top 100 candidate chunks. Second, a heavy **Cross-Encoder reranking model** evaluates the query and candidate chunks together, scoring their relevance. This keeps search latency low while maintaining high accuracy.

#### Navigating the Hugging Face Hub
The Hugging Face Hub serves as the central repository for open-source AI models, hosting datasets, embeddings, rerankers, and large language models (LLMs). When building RAG pipelines:
- **Model Formats**: Models are stored in formats like `safetensors` (for standard PyTorch/TensorFlow execution) or `GGUF` (quantized format optimized for CPU and local running).
- **Hugging Face Hub Library (`huggingface_hub`)**: Programmatic API to search, download, and cache weights locally, facilitating offline inferences.
- **Pipelines**: The `transformers` library abstracts model loading, tokenization, and generation into simple API calls (e.g., `pipeline("text-generation", model="...")`).

#### Ollama for Local Model Execution
Ollama is a lightweight framework that packages open-source LLMs (like Llama 3, Mistral, and Gemma) and embeddings into self-contained local services.
- **Local API Endpoint**: Runs a background daemon exposing a standard REST API (usually at `http://localhost:11434/api/generate`) compatible with OpenAI SDKs and orchestration engines like LangChain.
- **Benefits for RAG**:
  - **Zero Data Leakage**: Sensitive enterprise or user data never leaves the local machine.
  - **Zero Cost**: Eliminates token fees associated with commercial APIs.
  - **Offline Functionality**: RAG pipelines can run completely offline.
- **Modelfile**: A configuration file used to define system prompts, temperature settings, and base model parameters for custom local models.

### Advanced Concepts

#### Query Expansion & HyDE
- **Multi-Query Expansion**: Uses an LLM to rewrite a user's query into 3-5 variations, searching the vector database with all variations to improve retrieval recall.
- **Hypothetical Document Embeddings (HyDE)**: Uses an LLM to generate a hypothetical answer to the user's query. This hypothetical answer is embedded and used to search the vector database. Searching with a document-like vector matches the format of indexed chunks better than a short query.

```text
Query: "How to fix error X?" ──> [ LLM ] ──> Hypothetical Answer: "To fix error X, configure..."
                                                      │
                                                      v
                                             [ Generate Embedding ] 
                                                      │
                                                      v
                                            [ Search Vector DB ]
```

#### Advanced Retrieval Patterns
- **Parent Document Retrieval (PDR)**: Splits documents into tiny child chunks (e.g. 100 tokens) for precise indexing. During retrieval, if a child chunk matches the query, the system retrieves its larger parent document (e.g. 1000 tokens) to feed to the LLM, ensuring the model receives sufficient context.
- **Hierarchical Retrieval**: Summarizes long documents and indexes the summaries. The system searches the summary index first to locate the document, then searches that document's internal chunks.

#### RAG Evaluation Frameworks (RAGAS)
Evaluating RAG systems requires measuring the retrieval and generation stages separately using metrics:
- **Faithfulness**: Is the generated answer grounded *only* in the retrieved context? (Measures hallucinations).
- **Answer Relevance**: Does the generated answer directly address the user's query?
- **Context Recall**: Did the retrieval system successfully fetch all the information needed to answer the query?
- **Context Precision**: Are the retrieved chunks ordered by relevance?

---

## 3. Internal Working

### Step-by-Step RAG Execution Pipeline

A complete RAG query executes through the following ingestion and retrieval pipelines:

```text
[ Data Ingestion Pipeline ]
Raw Documents (PDF, Wiki) ---> Text Extraction ---> Recursive Splitter ---> Overlapping Chunks
                                                                                |
                                                                                v
Vector Database Index  <--- Index Vectors <--- Generate Embeddings <--- HuggingFace Model

[ Query & Generation Pipeline ]
User Query 
    │
    ├──> 1. Multi-Query Expansion ---> Generate 3 query variations
    │                                            │
    └──> 2. Hybrid Retrieval <───────────────────┘
               ├──> Vector Search (Dense)
               └──> BM25 Search (Sparse)
                         │
                         v
               3. Reciprocal Rank Fusion (RRF) ---> Merge and Rank Chunks
                         │
                         v
               4. Cross-Encoder Reranker ---> Rescore top 20, select top 5
                         │
                         v
               5. Prompt Construction ---> Format Prompt: [System Instructions + Context + Query]
                         │
                         v
               6. LLM Synthesis ---> Grounded Response + Source Citations
```

---

## 4. Important Terminology

- **Parametric Memory**: The knowledge an LLM learns during training, stored in its parameters (weights).
- **Non-Parametric Memory**: External knowledge accessed by the model at runtime (e.g., retrieved document chunks).
- **Reranker**: A cross-encoder model that scores the semantic relevance of retrieved documents relative to a query.
- **HyDE**: Hypothetical Document Embeddings. A query transformation technique that embeds an LLM-generated answer to search for similar documents.
- **RAGAS**: Retrieval-Augmented Generation Assessment. An evaluation framework used to measure RAG quality.
- **Context Fragmentation**: A retrieval issue where the information needed to answer a query is split across separate chunks, causing the LLM to generate incomplete answers.

---

## 5. Beginner Examples

### Example 1: Basic In-Memory RAG using FAISS and OpenAI API
This example demonstrates a complete, simple RAG pipeline: indexing text, retrieving matching chunks, formatting a prompt, and generating an answer.

```python
import numpy as np
import faiss
import openai

# 1. Initialize API client and dataset
openai.api_key = "your-api-key"
chunks = [
    "To reset your password, navigate to settings, click security, and select reset password.",
    "Our refund policy allows returns within 30 days of purchase with a valid receipt.",
    "Python is an interpreted, high-level programming language created by Guido van Rossum."
]

# 2. Generate embeddings for database chunks
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response['data'][0]['embedding']

dimension = 1536
db_vectors = np.array([get_embedding(c) for c in chunks]).astype('float32')

# 3. Index vectors in FAISS
index = faiss.IndexFlatIP(dimension)  # Inner Product index
index.add(db_vectors)

# 4. Process user query
query = "How long do I have to return an item?"
query_vector = np.array([get_embedding(query)]).astype('float32')

# 5. Retrieve closest chunk
distances, indices = index.search(query_vector, k=1)
retrieved_context = chunks[indices[0][0]]
print("Retrieved Context:", retrieved_context)

# 6. Generate grounded response using LLM
prompt = f"""Use the following context to answer the question. If you don't know the answer based on the context, say "I cannot find the answer".

Context: {retrieved_context}

Question: {query}
Answer:"""

completion = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)
print("\nGenerated Answer:", completion.choices[0].message['content'])
```

---

## 6. Intermediate Examples

### Example 1: Implementing a Cross-Encoder Reranker
This example demonstrates retrieving candidate chunks and rerank-sorting them using a local Cross-Encoder model.

```python
from sentence_transformers import CrossEncoder

# Initialize local Cross-Encoder model
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

query = "How to optimize database queries?"
retrieved_chunks = [
    "To speed up database lookups, create indexes on frequently queried columns and set up Redis caching.",
    "Docker basics include writing a Dockerfile, building images, and running containers.",
    "SQL joins combine rows from two or more tables based on a related column between them."
]

# 1. Format pairs for the Cross-Encoder: [ [query, chunk1], [query, chunk2]... ]
pairs = [[query, chunk] for chunk in retrieved_chunks]

# 2. Score relevance
scores = reranker.predict(pairs)

# 3. Sort chunks based on relevance scores descending
ranked_results = sorted(zip(retrieved_chunks, scores), key=lambda x: x[1], reverse=True)

print("Reranked Chunks:")
for rank, (chunk, score) in enumerate(ranked_results):
    print(f"Rank {rank+1} (Score {score:.4f}): {chunk}")
```

---

### Example 2: Implementing Multi-Query Expansion
This example uses an LLM to generate query variations, improving retrieval recall.

```python
import openai
import numpy as np

def generate_query_variations(original_query):
    prompt = f"Generate 3 diverse search query variations for: '{original_query}'. Output only the queries, one per line."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    
    variations = response.choices[0].message['content'].strip().split('\n')
    return [original_query] + [v.strip() for v in variations if v.strip()]

# Test query expansion
query = "python decorator wraps"
expanded_queries = generate_query_variations(query)

print("Generated Query Variations:")
for q in expanded_queries:
    print("-", q)
```

---

### Example 3: Gemini RAG with Firestore Vector Search & Vertex AI
This example demonstrates generating dense vectors with Vertex AI, executing a vector query on Firestore Vector Search, and feeding the context to Gemini using System Instructions and Structured Output (Pydantic schema).

```python
import os
from google.cloud import firestore_v1
from google.cloud.firestore_v1.vector import Vector
from google.cloud.firestore_v1.base_vector_query import DistanceMeasure
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

# 1. Initialize Firestore & Gemini Clients
# Requires: pip install google-cloud-firestore google-genai pydantic
db = firestore_v1.Client(project="my-gcp-project")
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

# 2. Schema for Structured Gemini Output
class RAGResponse(BaseModel):
    answer: str = Field(description="The generated answer based strictly on context.")
    citations: list[str] = Field(description="List of document IDs or filenames used to answer.")
    confidence_score: float = Field(description="Float between 0 and 1 indicating answer certainty.")

# 3. Generate query embeddings using Vertex AI (via Gemini Client API)
def get_vertex_embedding(text: str) -> list[float]:
    response = gemini_client.models.embed_content(
        model="text-embedding-004",
        contents=text
    )
    return response.embeddings[0].values

# 4. Perform Firestore Vector Search
def search_firestore_vectors(query_text: str, limit: int = 2):
    query_vector = get_vertex_embedding(query_text)
    
    # query_vector is a list of floats, we use Vector(query_vector)
    collection_ref = db.collection("documents")
    vector_query = collection_ref.find_nearest(
        vector_field="embedding",
        query_vector=Vector(query_vector),
        distance_measure=DistanceMeasure.COSINE,
        limit=limit
    )
    
    results = []
    for doc in vector_query.stream():
        data = doc.to_dict()
        results.append({
            "id": doc.id,
            "content": data.get("content", ""),
            "source": data.get("source", "")
        })
    return results

# 5. Execute RAG Chain with Gemini
def gemini_rag_query(query: str) -> RAGResponse:
    # Retrieve relevant documents
    contexts = search_firestore_vectors(query)
    context_str = "\n\n".join([
        f"Doc ID: {c['id']}\nSource: {c['source']}\nContent: {c['content']}" 
        for c in contexts
    ])
    
    # Invoke Gemini with System Instructions and Structured JSON output
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"User Query: {query}\n\nRetrieved Context:\n{context_str}",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are an expert RAG Assistant. Answer the query based ONLY on the "
                "provided Retrieved Context. If the context does not contain the answer, "
                "state that you do not know. Return structural JSON matching the schema."
            ),
            response_mime_type="application/json",
            response_schema=RAGResponse,
            temperature=0.0
        )
    )
    
    # Gemini returns parsed JSON matching RAGResponse schema directly
    return RAGResponse.model_validate_json(response.text)

# Example execution:
# result = gemini_rag_query("What is the refund policy for active members?")
# print(f"Answer: {result.answer}")
# print(f"Citations: {result.citations}")
```

---

### Example 4: Local RAG with Ollama, Chroma DB, and Hugging Face Embeddings

This example shows how to configure a local RAG pipeline using only open-source libraries and a local model. 

#### Part A: Creating a Custom Model via Ollama Modelfile
To build a custom model with system instructions, we create a file named `Modelfile`:
```dockerfile
# 1. Specify the base model (pulled from Hugging Face / Ollama registry)
FROM llama3

# 2. Set the temperature (lower values are better for factual RAG)
PARAMETER temperature 0.0

# 3. Set the system prompt to enforce context constraints
SYSTEM """
You are a local RAG assistant. Answer user questions using only the provided context.
If the answer is not present in the context, respond with 'Answer not found in context'.
Do not use pre-trained external knowledge.
"""
```
To build this custom model, run:
```bash
ollama create local-rag-assistant -f ./Modelfile
```

#### Part B: Running the Python local RAG Pipeline
This script runs the query using Chroma DB for local vector search, Hugging Face's `all-MiniLM-L6-v2` for embeddings, and queries our custom local Ollama model.

```python
import os
import requests
import chromadb
from chromadb.utils import embedding_functions

# 1. Setup local Chroma DB and load embedding function from Hugging Face Hub
# Requires: pip install chromadb sentence-transformers requests
chroma_client = chromadb.PersistentClient(path="./local_chroma")

# Use a local Sentence Transformer model from Hugging Face
hf_embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# 2. Get or create collection
collection = chroma_client.get_or_create_collection(
    name="local_knowledge_base",
    embedding_function=hf_embedding_func
)

# 3. Ingest documents
documents = [
    "Project Orion is scheduled for launch in Q4 2026 under lead developer Sarah Jenkins.",
    "The codebase coding standard mandates using explicit type hints for all public APIs.",
    "We use pre-receive git hooks to prevent committing secret keys to the repo."
]
collection.upsert(
    ids=["doc1", "doc2", "doc3"],
    documents=documents,
    metadatas=[{"source": "management"}, {"source": "guidelines"}, {"source": "security"}]
)

# 4. Search local collection
query = "When is Project Orion launching?"
results = collection.query(
    query_texts=[query],
    n_results=1
)

retrieved_doc = results["documents"][0][0]
retrieved_meta = results["metadatas"][0][0]
print(f"Retrieved Document: {retrieved_doc} (Source: {retrieved_meta['source']})")

# 5. Format prompt and query local Ollama API
ollama_url = "http://localhost:11434/api/generate"
prompt = f"""Context: {retrieved_doc}

Question: {query}
Answer:"""

payload = {
    "model": "local-rag-assistant",
    "prompt": prompt,
    "stream": False
}

try:
    response = requests.post(ollama_url, json=payload)
    response_data = response.json()
    print("\nOllama Local Answer:")
    print(response_data.get("response"))
except Exception as e:
    print(f"\nFailed to connect to local Ollama API: {e}")
    print("Ensure Ollama is running (`ollama serve`) and the custom model is created.")
```

---

## 7. Advanced Concepts

### Deep Pipeline Analysis and Evaluation

#### Parametric vs. Non-Parametric Memory Trade-offs
Understanding the trade-offs of storing knowledge in model weights (parametric) versus external databases (non-parametric):

| Feature | Parametric Memory (Fine-tuning) | Non-Parametric Memory (RAG) |
|---|---|---|
| **Knowledge Update Cost** | High (Requires GPU training runs). | Low (Add/update vectors in database). |
| **Hallucination Control** | Low (Model can still hallucinate). | High (Constrained by retrieved context). |
| **Access Control (RBAC)** | Impossible (Cannot selectively hide weights). | Simple (Enforced at database retrieval stage). |
| **Traceability (Citations)** | Poor (Cannot trace weight activations to sources). | High (Cites source chunks and URLs). |
| **Best Use Case** | Teaching models style, tone, or specific formatting rules. | Injecting facts, policies, and real-time data. |

#### Context Window Fragmentation and Lost in the Middle
LLMs can struggle to process information that appears in the middle of long prompts. If you retrieve 20 chunks and concatenate them, the model is more likely to ignore the chunks in the middle, focusing only on the beginning and the end.
- *Fixes*:
  1. Use a **Reranker** to limit retrieved chunks to the top 3-5.
  2. Structure the prompt to place the most critical context chunks at the very beginning and very end of the context block.

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers want to see if you can evaluate system trade-offs. They will check if you understand chunking strategies, how to measure RAG quality using metrics (faithfulness vs recall), how to handle latency budgets, and how to design production-ready retrieval pipelines.

### Red Flags
- **Ignoring Chunk Overlap**: Splitting text into fixed sizes without any overlap, which cuts sentences in half and loses semantic context at boundaries.
- **Assuming Fine-Tuning Solves Hallucinations**: Recommending fine-tuning to prevent a model from hallucinating facts. Fine-tuning teaches style, not facts.
- **No Ingestion Deduplication**: Designing a document ingestion pipeline that re-indexes the entire corpus on every document update, ignoring the high processing cost.

### Green Flags
- **Two-Stage Retrieval**: Proposing a fast Bi-Encoder for initial retrieval followed by a Cross-Encoder reranker to optimize relevance.
- **RAGAS Evaluation**: Using evaluation frameworks to measure faithfulness, answer relevance, and context recall.
- **Metadata Filtering during Graph Traversal**: Recommending single-stage filtering in vector databases to prevent empty search results.

### Answers Matrix

| Level | Question: "How do you evaluate and optimize a RAG system that is returning out-of-date answers?" |
|---|---|
| **Rejected** | "Re-train or fine-tune the LLM on the new data so it memorizes the updates." |
| **Shortlisted** | "Update the vector database index with the new documents and increase the context window size." |
| **Selected** | "I would set up an evaluation pipeline using the RAGAS framework to measure Faithfulness and Context Recall. If the system is returning out-of-date answers, it indicates a Context Recall issue. To fix this, I would check the ingestion pipeline to ensure updates are propagated to the vector database. I would implement hybrid search (BM25 + Dense) with Reciprocal Rank Fusion to improve retrieval accuracy. I would also add a Cross-Encoder reranker to prioritize the most relevant chunks in the prompt, and implement citation validation to ensure the model's assertions match the source documents." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is Retrieval-Augmented Generation (RAG) and why is it used?
- **Detailed Answer**: RAG is an architectural framework that enhances LLM outputs by retrieving relevant external knowledge from authoritative data sources at query time and injecting this context directly into the model's prompt. It is used because LLMs suffer from hallucinations, knowledge cutoffs, and have no access to private or real-time data. decoupling reasoning (LLM) from knowledge (Vector DB) makes system updates simple and cost-effective.
- **Follow-up Questions**: Can RAG be used with open-source local models? (Answer: Yes. You can host a local embedding model (like MiniLM) and a local LLM (like Llama-3) to run a complete RAG pipeline locally, keeping data secure).
- **Interviewer's Expectations**: Define RAG as a retrieval + generation pipeline that grounds LLM outputs in external context.

#### 2. What is chunking, and why does chunk overlap matter?
- **Detailed Answer**: Chunking is the process of breaking down long documents into smaller, coherent text segments before indexing. Chunk overlap is the number of characters or tokens shared between consecutive chunks.
  - Overlap is critical because it prevents losing context for information that falls on a chunk boundary. If a sentence discussing a critical fact is split in half across two chunks, the retriever may fail to match either chunk.
- **Follow-up Questions**: What is the typical overlap percentage? (Answer: Typically 10% to 25% of the chunk size).
- **Interviewer's Expectations**: Explain chunking and how overlap prevents context loss at boundaries.

#### 3. What is the difference between the retrieval stage and the generation stage in RAG?
- **Detailed Answer**:
  - **Retrieval Stage**: Querying a database (using embeddings or keywords) to find the most relevant document chunks. This stage is evaluated using metrics like **Context Recall** (did we retrieve the right information?) and **Context Precision** (are matches ranked correctly?).
  - **Generation Stage**: The LLM synthesizes the final response based on the retrieved context. Evaluated using **Faithfulness** (are there hallucinations?) and **Answer Relevance** (does it answer the query?).
- **Follow-up Questions**: Which stage is usually the primary bottleneck for accuracy? (Answer: The retrieval stage. If the retriever fails to fetch the correct context, the generator cannot write a correct answer).
- **Interviewer's Expectations**: Differentiate the functions and metrics of both stages.

#### 4. What is hybrid search and why is it preferred in production RAG systems?
- **Detailed Answer**: Hybrid search combines dense vector search (embeddings) with sparse keyword search (BM25).
  - Dense search captures semantic meaning and intent.
  - Sparse search matches exact keywords, codes, names, or serial numbers.
  - Production systems prefer hybrid search because it provides high recall for conceptual queries while still matching exact keywords and technical terms.
- **Follow-up Questions**: How do we merge results from both searches? (Answer: Using Reciprocal Rank Fusion (RRF)).
- **Interviewer's Expectations**: Explain the semantic vs keyword matching trade-offs and RRF merging.

#### 5. What is a reranker and why is it used in RAG pipelines?
- **Detailed Answer**: A reranker is a Cross-Encoder model that evaluates a query and a retrieved document chunk together, scoring their semantic relevance.
  - Standard retrieval uses Bi-Encoders to generate embeddings independently, which is fast but can miss complex relationships.
  - A reranker is slower but much more accurate. We use a two-stage pipeline: retrieve the top 100 candidates using a fast Bi-Encoder, then rerank them using a Cross-Encoder to select the top 5 most relevant chunks to feed to the LLM.
- **Follow-up Questions**: What is the latency impact of adding a reranker? (Answer: Typically adds 50-100ms, which is acceptable for most applications).
- **Interviewer's Expectations**: Compare Bi-Encoders and Cross-Encoders and explain the two-stage retrieval pipeline.

#### 6. Explain the HyDE (Hypothetical Document Embeddings) technique.
- **Detailed Answer**: HyDE is a query transformation technique:
  1. The user's query is passed to an LLM to generate a hypothetical answer.
  2. This hypothetical answer is embedded using an embedding model.
  3. The hypothetical vector is used to search the vector database.
  - This improves retrieval because a document-like vector matches the format and structure of indexed chunks better than a short query vector.
- **Follow-up Questions**: When does HyDE perform poorly? (Answer: When the LLM generates a highly incorrect hypothetical answer, leading the search to a completely wrong region of the vector space).
- **Interviewer's Expectations**: Describe the hypothetical generation, embedding, and search steps.

#### 7. What is context window overflow and how do you prevent it?
- **Detailed Answer**: Context window overflow occurs when the size of the prompt (including system instructions, retrieved context chunks, and history) exceeds the LLM's maximum token limit, causing the model to reject the request or truncate the input.
  - **Prevention**:
    1. Implement chunk sizing and limit retrieved candidates using a reranker.
    2. Compress context using tools like LLMLingua to remove redundant tokens.
    3. Monitor token counts dynamically using tokenizers before sending requests.
- **Follow-up Questions**: How does a model's performance change as the context window fills up? (Answer: Models can suffer from the "lost in the middle" effect, ignoring information placed in the middle of long prompts).
- **Interviewer's Expectations**: Define context limits and propose chunk control and token compression.

#### 8. How do you evaluate the quality of a RAG system?
- **Detailed Answer**: We use frameworks like RAGAS to measure the system using four core metrics:
  - **Faithfulness**: The percentage of claims in the generated answer that are present in the retrieved context (measures hallucinations).
  - **Answer Relevance**: How directly the generated answer addresses the query.
  - **Context Recall**: The percentage of ground-truth information successfully retrieved by the search system.
  - **Context Precision**: The ranking quality of the retrieved chunks.
- **Follow-up Questions**: How do we generate evaluation datasets? (Answer: Use an LLM to generate synthetic query-context-answer triplets from your document corpus).
- **Interviewer's Expectations**: List the core evaluation metrics and explain how they isolate retrieval and generation performance.

#### 9. What are the main techniques for mitigating hallucinations in RAG?
- **Detailed Answer**:
  - **Prompt Engineering**: Instruct the model to answer *only* based on the provided context, and write "I do not know" if the context does not contain the answer.
  - **Cross-Encoder Reranking**: Ensure only highly relevant chunks are included in the prompt.
  - **Self-RAG (Self-Reflection)**: Train or prompt the model to generate reflection tokens evaluating whether its answer is supported by the context.
  - **Post-Processing Checks**: Use a separate validator model to verify that all sentences in the answer match the source document text.
- **Follow-up Questions**: Can we completely eliminate hallucinations? (Answer: No, because LLMs are probabilistic models. We can only minimize the likelihood).
- **Interviewer's Expectations**: Propose prompt constraints, reranking, reflection, and validation checks.

#### 10. Contrast RAG with Fine-Tuning. When should you choose each?
- **Detailed Answer**:
  - **RAG**: Decouples reasoning from knowledge. Best for injecting facts, document data, and real-time updates. Low cost and simple to maintain.
  - **Fine-Tuning**: Modifies model behavior, style, tone, or formatting rules. Best for teaching a model specific syntaxes (like SQL queries), adapting to specialized vocabularies, or training on specific tasks (like classification). High cost and slow to execute.
- **Follow-up Questions**: Can we use them together? (Answer: Yes. Fine-tune a model to output structured JSON responses, and use RAG to inject the factual context for the JSON fields).
- **Interviewer's Expectations**: Compare style modifications vs knowledge injection in terms of cost and maintenance.

---

### Scenario-Based Questions

#### 11. Your RAG system retrieves relevant context, but the LLM still outputs incorrect answers. How do you diagnose and resolve this?
- **Detailed Answer**: This indicates a **Generation Failure** (the retriever succeeded, but the generator failed).
  - **Diagnosis**:
    1. Inspect the constructed prompt. Verify that the retrieved chunks are present and clear.
    2. Check for the "lost in the middle" effect: if the correct chunk is placed in the middle of 20 other chunks, the LLM may ignore it.
  - **Resolution**:
    - Improve prompt formatting: use clear XML tags (e.g. `<context>...</context>`) to separate chunks.
    - Reduce context size: use a reranker to limit retrieved chunks to the top 3-5.
    - Instruct the model to write step-by-step reasoning (Chain-of-Thought) before outputting the final answer.
- **Follow-up Questions**: Does increasing model temperature increase hallucinations? (Answer: Yes. Higher temperature increases randomness, which can cause the model to ignore context constraints).
- **Interviewer's Expectations**: Identify prompt formatting, context size, and reasoning constraints as key factors.

#### 12. You are building a legal document Q&A RAG system. Queries require referencing exact sections and clauses. How do you design this?
- **Detailed Answer**:
  - **Data Ingestion**: Use a parser that preserves document formatting (like layout headers and paragraph structures). Split text using **Recursive Character Splitting** on paragraph boundaries rather than arbitrary token counts.
  - **Parent Document Retrieval (PDR)**: Index small, specific clauses (child chunks) for precise retrieval, but map each child to its parent paragraph or section. During retrieval, if a clause matches the query, feed the full parent section to the LLM.
  - **Metadata Mapping**: Store document title, page number, and clause ID in chunk metadata, and prompt the LLM to cite these fields directly in its response (e.g., "[Document A, Clause 4.2]").
- **Follow-up Questions**: Why not use fixed-size chunking for legal documents? (Answer: Because fixed splits can cut clauses in half, losing their legal meaning).
- **Interviewer's Expectations**: Propose layout-aware chunking, parent document retrieval, and metadata citations.

#### 13. You are designing a customer support RAG bot. Policy updates occur in real-time. How do you keep the bot's knowledge fresh?
- **Detailed Answer**:
  - **Real-Time Sync**: Avoid full index rebuilds. Use a vector database that supports real-time upserts and deletes (like Qdrant or Pinecone).
  - **Ingestion Workers**: Set up event listeners on your policy database. When a policy is updated:
    1. Generate embeddings for the updated text.
    2. Upsert the new vectors into the vector database using their document IDs.
    3. Old segments are automatically overwritten or deleted.
  - **Cache Eviction**: Clear cached LLM responses when relevant policies are updated.
- **Follow-up Questions**: How do you handle queries that arrive during an index merge? (Answer: Vector databases use segment-level indexing to ensure search queries continue to run on the old index until the merge completes).
- **Interviewer's Expectations**: Recommend real-time database upserts, event listeners, and cache eviction.

#### 14. How do you design a multilingual RAG system where users query in Spanish, but documentation is stored in English?
- **Detailed Answer**:
  - **Approach 1: Multilingual Embeddings (Recommended)**: Use a multilingual embedding model (like `multilingual-e5-base` or Cohere multilingual). These models map translations of the same concept to nearby coordinates in the shared vector space. When a user queries in Spanish, the model retrieves the relevant English documents directly.
  - **Approach 2: Translation Pipeline**: Translate the query to English using a translation API before searching, and translate the generated English response back to Spanish. This is slower and more expensive but works with single-language models.
- **Follow-up Questions**: Which approach has lower latency? (Answer: Multilingual embeddings, as they bypass translation API round-trips).
- **Interviewer's Expectations**: Compare multilingual embeddings with translation pipelines in terms of latency and cost.

#### 15. Your RAG system retrieves conflicting information from two different documents. How do you instruct the LLM to resolve this?
- **Detailed Answer**:
  - **Prompt Constraints**: Instruct the model to identify the conflict explicitly in its response, state both viewpoints, and cite the respective sources:
    ```text
    "If the retrieved documents contain conflicting information, state both viewpoints, list their sources, and explain the contradiction. Do not attempt to choose a viewpoint unless one is marked as more recent."
    ```
  - **Metadata Versioning**: Add a `last_modified` timestamp to document metadata. In the prompt, list the timestamps along with the context chunks, allowing the LLM to prioritize the most recent information.
- **Follow-up Questions**: Can we filter out older versions before retrieval? (Answer: Yes, by applying a metadata filter that only searches the most recent version of each document).
- **Interviewer's Expectations**: Propose prompt instructions, metadata timestamps, and version filtering.

---

### Debugging Questions

#### 16. Your RAG bot outputs generic answers, ignoring the retrieved context. How do you debug this?
- **Detailed Answer**:
  - **Root Cause**:
    1. **System Prompt Overwrite**: The system prompt instructs the model to act as a general assistant, causing it to rely on its parametric memory instead of the context.
    2. **Weak Context Layout**: The retrieved chunks are formatted poorly in the prompt, making them difficult for the model to distinguish.
    3. **Context Length**: The context is too long, causing the model to ignore the details.
  - **Fixes**:
    - Update the system prompt to explicitly restrict answers to the provided context:
      ```text
      "Answer the query ONLY using the provided context. If the answer is not in the context, write 'I do not know'."
      ```
    - Wrap context chunks in XML tags: `<context><chunk id="1">...</chunk></context>`.
    - Reduce the number of retrieved chunks using a reranker.
- **Follow-up Questions**: Does lowering the model's temperature help? (Answer: Yes, it reduces randomness and keeps the model focused on the provided context).
- **Interviewer's Expectations**: Trace system prompt conflicts, prompt formatting, and context lengths.

#### 17. The retrieved document chunks are irrelevant to the user's query, despite having high vector similarity scores. How do you debug this?
- **Detailed Answer**:
  - **Root Cause**:
    1. **Mismatched Models**: The query is embedded using a different model or tokenizer than the one used to index the document corpus.
    2. **Semantic Drift**: The query contains slang or formatting styles that differ from the document corpus, causing the model to map the query to random coordinates.
    3. **Index Drift**: The vector index is corrupted or out-of-date.
  - **Fixes**:
    - Verify that both query and document ingestion pipelines use the exact same model and tokenizer configurations.
    - Check the cosine similarity values. If all matches have low scores (e.g. $<0.3$), implement a similarity threshold to filter out irrelevant matches.
- **Follow-up Questions**: Why do mismatched models cause irrelevant retrievals? (Answer: Because different models represent the vector space differently. A vector from Model A has no semantic relationship to a vector from Model B).
- **Interviewer's Expectations**: Verify model synchronization across pipelines and implement similarity thresholds.

#### 18. The LLM ignores the retrieved context and hallucinates a response. How do you prevent this?
- **Detailed Answer**:
  - **Root Cause**:
    1. **Lack of Prompt Constraints**: The prompt does not explicitly instruct the model to use the context.
    2. **High Temperature**: The model's temperature is set too high, increasing randomness.
    3. **Uninformative Context**: The retrieved context is irrelevant, forcing the model to guess.
  - **Fixes**:
    - Restrict the model's instructions:
      ```text
      "Answer the query ONLY using the provided context. Do not use external knowledge. If the context does not contain the answer, reply 'Context not found'."
      ```
    - Set the model's temperature to 0.0.
    - Monitor context recall. If the retriever fails, return a fallback message.
- **Follow-up Questions**: Does fine-tuning a model on your documents prevent hallucinations? (Answer: No. Fine-tuning teaches style and formatting, but does not prevent the model from hallucinating facts when prompt context is missing).
- **Interviewer's Expectations**: Restrict prompt instructions, lower model temperature, and monitor retrieval quality.

#### 19. The query latency of your RAG pipeline is too high for production (e.g., > 2 seconds). How do you optimize it?
- **Detailed Answer**:
  - **Latency Profiling**: Break down the pipeline latency:
    $$\text{Total Latency} = \text{Query Embedding} + \text{Retrieval} + \text{Reranking} + \text{LLM Generation}$$
  - **Optimization Steps**:
    1. **LLM Generation (usually the largest bottleneck)**: Use a smaller, faster model (e.g. GPT-4o-mini instead of GPT-4o), enable **Streaming** to return tokens to the user as they are generated, and lower the max token limit.
    2. **Reranking**: Reduce the number of candidates passed to the reranker (e.g. rerank the top 20 instead of the top 100).
    3. **Retrieval**: Use quantized vector indexes (SQ8 or PQ) to speed up database queries.
- **Follow-up Questions**: How does streaming tokens improve user-perceived latency? (Answer: It reduces the Time to First Token (TTFT), making the interface feel responsive even if the full generation takes time).
- **Interviewer's Expectations**: Profile the latency stages and propose model selection, streaming, and index optimizations.

#### 20. The citations generated by your RAG bot do not match the actual source documents. How do you fix this?
- **Detailed Answer**:
  - **Root Cause**: The LLM is hallucinating citation associations or getting confused by the layout of the retrieved context.
  - **Fixes**:
    1. **Unique Chunk Identifiers**: Assign a unique ID to each chunk in the prompt (e.g. `[Doc 1]`, `[Doc 2]`) and instruct the model to append these tags directly to its sentences:
       ```text
       "For every factual claim you make, append the corresponding source ID tag (e.g., [Doc 1]). Do not group citations at the end."
       ```
    2. **Post-Processing Validation**: Write a Python script to verify that all citation tags generated by the LLM match the IDs of the retrieved chunks. If a citation tag is invalid, remove it or flag the response.
- **Follow-up Questions**: Can we use a Cross-Encoder to validate citations? (Answer: Yes. We can score the similarity of each generated sentence against its cited chunk, removing citations with low relevance scores).
- **Interviewer's Expectations**: Implement structured citation tags and post-processing validation.

---

### System Design Questions

#### 21. Design a secure enterprise Q&A RAG system for 50,000 employees.
- **Detailed Answer**:
  - **Architecture Components**:
    1. **Data Connectors**: Ingest files from Google Drive, Slack, and Confluence.
    2. **Security Gateway**: Map user group permissions (active directory) to document metadata.
    3. **Vector Database**: Use a self-hosted vector database (like Qdrant) partitioned by tenant or group namespace.
    4. **Query Handler**:
       - Authenticate the user and retrieve their access permissions.
       - Query the vector database, applying metadata filters to restrict search to documents the user is authorized to view.
       - Rerank candidates and pass them to the LLM.
       - Log queries and audit citations for compliance.
- **Follow-up Questions**: How do you prevent sensitive company data from leaking to external LLM providers? (Answer: Host local, open-source models (like Llama-3) on private GPU instances, keeping data within the company's network).
- **Interviewer's Expectations**: Cover data connectors, role-based access control (RBAC), namespace partitioning, and data privacy.

---

#### 22. Design an automated Code Assistant RAG system for a software development team.
- **Detailed Answer**:
  - **Data Ingestion**:
    - Parse codebase repositories. Split code files into chunks using AST (Abstract Syntax Tree) parsing to keep classes and functions whole.
    - Index code chunks and natural language documentation in a vector database.
  - **Context Collection**:
    - The IDE extension collects: the user's active file lines, diagnostic warnings, and recent file edit histories.
  - **Retrieval and Generation**:
    - Generate query embeddings using a code-specific model (like CodeBERT).
    - Query the vector database to retrieve relevant functions and API documentation.
    - Format a prompt containing the active file code, diagnostic warnings, and retrieved context.
    - Generate code recommendations and return them to the IDE.
- **Follow-up Questions**: Why use AST parsing instead of character splitting for code? (Answer: Character splits can cut functions in half, breaking their logical structure and rendering the context useless).
- **Interviewer's Expectations**: Propose AST-based chunking, code-specific models, and IDE context collection.

---

#### 23. Design a medical Q&A RAG system with strict sourcing requirements.
- **Detailed Answer**:
  - **Ingestion Pipeline**:
    - Parse medical journals and textbooks, indexing text and table coordinates.
    - Add metadata fields containing the author, publication date, and journal section.
  - **Verification Pipeline**:
    - Use a high-precision model (like GPT-4) with a low temperature (0.0).
    - Implement a **Self-Reflection loop**: the model must verify that each generated assertion matches a specific sentence in the retrieved context before outputting the answer.
    - If the context does not contain the answer, return a fallback message.
  - **Logging**:
    - Save all user queries, retrieved chunks, and generated responses to an audit log for compliance reviews.
- **Follow-up Questions**: Why is a reflection loop critical for medical applications? (Answer: Because medical errors have high risks. A reflection loop acts as a validation boundary, catching hallucinations early).
- **Interviewer's Expectations**: Detail the metadata structure, self-reflection validation, fallback logic, and compliance logging.

---

#### 24. How do you build a completely offline RAG system using Hugging Face and Ollama? What are the limitations?
- **Detailed Answer**: To build a completely offline RAG system, you load local Hugging Face embeddings (e.g. `all-MiniLM-L6-v2`) via libraries like `sentence-transformers`, index the vectors in a local database like Chroma DB or FAISS, and query a local model hosted on Ollama (e.g. Llama 3) via REST requests. Limitations include performance bottlenecks on local hardware (CPUs vs GPUs), high memory footprints, and potential quality drops compared to massive cloud models.
- **Follow-up Questions**: How can you run a local model on CPU with acceptable latency? (Answer: Use quantized GGUF models via llama.cpp or Ollama which compress model weights and run fast on CPU).
- **Interviewer's Expectations**: Describe the offline pipeline steps (local embeddings, local DB, local model) and identify key resource constraints (CPU/GPU, quantization, memory limits).

---

#### 25. What is a Modelfile in Ollama and how do you use it to configure a local RAG assistant's behavior?
- **Detailed Answer**: A Modelfile is a configuration script for creating and sharing models with Ollama. It defines the base model (using `FROM`), system instructions (using `SYSTEM`), runtime parameters like temperature and context size (using `PARAMETER`), and template formatting (using `TEMPLATE`). In a local RAG setup, you use the Modelfile to lock down the temperature to `0.0` and set system prompts that enforce the model to only answer using retrieved context.
- **Follow-up Questions**: What parameters are crucial in a RAG Modelfile? (Answer: `PARAMETER temperature 0.0` to minimize randomness, and `PARAMETER num_ctx 4096` to ensure the model has enough context window size for the retrieved documents).
- **Interviewer's Expectations**: Explain the purpose of a Modelfile, its main commands (FROM, SYSTEM, PARAMETER), and how custom prompt restrictions ground local generation.

---

## 10. Common Mistakes

- **Splitting chunks without overlap**: Cuts sentences in half, causing the model to lose context at boundaries.
- **Using general models for specialized domains**: Using general text embedding models for code or medical searches, which results in poor retrieval quality. Use domain-specific models instead.
- **Overlooking retrieval evaluation**: Fine-tuning generation prompts without measuring retrieval recall. If the retriever fails to fetch the correct context, prompt optimization cannot fix the answer.

---

## 11. Comparison Section: Knowledge Representation Strategies

| Strategy | RAG (Retrieval-Augmented) | Fine-Tuning | Long Context Windows |
|---|---|---|---|
| **Knowledge Type** | Non-parametric (external DB). | Parametric (model weights). | Temporary context (in-prompt). |
| **Update Latency** | Instant (update database vectors). | Slow (requires training runs). | Instant (insert data in prompt). |
| **Max Capacity** | Practically unlimited (vector scale). | High (limited by model capacity). | Limited by context window (e.g. 128k). |
| **Cost per Query** | Low (small prompt size). | Low. | High (processing long prompts). |
| **Best Use Case** | Real-time data, wikis, policies. | Adapting style, tone, or formatting. | One-off document analysis. |

---

## 12. Practical Project Ideas

### Beginner
- **Markdown Wiki RAG**: Build a terminal search bot. Index 50 markdown files using a local Sentence-Transformer model, store the vectors in a FAISS index, and build a CLI to answer questions based on the wiki.

### Intermediate
- **Hybrid Search RAG with Reranking**: Build an API server that implements hybrid search:
  - Connect a search database (Elasticsearch/BM25) with a vector database (Qdrant).
  - Search both databases using a query, merge the results using RRF, rerank the top candidates using a Cross-Encoder, and generate the final answer using an LLM.
- **Historical Figure Chatbot**: Implement a conversational interface where the user chats with a simulated historical figure (e.g., Abraham Lincoln). Ingest public historical letters/speeches of the figure, store conversation history in memory, and feed both history and retrieved context to the LLM.

### Advanced/Resume-worthy
- **Agentic RAG with Iterative Retrieval**: Develop a production-ready conversational agent:
  - Implement a multi-step planner: the agent evaluates a query, decomposes it into sub-queries, and searches the index.
  - If the retrieved context is incomplete, the agent dynamically generates follow-up queries.
  - Integrate a reflection loop to validate citations and check for hallucinations before returning responses.
  - Wrap the system in Docker containers and expose REST API endpoints.
- **Legal Document Assistant with Chat History**: Build a tool to parse multi-page legal contracts. Set up parent-child retrieval so details are retrieved but whole clauses are returned. Implement a conversational buffer memory window to maintain context over a multi-turn dialogue, and add citation validation to ensure all claims references exist in the source document.

---

## 13. Internship Preparation Notes

- **Recruiters Focus on**: Core concepts of RAG pipelines, differences between sparse and dense search, and basic chunking strategies.
- **Applied ML Roles**: Require understanding of reranking, query transformation (HyDE), and evaluation frameworks (RAGAS).
- **Data Engineering Integration**: Be ready to explain how to design data ingestion pipelines and sync document updates to the search index.

---

## 14. Cheat Sheet

- **RAG Pipeline**: Document Ingestion $\to$ Chunking $\to$ Embedding $\to$ Indexing $\to$ Retrieval $\to$ Reranking $\to$ LLM Generation.
- **Chunk Size Recommendation**: 500-1000 characters with 10-25% overlap.
- **Evaluation Metrics**: Faithfulness (hallucinations), Answer Relevance (query match), Context Recall (retrieval quality).
- **Reranker Role**: A Cross-Encoder model that evaluates query-chunk pairs, optimizing relevance.

---

## 15. One-Day Revision Guide

- [ ] Write a script to build a basic RAG pipeline in Python.
- [ ] Explain how chunk overlap prevents context loss at boundaries.
- [ ] Describe the difference between Bi-Encoder retrieval and Cross-Encoder reranking.
- [ ] List two methods for mitigating hallucinations in RAG.
- [ ] Explain how Reciprocal Rank Fusion (RRF) merges search results.
- [ ] Compare RAG and Fine-Tuning in terms of update cost and use case.
