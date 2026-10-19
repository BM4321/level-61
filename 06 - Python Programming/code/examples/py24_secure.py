"""PY-24: match vs fullmatch, redaction, password hashing. Run: python examples/py24_secure.py"""
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py24_solutions import hash_password, redact, verify_password  # noqa: E402

CODE_RE = re.compile(r"[A-Z]{3}\d{5}")
print("match    :", bool(CODE_RE.match("CST06102; DROP TABLE marks")))
print("fullmatch:", bool(CODE_RE.fullmatch("CST06102; DROP TABLE marks")))
print(redact("login user=amina password=Hunter2! token=abc123&x=1"))

start = time.perf_counter()
stored = hash_password("correct horse battery staple")
print(f"PBKDF2 600k iterations took {time.perf_counter() - start:.2f}s (an attacker pays this per guess)")
print(stored[:40] + "...", verify_password("correct horse battery staple", stored))
