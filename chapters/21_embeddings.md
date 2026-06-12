# 21. Embeddings (Representation Learning)

## 1. Introduction

### What it is
Embeddings are dense, low-dimensional continuous vector representations of discrete entities—words, sentences, source code, images, users, or items. They project high-dimensional symbolic tokens or raw pixel grids into a continuous vector space (typically ranging from 128 to 1536 dimensions) where semantic relationships are captured as geometric proximity. In this embedding space, entities with similar semantic meanings, functions, or contextual properties are mapped to vectors that are geometrically close to one another.

### Why it exists
Computers cannot natively understand the meaning of symbols, categories, or unstructured documents. Traditionally, machine learning relied on symbolic representation methods like One-Hot Encoding or Bag-of-Words (BoW). These approaches present three fatal issues at scale:
1. **High Dimensionality**: A vocabulary of 100,000 words requires 100,000-dimensional vectors.
2. **Sparsity**: Each vector contains only a single `1` and 99,999 `0`s, making training highly inefficient.
3. **Semantic Orthogonality**: The dot product of any two distinct one-hot vectors is exactly `0`. Consequently, "cat" and "kitten" are represented as mathematically orthogonal (unrelated) concepts.

Embeddings solve this by learning mapping functions that compress sparse inputs into a dense, continuous vector space where distance represents conceptual similarity.

### Problems it solves
- **The Semantic Gap**: Bridges symbolic tokens (like words or category IDs) and geometric distance, allowing models to detect similarity.
- **Dimensionality Bottlenecks**: Compresses sparse representations (which scale linearly with vocabulary size $V$) into dense vectors of a fixed, manageable size $D$.
- **Transfer Learning**: Pretrained embeddings (like GloVe or Sentence-BERT) capture general language structures, allowing downstream models to perform well even with minimal training data.
- **Cold-Start Recommendations**: Maps new items or users into a shared vector space based on content descriptions or metadata, bypassing the need for initial interaction history.

### Industry Use Cases
- **Semantic Search**: Powering search engines by matching the semantic intent of queries (e.g., "how to fix a flat tire") with document chunks instead of relying on exact keyword matching.
- **Recommendation Systems**: Embedding users and items into a shared space (e.g., in YouTube or Spotify) to recommend items whose vectors are closest to a user's historical interaction vector.
- **Retrieval-Augmented Generation (RAG)**: Chunking enterprise documentation, embedding those chunks, and storing them in vector databases to retrieve relevant context for Large Language Models (LLMs).
- **Zero-Shot Classification**: Using joint image-text embedding models (like CLIP) to classify images based on text labels without training specific downstream classification heads.
- **Anomaly Detection**: Finding patterns or transactions whose embeddings lie far from the clusters of standard user behaviors.

### Analogy
If discrete words are filing cabinet labels, embeddings are **GPS coordinates**. Filing cabinet labels tell you which folder to open, but they don't tell you how close "Folder A" is to "Folder B". Embeddings assign exact coordinate coordinates to every concept. If you map "King", "Queen", "Man", and "Woman", you will find that the vector direction from "Man" to "King" is almost identical to the direction from "Woman" to "Queen", turning language processing into geometry.

---

## 2. Core Concepts

### Beginner Concepts

#### Dense vs. Sparse Vectors
- **Sparse Vectors** (e.g. One-Hot Encoding, TF-IDF): Sized according to the vocabulary size. Most values are zero. Suffer from the curse of dimensionality and cannot represent similarity.
- **Dense Vectors** (Embeddings): Fixed-length vectors where every position contains a floating-point value. They pack semantic information into a low-dimensional space.

```text
Sparse Word "Cat" (Vocab Size = 5):   [ 1.0,  0.0,  0.0,  0.0,  0.0 ]
Dense Word "Cat" (Dimensions = 4):   [ 0.25, -0.74, 0.81, 0.12 ]
```

#### Vector Similarity Metrics
To calculate how close two vectors $A$ and $B$ are in the embedding space, three main metrics are used:

- **Cosine Similarity**: Measures the cosine of the angle between two vectors, ignoring their magnitudes. Ranges from $-1$ to $1$:
  $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
- **Dot Product (Inner Product)**: Measures both angle and magnitude. If vectors are normalized to unit length ($\|A\| = 1$), the dot product is equivalent to cosine similarity:
  $$\text{Dot Product}(A, B) = A \cdot B = \sum_{i=1}^{n} A_i B_i$$
- **Euclidean Distance ($L_2$ Distance)**: Measures the straight-line distance between two points in Euclidean space. Highly sensitive to vector magnitudes:
  $$\text{Euclidean Distance}(A, B) = \|A - B\|_2 = \sqrt{\sum_{i=1}^{n} (A_i - B_i)^2}$$

### Intermediate Concepts

#### Word2Vec Architecture: CBOW vs. Skip-Gram
Word2Vec learns static word embeddings by training a single-layer neural network on one of two objective tasks:
- **Continuous Bag-of-Words (CBOW)**: Predicts the target word based on its context words. Faster to train and performs well on frequent words.
- **Skip-Gram**: Predicts context words given a target word. Handles rare words better because it generates more training pairs per word.

```text
[ CBOW Objective ]                      [ Skip-Gram Objective ]
Context: ["The", "cat", "on", "mat"]    Target Word: "sat"
               │                                      │
               ▼                                      ▼
     Predict Target: "sat"                  Predict Context Words:
                                            ["The", "cat", "on", "mat"]
```

#### Sentence-BERT (SBERT) and Siamese Networks
Standard BERT models are cross-encoders: they require passing both sentences together through the attention layers to compute similarity, which is too slow for large-scale searches. 
SBERT uses a **Siamese Network** layout. It passes two sentences through identical, weight-sharing BERT encoders separately, generates sentence-level embeddings using pooling, and optimizes their distance. Once trained, sentence vectors are indexed independently, enabling sub-millisecond retrieval.

```text
Sentence A ---> [ BERT Encoder ] ---> [ Mean Pooling ] ---> Vector u ──┐
                                                                       ├──> Cosine Sim / Contrastive Loss
Sentence B ---> [ BERT Encoder ] ---> [ Mean Pooling ] ---> Vector v ──┘
                     ^
             (Shared Weights)
```

#### Pooling Strategies
Since transformers generate token-level embeddings, we must pool them to create a single sentence-level vector:
- **Mean Pooling**: Averages all token embeddings, ignoring padding tokens. This is the most common and robust approach.
- **CLS Token Pooling**: Uses the embedding of the special `[CLS]` token. While common in classification, it can be biased toward the training classification task and perform poorly for semantic similarity.
- **Max Pooling**: Takes the maximum activation value across each dimension of the token embeddings.

