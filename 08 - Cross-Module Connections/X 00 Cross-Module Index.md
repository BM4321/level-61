---
title: "Cross-Module Index"
module: "Cross-Module"
type: "index"
tags:
  - semester-6
  - cross-module
  - index
---

# X 00 Cross-Module Index

The six modules teach overlapping ideas in different vocabularies. These notes connect them, with worked examples whose numbers are computed by tested code in `08 - Cross-Module Connections/code/` (`x_tools.py`, with tests that also import the PM, CS, SD and FYP calculators, so the modules can't drift apart silently).

> [!todo] ▶ Where to start
> After you have done roughly the first half of each module, read **[[X-01 Logic and Sets in Python and Requirements]]**, then follow the order below. Do the cases after X-05, and run the capstone alongside your FYP.

## Integration lessons
| Note | Connects | The idea in one line |
|---|---|---|
| [[X-01 Logic and Sets in Python and Requirements]] | DM · PY · SD · CS | Requirements are formulas; prove code matches them exhaustively |
| [[X-02 Graph Theory in Algorithms, Networks and Scheduling]] | DM · PY · PM · SD · CS | MSTs, shortest paths, CPM as a longest path, dependency cycles |
| [[X-03 Security Requirements in Software Architecture]] | CS · SD · PY | Threat → requirement → tactic → component → test, traced automatically |
| [[X-04 Testing as Software Quality Assurance]] | SD · PY · PM | QA vs QC; DRE, density, cost of quality, Pareto, control charts |
| [[X-05 Security Risk in Project Management]] | CS · PM | ALE for operations, EMV for projects; justifying controls |
| [[X-06 Research Methodology Applied to the Final Year Project]] | FYP · all | DSR mapped onto the SDLC; every module's method in the FYP |
| [[X-07 Scheduling Your Own Semester with CPM]] | PM · FYP · all | Your hours are the binding resource |

## Integrated cases and capstone
| Note | Scenario | Modules |
|---|---|---|
| [[X-CASE-01 Secure Exam Results Portal]] | A fictional university's results portal: access logic, maker–checker, threat model, plan and business case | CS · SD · PY · PM · DM |
| [[X-CASE-02 SME Inventory Rollout]] | The PM-CASE-02 distributor: reorder rules, design, multi-site security, recovery decisions | PM · SD · PY · CS · DM |
| [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]] | One problem from idea to defended prototype | All six |

## Concept bridges (same idea, different names)
| Idea | DM | PY | SD | PM | CS | FYP |
|---|---|---|---|---|---|---|
| Precedence / dependency | Partial order, DAG | Import graph | Module dependencies | Network diagram | Attack trees (AND/OR) | Research activity order |
| Rule | Proposition | Boolean expression | Business rule, guard | Acceptance criterion | Access policy | Inclusion criterion |
| State | Relation, finite-state machine | Enum + transition table | State diagram | Status (RAG, lifecycle) | Session state | Project stage gate |
| Evidence | Proof | Test | Verification | Quality control | Audit log | Data and analysis |
| Uncertainty | Probability | Random simulation | Risk in design | PERT, EMV, Monte Carlo | ALE, likelihood | Sampling error |

## Code
| File | Used by |
|---|---|
| `code/x_tools.py` | X-01, X-02, X-04, X-05, X-CASE-01, X-CASE-02 |
| `code/tests/test_x_tools.py` | Asserts every quoted number; cross-checks `pm_tools`, `cs_examples`, `sd_tools`, `fyp_tools` and the hostel project's tests |

Run with `python -m pytest` from `08 - Cross-Module Connections/code/`.

Back to [[00 Dashboard]] · [[Master Curriculum Inventory]] · [[Labs and Projects Index]]
