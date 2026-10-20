---
title: "Cyber Security Mock Examination"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "MOCK-CS-01"
type: "exam"
syllabus_status: "supplementary"
status: "not-started"
tags:
  - semester-6
  - cyber-security
  - exam
---

# MOCK-CS-01 Cyber Security Mock Examination

> [!warning] A designed practice paper
> This is **not** a past paper; the format (3 hours, 100 marks, Section A compulsory, any three of four in Section B) is designed. Check the real format with your lecturer. The calculations (CVSS, ALE, search spaces, permissions, log analysis) are computed with `02 - Cyber Security/code/cs_examples.py` in `09 - Revision and Exam Preparation/code/tests/test_mock_cs.py`. All organisations, hosts and addresses are fictional; IP addresses are from the documentation ranges.

**Instructions (designed):** 3 hours. Answer **all** of Section A (40 marks) and **three** questions from Section B (20 marks each). Scenario answers must refer to the scenario.

**Covers:** [[CS 01 Curriculum Map]], CS-01 to CS-19.

---

## Section A (40 marks)

**A1 (8 marks).** For each incident, name the CIA property mainly affected, and one preventive and one detective control: (a) a lecturer's laptop with unencrypted marks is stolen; (b) a disgruntled user changes prices in the shop database; (c) the registration server is flooded with traffic on registration day; (d) a backup tape is found to be unreadable when needed.

**A2 (8 marks).** (a) Why are passwords hashed with a slow, salted function rather than encrypted? *(3)* (b) Compare the search space of an 8-character password drawn from 62 symbols with a 15-character passphrase of lowercase letters only, in bits. *(3)* (c) At $10^{10}$ guesses per second against a leaked *fast* hash, roughly how long does an exhaustive search of each take? What does a memory-hard KDF change? *(2)*

**A3 (8 marks).** (a) Write the symbolic form of the Unix modes `640`, `4750` and `777`. *(3)* (b) Which of these would you flag on a file holding a database password, and why? *(2)* (c) Explain least privilege, and give one example of it in a web application. *(3)*

**A4 (8 marks).** For each requirement, choose symmetric encryption, a hash, a MAC or a digital signature, and justify: (a) detect accidental corruption of a downloaded file whose checksum is published on a trusted page; (b) a server must verify that messages came from a partner sharing a secret key; (c) anyone must be able to verify that results were issued by the registrar; (d) a laptop's disk must be unreadable if stolen.

**A5 (8 marks).** Compute the CVSS 3.1 base score and severity of: (a) `AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N`; (b) `AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N`; (c) `AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H`. For each, describe in words what kind of weakness the vector suggests. *(The metric tables are assumed to be provided in the exam; check your real exam.)*

---

## Section B (answer three, 20 marks each)

**B1 Web application security.** A fictional college's results website: students log in and view `/results?student=ID`; lecturers upload marks through a form; error pages show full stack traces; the session cookie has no flags. (a) Identify four weaknesses and map each to an OWASP Top 10 (2021) category. *(8)* (b) For each, give a specific control, and state where in the architecture it belongs. *(8)* (c) Which would you fix first, and why? *(4)*

**B2 Risk.** The (fictional) registrar's results database: asset value TZS 80 M, exposure factor 0.3 for a tampering incident, and an estimated 0.5 incidents a year. (a) Compute SLE and ALE. *(4)* (b) A control set reduces ALE to TZS 3 M at TZS 4 M a year. Is it justified? Show the calculation for the ALE of TZS 12 M. *(4)* (c) Rate three other risks on a 5×5 matrix: likelihood 4 / impact 4; 2/3; 5/4. *(3)* (d) Explain two weaknesses of quantitative risk analysis, and how you'd present the numbers honestly. *(9)*