### Advanced Concepts

#### Contrastive Learning and InfoNCE Loss
Contrastive learning trains encoders to map positive pairs (e.g. a query and its matching document) close together in the vector space, while pushing negative pairs (unrelated documents) far apart.
The standard objective function is the **InfoNCE (Information Noise-Contrastive Estimation) Loss**:
$$\mathcal{L}_{\text{InfoNCE}} = -\log \frac{\exp(\text{sim}(a, p) / \tau)}{\exp(\text{sim}(a, p) / \tau) + \sum_{i=1}^{K} \exp(\text{sim}(a, n_i) / \tau)}$$
- $a$: Anchor vector (e.g., user query).
- $p$: Positive vector (e.g., matching document).
- $n_i$: Negative vectors (unrelated documents).
- $\tau$: Temperature parameter, which scales logits to control the sharpness of the probability distribution.

#### Matryoshka Representation Learning (MRL)
MRL trains models to store the most critical semantic information in the early dimensions of the vector. For example, a 768-dimensional model trained with MRL can be truncated to 256, 128, or 64 dimensions. This allows matching the retrieval cost (storage and latency) to the application requirements without retraining the model.

```text
Full Vector (768d):    [ x1, x2, x3, ..., x64, ..., x256, ..., x768 ]
                         └─ High Info ──┘
                         └───── Medium Info ────────┘
                         └───────────── Full Detail ────────────────┘
```

#### Vector Quantization (PQ, SQ, Binary)
Storing millions of 1536-dimensional float32 vectors consumes significant RAM. Quantization reduces memory usage by compressing float values:
- **Scalar Quantization (SQ)**: Downsamples float32 values (4 bytes) to int8 values (1 byte) by mapping ranges linearly. Saves 75% memory.
- **Product Quantization (PQ)**: Splits the vector space into $M$ smaller sub-vectors, runs K-means clustering on each sub-space, and stores only the centroid index (usually 1 byte).
- **Binary Quantization (BQ)**: Converts values to 1 if positive, and 0 if negative, compressing the vector into a bit array. This saves up to 97% memory and speeds up similarity checks by using XOR operations on the hardware level.

---

## 3. Internal Working

### Step-by-Step Code Execution Flows

#### 1. Token-to-Vector Lookup Mechanics
When a neural network processes token IDs, it maps them to vectors using an embedding layer, which is internally represented as a matrix of size $V \times D$ (where $V$ is vocabulary size and $D$ is vector dimension).

```text
Input IDs: [3, 1] 

Embedding Weight Matrix (4 x 3):
Index  [  dim0,   dim1,   dim2  ]
  0    [  0.15,  -0.42,   0.88  ]
  1    [  0.92,   0.05,  -0.21  ]  <-- Row 1 Lookup
  2    [ -0.01,   0.72,   0.45  ]
  3    [  0.64,  -0.12,  -0.74  ]  <-- Row 3 Lookup

Resulting Tensors:
[
  [ 0.64, -0.12, -0.74 ],  # Word ID 3
  [ 0.92,  0.05, -0.21 ]   # Word ID 1
]
```

#### 2. Normalizing Vectors and Cosine Equivalence
Normalizing vectors to unit length ($\|A\| = 1$) makes calculating cosine similarity highly efficient.
1. Compute the $L_2$ norm of vector $A$:
   $$\|A\|_2 = \sqrt{a_1^2 + a_2^2 + \dots + a_d^2}$$
2. Divide each dimension by the norm to generate the normalized vector $\hat{A} = A / \|A\|_2$.
3. Once normalized, the Euclidean distance and cosine similarity are directly related:
   $$\|\hat{A} - \hat{B}\|_2^2 = \|\hat{A}\|_2^2 + \|\hat{B}\|_2^2 - 2(\hat{A} \cdot \hat{B}) = 2 - 2 \cdot \text{Cosine Similarity}(A, B)$$
   This mathematical equivalence allows search engines to use fast dot product hardware operations to perform exact cosine similarity rankings.

---

## 4. Important Terminology

- **Dense Vector**: A continuous, fixed-length array of floating-point numbers where every dimension contains info.
- **Siamese Network**: An architecture containing two or more identical subnetworks with shared weights, used to compare inputs.
- **Cosine Similarity**: A metric measuring the angle between two vectors, ranging from -1 to 1.
- **InfoNCE Loss**: A softmax-based contrastive loss function used to optimize positive pairs relative to negative pairs.
- **Quantization**: Compressing high-precision floating-point numbers into low-bit representations to optimize storage and speed.
- **Mean Pooling**: Averaging token-level embedding outputs to build a single sentence-level representation.
- **Recall@K**: The percentage of positive matches retrieved within the top $K$ search results.
- **Matryoshka Embeddings**: Nested embeddings trained to retain semantic details even when truncated to fewer dimensions.

---

## 5. Beginner Examples

### Example 1: Calculating Cosine Similarity from Scratch in Python
This example demonstrates how to calculate cosine similarity manually using standard Python libraries.

```python
import math

def dot_product(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))

def magnitude(v):
    return math.sqrt(sum(a * a for a in v))

def cosine_similarity(v1, v2):
    mag_1 = magnitude(v1)
    mag_2 = magnitude(v2)
    if not mag_1 or not mag_2:
        return 0.0  # Handle zero vectors
    return dot_product(v1, v2) / (mag_1 * mag_2)

# Semantic Vectors
king = [0.4, 0.8, 0.1]
man = [0.35, 0.75, 0.05]
apple = [0.1, -0.2, 0.9]

print("Sim(King, Man):", round(cosine_similarity(king, man), 4))     # Expected: High (~0.99)
print("Sim(King, Apple):", round(cosine_similarity(king, apple), 4)) # Expected: Low (~0.04)
```

---

### Example 2: Implementing static Word2Vec in Gensim
This example trains a Word2Vec model on local text inputs to discover semantic similarities.

```python
from gensim.models import Word2Vec

# 1. Prepare tokenized training text corpus
corpus = [
    ["the", "data", "scientist", "trains", "the", "model"],
    ["the", "machine", "learning", "model", "predicts", "output"],
    ["deep", "learning", "uses", "neural", "networks", "for", "ai"],
    ["the", "software", "engineer", "writes", "clean", "code", "in", "python"]
]

# 2. Train Skip-Gram Word2Vec model
model = Word2Vec(
    sentences=corpus, 
    vector_size=50,   # Latent dimensions
    window=3,         # Context token window
    min_count=1,      # Process all words
    sg=1,             # Use Skip-Gram (set to 0 for CBOW)
    workers=1
)

# 3. Query similarities
print("Vector for 'model':", model.wv["model"][:5]) # Show first 5 dimensions
print("Similar words to 'learning':", model.wv.most_similar("learning", topn=2))
```

