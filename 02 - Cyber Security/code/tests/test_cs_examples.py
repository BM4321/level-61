import hashlib

import pytest

from cs_examples import Forbidden, authorize, hotp, totp, verify_totp

KEY = b"12345678901234567890"   # RFC test key


def test_hotp_rfc4226_vectors():
    expected = ["755224", "287082", "359152", "969429", "338314", "254676", "287922", "162583", "399871", "520489"]
    assert [hotp(KEY, c) for c in range(10)] == expected


@pytest.mark.parametrize("t, code", [(59, "94287082"), (1111111109, "07081804"), (1111111111, "14050471"),
                                     (1234567890, "89005924"), (2000000000, "69279037"), (20000000000, "65353130")])
def test_totp_rfc6238_sha1_vectors(t, code):
    assert totp(KEY, at=t, digits=8) == code


def test_verify_window():
    code = totp(KEY, at=1000)
    assert verify_totp(KEY, code, at=1000) and verify_totp(KEY, code, at=1030)  # next step (34) is inside window=1
    assert not verify_totp(KEY, code, at=1059)  # step 35: two steps away
    assert not verify_totp(KEY, code, at=1000 + 120)


AMINA = {"id": "amina", "role": "student"}
BARAKA_REQ = {"id": 18, "reporter": "baraka", "technician": "juma"}
AMINA_REQ = {"id": 17, "reporter": "amina", "technician": "juma"}
JUMA = {"id": "juma", "role": "technician"}
OTHER_TECH = {"id": "neema", "role": "technician"}
WARDEN = {"id": "mrs_k", "role": "warden"}


@pytest.mark.parametrize("user, action, req, allowed", [
    (AMINA, "view_request", AMINA_REQ, True), (AMINA, "view_request", BARAKA_REQ, False),
    (JUMA, "view_request", BARAKA_REQ, True), (OTHER_TECH, "view_request", BARAKA_REQ, False),
    (WARDEN, "view_request", BARAKA_REQ, True), (JUMA, "update_status", BARAKA_REQ, True),
    (OTHER_TECH, "update_status", BARAKA_REQ, False), (AMINA, "update_status", AMINA_REQ, False),
    (WARDEN, "assign_technician", None, True), (AMINA, "assign_technician", None, False),
    ({"id": "x", "role": "hacker"}, "view_request", AMINA_REQ, False), (WARDEN, "delete_everything", None, False),
])
def test_authorize_matrix(user, action, req, allowed):
    if allowed:
        authorize(user, action, req)
    else:
        with pytest.raises(Forbidden):
            authorize(user, action, req)


# --- CS-07 toy RSA / Diffie-Hellman numbers (teaching values only; never use small keys) ---

