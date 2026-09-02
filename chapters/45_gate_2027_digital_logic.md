# 45. GATE 2027 Digital Logic (CS Syllabus Section 2)

## 1. Introduction

### What it is
Digital Logic is the foundational discipline underpinning every computing device, from microprocessors and GPUs to embedded controllers in IoT devices. For GATE 2027 Computer Science, Section 2 mandates mastery of Boolean algebra, function minimization (algebraic, Karnaugh map, Quine-McCluskey), combinational and sequential circuit design, and number representation including fixed-point and IEEE 754 floating-point arithmetic. This chapter unifies the mathematical theory of Boolean functions with the engineering practice of realizing those functions as optimized hardware.

### Why it exists
Digital logic exists because computation is fundamentally discrete. Unlike analog signals that can take infinitely many values and are corrupted by noise, digital signals at voltage levels representing 0 or 1 tolerate substantial noise margins (typically 30-40% of supply voltage). This robustness enables reliable, mass-producible, energy-efficient hardware at the nanometer scale.

### Problems it solves
- **Binary Decision Making**: Encoding arbitrary Boolean functions using minimal gate networks.
- **Arithmetic Computation**: Addition, subtraction, multiplication, division on signed/unsigned integers and reals.
- **State Retention**: Building memory elements (flip-flops, latches, registers) that store bits over time.
- **Sequence Generation**: Producing controlled sequences (counters, shift registers).
- **Algorithmic Control**: Implementing finite state machines.
- **Data Routing**: Multiplexers/demultiplexers route data based on control signals.
- **Code Translation**: Encoders/decoders convert between binary, BCD, Gray codes.
- **Optimization**: Minimizing literal/gate count to reduce silicon area, power, and delay.

### Industry Use Cases
- **CPU Design**: Built from combinational ALUs, sequential register files, FSM-based control.
- **GPU Shaders**: Parallel arithmetic units for floating-point operations.
- **ASIC/FPGA Design**: Verilog/VHDL express logic at register-transfer level.
- **Cryptography Hardware**: AES, SHA accelerators.
- **Signal Processing**: DSP chips use fixed-point arithmetic.
- **AI Accelerators**: TPU systolic arrays, NPU multiply-accumulate units.

### Analogy
Think of digital logic as the alphabet and grammar of all computation. Boolean algebra allows infinitely many logical expressions from a finite alphabet of variables and operators. A combinational circuit is a static sentence; a sequential circuit is a temporally evolving paragraph. The Karnaugh map is a style guide for more elegant, efficient prose. Floating-point arithmetic is the poetry of numbers.

---

## 2. Core Concepts

### Beginner Concepts

#### Number Systems and Base Conversion

A positional number system with base $b$ represents:
$$N = \sum d_i b^i$$

**Common Bases**:
- Binary (base 2), Octal (base 8; 3 bits/digit), Decimal (base 10), Hexadecimal (base 16; 4 bits/digit)

**Conversion Methods**:
- Decimal to Binary: Repeated division by 2.
- Binary to Octal/Hex: Group bits in 3s (octal) or 4s (hex) from the radix point.

#### Boolean Algebra Fundamentals

Operations on {0, 1}:
- **AND** ($a \cdot b$): both = 1
- **OR** ($a + b$): at least one = 1
- **NOT** ($\bar{a}$): invert

**Axioms**: Closure; Identity ($a+0=a$, $a \cdot 1=a$); Commutativity; Distributivity; Complement ($a+\bar{a}=1$, $a \cdot \bar{a}=0$).

**Derived Theorems**:
- Idempotence: $a+a=a$, $a \cdot a=a$
- Null: $a+1=1$, $a \cdot 0=0$
- Absorption: $a+ab=a$
- De Morgan's: $\overline{a+b}=\bar{a}\bar{b}$, $\overline{ab}=\bar{a}+\bar{b}$
- Consensus: $ab+\bar{a}c+bc=ab+\bar{a}c$

#### Logic Gates

| Gate | Function |
|------|----------|
| AND | $F = A \cdot B$ |
| OR | $F = A + B$ |
| NOT | $F = \bar{A}$ |
| NAND | $F = \overline{AB}$ |
| NOR | $F = \overline{A+B}$ |
| XOR | $F = A \oplus B$ |
| XNOR | $F = \overline{A \oplus B}$ |

XOR properties: $A \oplus A = 0$, $A \oplus \bar{A} = 1$, $A \oplus 0 = A$, $A \oplus 1 = \bar{A}$; multi-input XOR = 1 iff odd # of 1s.

**Universal Gates**: NAND and NOR are functionally complete.

#### Boolean Functions and Canonical Forms

**Minterm** ($m_i$): Product of all variables, complemented if bit i is 0.
**Maxterm** ($M_i$): Sum of all variables, complemented if bit i is 1.

**SOP** (DNF): $f = \sum m_i$ where $f(i) = 1$.
**POS** (CNF): $f = \prod M_i$ where $f(i) = 0$.

### Intermediate Concepts

#### Karnaugh Maps

Visual minimization using Gray code adjacency. Adjacent cells differ in one bit.

**Construction**:
- 2-var: $2 \times 2$
- 3-var: $2 \times 4$ (rows A, columns BC)
- 4-var: $4 \times 4$
- Labels: Gray code (00, 01, 11, 10)
- Wraparound (top-bottom, left-right adjacent)

**Grouping Rules**:
1. Power of 2 cells (1, 2, 4, 8, 16)
2. Rectangular (wraps allowed)
3. Overlap OK; larger better
4. Cover all 1s; don't-cares optional

**Reading**: $2^k$ cells give $n-k$ literals.

#### Quine-McCluskey Method

1. Group minterms by #1s
2. Combine pairs differing in 1 bit (dash for eliminated var); mark used
3. Iterate; survivors are prime implicants (PIs)
4. Build PI chart; find essential PIs
5. Petrick's method for cycles

#### Combinational Circuits

**Half Adder**: $S = A \oplus B$, $C = AB$.

**Full Adder**: $S = A \oplus B \oplus C_{in}$, $C_{out} = AB + (A \oplus B)C_{in}$.

**Ripple Carry Adder**: $n$ cascaded FAs, delay $O(n)$.

**Carry Lookahead Adder**: $G_i = A_iB_i$, $P_i = A_i \oplus B_i$, $C_{i+1} = G_i + P_i C_i$. Delay $O(\log n)$.

**Subtractor**: $A - B = A + \bar{B} + 1$ in 2's complement.

**Multiplier**: $n \times n$ uses $n^2$ AND gates + $n(n-1)$ adders.