---

### Example 3: Initializing custom PyTorch Embedding Tables
This example demonstrates how embedding layers map token IDs to trainable dense vectors.

```python
import torch
import torch.nn as nn

# Define dimensions
vocab_size = 10
embedding_dim = 4

# Initialize layer with random weights
embedding_layer = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dim)
print("Initial Weights:\n", embedding_layer.weight.data)

# Lookup token IDs
input_ids = torch.tensor([2, 5, 2], dtype=torch.long)
output_vectors = embedding_layer(input_ids)

print("\nResolved Dense Vectors:\n", output_vectors)
# Note: Token ID 2 maps to identical rows at index 0 and 2
```

---

## 6. Intermediate Examples

### Example 1: Extracting Sentence Embeddings from Raw Transformer Outputs
This example demonstrates tokenizing text, running a transformer model, and implementing mean pooling on the output tensors.

```python
import torch
from transformers import AutoTokenizer, AutoModel

# 1. Initialize tokenizer and model (E5-small)
model_name = "intfloat/e5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

sentences = ["query: how to build RAG", "query: python programming"]

# 2. Tokenize text inputs
encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')

# 3. Run model forward pass
with torch.no_grad():
    model_output = model(**encoded_input)

# 4. Implement Mean Pooling to extract sentence embeddings
def mean_pooling(model_output, attention_mask):
    # Retrieve last hidden state tensor (batch_size, sequence_length, hidden_dimension)
    token_embeddings = model_output[0] 
    
    # Expand attention mask to match token dimensions, ignoring padded tokens
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    
    # Sum embeddings and counts across tokens
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    
    return sum_embeddings / sum_mask

sentence_embeddings = mean_pooling(model_output, encoded_input['attention_mask'])

# 5. Normalize embeddings to unit length (L2 Normalization)
normalized_embeddings = torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1)

print("Generated Embeddings Shape:", normalized_embeddings.shape) # Expected: (2, 384)
```

---

### Example 2: Training a Contrastive Model using InfoNCE Loss
This example demonstrates training a model to map positive pairs close together while pushing negative pairs apart.

```python
import torch
import torch.nn as nn
import torch.nn.functional as F

class InfoNCELoss(nn.Module):
    def __init__(self, temperature=0.07):
        super(InfoNCELoss, self).__init__()
        self.temperature = temperature

    def forward(self, anchor, positive, negatives):
        # 1. Calculate cosine similarity for the positive pair
        pos_sim = F.cosine_similarity(anchor, positive, dim=-1) / self.temperature # Shape: (Batch_size)
        
        # 2. Calculate cosine similarity for negative pairs
        # anchor: (B, D) -> (B, 1, D)
        # negatives: (B, K, D)
        # We compute batched matrix multiplication (bmm) to get (B, K)
        anchor_expanded = anchor.unsqueeze(1)
        neg_sim = torch.bmm(negatives, anchor_expanded.transpose(1, 2)).squeeze(-1) / self.temperature
        
        # 3. Concatenate positive and negative similarities
        # Target index is 0 (the positive pair is at index 0 in the logits array)
        logits = torch.cat([pos_sim.unsqueeze(-1), neg_sim], dim=-1) # Shape: (B, 1 + K)
        labels = torch.zeros(anchor.size(0), dtype=torch.long, device=anchor.device)
        
        return F.cross_entropy(logits, labels)

# Run test batch
batch_size, dims, num_negatives = 2, 8, 3
loss_fn = InfoNCELoss(temperature=0.1)

a = torch.randn(batch_size, dims)
p = a + torch.randn(batch_size, dims) * 0.1 # Similar vector
n = torch.randn(batch_size, num_negatives, dims) # Random negative vectors

loss_val = loss_fn(a, p, n)
print("InfoNCE Loss value:", loss_val.item())
```

---

### Example 3: Approximate Nearest Neighbor (ANN) Search with FAISS
This example demonstrates indexing vectors and running sublinear nearest-neighbor searches.

```python
import numpy as np
import faiss

# 1. Generate random database and query vectors
d = 128                       # Vector dimensions
num_elements = 10000          # Corpus size
xb = np.random.random((num_elements, d)).astype('float32') # Database
xq = np.random.random((1, d)).astype('float32')            # Query

# 2. Build index (Flat L2 index for exact search)
index = faiss.IndexFlatL2(d)
print("Index initialized:", index.is_trained) # Flat indexes do not require training

# 3. Add vectors to index
index.add(xb)
print("Total Indexed Vectors:", index.ntotal)

# 4. Search for the top 3 nearest vectors
k = 3
distances, indices = index.search(xq, k)

print("\nClosest Match Indices:", indices)
print("L2 Distances to Query:", distances)
```

---

## 7. Advanced Concepts

### Deep System Analysis & Mathematical Proofs

#### HNSW Graph Architecture
Hierarchical Navigable Small World (HNSW) is a graph-based Approximate Nearest Neighbor (ANN) search algorithm. It builds a multi-layer graph structure, similar to skip-lists, to achieve logarithmic $\mathcal{O}(\log N)$ search times.

```text
[ Layer 2 (Sparse) ]       Node A ───────────────────────────> Node E
                             │                                   │
[ Layer 1 (Medium) ]       Node A ──────────> Node C ──────────> Node E
                             │                 │                 │
[ Layer 0 (Dense) ]        Node A ──> Node B ──> Node C ──> Node D ──> Node E
```

- **Layer 0 (Bottom)**: Contains all indexed vectors, linked as a dense graph.
- **Upper Layers (Sparse)**: Contain a fraction of the vectors, forming a sparse graph.
- **Search Logic**: The search starts at the top layer. It traverses the sparse graph using greedy search until it finds a local minimum. It then drops down to the next layer and resumes the search from that node, repeating this process until it reaches Layer 0. This multi-layer traversal prevents the search from getting stuck in local minima, ensuring fast and highly accurate queries.

#### Hard Negative Mining
Standard training batches are filled with "easy negatives" (randomly selected unrelated documents) that are easy for the model to distinguish.
To train high-quality embedding models, we must feed them **hard negatives**—documents that are semantically similar to the anchor but do not answer the query (e.g. a document discussing python programming syntax when the query asks how to run a python script).
- **In-Batch Negatives**: Using positive documents from other samples in the same batch as negatives.
- **Cross-Encoder Filtering**: Using a heavy Cross-Encoder model to score documents, selecting documents that have high similarity scores but are not positive matches.

