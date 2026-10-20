"""LAB-CS-06: input validation and SQL injection prevention, on a LOCAL in-memory SQLite database.

Run:  python lab06_sqli.py
The vulnerable functions exist only to be studied here. Never test payloads against systems you
do not own or have written permission to assess.
"""
import hashlib
import hmac
import os
import re
import sqlite3

REG_NO = re.compile(r"^[A-Z]{2,5}/[A-Z]{2,5}/\d{4}/\d{4}$")   # e.g. DEMO/BIT/2024/0117 (fictional format)


def _hash(pw: str, salt: bytes) -> bytes:
    return hashlib.scrypt(pw.encode(), salt=salt, n=2 ** 12, r=8, p=1, dklen=32)  # small cost: demo speed


def build_db() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (reg_no TEXT PRIMARY KEY, name TEXT, role TEXT, pw_plain TEXT,"
                 " salt BLOB, pw_hash BLOB)")
    conn.execute("CREATE TABLE requests (id INTEGER PRIMARY KEY, reg_no TEXT, room TEXT, issue TEXT)")
    people = [("DEMO/BIT/2024/0117", "Amina", "student", "ndizi mbili chai moto"),
              ("DEMO/BIT/2024/0233", "Baraka", "student", "maji ya kunywa safi sana"),
              ("DEMO/STF/2019/0001", "Mrs K", "warden", "warden passphrase for demo only")]
    for reg, name, role, pw in people:
        salt = os.urandom(16)
        # pw_plain is stored ONLY to show what the vulnerable design looks like. Never do this.
        conn.execute("INSERT INTO users VALUES (?,?,?,?,?,?)", (reg, name, role, pw, salt, _hash(pw, salt)))
    conn.executemany("INSERT INTO requests (reg_no, room, issue) VALUES (?,?,?)",
                     [("DEMO/BIT/2024/0117", "A-104", "Leaking tap"),
                      ("DEMO/BIT/2024/0233", "B-210", "Broken window latch"),
                      ("DEMO/BIT/2024/0117", "A-104", "No power in socket")])
    return conn


# ------------------------------------------------------------------ VULNERABLE (study only)
def login_vulnerable(conn, reg_no: str, password: str):
    sql = f"SELECT name, role FROM users WHERE reg_no = '{reg_no}' AND pw_plain = '{password}'"
    return sql, conn.execute(sql).fetchone()


def my_requests_vulnerable(conn, reg_no: str):
    return conn.execute(f"SELECT id, room, issue FROM requests WHERE reg_no = '{reg_no}'").fetchall()


# ------------------------------------------------------------------ FIXED
class ValidationError(ValueError):
    pass


def validate_reg_no(reg_no: str) -> str:
    reg_no = reg_no.strip().upper()
    if not REG_NO.fullmatch(reg_no):
        raise ValidationError("registration number format is invalid")
    return reg_no


def login_safe(conn, reg_no: str, password: str):
    reg_no = validate_reg_no(reg_no)
    row = conn.execute("SELECT name, role, salt, pw_hash FROM users WHERE reg_no = ?", (reg_no,)).fetchone()
    if row is None:
        _hash(password, b"\x00" * 16)          # similar work for unknown users (timing)
        return None
    name, role, salt, stored = row
    return (name, role) if hmac.compare_digest(_hash(password, salt), stored) else None


def my_requests_safe(conn, reg_no: str):
    return conn.execute("SELECT id, room, issue FROM requests WHERE reg_no = ?", (validate_reg_no(reg_no),)).fetchall()


def main() -> None:
    conn = build_db()
    print("== Part A: vulnerable login ==")
    for reg, pw in [("DEMO/BIT/2024/0117", "ndizi mbili chai moto"),
                    ("DEMO/BIT/2024/0117", "wrong"),
                    ("DEMO/STF/2019/0001' --", "anything"),
                    ("x' OR '1'='1' --", "anything")]:
        sql, row = login_vulnerable(conn, reg, pw)
        print(f"input reg_no={reg!r:28} -> {row}")
        print(f"   SQL: {sql}")

    print("\n== Part B: vulnerable data access (UNION) ==")
    payload = "x' UNION SELECT 0, reg_no, pw_plain FROM users --"
    for row in my_requests_vulnerable(conn, payload):
        print("  ", row)

    print("\n== Part C: fixed versions ==")
    print("correct login     :", login_safe(conn, "demo/bit/2024/0117", "ndizi mbili chai moto"))
    print("wrong password    :", login_safe(conn, "DEMO/BIT/2024/0117", "wrong"))
    for bad in ("DEMO/STF/2019/0001' --", "x' OR '1'='1' --", payload):
        try:
            login_safe(conn, bad, "anything")
        except ValidationError as e:
            print(f"rejected {bad[:26]!r:30}: {e}")
    print("own requests      :", my_requests_safe(conn, "DEMO/BIT/2024/0117"))
    # Even with validation disabled, parameters keep the payload as data:
    print("payload as a parameter returns:",
          conn.execute("SELECT id FROM requests WHERE reg_no = ?", (payload,)).fetchall())


if __name__ == "__main__":
    main()
