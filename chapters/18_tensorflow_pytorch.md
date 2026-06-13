# 18. TensorFlow & PyTorch (Deep Learning Frameworks)

## 1. Introduction
### What it is
TensorFlow and PyTorch are the two dominant open-source deep learning frameworks. TensorFlow, from Google, emphasizes production deployment and ecosystem tooling. PyTorch, from Meta, emphasizes research flexibility and Pythonic dynamic computation graphs.

### Why they exist
Before these frameworks, deep learning required implementing backpropagation, CUDA kernels, and optimization from scratch. TensorFlow (2015) and PyTorch (2017) automated autodifferentiation, GPU acceleration, and neural network building blocks, democratizing access to deep learning.

### Problems they solves
- **Manual gradient computation**: Autodiff (autograd) handles chain rule automatically.
- **GPU programming**: Abstracts CUDA/Metal/TPU kernels behind tensor operations.
- **Production deployment**: Serving, quantization, optimization, ONNX/TFLite export.
- **Research velocity**: Dynamic graphs enable debugging and rapid prototyping.

### Industry Use Cases
- **Research**: Paper implementations, new architectures, ablation studies.
- **Production**: Recommendation systems, NLP pipelines, computer vision APIs.
- **Edge/Mobile**: Quantized models via TFLite, ONNX Runtime, TensorRT.
- **Scientific computing**: Physics simulations, drug discovery, genomics.

### Analogy
TensorFlow is a commercial shipyard: massive infrastructure, standardized parts, built for long voyages (production). PyTorch is a custom boat workshop: flexible, easy to modify, favored by explorers (researchers).

---

## 2. Core Concepts

### Beginner Concepts
- **Tensor**: N-dimensional array with automatic differentiation support.
- **Computation Graph**: Directed graph of operations; enables autodiff.
- **Static vs Dynamic Graphs**:
  - Static (TensorFlow 1.x): graph defined before execution; optimized but rigid.
  - Dynamic (PyTorch default, TF Eager): define by run; debuggable, flexible.
- **Autograd**: Automatic differentiation engine computing gradients via chain rule.
- **GPU/TPU Acceleration**: Tensors can reside on accelerators; operations execute there.

### Intermediate Concepts
- **Optimizers**: SGD, Adam, AdamW, RMSprop, LAMB.
- **Data Loading**: `Dataset` + `DataLoader` (PyTorch), `tf.data` (TensorFlow).
- **Saved Formats**:
  - PyTorch: `state_dict`, `torch.save`, `torch.load`, TorchScript/TorchInductor.
  - TensorFlow: SavedModel, Keras H5, TFLite, ONNX.
- **Mixed Precision**: FP16 training with loss scaling for numerical stability.
- **Distributed Training**: `DistributedDataParallel` (DDP), `FullyShardedDataParallel` (FSDP), `tf.distribute`.

### Advanced Concepts
- **JIT Compilation**: TorchScript, `torch.compile` (Inductor), XLA for TensorFlow.
- **Quantization**: INT8/FP16 weight and activation quantization for deployment.
- **Pruning**: Structured/unstructured sparsity for inference speedup.
- **Custom Autograd Functions**: Extend autograd with custom forward/backward.
- **Meta-devices and Lazy Execution**: PyTorch 2.0 `torch.compile`, lazy tensors.
- **Accelerator Orchestration**: TPU pods, GPU clusters, pipeline parallelism.

### Deep-Dive: Framework Syntax Comparison
- **Tensor Operations**:
  - *PyTorch*: `x = torch.tensor([1.0, 2.0], dtype=torch.float32, requires_grad=True)`
  - *TensorFlow*: `x = tf.Variable([1.0, 2.0], dtype=tf.float32)`
- **Auto-differentiation**:
  - *PyTorch*: Uses dynamic graph execution under `autograd`. Gradients computed by running `loss.backward()`, populating `tensor.grad`.
  - *TensorFlow*: Uses `tf.GradientTape()` context manager. Tapes operations on variables, then `tape.gradient(loss, variables)` is called.
