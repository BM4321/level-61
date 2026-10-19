import io
import logging
import math
import random

import pytest

from _target import load

m = load("py25")


def test_has_duplicates_fast():
    assert m.has_duplicates_fast([1, 2, 3, 2])
    assert not m.has_duplicates_fast(list(range(10_000)))
    assert not m.has_duplicates_fast([])


def test_keyword_counts_equivalent():
    rng = random.Random(25)
    vocab = ["Alpha", "beta", "GAMMA", "delta", "eps"]
    docs = [" ".join(rng.choice(vocab) for _ in range(20)) for _ in range(30)]
    stop = ["BETA", "eps"]
    from solutions.py25_solutions import keyword_counts_slow
    assert m.keyword_counts_fast(docs, stop) == keyword_counts_slow(docs, stop)


@pytest.mark.parametrize("v, t", [("1.4.2", (1, 4, 2)), ("0.0.0", (0, 0, 0)), (" 10.20.30 ", (10, 20, 30))])
def test_parse_semver(v, t):
    assert m.parse_semver(v) == t


@pytest.mark.parametrize("bad", ["1.2", "01.2.3", "1.2.3.4", "a.b.c", "1.2.-3"])
def test_parse_semver_bad(bad):
    with pytest.raises(ValueError):
        m.parse_semver(bad)


def test_bump():
    assert m.bump("1.4.2", "patch") == "1.4.3"
    assert m.bump("1.4.2", "minor") == "1.5.0"
    assert m.bump("1.4.2", "major") == "2.0.0"
    with pytest.raises(ValueError):
        m.bump("1.4.2", "build")


def test_make_logger_idempotent():
    stream = io.StringIO()
    log = m.make_logger("semester6.test", stream)
    log2 = m.make_logger("semester6.test", stream)
    assert log is log2
    log.info("hello %s", "world")
    log.debug("hidden")
    assert stream.getvalue() == "INFO semester6.test: hello world\n"


def test_amdahl():
    assert math.isclose(m.amdahl_speedup(0.75, 10), 20 / 6.5)
    assert math.isclose(m.amdahl_speedup(0.25, 100), 20 / 15.05)
    assert math.isclose(m.amdahl_speedup(0.05, 1e12), 1 / 0.95, rel_tol=1e-6)
    with pytest.raises(ValueError):
        m.amdahl_speedup(1.5, 2)
