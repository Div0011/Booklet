# 20. LLM Fundamentals (Large Language Models)

## 1. Introduction
### What it is
Large Language Models (LLMs) are deep neural networks trained on massive text corpora to understand, generate, and reason with natural language. Modern LLMs are built on the Transformer architecture and typically contain billions of parameters.

### Why it exists
Earlier NLP models (RNNs, LSTMs) processed text sequentially, making parallel training impossible and limiting context retention. The Transformer (2017) replaced recurrence with self-attention, enabling parallel token processing, long-range context, and scaling to massive datasets and model sizes.

### Problems it solves
- **Context loss**: Self-attention retains dependencies across entire sequences.
- **Sequential bottleneck**: Parallel training on massive GPU clusters.
- **Task generalization**: One model replaces task-specific models (sentiment, translation, summarization).

### Industry Use Cases
- **Conversational AI**: Customer support, code assistants.
- **Content generation**: Marketing copy, summarization, translation.
- **Enterprise search**: Semantic retrieval from internal docs.
- **Code generation**: Copilots, automated review, test generation.

### Analogy
An LLM is a highly trained paralegal who has read every document in a massive library. It doesn't "know" facts like databases; it predicts plausible continuations based on statistical patterns in training data.

### Introduction to Generative AI
Generative AI refers to a class of artificial intelligence systems designed to create new content—such as text, images, music, audio, or code—based on the statistical patterns they learned from training datasets. Unlike traditional discriminative AI (which classifies or predicts labels from inputs, such as identifying spam emails), generative AI constructs entirely new data instances that are structurally similar to its training data.

### History of Generative AI & The GPT Evolution
1. **Early Probabilistic Models**: Early text generators relied on N-gram models and Markov chains, predicting the next word based purely on the frequency of adjacent word combinations. These models had no semantic understanding and struggled with contexts longer than a few words.
2. **Deep Representation & NLU (Natural Language Understanding)**: The introduction of Recurrent Neural Networks (RNNs) and Long Short-Term Memory (LSTM) networks enabled models to maintain a hidden state (memory) over sequences, laying the groundwork for NLU (parsing sentence structure, sentiment, and intent).
3. **Sequence-to-Sequence (Seq2Seq)**: Developed for machine translation, Seq2Seq mapped variable-length input sequences to variable-length outputs using an encoder-decoder architecture. However, sequential processing remained a major performance bottleneck.
4. **The Transformer Revolution (2017)**: The "Attention is All You Need" paper introduced parallelized self-attention, unlocking the ability to train massive models on web-scale datasets.
5. **The GPT Family Evolution (OpenAI)**:
   - **GPT-1 (2018)**: Demonstrated that unsupervised pre-training on a large corpus followed by supervised fine-tuning on specific tasks could achieve strong generalization.
   - **GPT-2 (2019)**: Expanded parameter size to 1.5 billion. It showed powerful zero-shot learning capabilities—meaning the model could generate highly coherent paragraphs, write poetry, translate languages, and compose stories without task-specific fine-tuning.
   - **GPT-3 (2020)**: Scaled to 175 billion parameters. It unlocked few-shot prompt learning (in-context learning), enabling users to program the model simply by providing a few input-output examples in the text prompt, bypassing the need for weight-updating fine-tuning.
   - **GPT-4 & Multimodal Models (2023+)**: Introduced multimodal capabilities, allowing the network to process and reason across text, code, images, and audio simultaneously.

---

## 2. Core Concepts

### Beginner Concepts
- **Autoregressive Generation**: The model generates one token at a time. Each generated token becomes part of the input context for predicting the next token.
- **Tokenization**: Raw text converted to integer token IDs via subword algorithms.
  - **BPE (Byte-Pair Encoding)**: Merges frequent character pairs iteratively.
  - **SentencePiece**: Language-agnostic BPE/Unigram tokenizer.
  - **WordPiece**: Used by BERT; similar to BPE with different scoring.
- **Context Window**: Maximum number of tokens the model can attend to at once (e.g., 4096, 8192, 128K tokens).
- **Decoding Strategies**:
  - **Greedy**: Always pick highest-probability token. Repetitive, deterministic.
  - **Sampling**: Randomly sample from probability distribution.
  - **Temperature**: Controls randomness. Low (<0.2): deterministic. High (>1.0): creative.
  - **Top-k/Top-p (nucleus)**: Restrict sampling to subset of vocabulary.