**B3 Incident response.** The (constructed) excerpt below is from a server's authentication log.
```text
2026-03-02T09:10:01Z host=app01 sshd[2101]: Failed password for root from 203.0.113.77 port 51001
2026-03-02T09:10:03Z host=app01 sshd[2101]: Failed password for root from 203.0.113.77 port 51003
2026-03-02T09:10:05Z host=app01 sshd[2102]: Failed password for invalid user admin from 203.0.113.77 port 51007
2026-03-02T09:10:07Z host=app01 sshd[2102]: Failed password for deploy from 203.0.113.77 port 51011
2026-03-02T09:10:09Z host=app01 sshd[2103]: Failed password for deploy from 203.0.113.77 port 51015
2026-03-02T09:10:12Z host=app01 sshd[2103]: Accepted password for deploy from 203.0.113.77 port 51019
2026-03-02T09:11:40Z host=app01 sshd[2110]: Accepted publickey for amina from 198.51.100.20 port 40220
2026-03-02T09:12:02Z host=app01 sshd[2111]: Failed password for amina from 198.51.100.20 port 40231
```
(a) What happened? Identify the suspicious source, the number of failures before the success, and the account affected. *(6)* (b) Using the NIST incident response phases, list your first five actions, in order. *(8)* (c) Name three configuration changes that would have prevented or limited this. *(6)*

**B4 Privacy and forensics.** (a) A dataset of hostel survey responses has quasi-identifiers (block, year). Five rows: (A, 2), (A, 2), (A, 3), (B, 2), (B, 2). What is its k-anonymity, and which row is at risk? *(5)* (b) Propose two ways to raise k without losing the study's purpose. *(5)* (c) Explain the chain of custody, and why a forensic image is hashed when it's acquired. *(10)*

---

## Marking guide

> [!success]- A1–A4
> **A1** (a) Confidentiality; prevent: full-disk encryption; detect: asset tracking / remote-wipe alerts. (b) Integrity; prevent: least privilege and maker–checker on price changes; detect: an audit log with alerts on bulk changes. (c) Availability; prevent: capacity and rate limiting, an upstream DDoS service; detect: traffic monitoring with thresholds. (d) Availability (and integrity of the backup); prevent: verified backups and the 3-2-1 approach; detect: regular restore tests. *(2 each.)*
>
> **A2** (a) A hash is one-way, so a breach doesn't reveal passwords directly, and nothing needs to decrypt them; a slow, salted KDF makes each guess expensive and stops precomputed tables and identical-password matching. (b) $\log_2 62^8 \approx$ **47.6 bits**; $\log_2 26^{15} \approx$ **70.5 bits**: the longer passphrase is far larger. (c) $62^8 \approx 2.18 \times 10^{14}$ → about **6 hours**; $26^{15} \approx 1.68 \times 10^{21}$ → about **5,300 years**. A memory-hard KDF (scrypt, Argon2id) cuts the guess rate by many orders of magnitude, and makes GPU parallelism expensive. *(3 + 3 + 2.)*
>
> **A3** (a) `rw-r-----`, `rwsr-x---`, `rwxrwxrwx`. (b) `777` (world-writable and readable: anyone can read or replace the secret); `640` may be acceptable if the group is restricted to the service; `4750` is setuid, which is inappropriate for a data file. (c) Each user, process and component gets only the access it needs; e.g. the web app's database account can SELECT/INSERT on its tables but can't DROP or read other schemas. *(3 + 2 + 3.)*
>
> **A4** (a) A hash (SHA-256), compared with the trusted published value: integrity against accidental corruption. (b) A MAC (HMAC): authenticity and integrity with a shared key. (c) A digital signature: anyone can verify with the registrar's public key, and only the private key holder could have signed. (d) Symmetric encryption (e.g. AES-based full-disk encryption): confidentiality at rest. *(2 each.)*

