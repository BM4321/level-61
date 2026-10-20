---
title: "Log Analysis and Incident Response"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-08"
type: "lab"
difficulty: "intermediate"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-15 Logging, Monitoring, Incident Response and Recovery]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-08 Log Analysis and Incident Response

> [!danger] Ethics and scope
> The default input `data/auth_sample.log` is a **constructed** log: fictional users, and IP addresses from the documentation ranges. To analyse a real log, use only a copy from a machine you administer. Real logs contain personal data (usernames, IP addresses), so handle them under your organisation's policy.

**Script:** `scripts/lab08_log_analysis.py` · **Data:** `data/auth_sample.log` (20 lines) · **Tests:** `tests/test_labs.py::test_lab08` (passing) · **Time:** 90–120 min · **Related lessons:** [[CS-15 Logging, Monitoring, Incident Response and Recovery]], [[CS-17 Digital Forensics Fundamentals]]

## Objectives
1. Treat the log as evidence: hash it before analysis.
2. Parse SSH and sudo events, and summarise them by kind, IP address and username.
3. Run four detections: fast bursts, slow guessing, password spraying, and success after failures.
4. Build an incident timeline and decide on containment actions.
5. Write a short incident report.

## Prerequisites
- Python 3.10+.
- CS-15 §5.3–5.4.

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
sha256sum data/auth_sample.log         # record this before analysis
```

## Procedure (commands)
1. Run the analysis: `python scripts/lab08_log_analysis.py`
2. Confirm that the hash printed by the script matches the one you recorded.
3. Read each detection (D1–D4) and decide: is it noise, suspicious, or an incident?
4. For the D4 hit, write the timeline in your own words, with what each event means.
5. Experiment with the thresholds: change `bursts(events, 5, …)` to 3, and `spraying(..., min_users=5)` to 4. Which new alerts appear? Are they useful or noise?
6. Write the incident report (see Questions 5).
7. Optional: copy a real `/var/log/auth.log` from **your own** Linux VM, and adapt the regular expressions to its format (the sample uses ISO timestamps and a `host=` field; syslog uses `Mon DD HH:MM:SS host`).

## Expected output
Real output from the build machine (deterministic):
```text
evidence: auth_sample.log  sha256=ad7822d2656a7135364eb6dc4198a42f9d1eaf68614f0cf4f7be72d733017044
parsed 20 events, skipped 0 unparseable lines
by kind: {'login_accepted': 3, 'login_failed': 16, 'sudo': 1}
failures by IP: {'203.0.113.50': 7, '192.0.2.99': 5, '198.51.100.23': 3, '198.51.100.7': 1}
invalid usernames tried: ['admin', 'guest', 'oracle', 'pi', 'test', 'ubuntu', 'user']

== Detections ==
D1 fast bursts (>=5 in 2 min): {'203.0.113.50': 7, '192.0.2.99': 5}
D2 slow guessing (>=3 in 1 h): {'203.0.113.50': 7, '198.51.100.23': 3, '192.0.2.99': 5}
D3 spraying (>=5 users in 10 min from one IP): {'192.0.2.99': 5}
D4 success after >=3 failures: [('juma', '203.0.113.50', '2026-03-02T08:14:36+00:00')]

== Timeline for each D4 hit (events from the same IP or user, next 10 minutes) ==
-- juma from 203.0.113.50
   08:14:22Z  login_failed (password) for test from 203.0.113.50
   08:14:24Z  login_failed (password) for oracle from 203.0.113.50
   08:14:25Z  login_failed (password) for root from 203.0.113.50
   08:14:27Z  login_failed (password) for root from 203.0.113.50
   08:14:29Z  login_failed (password) for juma from 203.0.113.50
   08:14:31Z  login_failed (password) for juma from 203.0.113.50
   08:14:33Z  login_failed (password) for juma from 203.0.113.50
   08:14:36Z  login_accepted (password) for juma from 203.0.113.50
   08:15:02Z  /usr/bin/cat /etc/shadow
