"""PY-03 exercises. Check: PY_TARGET=exercises python -m pytest tests/test_py03.py"""


def format_money(amount: float) -> str:
    """Return e.g. 'TZS 1,234.50' (comma separator, 2 decimals)."""
    raise NotImplementedError


def format_row(name: str, qty: int, price: float) -> str:
    """Return a 29-char row: name left in 14, qty right in 5, price right in 10 with 2 decimals."""
    raise NotImplementedError


def format_receipt(items: list[tuple[str, int, float]]) -> str:
    """Return the receipt string exactly as in PY-03 Example 2 (header, rows, TOTAL line)."""
    raise NotImplementedError


def progress_bar(done: int, total: int, width: int = 20) -> str:
    """Return '[#######.............]  35.0%'. Clamp done to [0,total]; ValueError if total <= 0."""
    raise NotImplementedError


def parse_mark(text: str) -> float:
    """Strip, convert to float; ValueError if non-numeric or outside 0-100."""
    raise NotImplementedError


def format_table(rows: list[list], headers: list[str]) -> str:
    """Column widths = longest entry; numbers right-aligned, text left-aligned; columns joined by 2 spaces."""
    raise NotImplementedError
