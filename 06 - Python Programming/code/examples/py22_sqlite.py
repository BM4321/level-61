"""PY-22: SQLite essentials and an injection demonstration (in memory, safe).
Run: python examples/py22_sqlite.py
"""
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("PRAGMA foreign_keys = ON")
conn.executescript("""
CREATE TABLE students (student_id TEXT PRIMARY KEY, name TEXT NOT NULL);
INSERT INTO students VALUES ('S1', 'Amina'), ('S2', 'Baraka');
""")
print(conn.execute("SELECT name FROM students ORDER BY name DESC").fetchall())

payload = "x' OR '1'='1"
unsafe_sql = f"SELECT student_id FROM students WHERE name = '{payload}'"
print("UNSAFE query text:", unsafe_sql)
print("UNSAFE result    :", conn.execute(unsafe_sql).fetchall())
print("SAFE result      :", conn.execute("SELECT student_id FROM students WHERE name = ?", (payload,)).fetchall())

conn.execute("CREATE TABLE marks_strict (mark REAL NOT NULL) STRICT")
try:
    conn.execute("INSERT INTO marks_strict VALUES ('seventy')")
except sqlite3.Error as exc:
    print("STRICT table rejected text:", exc)
conn.close()
