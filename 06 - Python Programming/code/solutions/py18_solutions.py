"""PY-18 reference solutions (iterators, generators, decorators, context managers)."""
import functools
import time
from contextlib import contextmanager
from itertools import islice


class Countdown:
    """Iterator yielding start, start-1, ..., 1."""

    def __init__(self, start: int):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self) -> int:
        if self.current <= 0:
            raise StopIteration
        self.current -= 1
        return self.current + 1


def fibonacci():
    """Infinite generator 0, 1, 1, 2, 3, ..."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def take(n: int, iterable) -> list:
    """First n items of any iterable."""
    return list(islice(iterable, n))


def chunks(iterable, size: int):
    """Yield lists of `size` items from any iterable (last may be shorter)."""
    if size < 1:
        raise ValueError("size must be >= 1")
    it = iter(iterable)
    while True:
        batch = list(islice(it, size))
        if not batch:
            return
        yield batch


def count_calls(func):
    """Decorator adding a .calls counter attribute."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


def retry(times: int, exceptions: tuple = (Exception,)):
    """Decorator factory: retry up to `times` attempts on the given exceptions."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise
        return wrapper
    return decorator


class Timer:
    """Context manager recording .elapsed seconds; never suppresses exceptions."""

    def __enter__(self):
        self.start = time.perf_counter()
        self.elapsed = None
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False


@contextmanager
def timer():
    """Generator-based timer: yields a dict that receives 'elapsed'."""
    start = time.perf_counter()
    result: dict = {}
    try:
        yield result
    finally:
        result["elapsed"] = time.perf_counter() - start


def failed_logins_by_ip(lines) -> dict[str, int]:
    """Count FAIL lines per ip= field, streaming over any iterable of lines."""
    counts: dict[str, int] = {}
    for line in lines:
        parts = line.split()
        if len(parts) < 4 or parts[1] != "FAIL":
            continue
        fields = dict(p.split("=", 1) for p in parts[2:] if "=" in p)
        ip = fields.get("ip")
        if ip:
            counts[ip] = counts.get(ip, 0) + 1
    return counts