**MUX**: $2^n$ inputs, $n$ selects, 1 output.

**DEMUX**: 1 input, $2^n$ outputs, $n$ selects.

**Decoder**: $n$ inputs, $2^n$ outputs (one-hot).

**Encoder**: $2^n$ inputs, $n$ outputs.

**Comparator**: $A_i$ XNOR $B_i$ ANDed = equality.

### Advanced Concepts

#### Sequential Circuits

**Latches**: SR (NOR-based, S=R=1 forbidden), D (level-sensitive).

**Flip-Flops** (edge-triggered):

| FF | $Q^+$ |
|----|-------|
| SR | $S + \bar{R}Q$ ($SR=0$) |
| JK | $J\bar{Q} + \bar{K}Q$ |
| D | $D$ |
| T | $T \oplus Q$ |

**Excitation Table**:
| $Q \to Q^+$ | SR | JK | D | T |
|---|---|---|---|---|
| $0 \to 0$ | $0X$ | $0X$ | $0$ | $0$ |
| $0 \to 1$ | $10$ | $10$ | $1$ | $1$ |
| $1 \to 0$ | $01$ | $01$ | $0$ | $1$ |
| $1 \to 1$ | $X0$ | $X0$ | $1$ | $0$ |

**Race-Around (JK, J=K=1)**: Oscillates when $T_p > t_{pd}$. Solved by master-slave or edge-triggered.

**Shift Registers**: SISO, SIPO, PISO, PIPO; bidirectional; universal.

**Counters**:
- Ripple (async): $T_{i+1}$ clocked by $Q_i$. Modulus $2^n$.
- Synchronous: common clock, $T_i = \prod_{j<i} Q_j$ for binary up.
- Mod-N: reset at $N-1$.
- Ring: single bit circulates, mod $n$.
- Johnson: $\bar{Q}$ fed back, mod $2n$.

**FSMs**: $(S, I, O, \delta, \lambda, s_0)$.
- Mealy: $O = \lambda(s, i)$
- Moore: $O = \lambda(s)$

**State Reduction**: Implication table.
**State Encoding**: Binary, Gray, One-hot.

#### Number Representation

**Unsigned**: $0$ to $2^n - 1$.

**Sign-Magnitude**: MSB = sign; range $\pm(2^{n-1}-1)$; two zeros.

**1's Complement**: Negative = invert; range $\pm(2^{n-1}-1)$; two zeros.

**2's Complement**: Negative = invert + 1; range $-2^{n-1}$ to $+(2^{n-1}-1)$; **one zero**.

**Excess-K**: $V$ stored as $V + K$.

