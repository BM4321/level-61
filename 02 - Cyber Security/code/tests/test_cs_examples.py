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
