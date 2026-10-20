---
title: "Hashing and Integrity Verification"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-02"
type: "lab"
difficulty: "foundation"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-06 Hashes, MACs and Integrity]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-02 Hashing and Integrity Verification

> [!danger] Ethics and scope
> The script creates and changes only its own practice files, inside a workspace directory that it creates. Run it on your own machine.

**Script:** `scripts/lab02_integrity.py` · **Tests:** `tests/test_labs.py::test_lab02` (passing) · **Time:** 45–60 min · **Related lessons:** [[CS-06 Hashes, MACs and Integrity]], [[CS-07 Public-Key Cryptography, Signatures and Key Management]]

## Objectives
1. Create a `SHA256SUMS` manifest and verify files against it, both in Python and with the standard `sha256sum` tool.
2. Detect tampering with one file.
3. Show that a plain manifest fails when the attacker can also rewrite it, and that a keyed HMAC tag (or a signature) still detects the change.
4. Observe the avalanche effect.

## Prerequisites
- Python 3.10+.
- Optional: `sha256sum` (Linux, WSL, Git Bash), or `shasum -a 256` (macOS), or `Get-FileHash` (PowerShell).

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
```
The workspace defaults to `./lab02_workspace`. You can pass another path as the first argument.

## Procedure (commands)
1. `python scripts/lab02_integrity.py`. The script runs steps 1–5 in sequence.
2. Check the manifest independently with the system tool. Note that the script has already rewritten the manifest in step 4, so re-run steps 1–2 first:
   ```bash
   python scripts/lab02_integrity.py && cd lab02_workspace && sha256sum -c SHA256SUMS; cd ..
   ```
   On Windows PowerShell, use `Get-FileHash .\lab02_workspace\policy.txt -Algorithm SHA256` and compare the value by eye.
3. Open `lab02_workspace/results_2026.csv`, change one character by hand, and run `sha256sum -c SHA256SUMS` again inside the workspace.
4. Clean up (see below).

## Expected output
Real output from the build machine. The file contents are fixed, so **your hashes should match exactly**:
```text
== Step 1: create manifest ==
cff4a4cb7fad9714439905348ba50662e15eb6fc23c618b13ada38116be4c467  installer_readme.txt
0aa481195825582a0d6a6f0281bafc549e374f494994801ed381d84d5c0d3c4d  policy.txt
27451312771f4b3cbdff237ac5d18be2a3814e4a37ebfef92c2e1651ba8f3c14  results_2026.csv
HMAC-SHA256 tag of manifest: 85f0194b7bd4c3e45b4978699c3cac16d222b1b07477bb74f2e333abcf0c1237

== Step 2: verify untouched files ==
installer_readme.txt: OK
policy.txt: OK
results_2026.csv: OK

== Step 3: tamper with one grade (B+ -> A) and verify again ==
installer_readme.txt: OK
policy.txt: OK
results_2026.csv: FAILED

== Step 4: attacker also rewrites SHA256SUMS ==
plain manifest check now says: ['installer_readme.txt: OK', 'policy.txt: OK', 'results_2026.csv: OK']
HMAC check of forged manifest: INVALID (tampering detected)

== Step 5: avalanche effect ==
b'grade=B+'  f56e4a901c724ac5952ef34a25ae9a9cb96daceeb551a2326245f4169261bd51
b'grade=A'   1d0d02d641c42588bc4f65100fe2a1c6cfd76f25501eaf52142915fbc173476e
```
`sha256sum -c SHA256SUMS` on a freshly created workspace printed `OK` for all three files during the build. So the script's manifest format is the standard one: a hex digest, two spaces, then the filename.

On Windows, files edited in Notepad may gain `\r\n` line endings. That changes the hash, which is itself a lesson in how strict integrity checks are.

## Interpretation
- **Step 3:** changing two bytes (`B+` → `A`) produces a completely different digest, so the check fails.
- **Step 4** is the key lesson. If the attacker can change both the file and the manifest stored next to it, a plain hash check passes. Integrity needs a reference the attacker **can't** forge: an HMAC under a key they don't hold, a digital signature, or a hash obtained through a separate trusted channel.
- **Step 5:** similar inputs give unrelated digests (the avalanche effect), so you can't "adjust" a file to keep its hash.

The HMAC key in the script is a labelled demo constant. Real keys come from a secrets manager and never appear in code.

## Cleanup
```bash
python scripts/lab02_integrity.py --cleanup
```
This removes the workspace only if it contains a `SHA256SUMS` file, so it won't delete an unrelated directory.

## Questions
1. Why does step 4's plain check pass, and which assumption broke?
2. Who can verify an HMAC tag, and who can verify a digital signature? Which would you use for a public software download?
3. Which hash property does the step 5 output illustrate?
4. Your colleague says: "We store the hashes of our backup files on the same backup server, so we'll know if ransomware changes them." Critique this.
5. Write the command that verifies one downloaded file `tool.zip` against a published hash value without a manifest file.

## Answers
> [!success]- Answers
> 1. The check assumed that the manifest itself was trustworthy. The attacker regenerated it after tampering, so the files matched the new hashes. A reference value is only as trustworthy as where it came from.
> 2. HMAC: only parties who hold the shared secret key, so it's suitable between your own systems. Signature: anyone with the public key, so it's suitable for public downloads, because users can verify it without being able to forge it.
> 3. The avalanche effect: a small change in the input flips about half the output bits, unpredictably.
> 4. Ransomware or an attacker with access to that server can rewrite the hashes too (step 4). Store the reference hashes, or an HMAC or signature over them, **somewhere else**: on a separate system, offline, or signed with a key that isn't on the backup server.
> 5. Linux: `echo "<published-hash>  tool.zip" | sha256sum -c -`. macOS: `shasum -a 256 tool.zip`, then compare. PowerShell: `(Get-FileHash tool.zip -Algorithm SHA256).Hash -eq "<PUBLISHED-HASH>"`.

## Defensive lessons
- Hashes detect change only if the reference value is trustworthy. Sign manifests, or obtain them from a separate channel.
- Use SHA-256 or stronger; never MD5 or SHA-1 for security.
- Automate integrity checks for critical files (configuration, backups, releases), and alert on failures.
- Keep MAC and signing keys off the systems they protect.

## Mastery checklist
- [ ] My hashes matched the expected output exactly
- [ ] I verified the manifest with a system tool
- [ ] I can explain why step 4 needs an HMAC or signature
- [ ] I cleaned up the workspace
