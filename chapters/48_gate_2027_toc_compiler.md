# 48. GATE 2027: Theory of Computation & Compiler Design

## Table of Contents
- [1. Introduction](#1-introduction)
- [2. Core Concepts](#2-core-concepts)
  - [2.1 Beginner Level (Finite Automata & Lexical Basics)](#21-beginner-level)
  - [2.2 Intermediate Level (Grammars, Pushdown Automata & Parsing)](#22-intermediate-level)
  - [2.3 Advanced Level (Turing Machines, Undecidability & Code Optimization)](#23-advanced-level)
- [3. Internal Working](#3-internal-working)
- [4. Important Terminology](#4-important-terminology)
- [5. Beginner Examples](#5-beginner-examples)
- [6. Intermediate Examples](#6-intermediate-examples)
- [7. Advanced Examples](#7-advanced-examples)
- [8. How Interviewers Think](#8-how-interviewers-think)
- [9. FAQs (25 High-Yield GATE & Interview Questions)](#9-faqs)
- [10. Common Mistakes](#10-common-mistakes)
- [11. Comparison Tables](#11-comparison-tables)
- [12. Practical Projects](#12-practical-projects)
- [13. Internship Preparation](#13-internship-preparation)
- [14. Cheat Sheet](#14-cheat-sheet)
- [15. One-Day Revision Checklist](#15-one-day-revision-checklist)

---

## 1. Introduction

### What is Theory of Computation & Compiler Design?
**Theory of Computation (TOC)** is the mathematical study of abstract computing machines, formal languages, computability, and complexity. It defines what can and cannot be computed under finite memory (Finite Automata), stack memory (Pushdown Automata), and infinite memory (Turing Machines).
**Compiler Design** applies formal language theory to construct software translation systems that map high-level code into executable machine instructions through lexical scanning, syntax analysis, semantic verification, intermediate code generation, and machine-independent/dependent optimizations.

### Why it Exists & Problems it Solves
1. **Defines Computational Limits:** Proves fundamentally undecidable problems (like the Halting Problem and Rice's Theorem) where no algorithm can ever exist.
2. **Deterministic Translation:** Enables rock-solid, unambiguous compilers and interpreters that parse programming languages in linear time.
3. **Database Query Engines:** SQL parsers build ASTs and execute relational algebra optimizations based directly on compiler pipeline theory.

### Industry Use Cases
- Domain-Specific Language (DSL) design in enterprise engines.
- Static application security testing (SAST) and compiler warnings (LLVM, Clang, GCC, Rustc).
- Regular expression engines in grep, Python `re`, JavaScript V8 runtime, and database indexing.

### Analogy: The Global Translation Embassy
- **Lexical Analysis (Scanner):** Groups characters into words (tokens) according to vocabulary rules.
- **Syntax Analysis (Parser):** Validates sentence grammar against formal rules and builds parse trees.
- **Semantic Analysis:** Checks that sentences make contextual sense (type checks, variable scope).
- **Intermediate Code:** Translates the parsed structure into a universal intermediate lingua franca (Three-Address Code).
- **Optimization:** Simplifies sentences without altering meaning (eliminating redundancies and dead code).
- **Code Generation:** Emits local machine dialects (x86, ARM, RISC-V).

---

## 2. Core Concepts

### 2.1 Beginner Level

#### Regular Languages and Finite Automata
- **Deterministic Finite Automaton (DFA):** Defined as 5-tuple $(Q, \Sigma, \delta, q_0, F)$ where $\delta: Q 	imes \Sigma ightarrow Q$. Exactly one deterministic transition per input symbol from each state. No $\epsilon$-transitions.
- **Nondeterministic Finite Automaton (NFA):** 5-tuple where $\delta: Q 	imes \Sigma ightarrow 2^Q$. Transitions to multiple states or on empty string $\epsilon$.
- **Equivalence:** For every NFA with $n$ states, there exists an equivalent DFA with at most $2^n$ states (Subset Construction).
- **Regular Expressions (RegEx):** Operators: Union ($+$ or $|$), Concatenation ($\cdot$), Kleene Star ($*$).
- **Arden's Theorem:** If $P$ and $Q$ are regular expressions and $P$ does not contain $\epsilon$, then the equation $R = Q + RP$ has a unique solution $R = QP^*$.
- **DFA Minimization:** Uses Myhill-Nerode theorem and the Table-Filling Algorithm (partitioning into equivalence classes of indistinguishable states). Minimal DFA is unique up to state isomorphism.

#### Lexical Analysis Basics
- Scans input characters and produces a stream of tokens `<token_type, attribute_value>`.
- Identifies lexemes, ignores whitespace and comments, populates the Symbol Table.
- Uses Flex/Lex regular expressions translated into NFAs via Thompson's Construction, converted to DFAs via Subset Construction.

---

### 2.2 Intermediate Level

#### Context-Free Grammars (CFG) & Pushdown Automata (PDA)
- **CFG Definition:** 4-tuple $(V, T, P, S)$ where production rules have form $A ightarrow lpha$ with $A \in V, lpha \in (V \cup T)^*$.
- **Derivations:** Leftmost Derivation (LMD), Rightmost Derivation (RMD), and Parse Trees.
- **Ambiguity:** A grammar is ambiguous if there exists at least one string with two or more distinct parse trees (or distinct LMDs/RMDs). Inherent ambiguity: a language is inherently ambiguous if *every* grammar generating it is ambiguous (e.g., $L = \{a^i b^j c^k \mid i=j \lor j=k\}$).
- **Pushdown Automata (PDA):** 7-tuple $(Q, \Sigma, \Gamma, \delta, q_0, Z_0, F)$ with an unbounded LIFO stack. Accepts by final state or by empty stack.
- **DPDA vs NPDA:** Deterministic PDA is strictly less powerful than Non-deterministic PDA. NPDAs accept all Context-Free Languages (CFLs); DPDAs accept Deterministic CFLs (DCFLs).

#### Syntax Analysis (Parsing)
- **Top-Down Parsing (LL(1)):** Builds parse tree from root down. Requires grammar to be free of left recursion and left factoring. Uses **FIRST** and **FOLLOW** sets.
  - $A ightarrow lpha \mid eta$ is LL(1) iff $FIRST(lpha) \cap FIRST(eta) = \emptyset$ and if $\epsilon \in FIRST(lpha)$, then $FIRST(eta) \cap FOLLOW(A) = \emptyset$.
- **Bottom-Up Parsing (LR Parsing):** Shifts tokens onto stack and reduces by productions (Rightmost derivation in reverse).
  - **LR(0):** Uses canonical collection of LR(0) items.
  - **SLR(1):** Uses LR(0) items + FOLLOW sets to resolve reductions.
  - **LALR(1):** Merges LR(1) states having identical LR(0) cores.
  - **CLR(1) / Canonical LR(1):** Uses LR(1) items $[A ightarrow lpha \cdot eta, a]$. Most powerful deterministic LR parser, but largest table size.
  - Power Hierarchy: $LR(0) \subset SLR(1) \subset LALR(1) \subset CLR(1) = LR(1)$.

---

### 2.3 Advanced Level

#### Turing Machines, Computability & Undecidability
- **Turing Machine (TM):** 7-tuple $(Q, \Sigma, \Gamma, \delta, q_0, B, F)$ with infinite two-way tape and read/write head. $\delta: Q 	imes \Gamma ightarrow Q 	imes \Gamma 	imes \{L, R\}$.
- **Chomsky Hierarchy:**
  - **Type 3:** Regular Languages $\leftrightarrow$ Finite Automata
  - **Type 2:** Context-Free Languages $\leftrightarrow$ Pushdown Automata
  - **Type 1:** Context-Sensitive Languages $\leftrightarrow$ Linear Bounded Automata
  - **Type 0:** Recursively Enumerable Languages (RE) $\leftrightarrow$ Turing Machines (Turing-recognizable)
  - **Recursive Languages (REC):** Decidable languages; TM always halts (accepts or rejects).
- **Undecidability:**
  - **Halting Problem ($H_{TM}$):** Undecidable and semi-decidable (RE but not REC).
  - **Rice's Theorem:** Any non-trivial semantic property of the language recognized by a Turing machine is undecidable.
  - **Post Correspondence Problem (PCP):** Undecidable for alphabets with $\ge 2$ symbols.

#### Syntax-Directed Translation (SDT) & Code Optimization
- **S-Attributed SDD:** Uses only synthesized attributes. Evaluated bottom-up during LR parsing.
- **L-Attributed SDD:** Attributes can be synthesized or inherited from left siblings/parent. Evaluated in depth-first left-to-right traversal.
- **Intermediate Representations:** Three-Address Code (TAC), Quadruples (op, arg1, arg2, result), Triples, Directed Acyclic Graphs (DAG).
- **Code Optimization:**
  - **Local Optimization:** Common Subexpression Elimination, Copy Propagation, Dead Code Elimination, Constant Folding.
  - **Loop Optimization:** Loop Invariant Code Motion, Strength Reduction, Loop Unrolling.
  - **Data Flow Analysis:** Reaching Definitions (union framework), Available Expressions (intersection framework), Live Variable Analysis (backward union).

---

## 3. Internal Working

### 3.1 Chomsky Hierarchy & Automata Capabilities
```
+-------------------------------------------------------------+
| Type 0: Recursively Enumerable (RE)                        |
| Turing Machine (May loop forever on non-members)           |
|  +--------------------------------------------------------+ |
|  | Recursive Languages (REC) - Decidable (TM Always Halts)| |
|  |  +---------------------------------------------------+ | |
|  |  | Type 1: Context-Sensitive (CSL)                   | | |
|  |  | Linear Bounded Automata (LBA)                     | | |
|  |  |  +----------------------------------------------+ | | |
|  |  |  | Type 2: Context-Free Languages (CFL)          | | | |
|  |  |  | Non-deterministic PDA (NPDA)                 | | | |
|  |  |  |  +-----------------------------------------+ | | | |
|  |  |  |  | Deterministic CFL (DCFL) - DPDA         | | | | |
|  |  |  |  |  +------------------------------------+ | | | | |
|  |  |  |  |  | Type 3: Regular Languages          | | | | | |
|  |  |  |  |  | DFA / NFA (Finite Memory)          | | | | | |
|  |  |  |  |  +------------------------------------+ | | | | |
|  |  |  |  +-----------------------------------------+ | | | |
|  |  |  +----------------------------------------------+ | | |
|  |  +---------------------------------------------------+ | |
|  +--------------------------------------------------------+ |
+-------------------------------------------------------------+
```

### 3.2 Compiler Execution Pipeline & Data Flow
```
 Source Program (Text Stream)
        │
        ▼
 [ 1. Lexical Analyzer ] ──────► Symbol Table
        │ (Tokens)
        ▼
 [ 2. Syntax Analyzer ]  ──────► Syntax Tree / AST
        │ (Parse Tree)
        ▼
 [ 3. Semantic Analyzer ] ─────► Type-Checked Decorated AST
        │
        ▼
 [ 4. Intermediate Code Gen ] ──► Three-Address Code (TAC) / DAG
        │
        ▼
 [ 5. Machine-Independent Opt ] ─► Optimized TAC (Dead code / Common subexpr removed)
        │
        ▼
 [ 6. Target Code Generator ] ──► Target Assembly / Machine Code
```

---

## 4. Important Terminology

- **DFA (Deterministic Finite Automaton):** State machine with deterministic transitions for every input symbol.
- **NFA (Non-deterministic Finite Automaton):** State machine allowing multiple simultaneous transitions and epsilon moves.
- **Pumping Lemma:** Mathematical property used to prove that a language is NOT regular or NOT context-free.
- **Ambiguity:** Grammar property where a string possesses more than one valid parse tree.
- **FIRST(α):** Set of terminals that begin strings derived from $lpha$.
- **FOLLOW(A):** Set of terminals that can appear immediately to the right of non-terminal $A$ in some sentential form.
- **Shift-Reduce Conflict:** LR parser state where it is valid to either shift the next token or reduce by an existing production.
- **Reduce-Reduce Conflict:** LR parser state where two distinct productions can be used for reduction simultaneously.
- **S-Attributed Grammar:** Syntax-directed definition using solely synthesized attributes computed bottom-up.
- **L-Attributed Grammar:** Syntax-directed definition where inherited attributes depend only on parents and left siblings.
- **Three-Address Code (TAC):** Linearized representation where each instruction has at most one operator on the right side.
- **DAG (Directed Acyclic Graph):** Graph representation for basic blocks that automatically identifies common subexpressions.
- **Decidable Problem:** A decision problem for which a Turing machine exists that halts and answers YES or NO for every input instance.
- **Rice's Theorem:** Formal theorem proving that any non-trivial semantic property of Turing machine languages is undecidable.

---

## 5. Beginner Examples

### Example 1: Minimal DFA for Binary Strings Divisible by 3
```python
# Transition Table for (Binary Number modulo 3)
# State q0 = Remainder 0 (Start & Final State)
# State q1 = Remainder 1
# State q2 = Remainder 2

def dfa_divisible_by_3(binary_str: str) -> bool:
    state = 0  # q0
    transitions = {
        0: {"0": 0, "1": 1},
        1: {"0": 2, "1": 0},
        2: {"0": 1, "1": 2}
    }
    for char in binary_str:
        if char not in transitions[state]:
            return False
        state = transitions[state][char]
    return state == 0

# Test cases
print(dfa_divisible_by_3("110"))  # 6 % 3 == 0 -> True
print(dfa_divisible_by_3("101"))  # 5 % 3 == 2 -> False
print(dfa_divisible_by_3("1001")) # 9 % 3 == 0 -> True
```

### Example 2: Computing FIRST and FOLLOW Sets
Given grammar:
$$S ightarrow A B$$
$$A ightarrow a \mid \epsilon$$
$$B ightarrow b \mid c$$

- $FIRST(A) = \{a, \epsilon\}$
- $FIRST(B) = \{b, c\}$
- $FIRST(S) = (FIRST(A) \setminus \{\epsilon\}) \cup FIRST(B) = \{a, b, c\}$
- $FOLLOW(S) = \{\$\}$, $FOLLOW(A) = FIRST(B) = \{b, c\}$, $FOLLOW(B) = FOLLOW(S) = \{\$\}$.

---

## 6. Intermediate Examples

### Example 1: Eliminating Left Recursion
Immediate Left Recursion rule:
$$A ightarrow Alpha_1 \mid Alpha_2 \mid eta_1 \mid eta_2$$
Transformed into:
$$A ightarrow eta_1 A' \mid eta_2 A'$$
$$A' ightarrow lpha_1 A' \mid lpha_2 A' \mid \epsilon$$

Given Expression Grammar:
$$E ightarrow E + T \mid T$$
$$T ightarrow T * F \mid F$$
$$F ightarrow ( E ) \mid id$$

Transformed non-left-recursive grammar for LL(1) parser:
$$E ightarrow T E'$$
$$E' ightarrow + T E' \mid \epsilon$$
$$T ightarrow F T'$$
$$T' ightarrow * F T' \mid \epsilon$$
$$F ightarrow ( E ) \mid id$$

---

## 7. Advanced Examples

### Example 1: Proving Non-Regularity with Pumping Lemma
**Claim:** $L = \{a^n b^n \mid n \ge 0\}$ is not regular.
1. Assume $L$ is regular with pumping length $p$.
2. Choose string $w = a^p b^p \in L$ where $|w| = 2p \ge p$.
3. By Pumping Lemma, $w = xyz$ where $|xy| \le p$ and $|y| > 0$.
4. Since $|xy| \le p$, $y$ consists entirely of $a$'s ($y = a^k, k \ge 1$).
5. Pump for $i=2$: $x y^2 z = a^{p+k} b^p$.
6. Since $k \ge 1$, number of $a$'s is $p+k 
e p$ (number of $b$'s).
7. Hence $x y^2 z 
otin L$, violating the lemma. Therefore $L$ is NOT regular.

### Example 2: Common Subexpression Elimination via DAG Construction
Expression:
```c
a = b + c;
d = b + c;
e = a * d;
```
1. Node $N_1 = +(b, c)$. Assign label $a$.
2. When evaluating $b + c$ for $d$, search DAG: Node $N_1$ with operator $+$ and children $(b, c)$ already exists. Reuse $N_1$ and attach label $d$.
3. Node $N_2 = *(a, d) = *(N_1, N_1)$. Assign label $e$.
Optimized Three-Address Code:
```c
t1 = b + c
a = t1
d = t1
e = t1 * t1
```

---

## 8. How Interviewers Think

- **Subset Construction Trap:** Examiners frequently ask for the maximum number of states in a minimal DFA converted from an $n$-state NFA. Maximum theoretical is $2^n$, but check reachability and dead states.
- **Ambiguity Detection:** Remember that determining if an arbitrary context-free grammar is ambiguous is **undecidable**.
- **Closure Properties:** Always memorize the closure matrix across union, intersection, complementation, concatenation, and reversal. Regular languages are closed under ALL major operations; CFLs are NOT closed under intersection and complementation.

---

## 9. FAQs (25 High-Yield GATE & Interview Questions)

### Q1: Is the language $L = \{w w^R \mid w \in \{a, b\}^*\}$ regular, DCFL, or CFL?
**Answer:** It is a Non-Deterministic CFL (CFL, but not DCFL). A PDA cannot know where the midpoint of the string occurs without nondeterministic guessing. In contrast, $L = \{w c w^R\}$ with a distinct center marker $c$ is a DCFL accepted by a DPDA.

### Q2: What is the difference between S-attributed and L-attributed SDDs?
**Answer:** S-attributed SDDs contain only synthesized attributes evaluated in bottom-up order. L-attributed SDDs permit both synthesized and inherited attributes, with the restriction that inherited attributes can only depend on inherited/synthesized attributes of parents and left siblings. Every S-attributed SDD is an L-attributed SDD, but not vice-versa.

### Q3: Why is LL(1) strictly weaker than LR(1)?
**Answer:** An LL(1) parser must decide which production to apply seeing only the first token (looking ahead 1 symbol) before seeing any child subtree. An LR(1) parser delays the decision until it has parsed the entire handle (entire right-hand side of production) plus 1 lookahead symbol, possessing significantly greater context.

### Q4: State Rice's Theorem and give an example of its application.
**Answer:** Rice's Theorem states that any non-trivial semantic property of the language recognized by a Turing machine is undecidable. A property is non-trivial if it holds for some RE languages and not for others. Example: "Is $L(M)$ empty?" is a semantic property (depends on language, not machine code length) and is non-trivial, so it is undecidable.

### Q5: Can an ambiguous grammar be parsed by an LR(1) parser?
**Answer:** No. An ambiguous grammar will always produce at least one shift-reduce or reduce-reduce conflict in any LR($k$) parsing table.

---

## 10. Common Mistakes

| Anti-Pattern | Why It Is Wrong | Correct Approach |
| :--- | :--- | :--- |
| Assuming all CFLs are closed under intersection | Intersection of two CFLs can produce non-CFL ($a^n b^n c^m \cap a^m b^n c^n = a^n b^n c^n$) | CFLs are NOT closed under intersection, but intersection of CFL with Regular is CFL |
| Confusing DPDA acceptance criteria | Acceptance by empty stack and final state are NOT equivalent for DPDAs | Empty stack DPDA accepts only prefix-free languages; final-state DPDA is more powerful |
| Confusing LR(0) and SLR(1) reduction placement | In LR(0), reduce actions are placed in ALL columns of the row | In SLR(1), reduce actions are placed ONLY in columns belonging to $FOLLOW(A)$ |

---

## 11. Comparison Tables

### Formal Language Properties Matrix
| Property | Regular | DCFL | CFL | CSL | Recursive | RE |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Union** | Yes | No | Yes | Yes | Yes | Yes |
| **Intersection** | Yes | No | No | Yes | Yes | Yes |
| **Complement** | Yes | Yes | No | Yes | Yes | No |
| **Concatenation**| Yes | No | Yes | Yes | Yes | Yes |
| **Kleene Star** | Yes | No | Yes | Yes | Yes | Yes |
| **Membership** | Decidable | Decidable | Decidable | Decidable | Decidable | Semi-Decidable |
| **Emptiness** | Decidable | Decidable | Decidable | Undecidable| Undecidable| Undecidable |
| **Equivalence**| Decidable | Decidable | Undecidable| Undecidable| Undecidable| Undecidable |

---

## 12. Practical Projects

### Project: Building a Miniature Lexer & Recursive Descent Calculator in Python
```python
import re

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def tokenize(code):
    token_spec = [
        ("NUMBER",  r"\d+(\.\d*)?"),
        ("PLUS",    r"\+"),
        ("MINUS",   r"-"),
        ("MUL",     r"\*"),
        ("DIV",     r"/"),
        ("LPAREN",  r"\("),
        ("RPAREN",  r"\)"),
        ("SKIP",    r"[ 	]+"),
    ]
    tok_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind != "SKIP":
            yield Token(kind, float(value) if kind == "NUMBER" else value)

class CalculatorParser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type=None):
        tok = self.peek()
        if expected_type and (not tok or tok.type != expected_type):
            raise SyntaxError(f"Expected {expected_type}, got {tok}")
        self.pos += 1
        return tok

    def expr(self):
        result = self.term()
        while self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.consume().type
            if op == "PLUS": result += self.term()
            elif op == "MINUS": result -= self.term()
        return result

    def term(self):
        result = self.factor()
        while self.peek() and self.peek().type in ("MUL", "DIV"):
            op = self.consume().type
            if op == "MUL": result *= self.factor()
            elif op == "DIV": result /= self.factor()
        return result

    def factor(self):
        tok = self.peek()
        if tok.type == "NUMBER":
            self.consume()
            return tok.value
        elif tok.type == "LPAREN":
            self.consume("LPAREN")
            val = self.expr()
            self.consume("RPAREN")
            return val
        raise SyntaxError(f"Unexpected token: {tok}")

# Execution test
calc = CalculatorParser(tokenize("3 + 5 * (10 - 2)"))
print("Evaluated Expression Result:", calc.expr())  # Output: 43.0
```

---

## 13. Internship Preparation

1. Master DFA state minimization algorithms and subset construction mechanics.
2. Be able to calculate FIRST and FOLLOW sets by hand for any grammar in under 2 minutes.
3. Be able to differentiate between S-attributed and L-attributed syntax directed definitions.
4. Know the exact decidability results for Turing Machines, PCP, and grammar equivalence.
5. Understand code generation for basic blocks and Directed Acyclic Graphs.

---

## 14. Cheat Sheet

- **Arden's Theorem:** $R = Q + RP \implies R = QP^*$.
- **Number of states in minimal DFA for binary string ending in specific pattern of length $k$:** Exactly $k+1$ states.
- **LL(1) Condition:** No Left Recursion, No Common Prefixes (Left Factored), Disjoint FIRST and FOLLOW sets for nullable productions.
- **Parser Table Size:** $LR(0) = SLR(1) < LALR(1) \le CLR(1)$. Number of states in $LALR(1) =$ Number of states in $LR(0)$.
- **3-Address Code:** $x = y 	ext{ op } z$ or $x = 	ext{op } y$.

---

## 15. One-Day Revision Checklist

- [ ] Review DFA minimization table-filling steps and Dead State properties.
- [ ] Calculate FIRST/FOLLOW sets on sample arithmetic grammar.
- [ ] Review LR(0), SLR(1), LALR(1), CLR(1) conflict resolution rules.
- [ ] Check closure properties table for Regular, CFL, and Recursive languages.
- [ ] Review Rice's Theorem conditions for Undecidability.
- [ ] Review Basic Block partitioning rules and DAG common subexpression elimination.
