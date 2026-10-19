---
title: "Cyber Security Dashboard"
module: "Cyber Security"
module_code: "ITT06102"
type: "dashboard"
syllabus_status: "provisional"
tags:
  - semester-6
  - cyber-security
  - dashboard
---

# Cyber Security: ITT06102 Dashboard

**Credits:** 12 · **LTP (as supplied):** 2,2,4 (meaning unverified, see [[Module Register]]) · **Curriculum status:** PROVISIONAL

> [!danger] Ethics and legal boundaries (read before any lab)
> All the practical work in this module is **defensive** and runs on **your own machine**, on in-memory or local test data, or in intentionally vulnerable training environments that you install and control. **Never** scan, probe, attack or test any system, network or account that you don't own or don't have explicit **written** permission to assess. Unauthorised access is illegal in most countries (in Tanzania, for example, the Cybercrimes Act, 2015; check the current law for your jurisdiction) and violates university regulations. Toy cryptography in this vault is for teaching only and **must never be used to protect real data**.

> [!todo] ▶ Next lesson
> The first lesson below with mastery < 3. New? Start with **[[CS-01 Security Foundations - CIA, Threats, Vulnerabilities and Risk]]**.

## What is this subject about?
Protecting information and systems against harm: understanding **what** must be protected (assets), **from whom** (threat actors), **how** they attack (vulnerabilities, exploits), and **which controls** (technical, administrative, physical) reduce the risk to an acceptable level. You'll learn to think like a defender who understands attackers, and to build security into software from the start.

## What should I know before starting?
Basic networking (IP addresses, ports, client/server), the file system and command line, and Python up to [[PY-14 Files, CSV and JSON]] for the labs. The discrete maths helps for cryptography: [[DM-07 Functions]] (bijections, hashing), [[DM-11 Counting Principles, Permutations and Combinations]] (key spaces) and [[DM-18 Introductory Discrete Probability]] (base rates, collisions).

## Learning order
| # | Lesson | Unit | Status | Lab |
|---|---|---|---|---|
| 1 | [[CS-01 Security Foundations - CIA, Threats, Vulnerabilities and Risk]] | U1 Foundations | core | |
| 2 | [[CS-02 Threat Modeling and Security Requirements]] | U1 | core | [[LAB-CS-07 Threat Modeling a Sample Web Application]] |
| 3 | [[CS-03 Authentication and Identity]] | U2 Identity and Access | core | |
| 4 | [[CS-04 Authorization and Access Control]] | U2 | core | |
| 5 | [[CS-05 Cryptography Foundations and Symmetric Encryption]] | U3 Cryptography | core | [[LAB-CS-03 Toy Ciphers and Why They Fail]] |
| 6 | [[CS-06 Hashes, MACs and Integrity]] | U3 | core | [[LAB-CS-02 Hashing and Integrity Verification]] |
| 7 | [[CS-07 Public-Key Cryptography, Signatures and Key Management]] | U3 | core | |
| 8 | [[CS-08 Password Storage and Authentication Security]] | U3 | core | [[LAB-CS-01 Password Strength and Secure Password Storage]] |
| 9 | [[CS-09 Network Security and Secure Communication]] | U4 Infrastructure | core | |
| 10 | [[CS-10 Operating System Security and Hardening]] | U4 | core | [[LAB-CS-04 File Permission Audit]] |
| 11 | [[CS-11 Web Application Security]] | U5 Application Security | core | [[LAB-CS-05 Security Headers and Configuration Analysis]] |
| 12 | [[CS-12 Secure Software Development and Database Security]] | U5 | core | [[LAB-CS-06 Input Validation and SQL Injection Prevention]] |
| 13 | [[CS-13 Social Engineering and Security Awareness]] | U6 Human and Threats | core | |
| 14 | [[CS-14 Malware and Defensive Detection]] | U6 | core | |
| 15 | [[CS-15 Logging, Monitoring, Incident Response and Recovery]] | U7 Operations | core | [[LAB-CS-08 Log Analysis and Incident Response]] |
| 16 | [[CS-16 Risk Analysis, Policy, Governance and Compliance]] | U7 | core | |
| 17 | [[CS-17 Digital Forensics Fundamentals]] | U7 | supplementary | |
| 18 | [[CS-18 Security Testing and Vulnerability Management]] | U8 Assurance | core | |
| 19 | [[CS-19 Cloud Security and Privacy]] | U8 | supplementary | |

Map: [[CS 01 Curriculum Map]] · Mind map: [[MM-CS Cyber Security Mind Map]] · Labs index: [[Labs and Projects Index]]

## What should I read, watch, calculate, code or build?
- **Read:** the lessons in order. The reference frameworks are free and authoritative: the OWASP Top 10 and Cheat Sheet Series, NIST publications (CSF 2.0, SP 800-63B, SP 800-61), and the CIS Controls (see [[Source Register]]). A widely used textbook, *not* confirmed as your prescribed text: W. Stallings & L. Brown, *Computer Security: Principles and Practice*, 4th ed., Pearson, 2018.
- **Calculate:** key spaces, brute-force times and risk scores (CS-05, CS-08, CS-16).
- **Code and do:** the eight labs. Each has objectives, setup, commands, expected output, interpretation, cleanup and questions with answers.

## Exercises I must complete
Levels 1–3 of each lesson. All eight labs, with written answers to the lab questions. One complete threat model (LAB-CS-07) of your own Final Year Project.

## How do I test my understanding?
Lesson self-tests, the lab questions, [[QB-CS Cyber Security Question Bank]], and [[MOCK-CS-01 Cyber Security Mock Examination]].

## Evidence of mastery (provisional outcomes, not official)
1. **CS-LO1** Explain the core security concepts (CIA, threat, vulnerability, risk, control) and apply them to scenarios.
2. **CS-LO2** Perform threat modelling and derive security requirements.
3. **CS-LO3** Select and justify identity, authentication and access-control mechanisms.
4. **CS-LO4** Explain and correctly apply cryptographic primitives (encryption, hashing, MACs, signatures, key management), and distinguish them.
5. **CS-LO5** Identify and mitigate common network, OS and web-application vulnerabilities.
6. **CS-LO6** Plan logging, monitoring, incident response, backup and recovery.
7. **CS-LO7** Analyse risk and relate controls to policy, governance and compliance.

| Evidence | Outcomes |
|---|---|
| The eight labs completed, with interpretations | LO3–LO6 |
| A threat model and security requirements for your FYP | LO2, LO7 |
| Mock exam ≥ 60% | All |

## What remains incomplete?
Vault gaps: [[BUILD-STATUS]]. Your progress: [[Progress Tracker]].
