---
title: "Project Management Question Bank"
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "QB-PM"
type: "question-bank"
tags:
  - semester-6
  - project-management
  - exam
---

# QB-PM Project Management Question Bank

> [!info] How to use
> Two questions per lesson. Answer closed book, then open the folded answer. Every number is computed with `pm_tools.py` in `09 - Revision and Exam Preparation/code/tests/test_qb.py` (`test_qb_pm_numbers`). Log misses in [[Mistake Log]].

## [[PM-01 Project Fundamentals and Organizational Context]]

**Q1 (L1).** What makes a project different from operations?

> [!success]- Answer
> A project is temporary (a defined start and end) and creates a unique product, service or result; operations are ongoing and repetitive.

**Q2 (L2).** How does a functional organisation limit a project manager compared with a projectized one?

> [!success]- Answer
> In a functional organisation the PM has little authority and borrows staff part-time from department heads; in a projectized one the PM has high authority and a dedicated team.

## [[PM-02 Project Lifecycles, Process Groups and Methodologies]]

**Q3 (L1).** Name the five process groups.

> [!success]- Answer
> Initiating, planning, executing, monitoring and controlling, closing.

**Q4 (L2).** Predictive vs adaptive lifecycle: when would you choose each?

> [!success]- Answer
> Predictive when scope is clear and stable (e.g. a hardware rollout); adaptive when requirements are uncertain and feedback matters (e.g. a new app).

## [[PM-03 Project Initiation, Business Case and Charter]]

**Q5 (L2).** Cash flows −100, +60, +60 (years 0–2). Compute the NPV at 10%.

> [!success]- Answer
> $-100 + 60/1.1 + 60/1.21 \approx$ **+4.13**: positive, so worthwhile at a 10% cost of capital.

**Q6 (L1).** What does a project charter do?

> [!success]- Answer
> It formally authorises the project, names the PM and sponsor, and records the high-level objectives, scope, milestones, budget and risks.

## [[PM-04 Scope Management, Requirements Traceability and WBS]]

**Q7 (L1).** State the 100% rule for a WBS.

> [!success]- Answer
> The WBS includes all the work of the project (and only that work), and each level's children add up to exactly their parent.

**Q8 (L2).** What's scope creep, and what controls it?

> [!success]- Answer
> Uncontrolled growth of scope without matching time, cost or resources; controlled by a baseline and a change control process.

## [[PM-05 Activity Sequencing, Network Diagrams and Gantt Charts]]

**Q9 (L1).** Name the four dependency types.

> [!success]- Answer
> Finish-to-start (most common), start-to-start, finish-to-finish, start-to-finish.

**Q10 (L2).** What does a Gantt chart show that a network diagram doesn't, and vice versa?

> [!success]- Answer
> Gantt: the timeline against calendar dates, and progress. Network: the logical dependencies and the critical path.

## [[PM-06 Critical Path Method and Float]]

**Q11 (L2).** A (2), B (3, after A), C (1, after A), D (2, after B and C). Find the duration, the critical path and C's float.

> [!success]- Answer
> **7**; critical path **A-B-D**; C has **2** weeks of float.

**Q12 (L2).** Can a project have more than one critical path? What does that mean for risk?

> [!success]- Answer
> Yes: several paths with zero float. Risk rises, because a delay on any of them delays the project.

## [[PM-07 PERT and Schedule Estimation]]

**Q13 (L2).** Optimistic 2, most likely 4, pessimistic 12. Find the PERT mean and standard deviation.

> [!success]- Answer
> Mean $(2 + 16 + 12)/6 =$ **5**; σ $= (12 - 2)/6 \approx$ **1.67**.

**Q14 (L3).** A project's mean is 20 weeks with σ = 2. What's the probability of finishing within 22 weeks?

> [!success]- Answer
> $z = 1$ → about **84%**.

## [[PM-08 Resource Allocation and Levelling]]

**Q15 (L2).** Resource levelling vs resource smoothing?

> [!success]- Answer
> Levelling resolves over-allocation even if the end date moves; smoothing adjusts only within float, keeping the end date.

**Q16 (L2).** Why can a resource limit lengthen the project beyond the critical path?

> [!success]- Answer
> Activities that could run in parallel must be serialised when they need the same scarce resource.

