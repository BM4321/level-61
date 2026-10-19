import sqlite3

import pytest

from _target import load

m = load("py22")


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    m.create_schema(c)
    for sid, name in [("S1", "Amina"), ("S2", "Baraka"), ("S3", "Chen"), ("S4", "100%_Dan")]:
        m.add_student(c, sid, name)
    m.add_course(c, "CST06102", "Python Programming")
    m.add_course(c, "GST06106", "Discrete Mathematics")
    for sid, code, mk in [("S1", "CST06102", 78), ("S2", "CST06102", 64), ("S1", "GST06106", 55),
                          ("S2", "GST06106", 81)]:
        m.record_mark(c, sid, code, mk)
    yield c
    c.close()


def test_constraints(conn):
    with pytest.raises(sqlite3.IntegrityError):
        m.record_mark(conn, "S1", "CST06102", 150)         # CHECK
    with pytest.raises(sqlite3.IntegrityError):
        m.record_mark(conn, "S99", "CST06102", 50)         # FK
    with pytest.raises(sqlite3.IntegrityError):
        m.add_student(conn, "S1", "Duplicate")            # PK


def test_upsert(conn):
    m.record_mark(conn, "S1", "CST06102", 90)
    assert conn.execute("SELECT COUNT(*), MAX(mark) FROM marks WHERE student_id='S1' AND code='CST06102'"
                        ).fetchone() == (1, 90.0)


def test_queries(conn):
    assert m.course_averages(conn) == [("CST06102", 71.0), ("GST06106", 68.0)]
    assert m.students_without_marks(conn) == ["100%_Dan", "Chen"]
    assert m.top_students(conn, "CST06102", 1) == [("Amina", 78.0)]


def test_search_escapes_wildcards(conn):
    assert m.search_students(conn, "ar") == ["Baraka"]
    assert m.search_students(conn, "AMI") == ["Amina"]
    assert m.search_students(conn, "%") == ["100%_Dan"]
    assert m.search_students(conn, "_") == ["100%_Dan"]


def test_injection_demo(conn):
    payload = "x' OR '1'='1"
    assert len(m.find_unsafe(conn, payload)) == 4      # vulnerable version leaks all rows
    assert m.find_safe(conn, payload) == []
    m.add_student(conn, "S5", "O'Brien")
    assert m.find_safe(conn, "O'Brien") == [("S5",)]
    with pytest.raises(sqlite3.OperationalError):
        m.find_unsafe(conn, "O'Brien")


def test_transfer_success_and_rollback(conn):
    m.transfer_marks(conn, "GST06106", "GST06999")
    assert {r[0] for r in conn.execute("SELECT code FROM marks")} == {"CST06102", "GST06999"}
    with pytest.raises(sqlite3.IntegrityError):
        m.transfer_marks(conn, "GST06999", "CST06102")      # target exists → rollback
    assert {r[0] for r in conn.execute("SELECT code FROM courses")} == {"CST06102", "GST06999"}
    assert conn.execute("SELECT COUNT(*) FROM marks WHERE code='GST06999'").fetchone() == (2,)


def test_sort_allowlist(conn):
    assert m.sort_students(conn, "name")[0] == "100%_Dan"
    with pytest.raises(ValueError):
        m.sort_students(conn, "name; DROP TABLE students")