### Intermediate Concepts
- **Attention Mechanism**: Core Transformer operation. Computes weighted relationships between all token pairs in a sequence, allowing the model to focus on relevant context regardless of distance.
- **Encoder-Decoder vs Decoder-Only**:
  - *Encoder-Decoder* (T5, BART): Encode input, decode output. Good for translation, summarization.
  - *Decoder-Only* (GPT, LLaMA, Claude): Sequential generation. Dominant for chat/completion.
- **KV Cache**: Stores Key/Value projections of previous tokens during autoregressive generation. Avoids recomputing them for every new token, reducing compute from O(N²) to O(N) per step.
- **System Prompt and Instruction Tuning**: Models fine-tuned on instructions; system prompt sets behavior for inference.

### Advanced Concepts
- **Model Scaling Laws**: Performance scales predictably with parameters, data, and compute (Chinchilla/Kaplan scaling laws).
- **RLHF (Reinforcement Learning from Human Feedback)**: Aligns model outputs with human preferences using reward models and PPO.
- **Quantization**: Reducing weight precision (FP16, INT8, INT4, GPTQ, AWQ) to fit larger models on consumer hardware.
- **Mixture of Experts (MoE)**: Sparse models activate only subset of parameters per token (e.g., Mixtral), increasing capacity without proportional compute.
- **KV Cache Optimization**: MQA (Multi-Query Attention), GQA (Grouped Query Attention) reduce KV cache memory.
- **Speculative Decoding**: Small draft model proposes tokens; large model verifies. Faster inference without sampling quality loss.
- **Autoencoders**: Unsupervised neural networks designed to compress input data into a low-dimensional **latent space** representation (Encoder) and then reconstruct the original input from this latent code (Decoder). They are trained by minimizing reconstruction error (e.g. Mean Squared Error).
- **Variational Autoencoders (VAEs)**: Probabilistic generative variants of autoencoders. Instead of mapping an input to a fixed point in the latent space, the encoder outputs the parameters of a probability distribution (mean $\mu$ and variance $\sigma^2$). The decoder then samples from this distribution to generate new, unseen data instances. VAEs are optimized using the **ELBO (Evidence Lower Bound)** loss, which balances reconstruction quality and **KL Divergence** (forcing the latent distribution to match a standard normal distribution $\mathcal{N}(0, I)$).
- **LLM Fine-Tuning Approaches**: Modifying pre-trained LLM weights to specialize them on domain-specific datasets:
  - **Full Fine-Tuning**: Updates all parameters of the model. Extremely expensive and prone to **catastrophic forgetting**.
  - **PEFT (Parameter-Efficient Fine-Tuning)**: Keeps the base model weights frozen and trains a small subset of additional weights (e.g., Prefix Tuning, Prompt Tuning).
  - **LoRA / QLoRA**: Low-Rank Adaptation. Decomposes weight updates into two smaller low-rank matrices, reducing trainable parameters by >99%. QLoRA runs this over a quantized 4-bit base model, allowing fine-tuning on consumer hardware.
  - **Instruction Tuning**: Fine-tuning pre-trained base models on prompt-response pairs to teach them to follow conversational instructions.

---

## 3. Internal Working

### Transformer Architecture Diagram
```
Input Tokens + Positional Encoding
         |
         v
+------------------------------------------+
|       Embedding Layer                    |
|   (Token + Position)                     |
+------------------------------------------+
         |
         v
+------------------------------------------+
|   N x Transformer Blocks                 |
|                                          |
|   +----------------------------------+   |
|   | Multi-Head Self-Attention        |   |
|   |   Q = xWq,  K = xWk, V = xWv    |   |
|   |   Attention(Q,K,V) = softmax     |   |
|   |     (QK^T / sqrt(d)) * V        |   |
|   +----------------------------------+   |
|   | Add & Norm (Residual)            |   |
|   +----------------------------------+   |
|   | Feed Forward Network (FFN)       |   |
|   |   Linear -> Activation -> Linear |   |
|   +----------------------------------+   |
|   | Add & Norm (Residual)            |   |
|   +----------------------------------+   |
+------------------------------------------+
         |
         v
+------------------------------------------+
|    Output Head (LM Head)                 |
|    Projects to vocabulary logits         |
+------------------------------------------+
         |
         v
    Softmax -> Sample next token
```

