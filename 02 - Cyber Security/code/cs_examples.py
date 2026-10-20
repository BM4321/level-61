"""Runnable, tested versions of code shown in the Cyber Security lessons (ITT06102).

Defensive teaching code. Standard library only (Python 3.10+).
"""
import base64
import hashlib
import html
import hmac
import ipaddress
import json
import math
import os
import re
import secrets
import shutil
import sqlite3
import stat
import struct
import time
from collections import Counter
from datetime import datetime, timedelta
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


# ---------------------------------------------------------------- CS-14 defensive detection helpers


def shannon_entropy(data: bytes) -> float:
    """Bits per byte (0..8). Packed or encrypted content tends towards 8; text is usually 4-5."""
    if not data:
        return 0.0
    n = len(data)
    return -sum(c / n * math.log2(c / n) for c in Counter(data).values())


def sha256_file(path: str, chunk: int = 65536) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def ioc_hash_matches(root: str, bad_hashes: set[str]) -> list[str]:
    """Relative paths of files whose SHA-256 is on an indicator-of-compromise list."""
    hits = []
    for dirpath, _dirs, files in os.walk(root):
        for name in files:
            full = os.path.join(dirpath, name)
            if not os.path.islink(full) and sha256_file(full) in bad_hashes:
                hits.append(os.path.relpath(full, root))
    return sorted(hits)


def rule_matches(data: bytes, rules: dict[str, dict]) -> list[str]:
    """A tiny YARA-like matcher: a rule fires when at least `min` of its byte strings occur."""
    fired = []
    for name, rule in rules.items():
        found = sum(1 for s in rule["strings"] if s in data)
        if found >= rule.get("min", len(rule["strings"])):
            fired.append(name)
    return sorted(fired)


# ---------------------------------------------------------------- CS-15 log analysis (constructed sample log)

_AUTH = re.compile(
    r"^(?P<ts>\S+) host=(?P<host>\S+) sshd\[\d+\]: (?P<result>Accepted|Failed) (?P<method>password|publickey) "
    r"for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+) port \d+")
_SUDO = re.compile(r"^(?P<ts>\S+) host=(?P<host>\S+) sudo: (?P<user>\S+) : .*COMMAND=(?P<command>.+)$")


def parse_auth_log(lines) -> list[dict]:
    """Turn sshd/sudo lines into event dicts; unparseable lines are skipped (count them in real use)."""
    events = []
    for line in lines:
        line = line.rstrip("\n")
        if m := _AUTH.match(line):
            e = m.groupdict()
            e["kind"] = "login_" + e.pop("result").lower()
            e["invalid_user"] = "invalid user" in line
        elif m := _SUDO.match(line):
            e = m.groupdict()
            e["kind"] = "sudo"
        else:
            continue
        e["ts"] = datetime.fromisoformat(e["ts"].replace("Z", "+00:00"))
        events.append(e)
    return events


def failure_bursts(events: list[dict], threshold: int = 5, window: timedelta = timedelta(minutes=2)) -> dict[str, int]:
    """Source IPs with >= threshold failed logins inside any sliding window -> max count in a window."""
    by_ip: dict[str, list[datetime]] = {}
    for e in events:
        if e["kind"] == "login_failed":
            by_ip.setdefault(e["ip"], []).append(e["ts"])
    out = {}
    for ip, times in by_ip.items():
        times.sort()
        best, start = 0, 0
        for end in range(len(times)):
            while times[end] - times[start] > window:
                start += 1
            best = max(best, end - start + 1)
        if best >= threshold:
            out[ip] = best
    return out


def success_after_failures(events: list[dict], min_failures: int = 3) -> list[tuple[str, str, datetime]]:
    """(user, ip, time) for successful logins preceded by >= min_failures consecutive failures from that IP."""
    streak: dict[str, int] = {}
    hits = []
    for e in sorted((e for e in events if e["kind"].startswith("login_")), key=lambda e: e["ts"]):
        if e["kind"] == "login_failed":
            streak[e["ip"]] = streak.get(e["ip"], 0) + 1
        else:
            if streak.get(e["ip"], 0) >= min_failures:
                hits.append((e["user"], e["ip"], e["ts"]))
            streak[e["ip"]] = 0
    return hits


# ---------------------------------------------------------------- CS-16 risk calculations


def ale(asset_value: float, exposure_factor: float, aro: float) -> tuple[float, float]:
    """Quantitative risk: SLE = AV x EF; ALE = SLE x ARO. Returns (SLE, ALE)."""
    if not 0 <= exposure_factor <= 1 or aro < 0 or asset_value < 0:
        raise ValueError("need AV >= 0, 0 <= EF <= 1, ARO >= 0")
    sle = asset_value * exposure_factor
    return sle, sle * aro


def control_value(ale_before: float, ale_after: float, annual_cost: float) -> float:
    """Annual net benefit of a control (positive = financially justified)."""
    return ale_before - ale_after - annual_cost


def risk_rating(likelihood: int, impact: int) -> tuple[int, str]:
    """5x5 qualitative matrix: score = L x I; bands Low 1-4, Medium 5-9, High 10-16, Critical 20-25."""
    if likelihood not in range(1, 6) or impact not in range(1, 6):
        raise ValueError("likelihood and impact must be 1..5")
    score = likelihood * impact
    band = "Low" if score <= 4 else "Medium" if score <= 9 else "High" if score <= 16 else "Critical"
    return score, band


# ---------------------------------------------------------------- CS-17 evidence handling (teaching model)


