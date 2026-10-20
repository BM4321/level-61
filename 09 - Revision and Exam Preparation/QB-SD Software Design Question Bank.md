---
title: "Software Design Question Bank"
module: "Software Design and Development"
module_code: "CST06101"
topic_id: "QB-SD"
type: "question-bank"
tags:
  - semester-6
  - software-design
  - exam
---

# QB-SD Software Design Question Bank

> [!info] How to use
> Two questions per lesson. Answer closed book, then open the folded answer. Computed answers (requirement smells, instability) are checked in `09 - Revision and Exam Preparation/code/tests/test_qb.py` (`test_qb_sd_numbers`). Log misses in [[Mistake Log]].

## [[SD-01 Software Engineering Fundamentals]]

**Q1 (L1).** Why is software engineering more than programming?

> [!success]- Answer
> It covers the whole lifecycle (requirements, design, verification, deployment, maintenance) and the process, people and quality concerns of building systems that others depend on, over time.

**Q2 (L2).** Name four software quality attributes, with a measurable example of one.

> [!success]- Answer
> Usability, reliability, performance, security, maintainability, portability. E.g. performance: "95% of searches return within 2 s at 50 concurrent users".

## [[SD-02 Software Process Models]]

**Q3 (L2).** When is waterfall appropriate?

> [!success]- Answer
> When requirements are well understood and stable, the technology is familiar, and regulation demands documented phases and verification evidence.

**Q4 (L2).** What problem does the spiral model address that waterfall doesn't?

> [!success]- Answer
> Risk: each cycle identifies and reduces the biggest risks (often with prototypes) before committing further.

## [[SD-03 Requirements Engineering]]

**Q5 (L1).** Distinguish functional and non-functional requirements, with an example of each.

> [!success]- Answer
> Functional: what the system does ("shall let a warden assign a request"). Non-functional: how well ("shall respond within 2 s for 95% of requests").

**Q6 (L3).** Why is "The system should be fast and user-friendly" a poor requirement?

> [!success]- Answer
> It's vague (`fast`, `user-friendly`), optional (`should`), and untestable; `requirement_smells` flags all of these. Rewrite with measurable thresholds and "shall".

## [[SD-04 Use Cases, User Stories and Traceability]]

**Q7 (L2).** Write a user story with acceptance criteria for reopening a resolved request.

> [!success]- Answer
> "As a resident, I want to reopen a resolved request within 7 days so that unfixed faults get attention." Given a request resolved 3 days ago, when I reopen it, its status becomes Reopened; given one resolved 8 days ago, reopening is refused with a message.

**Q8 (L2).** What does a traceability matrix link, and why?

> [!success]- Answer
> Requirements to design elements and tests (and back to their sources). It shows that every requirement is implemented and verified, and supports impact analysis when requirements change.

## [[SD-05 Software Architecture and Architectural Styles]]

**Q9 (L2).** In a layered architecture, which layer should hold authorisation checks, and why?

> [!success]- Answer
> The service (business) layer, so that every interface (CLI, web, API) goes through them and can't bypass them.

**Q10 (L3).** Compare layered and microservice architectures for a small university team.

> [!success]- Answer
> Layered (in a single deployable) is simpler to build, test and deploy, which suits a small team; microservices give independent deployment and scaling but add network, data-consistency and operational complexity that a small team may not be able to manage.

## [[SD-06 Modular Design, Cohesion and Coupling]]

**Q11 (L1).** Aim for high or low cohesion? High or low coupling?

> [!success]- Answer
> High cohesion, low coupling.

**Q12 (L3).** A module has $C_a = 5$ and $C_e = 1$. Compute its instability and interpret it.

> [!success]- Answer
> $I = 1/(5 + 1) = 0.17$: stable (many depend on it, it depends on little); it should be abstract or change rarely, like a domain model.

## [[SD-07 UML Class Diagrams]]

**Q13 (L2).** Aggregation vs composition: which applies to Room and Block, and to Request and StatusChange?

