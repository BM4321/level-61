---
title: "Scope Statement"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-A02"
type: "artefact-template"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - template
---

# PM-A02 Scope Statement

> [!info] How to use
> Filled in for [[PM-CASE-01 University Course Registration System]]. Lesson: [[PM-04 Scope Management, Requirements Traceability and WBS]].

## 1. Product scope description
A web-based system that lets students select and register for courses each semester, detects timetable clashes, enforces prerequisites and capacity, and gives registry staff administration and reporting screens.

## 2. Deliverables and acceptance criteria
| Deliverable | Acceptance criteria |
|---|---|
| Requirements specification (1.1.1) | Approved by the registrar; every requirement has an ID and priority |
| Software (1.2) | All Must requirements pass system tests and UAT; p95 ≤ 2 s at 2,000 concurrent users |
| Infrastructure (1.3) | Servers installed, hardened (CS-10 baseline), monitored, backed up |
| Data migration (1.4) | Record counts reconcile; a 200-record sample is 100% correct |
| Training (1.6.1) | 90% of registry staff trained and passing a practical check; a help page live |
| Go-live (1.6.2) | Live in week 19; 2 weeks of hypercare; handover to ICT operations signed |

## 3. Exclusions (out of scope)
Mobile app (release 2) · fee payment integration (separate project) · SMS reminders · timetable creation tool · hardware for faculties.

## 4. Constraints
Go-live before the semester (week 22 at the latest) · budget 60 M baseline · public procurement procedures · university single sign-on mandatory.

## 5. Assumptions
Registration rules frozen at design approval · registry staff are available 2 days a week · the existing student records export is available in CSV.

## 6. Approval
Registrar and sponsor sign. Changes go through [[PM-A10 Change Request]].