- **Layers & Model Definition**:
  - *PyTorch*: Class subclasses `nn.Module`. Defines layers in `__init__` and computation in `forward(x)`.
  - *TensorFlow*: Class subclasses `tf.keras.Model` or uses Keras Sequential API. Defines layers in `__init__` and computation in `call(x)`.

### Deep-Dive: Netron Visualization & Colab Pro Configuration
- **Netron Model Visualizer**:
  - Netron is a structural visualization tool for deep learning models. It inputs serialized model binaries (e.g., `.onnx`, `.tflite`, `.pb`, `.h5`, `.pt`) and produces an interactive, graphical representation of the model's computational DAG.
  - Useful for: validating layer connectivity, checking output shape matching, auditing parameter dimensions, and debugging custom tensor operations.
- **Google Colab Pro Optimization**:
  - **GPU Runtimes**: Access to high-performance accelerators: NVIDIA T4 (standard), V100, and A100 Tensor Core GPUs (delivering up to 40GB VRAM, critical for batch sizes of large LLMs/Vision models).
  - **Memory Management**: High-RAM runtimes allow up to 51GB RAM, avoiding Out-Of-Memory (OOM) crashes during large dataset transformations.
  - **Drive Mount**:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    ```
    Allows direct reading and writing of checkpoints to Google Drive, securing parameters against unexpected session timeouts.
  - **Command Terminal**: Colab Pro features a Linux terminal access, allowing developers to execute git commands, pip installations, and custom training launch scripts directly.

---

## 3. Internal Working

### PyTorch Autograd Mechanism
```text
Forward Pass:
  x -> Linear -> ReLU -> Linear -> output
       |        |       |
       v        v       v
  saved_tensor saved_tensor saved_tensor

  Each operation stores Function object + saved tensors

Backward Pass:
  output.grad -> function.apply(saved_tensors, grad_output)
              -> compute grad w.r.t inputs
              -> propagate to previous layer
```
Autograd records operations on tensors with `requires_grad=True`. During backward, saved tensors replay operations.

### TensorFlow Execution Paths
```text
Eager Mode (TF 2.x default):
  Python op execution immediate, tensors concrete values
  tf.GradientTape records operations for gradient computation

Graph Mode (@tf.function):
  Python code traces into TF graph
  XLA compiler optimizes graph (fusion, constant folding)
  Executes as single optimized unit
```
`tf.function` balances Python flexibility with graph performance.

### Memory Layout During Training
```text
GPU Memory:
  +----------------------------------+
  | Model Parameters (FP32/FP16/BF16)|
  +----------------------------------+
  | Optimizer States (FP32 often 2x-3x params) |
  +----------------------------------+
  | Activations (per layer outputs)  |
  +----------------------------------+
  | Gradients (same size as params)  |
  +----------------------------------+
  | Optimizer temporaries            |
  +----------------------------------+
```
ZeRO/FSDP shards optimizer states and gradients across devices to fit larger models.

---

## 4. Important Terminology
- **Tensor**: Multi-dimensional array with gradient support.
- **Autograd**: Automatic differentiation engine.
- **Computation Graph**: Directed graph of operations for gradient computation.
- **Eager Execution**: Immediate evaluation of operations (PyTorch default, TF 2 default).
- **Graph Execution**: Deferred execution with optimization (TF 1.x, TF `@tf.function`).
- **State Dict**: Serialized parameter dictionary for model save/load.
- **JIT Compilation**: Just-in-time compilation to optimized kernels.
- **Mixed Precision**: Mixed FP16/FP32 training for speed and memory.
- **DataLoader**: Batched, parallel data loading with prefetching.
- **DistributedDataParallel (DDP)**: Synchronous multi-GPU training.

---

## 5. Beginner Examples

### Example 1: PyTorch Tensor Operations and Autograd
```python
import torch

# Create tensors with gradient tracking
x = torch.tensor([[1.0, 2.0], [3.0, 4.0]], requires_grad=True)
y = x ** 2
z = y.sum()

