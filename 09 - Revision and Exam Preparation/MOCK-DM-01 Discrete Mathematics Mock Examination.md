---
title: "Discrete Mathematics Mock Examination"
module: "Discrete Mathematics"
module_code: "GST06106"
topic_id: "MOCK-DM-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - discrete-math
  - exam
---

# MOCK-DM-01 Discrete Mathematics Mock Examination

> [!warning] A designed practice paper
> This is **not** a past paper; the format (3 hours, 100 marks, answer all eight questions) is designed. Check the real format with your lecturer. Every numerical answer in the marking guide is computed in `09 - Revision and Exam Preparation/code/tests/test_mock_dm.py`.

**Instructions (designed):** 3 hours. Answer **all** questions. Show all working; justify every step of a proof. A basic calculator is assumed to be allowed (check your real exam's rules).

**Covers:** [[DM 01 Curriculum Map]], DM-01 to DM-18.

---

**Q1 Logic (12 marks).**
(a) Use a truth table to show that $\lnot(p \to q) \equiv p \land \lnot q$. *(4)*
(b) Show, using laws of logic (not a truth table), that $(p \to q) \land (q \to r) \to (p \to r)$ is a tautology, or verify it with a truth table and name the rule of inference it represents. *(4)*
(c) Let $S(x, y)$ mean "student $x$ has submitted assignment $y$". Write in symbols, then negate and simplify so that no $\lnot$ stands in front of a quantifier: "Every student has submitted at least one assignment." *(4)*

**Q2 Sets and relations (14 marks).**
(a) In a class of 120 students, 70 take Python, 50 take DM and 40 take CS; 25 take Python and DM, 20 Python and CS, 15 DM and CS, and 10 take all three. How many take at least one? How many take none? *(5)*
(b) On $A = \{1, 2, 3, 4\}$, let $R = \{(1,1),(2,2),(3,3),(4,4),(1,2),(2,1),(3,4),(4,3)\}$. Determine whether $R$ is reflexive, symmetric and transitive. If it is an equivalence relation, list its equivalence classes. *(6)*
(c) Is $f: \mathbb{Z} \to \mathbb{Z}$, $f(n) = 2n + 3$ injective? Surjective? Justify. *(3)*

**Q3 Proof (12 marks).**
(a) Prove by mathematical induction that $\sum_{i=1}^{n} (2i - 1) = n^2$ for all $n \ge 1$. *(6)*
(b) Prove by contrapositive: for integers $n$, if $n^2$ is even then $n$ is even. *(6)*

**Q4 Counting (14 marks).**
(a) A committee of 4 is chosen from 10 students, 4 of whom are women. How many committees are possible? How many include at least one woman? Compute the second number in two different ways. *(6)*
(b) How many codes consist of 2 letters (A–Z) followed by 4 digits, with repetition allowed? *(2)*
(c) How many ways can 3 different prizes be given to 8 students, at most one prize each? *(2)*
(d) How many distinct arrangements are there of the letters of LEVEL? *(2)*
(e) 30 students' birthdays fall in 12 months. Show that at least 3 share a birth month. *(2)*

**Q5 Binomial theorem and recurrences (12 marks).**
(a) Find the coefficient of $x^3$ in $(2x - 1)^5$. *(4)*
(b) Solve $a_n = 3a_{n-1} - 2a_{n-2}$ with $a_0 = 2$, $a_1 = 3$, and check your formula for $n = 2, 3$. *(8)*

**Q6 Graphs and trees (14 marks).** A weighted undirected graph has edges A–B 4, A–C 2, B–C 1, B–D 5, C–D 8, C–E 10, D–E 2.
(a) Use Dijkstra's algorithm from A, showing the table at each step. Give the shortest path and distance to E. *(6)*
(b) Find a minimum spanning tree using Kruskal's algorithm, and its total weight. *(5)*
(c) A simple graph has degree sequence 3, 3, 2, 2, 2. How many edges does it have? Does it have an Euler circuit? An Euler path? *(3)*

**Q7 Boolean algebra (10 marks).**
(a) Simplify $F = xy + x\bar{y} + \bar{x}y$ using Boolean laws, naming each law. *(5)*
(b) Draw a logic circuit for the simplified expression, and give its truth table. *(5)*

**Q8 Probability (12 marks).**
(a) A fair die is rolled 4 times. Find the probability of at least one 6. *(4)*
(b) A screening test for a condition with 2% prevalence detects 95% of cases, and gives a positive result for 10% of people without the condition. Find the probability that a person who tests positive has the condition. Comment on the result. *(8)*

---

## Marking guide

> [!success]- Q1
> (a) Truth table over $(p, q)$: $\lnot(p \to q)$ is T only for $(T, F)$; so is $p \land \lnot q$. Identical columns → equivalent. *(4: table 3, conclusion 1.)*
> (b) Using $a \to b \equiv \lnot a \lor b$: $\lnot[(\lnot p \lor q) \land (\lnot q \lor r)] \lor (\lnot p \lor r)$ ≡ (De Morgan) $(p \land \lnot q) \lor (q \land \lnot r) \lor \lnot p \lor r$. Now $(p \land \lnot q) \lor \lnot p \equiv \lnot q \lor \lnot p$ and $(q \land \lnot r) \lor r \equiv q \lor r$, giving $\lnot q \lor \lnot p \lor q \lor r$, which contains $\lnot q \lor q \equiv T$. A truth table (all 8 rows true) is also accepted. The rule is **hypothetical syllogism**. *(4.)*
> (c) $\forall x\, \exists y\, S(x, y)$. Negation: $\exists x\, \forall y\, \lnot S(x, y)$: "some student has submitted no assignment". *(2 + 2.)*

> [!success]- Q2
> (a) $|P \cup D \cup C| = 70 + 50 + 40 - 25 - 20 - 15 + 10 =$ **110**; none = 120 − 110 = **10**. *(5.)*
> (b) Reflexive (all $(a, a)$ present); symmetric (each pair's reverse is present); transitive (check, e.g. $(1,2),(2,1) \Rightarrow (1,1)$ ✓; no chain leaves $\{1,2\}$ or $\{3,4\}$). An equivalence relation with classes **{1, 2}** and **{3, 4}**. *(2 + 2 + 2.)*
> (c) Injective: $2a + 3 = 2b + 3 \Rightarrow a = b$. Not surjective: $2n + 3$ is always odd, so e.g. 4 has no preimage. *(3.)*

> [!success]- Q3
> (a) Base $n = 1$: $1 = 1^2$ ✓. Hypothesis: $\sum_{i=1}^{k}(2i - 1) = k^2$. Step: $\sum_{i=1}^{k+1}(2i - 1) = k^2 + 2(k + 1) - 1 = k^2 + 2k + 1 = (k + 1)^2$ ✓. By induction it holds for all $n \ge 1$. *(Base 1, hypothesis 1, step 3, conclusion 1.)*
> (b) Contrapositive: if $n$ is odd then $n^2$ is odd. Let $n = 2k + 1$; $n^2 = 4k^2 + 4k + 1 = 2(2k^2 + 2k) + 1$, odd. Since the contrapositive is equivalent to the original, the statement holds. *(6.)*

> [!success]- Q4
> (a) $\binom{10}{4} =$ **210**. At least one woman: complement $210 - \binom{6}{4} = 210 - 15 =$ **195**; directly $\binom41\binom63 + \binom42\binom62 + \binom43\binom61 + \binom44 = 80 + 90 + 24 + 1 = 195$ ✓. *(2 + 2 + 2.)*
> (b) $26^2 \times 10^4 =$ **6,760,000**. (c) $P(8, 3) = 8 \cdot 7 \cdot 6 =$ **336**. (d) $\frac{5!}{2!\,2!} =$ **30** (L and E each appear twice). (e) If each month had at most 2, there would be at most 24 students; 30 > 24, so some month has at least $\lceil 30/12 \rceil = 3$ (pigeonhole). *(2 each.)*

> [!success]- Q5
> (a) Term $\binom{5}{k}(2x)^k(-1)^{5-k}$ with $k = 3$: $\binom53 \cdot 8 \cdot (-1)^2 = 10 \cdot 8 =$ **80**. *(4.)*
> (b) Characteristic equation $r^2 - 3r + 2 = 0 \Rightarrow r = 1, 2$; $a_n = A + B\,2^n$. $a_0: A + B = 2$; $a_1: A + 2B = 3$ ⇒ $B = 1, A = 1$. So $a_n = 1 + 2^n$. Check: $a_2 = 3 \cdot 3 - 2 \cdot 2 = 5 = 1 + 4$ ✓; $a_3 = 3 \cdot 5 - 2 \cdot 3 = 9 = 1 + 8$ ✓. *(Equation 2, roots 1, general form 1, constants 2, checks 2.)*

> [!success]- Q6
> (a) Start A: 0. Visit A → C 2, B 4. Visit C (2) → B via C = 3 (better), D = 10, E = 12. Visit B (3) → D via B = 8 (better). Visit D (8) → E via D = 10 (better). Visit E (10). **Distances:** B 3, C 2, D 8, E 10. **Path to E:** A–C–B–D–E, length **10**. *(Table 4, path and distance 2.)*
> (b) Sorted: B–C 1, A–C 2, D–E 2, A–B 4, B–D 5, C–D 8, C–E 10. Take B–C, A–C, D–E; skip A–B (it would form a cycle A–B–C); take B–D. Edges {B–C, A–C, D–E, B–D}, total **10**. *(5.)*
> (c) Edges = (3 + 3 + 2 + 2 + 2)/2 = **6**. Two vertices have odd degree, so there's **no Euler circuit**, but an **Euler path** exists if the graph is connected (between the two odd vertices). *(3.)*

> [!success]- Q7
> (a) $xy + x\bar y = x(y + \bar y)$ (distributive) $= x \cdot 1$ (complement) $= x$ (identity). Then $x + \bar x y = (x + \bar x)(x + y)$ (distributive) $= 1 \cdot (x + y) = x + y$. **F = x + y.** *(5.)*
> (b) One OR gate with inputs $x, y$. Truth table: 00 → 0, 01 → 1, 10 → 1, 11 → 1 (matches the original expression in every row). *(5.)*

> [!success]- Q8
> (a) $1 - (5/6)^4 = 1 - 625/1296 = 671/1296 \approx$ **0.518**. *(4.)*
> (b) $P(C \mid +) = \dfrac{0.02 \times 0.95}{0.02 \times 0.95 + 0.98 \times 0.10} = \dfrac{0.019}{0.117} \approx$ **0.162**. Only about 16% of positives have the condition: with low prevalence, false positives outnumber true positives. A positive result should lead to a confirmatory test, not a diagnosis. *(Formula 3, value 3, comment 2.)*

**Self-assessment (designed):** ≥ 70 strong; 50–69 secure; < 50 on any question → that topic goes to [[Weak Area Tracker]].

Back to [[Exam Technique and Assessment Strategy]] · [[QB-DM Discrete Mathematics Question Bank]] · [[DM 00 Dashboard]]
