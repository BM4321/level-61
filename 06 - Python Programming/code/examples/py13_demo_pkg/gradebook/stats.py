"""Statistics helpers."""
from .grading import grade


def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("mean of empty list")
    return sum(values) / len(values)


def summary(marks: dict[str, float]) -> dict[str, object]:
    values = list(marks.values())
    return {"count": len(values), "mean": round(mean(values), 2),
            "grades": {name: grade(m) for name, m in marks.items()}}
