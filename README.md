---
title: "Semester 6 Obsidian Mastery Vault — README"
type: "system"
tags:
  - semester-6
  - system
---

# Semester 6 Obsidian Mastery Vault

A structured, interlinked learning system for six Computer Science diploma modules. It takes you from foundations to applied, defensible competence. It is a working vault of lessons, worked examples, exercises with separated solutions, labs, projects, mock exams and a mastery system, not just an outline.

> [!warning] Curriculum status: PROVISIONAL
> No official institutional syllabus, course outline, prescribed textbook list or past paper was supplied, and none could be found online for these module codes (searched 2026-10-19). The topic inventory is therefore a **standard undergraduate/diploma curriculum** that I designed. Every topic is labelled `provisional-core`, `supplementary` or `optional-advanced`. **No topic is claimed to be definitely examinable.** When you get your official module descriptors, follow [[Syllabus Verification Log]] to reconcile them.

## 1. Opening the vault in Obsidian

1. Clone or download this repository (`bm4321/level-61`, branch `claude/compassionate-fermi-btnhxw`) to a local folder.
2. In Obsidian: **Open folder as vault** → select the folder that contains this README.
3. Open **[[00 Dashboard]]** (in `00 - START HERE/`). It always tells you the next action.
4. Recommended core settings (Settings → Files & Links):
   - *New link format*: **Shortest path when possible** (all links in this vault use unique note names).
   - *Use [[Wikilinks]]*: **on**.
5. Optional community plugins (the vault works fully without them):
   - **Dataview**: powers the live tables in [[Progress Tracker]]; static tables are provided as a fallback.
   - **Spaced Repetition**: reads the `question::answer` flashcards found in every lesson.

## 2. Folder structure

| Folder | Purpose |
|---|---|
| `00 - START HERE/` | Dashboard, semester roadmap, weekly planner, progress tracker, next actions |
| `01 - Curriculum and Syllabi/` | Module register (codes, credits, LTP), master curriculum inventory, syllabus verification log |
| `02 - Cyber Security/` | ITT06102: dashboard, curriculum map, lessons |
| `03 - Discrete Mathematics/` | GST06106: dashboard, curriculum map, lessons |
| `04 - Final Year Project I/` | CST06103: dashboard, lessons, project templates, proposal workflow |
| `05 - Information System Project Management/` | ITT06105: dashboard, lessons, case studies, PM artifacts |
| `06 - Python Programming/` | CST06102: dashboard, lessons, runnable `code/` (examples, exercises, solutions, tests) |
| `07 - Software Design and Development/` | CST06101: dashboard, lessons, running LabBook case study, flawed-design clinic |
| `08 - Cross-Module Connections/` | Integration notes, integrated case studies, the full-lifecycle capstone |
| `09 - Revision and Exam Preparation/` | Mock exams with marking guides, question bank, review schedule, mistake log |
| `10 - Projects and Practical Labs/` | Python projects (reference implementations and tests), cyber security labs |
| `11 - Mind Maps and Visual Library/` | Semester concept map plus one mind-map index per module |
| `12 - Glossary and References/` | Glossary, source register, citation conventions |
| `99 - Templates and System/` | Note templates, metadata schema, vault validation script |

## 3. Naming conventions

- **Lessons**: `<TOPIC-ID> <Title>.md`, e.g. `PY-06 Functions, Parameters, Return Values and Scope.md`. The ID prefix keeps lessons in learning (dependency) order and makes every name unique.
- **Topic ID prefixes**: `CS` Cyber Security · `DM` Discrete Mathematics · `FYP` Final Year Project I · `PM` IS Project Management · `PY` Python Programming · `SD` Software Design and Development · `X` cross-module.
- **Dashboards**: `<Prefix> 00 Dashboard.md`. **Curriculum maps**: `<Prefix> 01 Curriculum Map.md`.
- **Labs**: `LAB-CS-NN …`; **projects**: `PRJ-PY-NN …`; **mock exams**: `MOCK-<prefix>-NN …`.
- Each filename is unique across the vault, so `[[Note Name]]` always resolves to exactly one note.

## 4. How a lesson is built

Each substantive lesson follows the template in [[Lesson Template]]: objectives → why it matters → prerequisites → intuition → rigorous explanation → terminology → diagrams → graded worked examples → application → common mistakes → comparisons → practice (Levels 1–5) → **hints** → **solutions** (collapsed callouts, so you can attempt the problems first) → self-test → flashcards → summary → links → sources → mastery checklist.

Solutions sit in folded callouts (`> [!success]- Solution`). Click to expand them, but only after you have made an honest attempt.

## 5. Metadata (YAML frontmatter)

The full field list is in [[Metadata Schema]]. Key fields:

```yaml
title: "Functions, Parameters, Return Values and Scope"
module: "Python Programming"
module_code: "CST06102"
topic_id: "PY-06"
type: "lesson"            # lesson | dashboard | curriculum-map | lab | project | exam | template | case-study | system | index
unit: "U2 Functions and Algorithms"
difficulty: "beginner"    # beginner | intermediate | advanced
syllabus_status: "provisional-core"   # provisional-core | supplementary | optional-advanced | verified
status: "not-started"     # not-started | learning | reviewing | mastered
mastery: 0                # 0–5 rubric, see Mastery Rubric
prerequisites: ["[[PY-05 Loops and Iteration]]"]
tags: [semester-6, python]
```

Update `status`, `mastery` and `last_reviewed` yourself as you study.

## 6. Running the Python code

Requires **Python 3.10 or newer**. The code was tested on CPython 3.13.

```bash
cd "06 - Python Programming/code"
python -m pip install pytest      # once
python -m pytest                  # runs tests against the reference solutions
python examples/py06_functions.py # run any example directly
```

Projects in `10 - Projects and Practical Labs/Python Projects/` each have their own `README.md` and test suite.

## 7. Maintaining the vault

1. **Validate** after each edit session:
   ```bash
   python "99 - Templates and System/scripts/validate_vault.py"
   ```
   It checks broken wikilinks, duplicate note names and topic IDs, missing metadata, near-empty notes, Python code fences that fail to parse, and malformed Mermaid blocks.
2. Record changes in [[CHANGELOG]] and the current state in [[BUILD-STATUS]].
3. When official syllabus documents arrive, follow the process in [[Syllabus Verification Log]].
4. Never commit secrets, real passwords or personal data. All sample data in this vault is fictional.

## 8. Ethics notice (Cyber Security)

All security labs are **defensive** and run only on your own machine or on intentionally vulnerable training environments you control. Never test systems you do not own or lack written permission to assess. Toy cryptography in this vault exists for teaching only. **It is never suitable for production.**
