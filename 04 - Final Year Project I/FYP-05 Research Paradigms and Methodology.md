---
title: "Research Paradigms and Methodology"
aliases:
  - Research methodology
  - Design science research
  - Research paradigms
  - Mixed methods
module: "Final Year Project I"
module_code: "CST06103"
topic_id: "FYP-05"
type: "lesson"
unit: "U3 Methodology"
difficulty: "intermediate"
syllabus_status: "provisional-core"
status: "not-started"
mastery: 0
prerequisites:
  - "[[FYP-02 Problem Statements, Research Questions, Objectives and Scope]]"
next: "[[FYP-06 Requirements Gathering, Stakeholder and Feasibility Analysis]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - final-year-project
  - methodology
---

# FYP-05 Research Paradigms and Methodology

> [!info] Topic card
> **Unit:** U3 · **Time:** 4 h · **Template:** [[FYP-T07 Methodology]] · **Engineering link:** the development methodology connects to [[SD-02 Software Process Models]].

## 1. Learning objectives
1. **Explain** research paradigms (positivism, interpretivism, pragmatism; also critical theory and design science) and their assumptions.
2. **Distinguish** a research methodology (the overall strategy) from a research method (a technique), and from the software development methodology.
3. **Describe** strategies used in IS projects: design science research, surveys, case studies, experiments, action research. **Select** and **justify** one.
4. **Describe** quantitative, qualitative and mixed-methods approaches, and their data and analysis.
5. **Write** a methodology section that aligns the paradigm → strategy → methods → evaluation with the RQs.

## 2. Why it matters
Examiners want to know *why* your way of answering the questions is appropriate. "I'll use agile" isn't a research methodology. For most IS projects that build something, **design science research (DSR)** gives a well-recognised framework that connects building an artefact to research questions and evaluation.

## 3. Prerequisites
[[FYP-02 Problem Statements, Research Questions, Objectives and Scope]] (RQs) · [[SD-02 Software Process Models]] (development lifecycles).

## 4. Intuition
- The **paradigm** is your *worldview* about knowledge.
- The **methodology** is your *battle plan*.
- **Methods** are your *weapons*: interviews, questionnaires, usability tests.
- The **software development methodology** (Scrum, prototyping) is *how you build the artefact*, inside the bigger research plan.

## 5. Rigorous explanation

### 5.1 Paradigms
| Paradigm | Reality (ontology) | Knowledge (epistemology) | Typical methods |
|---|---|---|---|
| Positivism | Objective, measurable | Observation and measurement; hypotheses tested | Experiments, surveys, statistics |
| Interpretivism | Socially constructed | Understanding meanings in context | Interviews, case studies, thematic analysis |
| Pragmatism | Whatever works to answer the question | Mixed; problem-centred | Mixed methods |
| Critical | Shaped by power relations | Knowledge for emancipation | Critical ethnography, action research |
| Design science (often described as a paradigm in IS) | — | Knowledge through building and evaluating artefacts | Build–evaluate cycles |

Many IS FYPs adopt **pragmatism** with a **design science** strategy and **mixed methods**.

### 5.2 Research strategies
- **Design science research (DSR):** create and evaluate IT artefacts (constructs, models, methods, instantiations) that solve identified problems (Hevner et al., 2004). The process model of Peffers et al. (2007) has six activities:
  1. problem identification and motivation;
  2. define the objectives of a solution;
  3. design and development;
  4. demonstration;
  5. evaluation;
  6. communication.
- **Survey:** standardised data from many respondents, for describing or testing relationships.
- **Case study:** an in-depth study of one or a few cases in a real context.
- **Experiment:** manipulate variables under controlled conditions (e.g. comparing two interface designs).
- **Action research:** the researcher participates in changing a situation, in cycles of plan–act–observe–reflect.

### 5.3 Approaches and data
| | Quantitative | Qualitative | Mixed |
|---|---|---|---|
| Data | Numbers (Likert scores, times, counts) | Words, observations | Both |
| Analysis | Descriptive and inferential statistics | Thematic analysis, coding | Integrated |
| Strength | Generalisable (with a good sample) | Depth, meaning | Complementary |
| FYP example | SUS scores, task completion times | Interviews with wardens | Interviews (RQ1) + SUS and tasks (RQ4) |

### 5.4 Mapping DSR to an FYP
| DSR activity (Peffers) | Running example | RQ | Methods |
|---|---|---|---|
| 1 Problem identification | Untracked maintenance requests | RQ1 | Interviews with wardens; a resident survey; document review |
| 2 Objectives of a solution | Tracking, prioritisation, bilingual, low-bandwidth | RQ2 | Requirements elicitation and analysis |
| 3 Design and development | A web app with a layered design | RQ3 | Incremental development (Scrum-lite sprints) |
| 4 Demonstration | A pilot in one hostel block | RQ3/4 | Scenario walkthroughs |
| 5 Evaluation | Usability and usefulness | RQ4 | SUS, task success, interviews |
| 6 Communication | Report and defence | — | — |