#### Quantization Trade-offs
Reducing precision from float32 to int8 saves storage but can degrade search accuracy:

| Format | Precision | Size per Dimension | Memory Footprint (10M vectors, 768d) | Search Speed | Accuracy (Recall@10) |
|---|---|---|---|---|---|
| **Float32** | Full | 4 bytes | 30.7 GB | Baseline | ~98% |
| **Int8 (SQ8)** | Medium | 1 byte | 7.68 GB | ~2x faster | ~95% |
| **Binary (BQ)** | Binary | 1 bit | 0.96 GB | ~10x faster (via hardware XOR) | ~70-80% (Requires rescoring) |

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers want to see if you can evaluate system trade-offs. They don't want you to just memorize APIs. They will check if you understand distance metrics, the difference between token and sentence pooling, indexing trade-offs (recall vs latency), and how to optimize vector databases for production.

### Red Flags
- **Unnormalized Cosine Similarity**: Computing cosine similarity by running a simple dot product on unnormalized vectors. This ignores vector length differences, leading to incorrect rankings.
- **Ignoring Padding in Mean Pooling**: Implementing mean pooling by dividing the sum of token embeddings by the sequence length, without filtering out padding tokens. This skews results toward the padding vectors.
- **Assuming Re-indexing is Free**: Proposing to frequently re-index a billion-scale vector database when new items are added, ignoring the high CPU and memory costs.

### Green Flags
- **Proactive Normalization**: Normalizing embeddings at index time, allowing search engines to use fast dot product operations at query time.
- **Matryoshka Truncation**: Recommending Matryoshka embeddings to dynamically match storage limits and search speeds to user tiers.
- **Quorum Rescoring**: Proposing a two-stage retrieval pipeline: retrieve a larger set of candidates using fast, compressed vectors (quantization), then rerank the top candidates using full-precision vectors.

### Answers Matrix

| Level | Question: "How do you handle updating an embedding index for a real-time recommendations system?" |
|---|---|
| **Rejected** | "Every time a user updates their profile, rebuild the entire vector index to make sure everything is up-to-date." |
| **Shortlisted** | "Add new user vectors to a buffer index and merge them into the main index periodically using background cron jobs." |
| **Selected** | "To support real-time updates, I would implement a hybrid index layout. I would use a fast, in-memory flat index (buffer) to store updates instantly. At query time, we search both the main HNSW index and the buffer index, merging the results. In the background, a worker process monitors the buffer size. Once it crosses a threshold, it commits the changes into the main HNSW index in a separate memory space and swaps the index reference atomically to avoid blocking queries." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is an embedding?
- **Detailed Answer**: An embedding is a dense, low-dimensional continuous vector representation of discrete data. It projects sparse, high-dimensional symbols (like words, items, or user IDs) into a continuous vector space where semantic similarity is represented as geometric proximity. Unlike sparse representations (like TF-IDF or One-Hot Encoding), embeddings capture semantic relationships and have a fixed dimension size that does not grow with the vocabulary size.
- **Follow-up Questions**: Why do we prefer dense vectors over sparse ones? (Answer: Dense vectors capture semantics, prevent sparsity issues, and have a fixed size that optimizes downstream modeling).
- **Interviewer's Expectations**: Define embeddings as dense, continuous, low-dimensional vectors and explain how they capture semantic relationships.

#### 2. What is the difference between sparse and dense embeddings?
- **Detailed Answer**:
  - **Sparse Embeddings** (e.g. BM25, TF-IDF): Have a size equal to the vocabulary. Most values are zero. They match exact keywords but cannot capture semantic meaning (e.g. "feline" and "cat" are treated as unrelated).
  - **Dense Embeddings** (e.g. Sentence-BERT, OpenAI text-embedding-3): Fixed-length vectors containing floating-point values. They capture semantic meaning and intent but can miss exact keyword matches (e.g. serial numbers or specific error codes).
- **Follow-up Questions**: Can we combine them? (Answer: Yes. Hybrid search combines BM25 keyword matching with dense vector semantic search, using reciprocal rank fusion (RRF) to merge the results).
- **Interviewer's Expectations**: Compare keyword matching vs semantic matching, and explain vocabulary size scaling.

#### 3. What is the difference between word embeddings and sentence embeddings?
- **Detailed Answer**:
  - **Word Embeddings** (e.g. Word2Vec, GloVe): Represent single words. They cannot capture word order, grammar, or context (e.g., "bank" has the same vector in "river bank" and "investment bank").
  - **Sentence Embeddings** (e.g. SBERT, E5): Represent full sentences or paragraphs. They capture the overall semantic meaning of a text block by processing the relationships between words.
- **Follow-up Questions**: How do we generate sentence embeddings from word embeddings? (Answer: Historically via bag-of-words averaging. Modern models use Transformer encoders combined with mean pooling).
- **Interviewer's Expectations**: Distinguish token-level representation from sequence-level context representation.

#### 4. What is the difference between static and contextual embeddings?
- **Detailed Answer**:
  - **Static Embeddings** (e.g. Word2Vec, GloVe): Use a static lookup table where each word maps to a single vector, regardless of its context in a sentence.
  - **Contextual Embeddings** (e.g. BERT, GPT-based embeddings): Generate vectors dynamically based on the surrounding tokens in a sentence using self-attention layers. This allows the same word to have different vectors depending on its meaning in context.
- **Follow-up Questions**: What is the memory cost difference? (Answer: Static embeddings require a simple lookup table, which has a very small memory footprint. Contextual embeddings require running a forward pass through a neural network, which is more CPU/GPU intensive).
- **Interviewer's Expectations**: Explain how self-attention layers enable context-aware representations.

#### 5. Explain the Curse of Dimensionality as it applies to embeddings.
- **Detailed Answer**: As the vector dimension $D$ increases, the volume of the space grows exponentially. Consequently, data points become sparse, and the distance between any two vectors converges to a constant value:
  $$\lim_{D \to \infty} \frac{\text{Dist}_{\text{max}} - \text{Dist}_{\text{min}}}{\text{Dist}_{\text{min}}} = 0$$
  This makes distance-based metrics (like Euclidean distance) less effective at measuring similarity in very high-dimensional spaces. In practice, keeping dimensions under 1536 and using cosine similarity helps mitigate this issue.
- **Follow-up Questions**: How does this impact indexing algorithms? (Answer: High-dimensional spaces increase the likelihood of getting stuck in local minima during graph traversals, reducing search recall).
- **Interviewer's Expectations**: Explain how high dimensions affect distance metrics and search accuracy.

