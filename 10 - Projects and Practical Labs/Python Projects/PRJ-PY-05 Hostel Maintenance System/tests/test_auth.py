import logging

import pytest

from conftest import PW
from hostel.errors import AuthError, ThrottledError, ValidationError
from hostel.models import Role
from hostel.security import PasswordHasher, password_problems
from hostel.services import AuthService, login_delay


def test_password_policy():
    assert password_problems("short") == ["use at least 15 characters"]
    assert password_problems("passwordpassword") == ["this password is too common"]
    assert password_problems("my-University X-pass", ["University X", "hostel"]) == ["don't include 'University X'"]
    assert password_problems("lantern-quiet-river-7", ["University X", "hostel"]) == []


def test_register_rejects_weak_and_personal_passwords(world):
    auth = world["auth"]
    with pytest.raises(ValidationError, match="15 characters"):
        auth.register("STU/21/0009", "Faraji Resident", Role.RESIDENT, "tooShort1", "A-101")
    with pytest.raises(ValidationError, match="Faraji"):
        auth.register("STU/21/0009", "Faraji Resident", Role.RESIDENT, "faraji-loves-the-sea", "A-101")
    with pytest.raises(ValidationError, match="room"):
        auth.register("STU/21/0009", "Faraji Resident", Role.RESIDENT, "lantern-quiet-river-7")


def test_hash_format_and_verify(hasher):
    h = hasher.hash("lantern-quiet-river-7")
    assert h.startswith("scrypt$1024$8$1$") and "lantern" not in h
    assert hasher.verify("lantern-quiet-river-7", h) and not hasher.verify("lantern-quiet-river-8", h)
    assert hasher.hash("same-password-twice") != hasher.hash("same-password-twice")      # random salts
    assert not hasher.verify("x", "md5$abc")


def test_login_success_failure_and_generic_message(world, caplog):
    auth = world["auth"]
    assert auth.authenticate("stu/21/0001", PW["STU/21/0001"]).name == "Baraka Resident"
    with caplog.at_level(logging.WARNING):
        with pytest.raises(AuthError) as wrong:
            auth.authenticate("STU/21/0001", "wrong-password-guess")
    with pytest.raises(AuthError) as unknown:
        auth.authenticate("NOBODY99", "wrong-password-guess")
    assert str(wrong.value) == str(unknown.value) == "invalid registration number or password"
    assert "wrong-password-guess" not in caplog.text and "STU/21/0001" in caplog.text


def test_backoff_schedule():
    assert [login_delay(n) for n in range(10)] == [0, 0, 0, 30, 60, 120, 240, 480, 900, 900]


def test_throttling_with_fake_clock(world):
    auth, clock = world["auth"], world["clock"]
    for _ in range(3):
        with pytest.raises(AuthError):
            auth.authenticate("TECH01", "not-the-password")
    with pytest.raises(ThrottledError) as t:
        auth.authenticate("TECH01", PW["TECH01"])          # even the right password must wait
    assert t.value.retry_after == 30
    clock.advance(seconds=31)
    with pytest.raises(AuthError):
        auth.authenticate("TECH01", "still-not-it-sorry")  # 4th failure -> 60 s
    clock.advance(seconds=59)
    with pytest.raises(ThrottledError) as t:
        auth.authenticate("TECH01", PW["TECH01"])
    assert t.value.retry_after == 1
    clock.advance(seconds=1)
    assert auth.authenticate("TECH01", PW["TECH01"]).reg_no == "TECH01"
    assert world["repo"].login_state("TECH01") == (0, None)


def test_rehash_on_login_when_parameters_change(world, clock):
    repo = world["repo"]
    old = repo.get_user("TECH02").password_hash
    stronger = AuthService(repo, PasswordHasher(n=2**11), clock)
    stronger.authenticate("TECH02", PW["TECH02"])
    new = repo.get_user("TECH02").password_hash
    assert old.startswith("scrypt$1024$") and new.startswith("scrypt$2048$")


def test_password_reset(world):
    auth, clock = world["auth"], world["clock"]
    assert auth.issue_reset("NOBODY99") is None
    token = auth.issue_reset("STU/21/0002")
    assert token and len(token) >= 43                       # 32 random bytes, base64url
    with pytest.raises(ValidationError):
        auth.reset_password(token, "weak")                  # rejected before the token is used
    auth.reset_password(token, "orchid-thunder-basket-3")
    assert auth.authenticate("STU/21/0002", "orchid-thunder-basket-3")
    with pytest.raises(AuthError):
        auth.reset_password(token, "another-fine-passphrase")   # single use
    late = auth.issue_reset("STU/21/0002")
    clock.advance(minutes=31)
    with pytest.raises(AuthError):
        auth.reset_password(late, "another-fine-passphrase")    # expired