> [!success]- Answer
> Composition for Request–StatusChange (history entries don't exist without their request). Room–Block is usually composition too (a room belongs to exactly one block for its lifetime); aggregation suits looser wholes, e.g. a Team of Technicians.

**Q14 (L2).** What does the multiplicity `0..1` on Request → Technician mean?

> [!success]- Answer
> Each request has at most one assigned technician (none until it's assigned).

## [[SD-08 UML Sequence, Activity and State Diagrams]]

**Q15 (L2).** Which diagram shows a request's lifecycle, and which shows the messages for "resolve request"?

> [!success]- Answer
> A state machine diagram for the lifecycle; a sequence diagram for the message exchange.

**Q16 (L3).** How can a sequence diagram expose a race condition?

> [!success]- Answer
> With a `par` fragment showing two users' check-then-act messages interleaving: both read "no booking", both insert, revealing a double booking.

## [[SD-09 Data Modeling and Interface Design]]

**Q17 (L2).** Why is storing stock as a sum of movements often better than an editable quantity column?

> [!success]- Answer
> It gives an audit trail by construction, and makes discrepancies traceable; an editable column loses the history.

**Q18 (L2).** What makes a good API error response?

> [!success]- Answer
> A consistent structure, the right status code, a message safe to show users, and no internal details (stack traces, SQL).

## [[SD-10 SOLID Principles]]

**Q19 (L1).** State the dependency inversion principle.

> [!success]- Answer
> High-level modules shouldn't depend on low-level modules; both should depend on abstractions.

**Q20 (L3).** A `ReportManager` queries SQLite, formats PDF/CSV/HTML in an if-chain, and sends email. Which principles does it violate?

> [!success]- Answer
> SRP (three responsibilities), OCP (new formats need edits), DIP (it creates its concrete database and email dependencies).

## [[SD-11 Creational and Structural Design Patterns]]

**Q21 (L2).** When would you use a Factory?

> [!success]- Answer
> When the code needs to create objects whose concrete class depends on configuration or input, and the callers shouldn't know the classes (e.g. choosing a repository implementation).

**Q22 (L2).** What does an Adapter do? Give an example.

> [!success]- Answer
> It converts one interface into another that clients expect: e.g. wrapping an SMS provider's API behind your `Notifier` interface.

## [[SD-12 Behavioral Design Patterns]]

**Q23 (L2).** Which pattern for interchangeable report formats? For notifying several listeners when a request changes?

> [!success]- Answer
> Strategy; Observer.

**Q24 (L3).** How does Strategy support the open/closed principle?

> [!success]- Answer
> New behaviours are new strategy classes registered with the context; the context's code doesn't change.

## [[SD-13 Implementation, Code Organization and Version Control]]

**Q25 (L1).** What makes a good commit message?

> [!success]- Answer
> A short imperative summary of what and why, with details in the body if needed; one logical change per commit.

**Q26 (L2).** Describe a feature-branch workflow.

> [!success]- Answer
> Branch from main, commit the feature, open a pull request, pass CI and review, merge, delete the branch.

## [[SD-14 Software Testing, Verification and Validation]]

**Q27 (L2).** Verification vs validation?

> [!success]- Answer
> Verification: are we building the product right (against the specification)? Validation: are we building the right product (against users' needs)?

**Q28 (L3).** A function has cyclomatic complexity 7. What does that say about testing?

> [!success]- Answer
> It has 7 linearly independent paths, so at least 7 test cases are needed for basis-path coverage; high complexity also suggests refactoring.

## [[SD-15 Refactoring, Technical Debt, Code Review and Quality]]

**Q29 (L1).** Define refactoring.

> [!success]- Answer
> Changing code's internal structure without changing its external behaviour, to make it easier to understand and modify.

**Q30 (L2).** Name three code smells and their refactorings.

> [!success]- Answer
> Long method → extract method; duplicated code → extract function; magic numbers → named constants; switch on type → polymorphism or Strategy.

## [[SD-16 Deployment, Maintenance and Documentation]]

**Q31 (L1).** Name the four types of maintenance.

> [!success]- Answer
> Corrective, adaptive, perfective, preventive.

**Q32 (L2).** Why keep configuration (database paths, secrets) out of the code?

> [!success]- Answer
> So the same build runs in different environments, and secrets aren't committed to version control; use environment variables or a secrets manager.

## [[SD-17 Secure and Reliable Software Design]]

**Q33 (L2).** What's "fail securely"? Give an example.

> [!success]- Answer
> When something goes wrong, default to the safe state: e.g. if the authorisation service is unreachable, deny access rather than allow it.

**Q34 (L3).** How does optimistic concurrency prevent lost updates?

> [!success]- Answer
> The update includes the expected current state (`UPDATE … WHERE id = ? AND status = ?`); if another user changed it first, no row matches, and the application reports a conflict instead of overwriting.

Back to [[Question Bank Index]] · [[MOCK-SD-01 Software Design and Development Mock Examination]] · [[SD 00 Dashboard]]