#### 6. What is contrastive learning in the context of embedding models?
- **Detailed Answer**: Contrastive learning is a self-supervised training paradigm where a model learns to map positive pairs close together in the vector space, while pushing negative pairs far apart. For text models, positive pairs are often generated using data augmentation (e.g. applying dropout to the same sentence twice, as in SimCSE) or using labeled datasets (e.g. query-document pairs).
- **Follow-up Questions**: Name a common loss function used in contrastive learning. (Answer: InfoNCE loss, which is mathematically equivalent to multi-class cross-entropy).
- **Interviewer's Expectations**: Describe the positive-negative pairing mechanism and the goal of contrastive optimization.

#### 7. What is the difference between hard negatives and easy negatives in contrastive learning?
- **Detailed Answer**:
  - **Easy Negatives**: Randomly selected unrelated documents from the corpus. They are easy for the model to distinguish and quickly reduce loss to near zero, but provide little training value.
  - **Hard Negatives**: Documents that are semantically similar to the anchor but do not match the query (e.g. a document discussing python programming syntax when the query asks how to run a python script). They force the model to learn fine-grained distinctions, improving search precision.
- **Follow-up Questions**: How do we find hard negatives? (Answer: By using a heavy Cross-Encoder model to score documents, selecting documents that have high similarity scores but are not positive matches).
- **Interviewer's Expectations**: Compare random negatives with semantically similar negatives, and explain how they impact model accuracy.

#### 8. What is the role of the temperature parameter ($\tau$) in contrastive loss functions?
- **Detailed Answer**: The temperature parameter ($\tau$) scales the logits before the softmax operation in InfoNCE loss:
  $$\text{Scaled Logit} = \frac{\text{sim}(A, B)}{\tau}$$
  - A **low temperature** (e.g., 0.05) increases the difference between similarities. This forces the model to focus on distinguishing the query from the hardest negatives, but makes training sensitive to noisy data or bad labels.
  - A **high temperature** (e.g., 1.0) flattens the logit distribution. The model treats all negatives more equally, which can slow down convergence and limit its ability to learn fine-grained distinctions.
- **Follow-up Questions**: What happens if the temperature is set to near zero? (Answer: The gradients can explode, causing training instability).
- **Interviewer's Expectations**: Explain how scaling logits affects the sharpness of the probability distribution.

#### 9. What is Vector Quantization?
- **Detailed Answer**: Vector Quantization is a compression technique that maps high-precision floating-point vectors to low-precision representation formats (like integers or bits).
  - **Scalar Quantization**: Downsamples float32 values (4 bytes) to int8 values (1 byte) by mapping ranges linearly. Saves 75% memory.
  - **Product Quantization**: Splits a vector into smaller sub-vectors, runs K-means clustering on each sub-space, and stores only the centroid index (usually 1 byte).
- **Follow-up Questions**: Does quantization impact search accuracy? (Answer: Yes. It introduces compression noise, which can reduce search recall. To mitigate this, search engines use a two-stage pipeline: retrieve candidates using quantized vectors, then rerank the top candidates using full-precision vectors).
- **Interviewer's Expectations**: Explain the mapping of float values to low-precision formats and the trade-offs between memory and accuracy.

#### 10. Compare the main Approximate Nearest Neighbor (ANN) index types: HNSW, IVF, and PQ.
- **Detailed Answer**:
  - **HNSW (Hierarchical Navigable Small World)**: Graph-based index. Offers high search recall and low query latency, but has a large memory footprint and is slow to build.
  - **IVF (Inverted File Index)**: Cluster-based index. Groups vectors into clusters using K-means. During queries, it searches only the closest clusters, reducing search latency. Has a small memory footprint but lower recall than HNSW.
  - **PQ (Product Quantization)**: Compression-based index. Compresses vectors into codebooks, reducing memory usage by up to 90%, but has the lowest search recall.
- **Follow-up Questions**: Can we combine IVF and PQ? (Answer: Yes, IVF-PQ is a common index configuration that uses IVF for fast clustering and PQ to compress the vectors within each cluster).
- **Interviewer's Expectations**: Compare graph, clustering, and compression approaches in terms of search speed, memory, and recall.

#### 11. What is the difference between brute-force exact search and Approximate Nearest Neighbor (ANN) search?
- **Detailed Answer**:
  - **Brute-Force Search (Flat Index)**: Compares the query vector against every single vector in the database. It guarantees 100% search accuracy (recall) but has a linear time complexity of $\mathcal{O}(N)$, making it too slow for large datasets.
  - **ANN Search**: Uses pre-computed data structures (like graphs or clusters) to search only a fraction of the vector space. It runs in sublinear time ($\mathcal{O}(\log N)$), enabling fast queries on large datasets, but does not guarantee finding the absolute nearest neighbors.
- **Follow-up Questions**: Under what scale is brute-force search acceptable? (Answer: Usually under 100,000 vectors, where flat queries run in under 10ms).
- **Interviewer's Expectations**: Compare time complexities and accuracy guarantees.

#### 12. How does the embedding dimension size affect search recall and query latency?
- **Detailed Answer**:
  - **Higher Dimensions** (e.g. 1536): Can capture more complex relationships and fine-grained details, leading to higher search recall. However, they increase storage requirements, CPU/GPU latency, and memory usage.
  - **Lower Dimensions** (e.g. 256): Reduce storage requirements and speed up similarity calculations, but can compress semantic information too much, reducing search recall.
- **Follow-up Questions**: How do Matryoshka embeddings help optimize this trade-off? (Answer: They allow using a single model to output high-dimensional vectors that can be truncated to lower dimensions on-the-fly, matching the latency requirements of different user tiers).
- **Interviewer's Expectations**: Describe the trade-offs between representation capacity and computational performance.

#### 13. What is the difference between dot product and cosine similarity?
- **Detailed Answer**:
  - **Cosine Similarity** measures only the angle between two vectors, ignoring their magnitudes. It is bounded between $-1$ and $1$.
  - **Dot Product** measures both the angle and the magnitudes of the vectors. It is unbounded.
  - **Equivalence**: If vectors are L2-normalized to unit length ($\|A\| = 1$), their dot product is mathematically equivalent to their cosine similarity.
- **Follow-up Questions**: Why is it best practice to normalize vectors before indexing them? (Answer: It allows the search engine to use fast dot product operations at query time, bypassing the expensive square root divisions required for cosine similarity calculations).
- **Interviewer's Expectations**: Define the mathematical relationship and explain the performance optimization of normalized dot products.