### Autoregressive Generation Flow
```text
Prompt: "The capital of France is"
         |
         v
Tokenize: [462, 1203, 345, 7890]
         |
         v
Embedding lookup + positional encoding
         |
         v
Transformer blocks (attention over all tokens)
         |
         v
LM head logits: [batch, seq_len, vocab_size]
         |
         v
Softmax over last position -> probabilities
         |
         v
Sample: " Paris" -> append to context
         |
         v
Repeat until EOS token or max length reached
```

### KV Cache Memory Layout
```text
Without KV Cache:
  Step 1: attend over 1 token  -> compute Q,K,V for 1 token
  Step 2: attend over 2 tokens -> compute Q,K,V for 2 tokens (recompute K,V for token 1)
  Step N: attend over N tokens -> O(N^2) total compute

With KV Cache:
  Step 1: compute K,V for token 1, store in cache
  Step 2: compute K,V for token 2, append to cache; only Q for token 2 is new
  Step N: only K,V,V for token N is new -> O(N) total compute
```
Memory cost: 2 * n_layers * n_heads * head_dim * seq_len * dtype_bytes

---

## 4. Important Terminology
- **Token**: Atomic unit of text processed by the model (subword).
- **Context Window**: Maximum sequence length the model can process in one forward pass.
- **KV Cache**: Cached Key/Value projections from previous tokens during generation.
- **Temperature**: Scaling factor applied to logits before softmax; controls randomness in sampling.
- **Top-k / Top-p**: Sampling truncation strategies.
- **PPL (Perplexity)**: Exponential of average negative log-likelihood; measures language model quality. Lower is better.
- **RLHF**: Reinforcement Learning from Human Feedback for alignment.
- **Emergent Abilities**: Capabilities that appear suddenly at scale (chain-of-thought, arithmetic).
- **Hallucination**: Model generates plausible-sounding but factually incorrect or fabricated content.
- **Context Window**: Total tokens the model can attend to.

---

## 5. Beginner Examples

### Example 1: Tokenization and Vocabulary
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
text = "The quick brown fox jumps over the lazy dog"
tokens = tokenizer.encode(text)
decoded = tokenizer.decode(tokens)
print("Tokens:", tokens)
print("Decoded:", decoded)
print("Vocab size:", tokenizer.vocab_size)
```
Tokenizers map text to integers and back. Each tokenizer has a fixed vocabulary.

### Example 2: Text Generation with Temperature
```python
from transformers import pipeline

generator = pipeline("text-generation", model="gpt2")

# Greedy decoding (deterministic)
out1 = generator("The future of AI is", max_new_tokens=30, do_sample=False)

# Sampling with low temperature (more deterministic)
out2 = generator("The future of AI is", max_new_tokens=30, do_sample=True, temperature=0.3)

# Sampling with high temperature (more creative)
out3 = generator("The future of AI is", max_new_tokens=30, do_sample=True, temperature=1.2)
```
Lower temperature = more focused and deterministic; higher = more random and creative.

### Example 3: Chat Template with System Prompt
```python
messages = [
    {"role": "system", "content": "You are a helpful coding assistant."},
    {"role": "user", "content": "Write a Python function to reverse a list."}
]
input_text = tokenizer.apply_chat_template(messages, tokenize=False)
```
System prompt sets behavior; chat template formats multi-turn conversations.

### Example 4: VAE Demo 1 - Basic Autoencoder in PyTorch
This example shows a simple Autoencoder that compresses 28x28 images (like MNIST) into a 2D latent space and reconstructs them, showing the bottleneck effect and MSE loss optimization.

```python
import torch
import torch.nn as nn
import torch.optim as optim

class Autoencoder(nn.Module):
    def __init__(self, latent_dim=2):
        super(Autoencoder, self).__init__()
        # Encoder: 784 -> 128 -> 64 -> latent_dim
        self.encoder = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, latent_dim)
        )
        # Decoder: latent_dim -> 64 -> 128 -> 784
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid() # Scale outputs between 0 and 1
        )

    def forward(self, x):
        # Flatten input from (batch, 1, 28, 28) to (batch, 784)
        x_flat = x.view(x.size(0), -1)
        latent = self.encoder(x_flat)
        reconstruction = self.decoder(latent)
        # Reshape back to image dimensions
        return reconstruction.view(x.size(0), 1, 28, 28)

