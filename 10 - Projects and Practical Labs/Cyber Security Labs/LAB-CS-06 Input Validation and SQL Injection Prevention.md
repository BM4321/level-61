---
title: "Input Validation and SQL Injection Prevention"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-06"
type: "lab"
difficulty: "intermediate"
status: "incomplete"
mastery: 0
prerequisites:
  - "[[CS-12 Secure Software Development and Database Security]]"
  - "[[PY-22 SQL and Database Integration]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-06 Input Validation and SQL Injection Prevention

> [!danger] Ethics and scope
> All injection happens against an **in-memory SQLite database that the script creates** and discards when it exits. Never try injection payloads against any website, form or database that you don't own or aren't authorised in writing to test. Doing so may be a crime, even if "nothing happens".

**Script:** `scripts/lab06_sqli.py` · **Tests:** `tests/test_labs.py::test_lab06` (passing) · **Time:** 60–90 min · **Related lessons:** [[CS-12 Secure Software Development and Database Security]], [[CS-11 Web Application Security]], [[PY-22 SQL and Database Integration]], [[PY-24 Secure Programming and Input Validation]]

## Objectives
1. See exactly how string-built SQL turns input into code: authentication bypass, and data extraction with `UNION`.
2. Fix the code with parameterised queries, server-side validation (an allow-list regular expression) and salted password hashing.
3. Show that parameters keep a payload as data even when validation is bypassed: defence in depth.
4. Practise writing tests that prove the fix.

## Prerequisites
- Python 3.10+ (standard library `sqlite3`, `hashlib`, `re`).
- Basic SQL (`SELECT … WHERE`, `UNION`).

> [!todo] Incomplete note
> The lab instructions (setup through to the mastery checklist) haven't been written yet. This is recorded in BUILD-STATUS. The script `scripts/lab06_sqli.py` is complete and runs offline against an in-memory database, and `tests/test_labs.py::test_lab06` passes; read the script's comments for the procedure.

## Links
[[CS-12 Secure Software Development and Database Security]] · [[LAB-CS-05 Security Headers and Configuration Analysis]] · [[LAB-CS-07 Threat Modeling a Sample Web Application]]