```

## Interpretation
| Detection | Verdict | Reasoning |
|---|---|---|
| D1 `192.0.2.99`, 5 failures | Suspicious, low priority | Automated scanning of default usernames (admin, pi, ubuntu…), all invalid, with no success |
| D3 `192.0.2.99` | The same activity | Five *different* usernames in seconds, typical of opportunistic scanning |
| D2 `198.51.100.23`, 3 failures over 38 minutes for `mrs_k` | Ambiguous | Could be slow guessing, or a user who forgot her password. Contact the user through a known channel |
| `198.51.100.7`: 1 failure, then success for `amina` | Normal | A single typo, then success |
| **D4 `juma` from `203.0.113.50`** | **Incident** | Guessing ended in success, followed within 26 seconds by reading the system's password-hash file with sudo |

**Immediate response (containment):**
1. Disable `juma` and kill their sessions.
2. Isolate web01 (network quarantine) while preserving it for investigation.
3. Block 203.0.113.50 (a weak control on its own).
4. Treat every credential hashed in `/etc/shadow` as exposed, and rotate them.

**Eradication and recovery:**
- check for persistence (new users, `authorized_keys`, cron jobs, services);
- rebuild from a known-good image if any compromise is confirmed;
- switch SSH to keys only, behind a VPN, with MFA;
- reduce `juma`'s sudo rights.

**Post-incident:**
- add a real-time alert for D4;
- review why password SSH was exposed to the Internet.

## Cleanup
Nothing is modified: the script only reads the log. If you copied a real log for step 7, delete the copy when you finish, or store it according to policy.

## Questions
1. Why hash the log before analysing it?
2. Why is D2 needed in addition to D1?
3. Why is blocking the attacker's IP address not enough on its own?
4. Which fields would you add to these logs to make the investigation easier?
5. Write a half-page incident report: summary, timeline, impact, actions taken, root cause, recommendations.

## Answers
> [!success]- Answers
> 1. To prove later that the analysed copy is identical to what was collected (integrity and chain of custody, [[CS-17 Digital Forensics Fundamentals]]), and to detect accidental changes.
> 2. Slow attacks spread their guesses out to stay under short-window thresholds. Only a longer window sees `198.51.100.23`'s three failures in 38 minutes. Using several windows trades sensitivity against noise.
> 3. Attackers can change IP addresses easily (cloud hosts, proxies, botnets). The account was already compromised, and the attacker may have persistence or stolen hashes. Containment must target the account, the host and the credentials.
> 4. A correlation or session ID linking login to subsequent commands; the authentication method and MFA result; the source port and geolocation; the target files for sudo commands (they are present here); and the host's NTP sync status. Never add passwords or secrets.
> 5. **Summary:** on 2026-03-02, a password-guessing attack from 203.0.113.50 succeeded against the SSH account `juma` on web01 at 08:14:36Z. The attacker then read `/etc/shadow` via sudo. **Timeline:** as above. **Impact:** a compromised account; root-level read of all local password hashes; potential further access still under investigation. **Actions:** the account was disabled, sessions killed, the host isolated, credentials rotated, a persistence check performed. **Root cause:** internet-facing SSH with password authentication, a weak password, no MFA, broad sudo rights, no real-time alerting. **Recommendations:** SSH keys only, via VPN and bastion, with MFA; least-privilege sudo; a D4 alert to on-call staff; a quarterly review of exposed services. Owners and due dates are assigned for each.

## Defensive lessons
- Centralise authentication logs and alert in real time on success-after-failure.
- Use several detection windows; tune the thresholds against your own baseline.
- Respond by account and host, not just by IP address.
- Remove the root cause: exposed password-based remote access.

## Mastery checklist
- [ ] I reproduced the expected output and the evidence hash
- [ ] I classified every detection with reasoning
- [ ] I wrote the timeline and the incident report
- [ ] I experimented with the thresholds and judged the noise
