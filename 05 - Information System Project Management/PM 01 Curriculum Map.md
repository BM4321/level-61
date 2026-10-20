---
title: "IS Project Management Curriculum Map"
module: "Information System Project Management"
module_code: "ITT06105"
type: "curriculum-map"
syllabus_status: "provisional"
tags:
  - semester-6
  - project-management
  - curriculum
---

# IS Project Management: Curriculum Map

Back to [[PM 00 Dashboard]]

## 1. Units
| Unit | Lessons | Artefacts |
|---|---|---|
| U1 Foundations | PM-01, PM-02 | — |
| U2 Initiation | PM-03 | A01 Charter |
| U3 Planning | PM-04 to PM-09 | A02 Scope, A03 WBS, A04 Schedule, A05 Budget |
| U4 Execution and control | PM-10 to PM-14 | A06 Risk register, A07 Stakeholder register, A08 Comms plan, A09 Status report, A10 Change request |
| U5 People and delivery approaches | PM-15, PM-16 | (RACI inside A08) |
| U6 Closing | PM-17 | A11 Closure report |

## 2. Prerequisite graph
```mermaid
flowchart TD
    P1[PM-01 Fundamentals] --> P2[PM-02 Lifecycles]
    P2 --> P3[PM-03 Initiation & business case]
    P3 --> P4[PM-04 Scope & WBS]
    P4 --> P5[PM-05 Networks & Gantt]
    P5 --> P6[PM-06 CPM & float]
    P6 --> P7[PM-07 PERT]
    P6 --> P8[PM-08 Resources]
    P4 --> P9[PM-09 Cost & budget]
    P9 --> P10[PM-10 Earned value]
    P6 --> P10
    P3 --> P11[PM-11 Risk]
    P7 --> P11
    P3 --> P12[PM-12 Stakeholders & comms]
    P4 --> P13[PM-13 Quality]
    P4 --> P14[PM-14 Procurement & change]
    P12 --> P15[PM-15 Teams & conflict]
    P2 --> P16[PM-16 Agile & hybrid]
    P10 --> P17[PM-17 Control & closure]
    P14 --> P17
```
*Text version: fundamentals and lifecycles lead to initiation. Initiation leads to scope (WBS), which drives scheduling (network → CPM → PERT and resources) and cost (→ earned value). Risk, stakeholders, quality and procurement build on initiation and scope. Teams follow stakeholders. Agile builds on lifecycles. Control and closure come last.*

## 3. Review alerts
| Before… | Review | Why |
|---|---|---|
| PM-05/06 | [[DM-15 Graphs, Representations, Paths and Connectivity]] | Networks as directed acyclic graphs; longest path |
| PM-07 | [[DM-18 Introductory Discrete Probability]] | Expected value, variance, the normal approximation |
| PM-03 | [[DM-08 Sequences and Summations]] | Discounting as a geometric-style sum |
| PM-04 | [[SD-04 Use Cases, User Stories and Traceability]] | Requirements traceability |
| PM-11 | [[CS-16 Risk Analysis, Policy, Governance and Compliance]] | The same risk vocabulary in security |
| PM-16 | [[SD-02 Software Process Models]] | Scrum and Kanban from the engineering side |

## 4. Cross-module links
[[X-02 Graph Theory in Algorithms, Networks and Scheduling]] · [[X-05 Security Risk in Project Management]] · [[X-07 Scheduling Your Own Semester with CPM]] · [[FYP-09 Project Scheduling, Milestones and Risk Assessment]] · [[X-CASE-02 SME Inventory Rollout]]
