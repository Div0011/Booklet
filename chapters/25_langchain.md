# 25. LangChain (AI Orchestration Framework)

## 1. Introduction
### What it is
LangChain is an open-source framework designed to simplify the construction of applications powered by Large Language Models. It provides standard abstractions for chaining components (prompts, models, parsers), managing memory, loading documents, and building autonomous agents.

### Why it exists
Building real-world AI applications requires more than just sending a single text prompt to an LLM. It requires orchestrating complex pipelines: loading PDFs, retrieving vector contexts, keeping track of conversation history, and enabling models to call external APIs (tools). LangChain was created to standardize these components into a clean, reusable framework.

### Problems it solves
- **API Fragmentation**: Unifies access to different LLM providers (OpenAI, Anthropic, Hugging Face) under a standard interface.
- **Complex Chain Mechanics**: Replaces manual string manipulation with **LCEL (LangChain Expression Language)** for pipeline composition.
- **State Management**: Simplifies managing chat memory and retrieval histories.

### Industry Use Cases
- **Enterprise Chatbots**: Conversational interfaces with database access and chat history.
- **Autonomous Agents**: AI workers that can browse the web, write code, and update databases.
- **Data Extraction Pipelines**: Ingesting, parsing, and structured cleaning of raw documents.

---

## 2. Core Concepts

### Beginner Concepts
- **Chains**: The basic building block of LangChain. It combines a Prompt Template, an LLM, and an Output Parser into a single executable pipeline.
- **Prompt Templates**: Reusable templates that accept dynamic parameters to construct prompts:
  ```python
  template = "Translate this text to {language}: {text}"
  ```
- **Models**: Unified interfaces for LLMs (text completion) and Chat Models (structured message arrays).

### Intermediate Concepts
- **LCEL (LangChain Expression Language)**: A declarative way to chain components together using the pipe operator (`|`). It supports streaming, async calls, and parallel execution automatically:
  ```python
  chain = prompt | model | parser
  ```
- **Retrievers**: Interfaces that wrap vector databases to retrieve relevant document chunks based on a query.
- **Memory**: State management tools (like `ConversationBufferMemory`) used to store and retrieve chat history across turns.

### Advanced Concepts
- **Agents**: Systems where the LLM acts as a reasoning engine, deciding which actions (tools) to execute based on user inputs.
- **Tools**: Functions that agents can call (e.g. search APIs, database query tools, file readers).
- **Runnables**: The core interface behind LCEL. Every LCEL component inherits from the `Runnable` class, which defines standard methods like `.invoke()`, `.stream()`, and `.ainvoke()`.

---

## 3. Internal Working

### LCEL Composition & Agent Execution Loop
LCEL uses Python's operator overloading (the `__or__` method) to pipe components together, managing data flow and execution.

```text
 [ User Inputs ] 
       |
       v
 [ PromptTemplate ] 
       |
       v (String Output)
 [ ChatModel (LLM) ] 
       |
       v (Message Output)
 [ OutputParser ] 
       |
       v
 [ Structured Result ]
```

1. **The Pipe Operator (`|`)**:
   - In Python, overloading the `__or__` operator allows piping components: `chain = prompt | model`.
   - Under the hood, this wraps the components in a `RunnableSequence`.
   - When `.invoke()` is called, the sequence passes the output of each component as the input to the next, handling serialization and type conversions automatically.
2. **The Agent Execution Loop**:
   - The user asks a question.
   - The Agent runs the prompt through the LLM, which outputs either an **AgentAction** (specifying a tool to call and its arguments) or an **AgentFinish** (the final answer).
   - If the output is an `AgentAction`, the system executes the specified tool, collects the output (Observation), appends it to the history, and routes it back to the LLM to decide the next step.
   - This loop repeats until the LLM outputs an `AgentFinish` response.

---

## 4. Important Terminology
- **LCEL**: LangChain Expression Language.
- **Runnable**: The base interface for all LCEL components.
- **Agent**: An LLM-driven executor that determines which actions to take.
- **Tool**: A function that can be executed by an agent.
- **LangSmith**: A developer platform used to trace, debug, and monitor LangChain pipelines.

---

## 5. Beginner Examples

### Example 1: Basic Translation Chain (LCEL)
This example demonstrates creating a basic chain using prompt templates, an LLM, and an output parser using LCEL syntax.

