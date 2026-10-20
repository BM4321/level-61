---
title: "Software Design and Development Mock Examination"
module: "Software Design and Development"
module_code: "CST06101"
topic_id: "MOCK-SD-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - software-design
  - exam
---

# MOCK-SD-01 Software Design and Development Mock Examination

> [!warning] A designed practice paper
> This is **not** a past paper; the format (3 hours, 100 marks, answer all seven questions) is designed. Check the real format with your lecturer. The computed answers (requirement smells, coupling metrics of real code, cyclomatic complexity) are produced with `07 - Software Design and Development/code/sd_tools.py` in `09 - Revision and Exam Preparation/code/tests/test_mock_sd.py`. Q4 uses the **actual** import graph of [[PRJ-PY-05 Hostel Maintenance System]] 1.1.0.

**Instructions (designed):** 3 hours. Answer **all** questions. UML must use correct notation; state any assumptions.

**Covers:** [[SD 01 Curriculum Map]], SD-01 to SD-17.

---

**Q1 Process models (10 marks).** Recommend a process model for each, and justify it in two or three sentences: (a) firmware for a medical infusion pump, with regulatory approval; (b) a start-up's mobile app whose features change with user feedback; (c) a university results system, with fixed core rules but an uncertain user interface, delivered over a year.

**Q2 Requirements (15 marks).**
(a) Critique each requirement, then rewrite it to be testable: *(9)*
1. "The system should be fast and user-friendly."
2. "The system shall let a resident submit a fault report and/or upload a photo."
3. "The system shall display a resident's open requests within 2 seconds for 95% of page loads."

(b) Write two user stories, with acceptance criteria in Given/When/Then form, for a warden assigning a fault to a technician. *(6)*

**Q3 UML (20 marks).** A hostel maintenance system: residents report faults in their rooms; a warden assigns each fault to a technician; technicians update the status; residents may reopen a resolved fault within 7 days.
(a) Draw a domain class diagram with at least five classes, multiplicities and one association class or enumeration. *(8)*
(b) Draw a sequence diagram for "technician resolves a fault", from the user interface to the database, including the audit record. *(6)*
(c) Draw the state machine for a fault (request), including rejection and reopening. *(6)*

**Q4 Modularity (15 marks).** The modules of a real Python package import each other as follows (module → modules it imports):

| Module | Imports |
|---|---|
| `cli` | errors, insights, models, reports, repository, security, services |
| `services` | errors, models, repository, security |
| `repository` | errors, models |
| `insights` | models |
| `reports` | models |
| `models` | errors |
| `security` | — |
| `errors` | — |

(`__main__`, which only imports `cli`, is left out.)

(a) For `cli`, `services`, `repository`, `models` and `errors`, compute afferent coupling $C_a$, efferent coupling $C_e$, and instability $I = C_e/(C_a + C_e)$. Count `__main__` as importing `cli`. *(8)*
(b) Is the graph acyclic? How do you know? *(3)*
(c) Use the stable dependencies principle to explain whether these dependencies point the right way. *(4)*

**Q5 SOLID and patterns (15 marks).**
```python
# question Q5
class ReportManager:
    def __init__(self):
        self.db = SqliteDatabase("hostel.db")

    def monthly_report(self, kind):
        rows = self.db.query("SELECT * FROM requests")
        if kind == "pdf":
            text = make_pdf(rows)
        elif kind == "csv":
            text = make_csv(rows)
        elif kind == "html":
            text = make_html(rows)
        send_email("warden@hostel.example", text)
        return text
```
(a) Identify which SOLID principles this violates, with reasons. *(6)* (b) Redesign it using an appropriate pattern for the output formats and dependency injection for the database and email. Give the class structure in code or UML. *(9)*

