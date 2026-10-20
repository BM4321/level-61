---
title: "PERT and Schedule Estimation"
aliases:
  - PERT
  - Three-point estimate
  - Monte Carlo schedule simulation
  - Estimation techniques
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-07"
type: "lesson"
unit: "U3 Planning"
difficulty: "intermediate"
syllabus_status: "provisional-core"
status: "not-started"
mastery: 0
prerequisites:
  - "[[PM-06 Critical Path Method and Float]]"
  - "[[DM-18 Introductory Discrete Probability]]"
next: "[[PM-08 Resource Allocation and Levelling]]"
last_reviewed: ""
next_review: ""
tags:
  - semester-6
  - project-management
  - estimation
---

# PM-07 PERT and Schedule Estimation

> [!info] Topic card
> **Unit:** U3 · **Time:** 5 h · **Calculator:** `pert`, `pert_project`, `prob_complete_by`, `duration_for_probability` and `monte_carlo` in `code/pm_tools.py`. All the PERT figures are asserted in `test_pert_registration_case`. The Monte Carlo figures come from one seeded run of 10,000 simulations on the build machine (Python 3.13); the test checks them within a tolerance band, because random-number streams can differ between Python versions.

## 1. Learning objectives
1. **Compare** estimation techniques: analogous, parametric, bottom-up, expert judgement, three-point.
2. **Calculate** PERT expected durations and standard deviations, and **combine** them along the critical path.
3. **Compute** the probability of meeting a deadline, and the deadline for a target probability, using the normal approximation.
4. **Explain** PERT's assumptions and **merge bias**, and **interpret** a Monte Carlo simulation.
5. **Set** schedule reserves (contingency) from probabilistic results.

## 2. Why it matters
"The system will be ready in 19 weeks" sounds precise, but it hides uncertainty. Sponsors make better decisions with "about a 55% chance by week 20, and a 93% chance by week 22". PERT turns expert ranges into probabilities, and simulation shows where PERT's simplifications mislead.

## 3. Prerequisites
[[PM-06 Critical Path Method and Float]] · [[DM-18 Introductory Discrete Probability]]: expected value, variance (variances of independent variables add), and the normal distribution.

## 4. Intuition
Ask an expert for three numbers: **best case**, **most likely** and **worst case**. The expected duration leans towards the most likely value, but is pulled towards the long tail, because tasks rarely finish much early but often run late. Adding up many uncertain activities along a path gives a total that is approximately **normal** (the central limit theorem), so normal tables give probabilities.

## 5. Rigorous explanation

### 5.1 Estimation techniques
| Technique | How | Good when |
|---|---|---|
| Analogous (top-down) | Scale from a similar past project | Early, with little detail |
| Parametric | Rate × quantity (e.g. 2 days per report × 15 reports) | Repeatable work with historical rates |
| Bottom-up | Estimate each work package, then sum | Detailed WBS available |
| Expert judgement / Delphi | Experts estimate, often iteratively and anonymously | Novel work |
| Three-point (PERT) | O, M, P per activity | Uncertainty matters |

### 5.2 PERT formulas
For each activity, with optimistic $O$, most likely $M$, pessimistic $P$ (the beta-PERT approximation):
$$t_e = \frac{O + 4M + P}{6}, \qquad \sigma = \frac{P - O}{6}, \qquad \sigma^2 = \left(\frac{P-O}{6}\right)^2$$
Along a path, assuming the activities are **independent**:
$$T_e = \sum t_e, \qquad \sigma_T^2 = \sum \sigma^2, \qquad \sigma_T = \sqrt{\sum \sigma^2}$$
**Add variances, not standard deviations.**

**Probability of finishing by deadline $D$:** $z = (D - T_e)/\sigma_T$, then $P(T \le D) = \Phi(z)$. **Deadline for probability $p$:** $D = T_e + z_p\,\sigma_T$ (e.g. $z_{0.90} = 1.2816$, $z_{0.95} = 1.6449$).

A simpler **triangular** alternative is $(O + M + P)/3$. Know which formula your course uses.

### 5.3 Assumptions and merge bias
PERT assumes:
- activity durations are independent;
- the critical path stays critical;
- the sum is approximately normal.