```python
# To run this, install: pip install langchain langchain-openai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# 1. Initialize Model
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 2. Define Prompt Template
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")

# 3. Initialize Output Parser
parser = StrOutputParser()

# 4. Compose Chain using LCEL pipe syntax
chain = prompt | model | parser

# 5. Execute Chain
# result = chain.invoke({"topic": "artificial intelligence"})
# print(result)
```

---

## 6. Intermediate Examples

### Example 1: Conversational Memory Agent with Tools
This example demonstrates building a conversational agent that uses memory to retain history and has access to a mock search tool.

```python
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

# 1. Define custom tools using the @tool decorator
@tool
def check_flight_status(flight_number: str) -> str:
    """Checks the real-time status of a flight."""
    # Mock lookup
    if flight_number == "AA101":
        return "Flight AA101 is delayed by 45 minutes due to weather."
    return f"Flight {flight_number} is currently on time."

tools = [check_flight_status]

# 2. Define System Prompt with Memory and Tool placeholders
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful travel assistant. Use tools if needed to check flights."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"), # Temporary workspace for tool logs
])

# 3. Initialize Model and bind tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# 4. Construct Agent
agent = create_openai_tools_agent(llm, tools, prompt)

# 5. Construct AgentExecutor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True # Logs thoughts and actions in the console
)

# 6. Run Agent with mock memory history
# history = []
# response = agent_executor.invoke({
#     "input": "Can you check flight AA101 for me?",
#     "chat_history": history
# })
# print(response["output"])
```

---

## 7. Advanced Concepts

### Streaming & LangSmith Tracing
- **Streaming Tokens**: LLMs generate text token-by-token. In web interfaces, waiting for the full response to generate before displaying it can feel slow. LCEL supports streaming natively using `.stream()`. For asynchronous operations, use `.astream()`, which returns an async generator that yields chunks of the response as they are generated.
- **LangSmith Tracing**: Debugging nested agent loops is difficult because you cannot see intermediate tool calls or LLM prompts. By configuring environment variables, LangSmith hooks into LangChain's callback system, logging every step, prompt, and tool execution in a web UI for easy debugging.

```python
# Enable LangSmith Tracing
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your_api_key"
```

### Advanced Retrievers and Text Splitters (LangChain Retrieval)
Real-world RAG systems require sophisticated ingestion and retrieval strategies beyond simple document-to-vector mappings.

* **RecursiveCharacterTextSplitter**: Splits text based on a prioritized list of characters (`["\n\n", "\n", " ", ""]`). This keeps related semantic paragraphs together before splitting on words, preventing loss of context.
* **Parent Document Retriever**: Splits documents into small chunks for vector search (to maximize retrieval accuracy) but returns the larger "parent" document or a larger section (to provide richer context to the LLM).
* **Self-Querying Retriever**: Uses an LLM to parse a natural language query into a structured query query filter + search string, allowing query filtering on metadata fields.
* **Multi-Query Retriever**: Uses an LLM to generate multiple variations of the query, retrieves documents for all queries, and takes the union of results to overcome query wording limitations.

#### Code Example: Parent Document and Multi-Query Ingestion Pipeline
```python
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.retrievers import ParentDocumentRetriever, MultiQueryRetriever
from langchain.storage import InMemoryStore

# 1. Load and Split Ingestion Configurations
loader = TextLoader("workspace_doc.txt")
documents = loader.load()

# Splitters for Parent Document Retriever:
# Small chunks for vector similarity search
child_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
# Large chunks (parent) to feed as context to LLM
parent_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# 2. Vectorstore and Docstore Setup
vectorstore = Chroma(
    collection_name="parent_documents",
    embedding_function=OpenAIEmbeddings()
)
store = InMemoryStore() # Stores parent documents mapped to child IDs

# 3. Initialize Parent Document Retriever
parent_retriever = ParentDocumentRetriever(
    vectorstore=vectorstore,
    docstore=store,
    child_splitter=child_splitter,
    parent_splitter=parent_splitter,
)

# Ingest documents (automatically splits parents, indexes children, maps them)
parent_retriever.add_documents(documents, ids=None)

# 4. Multi-Query Retriever Composition
# Wraps parent_retriever to generate query variations and retrieve matching documents
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
multi_query_retriever = MultiQueryRetriever.from_llm(
    retriever=parent_retriever,
    llm=llm
)

# 5. Retrieve Context
# unique_docs = multi_query_retriever.invoke("What are the system configuration limits?")
```

---

## 8. How Interviewers Think

### Interviewer's Perspective
Interviewers look for candidates who understand how LangChain works under the hood rather than just copying tutorial boilerplate. They want to see if you can explain LCEL compilation, manage chat histories in production databases, register custom tools with descriptive docstrings, and debug nested agents using tracing tools.

