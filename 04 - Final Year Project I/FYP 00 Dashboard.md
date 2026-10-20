---
title: "Final Year Project I Dashboard"
module: "Final Year Project I"
module_code: "CST06103"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - final-year-project
  - dashboard
---

# Final Year Project I: CST06103 Dashboard

**Credits:** 12 · **LTP (as supplied):** 2,2,3 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL. No official FYP handbook, proposal format, assessment weighting or deadlines were supplied (see [[Syllabus Verification Log]]). **Your department's handbook and your supervisor's instructions override everything here.** · **Calculator:** `04 - Final Year Project I/code/fyp_tools.py` (sample sizes, Cronbach's alpha, Likert summaries, SUS score; tested).

> [!warning] Academic integrity
> This vault teaches *how* to do research. It never supplies sources for you to cite without reading them. Every citation in your proposal must be a source **you found, read and verified** (that it exists and says what you claim). See [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]] and [[Citation Conventions]].

> [!todo] ▶ Next step
> Follow [[FYP 02 Idea-to-Defense Workflow]]. If you're new, start with **[[FYP-01 Identifying and Narrowing a Research Problem]]** and fill in [[FYP-T01 Project Idea Evaluation]].

## What is this subject about?
Turning an idea into a defensible **research and development proposal**: a real problem, precise research questions and objectives, a literature review that shows a gap, a justified methodology (often design science for IS projects), requirements and an architecture, a realistic schedule and risk plan, ethical approval, and an oral defence. FYP I typically ends with an approved proposal (and often a prototype or design). FYP II (later) builds and evaluates the system. Confirm this split with your department.

## What should I know before starting?
- Requirements and design: [[SD-03 Requirements Engineering]], [[SD-05 Software Architecture and Architectural Styles]].
- Planning: [[PM-04 Scope Management, Requirements Traceability and WBS]], [[PM-06 Critical Path Method and Float]], [[PM-11 Risk Management]].
- Security and privacy, if you handle user data: [[CS-19 Cloud Security and Privacy]].

## Learning order and lessons
| # | Lesson | Unit | Output (template) |
|---|---|---|---|
| 1 | [[FYP-01 Identifying and Narrowing a Research Problem]] | U1 | [[FYP-T01 Project Idea Evaluation]] |
| 2 | [[FYP-02 Problem Statements, Research Questions, Objectives and Scope]] | U1 | [[FYP-T02 Problem Statement]], [[FYP-T03 Research Questions]], [[FYP-T04 Objectives and Scope]] |
| 3 | [[FYP-03 Literature Searching and Critical Reading]] | U2 | [[FYP-T05 Literature Matrix]] |
| 4 | [[FYP-04 Literature Review Synthesis, Research Gaps and Contribution]] | U2 | [[FYP-T06 Research Gap Analysis]] |
| 5 | [[FYP-05 Research Paradigms and Methodology]] | U3 | [[FYP-T07 Methodology]] |
| 6 | [[FYP-06 Requirements Gathering, Stakeholder and Feasibility Analysis]] | U3 | [[FYP-T08 Requirements Specification]] |
| 7 | [[FYP-07 Data Collection Instruments, Sampling and Evaluation Planning]] | U3 | (methodology chapter sections) |
| 8 | [[FYP-08 Technical Architecture and Design Planning]] | U4 | (design chapter) |
| 9 | [[FYP-09 Project Scheduling, Milestones and Risk Assessment]] | U4 | [[FYP-T09 Work Breakdown Structure]], [[FYP-T10 Project Schedule]], [[FYP-T11 Risk Register]] |
| 10 | [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]] | U5 | [[FYP-T12 Ethics Checklist]] |
| 11 | [[FYP-11 Writing the Research Proposal]] | U6 | [[FYP-T13 Proposal Structure]], [[FYP-T14 Progress Report]] |
| 12 | [[FYP-12 Presentation, Defense and Working with Supervisor Feedback]] | U6 | [[FYP-T15 Presentation and Defense Preparation]] |

Map: [[FYP 01 Curriculum Map]] · Mind map: [[MM-FYP Final Year Project Mind Map]] · Running example: a **hostel maintenance request system** (the same domain as [[PRJ-PY-05 Hostel Maintenance System]] and [[X-CAPSTONE Hostel Maintenance System Full Lifecycle]]).

## What should I read, watch, calculate, code or build?
- **Read:** your department's FYP handbook *first*, then this module in order.
- **Calculate:**
  ```bash
  cd "04 - Final Year Project I/code"
  python -m pytest -q
  python -c "from fyp_tools import *; n0 = cochran_n0(); print(round(n0), finite_correction(n0, 6000))"
  ```
- **Build:** a small prototype or a set of design artefacts if your department expects one in FYP I.

## How do I test my understanding?
- The self-tests in each lesson.
- A supervisor meeting every 1–2 weeks, with a written progress report ([[FYP-T14 Progress Report]]).
- [[MOCK-FYP-01 Mock Proposal Defense]].

## Evidence of mastery (provisional outcomes)
*Designed outcomes, not official ones. Replace them when your handbook is available.*
1. **FYP-LO1** Identify and justify a significant, feasible IS problem.
2. **FYP-LO2** Formulate a precise problem statement, research questions, objectives and scope.
3. **FYP-LO3** Search, critically evaluate and synthesise literature to establish a research gap.
4. **FYP-LO4** Justify a research methodology, data collection and evaluation plan.
5. **FYP-LO5** Plan the technical solution, the schedule and the risks.
6. **FYP-LO6** Address ethics, privacy and academic integrity, and cite correctly.
7. **FYP-LO7** Write and defend a coherent research proposal.

## What remains incomplete?
See [[BUILD-STATUS]]. For your own progress, see [[Progress Tracker]].
