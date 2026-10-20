---
title: "Change Request"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A10"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A10 Change Request

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lesson: [[PM-14 Procurement and Change Management]].

| Field | Content |
|---|---|
| CR ID | CR-007 |
| Date raised | Week 9 |
| Requested by | Dean, Faculty of Engineering |
| Title | Course list report with student phone numbers, for SMS reminders |
| Description | A report per course listing registered students and their phone numbers, so the faculty can send SMS reminders |
| Reason / benefit | Fewer missed first lectures |

## Impact analysis
| Dimension | Impact |
|---|---|
| Scope | SMS was explicitly excluded (scope statement); the report is a new deliverable |
| Schedule | About 1 developer-week in E (critical), so +1 week to go-live if added there. Alternative: a simple report using F's float (no impact) |
| Cost | Full request about 0.8 M plus recurring SMS charges; simple report 0.2 M |
| Quality / testing | Extra test cases in G |
| Risk / privacy | Phone numbers are personal data, so a lawful basis and access control are needed ([[CS-19 Cloud Security and Privacy]]) |
| Requirements (RTM) | New R-12 (course list); R-05 (SMS) stays excluded |

## Options
1. Approve in full (+1 week, +0.8 M, privacy work).
2. **Approve the simple course list without phone numbers (0.2 M, no schedule impact); defer SMS to release 2.**
3. Reject.

## Decision
| Decision | Option 2 approved; SMS deferred to release 2 |
|---|---|
| Decided by | Change control board (chair: sponsor's delegate) |
| Date | Week 9 |
| Baselines updated | Scope (R-12), budget (0.2 M from contingency), RTM |
| Communicated to | The dean (letter), the team, the steering committee report |
