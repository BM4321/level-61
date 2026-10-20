---
title: "Small Business Point-of-Sale Software"
aliases:
  - CASE-03
  - POS case
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-CASE-03"
type: "case-study"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - case-study
---

# PM-CASE-03 Small Business Point-of-Sale Software

> [!info] About this case
> A **fictional** family-owned hardware shop in Dodoma (2 tills, 6 staff) wants a point-of-sale (POS) system: sales, stock, mobile-money receipts and daily reports. It's a small, agile-friendly project with a tight budget. The figures are asserted in `test_case03`. It's useful for practising business cases, the agile forecasting in PM-16, and scaling PM practices *down*.

## 1. Situation
The owner records sales in a notebook, and reconciles cash and mobile-money payments each evening, which takes about 2 hours a day. Stock-outs of popular items are frequent. Two options are on the table:
- **Option C (custom):** a local developer builds a tailored POS. TZS 8 M up front; estimated benefits of 3.5 M a year (time saved, fewer stock-outs, less shrinkage).
- **Option S (subscription):** a cloud POS service. 1.5 M set-up (hardware, configuration, training), and a net benefit of 1.2 M a year *after* the subscription fees.

## 2. Business case (discount rate 15%, 4 years)
| Measure | Custom (C) | Subscription (S) |
|---|---|---|
| NPV | **1,992,424** | **1,925,974** |
| IRR | 26.86% | 70.54% |
| Simple payback | 2.29 years | 1.25 years |
| Capital at risk | 8.0 M | 1.5 M |

The NPVs are almost equal, but S needs far less capital, pays back faster, and carries less delivery risk. For a small family business with limited cash, **S is the safer recommendation**, *unless* the custom features (e.g. a specific credit-account workflow for builders) are essential and unavailable in the subscription product. Check the data ownership and export terms of the subscription (lock-in).

## 3. Delivery (if Option C is chosen)
- **Approach:** Scrum-lite. One developer, with the owner as product owner; 1-week sprints; a sprint review in the shop each Friday.
- **Backlog:** 64 story points (sales screen, stock, receipts with mobile-money reference, daily report, user roles, backup).
- **Velocity** over the first three sprints: 12, 14 and 15, so `sprints_needed(64, [12, 14, 15])` gives **5–6 sprints** (5 likely).
- **Agile EVM after sprint 4** (BAC 8 M; planned 4 M; earned 3.4 M; actual 3.9 M): SPI **0.85**, CPI **0.872**, EAC **9.18 M**. The overrun mainly came from mobile-money integration taking longer than estimated.
- **Communication:** 4 people (the owner, the developer, the senior cashier, the bookkeeper), so only **6** channels. Weekly face-to-face reviews are enough.

## 4. Risks (for the register)
- Power cuts during sales: a UPS plus offline mode.
- Data loss: automatic daily backup off-site.
- Staff resistance: involve the senior cashier as a champion.
- Mobile-money API changes or fees.
- Developer availability (a single person).
- Customer data privacy (phone numbers on receipts: [[CS-19 Cloud Security and Privacy]]).

## 5. Discussion questions
1. Verify the NPV, IRR and payback figures with `pm_tools`. How sensitive is the custom option to benefits being 20% lower?
2. Which PM artefacts are worth producing for a project this size, and which would be overkill? Justify a "minimum viable" PM toolkit.
3. Write 6 user stories with acceptance criteria for the POS (SD-04 style).
4. The EAC is 9.18 M against an 8 M budget. Give the owner three options, with consequences.
5. Compare the security responsibilities in the two options (shared responsibility model, CS-19).

> [!success]- Model answer notes (1, 2, 4)
> 1. Custom with 2.8 M a year of benefits: `npv(0.15, [-8e6] + [2.8e6] * 4)` gives about −6,000, roughly zero. The custom option's value disappears if benefits are 20% lower, so it's **fragile**. The subscription's NPV stays positive under the same 20% cut (1.2 → 0.96 M a year gives NPV ≈ 1.24 M). 2. Keep: a one-page charter (goals, budget, owner's decisions), a backlog, a simple risk list, a weekly review, acceptance criteria, and a short handover note. Skip: a formal WBS dictionary, a stakeholder register, formal change control boards, a full EVM system (a simple burn chart plus costs is enough). 4. (a) Cut the lowest-value stories (e.g. advanced reports) to stay near 8 M. (b) Accept about 9.2 M if the core features justify it (re-check the NPV). (c) Switch to the subscription option for remaining features if available, accepting some sunk cost. The recommendation depends on the backlog's value ranking with the owner.

Back to [[PM 00 Dashboard]]
