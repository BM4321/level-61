---
title: "CHANGELOG"
type: "system"
tags:
  - semester-6
  - system
---

# CHANGELOG

Changes to the vault, newest first. Versions follow the idea of [Semantic Versioning](https://semver.org/) loosely: a **minor** version adds notes or features, a **patch** fixes content. The current state, including what's incomplete, is in [[BUILD-STATUS]].

## 1.0.0 (2026-10-20): first complete build
### Added
- **Revision layer** (`09 - Revision and Exam Preparation/`): six designed mocks with marking guides; six question banks (216 questions); [[Question Bank Index]]; [[Exam Technique and Assessment Strategy]]; [[Review Schedule]]; [[Mistake Log]]; [[Weak Area Tracker]]. A test suite (44 tests) recomputes every answer, executing code snippets taken from the notes.
- **Cross-module layer** (`08 - Cross-Module Connections/`): [[X 00 Cross-Module Index]], X-01 to X-07, [[X-CASE-01 Secure Exam Results Portal]], [[X-CASE-02 SME Inventory Rollout]], [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]], with `x_tools.py` and 9 cross-checking tests.
- **[[PRJ-PY-05 Hostel Maintenance System]]** 1.1.0: layered standard-library package (SQLite, scrypt authentication, state machine, atomic audit trail, optimistic concurrency, insights), 45 tests, mypy clean.
- **Final Year Project I**: FYP-04 to FYP-12, and fifteen templates (FYP-T01 to FYP-T15) in `Project Templates/`; new tested helpers (`citation_crosscheck`, `identifier_scan`, `alignment_gaps`, `word_budget`).
- **References and navigation**: [[Labs and Projects Index]], [[Source Register]] (generated; 344 sources, none verified online), [[Citation Conventions]], seven generated module glossaries and the [[Glossary Index]], six module mind maps and the [[MM Semester Concept Map]], [[Progress Tracker]].

### Changed
- [[PY-24 Secure Programming and Input Validation]] now says the capstone uses scrypt (the implementation), not PBKDF2.
- [[PY-17 Inheritance, Composition and Polymorphism]] and [[PY-25 Performance, Packaging and Project Organization]] describe PRJ-PY-05 as actually built (`HostelRepository`; `README.txt` and `CHANGES.txt`, named so they don't clash with this vault's README and CHANGELOG notes).
- The Master Curriculum Inventory points to `04 - Final Year Project I/Project Templates/`.
- [[Metadata Schema]] documents the `modules` field used by cross-module notes.

## 0.6.0 (2026-10-20): IS Project Management and Final Year Project I (part)
- PM-01 to PM-17, three case studies and eleven filled-in artefacts, with `pm_tools.py` (26 tests).
- FYP dashboard, curriculum map, idea-to-defence workflow, FYP-01 to FYP-09, and `fyp_tools.py`.

## 0.5.0 (2026-10-20): Software Design and Development
- SD-01 to SD-17, the LabBook running case study, the Flawed Design Clinic, pattern code and `sd_tools.py` (47 tests).
### Fixed
- LabBook: a double-counting bug in the weekly quota (regression test added), and the workstation double-booking race (atomic check-and-insert; the strict xfail test became a passing test). The quota race across workstations remains open: see [[BUILD-STATUS]].

## 0.4.0 (2026-10-19 to 2026-10-20): Cyber Security
- CS-01 to CS-19 (CS-18 partial), eight labs with scripts and tests (LAB-CS-06 note incomplete), and `cs_examples.py` (101 tests, including RFC test vectors and a CVSS v3.1 calculator).

## 0.3.0 (2026-10-19): Discrete Mathematics
- DM-01 to DM-18 and the [[DM Python Toolkit]]; every answer machine-checked (23 tests). The validator also checks code inside callouts.

## 0.2.0 (2026-10-19): Python Programming
- PY-01 to PY-25 with the tested code bank, and projects PRJ-PY-01 to PRJ-PY-04 with reference implementations and offline tests.

## 0.1.0 (2026-10-19): foundation
- Vault structure, [[00 Dashboard]], curriculum inventory and [[Module Register]], [[Syllabus Verification Log]], navigation notes, templates, [[Metadata Schema]] and the validator.
