"""LAB-CS-01: password strength estimates and secure storage (standard library only).

Run:  python lab01_passwords.py
Everything happens in memory; no files are written and nothing is sent anywhere.
"""
import base64
import hashlib
import hmac
import math
import os
import string
import time

# A tiny demonstration blocklist. Real systems use large breached-password corpora.
BLOCKLIST = {"password", "password123", "123456", "qwerty", "letmein", "admin", "welcome1", "chuo2026"}


def charset_size(pw: str) -> int:
    size = 0
    if any(c in string.ascii_lowercase for c in pw):
        size += 26
    if any(c in string.ascii_uppercase for c in pw):
        size += 26
    if any(c in string.digits for c in pw):
        size += 10
    if any(not c.isalnum() for c in pw):
        size += 33  # printable ASCII symbols incl. space
    return size


def naive_entropy_bits(pw: str) -> float:
    """L * log2(charset). Overestimates human-chosen passwords: an UPPER bound, not a measurement."""
    k = charset_size(pw)
    return len(pw) * math.log2(k) if k else 0.0


def assess(pw: str, min_length: int = 15) -> str:
    if pw.lower() in BLOCKLIST:
        return "REJECT: on blocklist"
    if len(pw) < min_length:
        return f"REJECT: shorter than {min_length}"
    return "ACCEPT"


def hash_password(pw: str, salt: bytes | None = None, n: int = 2 ** 14) -> str:
    salt = os.urandom(16) if salt is None else salt
    dk = hashlib.scrypt(pw.encode(), salt=salt, n=n, r=8, p=1, dklen=32)
    return f"scrypt${n}$8$1${base64.b64encode(salt).decode()}${base64.b64encode(dk).decode()}"


def verify_password(pw: str, stored: str) -> bool:
    _alg, n, r, p, salt_b64, dk_b64 = stored.split("$")
    dk = hashlib.scrypt(pw.encode(), salt=base64.b64decode(salt_b64), n=int(n), r=int(r), p=int(p), dklen=32)
    return hmac.compare_digest(dk, base64.b64decode(dk_b64))


def time_it(fn, repeat: int) -> float:
    start = time.perf_counter()
    for _ in range(repeat):
        fn()
    return (time.perf_counter() - start) / repeat


def main() -> None:
    print("== Part A: policy check and naive entropy (upper bound) ==")
    samples = ["password123", "Tr0ub4dor&3", "chuo2026", "ndizi mbili chai moto asubuhi",
               "correct horse battery staple", "Xk9#mP2$vL7!qR4z"]
    for pw in samples:
        print(f"{pw!r:34} len={len(pw):2}  charset={charset_size(pw):2}  "
              f"naive_bits={naive_entropy_bits(pw):6.1f}  {assess(pw)}")

    print("\n== Part B: fast hash vs slow KDF (seconds per hash on THIS machine) ==")
    pw = b"ndizi mbili chai moto asubuhi"
    salt = b"\x00" * 16
    t_sha = time_it(lambda: hashlib.sha256(pw).digest(), 20000)
    t_pbk = time_it(lambda: hashlib.pbkdf2_hmac("sha256", pw, salt, 600_000), 2)
    t_scr = time_it(lambda: hashlib.scrypt(pw, salt=salt, n=2 ** 14, r=8, p=1), 3)
    print(f"sha256             {t_sha:.2e} s")
    print(f"pbkdf2 600k iters  {t_pbk:.2e} s   ({t_pbk / t_sha:,.0f}x slower than sha256)")
    print(f"scrypt N=2^14      {t_scr:.2e} s   ({t_scr / t_sha:,.0f}x slower than sha256)")

    print("\n== Part C: salts make identical passwords store differently ==")
    a, b = hash_password("same-password"), hash_password("same-password")
    print("hash 1:", a)
    print("hash 2:", b)
    print("identical stored values?", a == b)
    print("verify correct:", verify_password("same-password", a), " verify wrong:", verify_password("Same-password", a))

    print("\n== Part D: unsalted fast hashes leak equal passwords ==")
    users = {"amina": "password123", "baraka": "ndizi mbili chai", "juma": "password123"}
    seen = {}
    for user, p in users.items():
        seen.setdefault(hashlib.sha256(p.encode()).hexdigest()[:16], []).append(user)
    for digest, who in seen.items():
        print(digest, who, "<- SAME PASSWORD" if len(who) > 1 else "")


if __name__ == "__main__":
    main()
