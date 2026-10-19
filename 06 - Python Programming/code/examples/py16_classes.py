"""PY-16: objects, invariants, value classes. Run: python examples/py16_classes.py"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py16_solutions import BankAccount, Fraction, Money  # noqa: E402

a, b = BankAccount("Juma", 1000), BankAccount("Neema")
a.deposit(500)
b.deposit(200)
a.withdraw(300)
print(a, b, a.history())
try:
    a.withdraw(10_000)
except ValueError as exc:
    print("invariant protected:", exc)

print(Fraction(1, 2) + Fraction(1, 3), Fraction(2, 4) == Fraction(1, 2))
print(sorted([Fraction(2, 3), Fraction(1, 2)]), len({Fraction(1, 2), Fraction(3, 6)}))
print(Money(100, "TZS").allocate([1, 1, 1]))


class Course:  # deliberately buggy: shared mutable class attribute
    students = []

    def __init__(self, code):
        self.code = code

    def enrol(self, sid):
        self.students.append(sid)


py, dm = Course("CST06102"), Course("GST06106")
py.enrol("S1")
print("bug demo, DM students:", dm.students)