# Backward pass computes gradients
z.backward()
print("dz/dx:", x.grad)  # Should be 2*x
```
`requires_grad=True` enables gradient computation. `backward()` populates `.grad`.

### Example 2: Simple Neural Network in PyTorch
```python
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.3),
    nn.Linear(256, 10)
)
print("Parameters:", sum(p.numel() for p in model.parameters()))
```
`nn.Sequential` chains layers. `sum(p.numel())` counts total parameters.

### Example 3: Basic Training Loop
```python
import torch.optim as optim

optimizer = optim.Adam(model.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

model.train()
for xb, yb in train_loader:
    optimizer.zero_grad()       # 1. Clear old gradients
    preds = model(xb)           # 2. Forward pass
    loss = criterion(preds, yb) # 3. Compute loss
    loss.backward()             # 4. Backward pass
    optimizer.step()            # 5. Update weights
```
Always call `zero_grad()` before `backward()` to avoid gradient accumulation.

### Example 4: Saving and Loading Models
```python
# Save
torch.save(model.state_dict(), "model.pt")

# Load
model.load_state_dict(torch.load("model.pt", map_location="cpu"))
model.eval()  # Set to evaluation mode
```
Save `state_dict` not entire model for portability. Call `eval()` for inference (disables dropout, uses running stats in BN).

---

## 6. Intermediate Examples

### Example 1: Custom Dataset and DataLoader
```python
from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):
    def __init__(self, features, labels):
        self.features = torch.tensor(features, dtype=torch.float32)
        self.labels = torch.tensor(labels, dtype=torch.long)
    
    def __len__(self):
        return len(self.features)
    
    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

dataset = MyDataset(X, y)
loader = DataLoader(dataset, batch_size=32, shuffle=True, num_workers=4)
```
Custom datasets enable data augmentation on-the-fly and lazy loading.

### Example 2: Learning Rate Scheduling
```python
from torch.optim.lr_scheduler import CosineAnnealingLR

optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
scheduler = CosineAnnealingLR(optimizer, T_max=50, eta_min=1e-5)

for epoch in range(50):
    train_one_epoch(model, loader, optimizer, criterion)
    scheduler.step()
    current_lr = scheduler.get_last_lr()[0]
```
Cosine annealing smoothly decreases LR; often yields better convergence than step decay.

### Example 3: TensorBoard Integration
```python
from torch.utils.tensorboard import SummaryWriter

writer = SummaryWriter(log_dir="runs/exp1")
writer.add_scalar('Loss/train', train_loss, epoch)
writer.add_scalar('Loss/val', val_loss, epoch)
writer.add_scalar('Accuracy/val', val_acc, epoch)
writer.close()
```
TensorBoard logs scalars, histograms, images, model graphs for debugging.

### Example 4: Transfer Learning with Frozen Backbone
```python
import torchvision.models as models

backbone = models.resnet50(weights="IMAGENET1K_V1")
for param in backbone.parameters():
    param.requires_grad = False  # Freeze backbone

# Replace classifier
backbone.fc = nn.Linear(2048, num_classes)
# Only train classifier layer
optimizer = optim.Adam(backbone.fc.parameters(), lr=1e-3)
```
Freezing backbone is essential when target dataset is small or fine-tuning budget is limited.

### Example 5: PyTorch vs. TensorFlow Custom Training Loops
Here we contrast the native API architectures for custom training loops on synthetic regression data.

**PyTorch Implementation:**
```python
import torch
import torch.nn as nn
import torch.optim as optim

# 1. Setup Model, Optimizer, and Loss
model = nn.Linear(10, 1)
optimizer = optim.SGD(model.parameters(), lr=0.01)
criterion = nn.MSELoss()

# 2. Training Loop
for epoch in range(100):
    inputs = torch.randn(32, 10)
    targets = torch.randn(32, 1)
    
    # Forward Pass
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    
    # Backward Pass & Optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    if epoch % 20 == 0:
        print(f"PyTorch Epoch {epoch} Loss: {loss.item():.4f}")
```

**TensorFlow Implementation:**
```python
import tensorflow as tf

# 1. Setup Model, Optimizer, and Loss
model = tf.keras.layers.Dense(1)
optimizer = tf.keras.optimizers.SGD(learning_rate=0.01)
loss_fn = tf.keras.losses.MeanSquaredError()