def test_cs07_toy_rsa_worked_example():
    p, q, e = 61, 53, 17
    n, phi = p * q, (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    assert (n, phi, d) == (3233, 3120, 2753)
    c = pow(65, e, n)
    assert c == 2790 and pow(c, d, n) == 65


def test_cs07_practice3_rsa():
    n, phi, e = 11 * 13, 10 * 12, 7
    d = pow(e, -1, phi)
    assert (n, phi, d) == (143, 120, 103)
    assert pow(9, e, n) == 48 and pow(48, d, n) == 9


def test_cs07_diffie_hellman():
    p, g = 23, 5
    A, B = pow(g, 6, p), pow(g, 15, p)
    assert (A, B) == (8, 19) and pow(B, 6, p) == pow(A, 15, p) == 2
    A, B = pow(g, 4, p), pow(g, 3, p)
    assert (A, B) == (4, 10) and pow(B, 4, p) == pow(A, 3, p) == 18


# --- CS-08 password storage (small scrypt cost so the tests stay fast) ---
from cs_examples import hash_password, needs_rehash, password_problems, verify_password  # noqa: E402

FAST = {"n": 2 ** 10, "r": 8, "p": 1}


def test_hash_and_verify_roundtrip():
    stored = hash_password("correct horse battery staple", **FAST)
    assert stored.startswith("scrypt$1024$8$1$")
    assert verify_password("correct horse battery staple", stored)
    assert not verify_password("Correct horse battery staple", stored)


def test_salt_makes_equal_passwords_differ():
    assert hash_password("same", **FAST) != hash_password("same", **FAST)
    fixed = bytes(16)
    assert hash_password("same", salt=fixed, **FAST) == hash_password("same", salt=fixed, **FAST)


def test_malformed_or_foreign_hash_rejected():
    assert not verify_password("x", "not-a-hash")
    assert not verify_password("x", "md5$1$1$1$AA==$AA==")


def test_needs_rehash():
    weak = hash_password("pw", **FAST)
    assert needs_rehash(weak)
    assert not needs_rehash(weak, **FAST)
    assert needs_rehash("legacy-sha1-hex")


def test_default_parameters_work():
    stored = hash_password("pw")
    assert verify_password("pw", stored) and not needs_rehash(stored)


def test_password_problems():
    block = {"password123456789", "qwertyuiopasdfgh"}
    assert password_problems("Tr0ub4dor&3", block) == ["shorter than 15 characters"]
    assert password_problems("Password123456789", block) == ["appears in the blocklist of common or breached passwords"]
    assert password_problems("ndizi mbili chai moto asubuhi", block) == []
    assert password_problems("a" * 65, set()) == ["longer than 64 characters"]


def test_pbkdf2_and_fast_hash_values_quoted_in_cs08():
    assert hashlib.sha256(b"password123").hexdigest().startswith("ef92b778bafe771e")
    assert hashlib.md5(b"password123").hexdigest() == "482c811da5d5b4bc6d497ffa98491e38"
    assert hashlib.pbkdf2_hmac("sha256", b"password", b"salt", 4096).hex().startswith("c5e478d59288c841")


# --- CS-09 packet filter model ---
from cs_examples import match_rule, shadowed_rules  # noqa: E402

HOSTEL_RULES = [
    ("allow", "any", "10.0.1.10/32", "tcp", 443),        # 0 public HTTPS to web server
    ("allow", "10.0.1.10/32", "10.0.2.20/32", "tcp", 5432),  # 1 web -> database only
    ("allow", "10.0.9.0/24", "10.0.0.0/16", "tcp", 22),   # 2 admin VLAN SSH
    ("deny", "any", "any", "any", None),                  # 3 explicit deny all
]


@pytest.mark.parametrize("src, dst, proto, port, expected", [
    ("41.59.1.2", "10.0.1.10", "tcp", 443, ("allow", 0)),
    ("41.59.1.2", "10.0.2.20", "tcp", 5432, ("deny", 3)),
    ("10.0.1.10", "10.0.2.20", "tcp", 5432, ("allow", 1)),
    ("10.0.9.5", "10.0.2.20", "tcp", 22, ("allow", 2)),
    ("10.0.3.7", "10.0.2.20", "tcp", 22, ("deny", 3)),
    ("41.59.1.2", "10.0.1.10", "udp", 443, ("deny", 3)),
])
def test_first_match(src, dst, proto, port, expected):
    assert match_rule(HOSTEL_RULES, src, dst, proto, port) == expected


def test_default_deny_without_explicit_rule():
    assert match_rule(HOSTEL_RULES[:1], "41.59.1.2", "10.0.1.11", "tcp", 443) == ("deny", None)


def test_shadowed_rules():
    rules = [("allow", "10.0.0.0/16", "any", "tcp", None),
             ("deny", "10.0.5.0/24", "any", "tcp", 23),   # shadowed: rule 0 already allows it
             ("deny", "any", "any", "any", None),
             ("allow", "any", "any", "tcp", 443)]          # shadowed by the deny-all
    assert shadowed_rules(rules) == [1, 3]
    assert shadowed_rules(HOSTEL_RULES) == []


# --- CS-10 permission audit ---
import os  # noqa: E402
import sys  # noqa: E402

from cs_examples import audit_tree, permission_findings, symbolic  # noqa: E402


@pytest.mark.parametrize("mode, text", [(0o644, "rw-r--r--"), (0o600, "rw-------"), (0o755, "rwxr-xr-x"),
                                        (0o4755, "rwsr-xr-x"), (0o777, "rwxrwxrwx"), (0o1777, "rwxrwxrwt"),
                                        (0o640, "rw-r-----")])
def test_symbolic(mode, text):
    assert symbolic(mode) == text


def test_permission_findings():
    assert permission_findings("a", 0o644) == []
    assert permission_findings("a", 0o666) == ["a: world-writable"]
    assert permission_findings(".env", 0o640, secret=True) == [".env: secret readable or writable by group/others (expected 600 or stricter)"]
    assert permission_findings(".env", 0o600, secret=True) == []
    assert permission_findings("bin", 0o4755) == ["bin: setuid bit set (review whether it is needed)"]


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission bits")
def test_audit_tree(tmp_path):
    (tmp_path / "app.py").write_text("print('hi')\n")
    (tmp_path / ".env").write_text("DEMO_ONLY=1\n")
    (tmp_path / "upload").mkdir()
    os.chmod(tmp_path / "app.py", 0o644)
    os.chmod(tmp_path / ".env", 0o644)
    os.chmod(tmp_path / "upload", 0o777)
    assert audit_tree(str(tmp_path)) == [
        ".env: secret readable or writable by group/others (expected 600 or stricter)",
        "upload: world-writable",
    ]
    os.chmod(tmp_path / ".env", 0o600)
    os.chmod(tmp_path / "upload", 0o750)
    assert audit_tree(str(tmp_path)) == []


# --- CS-11 web defences ---
from cs_examples import csrf_ok, header_findings, new_csrf_token, render_comment, safe_redirect  # noqa: E402


def test_render_comment_escapes():
    out = render_comment("amina", '<script>alert("x")</script>')
    assert out == "<p><b>amina</b>: &lt;script&gt;alert(&quot;x&quot;)&lt;/script&gt;</p>"
    assert "<script>" not in render_comment("<img src=x onerror=alert(1)>", "hi")


def test_csrf():
    t = new_csrf_token()
    assert len(t) >= 43 and csrf_ok(t, t)
    assert not csrf_ok(t, new_csrf_token()) and not csrf_ok(t, None) and not csrf_ok(None, None) and not csrf_ok("", "")


@pytest.mark.parametrize("target, expected", [
    ("/requests/17", "/requests/17"),
    ("https://hostel.example.ac.tz/home", "https://hostel.example.ac.tz/home"),
    ("https://evil.example/phish", "/"),
    ("//evil.example/phish", "/"),
    ("http://hostel.example.ac.tz/", "/"),
    ("javascript:alert(1)", "/"),
    ("/\\evil.example", "/"),
    ("https://hostel.example.ac.tz.evil.example/", "/"),
])
def test_safe_redirect(target, expected):
    assert safe_redirect(target, {"hostel.example.ac.tz"}) == expected


def test_header_findings_bad_and_good():
    bad = {"Server": "Apache/2.4.41", "Content-Type": "text/html",
           "Set-Cookie": "session=abc123; Path=/",
           "Content-Security-Policy": "script-src 'self' 'unsafe-inline'"}
    assert header_findings(bad) == [
        "missing strict-transport-security: enforce HTTPS (HSTS)",
        "missing x-content-type-options: stop MIME sniffing (should be nosniff)",
        "missing referrer-policy: limit referrer leakage",
        "content-security-policy allows inline or any-origin scripts",
        "no clickjacking protection (CSP frame-ancestors or X-Frame-Options)",
        "server header discloses a version",
        "session cookie missing secure",
        "session cookie missing httponly",
        "session cookie missing samesite",
    ]
    good = {"Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
            "X-Content-Type-Options": "nosniff", "Referrer-Policy": "strict-origin-when-cross-origin",
            "Set-Cookie": "session=abc123; Path=/; Secure; HttpOnly; SameSite=Lax"}
    assert header_findings(good) == []


# --- CS-12 SQL injection demo (in-memory database) ---
import sqlite3  # noqa: E402

from cs_examples import demo_db, find_user, find_user_UNSAFE, list_users  # noqa: E402


def test_unsafe_query_is_injectable():
    conn = demo_db()
    assert find_user_UNSAFE(conn, "amina") == [(1, "amina", "student")]
    assert len(find_user_UNSAFE(conn, "' OR '1'='1")) == 4            # returns every row
    with pytest.raises(sqlite3.OperationalError):
        find_user_UNSAFE(conn, "o'brien")                               # legitimate name breaks it


def test_parameterised_query_is_not():
    conn = demo_db()
    assert find_user(conn, "' OR '1'='1") == []
    assert find_user(conn, "o'brien") == [(4, "o'brien", "student")]
    find_user(conn, "x'; DROP TABLE users; --")
    assert conn.execute("SELECT COUNT(*) FROM users").fetchone() == (4,)


def test_sort_allow_list_and_like_escaping():
    conn = demo_db()
    assert [r[1] for r in list_users(conn, "username")] == ["amina", "juma", "mrs_k", "o'brien"]
    assert [r[1] for r in list_users(conn, "role", descending=True)][0] == "mrs_k"
    with pytest.raises(ValueError):
        list_users(conn, "id; DROP TABLE users")
    assert [r[1] for r in list_users(conn, name_contains="_")] == ["mrs_k"]   # literal underscore
    assert list_users(conn, name_contains="%") == []


# --- CS-13 phishing link heuristics ---
from cs_examples import edit_distance, url_red_flags  # noqa: E402

TRUSTED = {"chuo.example", "bankmfano.example"}  # fictional organisations on reserved .example names


def test_edit_distance():
    assert edit_distance("kitten", "sitting") == 3
    assert edit_distance("", "abc") == 3 and edit_distance("same", "same") == 0


@pytest.mark.parametrize("url, flags", [
    ("https://chuo.example/results", []),
    ("https://aris.chuo.example/login", []),
    ("http://chuo.example/", ["not https"]),
    ("https://chu0.example/login", ["lookalike of 'chuo.example'"]),
    ("https://chuo.example.verify-account.test/", ["contains trusted name 'chuo.example' but is a different domain"]),
    ("https://chuo.example@203.0.113.9/", ["userinfo '@' in URL hides the real host", "raw IP address instead of a domain"]),
    ("https://xn--bnkmfano-16g.example/", ["punycode (possible homograph) domain"]),
])
def test_url_red_flags(url, flags):
    assert url_red_flags(url, TRUSTED) == flags


# --- CS-14 detection helpers ---
from cs_examples import ioc_hash_matches, rule_matches, sha256_file, shannon_entropy  # noqa: E402


def test_entropy():
    assert shannon_entropy(b"") == 0.0
    assert shannon_entropy(b"aaaa") == 0.0
    assert shannon_entropy(b"abab") == 1.0
    assert shannon_entropy(bytes(range(256))) == 8.0
    assert 3.5 < shannon_entropy(b"The quick brown fox jumps over the lazy dog") < 4.5


def test_ioc_hash_matches(tmp_path):
    (tmp_path / "a.txt").write_bytes(b"harmless")
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "b.bin").write_bytes(b"pretend-indicator")
    bad = {hashlib.sha256(b"pretend-indicator").hexdigest()}
    assert ioc_hash_matches(str(tmp_path), bad) == [os.path.join("sub", "b.bin")]
    assert sha256_file(str(tmp_path / "a.txt")) == hashlib.sha256(b"harmless").hexdigest()


