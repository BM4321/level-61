"""PY-04: branching, short-circuit, guard clauses. Run: python examples/py04_branching.py"""


def grade(mark: float) -> str:
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
    return "F"


def grade_wrong(mark):  # deliberately buggy: thresholds in the wrong order
    if mark >= 40:
        return "D"
    elif mark >= 50:
        return "C"
    elif mark >= 60:
        return "B"
    elif mark >= 70:
        return "A"
    return "F"


for mk in (39, 40, 69.5, 70, 95):
    print(f"{mk:>5}: correct={grade(mk)}  buggy={grade_wrong(mk)}")

print("short-circuit:", "" or "guest", 5 and 0, None or [])
count, total = 0, 10
print("safe guard:", count != 0 and total / count > 5)   # no ZeroDivisionError
