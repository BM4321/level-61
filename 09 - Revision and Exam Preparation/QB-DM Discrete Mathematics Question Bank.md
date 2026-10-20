---
title: "Discrete Mathematics Question Bank"
module: "Discrete Mathematics"
module_code: "GST06106"
topic_id: "QB-DM"
type: "question-bank"
tags:
  - semester-6
  - discrete-math
  - exam
---

# QB-DM Discrete Mathematics Question Bank

> [!info] How to use
> Two questions per lesson, at the level shown. Answer closed book, then open the folded answer. Every numerical answer is recomputed in `09 - Revision and Exam Preparation/code/tests/test_qb.py` (`test_qb_dm_numbers`). Log misses in [[Mistake Log]].

## [[DM-01 Propositions, Connectives and Truth Tables]]

**Q1 (L1).** How many rows does a truth table for 4 propositional variables have?

> [!success]- Answer
> $2^4 = 16$.

**Q2 (L2).** When is $p \to q$ false? Translate "you pass only if you submit the project" with $p$ = pass, $q$ = submit.

> [!success]- Answer
> Only when $p$ is true and $q$ is false. "Pass only if submit" is $p \to q$.

## [[DM-02 Logical Equivalence and Laws of Logic]]

**Q3 (L2).** Is $p \to q$ equivalent to its contrapositive $\lnot q \to \lnot p$? To its converse $q \to p$?

> [!success]- Answer
> Contrapositive: yes (identical truth tables). Converse: no (they differ when $p$ is false and $q$ true).

**Q4 (L3).** Simplify $\lnot(p \lor \lnot q) \lor (\lnot p \land \lnot q)$, naming the laws.

> [!success]- Answer
> De Morgan: $(\lnot p \land q) \lor (\lnot p \land \lnot q)$; distributive: $\lnot p \land (q \lor \lnot q)$; complement and identity: $\lnot p$.

## [[DM-03 Predicates and Quantifiers]]

**Q5 (L2).** Negate $\forall x\,(P(x) \to Q(x))$ and simplify.

> [!success]- Answer
> $\exists x\,(P(x) \land \lnot Q(x))$.

**Q6 (L3).** Does $\exists y\,\forall x\,L(x, y)$ mean the same as $\forall x\,\exists y\,L(x, y)$? Use $L(x, y)$ = "$x$ likes $y$".

> [!success]- Answer
> No. The first says one $y$ is liked by everyone; the second says everyone likes someone (possibly different). The first implies the second, not conversely.

## [[DM-04 Rules of Inference]]

**Q7 (L2).** Name the rule: $p \to q$, $\lnot q$, therefore $\lnot p$.

> [!success]- Answer
> Modus tollens.

**Q8 (L3).** Is this valid? "If it rains, the match is cancelled. The match was cancelled. So it rained."

> [!success]- Answer
> Invalid: affirming the consequent. The match could have been cancelled for another reason.

## [[DM-05 Direct Proof, Contrapositive and Contradiction]]

**Q9 (L3).** Prove directly that the sum of two odd integers is even.

> [!success]- Answer
> $(2a + 1) + (2b + 1) = 2(a + b + 1)$, which is even.

**Q10 (L2).** Compute $\gcd(84, 36)$ with the Euclidean algorithm.

> [!success]- Answer
> $84 = 2 \cdot 36 + 12$; $36 = 3 \cdot 12 + 0$; so $\gcd = 12$.

## [[DM-06 Sets, Set Operations, Power Sets and Cartesian Products]]

**Q11 (L1).** For $A = \{1, 2, 3\}$, $B = \{2, 3, 4\}$, find $A \cap B$, $A \setminus B$ and $A \oplus B$ (symmetric difference).

> [!success]- Answer
> $\{2, 3\}$; $\{1\}$; $\{1, 4\}$.

**Q12 (L2).** How many elements are in $\mathcal{P}(\{a, b, c, d\})$? In $A \times B$ if $|A| = 3$, $|B| = 4$?

> [!success]- Answer
> $2^4 = 16$; $3 \times 4 = 12$.

## [[DM-07 Functions]]

**Q13 (L2).** How many functions are there from a 3-element set to a 4-element set? How many are injective?

> [!success]- Answer
> $4^3 = 64$; injective: $4 \cdot 3 \cdot 2 = 24$.

**Q14 (L3).** How many surjections are there from a 4-element set onto a 3-element set?

> [!success]- Answer
> By inclusion–exclusion: $3^4 - \binom31 2^4 + \binom32 1^4 = 81 - 48 + 3 = 36$.

## [[DM-08 Sequences and Summations]]

**Q15 (L1).** Compute $\sum_{i=1}^{100} i$ and $\sum_{i=1}^{10} i^2$.

> [!success]- Answer
> $100 \cdot 101 / 2 = 5050$; $10 \cdot 11 \cdot 21 / 6 = 385$.

**Q16 (L2).** Compute $\sum_{i=0}^{10} 2^i$.

> [!success]- Answer
> $2^{11} - 1 = 2047$.

## [[DM-09 Mathematical Induction]]

**Q17 (L3).** For which $n \ge 1$ is $2^n > n^2$? Prove it for $n \ge 5$.

