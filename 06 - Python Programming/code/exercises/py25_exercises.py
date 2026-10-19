"""PY25 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py25.py
"""

import logging
import re
from collections import Counter
SEMVER = re.compile('(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)')

def has_duplicates_fast(xs: list) -> bool:
    """O(n) average using a set."""
    raise NotImplementedError

def keyword_counts_slow(docs: list[str], stop_words: list[str]) -> dict[str, int]:
    """Deliberately slow reference version (rebuilds the stop list for every word)."""
    raise NotImplementedError

def keyword_counts_fast(docs: list[str], stop_words: list[str]) -> dict[str, int]:
    """Same result as keyword_counts_slow, built in one pass with a stop-word set."""
    raise NotImplementedError

def parse_semver(v: str) -> tuple[int, int, int]:
    """'1.4.2' -> (1, 4, 2); ValueError on malformed input (no leading zeros)."""
    raise NotImplementedError

def bump(version: str, part: str) -> str:
    """Increment major/minor/patch, resetting lower parts."""
    raise NotImplementedError

def make_logger(name: str, stream, level: int=logging.INFO) -> logging.Logger:
    """Logger writing 'LEVEL name: message' to stream; idempotent (no duplicate handlers)."""
    raise NotImplementedError

def amdahl_speedup(fraction: float, factor: float) -> float:
    """Overall speed-up when `fraction` of run time is made `factor` times faster."""
    raise NotImplementedError
