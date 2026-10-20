---
title: "Risk Register"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A06"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A06 Risk Register

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lesson: [[PM-11 Risk Management]]. The EMVs are tested in `test_risk_emv_and_decision_tree_pm11`. Review the register at every status meeting.

| ID | Risk (cause → event → effect) | Category | P | Impact (TZS) | EMV | P×I score (1–5) | Response | Owner | Trigger | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| R1 | Vendor lead time → servers late → install and migration delayed | External | 0.30 | 4.0 M | 1.2 M | 3×3 = 9 | Order in week 1; penalty clause; tracking | Procurement officer | No shipping notice by week 5 | Open (cost part occurred: 1.5 M in week 10) |
| R2 | Inconsistent legacy data → extra cleansing | Technical | 0.50 | 3.0 M | 1.5 M | 4×3 = 12 | Profiling spike in week 2; cleansing scripts | DB developer | > 2% invalid in the profile | Mitigated (4% found early) |
| R3 | Senior backend developer leaves → E delayed | Organisational | 0.20 | 6.0 M | 1.2 M | 2×5 = 10 | Pairing, documentation, a second developer | PM | Resignation signals; overtime | Open |
| R4 | Rules change after design → rework | Organisational | 0.40 | 2.5 M | 1.0 M | 3×2 = 6 | Rule freeze; change control | Registrar | A senate agenda item | Open |
| R5 | Peak load → outage on registration day | Technical | 0.25 | 4.4 M | 1.1 M | 2×4 = 8 | Load test at 2×; staggered registration; scale plan | Lead developer | p95 > 2 s in the load test | Open |
| | **Total EMV** | | | | **6.0 M** | | = contingency reserve | | | |

**Opportunities:** the vendor offers a 5% discount for early payment (exploit, if cash allows).

**Change history:** v1.0 week 0; v1.3 week 10 (R1 cost portion occurred; R2 downgraded).