> [!success]- Answer
> True for $n = 1$ and all $n \ge 5$; false for $n = 2, 3, 4$. Base $n = 5$: $32 > 25$. Step: if $2^k > k^2$ with $k \ge 5$, then $2^{k+1} > 2k^2 \ge (k + 1)^2$, because $k^2 \ge 2k + 1$ for $k \ge 3$.

**Q18 (L2).** What's wrong with an induction proof that skips the base case?

> [!success]- Answer
> Without a base case, the chain never starts: the step only proves "if $P(k)$ then $P(k+1)$". (E.g. "$n = n + 1$" has a valid step but no true base.)

## [[DM-10 Relations, Equivalence Relations and Partial Orders]]

**Q19 (L2).** Is "has the same birth month as" an equivalence relation? What are its classes?

> [!success]- Answer
> Yes: reflexive, symmetric and transitive. The classes are the (at most 12) groups of people sharing a month.

**Q20 (L3).** Draw the Hasse diagram of divisibility on $\{1, 2, 3, 4, 6, 12\}$. How many edges, and what are the minimal and maximal elements?

> [!success]- Answer
> Covering edges: 1–2, 1–3, 2–4, 2–6, 3–6, 4–12, 6–12: **7** edges. Minimal: 1; maximal: 12.

## [[DM-11 Counting Principles, Permutations and Combinations]]

**Q21 (L1).** In how many ways can 5 books be arranged on a shelf? How many ways to choose 3 of 7 students?

> [!success]- Answer
> $5! = 120$; $\binom73 = 35$.

**Q22 (L2).** In how many ways can 6 people sit at a round table (rotations considered the same)?

> [!success]- Answer
> $(6 - 1)! = 120$.

## [[DM-12 Pigeonhole Principle and Inclusion-Exclusion]]

**Q23 (L2).** How many integers from 1 to 100 are divisible by 3 or 5?

> [!success]- Answer
> $33 + 20 - 6 = 47$.

**Q24 (L2).** Show that among any 13 people, two share a birth month.

> [!success]- Answer
> 12 months (pigeonholes), 13 people: by pigeonhole, some month has at least 2.

## [[DM-13 Binomial Theorem and Pascal's Triangle]]

**Q25 (L1).** Write row 5 of Pascal's triangle.

> [!success]- Answer
> 1, 5, 10, 10, 5, 1.

**Q26 (L2).** Find the coefficient of $x^2y^3$ in $(x + y)^5$.

> [!success]- Answer
> $\binom53 = 10$.

## [[DM-14 Recurrence Relations]]

**Q27 (L2).** Towers of Hanoi: $h_n = 2h_{n-1} + 1$, $h_1 = 1$. Find $h_6$ and the closed form.

> [!success]- Answer
> $h_n = 2^n - 1$; $h_6 = 63$.

**Q28 (L3).** Solve $a_n = 5a_{n-1} - 6a_{n-2}$, $a_0 = 1$, $a_1 = 4$.

> [!success]- Answer
> Roots 2 and 3: $a_n = A\,2^n + B\,3^n$; $A + B = 1$, $2A + 3B = 4$ ⇒ $B = 2$, $A = -1$: $a_n = 2 \cdot 3^n - 2^n$. Check: $a_2 = 5 \cdot 4 - 6 = 14 = 18 - 4$ ✓.

## [[DM-15 Graphs, Representations, Paths and Connectivity]]

**Q29 (L2).** A graph has 6 vertices of degrees 2, 2, 3, 3, 4, 4. How many edges? Does it have an Euler circuit?

> [!success]- Answer
> $18/2 = 9$ edges. No Euler circuit (two odd-degree vertices); an Euler path exists if it's connected.

**Q30 (L3).** When would you use an adjacency list rather than an adjacency matrix?

> [!success]- Answer
> For sparse graphs: space $O(V + E)$ instead of $O(V^2)$, and iterating a vertex's neighbours is proportional to its degree.

## [[DM-16 Trees and Spanning Trees]]

**Q31 (L1).** How many edges does a tree with 15 vertices have?

> [!success]- Answer
> 14.

**Q32 (L2).** A full binary tree has 7 internal nodes. How many leaves?

> [!success]- Answer
> $i + 1 = 8$.

## [[DM-17 Boolean Algebra and Logic Circuits]]

**Q33 (L2).** How many distinct Boolean functions of 3 variables are there?

> [!success]- Answer
> $2^{2^3} = 256$.

**Q34 (L3).** Simplify $\bar{x}\bar{y} + \bar{x}y + x\bar{y}$.

> [!success]- Answer
> $\bar{x}(\bar y + y) + x\bar y = \bar x + x\bar y = \bar x + \bar y$ (absorption-type law $a + \bar a b = a + b$).

## [[DM-18 Introductory Discrete Probability]]

**Q35 (L1).** Two fair dice are rolled. What's the probability that the sum is 7?

> [!success]- Answer
> $6/36 = 1/6$.

**Q36 (L2).** Find the expected value of one fair die roll, and the probability of at least one head in 3 fair coin flips.

> [!success]- Answer
> $3.5$; $1 - (1/2)^3 = 7/8 = 0.875$.

Back to [[Question Bank Index]] · [[MOCK-DM-01 Discrete Mathematics Mock Examination]] · [[DM 00 Dashboard]]
