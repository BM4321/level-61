---
title: "Labs and Projects Index"
type: "index"
tags:
  - semester-6
  - project
  - lab
  - index
---

# Labs and Projects Index

All practical work in the vault, with what it builds and how to check it. Every code folder has its own tests; run `python -m pytest` inside it. The counts below were measured at the last build ([[BUILD-STATUS]]).

> [!warning] Safety and scope
> Security labs use only local, constructed data and your own files. Test only systems you own or have written permission to assess, and use intentionally vulnerable training environments for any exploitation practice. The teaching code here is **not** production-ready; each project lists what a real deployment would need.

## Python projects (CST06102)
| Project | Level | Builds | Tests |
|---|---|---|---|
| [[PRJ-PY-01 Student Marks and Grading System]] | Beginner | Functions, validation, grading, reports | 20 |
| [[PRJ-PY-02 Personal Expense Tracker]] | Beginner–intermediate | Files (CSV/JSON), summaries, CLI | 20 |
| [[PRJ-PY-03 Library Management System]] | Intermediate | Classes, invariants, exceptions, reservation queue | 12 |
| [[PRJ-PY-04 Weather API Client]] | Intermediate | HTTP client design, error handling, caching, tests without the network | 20 |
| [[PRJ-PY-05 Hostel Maintenance System]] | Advanced | Layered package, SQLite, scrypt authentication, state machine, audit trail, CLI | 45 |

## Cyber security labs (ITT06102)
Scripts and tests in `10 - Projects and Practical Labs/Cyber Security Labs/` (8 tests, one per lab).

| Lab | Focus | Status |
|---|---|---|
| [[LAB-CS-01 Password Strength and Secure Password Storage]] | Policy checks, KDF storage | Complete |
| [[LAB-CS-02 Hashing and Integrity Verification]] | SHA-256, manifests, tamper detection | Complete |
| [[LAB-CS-03 Toy Ciphers and Why They Fail]] | Classical ciphers and their weaknesses (toys, never for real use) | Complete |
| [[LAB-CS-04 File Permission Audit]] | Risky permission bits on your own files | Complete |
| [[LAB-CS-05 Security Headers and Configuration Analysis]] | Header and cookie-flag findings | Complete |
| [[LAB-CS-06 Input Validation and SQL Injection Prevention]] | Validation and parameterised queries | **Incomplete** (see the note and [[BUILD-STATUS]]) |
| [[LAB-CS-07 Threat Modeling a Sample Web Application]] | DFD, STRIDE, security requirements | Complete |
| [[LAB-CS-08 Log Analysis and Incident Response]] | Parsing a constructed auth log, bursts, response steps | Complete |

## Case studies and design work
| Item | Module | What you do |
|---|---|---|
| [[SD-CASE LabBook Running Case Study]] | SD | Follow one system through all SD lessons; `07 - Software Design and Development/code/labbook/` (part of the SD suite's 47 tests) |
| [[SD Flawed Design Clinic]] | SD | Diagnose and refactor flawed designs |
| [[PM-CASE-01 University Course Registration System]] | PM | CPM, PERT, EVM and risk on one project, with filled-in artefacts (PM-A01 to PM-A11) |
| [[PM-CASE-02 Wholesale Inventory Management System]] | PM | Behind schedule, under budget |
| [[PM-CASE-03 Small Business Point-of-Sale Software]] | PM | Delivery choice: build vs SaaS, NPV, agile forecasting |
| [[X-CASE-01 Secure Exam Results Portal]] | All | Access logic, maker–checker, threat model, plan and business case |
| [[X-CASE-02 SME Inventory Rollout]] | All | Reorder rules, design, multi-site security, recovery |

## Capstone and FYP
- [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]]: idea to defended prototype, using all six modules.
- FYP templates T01–T15 in `04 - Final Year Project I/Project Templates/`, starting with [[FYP-T01 Project Idea Evaluation]]; the workflow is [[FYP 02 Idea-to-Defense Workflow]].

## Code banks and calculators
| Folder | Contents | Tests |
|---|---|---|
| `06 - Python Programming/code/` | Lesson code bank | 531 |
| `03 - Discrete Mathematics/code/` | DM toolkit ([[DM Python Toolkit]]) | 23 |
| `02 - Cyber Security/code/` | `cs_examples.py` (defensive examples) | 101 |
| `05 - Information System Project Management/code/` | `pm_tools.py` (CPM, PERT, EVM, finance, risk) | 26 |
| `07 - Software Design and Development/code/` | LabBook, patterns, `sd_tools.py`, the clinic | 47 |
| `04 - Final Year Project I/code/` | `fyp_tools.py` (sampling, reliability, SUS, citations) | 11 |
| `08 - Cross-Module Connections/code/` | `x_tools.py` and cross-module checks | 9 |
| `09 - Revision and Exam Preparation/code/` | Mock and question-bank answer checks | 44 |

Back to [[00 Dashboard]] · [[X 00 Cross-Module Index]]