#### 14. What is Matryoshka Representation Learning (MRL)?
- **Detailed Answer**: MRL is a training technique that constrains a model to store the most critical semantic information in the early dimensions of the vector. For example, a 768-dimensional model trained with MRL can be truncated to 256, 128, or 64 dimensions. This allows matching the retrieval cost (storage and latency) to the application requirements without retraining the model.
- **Follow-up Questions**: How is the loss calculated during MRL training? (Answer: The model calculates contrastive loss at multiple truncation boundaries simultaneously, summing the losses to optimize all sub-vector configurations).
- **Interviewer's Expectations**: Explain nested dimension prioritization and its benefits for adaptive retrieval.

#### 15. What is the difference between exact and approximate nearest neighbor search?
- **Detailed Answer**:
  - **Exact Search**: Compares the query vector against every vector in the database, returning the true nearest neighbors. It is accurate but computationally expensive, scaling linearly with dataset size ($\mathcal{O}(N)$).
  - **Approximate Search (ANN)**: Uses pre-computed data structures (like graphs or clusters) to search only a fraction of the vector space. It runs in sublinear time ($\mathcal{O}(\log N)$), enabling fast queries on large datasets, but can miss the true nearest neighbors if they fall outside the searched space.
- **Follow-up Questions**: How do you evaluate the quality of an ANN index? (Answer: By measuring recall against an exact brute-force search baseline on a test query set).
- **Interviewer's Expectations**: Contrast search accuracy guarantees and computational complexities.

---

### Scenario-Based Questions

#### 16. Your semantic search system fails to find relevant documents when users use rare words or specific slang. How do you resolve this?
- **Detailed Answer**: This is a common failure point of dense embedding models, which can struggle to represent rare keywords or specific terms that were not present in their training data.
  - **Solutions**:
    1. **Hybrid Search**: Combine dense vector search with **BM25** (keyword matching). Use Reciprocal Rank Fusion (RRF) to merge the results:
       $$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$
       This ensures that exact matches for rare slang or serial numbers are still retrieved.
    2. **Domain-Specific Fine-Tuning**: Fine-tune the embedding model on your local document corpus using contrastive learning to teach it local terms and slang.
- **Follow-up Questions**: What does the parameter $k$ do in the RRF formula? (Answer: It is a smoothing constant, typically set to 60, that prevents high-ranking matches from dominating the merged score).
- **Interviewer's Expectations**: Propose hybrid search (BM25 + Dense) and model fine-tuning.

#### 17. You are designing a search system for 10 million items. The query latency must be under 50ms. Which index type and quantization strategy do you select?
- **Detailed Answer**:
  - **Scale and Memory estimation**: 10 million vectors with 768 dimensions using float32 coordinates require:
    $$10\text{M} \times 768 \times 4\text{ bytes} \approx 30.7\text{ GB of RAM}$$
    To keep query latency under 50ms at scale, we must fit the index in memory.
  - **Selected Configuration**:
    1. **IVF-PQ (Inverted File with Product Quantization) Index**: IVF clusters the vectors into $K$ centroids (e.g. $K=4096$), limiting the search to the closest clusters. PQ compresses each vector dimension to 1 byte, reducing the memory footprint to ~7.68 GB, which easily fits in a standard server's RAM.
    2. **Two-Stage Reranking**: If search recall drops too much due to PQ compression, we retrieve the top 100 candidates using IVF-PQ, then rerank them using full-precision vectors stored on disk.
- **Follow-up Questions**: Why not use HNSW here? (Answer: HNSW offers high recall but has a very large memory footprint, requiring up to 1.5x to 2x more memory than raw vectors, which would exceed our RAM budget).
- **Interviewer's Expectations**: Perform memory estimations and justify your index and quantization choices.

#### 18. You notice that sentence embeddings generated by mean pooling have different scales depending on the sentence length. How do you resolve this?
- **Detailed Answer**: Mean pooling calculates the average of token embeddings. Long sentences can have lower average magnitudes because they contain more uninformative words (like padding tokens, punctuation, or conjunctions).
  - **Resolution**: Apply **L2 Normalization** to the pooled vectors to project them onto a unit sphere ($\|v\|_2 = 1$). Once normalized, their lengths are identical, and similarity calculations depend only on the angle between the vectors, removing the bias of sentence length.
- **Follow-up Questions**: Does L2 normalization alter the relative semantic layout of the vectors? (Answer: No. It preserves the angular relationships, which are the primary measure of semantic similarity).
- **Interviewer's Expectations**: Identify average magnitude bias in mean pooling and recommend L2 normalization.

#### 19. You need to embed both source code and natural language text into a shared vector space to support code search. How do you implement this?
- **Detailed Answer**: Standard text embedding models perform poorly on code because code contains syntax structures, variables, and indentation patterns that differ from natural language.
  - **Implementation**:
    1. **Select a Bimodal Model**: Use a model pre-trained on both code and text datasets (like CodeBERT, GraphCodeBERT, or StarCoder embeddings).
    2. **Contrastive Training**: Fine-tune the model using positive pairs consisting of a natural language comment and its corresponding code snippet. This forces the model to map the comment vector and the code vector to nearby coordinates in the shared embedding space.
- **Follow-up Questions**: Why is it best to normalize inputs before embedding them? (Answer: To remove formatting inconsistencies like redundant white spaces or variable naming styles).
- **Interviewer's Expectations**: Recommend bimodal models and explain contrastive alignment.

#### 20. How do you choose an embedding model for a multilingual application that must support queries in English, Spanish, and Japanese?
- **Detailed Answer**:
  - **Model Selection**: Select a multilingual model trained on parallel corpora across target languages (like `multilingual-e5-base` or Cohere multilingual embeddings). These models map translations of the same concept (e.g. "dog", "perro", "犬") to nearby coordinates in the shared vector space.
  - **Evaluation**: Benchmark the model on a translation retrieval task using a test query set. Compare its performance using Recall@K and Mean Reciprocal Rank (MRR) metrics across all languages.
- **Follow-up Questions**: What is the risk of using a single-language model translated via an API? (Answer: It introduces translation errors, increases latency, and increases API costs).
- **Interviewer's Expectations**: Recommend multilingual models and explain parallel vector space mapping.

---

### Debugging Questions