**Q6 Testing (15 marks).**
```python
# question Q6
def shipping_cost(weight, express, region, member):
    if weight <= 0:
        raise ValueError("weight must be positive")
    cost = 2000 + 500 * weight
    if express and region != "local":
        cost *= 2
    elif express:
        cost += 1000
    for _ in range(int(weight // 10)):
        cost += 300
    if member:
        cost = cost * 0.9
    return cost
```
(a) Compute the cyclomatic complexity, counting each `if`, `elif`, loop and boolean operator. What does it tell you about the minimum number of tests for basis-path coverage? *(4)* (b) Identify equivalence partitions and boundary values for `weight`. *(5)* (c) Write six test cases (inputs and expected outputs). *(6)*

**Q7 Maintenance and quality (10 marks).** (a) Name the four types of maintenance, with an example of each for the hostel system. *(4)* (b) Define technical debt, and give two ways a team can manage it. *(3)* (c) Name three code smells, and the refactoring for each. *(3)*

---

## Marking guide

> [!success]- Q1
> (a) **V-model** (or plan-driven waterfall with verification at each stage): requirements are stable, safety-critical and must be traceable to verification evidence for approval. (b) **Scrum / agile**: requirements are uncertain and change with feedback; short iterations deliver value and learning. (c) **Incremental or hybrid**: a plan-driven core for the fixed rules (with traceability), and iterative UI development with user feedback; increments reduce delivery risk over the year. *(Choice 1, justification 2–3 each; accept well-argued alternatives.)*

> [!success]- Q2
> (a) 1. Vague terms "fast" and "user-friendly", optional "should", no "shall" (`requirement_smells` flags all four). Rewrite as two requirements: "The system shall return search results within 2 s for 95% of requests at 50 concurrent users" and "90% of first-time residents shall submit a fault without help in a usability test". 2. "and/or" is ambiguous: is a photo required, optional, or an alternative? Rewrite: "The system shall let a resident submit a fault report. The system shall let a resident attach up to 3 photos (JPEG/PNG, ≤ 5 MB each) to a report." 3. Already testable: it has a measurable threshold and a percentile, and `requirement_smells` finds nothing. Consider adding the load condition. *(3 each.)*
> (b) "As a warden, I want to assign a new fault to a technician so that it gets fixed." Given a new fault and an available technician, when I assign it, then its status becomes Assigned and the technician sees it in their queue. "As a warden, I want to see each technician's open jobs before assigning, so that I balance the workload." Given technicians with open jobs, when I open the assignment screen, then each technician's open job count is shown. *(3 each.)*

> [!success]- Q3
> (a) Classes such as Resident, Room, Block, Request (Fault), Technician, Warden, StatusChange; enumerations Status and Priority. Multiplicities: Block 1 — * Room; Room 1 — * Resident (or 0..1 room per resident); Resident 1 — * Request; Request * — 0..1 Technician (assignee); Request 1 — 1..* StatusChange. StatusChange can be modelled as an association class between Request and the acting user. *(8.)*
> (b) Technician UI → RequestService.transition(user, id, RESOLVED) → Repository.get_request → (service checks the allowed transition, role and assignee) → Repository.save_change → DB: BEGIN; UPDATE … WHERE status = 'in_progress'; INSERT history; COMMIT → return → UI shows the new status. Include an `alt` fragment for the concurrent-update failure. *(6.)*
> (c) new → assigned (warden) or rejected (warden); assigned → in_progress (assigned technician); in_progress → resolved (technician); resolved → closed (warden) or reopened (reporter, [within 7 days]); reopened → assigned. Closed and rejected are final. *(6; see [[PRJ-PY-05 Hostel Maintenance System]] §2.2.)*

