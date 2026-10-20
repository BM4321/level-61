"""Password hashing (scrypt, stdlib), a password policy, and reset tokens.

Teaching code: the policy blocklist is tiny. A real deployment checks a large breached-password
list, adds MFA for staff, rate-limits per IP, and is reviewed by someone qualified.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
from collections.abc import Sequence

COMMON_PASSWORDS = frozenset({
    "password", "password123", "123456789012345", "qwertyuiopasdfgh", "iloveyou", "letmein",
    "welcome123", "passwordpassword",
})


def _b64(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


class PasswordHasher:
    """Self-describing hashes: scrypt$n$r$p$salt$hash. Tests may pass a lower n for speed."""

    def __init__(self, n: int = 2**17, r: int = 8, p: int = 1) -> None:
        self.n, self.r, self.p = n, r, p

    def _derive(self, password: str, salt: bytes, n: int, r: int, p: int) -> bytes:
        return hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p,
                              maxmem=256 * 1024 * 1024, dklen=32)

    def hash(self, password: str) -> str:
        salt = secrets.token_bytes(16)
        digest = self._derive(password, salt, self.n, self.r, self.p)
        return f"scrypt${self.n}${self.r}${self.p}${_b64(salt)}${_b64(digest)}"

    def verify(self, password: str, stored: str) -> bool:
        try:
            scheme, n, r, p, salt, digest = stored.split("$")
        except ValueError:
            return False
        if scheme != "scrypt":
            return False
        actual = self._derive(password, base64.b64decode(salt), int(n), int(r), int(p))
        return hmac.compare_digest(actual, base64.b64decode(digest))

    def needs_rehash(self, stored: str) -> bool:
        parts = stored.split("$")
        return len(parts) != 6 or parts[1:4] != [str(self.n), str(self.r), str(self.p)]


def password_problems(password: str, context_words: Sequence[str] = ()) -> list[str]:
    """Length and blocklist checks (no composition rules), following CS-08."""
    problems = []
    if len(password) < 15:
        problems.append("use at least 15 characters")
    lowered = password.lower()
    if lowered in COMMON_PASSWORDS:
        problems.append("this password is too common")
    for word in context_words:
        if word and word.lower() in lowered:
            problems.append(f"don't include '{word}'")
    return problems


def new_reset_token() -> tuple[str, str]:
    """Return (token for the user, sha256 hex to store). 32 random bytes = 256 bits."""
    token = secrets.token_urlsafe(32)
    return token, hashlib.sha256(token.encode("ascii")).hexdigest()


def token_hash(token: str) -> str:
    return hashlib.sha256(token.encode("ascii", "replace")).hexdigest()