At **merge points**, several paths must all finish. If a near-critical path is long in a particular run, it becomes critical and pushes the end date later. The true probability of on-time completion is therefore **lower** than single-path PERT suggests. **Monte Carlo simulation** samples every activity many times, recomputes CPM each time, and reads the probabilities off the resulting distribution. It captures merge bias.

### 5.4 Reserves
- **Contingency reserve:** time or cost for identified risks. The PM controls it. It's part of the baseline.
- **Management reserve:** for unknown unknowns. The sponsor controls it. It's outside the baseline.
- Example: plan to week 20 (P ≈ 55%), and commit externally to week 22 (P ≈ 93%). The 2-week gap is the schedule reserve.

## 6. Terminology
| Term | Meaning |
|---|---|
| Optimistic / most likely / pessimistic | Best, usual and worst plausible durations |
| Expected time $t_e$ | The PERT weighted mean |
| Standard deviation / variance | Spread of the duration / its square (additive) |
| z-score | Standard deviations between the deadline and the mean |
| Merge bias | Underestimation of the risk where paths converge |
| Monte Carlo simulation | Repeated random sampling to estimate a distribution |
| P50 / P80 / P90 | The duration with a 50%, 80% or 90% chance of not being exceeded |

## 7. Step-by-step: CASE-01 PERT
Estimates in weeks (O, M, P), with the results from `pert`:

| Act | O | M | P | $t_e$ | σ | σ² |
|---|---|---|---|---|---|---|
| A | 2 | 3 | 4 | 3.0000 | 0.3333 | 0.1111 |
| B | 3 | 4 | 6 | 4.1667 | 0.5000 | 0.2500 |
| C | 1 | 2 | 3 | 2.0000 | 0.3333 | 0.1111 |
| D | 3 | 5 | 10 | 5.5000 | 1.1667 | 1.3611 |
| E | 4 | 6 | 11 | 6.5000 | 1.1667 | 1.3611 |
| F | 3 | 4 | 5 | 4.0000 | 0.3333 | 0.1111 |
| G | 2 | 3 | 5 | 3.1667 | 0.5000 | 0.2500 |
| H | 1 | 2 | 3 | 2.0000 | 0.3333 | 0.1111 |
| I | 1 | 2 | 4 | 2.1667 | 0.5000 | 0.2500 |
| J | 1 | 2 | 3 | 2.0000 | 0.3333 | 0.1111 |
| K | 1 | 1 | 1 | 1.0000 | 0 | 0 |

**Critical path A-B-E-G-J-K** (still the longest using the $t_e$ values: 19.8333, against 17.67, 17.33, 15.67 and 10.17 for the other paths):
- $T_e = 3 + 4.1667 + 6.5 + 3.1667 + 2 + 1 = $ **19.8333 weeks**
- $\sigma_T^2 = 0.1111 + 0.25 + 1.3611 + 0.25 + 0.1111 + 0 = $ **2.0833**, so $\sigma_T =$ **1.4434 weeks**

## 8. Diagram: deadline probabilities
```mermaid
flowchart LR
    W19["Week 19: 28.2%"] --> W20["Week 20: 54.6%"] --> W21["Week 21: 79.1%"] --> W22["Week 22: 93.3%"]
```
*PERT normal approximation, from `prob_complete_by`. Read it as: "the chance the project finishes by week X".*

## 9. Worked examples

### Example 1 (basic): one activity
E: O = 4, M = 6, P = 11. $t_e = (4 + 24 + 11)/6 = 39/6 = $ **6.5 weeks**; σ = (11 − 4)/6 = **1.1667**. Note that $t_e > M$, because the pessimistic tail is long (11 is 5 weeks above the most likely value, but 4 is only 2 below).

### Example 2 (intermediate): probabilities and deadlines (tested)
- P(T ≤ 21): z = (21 − 19.8333)/1.4434 = 0.8083, Φ(0.8083) = **0.7905** (79%).
- P(T ≤ 19) = **0.2819**. The CPM "19 weeks" (most-likely estimates) has only a 28% chance!
- P(T ≤ 20) = **0.5460**. P(T ≤ 22) = **0.9333**.
- 90% deadline: 19.8333 + 1.2816 × 1.4434 = **21.68 weeks**. 95% deadline: **22.21 weeks**.

### Example 3 (challenging): Monte Carlo vs PERT, and merge bias
`monte_carlo(REG, REG_PERT, runs=10_000, seed=2026)` samples every activity from its beta-PERT distribution and recomputes CPM each run. On the build machine:

