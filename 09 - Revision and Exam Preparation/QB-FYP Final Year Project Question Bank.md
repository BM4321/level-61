---
title: "Final Year Project Question Bank"
module: "Final Year Project I"
module_code: "CST06103"
topic_id: "QB-FYP"
type: "question-bank"
tags:
  - semester-6
  - final-year-project
  - exam
---

# QB-FYP Final Year Project Question Bank

> [!info] How to use
> Two questions per lesson. Answer closed book, then open the folded answer. Computed answers (sample sizes, SUS, Likert summaries, Boolean queries) are checked with `fyp_tools.py` in `09 - Revision and Exam Preparation/code/tests/test_qb.py` (`test_qb_fyp_numbers`). Log misses in [[Mistake Log]].

## [[FYP-01 Identifying and Narrowing a Research Problem]]

**Q1 (L1).** Is "an app for hostel maintenance" a research problem?

> [!success]- Answer
> No: it's a solution. The problem is the evidenced gap (e.g. lost requests and no prioritisation, affecting residents' safety).

**Q2 (L2).** Give the six criteria for a good FYP problem.

> [!success]- Answer
> Significant, feasible, researchable, a clear contribution, ethical, supervisable.

## [[FYP-02 Problem Statements, Research Questions, Objectives and Scope]]

**Q3 (L2).** What are the five parts of a problem statement?

> [!success]- Answer
> Context and the ideal; the current reality with evidence; the gap and its causes; consequences; the purpose of the study.

**Q4 (L2).** Delimitation vs limitation?

> [!success]- Answer
> A delimitation is a boundary you chose (one university's hostels); a limitation is a constraint you can't avoid (a small sample).

## [[FYP-03 Literature Searching and Critical Reading]]

**Q5 (L2).** Build a Boolean query for concepts {hostel, student housing}, {maintenance, repair\*}, {system, app}.

> [!success]- Answer
> `(hostel OR "student housing") AND (maintenance OR repair*) AND (system OR app)`.

**Q6 (L2).** `10.1000/xyz123` passes a DOI syntax check. Does that mean the source exists?

> [!success]- Answer
> No. Syntax proves nothing: resolve it at doi.org, find the paper, and read it before citing.

## [[FYP-04 Literature Review Synthesis, Research Gaps and Contribution]]

**Q7 (L2).** What's the difference between summarising and synthesising sources?

> [!success]- Answer
> Summarising describes sources one by one; synthesising organises them by theme, comparing where they agree and differ, to build an argument.

**Q8 (L3).** How do you show (not assert) a research gap?

> [!success]- Answer
> Compare the reviewed work against criteria from your problem, with citations in each cell, and state what none of it addresses.

## [[FYP-05 Research Paradigms and Methodology]]

**Q9 (L2).** Why does design science research suit many IS projects?

> [!success]- Answer
> The aim is to build and rigorously evaluate an artefact that solves an identified problem; DSR treats construction and evaluation as knowledge production.

**Q10 (L1).** Is Scrum a research methodology?

> [!success]- Answer
> No: it's a software process framework; it can organise the build within a DSR study.

## [[FYP-06 Requirements Gathering, Stakeholder and Feasibility Analysis]]

**Q11 (L2).** Name four elicitation techniques, and when to use each.

> [!success]- Answer
> Interviews (depth with key people), questionnaires (breadth), observation (tacit work practice), document analysis (existing forms, logs); workshops and prototyping for validation.

**Q12 (L2).** List the five feasibility dimensions.

> [!success]- Answer
> Technical, operational, economic, schedule, legal and ethical.

## [[FYP-07 Data Collection Instruments, Sampling and Evaluation Planning]]

**Q13 (L3).** Population 800, 95% confidence, ±5%. Compute the sample with Cochran plus the finite correction, and with Yamane. How many invitations at a 40% response rate (for 260)?

> [!success]- Answer
> Cochran + FPC: **260**; Yamane: **267**; invitations: **650**.

**Q14 (L3).** A participant answers 4, 2, 4, 2, 4, 2, 4, 2, 4, 2 on the SUS. Their score?

> [!success]- Answer
> Odd items contribute 3 each (15), even items 3 each (15): 30 × 2.5 = **75**.

## [[FYP-08 Technical Architecture and Design Planning]]

**Q15 (L2).** What must justify your technology choices in the proposal?

> [!success]- Answer
> The requirements and constraints (skills, hosting, cost, data, security), compared against alternatives, not preference alone.

**Q16 (L2).** Which design artefacts belong in a proposal's design chapter?

> [!success]- Answer
> An architecture diagram, key models (use cases, ERD, a sequence or state diagram), and technology choices with justification; detail goes in appendices.

## [[FYP-09 Project Scheduling, Milestones and Risk Assessment]]

**Q17 (L2).** Why is ethics approval often on the FYP critical path?

> [!success]- Answer
> Others control its timing, it can take weeks, and every participant-facing activity depends on it.

**Q18 (L2).** How should exam weeks appear in your plan?

> [!success]- Answer
> As reduced availability (a resource calendar); schedule non-critical work there.

## [[FYP-10 Research Ethics, Privacy, Academic Integrity and Citation]]

**Q19 (L2).** Anonymous vs pseudonymous data?

> [!success]- Answer
> Anonymous data can't be linked to anyone; pseudonymous data can, through a protected key, so it's still personal data.

**Q20 (L2).** Fabrication vs falsification?

> [!success]- Answer
> Fabrication invents data, results or sources; falsification manipulates real data, methods or results.

## [[FYP-11 Writing the Research Proposal]]

**Q21 (L1).** Which tense for planned work in a proposal?

> [!success]- Answer
> Future ("interviews will be conducted").

**Q22 (L2).** Ten Likert answers to an item: 5, 4, 4, 3, 2, 4, 5, 1, 4, 3. Report the median, the mode and the % agree (4–5).

> [!success]- Answer
> Median **4**, mode **4**, **60%** agree. Report the median for ordinal data (the mean is 3.5).

## [[FYP-12 Presentation, Defense and Working with Supervisor Feedback]]

**Q23 (L2).** Give the five-step pattern for answering a panel question.

> [!success]- Answer
> Listen; pause; answer briefly; support with evidence; acknowledge limitations (and if you don't know, say so and how you'd find out).

**Q24 (L2).** What does a feedback log record?

> [!success]- Answer
> Each comment and its source, your response, where it was addressed, and its status (planned, done, declined with a reason).

Back to [[Question Bank Index]] · [[MOCK-FYP-01 Mock Proposal Defense]] · [[FYP 00 Dashboard]]
