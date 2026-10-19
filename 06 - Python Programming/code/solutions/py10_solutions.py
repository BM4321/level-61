"""PY-10 reference solutions (lists and tuples)."""


def running_total(values: list[float]) -> list[float]:
    """Cumulative sums: [5, 3, 2] -> [5, 8, 10]."""
    totals = []
    acc = 0
    for v in values:
        acc += v
        totals.append(acc)
    return totals


def median(values: list[float]) -> float:
    """Median without mutating the input; ValueError if empty."""
    s = sorted(values)
    n = len(s)
    if n == 0:
        raise ValueError("median of empty list")
    mid = n // 2
    return s[mid] if n % 2 else (s[mid - 1] + s[mid]) / 2


def dedupe(xs: list) -> list:
    """Remove duplicates, keeping first occurrences in order; returns a new list."""
    seen = set()
    out = []
    for x in xs:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def rotate(xs: list, k: int) -> list:
    """Rotate right by k (negative k rotates left); returns a new list."""
    if not xs:
        return []
    k %= len(xs)
    return xs[-k:] + xs[:-k] if k else xs[:]


def chunk(xs: list, size: int) -> list[list]:
    """Split into consecutive pieces of length size (last may be shorter)."""
    if size < 1:
        raise ValueError("size must be >= 1")
    return [xs[i:i + size] for i in range(0, len(xs), size)]


def _check_rectangular(rows: list[list]) -> None:
    if not rows or any(len(r) != len(rows[0]) for r in rows):
        raise ValueError("rows must be non-empty and rectangular")


def column_averages(rows: list[list[float]]) -> list[float]:
    """Mean of each column; ValueError for empty or ragged input."""
    _check_rectangular(rows)
    return [sum(row[c] for row in rows) / len(rows) for c in range(len(rows[0]))]


def transpose(rows: list[list]) -> list[list]:
    """Rows become columns; ValueError for empty or ragged input."""
    _check_rectangular(rows)
    return [list(col) for col in zip(*rows)]


def top_n(students: list[tuple[str, float]], n: int) -> list[tuple[str, float]]:
    """n best (name, mark) pairs by mark descending, ties by name ascending."""
    return sorted(students, key=lambda s: (-s[1], s[0]))[:n]


def flatten_matrix(rows: list[list]) -> list:
    """Row-major flattening."""
    return [x for row in rows for x in row]


def reshape(flat: list, rows: int, cols: int) -> list[list]:
    """Inverse of flatten_matrix; ValueError unless len(flat) == rows * cols."""
    if rows < 0 or cols < 0 or len(flat) != rows * cols:
        raise ValueError("size mismatch")
    return [flat[r * cols:(r + 1) * cols] for r in range(rows)]


def sliding_window(xs: list, size: int) -> list[list]:
    """Overlapping windows of length size."""
    if size < 1:
        raise ValueError("size must be >= 1")
    return [xs[i:i + size] for i in range(len(xs) - size + 1)]
