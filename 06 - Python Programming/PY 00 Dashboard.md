---
title: "Python Programming Dashboard"
module: "Python Programming"
module_code: "CST06102"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - python
  - dashboard
---

# Python Programming: CST06102 Dashboard

**Credits:** 12 · **LTP (as supplied):** 3,3,2 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL · **Python version:** 3.10+ (examples tested on CPython 3.13)

> [!todo] ▶ Next lesson
> The first lesson in the table below whose mastery is below 3. If you are new: **[[PY-01 How Python Executes Programs and Environment Setup]]**.

## What is this subject about?
Writing correct, readable and maintainable programs in Python, and learning to **think algorithmically**: break a problem into steps, choose data structures, reason about correctness and cost, and prove your program works with tests. By the end you build modular applications with files, databases, tests and logging.

## What should I know before starting?
Nothing about programming is assumed. You need basic computer literacy (files, folders, a terminal) and school-level arithmetic. Logic from [[DM-01 Propositions, Connectives and Truth Tables]] helps with conditions from PY-04 onward. Study the two side by side.

## Learning order and lessons

| # | Lesson | Unit | Status | Key practical output |
|---|---|---|---|---|
| 1 | [[PY-01 How Python Executes Programs and Environment Setup]] | U1 | core | First script, REPL, venv |
| 2 | [[PY-02 Variables, Types, Expressions and Operators]] | U1 | core | Unit-converter calculations |
| 3 | [[PY-03 Input, Output and String Formatting]] | U1 | core | Receipt printer |
| 4 | [[PY-04 Conditions and Branching]] | U1 | core | Grade classifier |
| 5 | [[PY-05 Loops and Iteration]] | U1 | core | Validation loops, tables |
| 6 | [[PY-06 Functions, Parameters, Return Values and Scope]] | U2 | core | Reusable function library |
| 7 | [[PY-07 Recursion]] | U2 | core | Recursive algorithms |
| 8 | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing]] | U2 | core | Trace tables, pseudocode |
| 9 | [[PY-09 Strings and String Processing]] | U3 | core | Text analyser |
| 10 | [[PY-10 Lists and Tuples]] | U3 | core | Marks statistics |
| 11 | [[PY-11 Dictionaries, Sets and Comprehensions]] | U3 | core | Word counts, grouping |
| 12 | [[PY-12 Searching, Sorting and Complexity]] | U3 | core | Binary search, sorts, Big-O |
| 13 | [[PY-13 Modules, Packages, Imports and Virtual Environments]] | U4 | core | Multi-file program |
| 14 | [[PY-14 Files, CSV and JSON]] | U4 | core | Persistent storage |
| 15 | [[PY-15 Exceptions and Defensive Programming]] | U4 | core | Robust input handling |
| 16 | [[PY-16 Classes and Objects]] | U5 | core | Domain classes |
| 17 | [[PY-17 Inheritance, Composition and Polymorphism]] | U5 | core | Class hierarchies |
| 18 | [[PY-18 Iterators, Generators, Decorators and Context Managers]] | U5 | supplementary | Lazy pipelines |
| 19 | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring]] | U6 | core | Refactored code |
| 20 | [[PY-20 Testing, Debugging and Test-Driven Development]] | U6 | core | pytest suites, TDD |
| 21 | [[PY-21 Data Structures and Algorithm Design]] | U6 | core | Stack, queue, linked list, BST |
| 22 | [[PY-22 SQL and Database Integration]] | U7 | core | SQLite CRUD |
| 23 | [[PY-23 HTTP APIs and External Services]] | U7 | supplementary | JSON API client |
| 24 | [[PY-24 Secure Programming and Input Validation]] | U7 | core | Validation layer |
| 25 | [[PY-25 Performance, Packaging and Project Organization]] | U7 | supplementary | Profiled, packaged app |

Full dependency graph: [[PY 01 Curriculum Map]] · Mind map: [[MM-PY Python Programming Mind Map]]

## What should I read, watch, calculate, code or build?
- **Read:** each lesson in order. The official [Python Tutorial](https://docs.python.org/3/tutorial/) is the primary external reference (see [[Source Register]]).
- **Code:** every lesson's *Minimal working code* by typing it yourself, never copy-paste. Then do the exercises in `code/exercises/` (stubs) and check them with tests:
  ```bash
  cd "06 - Python Programming/code"
  python -m pytest                       # checks the reference solutions
  PY_TARGET=exercises python -m pytest   # checks YOUR answers in exercises/
  ```
  (On Windows PowerShell: `$env:PY_TARGET="exercises"; python -m pytest`.)
- **Build:** the five projects in [[Labs and Projects Index]], in order of difficulty.

## Exercises I must complete
- Levels 1–3 of every lesson's practice set (minimum for mastery 3).
- The `code/exercises/pyNN_exercises.py` file for each lesson, until all its tests pass.
- At least one L4 or L5 problem per unit.

## How do I test my understanding?
- The self-test at the end of each lesson (closed book, 80% to pass).
- `PY_TARGET=exercises python -m pytest` on your own solutions.
- [[QB-PY Python Question Bank]] and [[MOCK-PY-01 Python Programming Mock Examination]].

## Evidence of mastery (provisional learning outcomes)
*Designed outcomes, not official ones. Replace them when your module descriptor is available.*
1. **PY-LO1** Write, run and debug Python programs using variables, control flow and functions.
2. **PY-LO2** Select and use appropriate built-in data structures, and analyse the time complexity of simple algorithms.
3. **PY-LO3** Build robust programs that handle files, exceptions and invalid input safely.
4. **PY-LO4** Design programs with classes, composition and inheritance, and explain the trade-offs.
5. **PY-LO5** Verify programs with automated tests and apply clean-code and refactoring practices.
6. **PY-LO6** Integrate a database and external services in a modular, documented, secure application.

| Evidence | Demonstrates |
|---|---|
| All exercise tests pass with `PY_TARGET=exercises` | LO1–LO3 |
| [[PRJ-PY-01 Student Marks and Grading System]] and [[PRJ-PY-02 Personal Expense Tracker]] complete with tests | LO1–LO3, LO5 |
| [[PRJ-PY-03 Library Management System]] with a class diagram | LO4 |
| [[PRJ-PY-05 Hostel Maintenance System]] with database, tests, logging and architecture notes | LO5–LO6 |
| Mock exam ≥ 60% | All |

## What remains incomplete?
See [[BUILD-STATUS]] for vault gaps. For *your* progress, see [[Progress Tracker]] (Python section).
