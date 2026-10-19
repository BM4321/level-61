---
title: "Cyber Security Curriculum Map"
module: "Cyber Security"
module_code: "ITT06102"
type: "curriculum-map"
syllabus_status: "provisional"
tags:
  - semester-6
  - cyber-security
  - curriculum
---

# Cyber Security: Curriculum Map

Back to [[CS 00 Dashboard]]

## 1. Units
| Unit | Topics | Practical |
|---|---|---|
| U1 Foundations | CS-01 CIA, threats, risk · CS-02 threat modelling | LAB-CS-07 |
| U2 Identity and access | CS-03 authentication · CS-04 authorisation | (part of LAB-CS-01) |
| U3 Cryptography | CS-05 symmetric · CS-06 hashes and MACs · CS-07 public key and PKI · CS-08 passwords | LAB-CS-01, 02, 03 |
| U4 Infrastructure | CS-09 network · CS-10 OS hardening | LAB-CS-04 |
| U5 Application security | CS-11 web · CS-12 secure SDLC and databases | LAB-CS-05, 06 |
| U6 Human and threat landscape | CS-13 social engineering · CS-14 malware | |
| U7 Operations | CS-15 logging and IR · CS-16 risk and governance · CS-17 forensics | LAB-CS-08 |
| U8 Assurance | CS-18 security testing · CS-19 cloud and privacy | |

## 2. Prerequisite graph
```mermaid
flowchart TD
    C1[CS-01 Foundations] --> C2[CS-02 Threat modelling]
    C1 --> C3[CS-03 Authentication]
    C3 --> C4[CS-04 Access control]
    C1 --> C5[CS-05 Symmetric crypto]
    C5 --> C6[CS-06 Hashes & MACs]
    C5 --> C7[CS-07 Public key & PKI]
    C6 --> C7
    C3 --> C8[CS-08 Password storage]
    C6 --> C8
    C7 --> C9[CS-09 Network security]
    C4 --> C10[CS-10 OS hardening]
    C3 --> C11[CS-11 Web app security]
    C4 --> C11
    C9 --> C11
    C11 --> C12[CS-12 Secure SDLC & DB]
    C1 --> C13[CS-13 Social engineering]
    C10 --> C14[CS-14 Malware]
    C14 --> C15[CS-15 Logging & IR]
    C2 --> C16[CS-16 Risk & governance]
    C15 --> C17[CS-17 Forensics]
    C11 --> C18[CS-18 Security testing]
    C16 --> C18
    C9 --> C19[CS-19 Cloud & privacy]
    C16 --> C19
```
*Text version: foundations (01) feed threat modelling, authentication, crypto and social engineering. Crypto flows from symmetric ciphers (05) to hashes (06) to public key (07), and passwords (08) need hashes plus authentication. Network security (09) needs public-key crypto (TLS). Web security (11) builds on authentication, access control and networks, and leads to the secure SDLC (12) and testing (18). Operations: malware (14), then logging/IR (15), then forensics (17). Risk (16) underpins testing and cloud (19).*

## 3. Review alerts
| Before… | Review | Why |
|---|---|---|
| CS-05 | [[DM-07 Functions]] | Encryption must be a bijection for each key |
| CS-06 | [[DM-12 Pigeonhole Principle and Inclusion-Exclusion]], [[DM-18 Introductory Discrete Probability]] | Collisions exist, and birthday bounds |
| CS-07 | [[DM-05 Direct Proof, Contrapositive and Contradiction]], [[DM-10 Relations, Equivalence Relations and Partial Orders]] | Primes and modular arithmetic |
| CS-08 | [[DM-11 Counting Principles, Permutations and Combinations]] | Password keyspaces |
| CS-11/12 | [[PY-22 SQL and Database Integration]], [[PY-24 Secure Programming and Input Validation]] | Injection prevention in code |
| CS-15 | [[DM-18 Introductory Discrete Probability]] | Base rates and alert fatigue |
| CS-16 | [[PM-11 Risk Management]] | The same risk vocabulary, in the project context |

## 4. Cross-module links
[[X-03 Security Requirements in Software Architecture]] · [[X-05 Security Risk in Project Management]] · [[SD-17 Secure and Reliable Software Design]] · [[X-CASE-01 Secure Exam Results Portal]]