| Measure | PERT (critical path only) | Monte Carlo (whole network) |
|---|---|---|
| Mean duration | 19.83 | 19.86 |
| Std deviation | 1.44 | 1.57 |
| P(≤ 20 weeks) | 54.6% | 55.2% |
| P(≤ 21 weeks) | **79.1%** | **76.5%** |
| 95th percentile | 22.21 | 22.58 |

**Interpretation:**
- The simulation's spread is wider.
- Its chance of meeting week 21 is lower (76.5% vs 79.1%).
- Its 95th percentile is later.

That's because in some runs another path becomes the longest. In a check of 10,000 sampled networks (same seed), A-B-E-G-J-K was longest in 9,722, **A-D-H-I-J-K** (driven by D's wide 3–10 week range) in 201, and A-B-F-G-J-K in 77. Those 278 runs push the end date later. That's merge bias. For a high-stakes date, quote the simulation.

## 10. Application: committing to a go-live date
For CASE-01, registration must open by week 22 (the start of semester):
- Monte Carlo P(≤ 22) is above 90%, so the date is reasonably safe.
- Set the internal target at week 20, with a 2-week contingency reserve.
- Identify the activities that drive the variance: D (σ² = 1.36) and E (σ² = 1.36). Reduce their uncertainty: order the servers early, with a penalty clause; spike the backend's risky parts in sprint 1. This narrows the distribution more than anything else.

## 11. Common mistakes
| Mistake | Fix |
|---|---|
| Adding standard deviations | Add **variances**, then take the square root |
| Using M as the expected time | $t_e = (O + 4M + P)/6$ |
| Including non-critical activities in $\sigma_T$ | Use the critical path (or simulate the whole network) |
| Quoting the CPM duration as "the date" | Give probabilities, and plan reserves |
| Ignoring merge bias in large networks | Monte Carlo simulation |
| Estimates padded secretly by everyone | Honest three-point estimates; a visible, managed reserve |

## 12. Comparison: CPM vs PERT vs Monte Carlo
| | CPM | PERT | Monte Carlo |
|---|---|---|---|
| Durations | Single estimate | Three-point, giving mean and σ | Distributions |
| Output | One date | Mean ± σ along one path; probabilities | A full distribution over the whole network |
| Merge bias | Ignored | Ignored | Captured |
| Effort | Low | Low | Needs a tool |

## 13. Practice
**L1** 1. Write the PERT $t_e$ and σ formulas. 2. Why do we add variances?

**L2** 3. Compute $t_e$ and σ for O = 2, M = 4, P = 12. 4. A path has $T_e$ = 30 and σ = 2. What's P(T ≤ 33)?

**L3** 5. For CASE-01, what deadline gives an 80% probability (z = 0.8416)? 6. Explain why P(T ≤ 19) is so low even though CPM gives 19 weeks.

**L4** 7. Run `monte_carlo` with D's pessimistic estimate reduced from 10 to 7, and report the change in P(≤ 21). Explain it. 8. Discuss two situations where the independence assumption fails in IS projects.

**L5** 9. Do a three-point estimate for your FYP's activities, compute the PERT probability of meeting your submission date, run a simulation, and write a half-page note to your supervisor with the dates and the reserves.

## 14. Hints
> [!tip]- Hints
> 3: (2 + 16 + 12)/6. 4: z = 1.5, Φ = 0.9332. 5: 19.8333 + 0.8416 × 1.4434. 6: the CPM used M values, but the $t_e$ values are higher (skewed estimates), and there's uncertainty around them. 7: copy `REG_PERT` and change D to (3, 5, 7). 8: a shared team, a common cause (one late requirements change affects many activities).

## 15. Worked solutions
> [!success]- Solutions 1–2
> 1. $t_e = (O + 4M + P)/6$; σ = (P − O)/6. 2. For independent random variables, the variance of a sum is the sum of the variances. Standard deviations don't add.

> [!success]- Solution 3
> $t_e$ = (2 + 16 + 12)/6 = **5.0**; σ = (12 − 2)/6 = **1.6667**. (`pert(2, 4, 12)` gives `(5.0, 1.6666666666666667)`.)

> [!success]- Solution 4
> z = (33 − 30)/2 = 1.5, so Φ(1.5) = **0.9332**. (Check: `prob_complete_by(33, 30, 2)` gives about 0.93319.)

