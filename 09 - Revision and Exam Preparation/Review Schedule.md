---
title: "Review Schedule"
type: "tracker"
tags:
  - semester-6
  - revision
  - tracker
---

# Review Schedule

Spaced retrieval beats re-reading. Each lesson is reviewed at **D+1, D+3, D+7, D+14 and D+30** after you first study it (D = the day you complete its L1–L3 practice). Each review is a short closed-book session using [[Revision Session Template]]: blank-page recall, the lesson's self-test, and two practice problems.

## Rules
| Review score | Next step |
|---|---|
| ≥ 80% | Move to the next interval |
| 50–79% | Repeat the same interval |
| < 50% | Restart at D+1, drop `mastery` by one ([[Mastery Rubric]]), and add the topic to [[Weak Area Tracker]] |

After a passed D+30 review, review the topic monthly until the exam, or as part of a mock.

## How to record it
1. When you finish a lesson's practice, set `last_reviewed:` to today and `next_review:` to tomorrow in its frontmatter.
2. After each review, update both fields using the rules above.
3. Each Sunday, list the reviews due in the coming week ([[Weekly Study Planner]]).

## Due this week (Dataview)
If the Dataview plugin is installed, this table lists every lesson whose review is due within 7 days (the query was not run in Obsidian during the build; the manual log below always works):

```dataview
TABLE module, topic_id, mastery, next_review
FROM ""
WHERE type = "lesson" AND next_review AND date(next_review) <= date(today) + dur(7 days)
SORT next_review ASC
```

## Manual log (works without plugins)
| Topic | First studied (D) | D+1 | D+3 | D+7 | D+14 | D+30 | Notes |
|---|---|---|---|---|---|---|---|
| ____ | ____ | ☐ | ☐ | ☐ | ☐ | ☐ | ____ |
| ____ | ____ | ☐ | ☐ | ☐ | ☐ | ☐ | ____ |
| ____ | ____ | ☐ | ☐ | ☐ | ☐ | ☐ | ____ |

## Load check
Learning about 4 new lessons a week creates about 20 reviews a week once the cycle is full (each lesson has 5 reviews). At roughly 15–20 minutes each, that's 5–7 hours a week: budget for it in [[X-07 Scheduling Your Own Semester with CPM]].

Back to [[00 Dashboard]] · [[Exam Technique and Assessment Strategy]]
