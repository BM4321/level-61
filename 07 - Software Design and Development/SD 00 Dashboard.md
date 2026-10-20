---
title: "Software Design and Development Dashboard"
module: "Software Design and Development"
module_code: "CST06101"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - software-design
  - dashboard
---

# Software Design and Development: CST06101 Dashboard

**Credits:** 10 · **LTP (as supplied):** 2,2,0 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL (no official descriptor was supplied; see [[Syllabus Verification Log]]) · **Running example:** [[SD-CASE LabBook Running Case Study]] · **Code:** `07 - Software Design and Development/code/` (LabBook package plus the flawed-design clinic, 41 passing tests plus 1 documented expected failure, mypy-clean)

> [!todo] ▶ Next lesson
> The first lesson in the table below whose mastery is below 3. If you are new: **[[SD-01 Software Engineering Fundamentals]]**.

## What is this subject about?
How to turn a vague need into software that works, keeps working, and can be changed safely. That means choosing a process, capturing requirements, designing an architecture and modules, modelling with UML, applying design principles and patterns, and constructing, testing, refactoring, deploying and maintaining the result. Every lesson uses one system, **LabBook** (a university computer-lab booking system), so you can see each idea in context.

## What should I know before starting?
- Basic Python, including classes: [[PY-16 Classes and Objects]], [[PY-17 Inheritance, Composition and Polymorphism]].
- Testing basics: [[PY-20 Testing, Debugging and Test-Driven Development]].
- Some SQL for SD-09: [[PY-22 SQL and Database Integration]].
- Logic and relations from [[DM-10 Relations, Equivalence Relations and Partial Orders]] help with dependency and state models.

## Learning order and lessons

| # | Lesson | Unit | Status | Key practical output |
|---|---|---|---|---|
| 1 | [[SD-01 Software Engineering Fundamentals]] | U1 Process | core | Quality attributes for LabBook |
| 2 | [[SD-02 Software Process Models]] | U1 Process | core | Process choice with justification |
| 3 | [[SD-03 Requirements Engineering]] | U2 Requirements | core | SRS extract (FR/NFR) |
| 4 | [[SD-04 Use Cases, User Stories and Traceability]] | U2 Requirements | core | Use cases, stories, traceability matrix |
| 5 | [[SD-05 Software Architecture and Architectural Styles]] | U3 Design | core | Layered architecture + ADR |
| 6 | [[SD-06 Modular Design, Cohesion and Coupling]] | U3 Design | core | Module decomposition |
| 7 | [[SD-07 UML Class Diagrams]] | U4 Modelling | core | LabBook domain class diagram |
| 8 | [[SD-08 UML Sequence, Activity and State Diagrams]] | U4 Modelling | core | Booking sequence + state machine |
| 9 | [[SD-09 Data Modeling and Interface Design]] | U4 Modelling | core | ERD, schema, API contract |
| 10 | [[SD-10 SOLID Principles]] | U5 Principles | core | SOLID review of LabBook |
| 11 | [[SD-11 Creational and Structural Design Patterns]] | U5 Principles | core | Factory, composite, adapter |
| 12 | [[SD-12 Behavioral Design Patterns]] | U5 Principles | core | Strategy, observer, state |
| 13 | [[SD-13 Implementation, Code Organization and Version Control]] | U6 Construction | core | Package layout, Git workflow |
| 14 | [[SD-14 Software Testing, Verification and Validation]] | U6 Construction | core | Test plan + contract tests |
| 15 | [[SD-15 Refactoring, Technical Debt, Code Review and Quality]] | U6 Construction | core | God-class refactoring |
| 16 | [[SD-16 Deployment, Maintenance and Documentation]] | U7 Operation | core | Release + maintenance plan |
| 17 | [[SD-17 Secure and Reliable Software Design]] | U7 Operation | core | Secure-design review |

Also: [[SD-CASE LabBook Running Case Study]] · [[SD Flawed Design Clinic]] · Map: [[SD 01 Curriculum Map]] · Mind map: [[MM-SD Software Design Mind Map]]

## What should I read, watch, calculate, code or build?
- **Read:** the lessons in order, and keep the LabBook code open alongside them.
- **Code:**
  ```bash
  cd "07 - Software Design and Development/code"
  python -m pytest -q          # 41 passed, 1 xfailed (known concurrency defect, see SD-17)
  python -m mypy labbook       # type check
  python -m labbook --user u-amina --ws LAB1-01 --start 2026-03-02T09:00 --end 2026-03-02T11:00
  ```
- **Build:** extend LabBook in the exercises (new rules, a waiting list, a REST adapter), and refactor the clinic's flawed designs.
- **Draw:** every UML diagram in Mermaid or on paper. Exams usually expect hand-drawn notation.

## Exercises I must complete
- Levels 1–3 in every lesson.
- The refactoring tasks in [[SD Flawed Design Clinic]] (F1–F5).
- One full design document for LabBook or your own system: requirements, architecture, UML, data model, test plan.

## How do I test my understanding?
- Each lesson's self-test.
- `python -m pytest` after every change you make to LabBook.
- [[QB-SD Software Design Question Bank]] and [[MOCK-SD-01 Software Design and Development Mock Examination]].

## Evidence of mastery (provisional learning outcomes)
*Designed outcomes, not official ones. Replace them when your module descriptor is available.*
1. **SD-LO1** Compare software process models and select one for a given project context.
2. **SD-LO2** Elicit, specify, validate and trace functional and non-functional requirements.
3. **SD-LO3** Design an architecture and modular decomposition, justifying them with quality attributes, cohesion and coupling.
4. **SD-LO4** Model a system with UML class, sequence, activity and state diagrams, and a data model.
5. **SD-LO5** Apply SOLID principles and appropriate design patterns, including recognising when *not* to use them.
6. **SD-LO6** Plan and carry out testing, refactoring, code review, deployment and maintenance, including security and reliability concerns.

| Evidence | Demonstrates |
|---|---|
| A LabBook design document (requirements → architecture → UML → data → tests) | LO2–LO4 |
| A refactored F1 god class with tests passing before and after | LO5–LO6 |
| A pattern-choice essay that includes a "when not to use" case | LO5 |
| Mock exam ≥ 60% | All |

## What remains incomplete?
See [[BUILD-STATUS]]. For your own progress, see [[Progress Tracker]].
