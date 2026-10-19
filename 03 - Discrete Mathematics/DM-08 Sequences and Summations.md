---
title: "Sequences and Summations"
aliases:
  - Sigma notation
  - Arithmetic and geometric series
  - Summation formulas
module: "Discrete Mathematics"
module_code: "GST06106"
topic_id: "DM-08"
type: "lesson"
unit: "U3 Structures"
difficulty: "intermediate"
syllabus_status: "provisional-core"
status: "not-started"
mastery: 0
prerequisites:
  - "[[DM-07 Functions]]"
next: "[[DM-09 Mathematical Induction]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - discrete-math
  - sequences
---

# DM-08 Sequences and Summations

> [!info] Topic card
> **Unit:** U3 · **Time:** 4 h · **CS link:** counting loop iterations ([[PY-05 Loops and Iteration]], [[PY-12 Searching, Sorting and Complexity]])

## 1. Learning objectives
1. **Define** sequences (as functions on ℕ), and **write** explicit and recursive formulas for arithmetic and geometric sequences.
2. **Read and write** Σ (and Π) notation, including changing the index and splitting sums.
3. **Apply** the standard closed forms: $\sum i$, $\sum i^2$, $\sum i^3$, geometric series, and telescoping sums.
4. **Evaluate** double sums, and **translate** nested loops into sums to count their operations.
5. **Recognise** a sequence from its first terms, and **justify** a guess (which you'll prove by induction in DM-09).

## 2. Why it matters
"How many times does this loop body run?" is a summation. "How many nodes in a full binary tree of height h?" is a geometric series. Interest, depreciation and exponential growth in project budgets are geometric too ([[PM-09 Cost Estimation and Budgeting]]). Summations are the arithmetic of algorithm analysis.

## 3. Prerequisites
[[DM-07 Functions]] (a sequence is a function $a:\mathbb{N}\to\mathbb{R}$), and school algebra.

## 4. Intuition
A sequence is a **numbered list** $a_0, a_1, a_2, \dots$. Σ is a **loop written in mathematics**: $\sum_{i=1}^{n} f(i)$ is exactly `total = 0; for i in range(1, n+1): total += f(i)`.

## 5. Rigorous explanation

### 5.1 Sequences
- **Arithmetic:** a constant difference $d$. Explicit form $a_n = a_0 + nd$, recursive form $a_n = a_{n-1} + d$.
- **Geometric:** a constant ratio $r$. Explicit form $a_n = a_0 r^n$, recursive form $a_n = r\,a_{n-1}$.
- **Recursive (recurrence) definitions** give the first term(s) plus a rule. Solving them is [[DM-14 Recurrence Relations]].

### 5.2 Σ notation, symbol by symbol
$$\sum_{i=m}^{n} a_i = a_m + a_{m+1} + \dots + a_n$$
- $i$ is the **index** (a dummy variable: any letter works). $m$ is the lower limit and $n$ the upper limit, both **inclusive**. There are $n - m + 1$ terms.
- If $n < m$, the sum is **empty** and equals 0. (The empty product $\prod$ equals 1.)

**Rules**
| Rule | Formula |
|---|---|
| Linearity | $\sum (c\,a_i + b_i) = c\sum a_i + \sum b_i$ |
| Constant | $\sum_{i=1}^{n} c = cn$ |
| Splitting | $\sum_{i=1}^{n} a_i = \sum_{i=1}^{k} a_i + \sum_{i=k+1}^{n} a_i$ |
| Index shift | $\sum_{i=1}^{n} a_i = \sum_{j=0}^{n-1} a_{j+1}$ (substitute $j = i - 1$) |
| Telescoping | $\sum_{i=1}^{n}(a_i - a_{i-1}) = a_n - a_0$ |
| ⚠ Not valid | $\sum a_i b_i \ne (\sum a_i)(\sum b_i)$ in general |

### 5.3 Closed forms (memorise them)
| Sum | Closed form | Growth |
|---|---|---|
| $\sum_{i=1}^{n} i$ | $\dfrac{n(n+1)}{2}$ | $\Theta(n^2)$ |
| $\sum_{i=1}^{n} i^2$ | $\dfrac{n(n+1)(2n+1)}{6}$ | $\Theta(n^3)$ |
| $\sum_{i=1}^{n} i^3$ | $\left(\dfrac{n(n+1)}{2}\right)^2$ | $\Theta(n^4)$ |
| $\sum_{i=0}^{n} r^i$ ($r\ne1$) | $\dfrac{r^{n+1}-1}{r-1}$ | $\Theta(r^n)$ for $r > 1$ |
| $\sum_{i=0}^{\infty} r^i$ ($\lvert r\rvert<1$) | $\dfrac{1}{1-r}$ | |
| $\sum_{i=1}^{n} \frac{1}{i}$ (harmonic $H_n$) | no closed form, $\approx \ln n + 0.577$ | $\Theta(\log n)$ |

**Derivation of the geometric sum.** Let $S = 1 + r + \dots + r^n$. Then $rS = r + r^2 + \dots + r^{n+1}$. Subtracting, $rS - S = r^{n+1} - 1$, so $S = \frac{r^{n+1}-1}{r-1}$ (for $r\ne1$).

**Gauss's derivation of $\sum i$.** Write the sum forwards and backwards and add them: each column sums to $n+1$, there are $n$ columns, so $2S = n(n+1)$.

### 5.4 Double sums
$\sum_{i=1}^{n}\sum_{j=1}^{m} a_{ij}$: do the inner sum first (for a fixed $i$). When the inner limit depends on the outer index, like $\sum_{i=1}^{n}\sum_{j=1}^{i} 1 = \sum_{i=1}^{n} i$, you have a triangular loop.

## 6. Terminology
| Term | Meaning |
|---|---|
| Term | One element $a_n$ |
| Explicit (closed) formula | $a_n$ as a direct function of n |
| Recursive formula | $a_n$ in terms of earlier terms |
| Series / partial sum | A sum of terms / the sum of the first n terms |
| Telescoping | Consecutive terms cancel |
| Closed form | A formula without Σ or "…" |

## 7. Step-by-step: count the operations of a nested loop
```python
count = 0
for i in range(1, n + 1):        # i = 1..n
    for j in range(i, n + 1):    # j = i..n  →  n - i + 1 iterations
        count += 1
```
1. Inner iterations for a fixed $i$: $n - i + 1$.
2. Total: $\sum_{i=1}^{n}(n - i + 1)$.
3. Substitute $k = n - i + 1$ (as $i$ goes $1 \to n$, $k$ goes $n \to 1$): $\sum_{k=1}^{n} k = \frac{n(n+1)}{2}$.
4. Check with $n = 3$: (3 + 2 + 1) = 6 = 3·4/2 ✔. The cost is $\Theta(n^2)$.

## 8. Diagram: Gauss's pairing for n = 6
```text
  1   2   3   4   5   6
+ 6   5   4   3   2   1
= 7   7   7   7   7   7   → 2S = 6·7 = 42 → S = 21
```
*Writing the sum twice in opposite orders makes every column sum to n + 1, which is the idea behind the formula.*

## 9. Worked examples

### Example 1 (basic): evaluate sums
(a) $\sum_{i=1}^{5}(2i + 1) = 2\sum i + \sum 1 = 2\cdot15 + 5 = 35$. Check: 3 + 5 + 7 + 9 + 11 = 35 ✔.
(b) $\sum_{k=0}^{4} 3\cdot 2^k = 3\cdot\frac{2^5 - 1}{2 - 1} = 3\cdot31 = 93$.
(c) $\sum_{i=3}^{2} i = 0$ (an empty sum).

### Example 2 (intermediate): a sum not starting at 1
$\sum_{i=10}^{20} i = \sum_{i=1}^{20} i - \sum_{i=1}^{9} i = 210 - 45 = 165$.
(It has 11 terms with average $(10+20)/2 = 15$, giving $11 \cdot 15 = 165$ ✔. In general, an arithmetic series equals the number of terms × the average of the first and last terms.)

### Example 3 (challenging): telescoping
$\sum_{i=1}^{n}\frac{1}{i(i+1)}$. Partial fractions: $\frac{1}{i(i+1)} = \frac{1}{i} - \frac{1}{i+1}$. The sum telescopes:
$\left(1 - \tfrac12\right) + \left(\tfrac12 - \tfrac13\right) + \dots + \left(\tfrac1n - \tfrac1{n+1}\right) = 1 - \frac{1}{n+1} = \frac{n}{n+1}$.
For $n = 4$: $\frac12 + \frac16 + \frac1{12} + \frac1{20} = \frac{30+10+5+3}{60} = \frac{48}{60} = \frac45$ ✔.

### Example 4 (CS): nodes in a complete binary tree
Levels $0..h$, with $2^k$ nodes at level $k$. The total is $\sum_{k=0}^{h} 2^k = 2^{h+1} - 1$. With $n$ nodes, $h \approx \log_2 n$, which is why balanced-tree operations are $O(\log n)$ ([[PY-21 Data Structures and Algorithm Design]]). *The last level holds about half of all the nodes*, a property used in the analysis of heaps.

## 10. Application: loan repayment (geometric series)
A student saves 50 000 TZS at the start of each month, in an account paying 1% per month. After 12 months, the deposit made at month $k$ has grown for $12 - k + 1$ months: $\text{total} = 50000\sum_{j=1}^{12}1.01^j = 50000\cdot1.01\cdot\frac{1.01^{12}-1}{0.01} \approx 640\,466$ TZS. Geometric sums appear wherever compounding does: interest, population growth, and repeated doubling in algorithms. (The interest rate is illustrative.)

## 11. Common mistakes
| Mistake | Correct |
|---|---|
| Counting $n - m$ terms in $\sum_{i=m}^n$ | $n - m + 1$ terms (both limits inclusive) |
| $\sum_{i=1}^{n} c = c$ | $cn$ |
| $\sum a_ib_i = (\sum a_i)(\sum b_i)$ | False in general |
| Geometric sum $\frac{r^n-1}{r-1}$ for $\sum_{i=0}^{n}$ | The exponent is $n+1$ when the sum runs from 0 to n |
| Python `range(m, n)` vs $\sum_{i=m}^{n}$ | `range` excludes n, so use `range(m, n + 1)` |
| Assuming a pattern from 3 terms | 1, 2, 4 could continue 8 or 7 (and others), so prove it (DM-09) |

## 12. Comparison
| Sequence | Recursive | Explicit | Sum of the first n+1 terms |
|---|---|---|---|
| Arithmetic | $a_n = a_{n-1} + d$ | $a_0 + nd$ | $(n+1)a_0 + d\frac{n(n+1)}{2}$ |
| Geometric | $a_n = r a_{n-1}$ | $a_0 r^n$ | $a_0\frac{r^{n+1}-1}{r-1}$ |
| Fibonacci | $F_n = F_{n-1}+F_{n-2}$ | Binet's formula ([[DM-14 Recurrence Relations]]) | $F_{n+2} - 1$ (from $F_0$ to $F_n$) |

## 13. Practice
**L1** 1. Write the first five terms of $a_n = 3 \cdot 2^n$ and of $b_n = b_{n-1} + 4$ with $b_0 = 1$. 2. How many terms does $\sum_{i=-2}^{7}$ have?

**L2** 3. Evaluate $\sum_{i=1}^{100} i$, $\sum_{i=1}^{10} i^2$, and $\sum_{k=0}^{9} 2^k$. 4. Write $1 + 4 + 7 + \dots + 97$ in Σ notation and evaluate it.

**L3** 5. Evaluate $\sum_{i=1}^{n}(6i^2 - 2i)$ in closed form. 6. Use telescoping to evaluate $\sum_{i=1}^{n}\left((i+1)^2 - i^2\right)$, and so derive $\sum_{i=1}^{n}(2i + 1)$.

**L4** 7. Count the exact number of times `x += 1` runs, as a closed form in $n$:
```python
for i in range(n):
    for j in range(i):
        for k in range(j):
            x += 1
```
8. Find $\sum_{i=1}^{n}\sum_{j=1}^{n}(i + j)$.

**L5** 9. An exponential back-off retry policy waits $0.5, 1, 2, 4, \dots$ seconds ([[PY-15 Exceptions and Defensive Programming]]). (a) What is the total waiting time for $k$ retries? (b) What is the smallest $k$ for which the total exceeds 10 minutes? (c) Argue why production systems cap the delay, and recompute (a) with a cap of 30 s per wait.

## 14. Hints
> [!tip]- Hints
> 4: the terms are $1 + 3k$ for $k = 0..32$. 5: linearity with the closed forms. 7: the innermost loop runs $j$ times, so the total is $\sum_{i}\sum_{j<i} j = \sum_i \binom{i}{2}$, which equals $\binom{n}{3}$. 8: split into $\sum\sum i + \sum\sum j$. 9: geometric with ratio 2, first term 0.5.

## 15. Worked solutions
> [!success]- Solutions 1–2
> 1. 3, 6, 12, 24, 48. And 1, 5, 9, 13, 17. 2. $7 - (-2) + 1 = 10$.

> [!success]- Solution 3
> $\frac{100\cdot101}{2} = 5050$. $\frac{10\cdot11\cdot21}{6} = 385$. $\frac{2^{10}-1}{1} = 1023$.

> [!success]- Solution 4
> $\sum_{k=0}^{32}(1 + 3k)$: 33 terms (since $1 + 3\cdot32 = 97$). The sum is $33 + 3\cdot\frac{32\cdot33}{2} = 33 + 1584 = 1617$. Check: the average $(1 + 97)/2 = 49$, and $49 \cdot 33 = 1617$ ✔.

> [!success]- Solution 5
> $6\cdot\frac{n(n+1)(2n+1)}{6} - 2\cdot\frac{n(n+1)}{2} = n(n+1)(2n+1) - n(n+1) = n(n+1)\cdot2n = 2n^2(n+1)$. Check n = 1: $6 - 2 = 4 = 2\cdot1\cdot2$ ✔.

> [!success]- Solution 6
> Telescoping: $(n+1)^2 - 1^2 = n^2 + 2n$. But $(i+1)^2 - i^2 = 2i + 1$, so $\sum_{i=1}^{n}(2i+1) = n^2 + 2n$. Check n = 2: 3 + 5 = 8 = 4 + 4 ✔.

> [!success]- Solution 7
> The innermost loop runs $j$ times, so the total is $T = \sum_{i=0}^{n-1}\sum_{j=0}^{i-1} j = \sum_{i=0}^{n-1}\frac{i(i-1)}{2} = \sum_{i=0}^{n-1}\binom{i}{2} = \binom{n}{3} = \frac{n(n-1)(n-2)}{6}$ (the hockey-stick identity, [[DM-13 Binomial Theorem and Pascal's Triangle]]). The intuition: each increment corresponds to choosing three distinct indices $k < j < i$ from $0..n-1$. For n = 4 that's 4 ✔ (verified in the toolkit tests).

> [!success]- Solution 8
> $\sum_i\sum_j i = \sum_i n\cdot i = n\cdot\frac{n(n+1)}{2}$, and by symmetry the $j$ part is the same. The total is $n^2(n+1)$.

> [!success]- Solution 9
> (a) $\sum_{i=0}^{k-1} 0.5\cdot2^i = 0.5(2^k - 1)$ seconds. (b) We need $0.5(2^k - 1) > 600$, i.e. $2^k > 1201$, so $k = 11$ ($2^{11} = 2048$ gives 1023.5 s; $k = 10$ gives 511.5 s). (c) Uncapped, a single wait quickly becomes absurd (the 11th wait alone is 512 s), and users or upstream timeouts give up first. With a 30 s cap, the waits are 0.5, 1, 2, 4, 8, 16, 30, 30, … For $k \ge 6$ the total is $31.5 + 30(k - 6)$ seconds: **linear** growth after the cap.

## 16. Self-test (pass ≥ 4/5)
1. $\sum_{i=1}^{n} i$ = ? 2. $\sum_{i=0}^{n} 2^i$ = ? 3. How many terms in $\sum_{i=5}^{12}$? 4. What is an empty sum? 5. Θ-growth of $\sum_{i=1}^{n} i^2$?
> [!success]- Answers
> 1. $n(n+1)/2$. 2. $2^{n+1} - 1$. 3. 8. 4. 0. 5. $\Theta(n^3)$.

## 17. Flashcards
#flashcards/discrete-math
Sum 1 + 2 + … + n?::n(n+1)/2
Sum of squares 1² + … + n²?::n(n+1)(2n+1)/6
Geometric sum Σ_{i=0}^{n} rⁱ (r ≠ 1)?::(r^{n+1} − 1)/(r − 1)
Number of terms in Σ_{i=m}^{n}?::n − m + 1
Telescoping sum Σ (a_i − a_{i−1}) from i=1 to n?::a_n − a_0
Infinite geometric sum, |r| < 1?::1/(1 − r)

## 18. Blank-page recall
Derive the geometric-sum formula and Gauss's formula from scratch, and count the iterations of a triangular double loop.

## 19. Revision summary
- Sequences: arithmetic (+d), geometric (×r), recursive.
- Σ is a loop: limits are inclusive, there are $n - m + 1$ terms, and the empty sum is 0.
- Use the closed forms, linearity, splitting, index shifts and telescoping.
- Nested loops become double sums, which give the cost.

## 20. Links
Prev: [[DM-07 Functions]] · Next: [[DM-09 Mathematical Induction]] (proves these formulas) · Applied: [[PY-05 Loops and Iteration]], [[PY-12 Searching, Sorting and Complexity]], [[DM-14 Recurrence Relations]]

## 21. Sources
- Rosen (2019), §2.4 "Sequences and Summations" (table of useful summation formulas).
- Graham, R. L., Knuth, D. E. & Patashnik, O., *Concrete Mathematics*, 2nd ed., Addison-Wesley, 1994, ch. 2 (sums).

## 22. Mastery checklist
- [ ] I recall all the closed forms in §5.3
- [ ] I converted three nested loops into sums and closed forms correctly
- [ ] Practice 9 done · reviews scheduled
