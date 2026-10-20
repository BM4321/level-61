---
title: "Software Design and Development Curriculum Map"
module: "Software Design and Development"
module_code: "CST06101"
type: "curriculum-map"
syllabus_status: "provisional"
tags:
  - semester-6
  - software-design
  - curriculum
---

# Software Design and Development: Curriculum Map

Back to [[SD 00 Dashboard]]

## 1. Units
| Unit | Topics | LabBook artefact |
|---|---|---|
| U1 Process | SD-01 fundamentals · SD-02 process models | Quality-attribute list; process decision |
| U2 Requirements | SD-03 requirements engineering · SD-04 use cases, stories, traceability | SRS extract; use cases UC-01 to UC-03; traceability matrix |
| U3 Design | SD-05 architecture · SD-06 modularity | Layered architecture; ADR-001; module map |
| U4 Modelling | SD-07 class diagrams · SD-08 behaviour diagrams · SD-09 data and interfaces | Class, sequence and state diagrams; ERD; API contract |
| U5 Principles and patterns | SD-10 SOLID · SD-11 creational/structural · SD-12 behavioural | `rules.py` (Strategy, Composite), `events.py` (Observer), `app.py` (Factory) |
| U6 Construction | SD-13 implementation and VCS · SD-14 testing · SD-15 refactoring and quality | Package layout; contract tests; clinic refactorings |
| U7 Operation | SD-16 deployment and maintenance · SD-17 secure and reliable design | Release plan; security review |

## 2. Prerequisite graph
```mermaid
flowchart TD
    S1[SD-01 Fundamentals] --> S2[SD-02 Process models]
    S2 --> S3[SD-03 Requirements]
    S3 --> S4[SD-04 Use cases & traceability]
    S4 --> S5[SD-05 Architecture]
    S5 --> S6[SD-06 Modularity]
    S6 --> S7[SD-07 Class diagrams]
    S7 --> S8[SD-08 Behaviour diagrams]
    S7 --> S9[SD-09 Data & interfaces]
    S6 --> S10[SD-10 SOLID]
    S10 --> S11[SD-11 Creational & structural patterns]
    S10 --> S12[SD-12 Behavioural patterns]
    S6 --> S13[SD-13 Implementation & VCS]
    S13 --> S14[SD-14 Testing]
    S14 --> S15[SD-15 Refactoring & quality]
    S15 --> S16[SD-16 Deployment & maintenance]
    S5 --> S17[SD-17 Secure & reliable design]
```
*Text version: process (01–02) leads to requirements (03–04), then architecture (05) and modular design (06). Modularity feeds modelling (07–09), principles and patterns (10–12) and construction (13–15), which ends in deployment (16). Secure design (17) builds on architecture.*

## 3. Review alerts
| Before… | Review | Why |
|---|---|---|
| SD-07 | [[PY-16 Classes and Objects]], [[PY-17 Inheritance, Composition and Polymorphism]] | Classes, composition, inheritance |
| SD-08 | [[DM-10 Relations, Equivalence Relations and Partial Orders]] | State transitions as a relation |
| SD-09 | [[PY-22 SQL and Database Integration]] | Schemas, keys, constraints |
| SD-10/11/12 | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring]] | Protocols, interfaces in Python |
| SD-14 | [[PY-20 Testing, Debugging and Test-Driven Development]] | pytest, fixtures, TDD |
| SD-17 | [[CS-02 Threat Modeling and Security Requirements]] | STRIDE and security requirements |

## 4. Cross-module links
[[X-01 Logic and Sets in Python and Requirements]] · [[X-03 Security Requirements in Software Architecture]] · [[X-04 Testing as Software Quality Assurance]] · [[PM-04 Scope Management, Requirements Traceability and WBS]] · [[FYP-08 Technical Architecture and Design Planning]] · [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]]
