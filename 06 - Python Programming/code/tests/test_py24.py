import pytest

from _target import load

m = load("py24")


@pytest.mark.parametrize("raw, ok", [("Amina_1", "amina_1"), ("  bob ", "bob")])
def test_username_ok(raw, ok):
    assert m.validate_username(raw) == ok


@pytest.mark.parametrize("bad", ["ab", "1abc", "bob; rm -rf", "a" * 21, "名前abc", "bo b", ""])
def test_username_bad(bad):
    with pytest.raises(ValueError):
        m.validate_username(bad)


def test_module_code():
    assert m.validate_module_code(" cst06102 ") == "CST06102"
    for bad in ("CST0610", "CST06102; DROP", "CS106102", "CST٠٦١٠٢"):
        with pytest.raises(ValueError):
            m.validate_module_code(bad)


def test_safe_path(tmp_path):
    base = tmp_path / "uploads"
    base.mkdir()
    assert m.safe_path(base, "report.pdf") == (base / "report.pdf").resolve()
    assert m.safe_path(base, "sub/../ok.txt") == (base / "ok.txt").resolve()
    for bad in ("../secret.txt", "/etc/passwd", "a/../../x"):
        with pytest.raises(ValueError):
            m.safe_path(base, bad)


def test_password_hashing():
    stored = m.hash_password("correct horse", iterations=1000)
    assert stored.startswith("pbkdf2_sha256$1000$")
    assert m.verify_password("correct horse", stored)
    assert not m.verify_password("Correct horse", stored)
    assert m.hash_password("same", 1000) != m.hash_password("same", 1000)  # salted
    with pytest.raises(ValueError):
        m.verify_password("x", "md5$1$00$00")


def test_token():
    a, b = m.new_token(), m.new_token()
    assert a != b and len(a) >= 43


def test_ping_command():
    assert m.ping_command("example.org") == ["ping", "-c", "1", "example.org"]
    for bad in ("8.8.8.8; cat /etc/passwd", "$(reboot)", "", "a b"):
        with pytest.raises(ValueError):
            m.ping_command(bad)


def test_redact():
    assert m.redact("login user=amina password=Hunter2! token=abc123&x=1") == \
        "login user=amina password=[REDACTED] token=[REDACTED]&x=1"
    assert m.redact("card 4111 1111 1111 1234 ok") == "card **** **** **** 1234 ok"
    assert "\n" not in m.redact("user=x\nFAKE admin login OK")


def test_reserved():
    with pytest.raises(ValueError):
        m.validate_username_reserved("ADMIN")
    assert m.validate_username_reserved("amina") == "amina"
