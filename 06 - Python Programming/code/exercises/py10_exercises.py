"""PY10 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py10.py
"""

def running_total(values: list[float]) -> list[float]:
    """Cumulative sums: [5, 3, 2] -> [5, 8, 10]."""
    raise NotImplementedError

def median(values: list[float]) -> float:
    """Median without mutating the input; ValueError if empty."""
    raise NotImplementedError

def dedupe(xs: list) -> list:
    """Remove duplicates, keeping first occurrences in order; returns a new list."""
    raise NotImplementedError

def rotate(xs: list, k: int) -> list:
    """Rotate right by k (negative k rotates left); returns a new list."""
    raise NotImplementedError

def chunk(xs: list, size: int) -> list[list]:
    """Split into consecutive pieces of length size (last may be shorter)."""
    raise NotImplementedError

def _check_rectangular(rows: list[list]) -> None:
    raise NotImplementedError

def column_averages(rows: list[list[float]]) -> list[float]:
    """Mean of each column; ValueError for empty or ragged input."""
    raise NotImplementedError

def transpose(rows: list[list]) -> list[list]:
    """Rows become columns; ValueError for empty or ragged input."""
    raise NotImplementedError

def top_n(students: list[tuple[str, float]], n: int) -> list[tuple[str, float]]:
    """n best (name, mark) pairs by mark descending, ties by name ascending."""
    raise NotImplementedError

def flatten_matrix(rows: list[list]) -> list:
    """Row-major flattening."""
    raise NotImplementedError

def reshape(flat: list, rows: int, cols: int) -> list[list]:
    """Inverse of flatten_matrix; ValueError unless len(flat) == rows * cols."""
    raise NotImplementedError

def sliding_window(xs: list, size: int) -> list[list]:
    """Overlapping windows of length size."""
    raise NotImplementedError
