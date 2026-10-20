import ast
import io
import json
from datetime import timedelta
from pathlib import Path

from hostel.cli import main
from hostel.models import Priority, Request, Status
from hostel.reports import summary
from hostel.security import PasswordHasher


def test_summary_numbers(clock):
    t0 = clock()
    reqs = [
        Request(1, "A-101", "S1", "electrical", "x" * 10, Priority.URGENT, Status.CLOSED, t0,
                "T1", t0 + timedelta(hours=5)),
        Request(2, "A-101", "S1", "plumbing", "x" * 10, Priority.NORMAL, Status.RESOLVED, t0,
                "T1", t0 + timedelta(hours=26)),
        Request(3, "B-204", "S2", "electrical", "x" * 10, Priority.URGENT, Status.ASSIGNED, t0, "T2"),
        Request(4, "B-204", "S2", "furniture", "x" * 10, Priority.LOW, Status.NEW, t0 + timedelta(hours=40)),
    ]
    s = summary(reqs, t0 + timedelta(hours=48))
    assert s["total"] == 4 and s["by_status"]["closed"] == 1 and s["by_status"]["new"] == 1
    assert s["open_by_priority"] == {"urgent": 1, "normal": 0, "low": 1}
    assert s["mean_hours_to_resolve"] == 15.5                      # (5 + 26) / 2
    assert s["overdue_urgent"] == [3]                               # open, urgent, 48 h old
    assert summary([], t0)["mean_hours_to_resolve"] is None


def run(db, argv, *passwords):
    out = io.StringIO()
    code = main(["--db", db, *argv], stdin=io.StringIO("".join(p + "\n" for p in passwords)), stdout=out,
                hasher=PasswordHasher(n=2**10))
    return code, out.getvalue()


def test_cli_end_to_end(tmp_path, capsys):
    db = str(tmp_path / "cli.db")
    W, R, T = "violet-kettle-orbit-9", "maple-signal-copper-4", "granite-paper-swift-2"
    assert run(db, ["init"]) == (0, f"database ready: {db}\n")
    assert run(db, ["register", "STU/21/0001", "Baraka", "resident", "--room", "A-101"], R)[0] == 1  # first must be warden
    assert run(db, ["register", "WARDEN01", "Asha Warden", "warden"], W) == (0, "registered WARDEN01 (warden)\n")
    assert run(db, ["--as", "WARDEN01", "add-room", "A-101", "A", "2"], W)[0] == 0
    assert run(db, ["--as", "WARDEN01", "register", "STU/21/0001", "Baraka Resident", "resident", "--room", "A-101"],
               W, R)[0] == 0
    assert run(db, ["--as", "WARDEN01", "register", "TECH01", "Daudi Technician", "technician"], W, T)[0] == 0
    assert run(db, ["--as", "STU/21/0001", "submit", "A-101", "electrical", "Socket sparks near the desk"], R) == (
        0, "request 1 submitted (urgent)\n")
    assert run(db, ["--as", "STU/21/0001", "move", "1", "assigned", "--assignee", "TECH01"], R)[0] == 1
    assert "only a warden" in capsys.readouterr().err
    assert run(db, ["--as", "WARDEN01", "move", "1", "assigned", "--assignee", "TECH01"], W) == (
        0, "request 1 is now assigned\n")
    code, listing = run(db, ["--as", "TECH01", "list"], T)
    assert code == 0 and "assigned" in listing and "Socket sparks" in listing
    assert run(db, ["--as", "TECH01", "list"], "wrong-password-here")[0] == 1
    code, hist = run(db, ["--as", "STU/21/0001", "history", "1"], R)
    assert code == 0 and hist.count("\n") == 2 and "new -> assigned  by WARDEN01" in hist
    code, report = run(db, ["--as", "WARDEN01", "report"], W)
    assert code == 0 and json.loads(report)["open_by_priority"]["urgent"] == 1
    assert run(db, ["--as", "STU/21/0001", "report"], R)[0] == 1
    assert run(db, ["--as", "STU/21/0001", "submit", "A-101", "electrical", "Second socket also sparks"], R)[0] == 0
    code, insights = run(db, ["--as", "WARDEN01", "insights"], W)
    data = json.loads(insights)
    assert code == 0 and data["work_queue"] == [1, 2] and data["possible_duplicates"] == {"A-101/electrical": [1, 2]}
    assert data["repeat_rooms"] == []                                    # 2 reports < threshold 3


SRC = Path(__file__).resolve().parents[1] / "src" / "hostel"


def imports_of(name):
    tree = ast.parse((SRC / f"{name}.py").read_text())
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            found.add(("." * node.level) + (node.module or ""))
        elif isinstance(node, ast.Import):
            found.update(a.name for a in node.names)
    return found


def test_layering_rules():
    # domain depends on nothing internal except errors; services never touch sqlite or the CLI
    assert imports_of("models") & {".repository", ".services", ".cli", "sqlite3"} == set()
    assert imports_of("services") & {"sqlite3", ".cli", "argparse"} == set()
    assert imports_of("reports") & {".repository", ".services", ".cli", "sqlite3"} == set()
    assert imports_of("insights") & {".repository", ".services", ".cli", "sqlite3"} == set()