# 2. Training Loop with tf.function (graphs compilation)
@tf.function
def train_step(x, y):
    with tf.GradientTape() as tape:
        predictions = model(x)
        loss = loss_fn(y, predictions)
    gradients = tape.gradient(loss, model.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model.trainable_variables))
    return loss

for epoch in range(100):
    inputs = tf.random.normal((32, 10))
    targets = tf.random.normal((32, 1))
    loss = train_step(inputs, targets)
    
    if epoch % 20 == 0:
        print(f"TensorFlow Epoch {epoch} Loss: {loss.numpy():.4f}")
```

### Example 6: TensorBoard Tracking and Netron Visualization Setup
Exporting computational logs for profiling and visualizing a model using Netron.

```python
import torch
import torch.nn as nn
from torch.utils.tensorboard import SummaryWriter

# 1. Define Model
class SimpleMLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(28*28, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )
    def forward(self, x):
        return self.net(x)

model = SimpleMLP()

# 2. Export model graph to TensorBoard
writer = SummaryWriter("runs/netron_tb_demo")
dummy_input = torch.randn(1, 28*28)
writer.add_graph(model, dummy_input)
writer.close()

# 3. Export model structure to ONNX for Netron visualization
torch.onnx.export(
    model, 
    dummy_input, 
    "mlp_model.onnx", 
    input_names=["input_pixels"], 
    output_names=["class_logits"]
)
print("ONNX model saved. You can now open 'mlp_model.onnx' in Netron (https://netron.app) to inspect it.")
```

---

## 7. Advanced Concepts

### Distributed Data Parallel (DDP)
```python
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

torch.distributed.init_process_group("nccl")
local_rank = int(os.environ["LOCAL_RANK"])
torch.cuda.set_device(local_rank)
model = DDP(model.to(local_rank), device_ids=[local_rank])
```
DDP replicates model across GPUs, synchronizes gradients via all-reduce. More efficient than DataParallel.

### Model Quantization for Deployment
```python
import torch.quantization

model_fp32 = model.eval()
model_int8 = torch.quantization.quantize_dynamic(
    model_fp32, {nn.Linear, nn.Conv2d}, dtype=torch.qint8
)
```
Dynamic quantization converts weights to INT8 at runtime; reduces model size ~4x and speeds up CPU inference.

### Mixed Precision with Gradient Scaling
```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for batch in loader:
    optimizer.zero_grad()
    with autocast():
        output = model(batch)
        loss = criterion(output, target)
    scaler.scale(loss).backward()
    scaler.step(optimizer)
    scaler.update()
