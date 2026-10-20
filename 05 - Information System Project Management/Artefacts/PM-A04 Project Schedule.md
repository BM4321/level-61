---
title: "Project Schedule"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A04"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A04 Project Schedule

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lessons: [[PM-05 Activity Sequencing, Network Diagrams and Gantt Charts]], [[PM-06 Critical Path Method and Float]], [[PM-07 PERT and Schedule Estimation]]. Every value is from `pm_tools` (tested).

## 1. Activity table (weeks; week 0 = project start)
| ID | Activity | d | Pred. | ES | EF | LS | LF | TF | Owner |
|---|---|---|---|---|---|---|---|---|---|
| A | Requirements | 3 | — | 0 | 3 | 0 | 3 | 0 | BA |
| B | System design | 4 | A | 3 | 7 | 3 | 7 | 0 | Lead dev |
| C | Database design | 2 | A | 3 | 5 | 5 | 7 | 2 | DB dev |
| D | Procure servers | 5 | A | 3 | 8 | 7 | 12 | 4 | Procurement |
| E | Backend | 6 | B, C | 7 | 13 | 7 | 13 | 0 | Lead dev |
| F | Web UI | 4 | B | 7 | 11 | 9 | 13 | 2 | UI dev |
| G | Integrate and test | 3 | E, F | 13 | 16 | 13 | 16 | 0 | Tester |
| H | Install servers | 2 | D | 8 | 10 | 12 | 14 | 4 | ICT |
| I | Migrate data | 2 | C, H | 10 | 12 | 14 | 16 | 4 | DB dev |
| J | UAT and training | 2 | G, I | 16 | 18 | 16 | 18 | 0 | Registrar |
| K | Go-live | 1 | J | 18 | 19 | 18 | 19 | 0 | PM |

**Critical path:** A-B-E-G-J-K = 19 weeks.

## 2. Probabilistic view
PERT 19.83 ± 1.44 weeks. P(≤ 21) = 79% (PERT), about 76.5% (simulation). The internal target is week 20; the external commitment is week 22.

## 3. Resource view
Peak 7 developers at early start. Levelled to 5 by delaying H and I by 3 weeks (no change to the end date). Hard limit of 4 developers: 23 weeks ([[PM-08 Resource Allocation and Levelling]]).

## 4. Baseline and change control
This is the baseline v1.0. Changes go through [[PM-A10 Change Request]]. Report progress in [[PM-A09 Status Report]].