> [!success]- Q4
> (a)
>
> | Module | $C_a$ | $C_e$ | $I$ |
> |---|---|---|---|
> | cli | 1 | 7 | 0.88 |
> | services | 1 | 4 | 0.80 |
> | repository | 2 | 2 | 0.50 |
> | models | 5 | 1 | 0.17 |
> | errors | 4 | 0 | 0.00 |
>
> *(8: one mark per correct C_a/C_e pair, plus I values.)*
> (b) Yes, acyclic: every edge goes "down" the order cli → services → repository → models → errors (insights, reports and security only point downwards too), so a topological order exists. *(3.)*
> (c) The stable dependencies principle says depend in the direction of stability (decreasing $I$). Every edge here goes from a less stable module to a more stable one (e.g. services 0.80 → repository 0.50 → models 0.17 → errors 0.00), so the dependencies point the right way: the domain (`models`) is stable and depended on by many, and the volatile CLI depends on everything but nothing depends on it. *(4.)*

> [!success]- Q5
> (a) **SRP**: one class queries data, formats reports in three formats and sends email; three reasons to change. **OCP**: adding a format means editing the `if/elif` chain. **DIP**: it creates its concrete `SqliteDatabase` and calls `send_email` directly, so it can't be tested without a database and email. *(2 each.)*
> (b) **Strategy** for formats, injected collaborators:
> ```python
> from typing import Protocol
>
>
> class ReportFormat(Protocol):
>     def render(self, rows: list[dict]) -> str: ...
>
>
> class RequestSource(Protocol):
>     def all_requests(self) -> list[dict]: ...
>
>
> class Notifier(Protocol):
>     def send(self, to: str, body: str) -> None: ...
>
>
> class ReportService:
>     def __init__(self, source: RequestSource, notifier: Notifier, formats: dict[str, ReportFormat]):
>         self.source, self.notifier, self.formats = source, notifier, formats
>
>     def monthly_report(self, kind: str, recipient: str) -> str:
>         text = self.formats[kind].render(self.source.all_requests())
>         self.notifier.send(recipient, text)
>         return text
> ```
> New formats are new classes registered in `formats` (open for extension); tests inject fakes. *(Structure 5, pattern named and justified 2, DI 2.)*

> [!success]- Q6
> (a) **CC = 7**: 1 + `if weight <= 0` + `if express and …` (1 for the `if`, 1 for the `and`) + `elif` + `for` + `if member`. At least 7 test cases cover a basis set of independent paths. *(4.)*
> (b) Partitions: weight ≤ 0 (invalid); 0 < weight < 10 (no surcharge); 10 ≤ weight < 20 (one surcharge); ≥ 20 (two or more). Boundaries: 0, a small positive value (e.g. 0.1), 9.9 / 10, 19.9 / 20. *(5.)*
> (c) Six examples (cost before the member discount = 2000 + 500w, ×2 for express non-local, +1000 for express local, +300 per full 10 kg):
>
> | weight | express | region | member | expected |
> |---|---|---|---|---|
> | 0 | False | local | False | `ValueError` |
> | 1 | False | local | False | 2500 |
> | 10 | False | local | False | 7300 |
> | 2 | True | local | False | 4000 |
> | 2 | True | coast | False | 6000 |
> | 20 | False | local | True | 11340.0 |
>
> *(1 each; correct expected values required.)*

> [!success]- Q7
> (a) Corrective (fix the reopen-window bug); adaptive (move from SQLite to PostgreSQL on a new server); perfective (add the insights report); preventive (refactor the CLI into smaller functions, add tests). (b) The future cost of rework created by choosing an easier solution now; manage it by recording it in the backlog with an estimate, and by reserving capacity each sprint for paying it down (plus code review and definition of done). (c) Long method → extract method; duplicated code → extract function or pull up; switch on type → replace conditional with polymorphism (Strategy); magic numbers → named constants. *(4 + 3 + 3.)*

**Self-assessment (designed):** ≥ 70 strong; 50–69 secure; < 50 on any question → that topic goes to [[Weak Area Tracker]].

Back to [[Exam Technique and Assessment Strategy]] · [[QB-SD Software Design Question Bank]] · [[SD 00 Dashboard]]
