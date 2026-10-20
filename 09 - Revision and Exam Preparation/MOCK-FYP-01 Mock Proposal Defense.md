---
title: "Mock Proposal Defense"
module: "Final Year Project I"
module_code: "CST06103"
topic_id: "MOCK-FYP-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - final-year-project
  - exam
---

# MOCK-FYP-01 Mock Proposal Defense

> [!warning] A designed simulation
> No official defence format or marking scheme was supplied. This mock uses a **designed** format: a 12-minute presentation, 15 minutes of questions, and a written critique task. Replace it with your department's format. The numbers in the critique are computed with `fyp_tools.py` in `09 - Revision and Exam Preparation/code/tests/test_mock_fyp.py`.

**Prepare with:** [[FYP-12 Presentation, Defense and Working with Supervisor Feedback]] and [[FYP-T15 Presentation and Defense Preparation]].

---

## Part 1: your presentation (run it with peers as the panel)

**Timing (12 minutes = 720 s, weights 2, 2, 3, 2, 2, 1):** problem and RQs 120 s · literature and gap 120 s · methodology 180 s · design plan 120 s · work plan and ethics 120 s · summary 60 s. Rehearse with a timer; the panel stops you at 12 minutes.

**Panel instructions.** Three peers act as the panel: one chair (keeps time, asks the opening question), one methodology examiner, one technical examiner. Each asks at least two questions from the bank below, plus one of their own, then scores the presenter with the rubric (Part 3).

## Part 2: question bank for the panel
| # | Type | Question | Strong answer contains |
|---|---|---|---|
| 1 | Significance | "Why does this problem matter, and to whom?" | Evidence (with its source and n), affected stakeholders, consequences |
| 2 | Significance | "What happens if nothing is done?" | Concrete consequences from the evidence, not speculation |
| 3 | Gap | "How is this different from existing systems?" | The comparison table; what none of them do; citations to sources actually read |
| 4 | Gap | "Name the most relevant study you reviewed and its main limitation." | A specific source, accurately described |
| 5 | Methodology | "Why design science and not a survey?" | The aim is to build and evaluate an artefact; surveys are used within DSR for RQ1 and RQ4 |
| 6 | Methodology | "How will you know the system works?" | Evaluation measures mapped to RQs: task success, SUS, interviews; targets |
| 7 | Sampling | "Why that many participants?" | A calculation for the survey; saturation for interviews; feasibility; limitations |
| 8 | Ethics | "How will you protect participants' data?" | Consent, minimisation, pseudonymisation, storage, retention, approval status |
| 9 | Feasibility | "What's your biggest risk, and what will you do about it?" | A risk from the register, with a response and a trigger |
| 10 | Feasibility | "What will you cut if you run late?" | Pre-agreed priorities ("could" requirements first), not "I won't run late" |
| 11 | Technical | "Why this technology stack?" | Choices justified against the requirements and constraints |
| 12 | Technical | "How does your design prevent one user seeing another's data?" | Server-side authorisation in the service layer; tests |
| 13 | Contribution | "What will others learn from your project?" | The contribution statement, matched to the evaluation |
| 14 | Integrity | "Did you use AI tools? How did you check your references?" | An honest account, according to the institution's policy; every source found and read |
| 15 | Challenge | "Isn't this just a CRUD app?" | The research problem, the context-specific requirements, the evaluation; acknowledge what's routine |

## Part 3: panel rubric (designed, 50 marks)
| Criterion | 0–2 | 3–4 | 5–6 | 7–8 | Max |
|---|---|---|---|---|---|
| Problem and significance | Asserted | Some evidence | Evidenced | Evidenced, specific, consequences clear | 8 |
| RQs, objectives, alignment | Unclear | Partly aligned | Aligned | Precise and aligned | 8 |
| Literature and gap | List of sources | Some comparison | Clear gap | Gap follows from synthesis | 8 |
| Methodology and evaluation | Unjustified | Partly mapped | Mapped to RQs | Justified against alternatives | 8 |
| Plan, risks and ethics | Missing | Vague | Realistic | Realistic, with responses and approvals | 8 |
| Presentation and answers | Over time; evasive | Some clarity | Clear, on time | Clear, evidenced, honest about limits | 10 |

(The last row is out of 10: award 9–10 for answers that are concise, evidenced and candid about limitations.)

---

## Part 4: written critique (30 minutes, 20 marks)
Read this **fictional** proposal excerpt and identify **five** problems. For each, explain why it's a problem and how to fix it.

> "**1.2 Problem.** 85% of hostel residents are dissatisfied with maintenance (Smith, 2023). **1.3 Research question.** What factors affect student satisfaction with hostel services? **1.4 Objectives.** (i) To develop a web-based maintenance system. (ii) To make it user-friendly. **3.4 Sampling.** A random sample of 100 of the 2,400 residents gives a margin of error of ±5% at 95% confidence. **3.6 Evaluation.** The system will be evaluated by the developer, who will confirm that all features work. **3.7 Ethics.** No ethical issues arise because the system is for the university's benefit."

> [!success]- Marking guide for Part 4
> 1. **An unattributed or unverifiable statistic.** "85% … (Smith, 2023)": is this a real, read source about *this* context? If it isn't verifiable, it must be removed; use your own preliminary evidence with n. *(4.)*
> 2. **Misalignment.** The RQ is a broad satisfaction study (survey research), but the objectives are about building a system. Narrow the RQs to the maintenance process, the requirements, the design and its evaluation ([[FYP-02 Problem Statements, Research Questions, Objectives and Scope]] Example 3). *(4.)*
> 3. **Objectives aren't SMART.** "User-friendly" isn't measurable; turn it into an evaluation objective with a measure (e.g. a SUS score and task success with residents). *(4.)*
> 4. **Wrong sample-size claim.** With N = 2,400 at 95% confidence, ±5% needs **332** responses (`finite_correction(cochran_n0(), 2400)`), so about **664** invitations at a 50% response rate. With n = 100 the margin is about **±9.6%**. Fix the calculation, or state the larger margin honestly. *(4.)*
> 5. **Evaluation and ethics.** Self-evaluation by the developer isn't evidence for RQs about users; plan a usability study with real users. And any study with human participants raises ethical issues (consent, data protection, power relationships), whoever benefits; ethics approval is needed ([[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]]). *(4; either point earns the marks if well explained.)*

## Part 5: after the mock
1. Total your panel scores; anything below 5 of 8 goes to your [[Weak Area Tracker]].
2. Log every question you struggled with, and a better answer, in [[Mistake Log]].
3. Update your slides and backup slides; rehearse again within 3 days.

Back to [[Exam Technique and Assessment Strategy]] · [[QB-FYP Final Year Project Question Bank]] · [[FYP 00 Dashboard]]