**Overflow Detection (2's complement)**: $V = C_{n-1} \oplus C_n$.

**BCD**: 4 bits/digit; codes 1010-1111 invalid. 8421, Excess-3, 2421, 5211 weighted. Gray code: adjacent differ in 1 bit.

**BCD Add**: Add binary; if > 9 or carry, add 0110.

#### Fixed-Point Arithmetic

**Format $(n, m)$**: $n$ total bits, $m$ integer bits, $n-m$ fractional.
**Range**: $[-2^{m-1}, 2^{m-1} - 2^{-(n-m)}]$.
**Resolution**: $2^{-(n-m)}$.

#### Floating-Point Arithmetic

**IEEE 754 Single**: sign (1), exponent (8, bias 127), mantissa (23, implicit 1).
**Value**: $(-1)^s \times 1.f \times 2^{e-127}$.

**IEEE 754 Double**: sign (1), exponent (11, bias 1023), mantissa (52, implicit 1).

**Special Values**: $e=0, f=0 \to \pm 0$; $e=\text{max}, f=0 \to \pm\infty$; $e=\text{max}, f \ne 0 \to$ NaN; $e=0, f \ne 0 \to$ denormal.

**Machine Epsilon**: Single $2^{-23}$, Double $2^{-52}$.

**Rounding**: Round to nearest even (default), toward zero, $\pm\infty$.

**Pitfalls**: Not associative; $x + (-x)$ may not be 0; cancellation.

**Ops**: Add (align mantissas, add, normalize, round); Mul (add exponents, mul mantissas, normalize, round).

---

## 3. Internal Working

### Boolean Algebra — Theoretical Foundation

Boolean algebra is a complemented distributive lattice. The set {0, 1} with truth-table operations forms the smallest Boolean algebra.

**Functional Completeness**: $\{\cdot, +, \bar{}\}$, $\{\text{NAND}\}$, $\{\text{NOR}\}$ are functionally complete. $\{\text{AND, OR}\}$ alone is NOT.

### CMOS Implementation

- **Inverter**: 1 PMOS + 1 NMOS. Static power ~0. Dynamic $P = \alpha C V_{DD}^2 f$.
- **NAND**: PMOS parallel, NMOS series.
- **NOR**: PMOS series, NMOS parallel.
- **Transmission Gate**: NMOS + PMOS parallel; bidirectional switch.

**Delay**: $t_{PHL}$, $t_{PLH}$; $t_{pd} = (t_{PHL}+t_{PLH})/2$.

### Minimization Theory

**Implicant**: Term implying $f$. **Prime Implicant**: Not subsumed. **Essential PI**: Uniquely covers a minterm.

**Petrick's Method** (cyclic PI chart):
1. Conjunction of PIs per minterm
2. Product of conjunctions
3. Expand to SOP; pick term with minimum literals

### Hazards

- **Static-1 Hazard**: $f = AB + \bar{A}C$; add consensus $BC$.
- **Static-0 Hazard**: Add corresponding term in POS.
- **Dynamic Hazard**: Multiple glitches on one transition.

### Sequential Timing

**Setup $t_{su}$, Hold $t_h$, Clock-to-Q $t_{cq}$**: $f_{max} = 1/(t_{cq} + t_{pd} + t_{su})$.

**Metastability**: Setup/hold violation → may oscillate. Solution: 2-FF synchronizer.

**Clock Skew**: Difference in clock arrival; use H-tree/mesh distribution.

### Counter Implementation

**Sync Binary Up (4-bit)**: $T_0 = 1$; $T_1 = Q_0$; $T_2 = Q_0 Q_1$; $T_3 = Q_0 Q_1 Q_2$.

**Decade (Mod-10)**: Reset when count = 9 (1001).

### FSM Implementation

State register ($k$ FFs) + next-state logic + output logic. Gray encoding minimizes switching; one-hot simplifies decoding.

### FPU Internals

**Addition**: align (shift smaller mantissa by exponent diff), add/sub, normalize, round, special-case check.

**Multiplication**: add exponents (subtract bias), mul mantissas, normalize, round, sign = XOR.

**Subnormals**: Biased exp = 0; use $0.f$ with exponent $1 - \text{bias}$.

**Guard/Round/Sticky Bits**: 3 extra bits for accurate rounding.

---

## 4. Important Terminology

| Term | Definition |
|------|-----------|
| **Boolean Algebra** | Complemented distributive lattice |
| **Minterm** | Product of all variables (per index bits) |
| **Maxterm** | Sum of all variables (per index bits) |
| **Literal** | Variable or complement |
| **Implicant** | Product term implying the function |
| **Prime Implicant** | Implicant not subsumed by any other |
| **Essential PI** | PI covering a minterm uniquely |
| **Don't-Care** | Input that never occurs |
| **K-Map** | Visual minimization grid (Gray code) |
| **Quine-McCluskey** | Tabular algorithmic minimization |
| **Combinational Circuit** | Outputs depend only on current inputs |
| **Sequential Circuit** | Outputs depend on current and past inputs |
| **Latch** | Level-sensitive memory element |
| **Flip-Flop** | Edge-triggered memory element |
| **Race-Around** | JK with $J=K=1$ oscillating when $T_p > t_{pd}$ |
| **Mealy Machine** | Output from state + input |
| **Moore Machine** | Output from state only |
| **Multiplexer** | Routes one of many inputs to one output |
| **Decoder** | $n$ inputs activate one of $2^n$ outputs |
| **Encoder** | $2^n$ inputs to $n$-bit binary output |
| **Adder** | Binary addition circuit |
| **Counter** | Sequential circuit cycling through states |
| **Shift Register** | Cascaded FFs shifting per clock |
| **Ripple Counter** | Async counter with cascaded clocking |
| **Synchronous Counter** | Counter with common clock and combinational next-state |
| **BCD** | Binary-Coded Decimal (4 bits/digit) |
| **2's Complement** | Negation by invert + add 1 |
| **Excess-K** | Biased representation |
| **Overflow** | Result exceeds representable range |
| **Fixed-Point** | Binary point at fixed position |
| **Floating-Point** | Significand x base^exponent |
| **IEEE 754** | Floating-point standard |
| **Mantissa/Significand** | Significant digits of FP |
| **Bias** | Offset added to FP exponent |
| **Denormal** | Subnormal FP with exp = 0 |
| **NaN** | Not-a-Number |
| **Machine Epsilon** | Smallest x with 1+x != 1 in FP |
| **Guard/Round/Sticky** | Extra bits for FP rounding |
| **Setup/Hold Time** | Data stability around clock edge |
| **Metastability** | Unresolved FF output |
| **Clock Skew** | Variation in clock arrival |

---

## 5. Beginner Examples

### Example 1: Base Conversion
Convert $156_{10}$ to binary, octal, hex.

$156 = 10011100_2 = 234_8 = 9C_{16}$.

### Example 2: Boolean Expression Simplification
Simplify $F = AB + A(B+C) + B(B+C)$.

$F = AB + AB + AC + B + BC = B + AC$

### Example 3: Truth Table to Boolean Expression
$f(A,B,C) = 1$ for {000, 010, 101, 111}.

$f = \bar{A}\bar{B}\bar{C} + \bar{A}B\bar{C} + A\bar{B}C + ABC$

### Example 4: Gate Identification
Output 1 only when both inputs are 0. **NOR gate**.

### Example 5: Half Adder with NAND
- $S = A \oplus B$: NAND outputs of $(A,B)$ and $(\bar{A},\bar{B})$ then NANDed.
- $C = \overline{(\overline{AB})(\overline{AB})} = AB$

### Example 6: Verify De Morgan's
Show $\overline{A+B+C} = \bar{A}\bar{B}\bar{C}$.

$\overline{A+(B+C)} = \bar{A}\overline{B+C} = \bar{A}\bar{B}\bar{C}$. ✓

### Example 7: 1's Complement Subtraction
Compute $25 - 18$ in 8-bit 1's complement.

$-18 = 11101101$. $25 + (-18) = 100000110$. Discard end carry: $00000110 = 6$. ✓

---

## 6. Intermediate Examples

### Example 1: K-Map Minimization
$f(A,B,C) = \sum m(0, 1, 2, 4, 6)$, $d(3, 5)$.

Groups: $\bar{A}\bar{C}$ (covers 0,2,6), $\bar{B}\bar{C}$ (covers 0,4 with d5).

$f = \bar{A}\bar{C} + \bar{B}\bar{C}$

### Example 2: Quine-McCluskey Setup
$f(A,B,C,D) = \sum m(0, 1, 2, 5, 6, 7, 8, 9, 10, 14)$.

Group by #1s and combine pairs differing in one bit; iterate to find PIs.

After PI chart analysis, minimal cover: $f = \bar{A}\bar{C}\bar{D} + \bar{A}C\bar{D} + \bar{A}\bar{B}\bar{C}$ (or equivalent).

### Example 3: 4-Bit Ripple Carry Adder
Add $1101_2$ (13) + $0111_2$ (7).

- Stage 0: $1+1+0=0, C_1=1$
- Stage 1: $0+1+1=0, C_2=1$
- Stage 2: $1+1+1=1, C_3=1$
- Stage 3: $1+0+1=0, C_4=1$

Result: $1\,0100_2 = 20$. ✓

### Example 4: 2's Complement Subtraction
$30 - 17$: $-17 = 1110\,1111$. $30 + (-17) = 1\,0000\,1101$. Discard carry: $13$. ✓

### Example 5: 8-to-1 MUX for Parity Function
$f(A,B,C,D) = \sum m(1, 3, 5, 7, 9, 11, 13, 15)$ (odd parity).

With $A,B,C$ as selects, $D$ as data: every $I_i = D$ (since each minterm pair $(2k, 2k+1)$ has $f=0,1$).

### Example 6: Sync Counter Design (Mod-16)
JK FFs: $J_0=K_0=1$; $J_1=K_1=Q_0$; $J_2=K_2=Q_0 Q_1$; $J_3=K_3=Q_0 Q_1 Q_2$.

### Example 7: BCD Addition
$7 + 8$: $0111 + 1000 = 1111$. Since > 9, add 0110: $1111 + 0110 = 1\,0101$. Result: $15$ in BCD. ✓

---

## 7. Advanced Examples

### Example 1: Full Quine-McCluskey
$f(A,B,C,D) = \sum m(0, 1, 2, 5, 6, 7, 8, 9, 10, 14)$, $d(3, 11)$.

**Group by #1s**: 
- G0: 0000 (0)
- G1: 0001 (1), 0010 (2), 1000 (8)
- G2: 0101 (5), 0110 (6), 1001 (9), 1010 (10)
- G3: 0111 (7), 1110 (14)
- DC: 0011 (3), 1011 (11)

**First-level combinations** (pairs differing in 1 bit):
| Combined | Covers |
|---|---|
| 000- | 0,1 |
| 00-0 | 0,2 |
| -000 | 0,8 |
| 00-1 | 1,3 |
| 0-01 | 1,5 |
| -001 | 1,9 |
| 001- | 2,3 |
| 0-10 | 2,6 |
| -010 | 2,10 |
| 100- | 8,9 |
| 10-0 | 8,10 |
| 01-1 | 5,7 |
| -101 | 5,11 |
| 011- | 6,7 |
| -110 | 6,14 |
| 10-1 | 9,11 |
| 101- | 10,11 |
| 1-10 | 10,14 |

**Second-level**:
| Combined | Covers |
|---|---|
| -00- | 0,1,8,9 |
| -0-0 | 0,2,8,10 |
| 0-1- | 2,3,6,7 |
| 0--1 | 1,3,5,7 |
| 10-- | 8,9,10,11 |
| --01 | 1,5,9,13 |
| --10 | 2,6,10,14 |

**Third-level**:
- $-00- + -0-0$: differ in 2 bits
- $-00- + 10--$: differ in 1 bit → $-0--$ (covers 0,1,8,9,10,11)
- 0-1- + 0--1: differ in 2 bits
- $-00-$ already combined with $-0-0$? $-00-$ has B=0, second bit 0; $-0-0$ has B=0, third bit 0. They differ in position 1, so $00-$, $-000$? No, $-00-$ vs $-0-0$ differ in positions: $-00-$ is _00_; $-0-0$ is _0_0. They differ in column 2 only → $-0- -$ would be the combination... wait, they differ in C and D positions both. Let me recompute: $-00- = X00X$ (4 positions: ? B=0 C=0 ?); $-0-0 = X0X0$. Differ in position 1 (column C): -00- has C=0, -0-0 has C=X. So differ in 1 bit position → $-0--$? No wait: $-0-0$ has dash in position 1 (column 2), $-00-$ has dash in positions 0 and 3. Cannot combine these.
- $-0--$: covers 0,1,2,3,8,9,10,11

**Surviving Prime Implicants** (not combined further):
- $-0--$ (B=0, others X): covers 0,1,2,3,8,9,10,11
- $--10$ (C=1, D=0): covers 2,6,10,14
- $0-1-$ (A=0, C=1): covers 2,3,6,7
- $0--1$ (A=0, D=1): covers 1,3,5,7

**PI Chart**:
| PI | 0 | 1 | 2 | 5 | 6 | 7 | 8 | 9 | 10 | 14 |
|---|---|---|---|---|---|---|---|---|----|----|
| $-0--$ | X | X | X |   |   |   | X | X | X  |    |
| $--10$ |   |   | X |   | X |   |   |   | X  | X  |
| $0-1-$ |   |   | X |   | X | X |   |   |    |    |
| $0--1$ |   | X |   | X |   | X |   |   |    |    |

**Essential PIs**:
- $-0--$: only one covering 0, 8, 9 → essential
- $--10$: only one covering 14 → essential
- $0--1$: only one covering 5 → essential

After essentials, all minterms covered. **Minimum SOP**: $f = \bar{B} + C\bar{D} + \bar{A}D$.

### Example 2: IEEE 754 Single Encoding
Encode $-12.625$.

$-12.625 = -1100.101_2 = -1.100101_2 \times 2^3$.

- Sign: 1
- Exponent: $3 + 127 = 130 = 10000010$
- Mantissa: $100101\,0000\,0000\,0000\,0000$

Result: $1\,10000010\,100101\,0000\,0000\,0000\,0000 = 0xC14A0000$.

### Example 3: IEEE 754 Decoding
Decode $0x40E00000$.

$= 0100\,0000\,1110\,0000\,0000\,0000\,0000\,0000_2$

- Sign: 0
- Exponent: $10000001 = 129$, true = 2
- Mantissa: $.110 = 0.75$

Value: $+1.75 \times 4 = 7.0$.

### Example 4: FP Addition
Add $0.5 + 0.4375$ (simplified: 4-bit mantissa, excess-3 exp).

$0.5 = 0.1000 \times 2^{11}$, $0.4375 = 0.0111 \times 2^{11}$.

Sum: $0.1111 \times 2^{11} = 0.9375$. ✓

### Example 5: CLA Equations
4-bit CLA: $C_{i+1} = G_i + P_i C_i$.

$C_1 = G_0 + P_0 C_0$
$C_2 = G_1 + P_1 G_0 + P_1 P_0 C_0$
$C_3 = G_2 + P_2 G_1 + P_2 P_1 G_0 + P_2 P_1 P_0 C_0$
$C_4 = G_3 + P_3 G_2 + P_3 P_2 G_1 + P_3 P_2 P_1 G_0 + P_3 P_2 P_1 P_0 C_0$

$S_i = P_i \oplus C_i$.

### Example 6: Mealy Sequence Detector
Detect "101" with overlap. States: $S_0$ (none), $S_1$ ("1"), $S_2$ ("10").

| Current | X=0 | X=1 |
|---|---|---|
| $S_0$ | $S_0, 0$ | $S_1, 0$ |
| $S_1$ | $S_0, 0$ | $S_1, 0$ |
| $S_2$ | $S_0, 0$ | $S_1, 1$ |

### Example 7: Mod-6 Counter
3 FFs, count 0-5 then reset.

$J_0 = K_0 = 1$; $J_1 = K_1 = \bar{Q_2} Q_0$; $J_2 = K_2 = Q_0$ with sync reset at count 5.

---

## 8. How Interviewers Think

### Red Flags
- Forgetting De Morgan's laws or misapplying them.
- Confusing overflow rules for signed vs unsigned.
- Treating sign-magnitude and 2's complement identically.
- Failing to identify race-around condition.
- Drawing K-maps without Gray code ordering.
- Confusing Mealy vs Moore outputs.
- Using AND-OR instead of NAND-NAND when only NANDs available.
- Confusing exponent bias in IEEE 754 (127 vs 128).
- Thinking denormals and zero are the same.
- Confusing propagation delay with setup time.
- Misapplying XOR to multi-bit operations.

### Green Flags
- Applying De Morgan's law as distributivity of NOT.
- Quick overflow detection using $C_{n-1} \oplus C_n$.
- Recognizing XOR patterns in parity circuits, adders.
- Mapping sequential behavior to FSM diagram first.
- Using state reduction to minimize states.
- Knowing IEEE 754 special values by heart.
- Recognizing mantissa alignment in FP addition.
- Understanding metastability and mitigation.
- Using Gray code for K-maps and shaft encoders.
- Distinguishing latch (level) from flip-flop (edge).

### Answer Matrix

| Question Type | Key Insight | Common Trap | Approach |
|---|---|---|---|
| Simplify Boolean | De Morgan, absorption, consensus | Stop too early | Verify with truth table |
| K-Map | Gray code, wraparound | Missing don't-care | Cover all 1s minimally |
| Quine-McCluskey | Algorithmic | Missing higher-order PIs | Combine until no match |
| Adder Design | Compose from HAs/FAs | Forgetting carry | Compute C_out explicitly |
| FF Design | Use excitation table | Wrong char. equation | K-map of Q^+ |
| FSM Design | Mealy/Moore | Output timing | State diagram first |
| 2's Complement | Invert + 1 | Sign extension | Check MSB for sign |
| Floating-Point | Normalize after op | Forgetting guard/round | Separate mantissa/exp |
| IEEE 754 Decode | Special exp values | Denormal vs zero | Handle special cases first |
| BCD Add | Add 6 if > 9 | Forgetting correction | Check carry and value |

---

## 9. Frequently Asked Interview Questions

### Conceptual (1-10)

1. **Duality Principle**: Interchange AND <-> OR and 0 <-> 1 in a Boolean expression to get its dual. The dual of $a(b + c) = ab + ac$ is $a + bc = (a+b)(a+c)$.

2. **NAND/NOR Universality**: NAND alone (NOR alone) can implement any Boolean function because {NAND} can derive NOT ($x$ NAND $x$), AND (NAND-NAND), OR (NOT-AND via De Morgan).

3. **2's Complement vs 1's Complement**: 2's complement has a single representation of zero (cleaner comparison) and identical addition/subtraction hardware. 1's complement requires end-around carry.

4. **Mealy vs Moore Trade-offs**: Mealy has fewer states (often), but outputs can glitch (asynchronous with input). Moore is glitch-free (output changes only on clock) but may need more states.

5. **Race-Around in JK Flip-Flop**: When $J = K = 1$ and clock pulse width exceeds propagation delay, output toggles repeatedly during the pulse. Master-slave JK or edge-triggered JK resolves this.

6. **IEEE 754 Why Excess-127?**: Biased exponent is unsigned for comparison; the offset $127$ shifts the exponent range so that the smallest exponent ($-126$) is encoded as $1$, leaving $0$ reserved for subnormals/zero and $255$ for Inf/NaN.

7. **Why Floating-Point Is Non-Associative**: Limited precision forces rounding after each operation. Different groupings produce different rounding errors, hence $(a+b)+c$ may differ from $a+(b+c)$.

8. **Carry Lookahead vs Ripple Carry**: CLA computes all carries in parallel using generate/propagate signals, achieving $O(\log n)$ delay vs $O(n)$ for ripple. Trade-off: more hardware (AND-OR logic grows quadratically).

9. **K-Map Wraparound**: Edges of the K-map are considered adjacent because Gray code ensures the last column differs from the first by one bit. This enables wraparound groupings that may not be visually obvious.

10. **Why 2's Complement Wins for Arithmetic**: Sign-magnitude and 1's complement require separate sign handling or end-around carry. 2's complement makes addition the universal arithmetic operation: $A + (\text{2's comp of } B) = A - B$.