def test_rule_matches():
    rules = {
        "suspicious_macro": {"strings": [b"AutoOpen", b"Shell(", b"powershell -enc"], "min": 2},
        "ransom_note": {"strings": [b"your files have been encrypted", b"bitcoin"]},
    }
    assert rule_matches(b"Sub AutoOpen() Shell(\"calc\")", rules) == ["suspicious_macro"]
    assert rule_matches(b"Sub AutoOpen() MsgBox", rules) == []
    assert rule_matches(b"...your files have been encrypted... pay in bitcoin", rules) == ["ransom_note"]


# --- CS-15 log analysis on the constructed sample log ---
from datetime import timedelta  # noqa: E402
from pathlib import Path  # noqa: E402

from cs_examples import failure_bursts, parse_auth_log, success_after_failures  # noqa: E402

SAMPLE = Path(__file__).resolve().parent.parent / "data" / "auth_sample.log"


def _events():
    with open(SAMPLE, encoding="utf-8") as f:
        return parse_auth_log(f)


def test_parse_counts():
    ev = _events()
    assert len(ev) == 20
    kinds = [e["kind"] for e in ev]
    assert kinds.count("login_failed") == 16 and kinds.count("login_accepted") == 3 and kinds.count("sudo") == 1
    assert parse_auth_log(["garbage line", ""]) == []


