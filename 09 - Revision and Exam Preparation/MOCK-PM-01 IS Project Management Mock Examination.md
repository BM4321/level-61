---
title: "IS Project Management Mock Examination"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "MOCK-PM-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - project-management
  - exam
---

# MOCK-PM-01 IS Project Management Mock Examination

> [!warning] A designed practice paper
> This is **not** a past paper; the format (3 hours, 100 marks, answer all six questions) is designed. Check the real format with your lecturer. Every number in the marking guide is computed with `05 - Information System Project Management/code/pm_tools.py` in `09 - Revision and Exam Preparation/code/tests/test_mock_pm.py`. The organisation and figures are fictional (TZS).

**Instructions (designed):** 3 hours. Answer **all** questions. Show your working in tables. A calculator and a standard normal table are assumed to be allowed.

**Scenario.** *Kilele College* (fictional) is replacing its paper-based library system. You are the project manager.

---

**Q1 Scheduling (20 marks).**

| ID | Activity | Weeks | Predecessors |
|---|---|---|---|
| A | Requirements | 3 | — |
| B | System design | 4 | A |
| C | Hardware specification | 2 | A |
| D | Software development | 5 | B |
| E | Data preparation | 3 | C |
| F | Hardware procurement | 4 | C |
| G | Data migration | 2 | D, E |
| H | Hardware installation | 3 | F |
| I | Testing and go-live | 2 | G, H |

(a) Draw the activity-on-node network. *(4)* (b) Compute ES, EF, LS, LF and total float for every activity; give the critical path and the project duration. *(10)* (c) Give the free float of E and of C, and explain the difference between total and free float using these two. *(3)* (d) The supplier says procurement (F) will take 7 weeks instead of 4. What's the new duration and critical path? *(3)*

**Q2 PERT (14 marks).** Three-point estimates (optimistic, most likely, pessimistic) for the critical activities are A (2, 3, 4), B (3, 4, 8), D (4, 5, 9), G (1, 2, 3), I (1, 2, 4).
(a) Compute the expected duration and standard deviation of each activity, and of the critical path. *(6)* (b) Estimate the probability of finishing within 18 weeks. *(4)* (c) What duration gives 90% confidence? *(2)* (d) Why might this probability be optimistic? *(2)*

**Q3 Earned value (18 marks).** At the end of week 8: BAC = 120 M, PV = 60 M, EV = 54 M, AC = 63 M.
(a) Compute SV, CV, SPI and CPI, and interpret them. *(6)* (b) Compute EAC (assuming the current cost efficiency continues), ETC and VAC. *(6)* (c) Compute the TCPI needed to finish on the original budget, and comment on its realism. *(3)* (d) Compute EAC if the overrun was a one-off event, and say when you'd use each EAC. *(3)*

**Q4 Business case (14 marks).** The system costs 50 M now and is expected to save 15 M, 20 M, 20 M and 15 M at the ends of years 1–4.
(a) Compute the NPV at 12%. *(5)* (b) Compute the simple payback period and the discounted payback period at 12%. *(5)* (c) Compute the ROI over the four years, and explain why NPV is a better basis for the decision. *(4)*

**Q5 Risk (16 marks).**
(a) Compute the EMV of: R1, probability 0.3, impact 10 M; R2, probability 0.1, impact 40 M. Which deserves more contingency? *(4)*
(b) Decision tree (costs): *build in-house* costs 30 M with probability 0.6, or 45 M with probability 0.4; *buy a package* costs 32 M with probability 0.8, or 40 M with probability 0.2. Which option has the lower expected cost? What else should influence the decision? *(8)*
(c) Give one example each of avoid, mitigate, transfer and accept for this project. *(4)*

**Q6 People, quality and agile (18 marks).**
(a) The project has 12 stakeholders who communicate directly. How many communication channels are there? What does this imply for the communication plan? *(4)*
(b) Defects found in testing, by origin: coding 25, requirements 18, design 7, testing 5, deployment 3, documentation 2. Produce a Pareto table, and recommend where to act. *(6)*
(c) A later phase is run in Scrum. 80 story points remain; the last three sprints achieved 18, 22 and 20 points. Forecast the number of sprints (optimistic, average, pessimistic). *(4)*
(d) The head librarian and the IT officer disagree about whether to migrate old loan records. Describe how you'd resolve the conflict. *(4)*

---

## Marking guide

