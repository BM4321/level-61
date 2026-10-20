---
title: "Cyber Security Question Bank"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "QB-CS"
type: "question-bank"
tags:
  - semester-6
  - cyber-security
  - exam
---

# QB-CS Cyber Security Question Bank

> [!info] How to use
> Two questions per lesson, defensive in focus. Answer closed book, then open the folded answer. Computed answers (HOTP values, CVSS, edit distance, permissions, ALE) are checked in `09 - Revision and Exam Preparation/code/tests/test_qb.py` (`test_qb_cs_numbers`). Log misses in [[Mistake Log]].

## [[CS-01 Security Foundations - CIA, Threats, Vulnerabilities and Risk]]

**Q1 (L1).** Define threat, vulnerability and risk, with one hostel-system example of each.

> [!success]- Answer
> Threat: a potential cause of harm (an outsider guessing passwords). Vulnerability: a weakness it can exploit (no login throttling). Risk: the likelihood and impact of the threat exploiting the vulnerability (account takeover of a warden, moderately likely, high impact).

**Q2 (L2).** An admin page has no login, but "nobody knows the URL". What principle does this violate?

> [!success]- Answer
> It relies on security through obscurity; URLs leak (logs, history, referrers, guessing). Every privileged function needs authentication and authorisation.

## [[CS-02 Threat Modeling and Security Requirements]]

**Q3 (L1).** Expand STRIDE and give the property each threatens.

> [!success]- Answer
> Spoofing (authentication), Tampering (integrity), Repudiation (non-repudiation), Information disclosure (confidentiality), Denial of service (availability), Elevation of privilege (authorisation).

**Q4 (L3).** Write a testable security requirement for repudiation in a marks system.

> [!success]- Answer
> "Every change to a mark shall record the user, time, old value, new value and reason in an append-only audit log, written in the same transaction as the change."

## [[CS-03 Authentication and Identity]]

**Q5 (L2).** Name the three authentication factor types, and explain why a password plus a security question isn't MFA.

> [!success]- Answer
> Something you know, have, are. A password and a security question are both "know": one factor type twice.

**Q6 (L3).** RFC 4226 test key `12345678901234567890` (ASCII): what are the HOTP values for counters 0 and 1?

> [!success]- Answer
> 755224 and 287082 (6 digits, HMAC-SHA1), as computed by `hotp` in `cs_examples.py`.

## [[CS-04 Authorization and Access Control]]

**Q7 (L2).** Compare RBAC and ABAC with an example.

