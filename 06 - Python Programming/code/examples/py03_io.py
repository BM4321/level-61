"""PY-03: print, f-strings and a testable receipt. Run: python examples/py03_io.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py03_solutions import format_receipt, progress_bar  # noqa: E402

print("a", "b", "c", sep="-")
x = 5
print(f"{x=}  {3.14159:.2f}  {1234567:,}  {0.256:.1%}  {42:05d}  {'hi':*^10}  {12345.678:.2e}")
print(f"{3.14159:.2}  {2.675:.2f}  {'a' + chr(10) + 'b'!r}")
print(format_receipt([("Pen", 3, 1.5), ("Notebook", 12, 25)]))
for done in (0, 7, 20):
    print(progress_bar(done, 20))