### Scenario-Based (11-18)

11. **Design a circuit to detect odd number of 1s in a 4-bit input**: XOR all 4 bits together. $P = I_3 \oplus I_2 \oplus I_1 \oplus I_0$. Tree structure: 3 XOR gates.

12. **Build a 2-bit multiplier using only NAND gates**: $A_1A_0 \times B_1B_0$. Partial products: $P_0 = A_0 B_0$; $P_1 = A_1 B_0 \oplus A_0 B_1$ with carry $C_1 = A_1 B_0 \cdot A_0 B_1$; $P_2 = A_1 B_1 \oplus C_1$; $P_3 = A_1 B_1 \cdot C_1$. Implement each gate via NAND.

13. **Convert 8-bit signed number from 2's complement to BCD (for display)**: Add $0 \times 3333\,3333$ to convert BCD-friendly, then extract decimal digits. Hardware: ripple add + shift logic.

14. **Implement $f(A,B,C) = \sum m(0,3,5,6)$ using 4:1 MUX**: Use $A, B$ as selects, $C, \bar{C}$ as data inputs.
    - $I_0$ (AB=00): $f(00,0)=1, f(00,1)=0$ → $I_0 = \bar{C}$
    - $I_1$ (AB=01): $f(01,0)=0, f(01,1)=1$ → $I_1 = C$
    - $I_2$ (AB=10): unused = 0; for AB=10: $f(10,0)=1, f(10,1)=1$ → $I_2 = 1$
    - $I_3$ (AB=11): $f(11,0)=1, f(11,1)=0$ → $I_3 = \bar{C}$