```
Gradient scaling prevents FP16 underflow during backprop.

### TorchInductor (torch.compile)
```python
model = torch.compile(model, mode="max-autotune")
```
TorchInductor traces Python code, fuses operations, generates optimized kernels via Triton. Often yields 2x speedups with single line change.

---

## 8. How Interviewers Think

### Interviewer's Perspective
They test whether you understand the frameworks as tools, not magic. They want to see you can build, debug, train, and deploy models while understanding underlying mechanics: autodiff, GPU memory, distributed training, and optimization.

### Red Flags
- Not understanding forward/backward pass mechanics.
- Confusing `model.train()` and `model.eval()` modes.
- Not knowing why `zero_grad()` is necessary.
- Using FP16 without loss scaling.
- Saving entire model objects instead of `state_dict`.

### Green Flags
- Explaining computation graphs and autograd.
- Understanding GPU memory management.
- Knowing when to freeze layers in transfer learning.
- Using distributed training correctly (DDP over DataParallel).
- Articulating PyTorch eager vs graph tradeoffs.

### Answers Matrix
| Level | Question: "What is PyTorch's autograd and how does it work?" |
|---|---|
| **Rejected** | "It calculates gradients automatically." |
| **Shortlisted** | "It records operations for tensors with requires_grad=True, then backpropagates gradients." |
| **Selected** | "Autograd records operations on tensors with `requires_grad=True` by saving the `Function` and input tensors. During `backward()`, saved tensors replay operations in reverse topological order, computing local gradients via chain rule. This enables end-to-end gradient computation without manual derivative formulas." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions
1. What is the difference between PyTorch and TensorFlow?
- PyTorch: dynamic graphs, Pythonic, research-first. TensorFlow: static+dynamic, ecosystem-heavy, production-first.

2. What is a tensor and how does it differ from a NumPy array?
- Tensors are multi-dimensional arrays with GPU support and autograd. NumPy arrays lack automatic differentiation.

3. What is autograd?
- Automatic differentiation engine recording operations and replaying them for backpropagation.

4. What is the difference between `torch.Tensor` and `torch.nn.Parameter`?
- `Parameter` is a `Tensor` subclass registered as a model parameter (visible to `model.parameters()`).

5. What is a computation graph?
- Directed acyclic graph of operations; enables efficient gradient computation via backprop.

6. What is the difference between static and dynamic computation graphs?
- Static: graph defined before execution (TF 1.x). Dynamic: graph built during forward pass (PyTorch, TF 2.x eager).

7. What is a state dict in PyTorch?
- Dictionary mapping layer names to parameter tensors; used for `save`/`load`.

8. What is the difference between `model.train()` and `model.eval()`?
- `train()`: enables dropout, batch norm training mode. `eval()`: disables dropout, uses running stats.

9. What is `zero_grad()` and why is it necessary?
- Clears accumulated gradients. Without it, new gradients add to old ones from previous iterations.

10. What is the difference between `torch.save` and `pickle`?
- `torch.save` uses Python pickle under the hood but adds tensor serialization. Prefer `state_dict` for model weights.

11. What is the difference between CPU and CUDA tensors?
- CUDA tensors reside in GPU memory, enabling massive parallelism. Must move data between devices.

12. What is mixed precision training?
- Uses FP16/BF16 where possible to reduce memory and increase speed. Requires gradient scaling for numerical stability.

13. What is the difference between DataParallel and DistributedDataParallel?
- DataParallel: single process, replicates model on current GPU. DDP: multiple processes, each GPU runs one process, all-reduce gradients (faster).

14. What is a checkpoint in deep learning?
- Saved model state at an epoch: weights, optimizer state, scheduler state, epoch number.

15. What is the difference between eager and graph execution?
- Eager: run operations immediately (PyTorch default). Graph: define operations, execute optimized graph (TF `@tf.function`).

### Scenario-Based Questions
16. Your model trains on CPU but should use GPU.
- Call `model.to('cuda')` and move inputs to same device. Check `torch.cuda.is_available()`.

17. You get `CUDA out of memory` during training.
- Reduce batch size, use gradient accumulation, enable mixed precision, use gradient checkpointing, clear cache with `torch.cuda.empty_cache()`.

18. How do you debug a model that produces NaN losses?
- Check for division by zero, log(0), uninitialized layers, too-high learning rate. Use `torch.autograd.set_detect_anomaly(True)`.

19. Your model trains but validation accuracy doesn't improve.
- Check learning rate, model capacity, data quality, augmentation mismatch, overfitting (use regularization).

20. You need to deploy a PyTorch model for production.
- Export via TorchScript (`torch.jit.trace`/`script`), ONNX, or TorchInductor. Quantize for edge deployment.

21. How do you handle variable-length sequences in batching?
- Use `pack_padded_sequence`/`pad_packed_sequence` with `torch.nn.utils.rnn`, or pad manually and use attention masks.

22. Your DataLoader is much slower than GPU compute.
- Increase `num_workers`, use `pin_memory=True`, prefetch with `prefetch_factor`, avoid heavy CPU transforms in DataLoader.

23. How do you load a model trained on multiple GPUs on a single GPU?
- Load `state_dict` with `map_location='cpu'` first, then strip `module.` prefix from keys if needed.

24. You need to fine-tune a large language model with limited GPU memory.
- Use LoRA/QLoRA, gradient checkpointing, mixed precision, ZeRO stage 3/FSDP, offload optimizer states to CPU.

25. How do you ensure reproducible training?
- Set random seeds for Python, NumPy, PyTorch, CUDA. Use deterministic algorithms (`torch.use_deterministic_algorithms(True)`).

### Debugging Questions
26. `RuntimeError: size mismatch` in linear layer.
- Input shape doesn't match layer weight shape. Inspect `x.shape` before forward. Check flatten/view operations.

27. `AttributeError: 'NoneType' object has no attribute 'grad'`.
- Intermediate tensor lost gradient history due to inplace operation (`+=`) on tensor requiring grad. Use out-of-place ops.

28. `CUDA error: device-side assert triggered`.
- Usually label index out of range for CrossEntropyLoss. Check `labels.max() < num_classes`.

29. Model.load_state_dict() fails with size mismatch.
- Saved model architecture differs from current. Check layer shapes and keys. Use `strict=False` to load partial match.

30. Training is slow despite using GPU.
- Model too small for GPU (CPU bound), data loading bottleneck, too many CPU-to-GPU transfers, small batch size.

### System Design Questions
31. Design a distributed training pipeline for large models.
- Use FSDP or ZeRO-3 for sharding. Mixed precision. Gradient checkpointing. Checkpointing every N steps. Monitor GPU utilization and memory.

32. Design a model serving architecture.
- Model serialization -> batching service (TorchServe, TensorRT) -> REST/gRPC endpoint -> load balancer -> monitoring.

33. Design a recommendation model training and serving system.
- Two-tower model trained with sampled softmax. Embeddings exported to FAISS. Online serving: ANN retrieval + lightweight ranker.

---

#### 61. Contrast PyTorch dynamic graphs with TensorFlow static graphs. Discuss eagerness, trace compiling, and debugging.
- **Detailed Answer**: The core architectural difference lies in how they construct and execute the computational graph:
  - **PyTorch (Dynamic / Define-by-Run)**:
    - *Mechanism*: PyTorch builds the computation graph on-the-fly during the forward pass. Every operation (e.g., adding two tensors) dynamically appends a node to the execution graph.
    - *Eagerness*: Execution is immediate. Tensors contain concrete values.
    - *Debugging*: Standard Python debugging tools (e.g., `pdb`, print statements) work seamlessly. Error traces point exactly to the offending line of Python code.
    - *JIT Compilation*: Can compile graphs using `torch.compile` or TorchScript for production optimization.
  - **TensorFlow (Static / Define-then-Run)**:
    - *Mechanism*: Historically (TF 1.x), the graph structure was defined using symbolic placeholders before execution, and run inside a `Session`. Modern TF (2.x) runs in **Eager Execution** mode by default.
    - *Trace Compiling*: By wrapping a function in `@tf.function`, TF traces the Python operations, constructs a static computation graph (polymorphic tracing), and optimizes it using the XLA (Accelerated Linear Algebra) compiler.
    - *Debugging*: Harder to debug traced functions since variables contain symbolic nodes rather than concrete values. Error traces map to the compiled C++ runtime, rather than Python lines.
- **Follow-up Questions**: When should you disable `@tf.function` tracing? (Answer: During debugging, or when your function has dynamic Python control flow that changes execution logic per call, which would trigger constant re-tracing overhead).
- **Interviewer's Expectations**: Explain the concepts of define-by-run vs. define-then-run, discuss eager execution vs. static graphs, explain how tracing works in `@tf.function`, and compare their debugging profiles.

---

#### 62. What is the API contract for writing custom layers in PyTorch vs. TensorFlow Keras?
- **Detailed Answer**:
  - **PyTorch (`nn.Module`)**:
    - Subclass `nn.Module`.
    - Instantiate sub-layers or custom parameter tensors in `__init__`. Parameters must be wrapped in `nn.Parameter(tensor)` to register them in the model's parameter list so that optimizers can track them.
    - Implement `forward(*input)` defining the forward pass logic. Autograd automatically builds the backward pass.
    - Example:
      ```python
      class MyLinear(nn.Module):
          def __init__(self, in_features, out_features):
              super().__init__()
              self.weight = nn.Parameter(torch.randn(out_features, in_features))
              self.bias = nn.Parameter(torch.zeros(out_features))
          def forward(self, x):
              return x @ self.weight.t() + self.bias
      ```
  - **TensorFlow Keras (`tf.keras.layers.Layer`)**:
    - Subclass `tf.keras.layers.Layer`.
    - Implement `__init__` to handle input-independent configurations.
    - Implement `build(self, input_shape)`: This is where variables are created once the input shape is known, using `self.add_weight`. This avoids hardcoding input dimensions.
    - Implement `call(self, inputs)` defining the computation.
    - Example:
      ```python
      class MyLinear(tf.keras.layers.Layer):
          def __init__(self, units):
              super().__init__()
              self.units = units
          def build(self, input_shape):
              self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer="random_normal", trainable=True)
              self.b = self.add_weight(shape=(self.units,), initializer="zeros", trainable=True)
          def call(self, inputs):
              return tf.matmul(inputs, self.w) + self.b
      ```
- **Follow-up Questions**: Why is the `build` method useful in Keras? (Answer: It enables shape inference. Layers can be declared without specifying input feature dimensions, which are dynamically resolved during the first forward pass).
- **Interviewer's Expectations**: Compare PyTorch's `nn.Parameter` initialization in `__init__` to Keras's `add_weight` execution in `build`, show basic code snippets for both frameworks, and explain the dynamic shape inference benefits of the Keras `build` stage.

---

## 10. Common Mistakes
- Forgetting `.to(device)` on model and data.
- Using `model.eval()` only for inference, not validation.
- Accumulating gradients unintentionally (missing `zero_grad`).
- FP16 without loss scaling causing underflow.
- Saving optimizer alongside model when only weights needed.
- Modifying tensors in-place that require gradients.

---

## 11. Comparison Section: TensorFlow vs PyTorch
| Feature | TensorFlow | PyTorch |
|---|---|---|
| **Graph style** | Static (1.x) or dynamic/eager (2.x) | Dynamic by default |
| **API style** | Keras high-level + low-level | Pythonic, imperative |
| **Production** | TFLite, TF Serving, TFX | TorchScript, TorchServe, ONNX |
| **Research adoption** | High | Very High |
| **Debugging** | `tf.function` can obscure errors | Immediate tensor values |
| **Ecosystem** | Extensive (TFX, TFLite, TF Hub) | Growing (PyTorch Lightning, HF) |

---

## 12. Practical Project Ideas
- **Beginner**: MNIST classifier reaching 98% accuracy with PyTorch.
- **Intermediate**: CIFAR-10 classifier with data augmentation and transfer learning.
- **Advanced**: Distilled model deployment with ONNX/TensorRT optimization.

---

## 13. Internship Preparation Notes
- **Research roles**: PyTorch fluency, understanding training mechanics, reading papers.
- **ML Engineer**: deployment formats, quantization, TorchScript/TFLite.
- **Data Scientist**: transfer learning, fine-tuning, batch training.

---

## 14. Cheat Sheet
- **Tensors**: `requires_grad=True`, `.to(device)`, `.cpu()`, `.cuda()`.
- **Autograd**: `loss.backward()`, `torch.no_grad()`, `.detach()`, `retain_graph`.
- **NN modules**: `nn.Linear`, `nn.Conv2d`, `nn.ReLU`, `nn.Dropout`, `nn.Sequential`.
- **Optimizers**: Adam (default), SGD + momentum, AdamW.
- **Training loop**: `zero_grad()` -> forward -> loss -> `backward()` -> `step()`.
- **Save/Load**: `state_dict`, `torch.save`, `torch.load`, `model.eval()`.

---

## 15. One-Day Revision Guide
- [ ] Draw forward/backward pass for a 3-layer MLP.
- [ ] Explain autograd in one paragraph.
- [ ] List differences between PyTorch eager and TF graph modes.
- [ ] Write a minimal training loop in PyTorch.
- [ ] Describe mixed precision training and loss scaling.
- [ ] Compare DDP vs DataParallel for multi-GPU.
- [ ] Save and load model state dict correctly.
- [ ] Explain when to freeze layers during transfer learning.
- [ ] List 3 deployment export formats.
- [ ] Debug a single batch through model by hand.