Hevner et al.'s guidelines remind you to: produce an artefact; address a relevant problem; evaluate rigorously; contribute; use rigorous methods; treat design as a search process; and communicate.

### 5.5 Software development methodology inside DSR
Choose the build approach from [[SD-02 Software Process Models]]: often iterative or prototyping, or Scrum with 1–2-week sprints, because requirements will be refined with the users. Justify it briefly. It's part of the "design and development" activity, not a replacement for the research methodology.

## 6. Terminology
| Term | Meaning |
|---|---|
| Ontology / epistemology | Assumptions about reality / about how knowledge is gained |
| Methodology vs method | The overall strategy vs a specific technique |
| Artefact (DSR) | Constructs, models, methods or instantiations (systems) |
| Triangulation | Using multiple data sources or methods to strengthen findings |
| Validity / reliability | Measuring what's intended / consistency of measurement |
| Thematic analysis | Identifying patterns (themes) in qualitative data |

## 7. Step-by-step: writing the methodology section
1. **Paradigm:** state it and justify it (e.g. pragmatism: the RQs need both an understanding of the context and the measurement of usability).
2. **Strategy:** DSR, citing Hevner et al. (2004) and Peffers et al. (2007). Map the activities to your RQs (table §5.4).
3. **Methods per RQ:** data collection (FYP-07), participants and sampling, instruments, and analysis.
4. **Development methodology** for the artefact, with a justification.
5. **Evaluation design:** criteria, measures, participants, procedure (FYP-07).
6. **Ethics:** approvals, consent, data handling (FYP-10).
7. **Limitations of the methodology.**

## 8. Diagram: DSR cycle for the project
```mermaid
flowchart LR
    P[1 Problem: RQ1 interviews/survey] --> O[2 Objectives: RQ2 requirements]
    O --> D[3 Design & build: sprints]
    D --> DM[4 Demonstrate: pilot]
    DM --> E[5 Evaluate: SUS, tasks, interviews]
    E -->|iterate| D
    E --> C[6 Communicate: report & defence]
```

## 9. Worked examples

### Example 1 (basic): methodology vs method
| Statement | Category |
|---|---|
| Design science research | Methodology (strategy) |
| Semi-structured interviews | Method (data collection) |
| Thematic analysis | Method (analysis) |
| Scrum | Software development methodology |
| Pragmatism | Paradigm |

### Example 2 (intermediate): justifying DSR over a survey study
"The study's primary aim is to develop and evaluate an IT artefact that addresses an identified organisational problem. Design science research is appropriate because it treats artefact construction and evaluation as the means of generating knowledge (Hevner et al., 2004), whereas a survey strategy alone would describe current conditions without producing or testing a solution. Surveys and interviews are nevertheless used *within* the DSR process, for problem identification (RQ1) and evaluation (RQ4)."

### Example 3 (challenging): a misaligned methodology
A draft says: "Paradigm: positivism. Strategy: case study. Methods: build an app using agile. Evaluation: interviews." **Problems:**
- Positivism doesn't fit interpretive interviews as the main evidence.
- "Case study" doesn't describe building an artefact.
- "Agile" is a development method, not research.

**Fix:**
- pragmatism + DSR;
- methods per RQ (interviews and a survey for RQ1; requirements analysis for RQ2; iterative development for RQ3; SUS, tasks and interviews for RQ4);
- an explicit evaluation design.

## 10. Application: your methodology chapter outline
1. Research philosophy (paradigm), with justification.
2. Research strategy (DSR), with an activity-to-RQ table.
3. Data collection methods and instruments (FYP-07).
4. Population, sampling and participants (FYP-07).
5. Data analysis (statistics, thematic analysis).
6. System development methodology and tools (FYP-08).
7. Evaluation plan.
8. Ethical considerations (FYP-10).
9. Methodological limitations.

## 11. Common mistakes
| Mistake | Fix |
|---|---|
| "Methodology: agile" | Agile is the development approach; use DSR (or another research strategy) as the methodology |
| A paradigm stated but not justified | Link it to the nature of the RQs |
| Methods that don't map to the RQs | A table: RQ → method → data → analysis |
| No evaluation design | Criteria, measures, participants, procedure |
| Copying a methodology from another project | Adapt it to your RQs and context |

## 12. Comparison: research strategies for IS FYPs
| Strategy | Produces | Fits when |
|---|---|---|
| DSR | An evaluated artefact | Building a system to solve a problem (most IS FYPs) |
| Survey | Descriptive or relational findings | Measuring attitudes or behaviour in a population |
| Case study | Rich understanding of a context | "How/why" questions in one organisation |
| Experiment | Causal evidence | Comparing designs under control |
| Action research | Change plus learning | You're embedded in the organisation and can iterate with it |