15. **BCD to 7-segment decoder for common anode display**: For each segment a-g, derive a Boolean function of BCD inputs $A,B,C,D$. Active LOW outputs (since common anode). Use K-maps with don't-cares for 1010-1111.

16. **Design mod-10 counter using JK FFs that counts 0-9 then resets**: Detect 1001 (count = 9), use synchronous reset. Standard implementation: 4 FFs with $T_i$ derived via K-maps over states 0-9 (states 10-15 are don't-cares).

17. **Detect sequence "1101" in a bit stream (Moore)**: 5 states: $S_0$ (none), $S_1$ ("1"), $S_2$ ("11"), $S_3$ ("110"), $S_4$ ("1101" → output 1). On reset, return to $S_0$.

18. **Implement a 4-bit Gray code counter**: Use JK FFs. Gray code transitions toggle only one FF at a time. Toggle equations derived from current state.

### Debugging (19-22)

19. **My 4-bit adder produces wrong results for some inputs**: Check XOR gates (most common failure), verify carry propagation, ensure full adders are properly cascaded. Test with $0111 + 0001$ (max carry chain).

20. **Counter skips states**: Likely a race condition or incorrect toggle signal. Verify clock connections, check for hazards in combinational next-state logic.

21. **FP arithmetic gives unexpected $\pm 0$**: The result is below the smallest normal; check if intermediate computation underflowed. Verify denormal handling or scale inputs.

22. **Combinational circuit has glitches on output**: Static-1 hazard. Add consensus term to SOP. For $f = AB + \bar{A}C$, add $BC$.

### System Design (23-24)

23. **Design a comparator for two 8-bit numbers**: Cascade 8 XNOR gates for equality check + AND all outputs. For magnitude, use 4-bit magnitude comparators in cascade (MSB to LSB priority).

24. **Design a 16-bit ripple-carry vs lookahead adder**: RCA: 16 FAs in series, $O(n)$ delay, simple. CLA: generate/propagate logic, $O(\log n)$ delay, complex. Choose CLA for high-speed CPUs; RCA for low-power ASICs.

### Advanced (25)

25. **Prove ripple carry adder delay is $O(n)$**: Each FA has propagation delay $t_{pd,FA}$. In RCA, carry must propagate through $n$ FAs sequentially: $t_{total} = n \cdot t_{pd,FA}$. Hence $O(n)$ delay.

---

## 10. Common Mistakes

- **Forgetting De Morgan's**: When inverting complex expressions, apply De Morgan's repeatedly. $\overline{ABC} = \bar{A} + \bar{B} + \bar{C}$, NOT $\bar{A}\bar{B}\bar{C}$.
- **K-Map without Gray code**: Cells must be arranged so adjacent cells differ by one bit. Otherwise, the wraparound property breaks.
- **Confusing OR with XOR**: OR returns 1 for any 1 input; XOR returns 1 for exactly one. $A + B \ne A \oplus B$ when $A = B = 1$.
- **Missing don't-cares**: Don't-cares allow simpler expressions; ignoring them leaves minimization incomplete.
- **Boolean algebra equivalence**: $A + B \ne A \cdot B$ (only equal when $A=B$); $A + \bar{A} = 1$, not $A \cdot \bar{A} = 1$.
- **Stop condition in QM**: Combine until no new combinations form; failing to iterate leaves non-prime implicants.
- **Misidentifying essential PIs**: A PI is essential iff it uniquely covers at least one minterm.
- **Confusing latches and flip-flops**: Latches are level-sensitive (transparent while enabled); flip-flops are edge-triggered.
- **Wrong characteristic equation for JK**: $Q^+ = J\bar{Q} + \bar{K}Q$ is correct; using $Q^+ = J + KQ$ is wrong.
- **Sign extension errors**: When extending 2's complement numbers, replicate MSB, not 0. `0101` (5) -> `00000101`, but `1011` (-5) -> `11111011`, not `00001011`.
- **Overflow detection**: $C_{n-1} \oplus C_n$ detects signed overflow; carry-out alone is for unsigned.
- **Excess-K confusion**: Excess-127 means bias = 127, not exponent range [-127, 127]. Stored value = true exponent + 127.
- **Floating-point comparison pitfalls**: $0.1 + 0.2 \ne 0.3$ in floating-point due to binary representation. Use epsilon for comparison.
- **BCD correction omission**: Adding two BCD digits without checking if result > 9 gives wrong answer.
- **Race-around in JK**: Forgetting that $J = K = 1$ with long clock pulse causes oscillation.
- **Setup/hold time**: Data must be stable BEFORE clock edge (setup) and remain stable AFTER (hold).
- **Confusing propagation delay**: $t_{pd}$ is max delay through logic, not the time to propagate to next state register's input.
- **Mod-N counter reset**: Synchronous reset is preferred over asynchronous for clean transitions.

---

## 11. Comparison Tables

### Signed Number Representations

| Aspect | Sign-Magnitude | 1's Complement | 2's Complement | Excess-K |
|--------|----------------|----------------|----------------|----------|
| **Range** | $\pm(2^{n-1}-1)$ | $\pm(2^{n-1}-1)$ | $-2^{n-1}$ to $2^{n-1}-1$ | $-2^{n-1}$ to $2^{n-1}-1$ |
| **Zeros** | Two (+0, -0) | Two | One | One |
| **Negation** | Flip sign bit | Invert all bits | Invert + 1 | Subtract from bias |
| **Subtraction** | Special hardware | End-around carry | Add + negate | Special logic |
| **MSB meaning** | Sign | Sign + magnitude bit | Sign | Bias offset |
| **Hardware** | Complex | Medium | Simple | Special |

### Flip-Flop Comparison

| Aspect | SR | JK | D | T |
|--------|----|----|----|----|
| **Inputs** | S, R | J, K | D | T |
| **$Q^+$** | $S + \bar{R}Q$ | $J\bar{Q} + \bar{K}Q$ | $D$ | $T \oplus Q$ |
| **Toggle mode** | No | $J=K=1$ | No | $T=1$ |
| **Forbidden state** | $S=R=1$ | None | None | None |
| **Memory size** | 2 bits/FF | 2 bits/FF | 1 bit/FF | 1 bit/FF |
| **Use case** | Basic memory | Universal toggle | Data storage | Frequency division |

### Counter Comparison

| Type | Speed | Complexity | Power | Use Case |
|------|-------|-----------|-------|----------|
| **Ripple (Async)** | Slow ($O(n)$) | Low | Low | Simple freq. division |
| **Synchronous** | Fast ($O(1)$ clock) | High | High | General counting |
| **Ring** | Fast | Very low | Low | Sequence generation |
| **Johnson** | Fast | Very low | Low | 2n sequence |

### Adder Comparison

| Type | Delay | Area | Power | Use Case |
|------|-------|------|-------|----------|
| **Ripple Carry** | $O(n)$ | $O(n)$ | Low | Low-power ASIC |
| **Carry Lookahead** | $O(\log n)$ | $O(n \log n)$ | High | High-speed CPU |
| **Carry Select** | $O(\sqrt{n})$ | $O(n)$ | Medium | Moderate speed |
| **Carry Skip** | $O(\sqrt{n})$ | $O(n)$ | Medium | Balance |

### Floating-Point vs Fixed-Point

| Aspect | Fixed-Point | Floating-Point (IEEE 754) |
|--------|-------------|---------------------------|
| **Range** | Limited | Very wide |
| **Precision** | Uniform | Variable (relative) |
| **Hardware** | Integer ALU | Dedicated FPU |
| **Speed** | Faster | Slower |
| **Energy** | Lower | Higher |
| **Determinism** | Deterministic | Rounding non-deterministic |
| **Use Case** | DSP, embedded | Scientific, ML, graphics |

### IEEE 754 Single vs Double

| Aspect | Single | Double |
|--------|--------|--------|
| **Bits** | 32 | 64 |
| **Sign** | 1 | 1 |
| **Exponent** | 8 | 11 |
| **Mantissa** | 23 (+1 implicit) | 52 (+1 implicit) |
| **Bias** | 127 | 1023 |
| **Range** | $\sim 10^{\pm 38}$ | $\sim 10^{\pm 308}$ |
| **Precision** | ~7 decimal digits | ~15 decimal digits |
| **Epsilon** | $1.19 \times 10^{-7}$ | $2.22 \times 10^{-16}$ |

### K-Map vs Quine-McCluskey

| Aspect | K-Map | Quine-McCluskey |
|--------|-------|------------------|
| **Variables** | 2-6 practical | Unlimited |
| **Method** | Visual | Algorithmic |
| **Speed (human)** | Fast for small | Slow but systematic |
| **Computer-friendly** | No | Yes |
| **Don't-cares** | Easy | Easy |
| **Petrick's method** | N/A | Required for cyclic charts |

### Mealy vs Moore FSM

| Aspect | Mealy | Moore |
|--------|-------|-------|
| **Output depends on** | State + Input | State only |
| **States for same problem** | Fewer | More |
| **Output timing** | Asynchronous (with input) | Synchronous (with clock) |
| **Glitches** | Possible | None |
| **Output delay** | 0 cycles | 1 cycle |
| **Conversion** | To Moore: split states | To Mealy: label transitions |

### Latch vs Flip-Flop

| Aspect | Latch | Flip-Flop |
|--------|-------|-----------|
| **Trigger** | Level | Edge |
| **Transparency** | Yes (when enabled) | No |
| **Race-Around** | Yes (in JK) | No |
| **Use** | Simple storage, async logic | Synchronous design |
| **Area** | Smaller | Larger |

---

## 12. Practical Projects

### Beginner Projects
1. **Logic Gate Simulator**: Build a web app that simulates AND/OR/NOT/NAND/NOR/XOR gates with truth tables and waveform visualization.

2. **Boolean Function Minimizer**: Implement Quine-McCluskey in Python; takes minterms and outputs minimal SOP expression with literal count.

3. **Base Converter**: Tool to convert numbers between binary, octal, decimal, hex with arbitrary precision.

4. **Parity Generator/Checker**: 8-bit parity generator using XOR tree, plus parity checker with error LED indicator.

### Intermediate Projects
5. **BCD Arithmetic Unit**: BCD adder, subtractor, multiplier with display on 7-segment LEDs.

6. **4-Bit ALU**: Design a simple ALU supporting ADD, SUB, AND, OR, XOR, with status flags (zero, carry, sign, overflow).

7. **Binary Multiplier**: $n \times n$ array multiplier with optional Wallace tree optimization for $O(\log n)$ delay.

8. **Vending Machine Controller**: FSM with states for accepting coins, dispensing products, returning change.

9. **Traffic Light Controller**: Multi-state FSM sequencing red/yellow/green for 4-way intersection with pedestrian crossings.

10. **Floating-Point Converter**: Convert between IEEE 754 single/double and decimal string representations.

### Advanced Projects
11. **Carry Lookahead Adder**: 16/32/64-bit CLA with generate/propagate logic and benchmarking vs RCA.

12. **RISC-V Subset CPU**: Implement a subset of RISC-V (e.g., RV32I) on FPGA using FSM control + combinational datapath.

13. **IEEE 754 FPU**: Complete floating-point unit with addition, multiplication, division, and square root.

14. **Hardware SHA-256**: Implement SHA-256 compression function in Verilog targeting high throughput.

15. **MIPS Pipeline Simulator**: 5-stage pipeline (IF, ID, EX, MEM, WB) with hazard detection and forwarding in Verilog/SystemVerilog.

---

## 13. Internship Preparation

### Must-Know Concepts
- **Boolean Laws**: De Morgan's, absorption, distributivity, consensus theorem.
- **Gate Universality**: NAND and NOR are functionally complete.
- **K-Map Mastery**: 2/3/4 variables; wraparound groups; don't-cares.
- **Quine-McCluskey**: Prime implicants, essential PIs, Petrick's method for cycles.
- **Combinational Building Blocks**: Half/full adder, MUX, DEMUX, decoder, encoder, comparator.
- **Flip-Flop Types**: SR, JK, D, T with characteristic equations and excitation tables.
- **Counter Design**: Synchronous/ripple, mod-N, up/down.
- **FSM Design**: Mealy vs Moore, state reduction, state encoding.
- **Number Representations**: 2's complement arithmetic, overflow detection, IEEE 754 encoding/decoding.
- **BCD**: Encoding, arithmetic with correction.

### Must-Solve Problem Types
- K-map minimization (2/3/4 variables, with and without don't-cares).
- Full adder from gates; n-bit adder design.
- MUX-based function implementation.
- Flip-flop-based counter design (mod-N, up/down).
- FSM design (sequence detector, vending machine, traffic light).
- 2's complement arithmetic (add, subtract, overflow).
- IEEE 754 encoding/decoding (single and double precision).
- Floating-point arithmetic (add, multiply).

### Common GATE Question Patterns
- **Numerical Answer**: Compute minterms, simplify, give literal count.
- **MCQ on gates**: Identify output of gate network.
- **Assertion-Reason**: "Assertion: $A \oplus B = A + B$ when $AB = 0$. Reason: XOR and OR give same result when inputs cannot be 1 simultaneously."
- **Match the Following**: Match flip-flop types to characteristic equations.
- **Common Data**: Multi-part question on a single function or circuit.

### Time Management Strategy
- **Section 2 (Digital Logic)**: ~10 minutes for 1-mark questions.
- **2-mark questions**: 3-4 minutes each.
- **Skip if stuck**: Mark for review; FSM design and minimization can be time-consuming.
- **Verification**: Check K-map groupings with truth table; check overflow with sign extension.

---

## 14. Cheat Sheet

### Boolean Algebra Identities

| Law | AND Form | OR Form |
|-----|----------|---------|
| Identity | $A \cdot 1 = A$ | $A + 0 = A$ |
| Null | $A \cdot 0 = 0$ | $A + 1 = 1$ |
| Idempotent | $A \cdot A = A$ | $A + A = A$ |
| Complement | $A \cdot \bar{A} = 0$ | $A + \bar{A} = 1$ |
| Involution | $\overline{\bar{A}} = A$ | |
| Commutative | $AB = BA$ | $A+B = B+A$ |
| Associative | $(AB)C = A(BC)$ | $(A+B)+C = A+(B+C)$ |
| Distributive | $A(B+C) = AB + AC$ | $A + BC = (A+B)(A+C)$ |
| Absorption | $A(A+B) = A$ | $A + AB = A$ |
| De Morgan's | $\overline{AB} = \bar{A}+\bar{B}$ | $\overline{A+B} = \bar{A}\bar{B}$ |
| Consensus | $AB + \bar{A}C + BC = AB + \bar{A}C$ | |

### Flip-Flop Quick Reference

| Type | $Q^+$ | Toggle? | Use |
|------|-------|---------|-----|
| SR | $S + \bar{R}Q$ | No | Basic memory |
| JK | $J\bar{Q} + \bar{K}Q$ | Yes ($J=K=1$) | Universal |
| D | $D$ | No | Data register |
| T | $T \oplus Q$ | Yes ($T=1$) | Counter |

### Number Representation Quick Reference

| Representation | $n$-bit Range | Special |
|----------------|---------------|---------|
| Unsigned | $0$ to $2^n - 1$ | — |
| Sign-Magnitude | $\pm(2^{n-1} - 1)$ | Two zeros |
| 1's Comp | $\pm(2^{n-1} - 1)$ | Two zeros |
| 2's Comp | $-2^{n-1}$ to $2^{n-1}-1$ | One zero (standard) |
| Excess-K | $-K$ to $2^n - 1 - K$ | Used in IEEE 754 |

### IEEE 754 Quick Reference

| Format | Sign | Exp | Mantissa | Bias | Total |
|--------|------|-----|----------|------|-------|
| Single | 1 | 8 | 23 | 127 | 32 |
| Double | 1 | 11 | 52 | 1023 | 64 |
| Half | 1 | 5 | 10 | 15 | 16 |

**Special Patterns**:
- $+0$: $0/0/0$
- $-0$: $1/0/0$
- $+\infty$: $0/\text{max}/0$
- $-\infty$: $1/\text{max}/0$
- NaN: $X/\text{max}/\text{nonzero}$
- Denormal: $X/0/\text{nonzero}$

### K-Map Grouping Sizes

| Variables | Max Group Size | Cells Eliminated | Literals Remaining |
|-----------|----------------|------------------|---------------------|
| 2 | 2 | 1 | 1 |
| 3 | 4 | 2 | 1 |
| 4 | 8 | 3 | 1 |
| 5 | 16 | 4 | 1 |
| 6 | 32 | 5 | 1 |

### Adder Delay Comparison

| Type | Delay | Logic Depth |
|------|-------|-------------|
| Ripple Carry | $O(n)$ | $n$ FA delays |
| Carry Lookahead | $O(\log n)$ | $\log_2 n$ |
| Carry Select | $O(\sqrt{n})$ | $\sqrt{n}$ |
| Carry Skip | $O(\sqrt{n})$ | $\sqrt{n}$ |

### FSM Conversion

| From | To | Procedure |
|------|----|----|
| Mealy | Moore | Split each state per unique output |
| Moore | Mealy | Label incoming transitions with state output |

### Key Conversion Formulas

| From | To | Method |
|------|----|----|
| Decimal | Binary | Repeated div by 2 |
| Binary | Hex | Group 4 bits |
| Binary | Octal | Group 3 bits |
| Binary | BCD | Convert each digit |
| 2's comp | Decimal | MSB = sign, invert + 1 for magnitude |
| IEEE 754 | Decimal | Decode sign/exp/mantissa |

---

## 15. One-Day Revision Checklist

### Boolean Algebra
- [ ] State Huntington's postulates
- [ ] Apply De Morgan's laws to complex expressions
- [ ] Use absorption, distributivity, consensus theorems
- [ ] Convert between SOP, POS, canonical forms
- [ ] Identify functionally complete gate sets
- [ ] Verify NAND/NOR universality

### Gates and Combinational
- [ ] Identify all 7 basic gates from symbols/truth tables
- [ ] Derive XOR properties: $A \oplus A = 0$, $A \oplus 0 = A$, etc.
- [ ] Construct half adder from NAND only
- [ ] Build full adder; derive $C_{out} = AB + (A \oplus B)C_{in}$
- [ ] Design $n$-bit ripple carry adder
- [ ] Derive carry lookahead equations
- [ ] Use MUX to implement Boolean function
- [ ] Design decoder-based circuit
- [ ] Build magnitude comparator

### K-Map and Minimization
- [ ] Build K-map with Gray code labels
- [ ] Identify wraparound adjacencies
- [ ] Form largest groups (powers of 2)
- [ ] Use don't-cares to optimize
- [ ] Read off SOP and POS from groupings
- [ ] Explain why larger groups = fewer literals
- [ ] Run Quine-McCluskey algorithm to completion
- [ ] Build PI chart; identify essential PIs
- [ ] Apply Petrick's method for cyclic chart

### Sequential Circuits
- [ ] Distinguish latch (level) vs flip-flop (edge)
- [ ] Derive characteristic equations from K-maps
- [ ] Construct excitation tables
- [ ] Recognize race-around condition
- [ ] Design synchronous binary counter using JK FFs
- [ ] Design mod-N counter with reset logic
- [ ] Build shift register (SISO, SIPO, etc.)
- [ ] Convert between Mealy and Moore FSMs
- [ ] Apply state reduction via implication table
- [ ] Choose state encoding (binary/Gray/one-hot)

### Number Systems
- [ ] Convert between binary/octal/hex/decimal
- [ ] Perform BCD addition with correction
- [ ] Verify 2's complement overflow detection: $V = C_{n-1} \oplus C_n$
- [ ] Convert between sign-magnitude, 1's comp, 2's comp
- [ ] Apply excess-K bias: stored = value + K
- [ ] Compute fixed-point arithmetic

### IEEE 754 Floating-Point
- [ ] Encode decimal in single precision (sign, biased exp, mantissa)
- [ ] Decode IEEE 754 bit pattern to decimal
- [ ] Identify special values (0, Inf, NaN, denormal)
- [ ] Compute machine epsilon (single: $2^{-23}$, double: $2^{-52}$)
- [ ] Add/subtract two FP numbers (align, add, round, normalize)
- [ ] Multiply two FP numbers (add exp, mul mantissa, normalize)
- [ ] Explain why FP arithmetic is not associative
- [ ] Identify when denormal is used

### Hazards and Timing
- [ ] Identify static-1, static-0, dynamic hazards
- [ ] Add consensus terms to remove hazards
- [ ] Compute $f_{max} = 1/(t_{cq} + t_{pd} + t_{su})$
- [ ] Understand setup/hold time requirements
- [ ] Explain metastability and synchronizer chains

### Final Review
- [ ] Review all comparison tables
- [ ] Memorize IEEE 754 format (single/double)
- [ ] Practice 2-3 problems from each section
- [ ] Review common mistakes list
- [ ] Verify understanding of theorem statements
- [ ] Check time management strategy
- [ ] Get good sleep before exam!