> [!success]- Solution 5
> D = 19.8333 + 0.8416 × 1.4434 = 19.8333 + 1.2148 = **21.05 weeks**. (Check: `duration_for_probability(0.80, te, sd)` gives 21.048.)

> [!success]- Solution 6
> CPM used the most-likely durations (sum = 19). The PERT expected values are higher (19.83), because the estimates are right-skewed (D and E have long pessimistic tails), and the total has spread σ = 1.44. Nineteen is below the mean, so the probability is below 50%: z = (19 − 19.83)/1.44 = −0.577, and Φ(−0.577) = 0.28.

> [!success]- Solution 7
> With D = (3, 5, 7), the same seeded simulation gives P(≤ 21) = **77.35%**, up from 76.5%. D isn't on the PERT critical path, so the PERT figure (79.05%) doesn't change at all. But D's long tail was what made A-D-H-I-J-K occasionally critical. Narrowing it removes some of the merge bias. Lesson: reducing uncertainty on a near-critical activity can improve the schedule's probability, even though CPM and PERT say it doesn't matter.

> [!success]- Solution 8
> 1. **Shared resources:** the same two developers work on B, E and F; if one is ill, several activities slip together (positive correlation). 2. **Common causes:** a late change in registration rules affects design, backend and testing at once. 3. **Learning effects:** early overruns often signal later ones. Positive correlation makes the total's variance **larger** than PERT assumes, so the real risk is higher.

## 16. Self-test (pass ≥ 4/5)
1. $t_e$ for (3, 5, 13)? 2. P(T ≤ $T_e$) under PERT? 3. Which activities' σ go into $\sigma_T$? 4. What does merge bias do to the probability of on-time finishing? 5. Contingency vs management reserve?
> [!success]- Answers
> 1. (3 + 20 + 13)/6 = 6. 2. 50%. 3. Those on the critical path. 4. Lowers it (PERT is optimistic at merges). 5. Contingency: for known risks, PM-controlled, in the baseline. Management: for unknowns, sponsor-controlled, outside the baseline.

## 17. Flashcards
#flashcards/project-management
PERT expected time?::(O + 4M + P) / 6.
PERT standard deviation?::(P − O) / 6.
Project σ along a path?::The square root of the sum of the activity variances.
Probability of a deadline?::Φ((D − Te) / σT).
CASE-01 PERT?::Te = 19.83 weeks, σ = 1.44; P(≤21) = 79% (simulation: about 76.5%).
Merge bias?::Parallel near-critical paths make the real on-time probability lower than single-path PERT suggests.

## 18. Blank-page recall
Rebuild the CASE-01 PERT table for the critical path, and compute P(≤ 21) by hand.

## 19. Revision summary
- Estimation methods: analogous, parametric, bottom-up, expert, three-point.
- PERT: $t_e = (O + 4M + P)/6$, σ = (P − O)/6; add the variances along the critical path; use z-scores for probabilities.
- CASE-01: 19.83 ± 1.44 weeks; P(≤ 21) ≈ 79% by PERT, ≈ 76.5% by simulation (merge bias).
- Quote probabilities, set visible reserves, and reduce the activities that dominate the variance.

## 20. Links
Prev: [[PM-06 Critical Path Method and Float]] · Next: [[PM-08 Resource Allocation and Levelling]] · Related: [[DM-18 Introductory Discrete Probability]], [[PM-11 Risk Management]], [[FYP-09 Project Scheduling, Milestones and Risk Assessment]]

## 21. Sources
- Malcolm, D. G., Roseboom, J. H., Clark, C. E. & Fazar, W., "Application of a technique for research and development program evaluation", *Operations Research*, 7(5), 1959, pp. 646–669 (the original PERT paper).
- PMI, *PMBOK® Guide*, 6th ed., 2017, §6.4 (Estimate Activity Durations) and §11.4 (quantitative risk analysis, simulation).
- Python docs, `statistics.NormalDist` and `random.betavariate`: https://docs.python.org/3/library/statistics.html
- *(Not checked online during the build, because there was no network access.)*

## 22. Mastery checklist
- [ ] I can compute PERT values and path probabilities by hand
- [ ] I can find the deadline for a target probability
- [ ] I can explain merge bias and interpret a simulation
- [ ] Reviews scheduled