#### 21. You notice that the similarity score between two identical text inputs varies slightly between model runs. What is the root cause and how do you fix it?
- **Detailed Answer**:
  - **Root Cause**:
    1. **GPU Non-Determinism**: PyTorch or TensorFlow GPU operations (like atomic additions in attention layers) can run in non-deterministic order, introducing minor floating-point rounding errors.
    2. **Missing Eval Mode**: The model was not set to evaluation mode (`model.eval()`). As a result, active Dropout layers random-mask different tokens on every forward pass, changing the output vectors.
  - **Fixes**:
    - Call `model.eval()` and disable gradient calculations (`torch.no_grad()`).
    - Set random seeds and enable deterministic algorithms:
      ```python
      torch.manual_seed(42)
      torch.use_deterministic_algorithms(True)
      ```
- **Follow-up Questions**: Why does dropout change embeddings? (Answer: Dropout randomly zeroes out features during training to prevent overfitting. If active during inference, it alters the vector coordinates).
- **Interviewer's Expectations**: Identify active dropout or non-deterministic GPU operations and apply `model.eval()`.

#### 22. During training, your contrastive model's embedding outputs collapse, mapping all input tokens to the same vector coordinates. How do you debug this?
- **Detailed Answer**: This is called **Representation Collapse** (or dimensional collapse). It occurs when the model maps all inputs to a single point to minimize loss, failing to learn distinguishing features.
  - **Debugging Steps**:
    1. **Check the Loss function**: If you are using simple contrastive loss without negatives, the model will minimize loss by mapping all outputs to the same vector. Ensure you are using InfoNCE loss with a sufficient number of diverse negatives.
    2. **Verify Temperature ($\tau$)**: If the temperature is set too high, the loss function flattens the logit distribution, reducing the penalty for negatives and allowing collapse. Lower the temperature to between 0.05 and 0.1.
    3. **Learning Rate**: A very high learning rate can cause the model to get stuck in local minima early. Lower the learning rate and add a warm-up phase.
- **Follow-up Questions**: How does normalization help prevent representation collapse? (Answer: It constrains vectors to a unit sphere, preventing the model from minimizing loss by simply scaling vector magnitudes to infinity).
- **Interviewer's Expectations**: Identify missing negatives or incorrect temperature scaling and propose debugging steps.

#### 23. You calculate the cosine similarity between two sentence embeddings and get a value of 1.2. How is this possible and how do you fix it?
- **Detailed Answer**: By definition, cosine similarity is bounded between $-1$ and $1$. A value of $1.2$ indicates a calculation error.
  - **Root Cause**: The calculation assumed the vectors were already L2-normalized, but they were not. Running a simple dot product on unnormalized vectors:
    $$\text{Dot Product}(A, B) = \sum a_i b_i$$
    If the magnitudes of $A$ and $B$ are greater than 1, their dot product can exceed 1.
  - **Fix**: Calculate the norms of the vectors and divide the dot product by their magnitudes, or normalize the vectors before computing the dot product:
    ```python
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    cosine_sim = np.dot(a, b) / (norm_a * norm_b)
    ```
- **Follow-up Questions**: Can cosine similarity be negative for text embeddings? (Answer: In theory, yes, if the vectors point in opposite directions. In practice, text embeddings generated by transformers often group in a narrow cone, resulting in similarity values that are mostly positive (between 0 and 1)).
- **Interviewer's Expectations**: Explain cosine boundary mathematics and apply normalization.

#### 24. Your semantic search engine returns documents that are completely irrelevant to the user's query, despite having high similarity scores. How do you debug this?
- **Detailed Answer**:
  - **Root Cause**:
    1. **Hubness Problem**: In high-dimensional spaces, certain vectors (called "hubs") tend to appear as nearest neighbors to a disproportionately large number of query vectors, regardless of semantic similarity.
    2. **Out-of-Distribution Queries**: The query contains slang or formatting styles that differ from the model's training data, causing it to map the query to random coordinates.
  - **Debugging Steps**:
    - Calculate the average distance of queries to the corpus vectors. If a few documents are returned for almost all queries, apply **Inverted Document Frequency (IDF)** weight scalers to reduce the weight of common tokens, or use **Centering** to shift the vector space.
    - Implement a similarity score threshold: reject matches below a minimum score (e.g. $< 0.7$).
- **Follow-up Questions**: How does reranking with a Cross-Encoder resolve this? (Answer: Cross-Encoders process both query and document together through attention layers, which is slower but much more accurate at filtering out false positives).
- **Interviewer's Expectations**: Explain the hubness problem and propose similarity thresholds or reranking.

#### 25. Your Approximate Nearest Neighbor (ANN) search returns duplicate document IDs. How do you resolve this?
- **Detailed Answer**:
  - **Root Cause**:
    1. **Duplicate Vectors**: The database contains duplicate documents that were indexed multiple times.
    2. **HNSW Graph Loops**: During graph traversal, the search path can cycle through similar nodes if the graph has redundant links or if the search parameters (`efSearch`) are set too low.
  - **Fixes**:
    - Add a deduplication step before indexing: compute MD5 hashes of the document text and prevent indexing duplicate content.
    - Increase `efSearch` in your HNSW index to search a larger candidate pool, and deduplicate results in the application layer using a Set.
- **Follow-up Questions**: What does the `efSearch` parameter do in HNSW? (Answer: It controls the size of the dynamic candidate list evaluated during query traversal. Higher values improve search recall but increase latency).
- **Interviewer's Expectations**: Propose text deduplication at index time and tuning HNSW search parameters.

---

### System Design Questions

#### 26. Design a scalable semantic search system for an enterprise database containing 100 million documents.
- **Detailed Answer**:
  - **System Architecture**:
    1. **Document Ingestion Pipeline**: When a document is added or updated:
       - Split the text into overlapping chunks (e.g. 512 tokens with 10% overlap) to preserve context.
       - Send chunks in batches to an embedding worker queue (using PyTorch on GPU instances).
       - Write document metadata to a relational database (PostgreSQL) and write the chunk vectors to a distributed vector database (e.g. Qdrant or Pinecone).
    2. **Vector Indexing**: Use an **IVF-PQ** index to compress vectors and enable fast sublinear searches, keeping the index size within our memory budget.
    3. **Query Pipeline**:
       - Generate the query embedding using the same model.
       - Search the vector database to retrieve the top 100 candidate chunks.
       - Pass the candidates and query to a **Cross-Encoder reranking model** (like `bge-reranker-large`) to select the top 5 most relevant chunks.
       - Return the final results to the user.
- **Follow-up Questions**: How do you update the index when documents are deleted? (Answer: Perform soft deletes in the vector database using document ID filters, and run index optimization jobs overnight to reclaim storage).
- **Interviewer's Expectations**: Detail the ingestion, indexing, retrieval, and reranking pipelines.

---

