---
title: "Syllabus Verification Log"
type: "system"
tags:
  - semester-6
  - curriculum
  - verification
---

# Syllabus Verification Log

This note tracks what is **known**, what is **assumed**, and how to replace assumptions with official facts.

## 1. Searches performed

| Date | Where | Query / action | Result |
|---|---|---|---|
| 2026-10-19 | Supplied files | Inspected the repository/vault (it was empty) | No syllabus, outline, textbook list or past paper supplied |
| 2026-10-19 | Web search | `"CST06102" OR "ITT06102" OR "GST06106" Python Programming NTA Level 6 curriculum` | No document mentioning these codes was found |
| 2026-10-19 | Web search | `NACTVET NTA Level 6 Computer Science curriculum "Software Design and Development" "Final Year Project I"` | An Open University of Tanzania page for an *Ordinary Diploma in Computer Science, NTA Level 6* (https://www.out.ac.tz/?p=4338) was found. Its module list is **different** (e.g. Object Oriented Programming, System Analysis & Design), so it is **not** your curriculum and was not used as a source. |

**Conclusion:** the curriculum is **PROVISIONAL**. Every lesson carries `syllabus_status: provisional-core | supplementary | optional-advanced`.

## 2. What is verified

- Module names, codes, credits and LTP values (from you): see [[Module Register]].

## 3. What is assumed (and must be checked)

| Assumption | Where it affects the vault | How to verify |
|---|---|---|
| Topic lists per module | all lessons, mock exams | Obtain the official module descriptor / course outline |
| Learning outcomes | dashboards ("Evidence of mastery") | Module descriptor |
| Assessment pattern (e.g. coursework vs final exam weighting) | mock exam design, [[Exam Technique and Assessment Strategy]] | Course outline or lecturer |
| Meaning of LTP | [[Weekly Study Planner]] | Programme handbook |
| Prescribed textbooks | lesson "Sources" sections use widely recognised references instead | Reading list from lecturer |
| Final Year Project I deliverable (proposal? interim report? presentation?) | [[FYP 02 Idea-to-Defense Workflow]] | Project coordinator / project handbook |
| Referencing style required (APA, IEEE, Harvard) | [[Citation Conventions]] | Project handbook |

## 4. Reconciliation procedure (do this when official documents arrive)

1. Save the document (PDF or photos) in `01 - Curriculum and Syllabi/official/` and add a row to section 1.
2. For each module, copy the official topic list into a new section below, *Official topic list — <code>*.
3. Map each official topic to a vault topic ID in the table in section 5.
   - **Match found** → change that lesson's `syllabus_status` to `verified`.
   - **Official topic with no vault lesson** → add it to [[BUILD-STATUS]] under *Gaps*, then create the lesson from [[Lesson Template]].
   - **Vault lesson not in the official list** → change `syllabus_status` to `supplementary` (keep it; it is still useful).
4. Replace provisional learning outcomes on the module dashboard with the official ones, quoted exactly.
5. Rebuild mock exams so they sample only verified topics, using the official marks pattern.
6. Run the validator and record the change in [[CHANGELOG]].

## 5. Official-to-vault mapping

*(Empty until official documents are supplied. Do not fill it from memory or guesswork.)*

| Official topic (verbatim) | Module code | Vault topic ID | Action taken |
|---|---|---|---|
| — | — | — | — |
