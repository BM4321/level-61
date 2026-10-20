---
title: "Information System Project Management Dashboard"
module: "Information System Project Management"
module_code: "ITT06105"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - project-management
  - dashboard
---

# Information System Project Management: ITT06105 Dashboard

**Credits:** 12 · **LTP (as supplied):** 3,3,0 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL (no official descriptor supplied; see [[Syllabus Verification Log]]) · **Calculator:** `05 - Information System Project Management/code/pm_tools.py`. Every CPM, PERT, EVM, NPV and levelling number in this module is asserted in its tests.

> [!todo] ▶ Next lesson
> The first lesson below whose mastery is below 3. If you are new: **[[PM-01 Project Fundamentals and Organizational Context]]**.

## What is this subject about?
How to plan, run and close information-system projects so that they deliver the agreed value on time and within budget, with the risks, stakeholders, quality and change kept under control. It covers both the **quantitative** tools (network diagrams, critical path, PERT, earned value, NPV) and the **people and process** side (charters, stakeholders, communication, teams, agile).

## What should I know before starting?
- Basic arithmetic and algebra.
- Graphs and paths from [[DM-15 Graphs, Representations, Paths and Connectivity]] (networks).
- Probability from [[DM-18 Introductory Discrete Probability]] (PERT).
- The software lifecycle from [[SD-02 Software Process Models]].

## Learning order and lessons

| # | Lesson | Unit | Status | Key practical output |
|---|---|---|---|---|
| 1 | [[PM-01 Project Fundamentals and Organizational Context]] | U1 Foundations | core | Project vs operations; triple constraint |
| 2 | [[PM-02 Project Lifecycles, Process Groups and Methodologies]] | U1 Foundations | core | Lifecycle choice |
| 3 | [[PM-03 Project Initiation, Business Case and Charter]] | U2 Initiation | core | NPV/IRR/payback; charter |
| 4 | [[PM-04 Scope Management, Requirements Traceability and WBS]] | U3 Planning | core | WBS + dictionary |
| 5 | [[PM-05 Activity Sequencing, Network Diagrams and Gantt Charts]] | U3 Planning | core | Activity-on-node network; Gantt |
| 6 | [[PM-06 Critical Path Method and Float]] | U3 Planning | core | Forward/backward pass; float |
| 7 | [[PM-07 PERT and Schedule Estimation]] | U3 Planning | core | Three-point estimates, probabilities |
| 8 | [[PM-08 Resource Allocation and Levelling]] | U3 Planning | core | Resource histogram, levelling |
| 9 | [[PM-09 Cost Estimation and Budgeting]] | U3 Planning | core | Bottom-up estimate, S-curve |
| 10 | [[PM-10 Earned Value Management]] | U4 Execution & control | core | SV, CV, SPI, CPI, EAC, TCPI |
| 11 | [[PM-11 Risk Management]] | U4 | core | Risk register, EMV |
| 12 | [[PM-12 Stakeholder and Communication Management]] | U4 | core | Power/interest grid; comms plan |
| 13 | [[PM-13 Quality Management]] | U4 | core | Quality plan, cost of quality |
| 14 | [[PM-14 Procurement and Change Management]] | U4 | core | Contracts, change control |
| 15 | [[PM-15 Team Leadership and Conflict Management]] | U5 People | core | RACI; conflict approaches |
| 16 | [[PM-16 Agile, Scrum and Hybrid Delivery]] | U5 | core | Backlog, burndown, velocity |
| 17 | [[PM-17 Monitoring, Control, Closure and Lessons Learned]] | U6 Closing | core | Status and closure reports |

**Case studies:**
- [[PM-CASE-01 University Course Registration System]] (worked through in full: network, CPM, PERT, levelling, EVM)
- [[PM-CASE-02 Wholesale Inventory Management System]]
- [[PM-CASE-03 Small Business Point-of-Sale Software]]

**Artefact templates**, filled in for CASE-01:
- [[PM-A01 Project Charter]] · [[PM-A02 Scope Statement]] · [[PM-A03 Work Breakdown Structure]] · [[PM-A04 Project Schedule]]
- [[PM-A05 Project Budget]] · [[PM-A06 Risk Register]] · [[PM-A07 Stakeholder Register]] · [[PM-A08 Communication Plan]]
- [[PM-A09 Status Report]] · [[PM-A10 Change Request]] · [[PM-A11 Closure Report]]

Map: [[PM 01 Curriculum Map]] · Mind map: [[MM-PM Project Management Mind Map]]

## What should I read, watch, calculate, code or build?
- **Calculate by hand first**, then check with the calculator:
  ```bash
  cd "05 - Information System Project Management/code"
  python -m pytest -q        # all quoted numbers verified
  python -c "from pm_tools import *; print(pert(2, 4, 12))"
  ```
- **Build** the full artefact set for one case (charter → closure report).
- **Apply** CPM to your own semester plan: [[X-07 Scheduling Your Own Semester with CPM]].

## Exercises I must complete
- Levels 1–3 in every lesson, and all the calculation problems in PM-05 to PM-10 by hand.
- One complete case study with every artefact.
- At least one L5 problem in each unit.

## How do I test my understanding?
- Lesson self-tests; checking your hand calculations against `pm_tools`.
- [[MOCK-PM-01 IS Project Management Mock Examination]].

## Evidence of mastery (provisional learning outcomes)
*Designed outcomes, not official ones. Replace them when your module descriptor is available.*
1. **PM-LO1** Explain project management concepts, lifecycles and the organisational context of IS projects.
2. **PM-LO2** Prepare initiation documents, including a business case appraised with NPV, IRR and payback.
3. **PM-LO3** Plan scope, schedule (network, CPM, PERT), resources and cost for an IS project.
4. **PM-LO4** Monitor and control performance with earned value, and manage risk, quality, change and procurement.
5. **PM-LO5** Manage stakeholders, communication and teams, including agile and hybrid delivery.
6. **PM-LO6** Close projects and capture lessons learned.

| Evidence | Demonstrates |
|---|---|
| Hand calculations matching `pm_tools` for CPM, PERT and EVM | LO3, LO4 |
| A full artefact set for one case | LO2–LO6 |
| Mock exam ≥ 60% | All |

## What remains incomplete?
See [[BUILD-STATUS]]. For your own progress, see [[Progress Tracker]].
