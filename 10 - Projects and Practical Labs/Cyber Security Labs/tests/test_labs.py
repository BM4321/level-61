"""Checks that every Cyber Security lab script runs and produces the outputs quoted in the lab notes."""
import sys

import pytest

import lab01_passwords
import lab02_integrity
import lab03_toy_ciphers
import lab04_permissions
import lab05_headers
import lab06_sqli
import lab07_threat_model
import lab08_log_analysis


def test_lab01(capsys):
    assert lab01_passwords.assess("password123") == "REJECT: on blocklist"
    assert lab01_passwords.assess("Tr0ub4dor&3") == "REJECT: shorter than 15"
    assert lab01_passwords.assess("ndizi mbili chai moto asubuhi") == "ACCEPT"
    assert round(lab01_passwords.naive_entropy_bits("Tr0ub4dor&3"), 1) == 72.3
    stored = lab01_passwords.hash_password("x", n=2 ** 10)
    assert lab01_passwords.verify_password("x", stored) and not lab01_passwords.verify_password("y", stored)
    lab01_passwords.main()
    out = capsys.readouterr().out
    assert "identical stored values? False" in out and "['amina', 'juma'] <- SAME PASSWORD" in out


def test_lab02(tmp_path, capsys):
    w = tmp_path / "ws"
    lab02_integrity.main(w)
    out = capsys.readouterr().out
    assert "27451312771f4b3cbdff237ac5d18be2a3814e4a37ebfef92c2e1651ba8f3c14  results_2026.csv" in out
    assert "results_2026.csv: FAILED" in out and "INVALID (tampering detected)" in out
    lab02_integrity.cleanup(w)
    assert not w.exists()


def test_lab03(capsys):
    ct = lab03_toy_ciphers.caesar("Meet the examinations officer", 7)
    assert lab03_toy_ciphers.break_caesar(ct * 3)[0] == 7
    lab03_toy_ciphers.main()
    out = capsys.readouterr().out
    assert "key 'chuo'" in out and "b'PAY NEEMA 900 TZ'" in out


@pytest.mark.skipif(sys.platform == "win32", reason="POSIX permissions")
def test_lab04(tmp_path, capsys):
    w = tmp_path / "ws"
    lab04_permissions.main(w)
    out = capsys.readouterr().out
    before, after = out.split("== Step 3")
    for needle in ("app/.env", "tools/report_tool", "backup.sh", "uploads", "app/notes.txt"):
        assert needle in before.split("== Step 2")[0]
    assert "shared_tmp" not in before          # sticky 1777 directory is not flagged
    assert "no findings" in after
    lab04_permissions.cleanup(w)
    assert not w.exists()


def test_lab05():
    assert len(lab05_headers.review(lab05_headers.fetch_headers(lab05_headers.INSECURE))) == 11
    assert lab05_headers.review(lab05_headers.fetch_headers(lab05_headers.HARDENED)) == []


def test_lab06():
    conn = lab06_sqli.build_db()
    assert lab06_sqli.login_vulnerable(conn, "x' OR '1'='1' --", "a")[1] is not None
    assert lab06_sqli.login_vulnerable(conn, "DEMO/STF/2019/0001' --", "a")[1] == ("Mrs K", "warden")
    assert len(lab06_sqli.my_requests_vulnerable(conn, "x' UNION SELECT 0, reg_no, pw_plain FROM users --")) == 3
    assert lab06_sqli.login_safe(conn, "demo/bit/2024/0117", "ndizi mbili chai moto") == ("Amina", "student")
    assert lab06_sqli.login_safe(conn, "DEMO/BIT/2024/0117", "wrong") is None
    with pytest.raises(lab06_sqli.ValidationError):
        lab06_sqli.login_safe(conn, "x' OR '1'='1' --", "a")
    assert len(lab06_sqli.my_requests_safe(conn, "DEMO/BIT/2024/0117")) == 2


def test_lab07():
    ws = lab07_threat_model.worksheet()
    assert "Total candidate threats: 38" in ws
    import re
    assert len(re.findall(r"^\| T\d\d \|", ws, re.M)) == 38 and "dmz → internal" in ws


def test_lab08(capsys):
    lab08_log_analysis.main(lab08_log_analysis.DEFAULT_LOG)
    out = capsys.readouterr().out
    assert "parsed 20 events, skipped 0" in out
    assert "D3 spraying (>=5 users in 10 min from one IP): {'192.0.2.99': 5}" in out
    assert "('juma', '203.0.113.50', '2026-03-02T08:14:36+00:00')" in out
    assert "/usr/bin/cat /etc/shadow" in out