# Initialize model, loss function, and optimizer
model = Autoencoder(latent_dim=2)
criterion = nn.MSELoss() # Reconstruction loss
optimizer = optim.Adam(model.parameters(), lr=1e-3)

# Mock training step
dummy_batch = torch.rand(16, 1, 28, 28) # 16 dummy MNIST images
reconstructed = model(dummy_batch)
loss = criterion(reconstructed, dummy_batch)
print(f"Reconstruction Loss: {loss.item():.4f}")
```

---

## 6. Intermediate Examples

### Example 1: Controlling Generation with Top-p and Repetition Penalty
```python
outputs = model.generate(
    input_ids,
    max_new_tokens=100,
    do_sample=True,
    temperature=0.7,
    top_p=0.9,
    repetition_penalty=1.2,
    pad_token_id=tokenizer.eos_token_id
)
```
- `top_p=0.9`: nucleus sampling, restrict to top 90% cumulative probability.
- `repetition_penalty`: discourages repeating the same token.

### Example 2: Quantization for Consumer Hardware
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    quantization_config=bnb_config,
    device_map="auto"
)
```
4-bit quantization reduces a 7B model from ~14GB to ~3.5GB with minimal quality loss.

### Example 3: Measuring Perplexity
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained("gpt2")
tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "The quick brown fox jumps over the lazy dog"
encodings = tokenizer(text, return_tensors="pt")
input_ids = encodings.input_ids

with torch.no_grad():
    outputs = model(input_ids, labels=input_ids)
    loss = outputs.loss
    perplexity = torch.exp(loss)

print(f"Perplexity: {perplexity.item():.2f}")
```
Perplexity measures how "surprised" the model is by the text. Lower = more predictable.

### Example 4: VAE Demo 2 - Variational Autoencoder (VAE) Model in PyTorch
Unlike standard Autoencoders, a VAE encoder outputs mean ($\mu$) and log-variance ($\log(\sigma^2)$). It uses the **reparameterization trick** to sample latent vectors while allowing backpropagation: $z = \mu + \epsilon \odot \sigma$, where $\epsilon \sim \mathcal{N}(0, I)$.

```python
import torch
import torch.nn as nn

class VAE(nn.Module):
    def __init__(self, latent_dim=2):
        super(VAE, self).__init__()
        # Shared Encoder backbone
        self.encoder_backbone = nn.Sequential(
            nn.Linear(28 * 28, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU()
        )
        # Latent parameter projections
        self.fc_mu = nn.Linear(64, latent_dim)
        self.fc_logvar = nn.Linear(64, latent_dim)
        
        # Decoder
        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.ReLU(),
            nn.Linear(128, 28 * 28),
            nn.Sigmoid()
        )

    def encode(self, x):
        h = self.encoder_backbone(x)
        return self.fc_mu(h), self.fc_logvar(h)

    def reparameterize(self, mu, logvar):
        # Calculate standard deviation from log variance
        std = torch.exp(0.5 * logvar)
        # Sample standard normal noise epsilon
        eps = torch.randn_like(std)
        # Return reparameterized latent code z
        return mu + eps * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        x_flat = x.view(x.size(0), -1)
        mu, logvar = self.encode(x_flat)
        z = self.reparameterize(mu, logvar)
        reconstruction = self.decode(z)
        return reconstruction.view(x.size(0), 1, 28, 28), mu, logvar

# VAE Loss Function: Reconstruction (Binary Cross Entropy) + KL Divergence
def vae_loss_function(recon_x, x, mu, logvar):
    # Flatten outputs and targets
    recon_flat = recon_x.view(recon_x.size(0), -1)
    x_flat = x.view(x.size(0), -1)
    
    # 1. Reconstruction Loss (BCE)
    BCE = nn.functional.binary_cross_entropy(recon_flat, x_flat, reduction='sum')
    
    # 2. KL Divergence: -0.5 * sum(1 + log(sigma^2) - mu^2 - sigma^2)
    KLD = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
    
    return BCE + KLD
```

### Example 5: VAE Demo 3 - Latent Space Sampling and Image Generation
This example demonstrates how to generate new synthetic image instances by sampling random coordinate vectors directly from the latent Gaussian space and decoding them:

```python
import torch

