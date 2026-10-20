---
title: "Toy Ciphers and Why They Fail"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-03"
type: "lab"
difficulty: "intermediate"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-05 Cryptography Foundations and Symmetric Encryption]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-03 Toy Ciphers and Why They Fail

> [!danger] Ethics and scope
> You break ciphers here only on messages you encrypted yourself. The toy ciphers in this lab are **insecure by design**. Never use Caesar, Vigenère, repeating-key XOR or any home-made cipher to protect real data. Use vetted libraries (AES-GCM, ChaCha20-Poly1305) as in Part E.

**Script:** `scripts/lab03_toy_ciphers.py` · **Tests:** `tests/test_labs.py::test_lab03` (passing) · **Time:** 60–90 min · **Related lessons:** [[CS-05 Cryptography Foundations and Symmetric Encryption]], [[DM-07 Functions]], [[DM-18 Introductory Discrete Probability]]

## Objectives
1. Break a Caesar cipher by exhaustive key search plus frequency scoring (chi-squared).
2. Break a Vigenère cipher with a known key length by splitting it into Caesar columns, and see why short messages resist statistical attacks.
3. Show that reusing a one-time pad or stream key leaks $p_1 \oplus p_2$.
4. Contrast all of this with authenticated encryption (AES-256-GCM), which also detects tampering.

## Prerequisites
- Python 3.10+.
- Part E needs `cryptography` (`pip install cryptography`); it's skipped if the package is missing. During the build, `cryptography` 50.0.1 was used.

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
python -m venv .venv && . .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install cryptography                          # optional, for Part E
```

## Procedure (commands)
1. `python scripts/lab03_toy_ciphers.py`
2. Change the Caesar shift in Part A (e.g. 19) and confirm that `break_caesar` still finds it.
3. In Part C, change the key to a 6-letter word. Update the column split (`[i::6]` and `range(6)`) and recover the key again.
4. Shorten `long_msg` gradually. At roughly what length does key recovery start failing?
5. Read Part D, and explain on paper why $c_1 \oplus c_2 = p_1 \oplus p_2$.

## Expected output
Real output from the build machine. Parts A–D are deterministic and should match exactly. In Part E only the lengths and verdicts are printed, so it matches too.
```text
== Part A: Caesar cipher (shift 7) ==
ciphertext: Tlla aol lehtpuhapvuz vmmpjly ha aol spiyhyf ha uvvu huk iypun aol thyrlk zjypwaz
brute force + frequency score -> key 7: Meet the examinations officer at the library at noon and bring the marked scripts
keyspace: 26 keys; a computer checks them all instantly

== Part B: letter frequencies leak through substitution ==
most common ciphertext letters: [('l', 8), ('a', 8), ('h', 7)] (plaintext 'e' shifted by 7 is 'l')

== Part C: Vigenere (key 'chuo') ==
ciphertext (first 60): Olyh voy szhgwphnwqum chmcqgy uh voy zkilotf uh pvib cux ptp ...
split into 4 columns, break each as Caesar -> key 'chuo'
decrypt with recovered key: Meet the examinations officer at the library at noon and bri ...
same attack on the short message alone -> 'ohuo' (too little text for statistics)

== Part D: reusing a one-time pad / stream key ==
c1 xor c2 == p1 xor p2 ? True
attacker who knows (or guesses) p1 recovers p2: b'PAY NEEMA 900 TZ'

== Part E: the real thing (AES-256-GCM, authenticated) ==
ciphertext+tag length: 97 bytes (message 81 + 16-byte tag)
one flipped bit -> InvalidTag: tampering detected
decrypts correctly: True
```

## Interpretation
- **Caesar:** 26 keys is a trivially small keyspace, and the chi-squared score picks the right one automatically.
- **Frequencies:** a substitution keeps the shape of the letter distribution. Plaintext `e` (shifted to `l`) and `t` (shifted to `a`) stay among the most common letters.
- **Vigenère:** a longer key hides frequencies across columns, but each column is still a Caesar cipher. With enough text, every column breaks. On the short message, the attack got only the last three key letters right (`ohuo` vs `chuo`), because a few letters per column isn't enough for statistics. **That's not security:** an attacker waits for more ciphertext, or guesses words.
- **Key reuse:** XOR cancels the key, so two ciphertexts under the same pad leak the XOR of the plaintexts, and knowing (or guessing) one message reveals the other. This is why nonces must never repeat with stream ciphers or AES-GCM.
- **AES-GCM:** a large keyspace ($2^{256}$), no exploitable statistics, and an authentication tag. One flipped bit is rejected, which no toy cipher can do.

## Cleanup
Nothing is written to disk. Deactivate the virtual environment (`deactivate`), and delete `.venv` if you created it only for this lab.

## Questions
1. How many keys does a general monoalphabetic substitution cipher (any permutation of 26 letters) have? Why is it still easy to break?
2. Why does the Vigenère attack need the key length, and how could an attacker find it?
3. In Part D, what goes wrong if the attacker knows only that both messages start with `PAY `?
4. Why is "the attacker doesn't know my algorithm" not a defence (Kerckhoffs's principle)?
5. What would happen in Part E if the same nonce were reused for two different messages under the same key?

## Answers
> [!success]- Answers
> 1. $26! \approx 4.03\times10^{26}$ keys, about $2^{88}$, so brute force is impractical. But frequency analysis and common-word patterns break it by hand. A large keyspace is necessary, not sufficient.
> 2. Without the key length you can't split the ciphertext into Caesar columns. Methods: the **Kasiski examination** (repeated ciphertext fragments are often separated by multiples of the key length) or the **index of coincidence** (each candidate length is tested to see whether its columns look like English).
> 3. They recover only the first 4 bytes of $p_2$ (also `PAY `). Each correct guess of $p_1$ reveals the matching part of $p_2$; this is "crib dragging". Partial guesses leak partial plaintext.
> 4. Algorithms leak (reverse engineering, insiders, published code). Security must rest only on the **key**, so the algorithm should be public and well analysed.
> 5. GCM's keystream would repeat, leaking $p_1 \oplus p_2$ exactly as in Part D, and nonce reuse also lets attackers forge authentication tags. So nonces must be unique per key (random 96-bit nonces, with limits on the number of messages, or counters).

## Defensive lessons
- Never invent or use home-made ciphers; use vetted constructions through maintained libraries.
- Encryption needs authentication (AEAD) as well as secrecy.
- Never reuse a key and nonce pair.
- Keep keys secret and algorithms public (Kerckhoffs's principle).

## Mastery checklist
- [ ] I broke Caesar and Vigenère on my own messages
- [ ] I can explain the key-reuse XOR leak on paper
- [ ] I can explain what AES-GCM adds beyond secrecy
