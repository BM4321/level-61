---
title: "Wholesale Inventory Management System"
aliases:
  - CASE-02
  - Inventory system case
module: "Information System Project Management"
module_code: "ITT06105"
topic_id: "PM-CASE-02"
type: "case-study"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - project-management
  - case-study
---

# PM-CASE-02 Wholesale Inventory Management System

> [!info] About this case
> A **fictional** wholesale distributor with three warehouses (Dar es Salaam, Mwanza, Arusha) replaces spreadsheets with an inventory management system (stock levels, transfers, barcodes, reorder alerts). All the figures come from `pm_tools` and are asserted in `test_case02`. This case **contrasts** with CASE-01: here the project ends up *behind schedule but under budget*.

## 1. Situation
Stock-outs at one warehouse while another has surplus cost the company sales. The owner-director wants real-time stock visibility, barcode scanning and automated reorder alerts within about 5 months. The budget is TZS 56 M (work packages). There's a small internal IT team plus an external developer firm, and barcode hardware from a supplier.

## 2. Network (weeks)
| ID | Activity | d | Pred. |
|---|---|---|---|
| A | Requirements and process mapping (3 sites) | 2 | — |
| B | System design | 3 | A |
| C | Barcode and label integration | 4 | B |
| D | Procure scanners, printers, network upgrades | 6 | A |
| E | Core inventory software | 5 | B |
| F | Reorder alerts and reports | 3 | C, E |
| G | Install hardware at 3 sites | 2 | D |
| H | System and integration test | 2 | F, G |
| I | Pilot at Dar es Salaam | 2 | H |
| J | Data load and stock count at all sites | 2 | I |
| K | Rollout and training (Mwanza, Arusha) | 2 | J |

**Results:**
- Duration **21 weeks**; critical path **A-B-E-F-H-I-J-K**.
- Float: C 1 week; D and G 3 weeks (shared along D-G).
- Paths: A-B-E-F-H-I-J-K 21; A-B-C-F-H-I-J-K 20 (near-critical); A-D-G-H-I-J-K 18.

## 3. Uncertainty
- PERT along the critical path: **21.83 ± 1.42 weeks**; P(≤ 22 weeks) = **54.7%**.
- The Monte Carlo simulation (10,000 runs, seed 2026) gives P(≤ 22) ≈ **49.5%**, lower, because the near-critical path through C (and D's wide 4–12 week estimate) causes merge bias.
- **Lesson:** with a near-critical path only 1 week shorter, the single-path PERT is noticeably optimistic.

## 4. Status at the end of week 12
Cost baseline: 56 M; PV at week 12 = **45.5 M**.

| Act | Budget | % done | EV | AC |
|---|---|---|---|---|
| A | 2.0 M | 100% | 2.0 M | 2.1 M |
| B | 4.5 M | 100% | 4.5 M | 4.4 M |
| C | 8.0 M | 75% | 6.0 M | 6.0 M |
| D | 15.0 M | 100% | 15.0 M | 14.0 M |
| E | 10.0 M | 80% | 8.0 M | 8.5 M |
| G | 3.0 M | 50% | 1.5 M | 1.2 M |
| **Total** | | | **37.0 M** | **36.2 M** |

- SPI = 37.0/45.5 = **0.813** (behind).
- CPI = 37.0/36.2 = **1.022** (slightly under budget).
- EAC (typical) = **54.79 M**.

**Interpretation:** a typical **under-resourced** pattern. Work isn't being done fast enough, but what *is* done is efficient. Investigation shows the external firm assigned only 2 of the 3 agreed developers (a contract performance issue), and hardware installation at Mwanza waited for site access. E is critical and is 80% done when it should have finished at week 10.

## 5. Discussion questions
1. Confirm the critical path and float by hand. What happens if scanner delivery (D) slips 4 weeks? (Hint: D-G has 3 weeks of float.)
2. Why is PERT optimistic here? Which activity's estimate drives the merge bias?
3. Using the week-12 status, draft a status report with RAG ratings (PM-17 criteria). What decision do you request?
4. The contract with the developer firm is time-and-materials. How should the PM use the contract (PM-14) to restore the third developer? What would a fixed-price contract have changed?
5. Plan the stakeholder engagement for the warehouse supervisors, who fear being blamed for stock discrepancies revealed by the new system (PM-12).
6. Build the risk register (at least 6 risks) with EMV, including site connectivity in Mwanza and Arusha.

> [!success]- Model answer notes (1–4)
> 1. A slip of 4 weeks against 3 weeks of float delays H by 1 week, so the project takes 22 weeks and the critical path becomes A-D-G-H-I-J-K. 2. Path A-B-C-F… is only 1 week shorter (20 vs 21), and C's estimate (3–7) is skewed. Its uncertainty sometimes makes it the longest path. D's wide 4–12 range also makes A-D-G-H… occasionally critical. 3. Schedule **red** (SPI 0.81); cost **green** (CPI 1.02). Decision: enforce the contract's staffing commitment, or approve a short-term second firm; accept the forecast go-live slip of about 2 weeks, or descope the reports (F) to release 2. 4. Under T&M, fewer developers means lower cost but slower progress, which matches the data. Use the contract's resource commitment and the progress reviews to require the agreed staffing; escalate through contract administration. A fixed-price contract would have put the schedule risk on the seller (with delay damages), but at a higher price.

Back to [[PM 00 Dashboard]] · Cross-module version: [[X-CASE-02 SME Inventory Rollout]]
