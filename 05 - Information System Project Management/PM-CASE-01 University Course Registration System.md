---
title: "University Course Registration System"
aliases:
  - CASE-01
  - Course registration case
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-CASE-01"
type: "case-study"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - case-study
---

# PM-CASE-01 University Course Registration System

> [!info] About this case
> A **fictional** university replaces paper and queue-based course registration with an online system. It's the running case for the whole module. Every number below comes from `code/pm_tools.py` and is asserted in `tests/test_pm_tools.py` (24 tests pass). Amounts are illustrative TZS values, not real costs.

## 1. Situation
Each semester, about 6,000 students queue at the registry to register for courses. Clashes between timetable slots are found weeks later. Registry staff work overtime, and errors cause late fee disputes. The deputy vice-chancellor (Academic) sponsors a project to put registration online before the next academic year.

## 2. The case through the lessons
| Lesson | What the case shows | Key result |
|---|---|---|
| [[PM-01 Project Fundamentals and Organizational Context]] | A balanced matrix: part-time staff from ICT and the registry | Resource agreements and a steering committee |
| [[PM-03 Project Initiation, Business Case and Charter]] | Option A vs B appraisal | A: NPV 9.67 M, IRR 21.86%, payback 2.5 years |
| [[PM-04 Scope Management, Requirements Traceability and WBS]] | WBS 1.1–1.7; an RTM with R-05 SMS excluded | The scope baseline |
| [[PM-05 Activity Sequencing, Network Diagrams and Gantt Charts]] | 11 activities A–K; 5 paths | Longest path 19 weeks |
| [[PM-06 Critical Path Method and Float]] | Forward and backward pass; crashing | Critical path A-B-E-G-J-K; 15 weeks costs +2.1 M; the floor is 13 weeks |
| [[PM-07 PERT and Schedule Estimation]] | Three-point estimates; simulation | 19.83 ± 1.44 weeks; P(≤21) = 79% (PERT), about 76.5% (simulation) |
| [[PM-08 Resource Allocation and Levelling]] | A developer histogram | Peak 7 → 5 by delaying H and I by 3 weeks; with 4 developers, 23 weeks |
| [[PM-09 Cost Estimation and Budgeting]] | A bottom-up estimate | 54 M work + 6 M contingency = BAC 60 M; re-appraisal needed 22 M a year of benefits |
| [[PM-10 Earned Value Management]] | Week-10 status | SPI 0.926, CPI 0.897, EAC 57.9–60.2 M |
| [[PM-11 Risk Management]] | A 5-risk register; build vs buy | Total EMV 6.0 M (= contingency); pilot-first is the best option (54.64 M) |
| [[PM-12 Stakeholder and Communication Management]] | Power/interest grid; resistant clerks | Champions and an engagement plan |
| [[PM-14 Procurement and Change Management]] | A make-or-buy break-even; CR for the SMS report | 25 months; the CR was deferred, with a simpler report approved |
| [[PM-17 Monitoring, Control, Closure and Lessons Learned]] | RAG at week 10; closure and benefits | Schedule amber, cost red; registrar as benefits owner |

## 3. The network (weeks)
| ID | Activity | d | Pred. | ES | EF | TF |
|---|---|---|---|---|---|---|
| A | Requirements | 3 | — | 0 | 3 | 0 |
| B | System design | 4 | A | 3 | 7 | 0 |
| C | Database design | 2 | A | 3 | 5 | 2 |
| D | Procure servers | 5 | A | 3 | 8 | 4 |
| E | Backend | 6 | B, C | 7 | 13 | 0 |
| F | Web UI | 4 | B | 7 | 11 | 2 |
| G | Integrate and test | 3 | E, F | 13 | 16 | 0 |
| H | Install servers | 2 | D | 8 | 10 | 4 |
| I | Migrate data | 2 | C, H | 10 | 12 | 4 |
| J | UAT and training | 2 | G, I | 16 | 18 | 0 |
| K | Go-live | 1 | J | 18 | 19 | 0 |

## 4. Questions for exam practice
1. Recompute the forward and backward pass, and identify the critical path (PM-06).
2. If D slips 5 weeks, what's the new duration and critical path? (Answer: 20 weeks; A-D-H-I-J-K.)
3. Using the PERT table in PM-07, what deadline gives 95% confidence? (22.21 weeks.)
4. At week 10, compute SV, CV, SPI, CPI and the three EACs (PM-10).
5. Is crashing to 15 weeks worth 2.1 M, compared with deferring "Could" features? Argue both sides.
6. Write the charter, scope statement and closure report using the artefacts below.

## 5. Artefacts (filled in for this case)
[[PM-A01 Project Charter]] · [[PM-A02 Scope Statement]] · [[PM-A03 Work Breakdown Structure]] · [[PM-A04 Project Schedule]] · [[PM-A05 Project Budget]] · [[PM-A06 Risk Register]] · [[PM-A07 Stakeholder Register]] · [[PM-A08 Communication Plan]] · [[PM-A09 Status Report]] · [[PM-A10 Change Request]] · [[PM-A11 Closure Report]]

Back to [[PM 00 Dashboard]]