## [[PM-09 Cost Estimation and Budgeting]]

**Q17 (L1).** Name three estimating techniques.

> [!success]- Answer
> Analogous, parametric, bottom-up (also three-point).

**Q18 (L2).** Contingency reserve vs management reserve?

> [!success]- Answer
> Contingency covers identified risks ("known unknowns") and is in the cost baseline; management reserve covers unidentified risks and sits outside the baseline, released by management.

## [[PM-10 Earned Value Management]]

**Q19 (L2).** BAC 100, PV 40, EV 36, AC 45. Compute SPI, CPI, EAC (typical) and VAC.

> [!success]- Answer
> SPI **0.9**; CPI **0.8**; EAC = 100/0.8 = **125**; VAC = **−25**.

**Q20 (L3).** Why can SPI recover to 1.0 on a late project?

> [!success]- Answer
> At completion EV = BAC = PV regardless of lateness, so SPI tends to 1; use the critical path (or earned schedule) to judge delay late in the project.

## [[PM-11 Risk Management]]

**Q21 (L1).** Compute the EMV of a risk with probability 0.2 and impact 25 M.

> [!success]- Answer
> **5 M**.

**Q22 (L2).** Give the four negative-risk response strategies.

> [!success]- Answer
> Avoid, mitigate, transfer, accept (escalate is also recognised).

## [[PM-12 Stakeholder and Communication Management]]

**Q23 (L1).** How many communication channels for 5 people? For 8?

> [!success]- Answer
> $5 \cdot 4/2 =$ **10**; $8 \cdot 7/2 =$ **28**.

**Q24 (L2).** How do you manage a high-power, low-interest stakeholder?

> [!success]- Answer
> Keep satisfied: brief, targeted updates on what affects them; consult before decisions that touch their concerns.

## [[PM-13 Quality Management]]

**Q25 (L2).** Samples 10, 12, 11, 9, 13. Compute 3-sigma control limits (sample standard deviation).

> [!success]- Answer
> Mean **11**; σ ≈ 1.58; limits ≈ **6.26** to **15.74**.

**Q26 (L1).** Quality assurance vs quality control?

> [!success]- Answer
> QA: process-focused prevention (standards, reviews). QC: product-focused inspection and testing.

## [[PM-14 Procurement and Change Management]]

**Q27 (L3).** FPIF: target cost 100 M, target fee 10 M, ceiling 120 M, buyer share 70%. Find the point of total assumption, and the final price if actual cost is 110 M.

> [!success]- Answer
> PTA = 100 + (120 − 110)/0.7 ≈ **114.29 M**. Fee = 10 + 0.3 × (100 − 110) = 7 M → price **117 M** (below the ceiling).

**Q28 (L2).** Which contract type puts the most cost risk on the seller?

> [!success]- Answer
> Firm fixed price.

## [[PM-15 Team Leadership and Conflict Management]]

**Q29 (L1).** Name Tuckman's stages.

> [!success]- Answer
> Forming, storming, norming, performing (and adjourning).

**Q30 (L2).** Which conflict mode usually gives the best long-term result, and when is it impractical?

> [!success]- Answer
> Collaborating / problem-solving; impractical under severe time pressure or when the issue is trivial.

## [[PM-16 Agile, Scrum and Hybrid Delivery]]

**Q31 (L1).** Name the three Scrum roles and the four events (besides the sprint itself).

> [!success]- Answer
> Product owner, Scrum master, developers; sprint planning, daily scrum, sprint review, retrospective.

**Q32 (L2).** 80 points remain; recent velocities 18, 22, 20. Forecast sprints (optimistic, average, pessimistic).

> [!success]- Answer
> **4, 4, 5**.

## [[PM-17 Monitoring, Control, Closure and Lessons Learned]]

**Q33 (L1).** List four closure activities.

> [!success]- Answer
> Formal acceptance of deliverables; release of resources; contract closure; lessons learned; archiving project records.

**Q34 (L2).** Payback for −100, +30, +40, +50?

> [!success]- Answer
> After year 2: −30 remaining; year 3 brings 50 → payback **2.6 years**.

Back to [[Question Bank Index]] · [[MOCK-PM-01 IS Project Management Mock Examination]] · [[PM 00 Dashboard]]