def test_failure_bursts():
    ev = _events()
    assert failure_bursts(ev) == {"203.0.113.50": 7, "192.0.2.99": 5}
    slow = failure_bursts(ev, threshold=3, window=timedelta(hours=1))
    assert slow["198.51.100.23"] == 3          # slow guessing only visible with a wider window


def test_success_after_failures():
    hits = success_after_failures(_events())
    assert [(u, ip) for u, ip, _ in hits] == [("juma", "203.0.113.50")]
    assert hits[0][2].isoformat() == "2026-03-02T08:14:36+00:00"


# --- CS-16 risk calculations ---
from cs_examples import ale, control_value, risk_rating  # noqa: E402


def test_ale_examples():
    assert ale(40_000_000, 0.25, 0.5) == (10_000_000, 5_000_000)
    assert ale(40_000_000, 0.25, 0.1) == (10_000_000, 1_000_000)
    assert ale(2_500_000, 1.0, 3) == (2_500_000, 7_500_000)
    with pytest.raises(ValueError):
        ale(100, 1.5, 1)


def test_control_value():
    assert control_value(5_000_000, 1_000_000, 1_500_000) == 2_500_000
    assert control_value(5_000_000, 1_000_000, 6_000_000) == -2_000_000


@pytest.mark.parametrize("l, i, expected", [(1, 1, (1, "Low")), (2, 2, (4, "Low")), (1, 5, (5, "Medium")),
                                             (3, 3, (9, "Medium")), (2, 5, (10, "High")), (4, 4, (16, "High")),
                                             (4, 5, (20, "Critical")), (5, 5, (25, "Critical"))])