#### 27. Design a multi-tenant embedding storage service for a SaaS application where tenants cannot access each other's data.
- **Detailed Answer**:
  - **Security Requirements**: We must enforce strict data isolation between tenants at the index level.
  - **Partitioning Strategies**:
    1. **Namespace Partitioning** (Logical Isolation): Use a shared vector index but filter queries using a metadata field containing the tenant ID (e.g. `filter: {"tenant_id": "tenant_123"}`).
       - *Pros*: Cost-effective and simple to manage.
       - *Cons*: Metadata filtering can reduce search recall if the filter matches a very small subset of the index.
    2. **Index Partitioning** (Physical Isolation): Create a separate vector index for each tenant.
       - *Pros*: Complete security isolation and consistent search performance.
       - *Cons*: High resource overhead and expensive at scale for thousands of small tenants.
  - **Recommendation**: For small tenants, use namespace partitioning with strict application-level query filters. For enterprise tenants with large datasets, spin up dedicated indexes.
- **Follow-up Questions**: How does metadata filtering affect search speed in HNSW? (Answer: If we filter after the graph search (post-filtering), we may get fewer than $K$ results. If we filter during the graph search (pre-filtering), we must evaluate metadata at each node, which can slow down traversal).
- **Interviewer's Expectations**: Compare logical vs physical isolation strategies and analyze the performance impact of metadata filtering.

---

#### 28. Design a multimodal image-text retrieval system.
- **Detailed Answer**:
  - **Architecture**:
    1. **Joint Embedding Model**: Use a model trained on image-text pairs (like CLIP or SigLIP). The model contains two separate encoders—an **Image Encoder** (ViT) and a **Text Encoder** (Transformer)—that project images and text descriptions into a shared embedding space.
    2. **Database Pipeline**:
       - Pass all catalog images through the Image Encoder to generate vectors, and index them in a vector database.
       - Store image metadata (like URLs and category tags) in a relational database.
    3. **Query Pipeline**:
       - When a user searches using a text query (e.g. "red running shoes"), pass the query through the Text Encoder to generate a vector.
       - Search the vector database using the text vector to retrieve the closest image vectors.
       - Return the matching image URLs to the user.
- **Follow-up Questions**: How do you support searching using an image query instead of text? (Answer: Pass the query image through the Image Encoder to generate a vector, and search the same index).
- **Interviewer's Expectations**: Describe the shared embedding space and detail the dual-encoder query flow.

---

## 10. Common Mistakes

- **Comparing Unnormalized Vectors**: Computing cosine similarity by running a simple dot product on unnormalized vectors. This ignores vector length differences, leading to incorrect rankings.
- **Ignoring Padding in Mean Pooling**: Implementing mean pooling by dividing the sum of token embeddings by the sequence length, without filtering out padding tokens. This skews results toward the padding vectors.
- **Mismatched Tokenizers**: Using a different model or tokenizer for query embeddings than the one used to index the document corpus. This generates unrelated vectors, rendering search useless.
- **Over-Optimizing Dimension Sizes**: Choosing a very high dimension size (e.g. 1536) for a simple system with strict latency limits. Use dimension reduction (Matryoshka learning) or quantization instead.

---

## 11. Comparison Section: Embedding Models

| Model | Dimensions | Max Tokens | Best Use Case | Performance (MTEB Rank) | Shipped JS Code Size |
|---|---|---|---|---|---|
| **Word2Vec** | 50-300 | 1 (Static) | Legacy applications and fast word-level lookups. | Very Low | Minimal |
| **MiniLM-L6** | 384 | 512 | CPU-bound applications and fast semantic search. | Medium | ~90MB |
| **E5-Large** | 1024 | 512 | High-accuracy document search and retrieval. | High | ~1.3GB |
| **CLIP (ViT-B/32)**| 512 | 77 | Multimodal image-text search and retrieval. | High (Multimodal) | ~600MB |
| **Text-Embedding-3**| 1536 | 8191 | Large-scale RAG systems using cloud APIs. | Very High | Zero (API call) |

---

## 12. Practical Project Ideas

### Beginner
- **Semantic Book Search**: Build a book search tool. Extract descriptions of 100 books, generate embeddings using a local Sentence-Transformer model (`all-MiniLM-L6-v2`), index them in a FAISS flat index, and build a command-line interface to query books by semantic concept (e.g., "stories about space travel").

### Intermediate
- **Multilingual Search Portal**: Build a search backend that supports queries in English, Spanish, and French. Index a translated dataset using a multilingual embedding model, and evaluate search accuracy across languages using Recall@K metrics.

### Advanced/Resume-worthy
- **Enterprise RAG Search Engine with Reranking**: Develop a production-ready search pipeline:
  - Ingest document PDFs, split them into overlapping chunks, and index them in a vector database (like Qdrant).
  - Implement **hybrid search** (combining BM25 keyword matching with dense vector search) and merge results using Reciprocal Rank Fusion (RRF).
  - Deploy a local **Cross-Encoder reranking model** to filter and rerank the top candidates before returning them.
  - Wrap the system in a Docker container and expose REST API endpoints.

---

## 13. Internship Preparation Notes

- **Recruiters Focus on**: Understanding the difference between sparse (TF-IDF) and dense vectors, and knowing basic similarity metrics (cosine similarity vs dot product).
- **Applied ML Roles**: Require understanding of transformer pooling strategies (mean pooling vs CLS), contrastive learning loss functions (InfoNCE), and index optimization (quantization and ANN search).
- **System Sizing**: Be prepared to estimate the RAM and latency requirements of a vector index for a given dataset size.

---

## 14. Cheat Sheet

- **L2 Normalization Formula**: $\hat{x} = x / \|x\|_2$. Once normalized, the dot product is equivalent to cosine similarity.
- **InfoNCE Loss Goal**: Maximize the similarity of positive pairs relative to negative pairs.
- **Index Selection**:
  - Small scale ($<100$k vectors): Flat index (exact search).
  - Large scale ($>10$M vectors): IVF-PQ or HNSW (approximate search).
- **Matryoshka Truncation**: Safely truncate early dimensions of vectors to reduce storage costs without retraining.

---

## 15. One-Day Revision Guide

- [ ] Write a function to calculate cosine similarity between two lists in Python.
- [ ] Explain why the dot product is equivalent to cosine similarity for normalized vectors.
- [ ] Describe the difference between CBOW and Skip-gram architectures in Word2Vec.
- [ ] Explain how HNSW uses layers to perform sublinear vector searches.
- [ ] Identify a stale closure inside a PyTorch training loop.
- [ ] List two methods for compressing vector databases.
