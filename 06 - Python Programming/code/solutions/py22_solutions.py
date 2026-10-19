"""PY-22 reference solutions (sqlite3). Use sqlite3.connect(':memory:') to experiment."""
import sqlite3

SCHEMA = """
CREATE TABLE students (
    student_id  TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    programme   TEXT NOT NULL DEFAULT 'CS'
);
CREATE TABLE courses (
    code        TEXT PRIMARY KEY,
    title       TEXT NOT NULL UNIQUE
);
CREATE TABLE marks (
    student_id  TEXT NOT NULL REFERENCES students(student_id),
    code        TEXT NOT NULL REFERENCES courses(code),
    mark        REAL NOT NULL CHECK (mark BETWEEN 0 AND 100),
    PRIMARY KEY (student_id, code)
);
"""
SORTABLE = {"name": "name", "student_id": "student_id"}


def create_schema(conn: sqlite3.Connection) -> None:
    """Enable foreign keys and create the three tables."""
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)


def add_student(conn: sqlite3.Connection, student_id: str, name: str) -> None:
    with conn:
        conn.execute("INSERT INTO students (student_id, name) VALUES (?, ?)", (student_id, name))


def add_course(conn: sqlite3.Connection, code: str, title: str) -> None:
    with conn:
        conn.execute("INSERT INTO courses (code, title) VALUES (?, ?)", (code, title))


def record_mark(conn: sqlite3.Connection, student_id: str, code: str, mark: float) -> None:
    """Insert or update (upsert) a mark."""
    with conn:
        conn.execute(
            "INSERT INTO marks (student_id, code, mark) VALUES (?, ?, ?) "
            "ON CONFLICT(student_id, code) DO UPDATE SET mark = excluded.mark",
            (student_id, code, mark))


def course_averages(conn: sqlite3.Connection) -> list[tuple[str, float]]:
    """[(code, average rounded to 1 dp)] best first, ties by code."""
    rows = conn.execute(
        "SELECT code, ROUND(AVG(mark), 1) AS a FROM marks GROUP BY code ORDER BY a DESC, code").fetchall()
    return [tuple(r) for r in rows]


def students_without_marks(conn: sqlite3.Connection) -> list[str]:
    rows = conn.execute("""
        SELECT s.name FROM students s
        LEFT JOIN marks m ON m.student_id = s.student_id
        WHERE m.student_id IS NULL ORDER BY s.name""").fetchall()
    return [r[0] for r in rows]


def search_students(conn: sqlite3.Connection, fragment: str) -> list[str]:
    """Case-insensitive substring search; % and _ in the fragment are literal."""
    escaped = fragment.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    rows = conn.execute("SELECT name FROM students WHERE name LIKE ? ESCAPE '\\' ORDER BY name",
                        (f"%{escaped}%",)).fetchall()
    return [r[0] for r in rows]


def find_unsafe(conn: sqlite3.Connection, name: str) -> list:
    """DELIBERATELY VULNERABLE (for demonstration only): string-built SQL."""
    return conn.execute(f"SELECT student_id FROM students WHERE name = '{name}'").fetchall()


def find_safe(conn: sqlite3.Connection, name: str) -> list:
    """Parameterised equivalent of find_unsafe."""
    return conn.execute("SELECT student_id FROM students WHERE name = ?", (name,)).fetchall()


def transfer_marks(conn: sqlite3.Connection, from_code: str, to_code: str) -> None:
    """Atomically move a course (and its marks) to a new code."""
    with conn:
        conn.execute("INSERT INTO courses (code, title) SELECT ?, title || ' (new)' FROM courses WHERE code = ?",
                     (to_code, from_code))
        conn.execute("UPDATE marks SET code = ? WHERE code = ?", (to_code, from_code))
        conn.execute("DELETE FROM courses WHERE code = ?", (from_code,))


def top_students(conn: sqlite3.Connection, code: str, n: int) -> list[tuple[str, float]]:
    """Best n (name, mark) in a course, ties by name."""
    rows = conn.execute("""
        SELECT s.name, m.mark FROM marks m JOIN students s ON s.student_id = m.student_id
        WHERE m.code = ? ORDER BY m.mark DESC, s.name LIMIT ?""", (code, n)).fetchall()
    return [tuple(r) for r in rows]


def sort_students(conn: sqlite3.Connection, column: str) -> list[str]:
    """Names ordered by an allow-listed column; ValueError otherwise."""
    if column not in SORTABLE:
        raise ValueError(f"cannot sort by {column!r}")
    return [r[0] for r in conn.execute(f"SELECT name FROM students ORDER BY {SORTABLE[column]}")]
