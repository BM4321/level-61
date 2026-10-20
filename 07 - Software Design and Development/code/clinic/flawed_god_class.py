"""FLAWED DESIGN, for critique only (SD Flawed Design Clinic, case F1).

One class does everything: parsing, validation, business rules, SQL, formatting and notification.
It runs and mostly works, which is why designs like this survive.
"""
import sqlite3
from datetime import datetime

DB = sqlite3.connect(":memory:")          # global shared state
DB.execute("CREATE TABLE b (id INTEGER PRIMARY KEY, who TEXT, ws TEXT, s TEXT, e TEXT, st TEXT)")
SENT = []                                  # pretend email outbox


class LabManager:
    def do_booking(self, who, ws, s, e, role="student", send=True, fmt="text"):
        s2 = datetime.strptime(s, "%Y-%m-%d %H:%M")
        e2 = datetime.strptime(e, "%Y-%m-%d %H:%M")
        if e2 <= s2:
            print("bad time")
            return False
        if s2.hour < 7 or e2.hour > 22:            # magic numbers; 22:30 end slips through
            print("closed")
            return False
        if ws == "LAB1-03":                         # hard-coded out-of-service list
            print("broken pc")
            return False
        rows = DB.execute(f"SELECT s, e FROM b WHERE ws = '{ws}' AND st != 'x'").fetchall()   # SQL injection
        for r in rows:
            if not (e <= r[0] or s >= r[1]):        # string comparison of times
                print("taken")
                return False
        if role == "student":
            tot = 0
            for r in DB.execute(f"SELECT s, e FROM b WHERE who = '{who}' AND st != 'x'").fetchall():
                tot += (datetime.strptime(r[1], "%Y-%m-%d %H:%M") - datetime.strptime(r[0], "%Y-%m-%d %H:%M")).seconds / 3600
            if tot + (e2 - s2).seconds / 3600 > 10:   # quota is per all time, not per week
                print("quota")
                return False
        DB.execute(f"INSERT INTO b (who, ws, s, e, st) VALUES ('{who}', '{ws}', '{s}', '{e}', 'c')")
        if send:
            SENT.append(f"Dear {who}, booked {ws} {s}")
        if fmt == "text":
            print(f"OK {who} {ws} {s}-{e}")
        elif fmt == "html":
            print(f"<p>OK {who} {ws}</p>")      # unescaped HTML
        return True
