---
title: "Master Curriculum Inventory"
type: "index"
syllabus_status: "provisional"
tags:
  - semester-6
  - curriculum
---

# Master Curriculum Inventory

> [!warning] PROVISIONAL CURRICULUM
> This inventory is a **designed** standard curriculum, not your institution's official syllabus. No official module descriptors were supplied, and none were found publicly (see [[Syllabus Verification Log]]). Status labels:
> - **provisional-core**: standard content for a module with this title at diploma / early-undergraduate level. Very likely relevant, but **not verified** against your syllabus.
> - **supplementary**: useful enrichment that is commonly but not universally taught.
> - **optional-advanced**: beyond typical diploma scope; for strong students and long-term use.
> - **verified**: confirmed against official documents. *(No topic has this status yet.)*

Hierarchy: **Module → Unit → Topic (lesson) → worked examples → exercises (L1–L5) → self-test → assessment (mock exam / lab / project)**.
Topics are listed in **dependency order**, which is the order you should study them.

Module codes, credits and LTP figures are in [[Module Register]].

---

## ITT06102 Cyber Security (prefix `CS`)

Dashboard: [[CS 00 Dashboard]] · Map: [[CS 01 Curriculum Map]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| CS-01 | [[CS-01 Security Foundations - CIA, Threats, Vulnerabilities and Risk]] | U1 Foundations | provisional-core | none |
| CS-02 | [[CS-02 Threat Modeling and Security Requirements]] | U1 Foundations | provisional-core | CS-01 |
| CS-03 | [[CS-03 Authentication and Identity]] | U2 Identity and Access | provisional-core | CS-01 |
| CS-04 | [[CS-04 Authorization and Access Control]] | U2 Identity and Access | provisional-core | CS-03 |
| CS-05 | [[CS-05 Cryptography Foundations and Symmetric Encryption]] | U3 Cryptography | provisional-core | CS-01, DM-01 |
| CS-06 | [[CS-06 Hashes, MACs and Integrity]] | U3 Cryptography | provisional-core | CS-05 |
| CS-07 | [[CS-07 Public-Key Cryptography, Signatures and Key Management]] | U3 Cryptography | provisional-core | CS-05, CS-06 |
| CS-08 | [[CS-08 Password Storage and Authentication Security]] | U3 Cryptography | provisional-core | CS-03, CS-06 |
| CS-09 | [[CS-09 Network Security and Secure Communication]] | U4 Infrastructure | provisional-core | CS-01, CS-07 |
| CS-10 | [[CS-10 Operating System Security and Hardening]] | U4 Infrastructure | provisional-core | CS-04 |
| CS-11 | [[CS-11 Web Application Security]] | U5 Application Security | provisional-core | CS-03, CS-04, CS-09 |
| CS-12 | [[CS-12 Secure Software Development and Database Security]] | U5 Application Security | provisional-core | CS-11 |
| CS-13 | [[CS-13 Social Engineering and Security Awareness]] | U6 Human and Threat Landscape | provisional-core | CS-01 |
| CS-14 | [[CS-14 Malware and Defensive Detection]] | U6 Human and Threat Landscape | provisional-core | CS-10 |
| CS-15 | [[CS-15 Logging, Monitoring, Incident Response and Recovery]] | U7 Operations | provisional-core | CS-14 |
| CS-16 | [[CS-16 Risk Analysis, Policy, Governance and Compliance]] | U7 Operations | provisional-core | CS-01, CS-02 |
| CS-17 | [[CS-17 Digital Forensics Fundamentals]] | U7 Operations | supplementary | CS-15 |
| CS-18 | [[CS-18 Security Testing and Vulnerability Management]] | U8 Assurance | provisional-core | CS-11, CS-16 |
| CS-19 | [[CS-19 Cloud Security and Privacy]] | U8 Assurance | supplementary | CS-04, CS-09, CS-16 |

**Labs:** [[LAB-CS-01 Password Strength and Secure Password Storage]] · [[LAB-CS-02 Hashing and Integrity Verification]] · [[LAB-CS-03 Toy Ciphers and Why They Fail]] · [[LAB-CS-04 File Permission Audit]] · [[LAB-CS-05 Security Headers and Configuration Analysis]] · [[LAB-CS-06 Input Validation and SQL Injection Prevention]] · [[LAB-CS-07 Threat Modeling a Sample Web Application]] · [[LAB-CS-08 Log Analysis and Incident Response]]

---

## GST06106 Discrete Mathematics (prefix `DM`)

Dashboard: [[DM 00 Dashboard]] · Map: [[DM 01 Curriculum Map]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| DM-01 | [[DM-01 Propositions, Connectives and Truth Tables]] | U1 Logic | provisional-core | none |
| DM-02 | [[DM-02 Logical Equivalence and Laws of Logic]] | U1 Logic | provisional-core | DM-01 |
| DM-03 | [[DM-03 Predicates and Quantifiers]] | U1 Logic | provisional-core | DM-02 |
| DM-04 | [[DM-04 Rules of Inference]] | U1 Logic | provisional-core | DM-02, DM-03 |
| DM-05 | [[DM-05 Direct Proof, Contrapositive and Contradiction]] | U2 Proof | provisional-core | DM-04 |
| DM-06 | [[DM-06 Sets, Set Operations, Power Sets and Cartesian Products]] | U3 Structures | provisional-core | DM-03 |
| DM-07 | [[DM-07 Functions]] | U3 Structures | provisional-core | DM-06 |
| DM-08 | [[DM-08 Sequences and Summations]] | U3 Structures | provisional-core | DM-07 |
| DM-09 | [[DM-09 Mathematical Induction]] | U2 Proof | provisional-core | DM-05, DM-08 |
| DM-10 | [[DM-10 Relations, Equivalence Relations and Partial Orders]] | U3 Structures | provisional-core | DM-06, DM-07 |
| DM-11 | [[DM-11 Counting Principles, Permutations and Combinations]] | U4 Counting | provisional-core | DM-06 |
| DM-12 | [[DM-12 Pigeonhole Principle and Inclusion-Exclusion]] | U4 Counting | provisional-core | DM-11 |
| DM-13 | [[DM-13 Binomial Theorem and Pascal's Triangle]] | U4 Counting | provisional-core | DM-11, DM-09 |
| DM-14 | [[DM-14 Recurrence Relations]] | U4 Counting | provisional-core | DM-08, DM-09 |
| DM-15 | [[DM-15 Graphs, Representations, Paths and Connectivity]] | U5 Graphs | provisional-core | DM-10 |
| DM-16 | [[DM-16 Trees and Spanning Trees]] | U5 Graphs | provisional-core | DM-15, DM-09 |
| DM-17 | [[DM-17 Boolean Algebra and Logic Circuits]] | U6 Boolean Algebra | provisional-core | DM-02 |
| DM-18 | [[DM-18 Introductory Discrete Probability]] | U4 Counting | supplementary | DM-11, DM-12 |

---

## CST06103 Final Year Project I (prefix `FYP`)

Dashboard: [[FYP 00 Dashboard]] · Map: [[FYP 01 Curriculum Map]] · Workflow: [[FYP 02 Idea-to-Defense Workflow]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| FYP-01 | [[FYP-01 Identifying and Narrowing a Research Problem]] | U1 Problem Definition | provisional-core | none |
| FYP-02 | [[FYP-02 Problem Statements, Research Questions, Objectives and Scope]] | U1 Problem Definition | provisional-core | FYP-01 |
| FYP-03 | [[FYP-03 Literature Searching and Critical Reading]] | U2 Literature | provisional-core | FYP-02 |
| FYP-04 | [[FYP-04 Literature Review Synthesis, Research Gaps and Contribution]] | U2 Literature | provisional-core | FYP-03 |
| FYP-05 | [[FYP-05 Research Paradigms and Methodology]] | U3 Methodology | provisional-core | FYP-02 |
| FYP-06 | [[FYP-06 Requirements Gathering, Stakeholder and Feasibility Analysis]] | U3 Methodology | provisional-core | FYP-05, SD-03 |
| FYP-07 | [[FYP-07 Data Collection Instruments, Sampling and Evaluation Planning]] | U3 Methodology | provisional-core | FYP-05 |
| FYP-08 | [[FYP-08 Technical Architecture and Design Planning]] | U4 Planning | provisional-core | FYP-06, SD-05 |
| FYP-09 | [[FYP-09 Project Scheduling, Milestones and Risk Assessment]] | U4 Planning | provisional-core | FYP-08, PM-06 |
| FYP-10 | [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]] | U5 Integrity | provisional-core | FYP-07 |
| FYP-11 | [[FYP-11 Writing the Research Proposal]] | U6 Proposal | provisional-core | FYP-04, FYP-09, FYP-10 |
| FYP-12 | [[FYP-12 Presentation, Defense and Working with Supervisor Feedback]] | U6 Proposal | provisional-core | FYP-11 |

**Templates** (in `04 - Final Year Project I/Project Templates/`): [[FYP-T01 Project Idea Evaluation]] · [[FYP-T02 Problem Statement]] · [[FYP-T03 Research Questions]] · [[FYP-T04 Objectives and Scope]] · [[FYP-T05 Literature Matrix]] · [[FYP-T06 Research Gap Analysis]] · [[FYP-T07 Methodology]] · [[FYP-T08 Requirements Specification]] · [[FYP-T09 Work Breakdown Structure]] · [[FYP-T10 Project Schedule]] · [[FYP-T11 Risk Register]] · [[FYP-T12 Ethics Checklist]] · [[FYP-T13 Proposal Structure]] · [[FYP-T14 Progress Report]] · [[FYP-T15 Presentation and Defense Preparation]]

---

## ITT06105 Information System Project Management (prefix `PM`)

Dashboard: [[PM 00 Dashboard]] · Map: [[PM 01 Curriculum Map]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| PM-01 | [[PM-01 Project Fundamentals and Organizational Context]] | U1 Foundations | provisional-core | none |
| PM-02 | [[PM-02 Project Lifecycles, Process Groups and Methodologies]] | U1 Foundations | provisional-core | PM-01 |
| PM-03 | [[PM-03 Project Initiation, Business Case and Charter]] | U2 Initiation and Scope | provisional-core | PM-02 |
| PM-04 | [[PM-04 Scope Management, Requirements Traceability and WBS]] | U2 Initiation and Scope | provisional-core | PM-03 |
| PM-05 | [[PM-05 Activity Sequencing, Network Diagrams and Gantt Charts]] | U3 Time | provisional-core | PM-04 |
| PM-06 | [[PM-06 Critical Path Method and Float]] | U3 Time | provisional-core | PM-05 |
| PM-07 | [[PM-07 PERT and Schedule Estimation]] | U3 Time | provisional-core | PM-06 |
| PM-08 | [[PM-08 Resource Allocation and Levelling]] | U3 Time | provisional-core | PM-06 |
| PM-09 | [[PM-09 Cost Estimation and Budgeting]] | U4 Cost | provisional-core | PM-04 |
| PM-10 | [[PM-10 Earned Value Management]] | U4 Cost | provisional-core | PM-09, PM-06 |
| PM-11 | [[PM-11 Risk Management]] | U5 Risk and Quality | provisional-core | PM-04, PM-09 |
| PM-12 | [[PM-12 Stakeholder and Communication Management]] | U6 People | provisional-core | PM-03 |
| PM-13 | [[PM-13 Quality Management]] | U5 Risk and Quality | provisional-core | PM-04 |
| PM-14 | [[PM-14 Procurement and Change Management]] | U5 Risk and Quality | provisional-core | PM-04, PM-09 |
| PM-15 | [[PM-15 Team Leadership and Conflict Management]] | U6 People | provisional-core | PM-12 |
| PM-16 | [[PM-16 Agile, Scrum and Hybrid Delivery]] | U7 Delivery Approaches | provisional-core | PM-02, PM-04 |
| PM-17 | [[PM-17 Monitoring, Control, Closure and Lessons Learned]] | U7 Delivery Approaches | provisional-core | PM-10, PM-14 |

**Case studies:** [[PM-CASE-01 University Course Registration System]] · [[PM-CASE-02 Wholesale Inventory Management System]] · [[PM-CASE-03 Small Business Point-of-Sale Software]]

**Artifacts** (template plus filled example): [[PM-A01 Project Charter]] · [[PM-A02 Scope Statement]] · [[PM-A03 Work Breakdown Structure]] · [[PM-A04 Project Schedule]] · [[PM-A05 Project Budget]] · [[PM-A06 Risk Register]] · [[PM-A07 Stakeholder Register]] · [[PM-A08 Communication Plan]] · [[PM-A09 Status Report]] · [[PM-A10 Change Request]] · [[PM-A11 Closure Report]]

---

## CST06102 Python Programming (prefix `PY`)

Dashboard: [[PY 00 Dashboard]] · Map: [[PY 01 Curriculum Map]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| PY-01 | [[PY-01 How Python Executes Programs and Environment Setup]] | U1 Foundations | provisional-core | none |
| PY-02 | [[PY-02 Variables, Types, Expressions and Operators]] | U1 Foundations | provisional-core | PY-01 |
| PY-03 | [[PY-03 Input, Output and String Formatting]] | U1 Foundations | provisional-core | PY-02 |
| PY-04 | [[PY-04 Conditions and Branching]] | U1 Foundations | provisional-core | PY-03 |
| PY-05 | [[PY-05 Loops and Iteration]] | U1 Foundations | provisional-core | PY-04 |
| PY-06 | [[PY-06 Functions, Parameters, Return Values and Scope]] | U2 Functions and Algorithms | provisional-core | PY-05 |
| PY-07 | [[PY-07 Recursion]] | U2 Functions and Algorithms | provisional-core | PY-06 |
| PY-08 | [[PY-08 Algorithmic Thinking, Pseudocode, Flowcharts and Tracing]] | U2 Functions and Algorithms | provisional-core | PY-06 |
| PY-09 | [[PY-09 Strings and String Processing]] | U3 Data Collections | provisional-core | PY-05 |
| PY-10 | [[PY-10 Lists and Tuples]] | U3 Data Collections | provisional-core | PY-06 |
| PY-11 | [[PY-11 Dictionaries, Sets and Comprehensions]] | U3 Data Collections | provisional-core | PY-10 |
| PY-12 | [[PY-12 Searching, Sorting and Complexity]] | U3 Data Collections | provisional-core | PY-08, PY-10 |
| PY-13 | [[PY-13 Modules, Packages, Imports and Virtual Environments]] | U4 Robust Programs | provisional-core | PY-06 |
| PY-14 | [[PY-14 Files, CSV and JSON]] | U4 Robust Programs | provisional-core | PY-11 |
| PY-15 | [[PY-15 Exceptions and Defensive Programming]] | U4 Robust Programs | provisional-core | PY-14 |
| PY-16 | [[PY-16 Classes and Objects]] | U5 Object-Oriented Programming | provisional-core | PY-11, PY-15 |
| PY-17 | [[PY-17 Inheritance, Composition and Polymorphism]] | U5 Object-Oriented Programming | provisional-core | PY-16 |
| PY-18 | [[PY-18 Iterators, Generators, Decorators and Context Managers]] | U5 Object-Oriented Programming | supplementary | PY-17 |
| PY-19 | [[PY-19 Type Hints, Documentation, Clean Code and Refactoring]] | U6 Software Engineering in Python | provisional-core | PY-16 |
| PY-20 | [[PY-20 Testing, Debugging and Test-Driven Development]] | U6 Software Engineering in Python | provisional-core | PY-15, PY-19 |
| PY-21 | [[PY-21 Data Structures and Algorithm Design]] | U6 Software Engineering in Python | provisional-core | PY-12, PY-16 |
| PY-22 | [[PY-22 SQL and Database Integration]] | U7 Integration | provisional-core | PY-15, PY-16 |
| PY-23 | [[PY-23 HTTP APIs and External Services]] | U7 Integration | supplementary | PY-14, PY-15 |
| PY-24 | [[PY-24 Secure Programming and Input Validation]] | U7 Integration | provisional-core | PY-22 |
| PY-25 | [[PY-25 Performance, Packaging and Project Organization]] | U7 Integration | supplementary | PY-13, PY-20 |

**Projects:** [[PRJ-PY-01 Student Marks and Grading System]] (beginner) · [[PRJ-PY-02 Personal Expense Tracker]] (beginner/intermediate) · [[PRJ-PY-03 Library Management System]] (intermediate) · [[PRJ-PY-04 Weather API Client]] (intermediate) · [[PRJ-PY-05 Hostel Maintenance System]] (advanced; also the capstone prototype)

---

## CST06101 Software Design and Development (prefix `SD`)

Dashboard: [[SD 00 Dashboard]] · Map: [[SD 01 Curriculum Map]] · Running case study: [[SD-CASE LabBook Running Case Study]] · [[SD Flawed Design Clinic]]

| ID | Lesson | Unit | Status | Prerequisites |
|---|---|---|---|---|
| SD-01 | [[SD-01 Software Engineering Fundamentals]] | U1 Process | provisional-core | none |
| SD-02 | [[SD-02 Software Process Models]] | U1 Process | provisional-core | SD-01 |
| SD-03 | [[SD-03 Requirements Engineering]] | U2 Requirements | provisional-core | SD-02 |
| SD-04 | [[SD-04 Use Cases, User Stories and Traceability]] | U2 Requirements | provisional-core | SD-03 |
| SD-05 | [[SD-05 Software Architecture and Architectural Styles]] | U3 Design | provisional-core | SD-04 |
| SD-06 | [[SD-06 Modular Design, Cohesion and Coupling]] | U3 Design | provisional-core | SD-05 |
| SD-07 | [[SD-07 UML Class Diagrams]] | U4 Modelling | provisional-core | SD-06, PY-16 |
| SD-08 | [[SD-08 UML Sequence, Activity and State Diagrams]] | U4 Modelling | provisional-core | SD-07 |
| SD-09 | [[SD-09 Data Modeling and Interface Design]] | U4 Modelling | provisional-core | SD-07 |
| SD-10 | [[SD-10 SOLID Principles]] | U5 Design Principles | provisional-core | SD-06, PY-17 |
| SD-11 | [[SD-11 Creational and Structural Design Patterns]] | U5 Design Principles | provisional-core | SD-10 |
| SD-12 | [[SD-12 Behavioral Design Patterns]] | U5 Design Principles | provisional-core | SD-10 |
| SD-13 | [[SD-13 Implementation, Code Organization and Version Control]] | U6 Construction | provisional-core | SD-06 |
| SD-14 | [[SD-14 Software Testing, Verification and Validation]] | U6 Construction | provisional-core | SD-13, PY-20 |
| SD-15 | [[SD-15 Refactoring, Technical Debt, Code Review and Quality]] | U6 Construction | provisional-core | SD-14 |
| SD-16 | [[SD-16 Deployment, Maintenance and Documentation]] | U7 Operation | provisional-core | SD-15 |
| SD-17 | [[SD-17 Secure and Reliable Software Design]] | U7 Operation | provisional-core | SD-05, CS-02 |

---

## Cross-module layer (prefix `X`)

[[X 00 Cross-Module Index]]: [[X-01 Logic and Sets in Python and Requirements]] · [[X-02 Graph Theory in Algorithms, Networks and Scheduling]] · [[X-03 Security Requirements in Software Architecture]] · [[X-04 Testing as Software Quality Assurance]] · [[X-05 Security Risk in Project Management]] · [[X-06 Research Methodology Applied to the Final Year Project]] · [[X-07 Scheduling Your Own Semester with CPM]] · [[X-CASE-01 Secure Exam Results Portal]] · [[X-CASE-02 SME Inventory Rollout]] · [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]]

## Counts

| Module | Lessons | Labs / case studies / artifacts | Projects | Mock assessment |
|---|---|---|---|---|
| CS ITT06102 | 19 | 8 labs | — | [[MOCK-CS-01 Cyber Security Mock Examination]] |
| DM GST06106 | 18 | — | — | [[MOCK-DM-01 Discrete Mathematics Mock Examination]] |
| FYP CST06103 | 12 | 15 templates, 1 workflow | proposal | [[MOCK-FYP-01 Mock Proposal Defense]] |
| PM ITT06105 | 17 | 3 case studies, 11 artifacts | — | [[MOCK-PM-01 IS Project Management Mock Examination]] |
| PY CST06102 | 25 | runnable code bank | 5 | [[MOCK-PY-01 Python Programming Mock Examination]] |
| SD CST06101 | 17 | running case study, design clinic | LabBook | [[MOCK-SD-01 Software Design and Development Mock Examination]] |
