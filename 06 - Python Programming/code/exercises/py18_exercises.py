"""PY18 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py18.py
"""

import functools
import time
from contextlib import contextmanager
from itertools import islice

class Countdown:
    """Iterator yielding start, start-1, ..., 1."""

    def __init__(self, start: int):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __next__(self) -> int:
        raise NotImplementedError

def fibonacci():
    """Infinite generator 0, 1, 1, 2, 3, ..."""
    raise NotImplementedError

def take(n: int, iterable) -> list:
    """First n items of any iterable."""
    raise NotImplementedError

def chunks(iterable, size: int):
    """Yield lists of `size` items from any iterable (last may be shorter)."""
    raise NotImplementedError

def count_calls(func):
    """Decorator adding a .calls counter attribute."""
    raise NotImplementedError

def retry(times: int, exceptions: tuple=(Exception,)):
    """Decorator factory: retry up to `times` attempts on the given exceptions."""
    raise NotImplementedError

class Timer:
    """Context manager recording .elapsed seconds; never suppresses exceptions."""

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, exc_type, exc, tb):
        raise NotImplementedError

@contextmanager
def timer():
    """Generator-based timer: yields a dict that receives 'elapsed'."""
    raise NotImplementedError

def failed_logins_by_ip(lines) -> dict[str, int]:
    """Count FAIL lines per ip= field, streaming over any iterable of lines."""
    raise NotImplementedError
