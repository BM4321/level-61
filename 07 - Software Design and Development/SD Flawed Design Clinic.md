---
title: "Flawed Design Clinic"
aliases:
  - Design critique exercises
  - Anti-patterns
module: "Software Design and Development"
module_code: "CST06101"
topic_id: "SD-CLINIC"
type: "exercise-set"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - software-design
  - exercises
---

# SD Flawed Design Clinic

> [!info] How to use the clinic
> Each case is a **deliberately flawed** design. F1–F3 are runnable code in `code/clinic/`, with tests in `tests/test_clinic.py` that *pass by demonstrating each defect*. F4–F5 are design descriptions. For each case:
> 1. Diagnose: smells, violated principles, risks.
> 2. Propose: a target design (diagram plus a short rationale).
> 3. Refactor in small steps, with tests (F1–F3).
> 4. Compare with the model answer, *after* trying it yourself.
>
> Never copy these designs into real projects.

## F1 The god class (`clinic/flawed_god_class.py`)
**Scenario:** an early LabBook prototype. `LabManager.do_booking(who, ws, s, e, role="student", send=True, fmt="text")` parses times, enforces rules, runs SQL, "sends" email and prints HTML or text.

**Evidence from the tests and tools:**
- 22:30 is accepted although the labs close at 22:00 (only the hour is compared).
- The quota counts *all-time* hours, so a booking a month later is refused.
- `o'brien` crashes the query (string-built SQL, an injection risk).
- Results are visible only via stdout.
- Cyclomatic complexity is **14** (`sd_tools.cyclomatic_complexity`).

**Your tasks:**
1. List at least 8 smells, with the principle each violates.
2. Draw the target module diagram.
3. Refactor in at least 6 commits, keeping the characterisation tests green, then deliberately change the tests for the two behaviour bugs.

> [!success]- Model answer (F1)
> **Smells → principles:**
> - god class / long function: SRP;
> - flag arguments `send` and `fmt`: control coupling, OCP;
> - primitive obsession (string times compared as strings): a missing value object;
> - magic numbers 7, 22, 10;
> - global `DB` and `SENT`: common coupling, DIP;
> - string-built SQL: security (CS-12);
> - unescaped HTML: XSS (CS-11);
> - output mixed with logic: SRP, testability;
> - a hard-coded out-of-service list: OCP / data;
> - a quota with the wrong period: a requirements defect.
>
> **Target:** exactly LabBook:
> - `TimeSlot` (value object);
> - `rules.py` (Strategy + Composite: `OpeningHours` with full-time comparison, `WeeklyQuota` per Monday–Sunday week, `WorkstationInService` using data);
> - a repository with parameterised SQL;
> - `EventBus` + `Outbox` for notifications;
> - the CLI adapter for formatting;
> - `app.py` composition root.
>
> **Steps** (SD-15 §7): characterise → extract `parse_slot` → introduce `TimeSlot` → extract rules → introduce the repository (fixes injection) → extract notification → move formatting to the adapter → inject dependencies. The two behaviour fixes (22:30, weekly quota) go in separate commits, with updated requirement tests. **Measured result:** at most 6 per function in LabBook (`WeeklyQuota.check`); the service's methods are at most 3.

## F2 Inheritance misuse (`clinic/flawed_inheritance.py`)
**Scenario:**
- `GpuWorkstation(Workstation)` overrides `book` to refuse sessions over 2 h.
- `OutOfServiceWorkstation` overrides `book` to raise `NotImplementedError`.
- `BookingList(list)` adds `add_booking`, but inherits `append`.

**Evidence:**
- `book_whole_lab` works for `Workstation` but raises for the subclasses (`test_lsp_violation`).
- `BookingList.append` lets duplicates in (`test_inheriting_from_list_bypasses_rules`).

**Tasks:** explain each LSP violation in terms of preconditions and postconditions; redesign without subclassing; show that client code works for every workstation.

> [!success]- Model answer (F2)
> - `GpuWorkstation` **strengthens a precondition**: callers must now know about the 2 h limit.
> - `OutOfServiceWorkstation` is a **refused bequest**: it can't honour the parent's contract at all.
> - `BookingList` exposes the entire `list` API, which **bypasses the invariant** (no duplicates). That's inheritance used for reuse rather than an is-a relationship.
>
> **Redesign:** make variation **data** (`has_gpu`, `in_service`, an optional `max_session_hours`) checked by **rules**, as LabBook does (`WorkstationInService`, `GpuForLecturersAndApprovedOnly`, and a new `MaxSessionHours`). Use **composition** for collections: a `Bookings` class *containing* a private list and exposing only `add` (which checks duplicates) and iteration. Client code now gets a consistent `RuleViolation` for any refused booking.