## 13. Practice
**L1** 1. Define ontology and epistemology. 2. List Peffers' six DSR activities.

**L2** 3. Classify 6 statements as paradigm, methodology, method or development methodology. 4. Explain why pragmatism often suits IS FYPs.

**L3** 5. Map DSR activities to your own RQs in a table. 6. Write a 150-word justification of your strategy.

**L4** 7. Compare DSR and action research for a project embedded in a hostel office. 8. Critique a past proposal's methodology section for alignment.

**L5** 9. Write the complete methodology chapter outline (§10) for your project, with a paragraph per section.

## 14. Hints
> [!tip]- Hints
> 2: problem, objectives, design and development, demonstration, evaluation, communication. 4: mixed RQs (understand + build + measure). 7: the researcher's role and the organisation's involvement differ.

## 15. Worked solutions
> [!success]- Solutions 1–2
> 1. Ontology: assumptions about the nature of reality (objective vs socially constructed). Epistemology: assumptions about how we can know it (measurement vs interpretation). 2. Problem identification and motivation; define objectives of a solution; design and development; demonstration; evaluation; communication.

> [!success]- Solution 4
> IS FYPs usually combine questions about **understanding a context** (best suited to qualitative, interpretive methods), **building an artefact**, and **measuring its quality** (best suited to quantitative measures like the SUS and task times). Pragmatism accepts whichever methods best answer each question, which supports mixed methods within DSR.

> [!success]- Solution 7
> **DSR:** the main output is an artefact plus its evaluation. The researcher builds; the organisation provides the context and the evaluators. **Action research:** the researcher works *with* the organisation to change practice through repeated plan–act–observe–reflect cycles; the main output is organisational change plus learning. If you're embedded with the hostel office and will repeatedly change *their process* (not just the software), action research or "action design research" fits. For a time-boxed FYP producing a system, DSR is usually more practical.

## 16. Self-test (pass ≥ 4/5)
1. Is Scrum a research methodology? 2. What do Hevner et al. say must be evaluated? 3. Which paradigm suits mixed methods? 4. Name two artefact types in DSR. 5. Why map methods to RQs?
> [!success]- Answers
> 1. No: it's a software development approach. 2. The artefact's utility, quality and efficacy, rigorously. 3. Pragmatism. 4. Constructs, models, methods, instantiations (any two). 5. To show every question has a way of being answered, and that nothing in the method is unjustified.

## 17. Flashcards
#flashcards/fyp
Methodology vs method?::The overall research strategy vs a specific data-collection or analysis technique.
DSR (Peffers) activities?::Problem, objectives, design and development, demonstration, evaluation, communication.
Typical IS FYP stance?::Pragmatism, a design science strategy, mixed methods.
Where does Scrum fit?::In the design-and-development activity, for building the artefact.

## 18. Blank-page recall
Draw the DSR cycle for your project, with the RQs and methods attached to each activity.

## 19. Revision summary
- Paradigm (worldview) → methodology (strategy) → methods (techniques) → analysis, all aligned with the RQs.
- DSR builds and evaluates artefacts. Peffers' six activities map neatly onto FYP RQs.
- Mixed methods: qualitative to understand the context, quantitative to measure quality.
- The software development methodology sits inside DSR.

## 20. Links
Prev: [[FYP-04 Literature Review Synthesis, Research Gaps and Contribution]] · Next: [[FYP-06 Requirements Gathering, Stakeholder and Feasibility Analysis]] · Template: [[FYP-T07 Methodology]] · Related: [[X-06 Research Methodology Applied to the Final Year Project]], [[SD-02 Software Process Models]]

## 21. Sources
- Hevner, A. R., March, S. T., Park, J. & Ram, S., "Design science in information systems research", *MIS Quarterly*, 28(1), 2004, pp. 75–105.
- Peffers, K., Tuunanen, T., Rothenberger, M. A. & Chatterjee, S., "A design science research methodology for information systems research", *Journal of Management Information Systems*, 24(3), 2007, pp. 45–77.
- Saunders, M., Lewis, P. & Thornhill, A., *Research Methods for Business Students*, 8th ed., Pearson, 2019 (the "research onion" of philosophies and strategies).
- Creswell, J. W. & Creswell, J. D., *Research Design*, 5th ed., SAGE, 2018.
- *(Not checked online during the build, because there was no network access. Verify them before citing.)*

## 22. Mastery checklist
- [ ] I can explain and justify my paradigm and strategy
- [ ] I mapped DSR activities and methods to my RQs
- [ ] I distinguished the research and development methodologies
- [ ] Reviews scheduled
