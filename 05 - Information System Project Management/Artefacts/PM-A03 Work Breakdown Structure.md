---
title: "Work Breakdown Structure"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A03"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A03 Work Breakdown Structure

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lesson: [[PM-04 Scope Management, Requirements Traceability and WBS]]. Rule: deliverables (nouns), the 100% rule, and work packages small enough to estimate and assign.

## 1. WBS (outline)
```text
1.0 Course Registration System
 1.1 Requirements & design
   1.1.1 Requirements specification          -> activity A
   1.1.2 System design                       -> activity B
   1.1.3 Database design                     -> activity C
 1.2 Software
   1.2.1 Backend services                    -> activity E
   1.2.2 Student web UI                      -> activity F
   1.2.3 Integration build                   -> activity G (with 1.5.1)
 1.3 Infrastructure
   1.3.1 Server procurement                  -> activity D
   1.3.2 Server installation                 -> activity H
 1.4 Data migration                          -> activity I
 1.5 Testing & acceptance
   1.5.1 System & performance test           -> activity G
   1.5.2 UAT & sign-off                      -> activity J
 1.6 Deployment & training
   1.6.1 Training                            -> activity J
   1.6.2 Go-live & hypercare                 -> activity K
 1.7 Project management (charter, plans, reporting, closure)
```

## 2. WBS dictionary (sample entries)
| Code | Deliverable | Owner | Acceptance | Estimate | Depends on |
|---|---|---|---|---|---|
| 1.1.1 | Requirements specification | Business analyst | Approved by the registrar | 3 weeks, 3.0 M | — |
| 1.2.1 | Backend services (registration, clash detection, rules) | Lead developer | ST cases ST-01–ST-12 pass | 6 weeks, 12.0 M | 1.1.2, 1.1.3 |
| 1.3.1 | Servers delivered to specification | Procurement officer | Delivery note + acceptance test | 5 weeks, 12.0 M | 1.1.1 |
| 1.4 | Migrated enrolments + reconciliation report | Database developer | Counts match; 0 errors in a 200-record sample | 2 weeks, 2.5 M | 1.1.3, 1.3.2 |
| 1.6.2 | Live system + 2 weeks of hypercare | PM | Handover signed by ICT operations | 1 week, 0.6 M | 1.5.2 |

The work-package total is 54 M ([[PM-A05 Project Budget]]).
