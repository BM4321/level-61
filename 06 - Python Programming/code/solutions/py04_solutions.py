"""PY-04 reference solutions (illustrative grading scale: A>=70, B>=60, C>=50, D>=40, else F)."""

BANDS = [(70, "A", 5), (60, "B", 4), (50, "C", 3), (40, "D", 2), (0, "F", 0)]


def grade(mark: float) -> str:
    """Return letter grade A-F for 0 <= mark <= 100; raise ValueError otherwise."""
    if not 0 <= mark <= 100:
        raise ValueError(f"mark out of range: {mark}")
    if mark >= 70:
        return "A"
    elif mark >= 60:
        return "B"
    elif mark >= 50:
        return "C"
    elif mark >= 40:
        return "D"
    else:
        return "F"


def is_leap(year: int) -> bool:
    """Gregorian leap-year rule."""
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def max_of_three(a, b, c):
    """Largest of three values, without using max()."""
    largest = a
    if b > largest:
        largest = b
    if c > largest:
        largest = c
    return largest


def classify_triangle(a: float, b: float, c: float) -> str:
    """'invalid', 'equilateral', 'isosceles' or 'scalene'."""
    if a <= 0 or b <= 0 or c <= 0:
        return "invalid"
    if a + b <= c or a + c <= b or b + c <= a:
        return "invalid"
    if a == b == c:
        return "equilateral"
    if a == b or b == c or a == c:
        return "isosceles"
    return "scalene"


def ticket_price(age: int, is_student: bool) -> int:
    """<5: 0; 5-17: 2000; 18+: 5000 (students 18+ pay 50%). ValueError if age < 0."""
    if age < 0:
        raise ValueError("age cannot be negative")
    if age < 5:
        return 0
    if age < 18:
        return 2000
    return 2500 if is_student else 5000


def quadrant(x: float, y: float):
    """Return 1-4, 'x-axis', 'y-axis' or 'origin'."""
    if x == 0 and y == 0:
        return "origin"
    if y == 0:
        return "x-axis"
    if x == 0:
        return "y-axis"
    if x > 0:
        return 1 if y > 0 else 4
    return 2 if y > 0 else 3


def discount_rate(total: float, is_member: bool, is_gift_card: bool) -> float:
    """10% if total >= 100000, +5% for members, capped at 12%, 0 for gift cards."""
    if is_gift_card:
        return 0.0
    rate = 0.0
    if total >= 100_000:
        rate += 0.10
    if is_member:
        rate += 0.05
    return min(rate, 0.12)


def grade_with_points(mark: float) -> tuple[str, int]:
    """Return (letter, points) using the BANDS table; ValueError outside 0-100."""
    if not 0 <= mark <= 100:
        raise ValueError(mark)
    for threshold, letter, points in BANDS:
        if mark >= threshold:
            return letter, points
    raise AssertionError("unreachable")
