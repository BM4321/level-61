import pytest

from _target import load

m = load("py18")


def test_countdown():
    assert list(m.Countdown(3)) == [3, 2, 1]
    c = m.Countdown(2)
    list(c)
    assert list(c) == []  # single-use


def test_fibonacci_take():
    assert m.take(10, m.fibonacci()) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    assert m.take(3, "abcdef") == ["a", "b", "c"]


def test_chunks_any_iterable():
    assert list(m.chunks([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]
    assert list(m.chunks((x for x in range(4)), 2)) == [[0, 1], [2, 3]]
    assert list(m.chunks([], 3)) == []
    with pytest.raises(ValueError):
        list(m.chunks([1], 0))


def test_count_calls():
    @m.count_calls
    def fib(n):
        """doc"""
        return n if n < 2 else fib(n - 1) + fib(n - 2)

    fib(10)
    assert fib.calls == 177
    assert fib.__name__ == "fib" and fib.__doc__ == "doc"


def test_retry():
    state = {"n": 0}

    @m.retry(times=3, exceptions=(ConnectionError,))
    def flaky():
        state["n"] += 1
        if state["n"] < 3:
            raise ConnectionError
        return "ok"

    assert flaky() == "ok" and state["n"] == 3

    @m.retry(times=2, exceptions=(ConnectionError,))
    def broken():
        raise ValueError("not retried")

    with pytest.raises(ValueError):
        broken()


def test_timers():
    t = m.Timer()
    with pytest.raises(ZeroDivisionError):
        with t:
            1 / 0
    assert t.elapsed is not None and t.elapsed >= 0
    with m.timer() as r:
        sum(range(1000))
    assert r["elapsed"] >= 0


def test_failed_logins_streaming():
    def lines():
        for i in range(100_000):
            status = "FAIL" if i % 4 == 0 else "OK"
            yield f"2026-10-19T08:00:{i % 60:02d} {status} user=u{i % 7} ip=10.0.0.{i % 3}"
        yield "garbage line"
        yield "2026-10-19T09:00:00 FAIL user=x"
    counts = m.failed_logins_by_ip(lines())
    assert sum(counts.values()) == 25_000
    assert set(counts) == {"10.0.0.0", "10.0.0.1", "10.0.0.2"}