def generate_new_images(vae_model, num_samples=10, latent_dim=2):
    # Set model to evaluation mode
    vae_model.eval()
    
    with torch.no_grad():
        # 1. Sample random noise from standard normal distribution
        random_latent_coords = torch.randn(num_samples, latent_dim)
        
        # 2. Pass latent samples through decoder
        generated_images_flat = vae_model.decode(random_latent_coords)
        
        # 3. Reshape flat vectors back to MNIST image dimensions
        generated_images = generated_images_flat.view(num_samples, 1, 28, 28)
        
    print(f"Successfully generated {num_samples} synthetic images from latent space.")
    return generated_images

# Sample run
vae_model = VAE(latent_dim=2)
new_digits = generate_new_images(vae_model, num_samples=5)
```

---

## 7. Advanced Concepts

### Attention Computation Complexity
```text
Standard Multi-Head Attention:
  Q: (batch, seq_len, d_model)
  K: (batch, seq_len, d_model)
  Attention scores: Q @ K^T -> (batch, heads, seq_len, seq_len)
  Memory: O(seq_len^2) for attention matrix
  Compute: O(seq_len^2 * d_model)

Efficient Attention variants:
  FlashAttention: IO-aware tiled attention, reduces HBM accesses
  Multi-Query/Grouped-Query: share K,V across heads, reduce KV cache
  Linear Attention: kernel methods to reduce to O(seq_len * d_model)
```

### Parameter-Efficient Fine-Tuning (PEFT)
```python
from peft import LoraConfig, get_peft_model, TaskType

peft_config = LoraConfig(
    r=8, lora_alpha=32, target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05, bias="none", task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)
model.print_trainable_parameters()
```
LoRA freezes base model and trains low-rank adapters. For a 7B model, trainable params drop from 7B to ~10M.

### Speculative Decoding Concept
```text
Draft model (small, fast): proposes candidate tokens
Verifier model (large): verifies candidates in a single forward pass
                          |
                          v
                If all correct: accept + generate more
                If rejection: resample from correct prefix + large model
