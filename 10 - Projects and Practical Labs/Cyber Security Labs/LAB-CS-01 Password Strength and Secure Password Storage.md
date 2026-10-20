---
title: "Password Strength and Secure Password Storage"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-01"
type: "lab"
difficulty: "foundation"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-08 Password Storage and Authentication Security]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-01 Password Strength and Secure Password Storage

> [!danger] Ethics and scope
> Run this lab only on your own machine. It uses made-up passwords in memory. Never put real passwords (yours or anyone else's) into lab scripts, and never try cracking hashes you don't own.

**Script:** `scripts/lab01_passwords.py` · **Tests:** `tests/test_labs.py::test_lab01` (passing) · **Time:** 60–90 min · **Related lessons:** [[CS-08 Password Storage and Authentication Security]], [[CS-03 Authentication and Identity]]

## Objectives
1. Apply a modern password policy (length + blocklist) and see why "complex but short" passwords fail it.
2. See why naive entropy formulas **overestimate** the strength of human-chosen passwords.
3. Measure, on your own machine, how much slower a password KDF is than a plain hash.
4. Show that salts make identical passwords store differently, and that unsalted hashes reveal password reuse.

## Prerequisites
- Python 3.10+ (standard library only).
- CS-08 sections 5.2–5.6.

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
python --version          # 3.10 or later
```
No packages are needed and no files are written.

## Procedure (commands)
1. Run the script: `python scripts/lab01_passwords.py`
2. Read Part A, and add two passwords of your own invention (not real ones) to `samples` in `main()`. Predict each verdict before re-running.
3. Run it twice more and compare Part B's timings. Change `600_000` to `100_000` and note the change.
4. In Part C, note that the two stored values differ, although the password is the same.
5. Optional: run the tests with `python -m pytest -q`.

## Expected output
Real output from the build machine (Python 3.13, Linux). **Your timings and salts will differ.** The salts are random by design, and the timings depend on the hardware.
```text
== Part A: policy check and naive entropy (upper bound) ==
'password123'                      len=11  charset=36  naive_bits=  56.9  REJECT: on blocklist
'Tr0ub4dor&3'                      len=11  charset=95  naive_bits=  72.3  REJECT: shorter than 15
'chuo2026'                         len= 8  charset=36  naive_bits=  41.4  REJECT: on blocklist
'ndizi mbili chai moto asubuhi'    len=29  charset=59  naive_bits= 170.6  ACCEPT
'correct horse battery staple'     len=28  charset=59  naive_bits= 164.7  ACCEPT
'Xk9#mP2$vL7!qR4z'                 len=16  charset=95  naive_bits= 105.1  ACCEPT

== Part B: fast hash vs slow KDF (seconds per hash on THIS machine) ==
sha256             4.72e-07 s
pbkdf2 600k iters  1.71e-01 s   (362,757x slower than sha256)
scrypt N=2^14      4.48e-02 s   (94,888x slower than sha256)

== Part C: salts make identical passwords store differently ==
hash 1: scrypt$16384$8$1$sIw2n9wgjlDQRK9u+Zp6Sw==$7l86uwoxy8mCPasTpP7udbAb3KF81MoQF2UlYhxxnpo=
hash 2: scrypt$16384$8$1$kbZQhx99HUSBib59y966qQ==$afZ4p+cFM58cQqv65Z9mxQKW/+RL79LZFXxxtnyuaJQ=
identical stored values? False
verify correct: True  verify wrong: False

== Part D: unsalted fast hashes leak equal passwords ==
ef92b778bafe771e ['amina', 'juma'] <- SAME PASSWORD
744a8627446a80d0 ['baraka']
```

## Interpretation
- **Part A:** `password123` scores 56.9 "naive bits" but is one of the first guesses any attacker tries, so the blocklist matters more than the formula. `Tr0ub4dor&3` looks complex but is short and follows a predictable substitution pattern. The formula gives `correct horse battery staple` 164.7 bits, but if it was chosen as four random words from a 2,048-word list, its true strength is $4\log_2 2048 = 44$ bits. **The formula measures the alphabet, not how the password was chosen.**
- **Part B:** the slow KDF costs about 0.04–0.2 s per guess on this machine. That's harmless at login, but it multiplies an offline attacker's work by roughly $10^5$ compared with SHA-256.
- **Part C:** random salts make every stored value unique, so precomputed tables are useless and each account must be attacked separately.
- **Part D:** without salts, equal passwords give equal hashes. A leaked table immediately shows who shares passwords, and cracking one cracks all of them.

The scrypt cost here (N = 2¹⁴) is kept small so the lab runs quickly. Production systems should follow current guidance (CS-08 §5.4, e.g. scrypt N = 2¹⁷ or Argon2id) and use a maintained library.

## Cleanup
Nothing to clean up: the script writes no files. Remove any passwords you added to `samples`.

## Questions
1. Why does the script call naive entropy an "upper bound"?
2. Part B on your machine: how many scrypt guesses per second could one CPU core make? How many SHA-256 guesses?
3. Why is `compare_digest` used in `verify_password`?
4. A system stores `sha256(password)`. List two things an attacker learns immediately from a leaked table, before any cracking.
5. Change the policy to "minimum 8 characters, no blocklist". Which sample passwords now pass that shouldn't?

## Answers
> [!success]- Answers
> 1. The formula assumes every character was chosen uniformly at random from the full alphabet. People choose words, names, dates and patterns, so the real search space is far smaller.
> 2. Guesses per second ≈ 1 / (seconds per hash). With the build machine's numbers: scrypt ≈ 1 / 0.0448 ≈ 22 per second; SHA-256 ≈ 1 / 4.72×10⁻⁷ ≈ 2.1 million per second. Use your own measurements.
> 3. A normal `==` comparison can stop at the first differing byte, so response times could leak how much of a guessed hash matched. `compare_digest` takes the same time regardless.
> 4. (a) Which users share the same password (equal hashes). (b) Which accounts use very common passwords: look the hash up in public tables (e.g. `ef92b778…` is SHA-256 of `password123`).
> 5. `password123` (11 characters), `Tr0ub4dor&3` and `chuo2026` (8) would all pass, although the first and third are on the blocklist and the second is predictable.

## Defensive lessons
- Store passwords only with a slow, salted KDF (Argon2id or scrypt; bcrypt or PBKDF2 where required), using current parameters.
- Policies should require length and check a blocklist; composition rules add little.
- Never trust strength meters based only on character classes.
- Assume hash tables will leak one day, and design so that a leak is survivable.

## Mastery checklist
- [ ] I ran the script and can explain each part's output
- [ ] I can explain why naive entropy overestimates human passwords
- [ ] I measured my own fast-hash vs KDF timings
- [ ] I can explain what salts do and don't protect against