> [!success]- Answer
> RBAC grants permissions to roles (wardens can assign requests). ABAC decides from attributes of the user, resource and context (a technician can update a request if `request.assignee == user.id` and it's during working hours).

**Q8 (L2).** What is an IDOR, and how is it prevented?

> [!success]- Answer
> Insecure direct object reference: the app trusts an ID in the request (`/results?student=123`) without checking that the user may access that object. Prevent it with a server-side authorisation check on every access.

## [[CS-05 Cryptography Foundations and Symmetric Encryption]]

**Q9 (L2).** Why is ECB mode unsafe for most data?

> [!success]- Answer
> Identical plaintext blocks produce identical ciphertext blocks, so patterns leak. Use an authenticated mode such as AES-GCM.

**Q10 (L1).** What does Kerckhoffs's principle say?

> [!success]- Answer
> A system should stay secure even if everything except the key is public.

## [[CS-06 Hashes, MACs and Integrity]]

**Q11 (L2).** Distinguish a hash from a MAC.

> [!success]- Answer
> A hash has no key: anyone can compute it, so it detects accidental changes only if the hash itself is trusted. A MAC uses a secret key, so only key holders can produce a valid tag: it gives integrity and authenticity.

**Q12 (L3).** Why should two MACs be compared with `hmac.compare_digest`?

> [!success]- Answer
> It takes time independent of where the inputs differ, avoiding a timing side channel that could reveal a valid tag byte by byte.

## [[CS-07 Public-Key Cryptography, Signatures and Key Management]]

**Q13 (L2).** Alice signs a document. Which key does she use, and which key does Bob use to verify?

> [!success]- Answer
> Alice's private key to sign; Alice's public key (from a trusted certificate) to verify.

**Q14 (L3).** Why does TLS use both public-key and symmetric cryptography?

> [!success]- Answer
> Public-key methods authenticate the server and agree a shared secret; fast symmetric encryption then protects the bulk data.

## [[CS-08 Password Storage and Authentication Security]]

**Q15 (L2).** Why a unique salt per password?

> [!success]- Answer
> Identical passwords get different hashes, and precomputed tables become useless; attackers must attack each hash separately.

**Q16 (L3).** Current guidance favours length and blocklists over composition rules and forced rotation. Why?

> [!success]- Answer
> Composition rules produce predictable patterns (`Password1!`) and rotation causes small, guessable changes; length and blocking known-breached passwords improve real strength. Change passwords after a suspected compromise.

## [[CS-09 Network Security and Secure Communication]]

**Q17 (L2).** What's the purpose of network segmentation? Give an example.

> [!success]- Answer
> It limits what an attacker can reach after compromising one device: e.g. warehouse scanners on their own segment, with access only to the inventory server.

**Q18 (L2).** Stateful firewall vs packet filter?

> [!success]- Answer
> A packet filter checks each packet against rules alone; a stateful firewall tracks connections, allowing return traffic for established sessions only.

## [[CS-10 Operating System Security and Hardening]]

**Q19 (L1).** Give the symbolic form of mode 640 and say who can read the file.

> [!success]- Answer
> `rw-r-----`: the owner reads and writes, the group reads, others have no access.

**Q20 (L2).** List four hardening steps for a new Linux server.

> [!success]- Answer
> Patch and enable automatic security updates; remove unused services; key-only SSH with no root login; host firewall allowing only needed ports; least-privilege accounts and sudo; logging to a central server.

## [[CS-11 Web Application Security]]

**Q21 (L2).** What do the cookie flags `Secure`, `HttpOnly` and `SameSite` each protect against?

> [!success]- Answer
> `Secure`: sending the cookie over plain HTTP. `HttpOnly`: scripts reading it (limits session theft through injected scripts). `SameSite`: sending it on cross-site requests (helps against CSRF).

**Q22 (L3).** Why is output encoding needed even when input is validated?

> [!success]- Answer
> Valid data can still contain characters that are special in HTML, JavaScript or URLs; context-aware encoding at output prevents them being interpreted as code.

## [[CS-12 Secure Software Development and Database Security]]

**Q23 (L2).** How do parameterised queries prevent SQL injection?

> [!success]- Answer
> The SQL text and the data are sent separately; the database never parses data as SQL, so input can't change the query's structure.

**Q24 (L2).** Name three practices in a secure development lifecycle.

> [!success]- Answer
> Threat modelling in design; code review with a security checklist; static analysis and dependency scanning in CI; security tests; least-privilege database accounts.

## [[CS-13 Social Engineering and Security Awareness]]

**Q25 (L1).** List four warning signs in a phishing email.

> [!success]- Answer
> Urgency or threats; a sender or link domain that doesn't match the organisation; requests for credentials or payment; unexpected attachments; generic greetings.

**Q26 (L2).** `univercity.example` vs `university.example`: what's the edit distance, and why does it matter?

> [!success]- Answer
> 1 (one substitution). Lookalike domains with a small edit distance are a common phishing trick; filters can flag them.

## [[CS-14 Malware and Defensive Detection]]

**Q27 (L2).** Signature-based vs behaviour-based detection?

> [!success]- Answer
> Signatures match known malware (hashes, patterns): precise but blind to new variants. Behaviour-based detection flags suspicious actions (mass file encryption, unusual process trees): catches new threats, with more false positives.

**Q28 (L3).** Why can high Shannon entropy in a file be a signal, and why isn't it proof?

> [!success]- Answer
> Encrypted or packed content approaches 8 bits per byte, which malware often uses; but compressed archives and media files are also high-entropy, so it's one indicator among several.

## [[CS-15 Logging, Monitoring, Incident Response and Recovery]]

**Q29 (L1).** List the NIST incident response phases.

> [!success]- Answer
> Preparation; detection and analysis; containment, eradication and recovery; post-incident activity (lessons learned).

**Q30 (L2).** What does the 3-2-1 backup approach mean, and why test restores?

> [!success]- Answer
> 3 copies, on 2 different media, 1 off-site (or offline). Untested backups often fail when needed: only a restore test proves they work.

## [[CS-16 Risk Analysis, Policy, Governance and Compliance]]

**Q31 (L2).** AV = 50 M, EF = 0.2, ARO = 2. Compute SLE and ALE.

> [!success]- Answer
> SLE = 10 M; ALE = 20 M per year.

**Q32 (L2).** Distinguish a policy, a standard and a procedure.

> [!success]- Answer
> Policy: management's high-level intent ("data shall be classified"). Standard: mandatory specifics (AES-256 for confidential data). Procedure: step-by-step instructions to comply.

## [[CS-17 Digital Forensics Fundamentals]]

**Q33 (L2).** Why work on a forensic copy rather than the original, and how do you show it's identical?

> [!success]- Answer
> Analysis can alter evidence; the original must be preserved. Hash the original at acquisition and the copy; matching hashes show they're identical.

**Q34 (L1).** What does the order of volatility say?

> [!success]- Answer
> Collect the most volatile evidence first (CPU state, memory, network connections), then disks, then backups and archives.

## [[CS-18 Security Testing and Vulnerability Management]]

**Q35 (L1).** What must be in place before any security test of a system?

> [!success]- Answer
> Written authorisation from the system owner, an agreed scope and rules of engagement, and a contact for emergencies. Test only systems you own or are permitted to assess, or intentionally vulnerable training environments.

**Q36 (L2).** A scan reports a CVSS 9.8 vulnerability on an internal test server, and a 6.5 one on the internet-facing results portal. Which do you fix first?

> [!success]- Answer
> Prioritise by risk, not by score alone: exposure, asset value and exploitability matter. The portal is internet-facing and holds sensitive data, so its 6.5 may well come first; the 9.8 still needs prompt remediation, and compensating controls (isolate it) meanwhile. CVSS `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` = 9.8.

## [[CS-19 Cloud Security and Privacy]]

**Q37 (L2).** In the shared responsibility model for IaaS, who patches the guest operating system?

> [!success]- Answer
> The customer. The provider secures the physical infrastructure and hypervisor; in SaaS the provider takes on much more.

**Q38 (L3).** Is HMAC-pseudonymised data anonymous? Explain.

> [!success]- Answer
> No: whoever holds the key can re-identify people, so it's still personal data and must be protected; pseudonymisation reduces risk but doesn't remove obligations.

Back to [[Question Bank Index]] · [[MOCK-CS-01 Cyber Security Mock Examination]] · [[CS 00 Dashboard]]
