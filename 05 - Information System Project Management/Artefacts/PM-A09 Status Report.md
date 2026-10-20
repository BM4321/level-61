---
title: "Status Report"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A09"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A09 Status Report

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]] at the end of week 10. Lessons: [[PM-10 Earned Value Management]], [[PM-17 Monitoring, Control, Closure and Lessons Learned]]. The EVM figures are tested in `test_case01_week10_evm_pm10`.

**Project:** Course Registration System · **Period:** weeks 9–10 · **PM:** *(name)* · **Date:** end of week 10

## 1. Overall status
| Area | RAG | Criterion (from the plan) | Comment |
|---|---|---|---|
| Schedule | **Amber** | SPI 0.90–0.95, or critical path < 1 week late | SPI 0.926; backend (critical) 0.6 weeks behind |
| Cost | **Red** | CPI < 0.90 | CPI 0.8966 |
| Scope | Green | No unapproved changes | CR-007 decided (deferred SMS; simple report approved) |
| Quality | Green | No open critical defects | 2 minor defects open |
| Risk | Amber | A top risk is materialising | R1 cost portion occurred (server price +1.5 M) |

## 2. Earned value (work-package BAC 54 M)
| PV | EV | AC | SV | CV | SPI | CPI | EAC range |
|---|---|---|---|---|---|---|---|
| 36.5 M | 33.8 M | 37.7 M | −2.7 M | −3.9 M | 0.926 | 0.897 | 57.9–60.2 M (most likely about 60.1 M) |

TCPI to finish at 54 M = 1.24 (not credible); to 60 M = 0.91 (achievable).

## 3. Achievements this period
Servers installed (H). Database design complete (C). Backend 40% done; web UI 50% done.

## 4. Next period
Complete the backend core services; start data migration (I); the first load-test rehearsal.

## 5. Top risks and issues
- **Issue:** server price increase, 1.5 M (drawn from contingency).
- **Risk R3:** key developer workload. Mitigation: pairing started.
- **Risk R5:** peak load. The load test is scheduled for week 14.

## 6. Decisions requested
1. Approve the use of 0.6 M from contingency for a 2-week senior reviewer on the backend (E).
2. Endorse a scope review of the "Could" reporting features, to protect the go-live date.
