"""PY22 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py22.py
"""

import sqlite3
SCHEMA = "\nCREATE TABLE students (\n    student_id  TEXT PRIMARY KEY,\n    name        TEXT NOT NULL,\n    programme   TEXT NOT NULL DEFAULT 'CS'\n);\nCREATE TABLE courses (\n    code        TEXT PRIMARY KEY,\n    title       TEXT NOT NULL UNIQUE\n);\nCREATE TABLE marks (\n    student_id  TEXT NOT NULL REFERENCES students(student_id),\n    code        TEXT NOT NULL REFERENCES courses(code),\n    mark        REAL NOT NULL CHECK (mark BETWEEN 0 AND 100),\n    PRIMARY KEY (student_id, code)\n);\n"
SORTABLE = {'name': 'name', 'student_id': 'student_id'}

def create_schema(conn: sqlite3.Connection) -> None:
    """Enable foreign keys and create the three tables."""
    raise NotImplementedError

def add_student(conn: sqlite3.Connection, student_id: str, name: str) -> None:
    raise NotImplementedError

def add_course(conn: sqlite3.Connection, code: str, title: str) -> None:
    raise NotImplementedError

def record_mark(conn: sqlite3.Connection, student_id: str, code: str, mark: float) -> None:
    """Insert or update (upsert) a mark."""
    raise NotImplementedError

def course_averages(conn: sqlite3.Connection) -> list[tuple[str, float]]:
    """[(code, average rounded to 1 dp)] best first, ties by code."""
    raise NotImplementedError

def students_without_marks(conn: sqlite3.Connection) -> list[str]:
    raise NotImplementedError

def search_students(conn: sqlite3.Connection, fragment: str) -> list[str]:
    """Case-insensitive substring search; % and _ in the fragment are literal."""
    raise NotImplementedError

def find_unsafe(conn: sqlite3.Connection, name: str) -> list:
    """DELIBERATELY VULNERABLE (for demonstration only): string-built SQL."""
    raise NotImplementedError

def find_safe(conn: sqlite3.Connection, name: str) -> list:
    """Parameterised equivalent of find_unsafe."""
    raise NotImplementedError

def transfer_marks(conn: sqlite3.Connection, from_code: str, to_code: str) -> None:
    """Atomically move a course (and its marks) to a new code."""
    raise NotImplementedError

def top_students(conn: sqlite3.Connection, code: str, n: int) -> list[tuple[str, float]]:
    """Best n (name, mark) in a course, ties by name."""
    raise NotImplementedError

def sort_students(conn: sqlite3.Connection, column: str) -> list[str]:
    """Names ordered by an allow-listed column; ValueError otherwise."""
    raise NotImplementedError
