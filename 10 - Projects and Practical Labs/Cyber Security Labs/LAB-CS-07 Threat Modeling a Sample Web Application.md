---
title: "Threat Modeling a Sample Web Application"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-07"
type: "lab"
difficulty: "intermediate"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-02 Threat Modeling and Security Requirements]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-07 Threat Modeling a Sample Web Application

> [!info] Nature of this lab
> This is a design-analysis lab: you analyse a *fictional* system on paper. No system is tested. The script only generates the empty STRIDE worksheet.

**Script:** `scripts/lab07_threat_model.py` · **Tests:** `tests/test_labs.py::test_lab07` (passing) · **Time:** 2–3 h (good as a group exercise) · **Related lessons:** [[CS-02 Threat Modeling and Security Requirements]], [[X-03 Security Requirements in Software Architecture]], [[SD-17 Secure and Reliable Software Design]]

## Objectives
1. Draw a data-flow diagram (DFD) with trust boundaries for a web application.
2. Apply STRIDE per element to generate candidate threats systematically.
3. Prioritise threats (risk = likelihood × impact) and write mitigations as testable security requirements.
4. Record assumptions and residual risks.

## Prerequisites
- CS-02 (STRIDE, DFDs, trust boundaries).
- CS-16 §5.2 (the risk matrix).

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
python scripts/lab07_threat_model.py > threat_worksheet.md
```
Open `threat_worksheet.md` in Obsidian or a text editor.

**The system:** a hostel maintenance web app (fictional).
- **Students** log in and report faults, with photos.
- **Wardens** assign technicians.
- The **web app** stores requests in a database and photos in object storage, and sends status emails through a third-party email service.

## Procedure
1. **Draw the DFD.** Copy this Mermaid diagram into a note and check it against the system description:
   ```mermaid
   flowchart LR
       S([Student]) -->|login, new request| W[Web app]
       WD([Warden]) -->|assign technician| W
       W -->|SQL| DB[(Request DB)]
       W -->|photos| PS[(Photo store)]
       W -->|notifications| E([Email service])
       W -->|status pages| S
   ```
   Mark the trust boundaries: Internet | DMZ (web app) | internal (DB, photo store) | third party (email).
2. **Generate candidates.** The worksheet lists 38 rows (each element × its applicable STRIDE categories) and the 6 flows that cross trust boundaries. Start with those flows.
3. **Fill in threats.** For each row, write a concrete threat or "not applicable because …". Aim for at least 15 meaningful threats.
4. **Rate them.** Give each one L (1–5) and I (1–5) with a one-line justification, and compute L × I.
5. **Mitigate.** For the top 8, write a mitigation as a **testable requirement**, e.g. "SR-04: The system shall reject photo uploads whose content is not JPEG or PNG (checked by magic bytes) or that are larger than 5 MB."
6. **Assumptions and residual risk.** List what you assumed (e.g. "the email provider is trustworthy") and what risk remains.

## Expected output
The generated worksheet ends with (real output):
```text
Total candidate threats: 38

## Flows crossing trust boundaries (analyse these first)

- Student → Web app (login + new request (HTTPS)): internet → dmz
- Warden → Web app (assign technician (HTTPS)): internet → dmz
- Web app → Request DB (SQL queries): dmz → internal
- Web app → Photo store (upload / fetch photos): dmz → internal
- Web app → Email service (status notifications): dmz → third_party
- Web app → Student (request status pages): dmz → internet
```
The count is 3 external entities × 2 (S, R) + 1 process × 6 + 2 stores × 4 (T, R, I, D) + 6 flows × 3 (T, I, D) = 6 + 6 + 8 + 18 = 38.

Your filled-in worksheet is the real deliverable. A sample of good rows is in the Answers.

## Interpretation
- STRIDE per element is a **completeness aid**: it makes you ask every relevant question, but it doesn't rank threats or pick mitigations.
- Flows that cross trust boundaries are where data passes from less-trusted to more-trusted zones, so they need authentication, validation and encryption.
- Good threat statements name an **actor, an action, an asset and an impact**: "A student changes the request ID in the URL to view another student's room and phone number."

## Cleanup
Delete `threat_worksheet.md` once you've copied your work into your notes, or keep it as evidence of your work.

## Questions
1. Why do external entities get only S and R in STRIDE per element?
2. Write two threats for the flow Web app → Photo store.
3. Which single threat would you rate highest, and why?
4. Turn "use HTTPS" into a testable security requirement.
5. What's one weakness of STRIDE per element?

## Answers
> [!success]- Answers
> 1. External entities are outside the system's control. The system can be fooled about *who* they are (spoofing) and can lose proof of *what they did* (repudiation). Tampering with them, or disclosure inside them, isn't something the system models.
> 2. (a) Tampering: a malicious "photo" is actually an HTML or script file that's later served to wardens, giving stored XSS. (b) Information disclosure: photo URLs are guessable, so anyone can view photos of students' rooms. Mitigations: validate content types, re-encode images, serve them with `Content-Disposition: attachment` or from a separate domain, and use unguessable, access-checked or expiring URLs.
> 3. A reasonable choice: **elevation of privilege / broken access control in the web app** (a student acting as a warden, or viewing others' requests). It's likely (a common bug class) and high-impact (personal and location data for all residents). Other well-justified choices are acceptable.
> 4. "SR-01: All pages and API endpoints shall be served only over TLS 1.2 or later. HTTP requests shall be redirected to HTTPS, and responses shall include `Strict-Transport-Security: max-age=31536000`. Verified by an automated header test in CI and a TLS configuration scan of staging."
> 5. Any of: it generates many low-value rows; it doesn't prioritise; it can miss business-logic abuse (e.g. students flooding the system with fake urgent requests) and privacy harms; and its quality depends on how accurate the DFD is.

## Defensive lessons
- Threat-model during design, when fixes are cheapest, and update the model when the architecture changes.
- Write mitigations as testable requirements, and trace them to tests ([[SD-04 Use Cases, User Stories and Traceability]]).
- Focus first on flows that cross trust boundaries and on assets with personal data.
- Record assumptions explicitly; they're where attacks often hide.

## Mastery checklist
- [ ] I drew the DFD with trust boundaries
- [ ] I wrote at least 15 concrete threats and rated them
- [ ] I wrote 8 testable security requirements
- [ ] I listed my assumptions and residual risks