def _entry_hash(entry: dict) -> str:
    body = {k: v for k, v in entry.items() if k != "entry_hash"}
    return hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()


def custody_append(log: list[dict], action: str, item: str, sha256: str, person: str, when: str) -> dict:
    """Append a hash-chained chain-of-custody entry (tamper-evident, not tamper-proof)."""
    entry = {"seq": len(log), "when": when, "person": person, "action": action, "item": item,
             "sha256": sha256, "prev": log[-1]["entry_hash"] if log else "0" * 64}
    entry["entry_hash"] = _entry_hash(entry)
    log.append(entry)
    return entry


def custody_problems(log: list[dict]) -> list[str]:
    """Check the chain links, entry hashes, and that the evidence hash never changes for an item."""
    problems, first_hash = [], {}
    for i, e in enumerate(log):
        if e["seq"] != i:
            problems.append(f"entry {i}: sequence number {e['seq']}")
        if e["prev"] != (log[i - 1]["entry_hash"] if i else "0" * 64):
            problems.append(f"entry {i}: broken link to previous entry")
        if e["entry_hash"] != _entry_hash(e):
            problems.append(f"entry {i}: entry altered after recording")
        if first_hash.setdefault(e["item"], e["sha256"]) != e["sha256"]:
            problems.append(f"entry {i}: evidence hash changed for {e['item']}")
    return problems


def acquire_copy(src: str, dst: str) -> tuple[str, str]:
    """Copy a file, hash source and copy, make the copy read-only. Returns (source_hash, copy_hash)."""
    h_src = sha256_file(src)
    shutil.copy2(src, dst)
    os.chmod(dst, 0o444)
    return h_src, sha256_file(dst)


# ---------------------------------------------------------------- CS-18 CVSS v3.1 base score
# Implements the base-score equations of the FIRST CVSS v3.1 specification (section 7).
_CVSS_W = {
    "AV": {"N": 0.85, "A": 0.62, "L": 0.55, "P": 0.2},
    "AC": {"L": 0.77, "H": 0.44},
    "UI": {"N": 0.85, "R": 0.62},
    "CIA": {"H": 0.56, "L": 0.22, "N": 0.0},
}
_CVSS_PR = {"U": {"N": 0.85, "L": 0.62, "H": 0.27}, "C": {"N": 0.85, "L": 0.68, "H": 0.5}}


def _roundup(x: float) -> float:
    """CVSS v3.1 Roundup: smallest one-decimal number >= x, robust to floating-point error."""
    i = round(x * 100000)
    return i / 100000.0 if i % 10000 == 0 else (math.floor(i / 10000) + 1) / 10.0


def cvss31_base(vector: str) -> tuple[float, str]:
    """'CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H' -> (9.8, 'Critical')."""
    parts = vector.split("/")
    if parts[0] != "CVSS:3.1":
        raise ValueError("expected a CVSS:3.1 vector")
    m = dict(p.split(":") for p in parts[1:])
    required = ["AV", "AC", "PR", "UI", "S", "C", "I", "A"]
    if sorted(m) != sorted(required):
        raise ValueError(f"vector must contain exactly {required}")
    s = m["S"]
    iss = 1 - (1 - _CVSS_W["CIA"][m["C"]]) * (1 - _CVSS_W["CIA"][m["I"]]) * (1 - _CVSS_W["CIA"][m["A"]])
    impact = 6.42 * iss if s == "U" else 7.52 * (iss - 0.029) - 3.25 * (iss - 0.02) ** 15
    exploit = 8.22 * _CVSS_W["AV"][m["AV"]] * _CVSS_W["AC"][m["AC"]] * _CVSS_PR[s][m["PR"]] * _CVSS_W["UI"][m["UI"]]
    if impact <= 0:
        score = 0.0
    elif s == "U":
        score = _roundup(min(impact + exploit, 10))
    else:
        score = _roundup(min(1.08 * (impact + exploit), 10))
    rating = ("None" if score == 0 else "Low" if score < 4 else "Medium" if score < 7
              else "High" if score < 9 else "Critical")
    return score, rating


# ---------------------------------------------------------------- CS-19 privacy and cloud configuration helpers


def pseudonymise(identifier: str, key: bytes) -> str:
    """Keyed pseudonym (HMAC-SHA256, truncated). Re-identifiable by whoever holds the key: still personal data."""
    return hmac.new(key, identifier.encode("utf-8"), hashlib.sha256).hexdigest()[:16]


def k_anonymity(rows: list[dict], quasi_identifiers: list[str]) -> int:
    """Smallest group size when rows are grouped by their quasi-identifier values (higher = harder to single out)."""
    if not rows:
        return 0
    groups = Counter(tuple(r[q] for q in quasi_identifiers) for r in rows)
    return min(groups.values())


def storage_policy_findings(bucket: dict) -> list[str]:
    """Review a simplified object-storage configuration (cloud-provider-neutral teaching model)."""
    f = []
    if bucket.get("public_read") or "*" in bucket.get("readers", []):
        f.append("objects readable by anyone on the Internet")
    if not bucket.get("encryption_at_rest", False):
        f.append("encryption at rest disabled")
    if not bucket.get("versioning", False):
        f.append("versioning disabled (no recovery from overwrite or ransomware)")
    if not bucket.get("access_logging", False):
        f.append("access logging disabled")
    if bucket.get("contains_personal_data") and bucket.get("region") not in bucket.get("approved_regions", []):
        f.append("personal data stored outside approved regions")
    return f
