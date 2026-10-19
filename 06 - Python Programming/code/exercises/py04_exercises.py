"""PY04 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py04.py
"""

BANDS = [(70, 'A', 5), (60, 'B', 4), (50, 'C', 3), (40, 'D', 2), (0, 'F', 0)]

def grade(mark: float) -> str:
    """Return letter grade A-F for 0 <= mark <= 100; raise ValueError otherwise."""
    raise NotImplementedError

def is_leap(year: int) -> bool:
    """Gregorian leap-year rule."""
    raise NotImplementedError

def max_of_three(a, b, c):
    """Largest of three values, without using max()."""
    raise NotImplementedError

def classify_triangle(a: float, b: float, c: float) -> str:
    """'invalid', 'equilateral', 'isosceles' or 'scalene'."""
    raise NotImplementedError

def ticket_price(age: int, is_student: bool) -> int:
    """<5: 0; 5-17: 2000; 18+: 5000 (students 18+ pay 50%). ValueError if age < 0."""
    raise NotImplementedError

def quadrant(x: float, y: float):
    """Return 1-4, 'x-axis', 'y-axis' or 'origin'."""
    raise NotImplementedError

def discount_rate(total: float, is_member: bool, is_gift_card: bool) -> float:
    """10% if total >= 100000, +5% for members, capped at 12%, 0 for gift cards."""
    raise NotImplementedError

def grade_with_points(mark: float) -> tuple[str, int]:
    """Return (letter, points) using the BANDS table; ValueError outside 0-100."""
    raise NotImplementedError