```
Can achieve 2-3x faster inference without changing output distribution.

### Claude Agents & Autonomous Agentic Loops
LLMs can be structured as autonomous agents that orchestrate multi-step planning, tool selection, and tool execution.

- **Anthropic Claude's Native Tool Use (Function Calling)**: Instead of arbitrary text, Claude accepts a list of tool definitions (name, description, input schema in JSON). In its forward pass, Claude decides if a tool is needed, pauses generation, and returns a structured `tool_use` JSON response specifying the tool and arguments. The application executes the tool and passes the results back in a `tool_result` block.
- **Agentic Loops (ReAct)**: The "Reason-Act-Observe" loop patterns. The agent reasons about the current state, acts by using a tool, observes the results, and repeats until the goal is met.
- **Claude Computer Use API**: Enables Claude to interact directly with standard OS desktop interfaces by simulating mouse clicks, cursor movements, and keyboard inputs on screenshots.

### Project | Code Autocompletion and Bug Detection
This project demonstrates parameter-efficient fine-tuning (PEFT) of a pre-trained programming model (e.g., CodeLlama-7B) using **QLoRA** (Quantized Low-Rank Adaptation) on custom code bug-fix datasets.

#### Implementation Architecture
1. **Base Model Quantization**: Load the base model in 4-bit precision using `bitsandbytes` to reduce VRAM requirements:
   ```python
   from transformers import AutoModelForCausalLM, BitsAndBytesConfig
   import torch
   
   bnb_config = BitsAndBytesConfig(
       load_in_4bit=True,
       bnb_4bit_quant_type="nf4",
       bnb_4bit_compute_dtype=torch.bfloat16
   )
   base_model = AutoModelForCausalLM.from_pretrained(
       "codellama/CodeLlama-7b-hf",
       quantization_config=bnb_config,
       device_map="auto"
   )
   ```
2. **LoRA Adapter Setup**: Wrap the model with a PEFT configuration, targeting target linear projection modules (specifically attention layers):
   ```python
   from peft import LoraConfig, get_peft_model
   
   peft_config = LoraConfig(
       r=16, # Rank of decomposed update matrices
       lora_alpha=32, # Scaling factor
       target_modules=["q_proj", "k_proj", "v_proj", "o_proj"], # Target attention layers
       lora_dropout=0.05,
       bias="none",
       task_type="CAUSAL_LM"
   )
   peft_model = get_peft_model(base_model, peft_config)
   peft_model.print_trainable_parameters()
   ```
3. **Training Configuration**: Set up Hugging Face `SFTTrainer` (Supervised Fine-Tuning) using cosine learning decay, mixed-precision `bf16`, and gradient accumulation to simulate large batch sizes:
   ```python
   from trl import SFTTrainer
   from transformers import TrainingArguments
   
   training_args = TrainingArguments(
       output_dir="./code_qlora_results",
       learning_rate=2e-4,
       per_device_train_batch_size=4,
       gradient_accumulation_steps=4,
       logging_steps=10,
       max_steps=100,
       fp16=False,
       bf16=True, # Recommended for modern GPUs
       optim="paged_adamw_32bit"
   )
   ```
4. **Evaluation**: After training, merge weights and test the model on buggy code segments to verify that it generates syntactically correct autocompletions and detects code bugs zero-shot.

---

## 8. How Interviewers Think

### Interviewer's Perspective
They test whether you understand LLMs as statistical sequence models, not magic. They want you to explain architecture basics, tradeoffs (speed vs quality, cost vs capability), and practical deployment considerations.

### Red Flags
- Believing LLMs "store facts" like databases.
- Not knowing what tokenization does.
- Not understanding temperature and sampling.
- Confusing encoder-only, decoder-only, encoder-decoder.

### Green Flags
- Explaining attention in one paragraph.
- Understanding context window limitations.
- Knowing quantization trade-offs (speed vs quality).
- Articulating hallucinations as distributional phenomenon.
- Comparing model sizes and their hardware implications.

### Answers Matrix
| Level | Question: "What is the attention mechanism?" |
|---|---|
| **Rejected** | "It helps the model focus on important words." |
| **Shortlisted** | "Attention computes weighted sums of values based on query-key similarity." |
| **Selected** | "Self-attention computes compatibility between all token pairs via scaled dot-product: attention(Q,K,V) = softmax(QK^T / sqrt(d_k)) V. This lets every token directly attend to any other token in the sequence, capturing long-range dependencies regardless of distance in the original sequence." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions
1. What is a Transformer and how does it work?
- Architecture using self-attention to process sequences in parallel. Input tokens embedded with positional info; N attention + FFN blocks; output projected to vocabulary logits.

2. What is the difference between encoder-only, decoder-only, and encoder-decoder models?
- Encoder-only (BERT): bidirectional, good for understanding tasks.
- Decoder-only (GPT): autoregressive, good for generation.
- Encoder-decoder (T5): combines both, good for seq2seq.

3. What is tokenization and why does it matter?
- Splitting text into subword units for model processing. Affects vocabulary size, handling of rare words, token count, and cost.

4. What is the context window?
- Maximum tokens processed in one forward pass. Longer windows cost more memory and compute.

5. What is the difference between greedy decoding and sampling?
- Greedy: deterministic, always pick max probability. Sampling: stochastic, introduces variety.

6. What is temperature in LLM generation?
- Scaling logits before softmax. Low <0.3: focused. High >1.0: creative.

7. What is top-k and top-p (nucleus) sampling?
- Top-k: restrict to k most likely tokens. Top-p: restrict to smallest set with cumulative probability > p.

8. What is the KV cache and why is it important?
- Stores past Key/Value tensors during generation. Avoids recomputation, reducing generation cost from O(N²) to O(N).

9. What is RLHF and why is it used?
- Aligns model outputs with human preferences using reward model + reinforcement learning. Reduces harmful/boring outputs.

10. What is hallucination in LLMs?
- Generation of plausible but factually incorrect or fabricated content. Root cause: model predicts tokens based on training distribution, not factual database.

11. What is prompt engineering?
- Crafting input prompts to elicit desired outputs from LLMs without changing model weights.

12. What is few-shot learning for LLMs?
- Providing examples in the prompt to guide model behavior without fine-tuning.

13. What is the difference between fine-tuning and prompting?
- Fine-tuning: update model weights on task-specific data. Prompting: guide behavior via input text only.

14. What is quantization for LLMs?
- Reducing weight precision (4-bit, 8-bit) to decrease memory/speed requirements with minimal quality loss.

15. What is the difference between PPO and DPO for alignment?
- PPO: RL-based with reward model. DPO: direct preference optimization without explicit reward model (simpler, more stable).

16. What are scaling laws for LLMs?
- Predictable relationships between model size, training data, compute, and downstream performance. Loss ~ N^alpha, etc.

17. What is the difference between inference and training for LLMs?
- Training: forward + backward pass on batches, updates weights. Inference: forward pass only, generates tokens autoregressively.

18. What is catastrophic forgetting in LLMs?
- Model loses previously learned knowledge when fine-tuned on new tasks.

19. What is instruction tuning and instruction-tuning?
- Fine-tuning on (instruction, response) pairs to make models follow instructions better.

20. What is the difference between open and closed LLM APIs?
- Open: weights available for self-hosting and modification. Closed: API-only, no weight access.

20a. What is the difference between an Autoencoder and a Variational Autoencoder (VAE)?
- **Detailed Answer**: An Autoencoder compresses input data into a deterministic bottleneck vector (latent representation) and reconstructs it. A Variational Autoencoder (VAE) maps inputs to a probability distribution (mean and variance) in latent space. This allows VAEs to act as true generative models by sampling new coordinate vectors from the distribution to construct novel data instances.
- **Follow-up Questions**: What is the loss function of a VAE? (Answer: ELBO loss, combining Reconstruction loss (e.g. MSE/BCE) and KL Divergence).
- **Interviewer's Expectations**: Distinguish deterministic compression from probabilistic generative mapping.

20b. How does the reparameterization trick work in a VAE and why is it necessary?
- **Detailed Answer**: In a VAE, the encoder outputs distribution parameters ($\mu$ and $\log(\sigma^2)$) and the latent code is sampled as $z \sim \mathcal{N}(\mu, \sigma^2)$. Sampling is a stochastic process, which has no derivative and blocks backpropagation. The reparameterization trick resolves this by isolating the stochasticity: sampling $\epsilon \sim \mathcal{N}(0, I)$ and computing $z = \mu + \epsilon \odot \sigma$. Now, the model weights can be updated during training because the gradient flows through $\mu$ and $\sigma$ deterministically.
- **Follow-up Questions**: Can we train a VAE without this trick? (Answer: No, because backpropagation cannot calculate gradients through random sampling).
- **Interviewer's Expectations**: Explain the gradient bottleneck of stochastic nodes and how the trick isolates random noise.

20c. Explain the difference between full fine-tuning, PEFT, and LoRA/QLoRA.
- **Detailed Answer**: Full fine-tuning updates all model parameters, which is computationally expensive and requires high VRAM. PEFT (Parameter-Efficient Fine-Tuning) freezes the base model weights and trains only a small set of adapter weights. LoRA (Low-Rank Adaptation) decomposes weight changes by inserting two low-rank matrices ($W_0 + \Delta W$, where $\Delta W = A \times B$) into attention layers. QLoRA (Quantized LoRA) quantizes the base model to 4-bit NormalFloat (NF4) and uses a double quantization technique, drastically reducing memory footprint so a 7B model can be fine-tuned on a single 16GB GPU.
- **Follow-up Questions**: What are the trade-offs of QLoRA vs. Full Fine-Tuning? (Answer: QLoRA saves >90% VRAM with very minimal loss in model performance).
- **Interviewer's Expectations**: Detail rank decomposition, parameter savings, and quantization benefits.

### Scenario-Based Questions
21. You need to deploy a 70B parameter model on a single A100 80GB GPU.
- Use 4-bit quantization (NF4), batch size=1, flash attention, tensor parallelism if needed, or choose smaller model.

22. Your LLM output is repetitive and low-quality.
- Increase temperature, add repetition penalty, adjust top-p, improve prompt, or use better model.

23. How do you reduce LLM inference latency for production?
- Use smaller/faster model, quantization, batching, KV cache optimization, speculative decoding, caching frequent queries.

24. Your RAG system returns wrong context but retrieval looks good.
- Chunking too fine/coarse, missing metadata filtering, embedding mismatch, reranking missing, or context exceeds window.

25. Design a chatbot with conversation memory.
- Store conversation history, summarize old turns when context fills, use retrieval for long-term memory, manage system prompts.

26. How do you evaluate LLM output quality?
- Automated metrics (perplexity, BLEU, ROUGE), LLM-as-judge, human evaluation, domain-specific metrics.

27. Your 128K context model crashes with OOM.
- Reduce batch size, use gradient checkpointing, enable CPU offload for attention, or process in sliding windows.

28. How do you ensure LLM outputs are factually grounded?
- RAG with verified sources, constrain output format, use tool use APIs, post-hoc verification, lower temperature.

29. Design a multi-turn customer support LLM system.
- Conversation state management, context window management, escalation to human, logging for quality, PII redaction.

30. You need to fine-tune an LLM on domain documents.
- Use LoRA/QLoRA for efficiency, chunk documents, create instruction pairs, validate on held-out domain data.

### Debugging Questions
31. Model generates Empty or garbage output.
- Check tokenizer compatibility, prompt format, EOS token handling, model loading errors.

32. Text generation is extremely slow.
- Batch size=1, no KV cache, CPU inference, large model on insufficient hardware. Enable all optimizations.

33. Model repeats phrases infinitely.
- Missing EOS token handling, too high temperature, bad sampling params. Add stop sequences.

34. Different runs produce different outputs with same prompt.
- Sampling is stochastic (temperature > 0). Use `do_sample=False` for determinism.

35. Fine-tuned model is worse than base model.
- Catastrophic forgetting, bad hyperparameters, too few examples, learning rate too high.

### System Design Questions
36. Design an LLM inference serving system.
- Model sharding, request batching, queue management, caching (Redis), load balancing, monitoring (latency, throughput, cost).

37. Design a coding assistant with codebase context.
- Index repository embeddings, chunk by function/file, hybrid search (BM25 + semantic), reranker, context window management.

38. Design a document QA system.
- Multi-stage: query rewriting -> dense retrieval -> reranking -> LLM generation -> citation extraction -> confidence scoring.

---

## 10. Common Mistakes
- Not understanding LLMs predict tokens, not "look up facts."
- Ignoring context window limits.
- Using greedy decoding for creative tasks.
- Not handling tokenization edge cases (special tokens, encoding errors).
- Forgetting to set pad_token_id for batch generation.
- Deploying without rate limiting or cost controls.

---

## 11. Comparison Section: LLM Architectures
| Architecture | Type | Context | Strengths | Weaknesses |
|---|---|---|---|---|
| **Decoder-only** | Autoregressive | Long | Strong generation, simple | Slow generation |
| **Encoder-only** | Bidirectional | Medium | Understanding tasks | No generation |
| **Encoder-Decoder** | Seq2seq | Long | Translation, summarization | More complex |
| **State Space (Mamba)** | Selective SSM | Very Long | O(L) training, long context | Less mature ecosystem |

---

## 12. Practical Project Ideas
- **Beginner**: Fine-tune a small LLM (GPT-2) on custom text using LoRA.
- **Intermediate**: Build RAG system with retrieval and generation pipeline.
- **Advanced**: Optimize inference with quantization and speculative decoding.

---

## 13. Internship Preparation Notes
- **Research roles**: Transformers, attention, scaling laws, training dynamics.
- **Applied ML/ML Eng**: Inference optimization, quantization, serving architectures.
- **Prompt engineering roles**: prompt design, few-shot learning, evaluation frameworks.

---

## 14. Cheat Sheet
- **Tokenization**: Text -> tokens -> IDs. Vocab size fixed.
- **Decoding**: greedy, sampling temperature, top-k, top-p.
- **KV Cache**: stores past K,V for efficient autoregressive generation.
- **RLHF**: RL with human preferences for alignment.
- **Scaling**: More parameters + data + compute generally improves performance.
- **Quantization**: INT4/INT8 for deployment, smaller models, faster inference.
- **PEFT**: LoRA, prefix-tuning, prompt-tuning for efficient fine-tuning.

---

## 15. One-Day Revision Guide
- [ ] Explain Transformer self-attention formula.
- [ ] Draw encoder-decoder vs decoder-only flow.
- [ ] Explain autoregressive generation and KV cache.
- [ ] Compare decoding strategies (greedy, sampling, top-k, top-p).
- [ ] List 3 LLM deployment optimization techniques.
- [ ] Explain hallucination and when it occurs.
- [ ] Compare fine-tuning vs prompting vs RAG.
- [ ] Describe quantization and PEFT briefly.
