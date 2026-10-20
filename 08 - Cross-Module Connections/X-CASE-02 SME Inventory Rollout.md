---
title: "SME Inventory Rollout"
aliases:
  - X-CASE-02
  - Inventory rollout case
module: "Cross-Module"
module_code: "multiple"
modules:
  - "ITT06105"
  - "CST06101"
  - "CST06102"
  - "ITT06102"
  - "GST06106"
topic_id: "X-CASE-02"
type: "case-study"
syllabus_status: "supplementary"
status: "not-started"
mastery: 0
tags:
  - semester-6
  - cross-module
  - case-study
---

# X-CASE-02 SME Inventory Rollout

> [!info] About this case
> The cross-module version of [[PM-CASE-02 Wholesale Inventory Management System]]: the same **fictional** three-warehouse distributor, seen through every module. PM-CASE-02 covers the schedule and earned value; this case adds the inventory rules (DM, PY), the design (SD) and the security of a multi-site system (CS). Numbers are asserted in `test_xcase02_inventory` (`08 - Cross-Module Connections/code/`), which also re-checks PM-CASE-02's CPM and EVM figures.

## 1. Recap of the project (PM)
- Network: **21 weeks**, critical path **A-B-E-F-H-I-J-K**; the barcode integration (C) has 1 week of float, and procurement and installation (D, G) 3 weeks.
- End of week 12: PV 45.5 M, EV 37.0 M, AC 36.2 M → SV **−8.5 M**, CV **+0.8 M**; SPI **0.813**, CPI **1.022**; EAC (typical) **54.79 M** against a 56 M budget.
- Diagnosis: behind schedule, under budget: the developer firm supplied 2 of the 3 contracted developers.

## 2. The business rules (DM, PY)

### 2.1 Reorder point and order size
For a fast-moving SKU (50 kg cement bags; fictional figures): mean demand 40 bags/day, standard deviation 12, supplier lead time 9 days, 95% service level ($z = 1.645$):
- safety stock $= z\,\sigma_d\sqrt{L} = 1.645 \times 12 \times 3 =$ **59.22** bags;
- reorder point $= \bar d L + SS = 360 + 59.22 = 419.22$, rounded up to **420** bags;
- EOQ with 14,400 bags a year (360 trading days), TZS 50,000 per order and TZS 600 per bag per year holding cost: $\sqrt{2DS/H} = \sqrt{2{,}400{,}000} \approx$ **1,549** bags.

(The formula assumes roughly normal, independent daily demand; check that against the sales history before relying on it.)

### 2.2 The alert rule as logic
"Raise a reorder alert for a warehouse and SKU when stock is at or below the reorder point, unless an order is already open, and only for active SKUs": $alert = active \land (stock \le ROP) \land \lnot open$.

`reorder_alerts` implements it. With the example stock levels:

| Warehouse, SKU | Stock | ROP | Open order? | Active? | Alert |
|---|---|---|---|---|---|
| DAR, CEM50 | 380 | 420 | no | yes | **yes** |
| MWZ, CEM50 | 900 | 420 | no | yes | no |
| ARU, CEM50 | 420 | 420 | no | yes | **yes** (boundary: "at or below") |
| DAR, NAIL3 | 40 | 60 | no | yes | **yes** |
| ARU, NAIL3 | 15 | 60 | yes | yes | no (already ordered) |
| MWZ, OLDPAINT | 2 | 10 | no | no | no (discontinued) |

The ARU cement row is the boundary case that a `<` instead of `≤` would miss: a test for exactly this row belongs in the suite ([[SD-14 Software Testing, Verification and Validation]]).

**Sets:** warehouses below the reorder point for cement are {DAR, ARU}; for nails, also {DAR, ARU}. Their intersection says where *both* need attention, which is a hint to check for a common cause (e.g. a delayed delivery route), not just to reorder.

### 2.3 Transfers before purchases
Mwanza holds 900 bags, 480 above its reorder point. Before buying, the system could suggest a transfer to a warehouse below its reorder point, if the transfer cost and time are lower than the supplier's. That's a shortest-path and cost comparison over the transport network ([[X-02 Graph Theory in Algorithms, Networks and Scheduling]]), with the real distances and costs supplied by the business.

