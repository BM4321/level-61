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
