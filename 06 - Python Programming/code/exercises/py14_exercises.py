"""PY14 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py14.py
"""

import csv
import json
import os
import tempfile
from pathlib import Path
DEFAULTS = {'currency': 'TZS', 'decimals': 2, 'categories': ['food', 'transport']}

def write_lines(path: Path, lines: list[str]) -> None:
    """Write each string followed by a newline (UTF-8)."""
    raise NotImplementedError

def read_lines(path: Path) -> list[str]:
    """Return the file's lines without newline characters."""
    raise NotImplementedError

def file_stats(path: Path) -> tuple[int, int]:
    """(line count, word count), reading lazily."""
    raise NotImplementedError

def load_marks(path: Path) -> tuple[dict[str, float], list[str]]:
    """Read a name,mark CSV -> (valid marks, error messages with line numbers)."""
    raise NotImplementedError

def save_marks(path: Path, marks: dict[str, float]) -> None:
    """Write a name,mark CSV sorted by name."""
    raise NotImplementedError

def load_settings(path: Path) -> dict:
    """Defaults merged with a JSON object file; ValueError for unknown keys / non-objects."""
    raise NotImplementedError

def append_jsonl(path: Path, record: dict) -> None:
    """Append one JSON object as a line."""
    raise NotImplementedError

def read_jsonl(path: Path) -> list[dict]:
    """Read JSON Lines, skipping blanks; ValueError listing corrupt line numbers."""
    raise NotImplementedError

def atomic_write_json(path: Path, data) -> None:
    """Write JSON via temp file + os.replace so the target is never half-written."""
    raise NotImplementedError