### Red Flags
- Believing that LangChain is a model itself (it is only an orchestration framework).
- Writing custom tools without docstrings. LangChain reads the tool's docstring to generate instructions for the LLM; omitting the docstring prevents the model from understanding when to call the tool.
- Hardcoding system prompts inside application logic instead of using Prompt Templates.

### Green Flags
- Writing custom tools with descriptive docstrings that explain input schemas and use cases.
- Using LCEL's `.stream()` or `.astream()` to optimize user experience.
- Using LangSmith or custom callbacks to trace and debug agent execution pipelines.

### Answers Matrix
| Level | Question: "How does an agent determine which tool to call in LangChain?" |
|---|---|
| **Rejected** | "The framework has code that maps keywords to the tool names automatically." |
| **Shortlisted** | "LangChain passes the tool names and descriptions to the LLM. The LLM decides which tool to use and returns the tool name in its response." |
| **Selected** | "When a tool is registered, LangChain extracts its name, description, and input schema (often using Pydantic). These descriptions are formatted into a system prompt or passed as tool schemas to the LLM API (like OpenAI's function calling). The LLM decides which tool is needed, generates a structured response specifying the tool name and arguments, and LangChain intercepts this output to execute the tool function locally." |

---

## 9. Frequently Asked Interview Questions

### Conceptual Questions

#### 1. What is LCEL (LangChain Expression Language) and what are its benefits?
- **Detailed Answer**: LCEL is a declarative language used to chain LangChain components together using the pipe operator (`|`). It abstracts data flow, input/output parsing, and serialization. Its benefits include:
  1. **Built-in Streaming**: Allows streaming tokens directly to the client.
  2. **Async Support**: Allows running chains asynchronously.
  3. **Parallel Execution**: Automatically executes independent steps in parallel to reduce latency.
- **Follow-up Questions**: How do you run steps in parallel in LCEL? (Answer: Use `RunnableParallel` or pass a dictionary of runnables).
- **Interviewer's Expectations**: Describe composition syntax, async/streaming support, and parallel execution.

#### 2. What is the role of the `agent_scratchpad` in agent prompts?
- **Detailed Answer**: The `agent_scratchpad` is a temporary message history placeholder. It stores the intermediate thoughts, tool calls, and tool outputs (observations) generated during the current reasoning cycle. This history is sent back to the LLM on each iteration so the model can inspect past tool outputs and decide the next step.
- **Follow-up Questions**: What happens if the scratchpad runs out of token space?
- **Interviewer's Expectations**: Explain the scratchpad's role in storing intermediate thoughts and observations.

*(Remaining questions available in the interactive reader...)*

### Scenario-Based Questions

#### 3. You build a LangChain agent with access to a database query tool. During testing, the agent occasionally enters an infinite loop, querying the same table repeatedly. How do you resolve this?
- **Detailed Answer**:
  - Set the `max_iterations` parameter on the `AgentExecutor` to force the loop to stop after a set number of steps.
  - Implement custom parser validation or check tool outputs in a callback to detect repeating cycles.
  - Adjust the system prompt. Instruct the agent to stop querying and report an error if it receives empty or identical results.
- **Follow-up Questions**: How does the `max_execution_time` parameter help?
- **Interviewer's Expectations**: Detail execution limits, prompt constraints, and validation options.

#### 4. How do you persist chat memory across sessions in a multi-user production chatbot using LangChain?
- **Detailed Answer**: In-memory storage (like `ConversationBufferMemory`) will lose history when the server restarts.
  1. Store chat logs in an external database (like Redis, DynamoDB, or PostgreSQL) using LangChain's message history integrations (e.g. `RedisChatMessageHistory`).
  2. Map message history instances to unique session IDs: `session_history = RedisChatMessageHistory(session_id=user_session_id)`.
  3. Pass the session history to a `RunnableWithMessageHistory` wrapper to manage loading and saving message histories automatically.
- **Follow-up Questions**: How do you summarize older messages to save token costs? (Answer: Use `ConversationSummaryMemory` to compress history).
- **Interviewer's Expectations**: Propose database-backed storage (Redis) and outline how to manage sessions.

*(Remaining questions available in the interactive reader...)*

### Debugging Questions

