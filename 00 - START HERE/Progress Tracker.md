---
title: "Progress Tracker"
type: "tracker"
tags:
  - semester-6
  - tracker
---

# Progress Tracker

*(The Dataview queries below were written for the Dataview plugin but not run in Obsidian during the build; if one errors, the static checklist still works.)*

Your progress lives in each lesson's frontmatter: `status`, `mastery` (0–5, see [[Mastery Rubric]]), `last_reviewed` and `next_review`. This note summarises them. With the **Dataview** plugin the tables below update live; without it, use the static checklist at the end.

## Readiness rule (per module)
A module is exam-ready when **every `provisional-core` lesson is at mastery ≥ 3, and at least 70% are at mastery ≥ 4** ([[Mastery Rubric]] rule 4).

## Live tables (Dataview)

### Summary by module
```dataview
TABLE length(rows) AS Lessons,
  length(filter(rows, (r) => r.mastery >= 3)) AS "Mastery ≥ 3",
  length(filter(rows, (r) => r.mastery >= 4)) AS "Mastery ≥ 4",
  length(filter(rows, (r) => r.status = "mastered")) AS Mastered
FROM ""
WHERE type = "lesson" AND syllabus_status = "provisional-core"
GROUP BY module
```

### Lessons in progress
```dataview
TABLE module, topic_id, status, mastery, next_review
FROM ""
WHERE type = "lesson" AND (status = "learning" OR status = "reviewing")
SORT module ASC, topic_id ASC
```

### Low mastery on core topics (study next)
```dataview
TABLE module, mastery, status
FROM ""
WHERE type = "lesson" AND syllabus_status = "provisional-core" AND mastery < 3 AND status != "not-started"
SORT mastery ASC
```

## Static checklist (no plugins needed)
Tick a lesson when it reaches mastery ≥ 3; bold it (or add ★) at mastery ≥ 4.

| Module | Core lessons | Supplementary | Dashboard |
|---|---|---|---|
| Python Programming CST06102 | 22 | 3 (PY-18, PY-23, PY-25) | [[PY 00 Dashboard]] |
| Cyber Security ITT06102 | 19 | — | [[CS 00 Dashboard]] |
| Discrete Mathematics GST06106 | 17 | 1 (DM-18) | [[DM 00 Dashboard]] |
| IS Project Management ITT06105 | 17 | — | [[PM 00 Dashboard]] |
| Software Design and Development CST06101 | 17 | — | [[SD 00 Dashboard]] |
| Final Year Project I CST06103 | 12 | — | [[FYP 00 Dashboard]] |
| Cross-module | — | 7 integration lessons | [[X 00 Cross-Module Index]] |

Each dashboard lists its lessons in order; copy the list into the table below, or tick them in the mind maps' outlines (e.g. [[MM-PY Python Programming Mind Map]]).

### My weekly snapshot
| Week | Lessons at ≥ 3 (total) | Lessons at ≥ 4 (total) | Reviews done / due | Mocks done | Top weak area |
|---|---|---|---|---|---|
| ____ | ____ | ____ | ____ | ____ | ____ |

## Practical work
| Item | Done? |
|---|---|
| PRJ-PY-01 to PRJ-PY-05 ([[Labs and Projects Index]]) | ☐ ☐ ☐ ☐ ☐ |
| LAB-CS-01 to LAB-CS-08 | ☐ ☐ ☐ ☐ ☐ ☐ ☐ ☐ |
| PM case studies 1–3, X-CASE-01, X-CASE-02 | ☐ ☐ ☐ ☐ ☐ |
| Mocks: PY, DM, CS, PM, SD, FYP ([[Question Bank Index]]) | ☐ ☐ ☐ ☐ ☐ ☐ |
| FYP templates T01–T15 | ____ / 15 |

Back to [[00 Dashboard]] · [[Review Schedule]] · [[Weak Area Tracker]]
