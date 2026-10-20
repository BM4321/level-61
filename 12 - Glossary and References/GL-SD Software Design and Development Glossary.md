---
title: "Software Design and Development Glossary"
module: "Software Design and Development"
module_code: "CST06101"
type: "glossary"
tags:
  - semester-6
  - software-design
  - glossary
---

# GL-SD Software Design and Development Glossary

Every term below is taken from the Terminology section (§6) of the lesson it links to, so the definitions match the lessons. Generated at the last build; 121 terms.

| Term | Meaning | Lesson |
|---|---|---|
| Abstract class | Can't be instantiated; it may have abstract operations | [[SD-07 UML Class Diagrams\|SD-07]] |
| Acceptance criteria | Conditions that must be true for a requirement or story to be accepted | [[SD-03 Requirements Engineering\|SD-03]] |
| Activation | The period during which a participant is executing | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Actor | An external role interacting with the system | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| ADR | Architecture decision record | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Architecture style | A named, reusable pattern of structure and interaction | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Artefact | A built, versioned deliverable (wheel, image) | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Association class | A class attached to an association to hold its attributes | [[SD-07 UML Class Diagrams\|SD-07]] |
| Atomicity | All of an operation happens, or none of it | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Baseline | An agreed version, after which changes go through change control | [[SD-03 Requirements Engineering\|SD-03]] |
| Boundary value | A value at or adjacent to an edge of a class | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Boy scout rule | Leave the code a little better than you found it | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Branch | A movable pointer to a line of commits | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Cardinality | How many instances relate (1:1, 1:N, M:N) | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| Characterisation test | A test pinning down existing behaviour before changing legacy code | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Check-then-act | A pattern vulnerable to races: the condition changes between the check and the act | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Circuit breaker | Stops calls to a failing dependency, then probes for recovery | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Code smell | A surface symptom suggesting a deeper design problem | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Cohesion | How closely a module's elements belong together | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Combined fragment | A framed region with an operator (alt, opt, loop…) | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Commit | A snapshot of tracked files, with a message, author and parent(s) | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Complete mediation | Every access is checked | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Composition root | The single place where the object graph is assembled (`app.py`) | [[SD-10 SOLID Principles\|SD-10]] |
| Conflict | Both sides changed the same region; it needs a human decision | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Consequences | The trade-offs of applying it | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| Container (C4) | A separately deployable or runnable unit | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Context | The object that uses a strategy or state (BookingService, RepairTicket) | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Contract test | A test that an implementation honours an interface's promised behaviour | [[SD-09 Data Modeling and Interface Design\|SD-09]], [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Coupling | The degree of interdependence between modules | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Cyclomatic complexity | The number of linearly independent paths through code | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Definition of Done | The shared quality criteria an increment must meet | [[SD-02 Software Process Models\|SD-02]] |
| Dependency injection | Supplying dependencies from outside (constructor, parameters) | [[SD-10 SOLID Principles\|SD-10]] |
| Elicitation | Discovering requirements from sources | [[SD-03 Requirements Engineering\|SD-03]] |
| Environment | A deployment target: dev, staging, production | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Equivalence class | Inputs expected to behave the same way | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Essential / accidental complexity | Complexity inherent in the problem / introduced by the solution | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| Eventual consistency | Data converges over time instead of being instantly consistent | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Expand–contract migration | Add the new schema, migrate, then remove the old: a zero-downtime schema change | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Extension | An alternative or failure path from a step | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Extension point | A place designed for new behaviour to plug in | [[SD-10 SOLID Principles\|SD-10]] |
| Fail closed / fail safe | On failure, deny access / move to a safe state | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Fan-in / fan-out | The number of dependants / dependencies | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Flaky test | A test that passes or fails non-deterministically | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Fluent interface | Methods returning `self` so calls can be chained (Builder) | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| Fork / join | Splitting into parallel flows / synchronising them | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Functional dependency | X → Y: X determines Y | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| Functional requirement | What the system does (e.g. "book a workstation") | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| Gold-plating | Work that no requirement asked for | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Graceful degradation | Reduced but safe functionality under failure | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Guard | A boolean condition in brackets that must be true to proceed | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| HEAD | Your current position (branch or commit) | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Hook method | An overridable step in a Template Method | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Idempotency | Repeating a request has the same effect as doing it once | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Idempotent | Repeating the operation has the same effect as doing it once | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| «include» / «extend» | Mandatory shared behaviour / optional conditional behaviour | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Increment | A usable slice of the system delivered in one cycle | [[SD-02 Software Process Models\|SD-02]] |
| Information hiding | Hiding changeable design decisions behind interfaces | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Instability (I) | Ce / (Ca + Ce) | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Intent | The problem a pattern solves | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| Interface | What a module offers and requires, visible to others | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]], [[SD-07 UML Class Diagrams\|SD-07]] |
| INVEST | The quality criteria for user stories | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Invoker / receiver | Runs commands (CommandHistory) / does the work (BookingService) | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Iteration | A cycle of building and refining | [[SD-02 Software Process Models\|SD-02]] |
| Junction (associative) table | A table that resolves an M:N relationship | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| Lifeline | A participant in a sequence diagram | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Main success scenario | The typical path to the goal | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Maintainability | The ease of analysing, modifying and testing the software | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| Merge commit | A commit with two parents, combining histories | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Module | A unit of decomposition (file, package, class, service) with an interface | [[SD-06 Modular Design, Cohesion and Coupling\|SD-06]] |
| Multiplicity | The allowed number of linked objects at an association end | [[SD-07 UML Class Diagrams\|SD-07]] |
| Navigability | Which direction an association can be traversed in code | [[SD-07 UML Class Diagrams\|SD-07]] |
| Non-functional requirement / quality attribute | How well it does it (performance, security, usability…) | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| Observer / subscriber | A receiver of notifications (Outbox, WaitingList) | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Oracle | The way to decide whether an output is correct | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Outbox pattern | Store events in the database in the same transaction, deliver them later | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Participants | The roles in the pattern (Component, Leaf, Composite…) | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| Phase gate | A sign-off point before the next phase starts | [[SD-02 Software Process Models\|SD-02]] |
| Port / adapter | An interface defined by the core / an implementation connecting it to a technology | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Precondition / postcondition / invariant | What callers must ensure / what the method guarantees / what always holds | [[SD-10 SOLID Principles\|SD-10]] |
| Primary / foreign key | A unique identifier / a reference to another table's key | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| Primary / supporting actor | The actor with the goal / an actor that helps (e.g. the email service) | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Product backlog | An ordered list of everything that might be built | [[SD-02 Software Process Models\|SD-02]] |
| Protocol (Python) | A structural interface: conformance by shape, not by inheritance | [[SD-10 SOLID Principles\|SD-10]] |
| Pseudostate | The initial node, or a choice/junction (not a real state) | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Pull request (PR) | A request to merge a branch, with review and CI | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Qualified association | An association looked up by a key (e.g. a Directory, by `user_id`) | [[SD-07 UML Class Diagrams\|SD-07]] |
| Quality-attribute scenario | A testable statement of a quality requirement for architecture | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| Race condition | The outcome depends on the timing of concurrent operations | [[SD-17 Secure and Reliable Software Design\|SD-17]] |
| Readiness / liveness probe | Is the service ready for traffic? / Is it alive? | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Rebase | Replaying commits onto a new base (rewrites history) | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Refactoring | A behaviour-preserving structural change | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Registry | A mapping from names to constructors, used by factories | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| Regression | A previously working feature now broken | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Remote | A shared copy of the repository (origin) | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Requirements creep | Uncontrolled growth of scope | [[SD-03 Requirements Engineering\|SD-03]] |
| Responsibility | A reason to change (an actor or concern) | [[SD-10 SOLID Principles\|SD-10]] |
| Role name | A label on an association end (e.g. `booker`) | [[SD-07 UML Class Diagrams\|SD-07]] |
| RTM | Requirements traceability matrix | [[SD-04 Use Cases, User Stories and Traceability\|SD-04]] |
| Runbook | Operational procedures for a service | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Semantic versioning | MAJOR.MINOR.PATCH: breaking change, feature, fix | [[SD-13 Implementation, Code Organization and Version Control\|SD-13]] |
| Single point of failure | A component whose failure stops the whole system | [[SD-05 Software Architecture and Architectural Styles\|SD-05]] |
| SLO / SLI / SLA | Objective / indicator / agreement for service levels | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Smoke test | A quick check that the main functions work after a deploy | [[SD-16 Deployment, Maintenance and Documentation\|SD-16]] |
| Sprint | A Scrum time-box (1–4 weeks) producing an increment | [[SD-02 Software Process Models\|SD-02]] |
| SRS | Software requirements specification | [[SD-03 Requirements Engineering\|SD-03]] |
| Stakeholder | Anyone affected by, or able to affect, the system | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| Statement / branch coverage | Statements executed / decision outcomes taken | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Strangler fig | Replacing a legacy system piece by piece behind a stable interface | [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Subject / publisher | The source of notifications (EventBus) | [[SD-12 Behavioral Design Patterns\|SD-12]] |
| Swimlane | A partition showing responsibility | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Tacit knowledge | Knowledge people use but don't articulate | [[SD-03 Requirements Engineering\|SD-03]] |
| Technical debt | The future cost of shortcuts taken now | [[SD-01 Software Engineering Fundamentals\|SD-01]], [[SD-15 Refactoring, Technical Debt, Code Review and Quality\|SD-15]] |
| Test case | Inputs + preconditions + expected result | [[SD-14 Software Testing, Verification and Validation\|SD-14]] |
| Transition | A state change triggered by an event, possibly guarded, possibly with an action | [[SD-08 UML Sequence, Activity and State Diagrams\|SD-08]] |
| Transitive dependency | A → B → C, where B isn't a key | [[SD-09 Data Modeling and Interface Design\|SD-09]] |
| Triangulation | Combining techniques to cross-check findings | [[SD-03 Requirements Engineering\|SD-03]] |
| Velocity | The amount of backlog completed per sprint (team-specific; not a cross-team metric) | [[SD-02 Software Process Models\|SD-02]] |
| Verification / validation | Built right? / right thing built? | [[SD-01 Software Engineering Fundamentals\|SD-01]] |
| WIP limit | The maximum number of items allowed in a Kanban column | [[SD-02 Software Process Models\|SD-02]] |
| Wrapper | An object that holds another and forwards calls (Adapter, Decorator, Proxy) | [[SD-11 Creational and Structural Design Patterns\|SD-11]] |
| YAGNI | Don't build abstractions before they're needed | [[SD-10 SOLID Principles\|SD-10]] |

Back to [[Glossary Index]]