#### 5. Debug the following custom tool definition, which the agent fails to call correctly:
```python
from langchain_core.tools import tool

@tool
def get_user_balance(user_id):
    # Mock query
    return f"Balance is $150"
```
- **Detailed Answer**: The tool lacks a docstring and type hints. LangChain reads the function's docstring and type hints to generate instructions for the LLM. Without them, the LLM does not know what inputs the tool expects or when to call it.
- **Fix**: Add type hints and a descriptive docstring explaining the tool's purpose and input parameters:
  ```python
  @tool
  def get_user_balance(user_id: str) -> str:
      """Retrieves the current bank account balance for a specified user ID."""
      return f"Balance is $150"
  ```
- **Follow-up Questions**: How do you define complex input schemas using Pydantic?
- **Interviewer's Expectations**: Explain that docstrings and type hints are used to define the tool's API schema for the LLM.

*(Remaining questions available in the interactive reader...)*

### System Design Questions

#### 6. Design an agent architecture that processes user queries, searches a knowledge base, generates SQL queries to retrieve metrics, and returns a formatted report.
- **Detailed Answer**:
  - **Tool Definitions**: Define two tools: `knowledge_retriever` (wraps a vector database search) and `sql_query_runner` (executes SQL queries against a read-only database).
  - **Orchestration**: Use **LangGraph** to define the workflow as a state machine. This allows us to define loops (e.g. if the SQL query fails, return to the SQL generation node to fix the error).
  - **Memory**: Use a Redis-backed memory store to retain chat history.
  - **Deployment**: Serve the graph using FastAPI, streaming tokens back to the user.
- **Follow-up Questions**: Why is LangGraph preferred over a simple AgentExecutor for complex workflows? (Answer: LangGraph provides precise control over loops and states, whereas AgentExecutor is a black box).
- **Interviewer's Expectations**: Propose a structured agent architecture with specific tools, graph layouts, and memory management.

*(Remaining questions available in the interactive reader...)*

### Real Interview Questions

#### 7. What is the difference between LangChain and LlamaIndex?
- **Detailed Answer**:
  - **LangChain** is a general-purpose orchestration framework, best for building complex agents, pipelines, and workflows.
  - **LlamaIndex** is data-centric, focusing on indexing, retrieving, and connecting external data sources to LLMs. Use it for data-heavy RAG pipelines.
- **Follow-up Questions**: Can you use LlamaIndex retrievers inside a LangChain pipeline? (Answer: Yes).
- **Interviewer's Expectations**: Compare the strengths and primary focus areas of both frameworks.

*(Remaining questions available in the interactive reader...)*

---

## 10. Common Mistakes
- **Omitting Tool Docstrings**: Prevents the LLM from understanding what inputs the tool expects or when to call it.
- **Using raw chat memory at scale**: Storing long conversation histories increases token costs and can exceed the model's context window. Implement message pruning or summarization strategies.

---

## 11. Comparison Section: AI Orchestration Frameworks
| Feature | LangChain | LlamaIndex | LangGraph |
|---|---|---|---|
| **Primary Focus** | General orchestration | Data indexing & RAG | Cyclic agent state machines |
| **Workflow Model** | Sequential chains (LCEL) | Data index loaders | State graphs (Nodes & Edges) |
| **Loop Control** | Hard to control loops | Basic loops | Full loop control |
| **Best For** | Standard LLM applications | Structured data retrieval | Custom, multi-agent workflows |

---

## 12. Practical Project Ideas
- **Beginner**: A translation chain utilizing LCEL prompts and chat models.
- **Intermediate**: A conversational document assistant using LangChain retrievers and database-backed memory.
- **Advanced/Resume-worthy**: A multi-agent collaboration graph (using LangGraph) that searches the web, writes code, executes it in a sandbox, and generates a formatted PDF report.

---

## 13. Internship Preparation Notes
- **Recruiters ask**: LangChain basics, chains, and prompt templates.
- **AI startups expect**: Experience writing custom tools, managing memory, composing LCEL pipelines, and debugging agents using LangSmith.

---

## 14. Cheat Sheet
- **LCEL Pipe**: `chain = prompt | model | parser`
- **Tool docstrings**: Always include descriptive docstrings and type hints to define the tool's schema for the LLM.
- **Memory**: Use database-backed memory (like Redis) for production chatbots.
- **Tracing**: Use LangSmith to trace and debug agent execution steps.

---

## 15. One-Day Revision Guide
- [ ] Write a basic LCEL chain using prompt templates, an LLM, and an output parser.
- [ ] Understand why type hints and docstrings are mandatory for custom tools.
- [ ] Explain how the Agent execution loop works.
- [ ] Compare LangChain, LlamaIndex, and LangGraph.
