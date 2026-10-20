---
title: "Cyber Security Glossary"
module: "Cyber Security"
module_code: "ITT06102"
type: "glossary"
tags:
  - semester-6
  - cyber-security
  - glossary
---

# GL-CS Cyber Security Glossary

Every term below is taken from the Terminology section (§6) of the lesson it links to, so the definitions match the lessons. Generated at the last build; 129 terms.

| Term | Meaning | Lesson |
|---|---|---|
| AAA | Authentication, Authorisation, Accounting | [[CS-03 Authentication and Identity\|CS-03]] |
| ACL / capability | Per-object list / per-subject token or list | [[CS-04 Authorization and Access Control\|CS-04]] |
| AEAD | Authenticated Encryption with Associated Data | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| Anti-forensics | Attempts to hide or destroy evidence (wiping, timestomping, log deletion) | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| ASVS | OWASP's catalogue of verifiable application-security requirements | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Attack surface | Everything an attacker can interact with: services, ports, accounts, files | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Attack tree | Goal-decomposition tree of attacks | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Attribution | Linking actions to a specific person or group (hard; needs corroboration) | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| Avalanche effect | Small input changes cause large, unpredictable output changes | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| Baseline | A documented secure configuration standard | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| BEC | Business email compromise: fraud using real or spoofed business email | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| Birthday bound | Collisions are expected after about $2^{n/2}$ attempts | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| Blameless review | A post-incident review focused on system and process causes, not individual blame | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| Block / stream cipher | Encrypts fixed blocks / XORs a keystream | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| C2 | Command-and-control channel between malware and its operator | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| Certificate / CA / PKI | Signed identity-key binding / its issuer / the whole trust infrastructure | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| Chain of custody | A documented history of an evidence item's handling | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| Collision | Two different inputs with the same digest | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| Configuration drift | Systems slowly diverging from their baseline | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Containment | Limiting the spread and impact of an incident | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| Control plane | The management API and console used to create and configure resources | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Control types | Preventive, detective, corrective; administrative, technical, physical | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| Credential stuffing | Trying username/password pairs leaked from other sites | [[CS-03 Authentication and Identity\|CS-03]], [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Cryptanalysis | The study of breaking ciphers | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| CSP | Content-Security-Policy header restricting resource sources | [[CS-11 Web Application Security\|CS-11]] |
| CSRF | A forged state-changing request riding on the victim's cookies | [[CS-11 Web Application Security\|CS-11]] |
| Data minimisation | Collect and keep only the necessary personal data | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| DFD | Data-flow diagram | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Digest | The output of a hash | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| Digital signature | Value proving origin and integrity, verifiable with the public key | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| DMZ | A network zone for Internet-facing services, isolated from internal zones | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Double extortion | Encrypting data *and* threatening to leak stolen copies | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| DPIA | A data-protection impact assessment of high-risk processing | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Due care / due diligence | Doing what a reasonable organisation would do / investigating to know what is needed | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| EDR | Endpoint detection and response: behavioural telemetry with response actions | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| Egress filtering | Restricting *outbound* traffic (limits exfiltration and malware callbacks) | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Event / alert / incident | Something observed / a notification that might matter / a confirmed violation or imminent threat | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| FIDO2 / WebAuthn / passkey | Standards for public-key, origin-bound authentication | [[CS-03 Authentication and Identity\|CS-03]] |
| Forensic image | A bit-for-bit copy of storage, including unallocated space | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| Forward secrecy | Past sessions stay safe after a long-term key is compromised | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]], [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Homograph attack | A domain with lookalike Unicode characters (shown as punycode `xn--…`) | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| Horizontal escalation / IDOR | Accessing a peer's objects (Amina → Baraka's record) through Insecure Direct Object References | [[CS-04 Authorization and Access Control\|CS-04]] |
| HSM / KMS | Hardware security module / key management service | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| Hybrid encryption | Public-key for the key exchange, symmetric for the data | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| IAM | Identity and access management | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| IDOR | Insecure direct object reference: accessing objects by ID without an ownership check | [[CS-11 Web Application Security\|CS-11]] |
| IdP / SP | Identity provider / service (relying) provider | [[CS-03 Authentication and Identity\|CS-03]] |
| Infrastructure as code (IaC) | Defining infrastructure in version-controlled files | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Inherent / residual risk | Risk before / after controls | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| IOC | Indicator of compromise: a file hash, domain, IP or registry key associated with an attack | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| IV / nonce | Initialisation vector / number used once (must be unique, and for CBC unpredictable) | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| k-anonymity | Every quasi-identifier combination appears in at least k records | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| KDF | Key derivation function; a password-hashing KDF is deliberately slow | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Key agreement / exchange | Establishing a shared secret over an open channel | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| Key / key space | The secret parameter / the set of possible keys | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| KMS | Key management service | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Known-good / known-bad hash sets | Hashes used to exclude standard files or to find malicious ones | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| Lateral movement | An attacker moving from a first compromised host to others | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Least privilege (database) | The app account has only the permissions it needs | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| Least privilege / need-to-know | Minimum rights / access only to the data needed for the task | [[CS-04 Authorization and Access Control\|CS-04]] |
| Length extension | Extending $H(k\|m)$ to $H(k\|m\|\ldots)$ without the key | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| Living off the land | Abusing built-in OS tools to avoid dropping new files | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| MAC / HMAC | Keyed integrity tag / the hash-based MAC construction | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| MAC (OS sense) | Mandatory access control policy (SELinux, AppArmor) | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Malleability | Being able to change the ciphertext so the plaintext changes meaningfully | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| Memory-hard | Needs large RAM per evaluation, which limits parallel hardware | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Merkle tree | A tree of hashes allowing efficient integrity proofs for large data sets | [[CS-06 Hashes, MACs and Integrity\|CS-06]] |
| MFA | Multi-factor authentication (≥ 2 different factor types) | [[CS-03 Authentication and Identity\|CS-03]] |
| Misuse case | Use case describing hostile behaviour | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Mitigation | A control reducing a threat's risk | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| MITM | An attacker relaying and altering communications between two parties | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]], [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Mode of operation | How a block cipher handles messages longer than one block | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| MTTD / MTTR | Mean time to detect / to respond or recover | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| OAuth vs OIDC | Delegated authorisation vs authentication on top of it | [[CS-03 Authentication and Identity\|CS-03]] |
| Open redirect | The site forwards users to an attacker-supplied URL (used in phishing) | [[CS-11 Web Application Security\|CS-11]] |
| Order of volatility | Collection priority from most to least volatile data | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| OTP / HOTP / TOTP | One-time password / HMAC-based / time-based | [[CS-03 Authentication and Identity\|CS-03]] |
| Out-of-band verification | Confirming a request through a different, trusted channel | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| Packing / obfuscation | Compressing or encrypting code to evade signatures | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| Parameterised query / prepared statement | SQL with placeholders; values are bound separately | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| Password spraying | Trying a few common passwords against many accounts, staying under lockout limits | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Patch management | The process of identifying, testing, deploying and verifying updates | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| PEP / PDP | Policy enforcement point / policy decision point | [[CS-04 Authorization and Access Control\|CS-04]] |
| Pepper | A secret value stored outside the database | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Persistence | Mechanisms that survive reboot or logoff | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| Phishing-resistant MFA | MFA bound to the legitimate origin (FIDO2/WebAuthn), so it can't be relayed through a fake site | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| Plaintext / ciphertext | Readable data / encrypted data | [[CS-05 Cryptography Foundations and Symmetric Encryption\|CS-05]] |
| Pretext | A fabricated scenario used to justify a request | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| Privilege escalation | Gaining higher rights than granted (vertical) or another user's rights (horizontal) | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Public / private key | Shareable / secret halves of a key pair | [[CS-07 Public-Key Cryptography, Signatures and Key Management\|CS-07]] |
| Quasi-identifier | An attribute that isn't identifying alone but can be in combination | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Rainbow table | Precomputed chains mapping hashes back to passwords (defeated by salts) | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Risk appetite | The amount and type of risk an organisation is willing to pursue or retain | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| Risk register | A list of risks with owner, rating, treatment and status | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| RTO / RPO | Maximum tolerable downtime / data loss | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| Salt | Random, non-secret, per-password value mixed in before hashing | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Same-origin policy | Browser rule isolating content by scheme + host + port | [[CS-11 Web Application Security\|CS-11]] |
| SAST / DAST / SCA | Static code analysis / dynamic testing of the running app / software composition (dependency) analysis | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| SBOM | Software bill of materials: a list of components and versions | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| Second-order injection | Malicious input stored safely, then later concatenated into SQL | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| Secure SDLC | A development lifecycle with security activities in every phase | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| Separation of duties | Splitting critical tasks among different people | [[CS-04 Authorization and Access Control\|CS-04]] |
| Session fixation | Forcing a known session ID on a victim before login | [[CS-11 Web Application Security\|CS-11]] |
| Session fixation / hijacking | Forcing a known session ID / stealing an active one | [[CS-03 Authentication and Identity\|CS-03]] |
| setuid | Executable runs with the owner's privileges | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Shared responsibility model | The division of security duties between cloud provider and customer | [[CS-19 Cloud Security and Privacy\|CS-19]] |
| Shift left | Doing security activities earlier in the lifecycle | [[CS-12 Secure Software Development and Database Security\|CS-12]] |
| SIEM | Security information and event management: central collection, correlation and alerting | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| SLE / ARO / ALE | Loss per incident / incidents per year / expected annual loss | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| SNI | Server Name Indication: the hostname sent in the ClientHello | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| SPF / DKIM / DMARC | Email sender authorisation / signature / policy and reporting | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| SSRF | Making the server fetch attacker-chosen URLs, often internal ones | [[CS-11 Web Application Security\|CS-11]] |
| Stateful inspection | Filtering that tracks connection state | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Statement of Applicability (SoA) | An ISO 27001 document listing the selected controls and justifications | [[CS-16 Risk Analysis, Policy, Governance and Compliance\|CS-16]] |
| STRIDE | Spoofing, Tampering, Repudiation, Information disclosure, DoS, Elevation of privilege | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Subject / object / right | Actor / resource / permitted operation | [[CS-04 Authorization and Access Control\|CS-04]] |
| Tabletop exercise | A discussion-based walkthrough of a scenario | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| Threat model | Structured representation of a system's threats and mitigations | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| Timeline | An ordered, merged list of events from several sources | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| Triage | Prioritising alerts by severity and confidence | [[CS-15 Logging, Monitoring, Incident Response and Recovery\|CS-15]] |
| Trust boundary | Where the level of trust changes | [[CS-02 Threat Modeling and Security Requirements\|CS-02]] |
| TTP | Tactics, techniques and procedures (attacker behaviour), more durable than IOCs | [[CS-14 Malware and Defensive Detection\|CS-14]] |
| Typosquatting | Registering misspellings of real domains | [[CS-13 Social Engineering and Security Awareness\|CS-13]] |
| umask | Bits removed from the default permissions of new files | [[CS-10 Operating System Security and Hardening\|CS-10]] |
| Vertical escalation | Gaining a higher role's functions (student → admin) | [[CS-04 Authorization and Access Control\|CS-04]] |
| VLAN | A logical network segment on shared switches | [[CS-09 Network Security and Secure Communication\|CS-09]] |
| Work factor / cost | Parameter controlling the time (and memory) per hash | [[CS-08 Password Storage and Authentication Security\|CS-08]] |
| Write blocker | Hardware or software that prevents writes to the source media | [[CS-17 Digital Forensics Fundamentals\|CS-17]] |
| XSS | Injected script executing in a victim's browser in the site's origin | [[CS-11 Web Application Security\|CS-11]] |

Back to [[Glossary Index]]
