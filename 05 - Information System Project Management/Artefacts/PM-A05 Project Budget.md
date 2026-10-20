---
title: "Project Budget"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A05"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A05 Project Budget

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lesson: [[PM-09 Cost Estimation and Budgeting]]. The figures are illustrative TZS values, tested in `test_cost_baseline_pm09`.

## 1. Bottom-up estimate
| WBS | Activity | Basis | Cost |
|---|---|---|---|
| 1.1.1 | A Requirements | 2 people × 15 days × 100,000 | 3,000,000 |
| 1.1.2 | B System design | 2 × 20 days × 150,000 | 6,000,000 |
| 1.1.3 | C Database design | 2 × 10 days × 150,000 | 3,000,000 |
| 1.3.1 | D Servers | Vendor quotation | 12,000,000 |
| 1.2.1 | E Backend | 3 × 30 days × 133,333 | 12,000,000 |
| 1.2.2 | F Web UI | 2 × 20 days × 150,000 | 6,000,000 |
| 1.2.3/1.5.1 | G Integration and test | 3 × 15 days × 100,000 | 4,500,000 |
| 1.3.2 | H Installation | Vendor service + technician | 2,000,000 |
| 1.4 | I Migration | 2 × 10 days × 125,000 | 2,500,000 |
| 1.5.2/1.6.1 | J UAT and training | 2 × 10 days × 120,000 | 2,400,000 |
| 1.6.2 | K Go-live | 1 × 5 days × 120,000 | 600,000 |
| | **Work packages** | | **54,000,000** |
| | Contingency reserve (= total risk EMV, [[PM-A06 Risk Register]]) | | 6,000,000 |
| | **Cost baseline (BAC)** | | **60,000,000** |
| | Management reserve (sponsor) | | 4,000,000 |
| | **Total budget** | | **64,000,000** |

## 2. Time-phased PV (cumulative, TZS millions, end of each week)
| Week | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| PV | 1.0 | 2.0 | 3.0 | 8.4 | 13.8 | 17.7 | 21.6 | 27.5 | 32.0 | 36.5 |

| Week | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 |
|---|---|---|---|---|---|---|---|---|---|
| PV | 41.25 | 44.5 | 46.5 | 48.0 | 49.5 | 51.0 | 52.2 | 53.4 | 54.0 |

## 3. Recurring costs (after go-live, per year, estimates)
Server support and power 2.0 M · licences 0.8 M · a 0.3 FTE support developer 4.0 M. Include them in the TCO and in the operations budget.

## 4. Controls
- The PM may move up to 5% between work packages.
- Contingency is drawn down via the change log.
- Management reserve is released only by the sponsor.
