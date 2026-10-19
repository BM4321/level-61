---
title: "DM Python Toolkit"
module: "Discrete Mathematics"
module_code: "GST06106"
type: "system"
tags:
  - semester-6
  - discrete-math
  - python
---

# DM Python Toolkit (`code/dm_tools.py`)

A small, standard-library-only Python module for **checking** your discrete-mathematics work. It is a calculator for verification, not a substitute for written working. Exams require full reasoning.

## Run it
```bash
cd "03 - Discrete Mathematics/code"
python -m pytest                 # 23 tests: toolkit self-tests + machine checks of every lesson's answers
python -c "from dm_tools import *; print_truth_table('(p -> q) and p -> q', ['p', 'q'])"
```

## Functions by lesson
| Lesson | Functions |
|---|---|
| [[DM-01 Propositions, Connectives and Truth Tables]], [[DM-02 Logical Equivalence and Laws of Logic]] | `evaluate`, `truth_table`, `print_truth_table`, `is_tautology`, `is_contradiction`, `equivalent`, `minterms` |
| [[DM-04 Rules of Inference]] | `valid_argument(premises, conclusion, variables)` |
| [[DM-06 Sets, Set Operations, Power Sets and Cartesian Products]] | `power_set`, `cartesian` (plus Python's own `set` operators) |
| [[DM-07 Functions]] | `is_injective`, `is_surjective`, `count_functions` |
| [[DM-10 Relations, Equivalence Relations and Partial Orders]] | `is_reflexive`, `is_symmetric`, `is_antisymmetric`, `is_transitive`, `equivalence_classes` |
| [[DM-11 Counting Principles, Permutations and Combinations]] – [[DM-13 Binomial Theorem and Pascal's Triangle]] | `perm`, `comb`, `multiset_perm`, `combinations_with_repetition`, `derangements`, `count_divisible`, `binomial_coefficients` |
| [[DM-14 Recurrence Relations]] | `iterate_recurrence(coeffs, initial, n, f)` |
| [[DM-15 Graphs, Representations, Paths and Connectivity]], [[DM-16 Trees and Spanning Trees]] | `degrees`, `is_connected`, `euler_status`, `kruskal` |
| [[DM-17 Boolean Algebra and Logic Circuits]] | `minterms`, `equivalent` |
| [[DM-18 Introductory Discrete Probability]] | `probability` (exact `Fraction`) |

## Logic syntax
`and`, `or`, `xor`, `not`, `->`, `<->`, `T`, `F` and parentheses. Precedence from high to low: `not`, `and`, `xor`, `or`, `->`, `<->`, and `->` is right-associative, matching [[DM-01 Propositions, Connectives and Truth Tables]] §5.4. The parser is a small recursive-descent parser. An earlier draft translated `->` textually into Python's `<=`, which gave **wrong precedence** for `not p -> q`. The current tests guard against that regression.

## How the answers were verified
`tests/test_dm_answers.py` contains one test function per lesson that recomputes the worked examples and solutions: truth tables, counts (by formula **and** brute-force enumeration where feasible), closed forms of recurrences (against iterated terms), MST weights, chromatic numbers, Dijkstra distances and probabilities. During the build these checks caught one wrong figure in a draft solution (DM-11 practice 9(c), corrected to 194 400) and a precedence bug in the toolkit itself (fixed by the parser). Draft text errors in DM-09 (string slicing) and PY-10/PY-12 were caught by running the code. See [[BUILD-STATUS]].