## 3. Design (SD)
- **Domain model:** Product (SKU, active), Warehouse, StockLevel (warehouse, SKU, quantity), Movement (receipt, issue, transfer, adjustment, each with a user and reason), PurchaseOrder, ReorderPolicy (ROP, EOQ per SKU).
- **Stock is derived from movements**, not edited directly: an audit trail by construction, and adjustments need a reason ([[SD-09 Data Modeling and Interface Design]]).
- **Events:** `StockMoved` → a handler re-evaluates the alert rule → `ReorderAlertRaised` → notify the buyer (Observer, [[SD-12 Behavioral Design Patterns]]).
- **Offline scanners:** scanners queue movements when Wi-Fi drops, and sync later. Each queued movement has a unique ID, so a resend is idempotent (no double counting).

## 4. Security (CS)
| Concern | Control |
|---|---|
| Scanners on the warehouse network | WPA2/WPA3-Enterprise, a separate network segment for scanners, no direct internet access ([[CS-09 Network Security and Secure Communication]]) |
| Tampered or replayed sync data | TLS to the server; per-device credentials; idempotent movement IDs; server-side validation of quantities |
| Staff adjusting stock to hide losses | Adjustments need a reason and a second approver above a threshold; reports of adjustments per user |
| Least privilege across sites | Roles scoped by warehouse (a Mwanza supervisor can't adjust Arusha stock) ([[CS-04 Authorization and Access Control]]) |
| Ransomware or server loss | Offline, tested backups (e.g. the 3-2-1 approach) and a recovery plan ([[CS-15 Logging, Monitoring, Incident Response and Recovery]]) |

## 5. People and change (PM)
Warehouse supervisors fear blame when the new system reveals discrepancies ([[PM-CASE-02 Wholesale Inventory Management System]] question 5). The design helps: the opening stock count (activity J) sets a **baseline** with no blame for earlier differences, and the movement history makes later discrepancies traceable to process, not to guesswork.

## 6. Discussion questions
1. Recompute the safety stock for a 99% service level ($z \approx 2.326$). What happens to the reorder point?
2. Write a failing test that a `<` comparison in `reorder_alerts` would fail.
3. The developer firm proposes to catch up by starting the reorder alerts and reports (F) before the core software (E) is finished, with the developers it already has. Evaluate this using the network.
4. A supervisor wants to edit stock levels directly "to fix mistakes quickly". Respond as the designer and as the security lead.
5. Which two STRIDE threats are most likely for offline scanners, and what does idempotency protect against?
6. Should the transfer suggestion (§2.3) be in the first release? Use scope management and the schedule position to argue.

> [!success]- Model answer notes
> 1. $SS = 2.326 \times 12 \times 3 \approx 83.7$; ROP $\approx 443.7$, rounded up to 444. Higher service costs more safety stock. 2. A test with stock exactly 420 and ROP 420 expecting an alert: `assert ("ARU", "CEM50") in reorder_alerts(...)`. 3. That's fast-tracking: F depends on C and E, and E is critical, so overlapping them can recover part of the slip, but it risks rework if E's interfaces change. Agree an interface freeze for E first. It doesn't fix the root cause, the missing third developer, which is a contract issue ([[PM-14 Procurement and Change Management]]). 4. Designer: direct edits destroy the movement history; use an adjustment movement with a reason, which is as quick but auditable. Security lead: direct edits are the tampering path that hides theft; adjustments above a threshold need a second approver. 5. Tampering (altered quantities in the queue) and repudiation (who scanned?); spoofing of a device is also possible. Idempotency protects against double counting when a movement is resent after a dropped connection (it's an integrity property, not a security control by itself). 6. Probably not: the project is already behind (SPI 0.813), and the feature isn't in the agreed scope. Record it as a change request for release 2, with its own estimate.

Back to [[X 00 Cross-Module Index]] · PM version: [[PM-CASE-02 Wholesale Inventory Management System]]
