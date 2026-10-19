---
title: "Discrete Mathematics Dashboard"
module: "Discrete Mathematics"
module_code: "GST06106"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - discrete-math
  - dashboard
---

# Discrete Mathematics: GST06106 Dashboard

**Credits:** 9 · **LTP (as supplied):** 3,2,3 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL

> [!todo] ▶ Next lesson
> The first lesson below with mastery < 3. New? Start with **[[DM-01 Propositions, Connectives and Truth Tables]]**.

## What is this subject about?
The mathematics of **separate, countable things**: true/false statements, sets, relations, functions, counting, recurrences, graphs and trees. It's the mathematical foundation of computing. Logic underlies `if` statements and circuits, sets underlie databases, counting underlies algorithm cost and password strength, recurrences underlie recursive algorithms, and graphs underlie networks and project schedules. Above all, it teaches you to **prove** things, not just believe them.

## What should I know before starting?
School algebra (expanding brackets, solving linear equations, exponents, summation of simple series) and comfort with careful reading. No calculus is needed. If algebra is rusty, revise exponent laws and factorisation before DM-08.

## Learning order
| # | Lesson | Unit | Status | CS connection |
|---|---|---|---|---|
| 1 | [[DM-01 Propositions, Connectives and Truth Tables]] | U1 Logic | core | Conditions in code, circuits |
| 2 | [[DM-02 Logical Equivalence and Laws of Logic]] | U1 | core | Simplifying conditions, De Morgan |
| 3 | [[DM-03 Predicates and Quantifiers]] | U1 | core | Specifications, SQL, `all()`/`any()` |
| 4 | [[DM-04 Rules of Inference]] | U1 | core | Valid reasoning, debugging, security arguments |
| 5 | [[DM-05 Direct Proof, Contrapositive and Contradiction]] | U2 Proof | core | Algorithm correctness |
| 6 | [[DM-06 Sets, Set Operations, Power Sets and Cartesian Products]] | U3 Structures | core | Python `set`, SQL, types |
| 7 | [[DM-07 Functions]] | U3 | core | Hashing, encodings, bijections |
| 8 | [[DM-08 Sequences and Summations]] | U3 | core | Loop costs |
| 9 | [[DM-09 Mathematical Induction]] | U2 | core | Recursion and loop invariants |
| 10 | [[DM-10 Relations, Equivalence Relations and Partial Orders]] | U3 | core | Databases, grouping, dependency order |
| 11 | [[DM-11 Counting Principles, Permutations and Combinations]] | U4 Counting | core | Password spaces, brute force |
| 12 | [[DM-12 Pigeonhole Principle and Inclusion-Exclusion]] | U4 | core | Hash collisions, survey counts |
| 13 | [[DM-13 Binomial Theorem and Pascal's Triangle]] | U4 | core | Combinatorics, probability |
| 14 | [[DM-14 Recurrence Relations]] | U4 | core | Recursive algorithm costs |
| 15 | [[DM-15 Graphs, Representations, Paths and Connectivity]] | U5 Graphs | core | Networks, BFS, CPM |
| 16 | [[DM-16 Trees and Spanning Trees]] | U5 | core | Data structures, network design |
| 17 | [[DM-17 Boolean Algebra and Logic Circuits]] | U6 Boolean | core | Hardware, simplification |
| 18 | [[DM-18 Introductory Discrete Probability]] | U4 | supplementary | Risk, hashing, testing |

Dependency graph: [[DM 01 Curriculum Map]] · Mind map: [[MM-DM Discrete Mathematics Mind Map]] · Python verification toolkit: `code/dm_tools.py` ([[DM Python Toolkit]])

## What should I read, calculate or code?
- **Read and calculate:** each lesson, re-deriving every worked example **on paper** before reading the solution.
- **Reference text** (widely used, not confirmed as your prescribed text): K. H. Rosen, *Discrete Mathematics and Its Applications*, 8th ed., McGraw-Hill, 2019. Free alternative: O. Levin, *Discrete Mathematics: An Open Introduction* (open textbook, https://discrete.openmathbooks.org/). See [[Source Register]].
- **Code:** check counting and truth-table answers with `code/dm_tools.py`. Use it to *verify* your work, not to replace it.

## Exercises I must complete
Levels 1–3 of every lesson, plus at least two Level-4 proofs per unit. Proof exercises must be **written in full sentences** with a justification for each step.

## How do I test my understanding?
Lesson self-tests, [[QB-DM Discrete Mathematics Question Bank]], [[MOCK-DM-01 Discrete Mathematics Mock Examination]] (timed, with a marking guide).

## Evidence of mastery (provisional learning outcomes, not official)
1. **DM-LO1** Translate between English and propositional/predicate logic, and determine validity using truth tables and rules of inference.
2. **DM-LO2** Construct direct, contrapositive, contradiction and induction proofs with justified steps.
3. **DM-LO3** Apply set, relation and function concepts, including properties of relations and functions.
4. **DM-LO4** Solve counting problems (product/sum rules, permutations, combinations, pigeonhole, inclusion–exclusion, binomial theorem).
5. **DM-LO5** Formulate and solve recurrence relations, and analyse recursive algorithms.
6. **DM-LO6** Model problems with graphs and trees, and apply traversal and spanning-tree algorithms.
7. **DM-LO7** Simplify Boolean expressions and relate them to logic circuits.

| Evidence | Outcomes |
|---|---|
| Mock exam ≥ 60%, with every proof question attempted in full | All |
| Three written proofs (direct, contradiction, induction) self-marked against the rubric in [[DM-05 Direct Proof, Contrapositive and Contradiction]] | LO2 |
| [[X-02 Graph Theory in Algorithms, Networks and Scheduling]] completed | LO6 |

## What remains incomplete?
Vault gaps: [[BUILD-STATUS]]. Your progress: [[Progress Tracker]].
