---
title: "BUILD-STATUS"
type: "system"
tags:
  - semester-6
  - system
---

# BUILD-STATUS

The state of the vault at the last build (2026-10-20). What's complete, what isn't, what was verified, and what wasn't. History: [[CHANGELOG]].

## 1. Summary
| Area | State |
|---|---|
| Six modules: dashboards, curriculum maps, lessons | Complete, except **CS-18** (partial; see §3) |
| Lessons | PY 25 · CS 19 · DM 18 · PM 17 · SD 17 · FYP 12 · cross-module 7 |
| Labs and projects | 5 Python projects; 8 CS labs (**LAB-CS-06 note incomplete**; its script and test are complete); LabBook; 3 PM cases, 2 cross-module cases, capstone |
| FYP templates | T01–T15 complete |
| Revision | 6 mocks with marking guides; 6 question banks (216 questions); trackers |
| Navigation and references | Mind maps (7), glossaries (7 + index), Source Register, Citation Conventions, Labs and Projects Index, Progress Tracker |
| Validator | 0 errors, 0 warnings at the last run (see §4) |
| Tests | 917 passing across 14 suites (see §4) |

## 2. Curriculum status
**Provisional.** No official syllabus, outcomes, prescribed texts, assessment formats or past papers were supplied, and web searches found none for these module codes ([[Syllabus Verification Log]]). Module codes, credits and LTP values are exactly as supplied, and the meaning of LTP hasn't been assumed ([[Module Register]]). Outcomes in the dashboards are **designed**, not official. Mocks are **designed practice papers**, not past papers.

## 3. Incomplete items
| Item | State | Why | What exists |
|---|---|---|---|
| [[CS-18 Security Testing and Vulnerability Management]] | Partial: the lesson stops in §5.2; §5.2 (remainder) to §22 are unwritten | Generation of the remaining content was stopped during the build, and it wasn't rewritten | The CVSS v3.1 calculator (`cvss31_base`) and its tests; the note's opening sections. The note carries an "Incomplete note" callout and `status: incomplete`. |
| [[LAB-CS-06 Input Validation and SQL Injection Prevention]] | The lab instructions are unwritten | As above | `scripts/lab06_sqli.py` (complete, offline) and its passing test; the note's card and links. The note carries an "Incomplete note" callout. |

Related practice that *is* complete: [[CS-12 Secure Software Development and Database Security]] (parameterised queries), [[PY-22 SQL and Database Integration]], [[PY-24 Secure Programming and Input Validation]], and the defensive vulnerability-management questions in [[QB-CS Cyber Security Question Bank]].

## 4. Verification performed
### 4.1 Validator
`python "99 - Templates and System/scripts/validate_vault.py"` checks wikilinks (including inside callouts), duplicate names and topic IDs, lesson metadata, near-empty notes, that every Python fence parses, Mermaid diagram keywords, and placeholder markers. Result at the last build: **0 errors, 0 warnings**.

### 4.2 Test suites (all run on CPython 3.13 at the last build)
| Suite | Tests |
|---|---|
| `06 - Python Programming/code/` | 531 |
| `02 - Cyber Security/code/` | 101 |
| `07 - Software Design and Development/code/` (incl. LabBook) | 47 |
| `09 - Revision and Exam Preparation/code/` | 44 |
| `05 - Information System Project Management/code/` | 26 |
| `03 - Discrete Mathematics/code/` | 23 |
| `04 - Final Year Project I/code/` | 11 |
| `08 - Cross-Module Connections/code/` | 9 |
| `10 - …/Cyber Security Labs/` | 8 |
| PRJ-PY-01 / 02 / 03 / 04 / 05 | 20 / 20 / 12 / 20 / 45 |
| **Total** | **917** |

`mypy` was run clean on the LabBook package and on `hostel` (PRJ-PY-05).

### 4.3 Numbers in notes
Every calculation quoted in lessons, cases, mocks and question banks was computed by tested code before being written (the tests name the note or question they cover). Several mistakes were caught that way and corrected before publication (recorded in the git history).

## 5. Not verified (be careful)
| What | Status |
|---|---|
| Sources and links | **None opened or checked**: the build container had no direct network access. See [[Source Register]]. Verify every source before citing it. |
| Open-Meteo API ([[PRJ-PY-04 Weather API Client]]) | Never called live; fixtures are constructed in the documented shape |
| Obsidian rendering | Mermaid diagrams, callouts and Dataview queries weren't viewed in Obsidian; the validator checks syntax only |
| Dataview queries ([[Progress Tracker]], [[Review Schedule]]) | Not run; static fallbacks provided |
| Laws and standards | Cited by name and year (e.g. Tanzania's Personal Data Protection Act, 2022; NIST and ISO documents); their current texts weren't checked |
| Reading-time and effort estimates | Judgement, not measured |

## 6. Known issues
- **LabBook weekly-quota race (open).** Two concurrent bookings by one student on *different* workstations can both pass the weekly quota check: measured 100/100 runs ([[SD-17 Secure and Reliable Software Design]], Practice 7; [[SD-CASE LabBook Running Case Study]] §7). The workstation double-booking race and the quota double counting are fixed, with tests.
- **PRJ-PY-05** is teaching code: no web interface, no MFA (security requirement SR8 is untested and documented as an accepted risk in [[X-03 Security Requirements in Software Architecture]]), no per-IP limiting, no email delivery.
- **Glossaries and the Source Register are generated** from the lessons' Terminology and Sources sections; regenerate them after editing those sections, or they'll drift.

## 7. What you should do next
1. Get your official module descriptors and handbooks, and follow [[Syllabus Verification Log]].
2. Open [[00 Dashboard]] and start the semester plan.
3. Run the validator and the test suites once on your machine (`python -m pytest` in each code folder).
4. Before citing anything, verify it ([[Citation Conventions]]).