## F3 Hidden dependencies (`clinic/flawed_coupling.py`)
**Scenario:**
- `ReminderService` creates `SmtpMailer()` internally.
- It calls `datetime.now()` directly.
- It reads a global singleton `Config`.
- It navigates `booking["user"]["contact"]["email"]`.

**Evidence:** it can't be tested without a mail server (`ConnectionError`), and `Config()` is shared by every test.

**Tasks:** list the dependencies; apply DIP; write a test with a fake mailer and a fixed clock.

> [!success]- Model answer (F3)
> The dependencies are the mailer (infrastructure), the clock (non-deterministic), the global configuration, and the structure of the booking dictionary (a message chain, Law of Demeter). The refactored `ReminderService(mailer: Mailer, clock=datetime.now, window=…)`, with `remind_if_soon(start, email)`, is given and *run* in [[SD-10 SOLID Principles]] Example 3. With a `FakeMailer` and `clock=lambda: datetime(2026, 3, 2, 8, 30)`, a session at 09:00 triggers one message, and 11:00 triggers none.

## F4 The anaemic domain with a fat service (design description)
**Scenario:** a team's hostel system has:
- `Request` objects that are pure data bags (getters and setters only);
- a 1,200-line `RequestService` holding every rule (status changes, assignment, SLA timers);
- direct status assignments everywhere: `req.status = "closed"`.

Bugs keep appearing: requests jump from NEW to CLOSED, skipping assignment.

**Tasks:** identify the problems; propose where the rules should live; show how a state machine prevents the bug.

> [!success]- Model answer (F4)
> **Problems:**
> - the invariants (legal status changes) aren't owned by the object that has the state, so any code can set any status;
> - the service is a god class (SRP);
> - nothing can be tested in isolation.
>
> **Redesign:**
> - move the lifecycle into `Request` with a transition table and a single `transition()` method that raises on illegal moves (exactly `Booking.transition` with `ALLOWED`; SD-08), or the State pattern if states have distinct behaviour (`RepairTicket`; SD-12);
> - make `status` read-only from outside;
> - keep the *orchestration* (load, check permissions, save, publish) in a thin application service;
> - put the assignment policy in a Strategy.
>
> **Test:** iterate over all state pairs, and assert that only the allowed ones succeed.

## F5 The distributed monolith (design description)
**Scenario:** to be "modern", a 3-person student team split LabBook into 6 microservices:
- users, workstations, bookings, rules, notifications, reports.

Every booking request makes 5 synchronous HTTP calls (to users, workstations, rules ×2, notifications). All the services share one database, and any schema change needs coordinated deployment of 4 services. Demo day fails when the notifications service is slow and bookings time out.

**Tasks:** diagnose; propose an architecture; write the ADR.

> [!success]- Model answer (F5)
> **Diagnosis:** a **distributed monolith**. The services are coupled through a shared database and synchronous call chains, so the team pays microservice costs (network failures, latency, deployment coordination) without the benefits (independent deployment, independent data). The slow notification service is on the **critical path**, so the "side effect" became essential (an Observer misuse; SD-12), and there are no timeouts or isolation (SD-17).
>
> **Proposal:** a **modular monolith** (SD-05 ADR-001): the same module boundaries as packages, one deployment and one database, with notifications as asynchronous subscribers that can't block bookings. Revisit services only when there's a concrete driver (separate teams, independent scaling).
>
> **ADR:** context (team size, a demo-day failure, coupling evidence), decision (consolidate), consequences (+ reliability and simplicity; − rework now; module boundaries enforced by dependency tests, as in `test_labbook_dependency_rules`).

## Clinic scoring rubric (self-assessment, per case)
| Score | Diagnosis | Redesign | Refactoring / evidence |
|---|---|---|---|
| 1 | Finds 1–2 surface issues | None | None |
| 3 | Most smells, named with principles | A sound target design | Partial refactoring, with tests |
| 5 | All issues, with risks and trade-offs | A justified design with an ADR and a diagram | Complete, small-step refactoring; tests green throughout; behaviour changes deliberate |

Links: [[SD 00 Dashboard]] · [[SD-15 Refactoring, Technical Debt, Code Review and Quality]] · [[SD-10 SOLID Principles]] · [[SD-CASE LabBook Running Case Study]]
