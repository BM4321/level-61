"""PY-25 reference solutions (performance, versioning, logging)."""
import logging
import re
from collections import Counter

SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")


def has_duplicates_fast(xs: list) -> bool:
    """O(n) average using a set."""
    seen = set()
    for x in xs:
        if x in seen:
            return True
        seen.add(x)
    return False


def keyword_counts_slow(docs: list[str], stop_words: list[str]) -> dict[str, int]:
    """Deliberately slow reference version (rebuilds the stop list for every word)."""
    counts: dict[str, int] = {}
    for doc in docs:
        for w in doc.split():
            if w.lower() not in [s.lower() for s in stop_words]:
                counts[w.lower()] = counts.get(w.lower(), 0) + 1
    return counts


def keyword_counts_fast(docs: list[str], stop_words: list[str]) -> dict[str, int]:
    """Same result as keyword_counts_slow, built in one pass with a stop-word set."""
    stop = {s.lower() for s in stop_words}
    return dict(Counter(w for doc in docs for w in (x.lower() for x in doc.split()) if w not in stop))


def parse_semver(v: str) -> tuple[int, int, int]:
    """'1.4.2' -> (1, 4, 2); ValueError on malformed input (no leading zeros)."""
    m = SEMVER.fullmatch(v.strip())
    if not m:
        raise ValueError(f"not a semantic version: {v!r}")
    major, minor, patch = (int(g) for g in m.groups())
    return major, minor, patch


def bump(version: str, part: str) -> str:
    """Increment major/minor/patch, resetting lower parts."""
    major, minor, patch = parse_semver(version)
    if part == "major":
        return f"{major + 1}.0.0"
    if part == "minor":
        return f"{major}.{minor + 1}.0"
    if part == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError("part must be major, minor or patch")


def make_logger(name: str, stream, level: int = logging.INFO) -> logging.Logger:
    """Logger writing 'LEVEL name: message' to stream; idempotent (no duplicate handlers)."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    if not any(getattr(h, "_semester6", False) for h in logger.handlers):
        handler = logging.StreamHandler(stream)
        handler.setFormatter(logging.Formatter("%(levelname)s %(name)s: %(message)s"))
        handler._semester6 = True  # type: ignore[attr-defined]
        logger.addHandler(handler)
    return logger


def amdahl_speedup(fraction: float, factor: float) -> float:
    """Overall speed-up when `fraction` of run time is made `factor` times faster."""
    if not 0 <= fraction <= 1 or factor <= 0:
        raise ValueError("fraction in [0,1], factor > 0")
    return 1 / ((1 - fraction) + fraction / factor)
