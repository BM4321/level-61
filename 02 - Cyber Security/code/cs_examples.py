"""Runnable, tested versions of code shown in the Cyber Security lessons (ITT06102).

Defensive teaching code. Standard library only (Python 3.10+).
"""
import base64
import hashlib
import html
import hmac
import ipaddress
import os
import secrets
import sqlite3
import stat
import struct
import time
from urllib.parse import urlsplit

# ---------------------------------------------------------------- CS-03 HOTP / TOTP


def hotp(key: bytes, counter: int, digits: int = 6) -> str:
    """RFC 4226 HOTP with HMAC-SHA1 and dynamic truncation."""
    mac = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = mac[-1] & 0x0F
    code = (int.from_bytes(mac[offset:offset + 4], "big") & 0x7FFFFFFF) % 10 ** digits
    return str(code).zfill(digits)


def totp(key: bytes, at: float | None = None, step: int = 30, digits: int = 6) -> str:
    """RFC 6238 TOTP (T0 = 0)."""
    t = time.time() if at is None else at
    return hotp(key, int(t // step), digits)


def verify_totp(key: bytes, code: str, at: float, window: int = 1, step: int = 30) -> bool:
    """Accept codes within +-window time steps, compared in constant time."""
    return any(hmac.compare_digest(hotp(key, int(at // step) + d, len(code)), code)
               for d in range(-window, window + 1))


# ---------------------------------------------------------------- CS-04 RBAC + object-level checks
PERMISSIONS = {
    "student": {"view_own_requests"},
    "technician": {"view_assigned_requests", "update_status"},
    "warden": {"view_all_requests", "assign_technician", "close_request"},
}


class Forbidden(Exception):
    pass


def authorize(user: dict, action: str, req: dict | None = None) -> None:
    """Deny by default; raise Forbidden unless the role and object rules allow the action."""
    perms = PERMISSIONS.get(user.get("role"), set())
    if action == "view_request":
        if "view_all_requests" in perms:
            return
        if "view_own_requests" in perms and req and req["reporter"] == user["id"]:
            return
        if "view_assigned_requests" in perms and req and req.get("technician") == user["id"]:
            return
    elif action in perms:
        if action == "update_status" and (not req or req.get("technician") != user["id"]):
            raise Forbidden("not your assigned job")
        return
    raise Forbidden(f"{user.get('id')} may not {action}")


# ---------------------------------------------------------------- CS-08 password storage (scrypt)
# Parameters follow the OWASP Password Storage Cheat Sheet's scrypt guidance (N=2**17, r=8, p=1).
# Prefer a maintained library (argon2-cffi, bcrypt) in production; this shows the mechanics.
SCRYPT_N, SCRYPT_R, SCRYPT_P = 2 ** 17, 8, 1
_MAXMEM = 256 * 1024 * 1024


def hash_password(password: str, *, n: int = SCRYPT_N, r: int = SCRYPT_R, p: int = SCRYPT_P,
                  salt: bytes | None = None) -> str:
    """Return a self-describing string: scrypt$n$r$p$salt_b64$hash_b64."""
    salt = os.urandom(16) if salt is None else salt
    dk = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=n, r=r, p=p, maxmem=_MAXMEM, dklen=32)
    b64 = lambda b: base64.b64encode(b).decode("ascii")  # noqa: E731
    return f"scrypt${n}${r}${p}${b64(salt)}${b64(dk)}"


def verify_password(password: str, stored: str) -> bool:
    """Recompute with the stored parameters and compare in constant time."""
    try:
        alg, n, r, p, salt_b64, dk_b64 = stored.split("$")
        if alg != "scrypt":
            return False
        salt, expected = base64.b64decode(salt_b64), base64.b64decode(dk_b64)
    except ValueError:
        return False
    dk = hashlib.scrypt(password.encode("utf-8"), salt=salt, n=int(n), r=int(r), p=int(p),
                        maxmem=_MAXMEM, dklen=len(expected))
    return hmac.compare_digest(dk, expected)


def needs_rehash(stored: str, *, n: int = SCRYPT_N, r: int = SCRYPT_R, p: int = SCRYPT_P) -> bool:
    """True if the stored hash used weaker (or different) parameters than the current policy."""
    parts = stored.split("$")
    return len(parts) != 6 or parts[0] != "scrypt" or (int(parts[1]), int(parts[2]), int(parts[3])) != (n, r, p)


def password_problems(password: str, blocklist: set[str], min_length: int = 15,
                      max_length: int = 64) -> list[str]:
    """Length + blocklist checks in the spirit of NIST SP 800-63B; no composition rules."""
    problems = []
    if len(password) < min_length:
        problems.append(f"shorter than {min_length} characters")
    if len(password) > max_length:
        problems.append(f"longer than {max_length} characters")
    if password.lower() in blocklist:
        problems.append("appears in the blocklist of common or breached passwords")
    return problems


# ---------------------------------------------------------------- CS-09 first-match packet filter
# A teaching model of an ordered rule list (like iptables/nftables chains or cloud security groups).
# Rule: (action, src_cidr, dst_cidr, protocol, dst_port) where "any" / None mean wildcard.
Rule = tuple[str, str, str, str, int | None]


def match_rule(rules: list[Rule], src: str, dst: str, proto: str, port: int,
               default: str = "deny") -> tuple[str, int | None]:
    """Return (action, index of matching rule) for the first rule that matches; else the default."""
    s, d = ipaddress.ip_address(src), ipaddress.ip_address(dst)
    for i, (action, src_net, dst_net, r_proto, r_port) in enumerate(rules):
        if src_net != "any" and s not in ipaddress.ip_network(src_net):
            continue
        if dst_net != "any" and d not in ipaddress.ip_network(dst_net):
            continue
        if r_proto != "any" and r_proto != proto:
            continue
        if r_port is not None and r_port != port:
            continue
        return action, i
    return default, None


def shadowed_rules(rules: list[Rule]) -> list[int]:
    """Indices of rules that can never match because an earlier rule covers them entirely."""
    def covers(a: Rule, b: Rule) -> bool:
        def net_covers(x: str, y: str) -> bool:
            return x == "any" or (y != "any" and ipaddress.ip_network(y).subnet_of(ipaddress.ip_network(x)))
        return (net_covers(a[1], b[1]) and net_covers(a[2], b[2])
                and (a[3] == "any" or a[3] == b[3]) and (a[4] is None or a[4] == b[4]))
    return [j for j in range(len(rules)) if any(covers(rules[i], rules[j]) for i in range(j))]


# ---------------------------------------------------------------- CS-10 Unix permission audit


def symbolic(mode: int) -> str:
    """Render permission bits like `ls -l` (without the file-type character), e.g. 0o4755 -> 'rwsr-xr-x'."""
    return stat.filemode(stat.S_IFREG | mode)[1:]


def permission_findings(path: str, mode: int, *, secret: bool = False) -> list[str]:
    """Flag risky permission bits. `secret=True` for keys, .env files, databases with personal data."""
    findings = []
    if mode & stat.S_IWOTH:
        findings.append(f"{path}: world-writable")
    if mode & stat.S_ISUID:
        findings.append(f"{path}: setuid bit set (review whether it is needed)")
    if mode & stat.S_ISGID:
        findings.append(f"{path}: setgid bit set (review whether it is needed)")
    if secret and mode & (stat.S_IRWXG | stat.S_IRWXO):
        findings.append(f"{path}: secret readable or writable by group/others (expected 600 or stricter)")
    return findings


def audit_tree(root: str, secret_names: tuple[str, ...] = (".env", "id_rsa", "id_ed25519", ".pem", ".key", ".db")) -> list[str]:
    """Walk a directory you own and report permission findings (does not follow symlinks)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in dirnames + filenames:
            full = os.path.join(dirpath, name)
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                continue
            is_secret = any(name == s or name.endswith(s) for s in secret_names)
            out.extend(permission_findings(os.path.relpath(full, root), stat.S_IMODE(st.st_mode), secret=is_secret))
    return sorted(out)


# ---------------------------------------------------------------- CS-11 web application defences


def render_comment(author: str, text: str) -> str:
    """Output-encode untrusted data for an HTML element context (prevents stored/reflected XSS)."""
    return f"<p><b>{html.escape(author)}</b>: {html.escape(text)}</p>"


def new_csrf_token() -> str:
    return secrets.token_urlsafe(32)


def csrf_ok(session_token: str | None, submitted: str | None) -> bool:
    """Synchronizer-token check: the form value must equal the token stored in the server session."""
    return bool(session_token) and bool(submitted) and hmac.compare_digest(session_token, submitted)


def safe_redirect(target: str, allowed_hosts: set[str], fallback: str = "/") -> str:
    """Allow relative paths and allow-listed hosts only (prevents open redirects)."""
    parts = urlsplit(target)
    if target.startswith("//") or "\\" in target:
        return fallback
    if not parts.scheme and not parts.netloc and target.startswith("/"):
        return target
    if parts.scheme == "https" and parts.hostname in allowed_hosts:
        return target
    return fallback


RECOMMENDED_HEADERS = {
    "strict-transport-security": "enforce HTTPS (HSTS)",
    "content-security-policy": "restrict script sources (XSS mitigation)",
    "x-content-type-options": "stop MIME sniffing (should be nosniff)",
    "referrer-policy": "limit referrer leakage",
}


def header_findings(headers: dict[str, str]) -> list[str]:
    """Review HTTP response headers (names are case-insensitive) and cookie flags."""
    h = {k.lower(): v for k, v in headers.items()}
    findings = [f"missing {name}: {why}" for name, why in RECOMMENDED_HEADERS.items() if name not in h]
    if h.get("x-content-type-options", "nosniff").lower() != "nosniff":
        findings.append("x-content-type-options should be nosniff")
    csp = h.get("content-security-policy", "")
    if "'unsafe-inline'" in csp or "script-src *" in csp:
        findings.append("content-security-policy allows inline or any-origin scripts")
    if "frame-ancestors" not in csp and "x-frame-options" not in h:
        findings.append("no clickjacking protection (CSP frame-ancestors or X-Frame-Options)")
    if "server" in h and any(ch.isdigit() for ch in h["server"]):
        findings.append("server header discloses a version")
    cookie = h.get("set-cookie")
    if cookie:
        flags = {p.strip().split("=")[0].lower() for p in cookie.split(";")[1:]}
        for flag in ("secure", "httponly", "samesite"):
            if flag not in flags:
                findings.append(f"session cookie missing {flag}")
    return findings


# ---------------------------------------------------------------- CS-12 SQL injection: unsafe vs safe
# Local, in-memory training database only. The unsafe function exists to be studied and tested.


def demo_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, role TEXT);
        INSERT INTO users (username, role) VALUES ('amina', 'student'), ('juma', 'technician'),
                                                  ('mrs_k', 'warden'), ('o''brien', 'student');
    """)
    return conn


def find_user_UNSAFE(conn: sqlite3.Connection, username: str) -> list[tuple]:
    """INSECURE (string formatting builds SQL from input). For the injection demonstration only."""
    return conn.execute(f"SELECT id, username, role FROM users WHERE username = '{username}'").fetchall()


def find_user(conn: sqlite3.Connection, username: str) -> list[tuple]:
    """Parameterised query: the driver sends the value separately from the SQL text."""
    return conn.execute("SELECT id, username, role FROM users WHERE username = ?", (username,)).fetchall()


SORTABLE = {"username": "username", "role": "role", "id": "id"}


def list_users(conn: sqlite3.Connection, sort: str = "id", descending: bool = False,
               name_contains: str = "") -> list[tuple]:
    """Identifiers can't be parameters, so map them through an allow-list; escape LIKE wildcards."""
    column = SORTABLE.get(sort)
    if column is None:
        raise ValueError(f"cannot sort by {sort!r}")
    pattern = "%" + name_contains.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
    sql = (f"SELECT id, username, role FROM users WHERE username LIKE ? ESCAPE '\\' "
           f"ORDER BY {column} {'DESC' if descending else 'ASC'}")
    return conn.execute(sql, (pattern,)).fetchall()


# ---------------------------------------------------------------- CS-13 phishing-link red flags


def edit_distance(a: str, b: str) -> int:
    """Levenshtein distance (dynamic programming), used to spot lookalike domains."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def url_red_flags(url: str, trusted: set[str]) -> list[str]:
    """Heuristic warnings for a link. Absence of flags does NOT prove a link is safe."""
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    flags = []
    if parts.scheme != "https":
        flags.append("not https")
    if "@" in parts.netloc:
        flags.append("userinfo '@' in URL hides the real host")
    try:
        ipaddress.ip_address(host)
        flags.append("raw IP address instead of a domain")
    except ValueError:
        pass
    if host.startswith("xn--") or ".xn--" in host:
        flags.append("punycode (possible homograph) domain")
    if host in trusted or any(host.endswith("." + t) for t in trusted):
        return flags
    for t in trusted:
        if t in host:
            flags.append(f"contains trusted name {t!r} but is a different domain")
        elif edit_distance(host, t) <= 2:
            flags.append(f"lookalike of {t!r}")
    return flags