> [!success]- A5
> (a) **6.5 Medium**: network-reachable, needs a low-privilege account, discloses confidential data (e.g. one user reading others' records through a broken access check). (b) **6.1 Medium**: needs a user to interact, and the impact crosses into another component (scope changed), with limited confidentiality/integrity impact, typical of a reflected script injection in a web page. (c) **7.8 High**: local access with a low-privilege account and full impact, typical of local privilege escalation. *(Scores 1 each; severity and interpretation 1–2 each.)*

> [!success]- B1
> (a) Broken access control (A01): `student=ID` lets one student request another's results. Security misconfiguration (A05): stack traces in error pages. Identification and authentication failures (A07) / session handling: cookie without `Secure`, `HttpOnly`, `SameSite`. Insecure design or missing CSRF protection on the mark-upload form (relevant to A01/A04). (b) Server-side authorisation on every request (compare the requested ID with the session user, or check the lecturer's course), in the service layer; generic error pages, details only in server logs (configuration); cookie flags set by the framework configuration; CSRF tokens on state-changing forms (web layer). (c) A01 first: it exposes every student's results to any logged-in user, with trivial effort; then the session flags and CSRF (they protect lecturers' mark changes). *(8 + 8 + 4.)*

> [!success]- B2
> (a) SLE = 80 M × 0.3 = **24 M**; ALE = 24 M × 0.5 = **12 M/year**. (b) Net benefit = 12 − 3 − 4 = **5 M/year** > 0: justified on these estimates. (c) 4×4 = **16 High**; 2×3 = **6 Medium**; 5×4 = **20 Critical**. (d) ARO and EF are often guesses with false precision; results are sensitive to them; intangible impacts (reputation, student harm) are hard to value. Present ranges, state assumptions, show a break-even (here, the control pays off as long as it removes more than 4 M of ALE), and combine with qualitative judgement ([[X-05 Security Risk in Project Management]]). *(4 + 4 + 3 + 9.)*

> [!success]- B3
> (a) Source **203.0.113.77** made **5** failed attempts (root ×2, invalid user admin, deploy ×2) in about 8 seconds, then **successfully logged in as `deploy`** with a password at 09:10:12. That's a likely password-guessing compromise of `deploy`. The other source (198.51.100.20, `amina`) logged in with a key and then had one failure: not suspicious on this evidence. *(6.)*
> (b) Following NIST SP 800-61 (preparation; detection and analysis; containment, eradication and recovery; post-incident activity): 1. confirm and record (preserve the logs, hash them, note the times); 2. contain: disable the `deploy` account's password login and terminate its sessions, block 203.0.113.77 at the firewall; 3. scope: what did `deploy` do after 09:10:12 (commands, sudo, files changed, outbound connections)? 4. eradicate: rotate credentials and keys that `deploy` could reach; remove persistence if found; 5. recover and report: restore from known-good state if needed, monitor, notify according to policy; then lessons learned. *(8.)*
> (c) Disable SSH password authentication (keys only); no direct root login; rate limiting or fail2ban-style blocking; MFA for remote access; restrict SSH to a VPN or allow-listed addresses. *(Any three, 2 each.)*

> [!success]- B4
> (a) Groups by (block, year): (A, 2) ×2, (A, 3) ×1, (B, 2) ×2 → **k = 1**; the (A, 3) row is unique and can be singled out. (b) Generalise (e.g. year groups "2–3"), or suppress or merge small groups (report "other" for groups below a threshold), or remove a quasi-identifier the analysis doesn't need. (c) The chain of custody documents who held the evidence, when, where and what was done to it, from seizure to court, so that its integrity can be shown. Hashing the image at acquisition (e.g. SHA-256) lets anyone later verify that the analysed copy is bit-for-bit identical to what was acquired; analysis is done on a verified copy, never the original. *(5 + 5 + 10.)*

**Self-assessment (designed):** ≥ 70 strong; 50–69 secure; < 50 on any question → that topic goes to [[Weak Area Tracker]].

Back to [[Exam Technique and Assessment Strategy]] · [[QB-CS Cyber Security Question Bank]] · [[CS 00 Dashboard]]