def test_risk_rating(l, i, expected):
    assert risk_rating(l, i) == expected


def test_cs16_sensitivity_and_practice_values():
    after = ale(40_000_000, 0.25, 0.1)[1]
    values = [control_value(ale(40_000_000, 0.25, a)[1], after, 1_500_000) for a in (0.2, 0.25, 0.5, 1.0)]
    assert values == [-500_000, 0, 2_500_000, 7_500_000]
    assert ale(12_000_000, 0.4, 0.25) == (4_800_000, 1_200_000)
    assert control_value(5_000_000, 0, 6_000_000) < 0     # package B never breaks even


# --- CS-17 chain of custody ---
from cs_examples import acquire_copy, custody_append, custody_problems  # noqa: E402


def _custody_log():
    log = []
    h = hashlib.sha256(b"exported-log-bytes").hexdigest()
    custody_append(log, "acquired", "EV-001 auth.log export", h, "Neema (ICT)", "2026-03-02T10:05Z")
    custody_append(log, "transferred", "EV-001 auth.log export", h, "Baraka (security officer)", "2026-03-02T10:40Z")
    custody_append(log, "examined", "EV-001 auth.log export", h, "Baraka (security officer)", "2026-03-02T13:15Z")
    return log


def test_custody_chain_ok():
    assert custody_problems(_custody_log()) == []


def test_custody_detects_tampering():
    log = _custody_log()
    log[1]["person"] = "Someone else"
    assert custody_problems(log) == ["entry 1: entry altered after recording"]
    log = _custody_log()
    custody_append(log, "examined", "EV-001 auth.log export", "f" * 64, "X", "2026-03-03T09:00Z")
    assert custody_problems(log) == ["entry 3: evidence hash changed for EV-001 auth.log export"]
    log = _custody_log()
    del log[1]
    assert "entry 1: broken link to previous entry" in custody_problems(log)


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permission bits")
def test_acquire_copy(tmp_path):
    src = tmp_path / "evidence.txt"
    src.write_bytes(b"line 1\nline 2\n")
    h1, h2 = acquire_copy(str(src), str(tmp_path / "copy.txt"))
    assert h1 == h2 == hashlib.sha256(b"line 1\nline 2\n").hexdigest()
    assert oct(os.stat(tmp_path / "copy.txt").st_mode & 0o777) == "0o444"


# --- CS-18 CVSS v3.1 ---
from cs_examples import cvss31_base  # noqa: E402


@pytest.mark.parametrize("vector, expected", [
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H", (9.8, "Critical")),
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N", (6.1, "Medium")),     # typical reflected XSS
    ("CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:N/A:N", (6.5, "Medium")),     # IDOR read by a logged-in user
    ("CVSS:3.1/AV:L/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:H", (7.8, "High")),       # local privilege escalation
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H", (7.5, "High")),       # remote DoS
    ("CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:N/A:N", (5.9, "Medium")),
    ("CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H", (10.0, "Critical")),
    ("CVSS:3.1/AV:P/AC:H/PR:H/UI:R/S:U/C:N/I:N/A:N", (0.0, "None")),
])
def test_cvss31(vector, expected):
    assert cvss31_base(vector) == expected


def test_cvss_rejects_bad_vectors():
    with pytest.raises(ValueError):
        cvss31_base("CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    with pytest.raises(ValueError):
        cvss31_base("CVSS:3.1/AV:N/AC:L")
