"""PY-24 reference solutions (secure programming). Teaching code: for production password
hashing prefer a maintained library (argon2-cffi / bcrypt) or your framework's hasher."""
import hashlib
import hmac
import re
import secrets
from pathlib import Path

USERNAME_RE = re.compile(r"[a-z][a-z0-9_]{2,19}")
MODULE_RE = re.compile(r"[A-Z]{3}[0-9]{5}")
HOST_RE = re.compile(r"[A-Za-z0-9.-]{1,253}")
SECRET_KEYS = re.compile(r"(?i)\b(password|passwd|token|api_key|secret)=([^\s&]+)")
CARD = re.compile(r"\b(?:\d[ -]?){12,15}(\d{4})\b")
DEFAULT_ITERATIONS = 600_000


def validate_username(raw: str) -> str:
    """Lower-cased 3-20 chars [a-z0-9_] starting with a letter; ValueError otherwise."""
    name = raw.strip().lower()
    if not USERNAME_RE.fullmatch(name):
        raise ValueError("username: 3-20 chars, letters/digits/_, starting with a letter")
    return name


def validate_module_code(raw: str) -> str:
    """'cst06102 ' -> 'CST06102'; ValueError if not 3 letters + 5 ASCII digits."""
    code = raw.strip().upper()
    if not MODULE_RE.fullmatch(code):
        raise ValueError("module code must be 3 letters followed by 5 digits, e.g. CST06102")
    return code


def safe_path(base: Path, user_name: str) -> Path:
    """Resolved path inside base; ValueError if it escapes (.., absolute paths, symlinks)."""
    root = Path(base).resolve()
    candidate = (root / user_name).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("path escapes the base folder")
    return candidate


def hash_password(password: str, iterations: int = DEFAULT_ITERATIONS) -> str:
    """'pbkdf2_sha256$iters$salthex$hashhex' with a fresh 16-byte salt."""
    salt = secrets.token_bytes(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${dk.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """Recompute with stored parameters; constant-time comparison."""
    algo, iters, salt_hex, dk_hex = stored.split("$")
    if algo != "pbkdf2_sha256":
        raise ValueError("unknown algorithm")
    dk = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), int(iters))
    return hmac.compare_digest(dk.hex(), dk_hex)


def new_token() -> str:
    """URL-safe token with 32 bytes of randomness."""
    return secrets.token_urlsafe(32)


def ping_command(host: str) -> list[str]:
    """Validated argv list for one ping (never use a shell)."""
    if not HOST_RE.fullmatch(host):
        raise ValueError("invalid hostname")
    return ["ping", "-c", "1", host]


def redact(line: str) -> str:
    """Mask secrets and card numbers; escape CR/LF to prevent log forging."""
    line = SECRET_KEYS.sub(lambda m: f"{m.group(1)}=[REDACTED]", line)
    line = CARD.sub(lambda m: "**** **** **** " + m.group(1), line)
    return line.replace("\n", "\\n").replace("\r", "\\r")


def validate_username_reserved(raw: str, reserved: frozenset = frozenset({"admin", "root", "system"})) -> str:
    """validate_username plus rejection of reserved names (case-insensitive)."""
    name = validate_username(raw)
    if name in {r.lower() for r in reserved}:
        raise ValueError("this username is reserved")
    return name