> [!success]- Q1
> (b)
>
> | Act | ES | EF | LS | LF | TF |
> |---|---|---|---|---|---|
> | A | 0 | 3 | 0 | 3 | 0 |
> | B | 3 | 7 | 3 | 7 | 0 |
> | C | 3 | 5 | 5 | 7 | 2 |
> | D | 7 | 12 | 7 | 12 | 0 |
> | E | 5 | 8 | 9 | 12 | 4 |
> | F | 5 | 9 | 7 | 11 | 2 |
> | G | 12 | 14 | 12 | 14 | 0 |
> | H | 9 | 12 | 11 | 14 | 2 |
> | I | 14 | 16 | 14 | 16 | 0 |
>
> Critical path **A-B-D-G-I**, **16 weeks**. Paths: A-B-D-G-I 16; A-C-F-H-I 14; A-C-E-G-I 12. *(Forward pass 4, backward pass 4, path and duration 2.)*
> (c) Free float: E **4** (its successor G can't start before week 12 anyway, so E can slip 4 weeks without delaying any successor); C **0** (any slip delays the early start of E and F), although C's total float is 2. Total float is shared along the path C-F-H; free float belongs to the activity alone. *(3.)*
> (d) F = 7 makes A-C-F-H-I = 3 + 2 + 7 + 3 + 2 = **17 weeks**, the new critical path (F had only 2 weeks of float, so a 3-week slip delays the project 1 week). *(3.)*

> [!success]- Q2
> (a) $t_e = (o + 4m + p)/6$, $\sigma = (p - o)/6$: A 3.0, 0.333; B 4.5, 0.833; D 5.5, 0.833; G 2.0, 0.333; I 2.17, 0.5. Path: $T_e$ = **17.17** weeks; $\sigma = \sqrt{\sum \sigma_i^2} =$ **1.36**. *(6.)*
> (b) $z = (18 - 17.17)/1.36 \approx 0.61$ → $P \approx$ **0.73**. *(4.)*
> (c) $T = 17.17 + 1.2816 \times 1.36 \approx$ **18.9 weeks**. *(2.)*
> (d) It considers only one path. A-C-F-H-I (14 weeks expected) could become critical if F slips (merge bias), and the activities may not be independent. A Monte Carlo simulation over the whole network handles both ([[PM-07 PERT and Schedule Estimation]]). *(2.)*

> [!success]- Q3
> (a) SV = 54 − 60 = **−6 M**; CV = 54 − 63 = **−9 M**; SPI = **0.90** (behind schedule); CPI = **0.857** (over budget: each 1 M spent earns 0.857 M of work). *(6.)*
> (b) EAC = BAC/CPI = 120/0.857 = **140 M**; ETC = 140 − 63 = **77 M**; VAC = 120 − 140 = **−20 M**. *(6.)*
> (c) TCPI = (120 − 54)/(120 − 63) = 66/57 = **1.158**: the remaining work must be done 16% more efficiently than planned, while the project is running at 0.857. That's unrealistic without a change in scope or method; ask for a revised budget instead. *(3.)*
> (d) Atypical EAC = AC + (BAC − EV) = 63 + 66 = **129 M**: use it when the cause of the overrun won't recur (e.g. a one-off hardware price rise); use BAC/CPI when the inefficiency is systemic. *(3.)*

> [!success]- Q4
> (a) NPV = −50 + 15/1.12 + 20/1.12² + 20/1.12³ + 15/1.12⁴ ≈ **+3.11 M**: positive, so the project earns more than 12%. (Its IRR is about 14.9%.) *(5.)*
> (b) Cumulative: −35, −15, +5 → simple payback **2.75 years** (15 of the 20 M in year 3). Discounted: **≈ 3.67 years**. *(5.)*
> (c) ROI = (70 − 50)/50 = **40%** over 4 years. ROI ignores the timing of the cash flows and the cost of capital; NPV accounts for both, and shows value in today's money. *(4.)*

> [!success]- Q5
> (a) R1 EMV = **3 M**; R2 EMV = **4 M**. R2 needs more contingency, despite its low probability: high impact. *(4.)*
> (b) Build: 0.6 × 30 + 0.4 × 45 = **36.0 M**. Buy: 0.8 × 32 + 0.2 × 40 = **33.6 M**. **Buy** has the lower expected cost. Other factors: fit to requirements, vendor viability and support, customisation limits, data ownership and exit costs, internal skills, risk attitude (build has the larger worst case). *(4 + 4.)*
> (c) Avoid: don't migrate 20 years of unreliable loan history; mitigate: a data-cleansing spike before migration; transfer: a fixed-price contract or warranty with the supplier; accept: a 1-week slip in training, covered by contingency. *(4.)*

> [!success]- Q6
> (a) $n(n - 1)/2 = 12 \times 11/2 =$ **66** channels: too many for ad hoc communication. Use a communication plan with defined channels, hub-and-spoke reporting through the PM, and targeted messages per stakeholder group. *(4.)*
> (b)
>
> | Origin | Count | Cumulative % |
> |---|---|---|
> | coding | 25 | 41.7 |
> | requirements | 18 | 71.7 |
> | design | 7 | 83.3 |
> | testing | 5 | 91.7 |
> | deployment | 3 | 96.7 |
> | documentation | 2 | 100.0 |
>
> Coding and requirements cause about 72% of the 60 defects: invest in code review and unit testing, and in requirements reviews with the librarians. *(6.)*
> (c) 80/22 → **4**; 80/20 → **4**; 80/18 → **5** sprints. *(4.)*
> (d) Understand both interests (history for reporting vs data quality and effort); use collaborating / problem-solving: e.g. migrate the last 3 years, archive the rest read-only; record the decision with the sponsor; escalate only if needed ([[PM-15 Team Leadership and Conflict Management]]). *(4.)*

**Self-assessment (designed):** ≥ 70 strong; 50–69 secure; < 50 on any question → that topic goes to [[Weak Area Tracker]].

Back to [[Exam Technique and Assessment Strategy]] · [[QB-PM Project Management Question Bank]] · [[PM 00 Dashboard]]
