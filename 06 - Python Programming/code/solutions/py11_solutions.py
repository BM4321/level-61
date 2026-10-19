"""PY-11 reference solutions (dicts, sets, comprehensions)."""
import string
from collections import Counter


def word_counts(text: str) -> dict[str, int]:
    """Lower-cased word frequencies with surrounding punctuation stripped."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        word = word.strip(".,!?;:\"'")
        if word:
            counts[word] = counts.get(word, 0) + 1
    return counts


def common(a: list, b: list) -> list:
    """Elements of a also in b, in a's order, without duplicates, O(n + m)."""
    b_set = set(b)
    seen = set()
    out = []
    for x in a:
        if x in b_set and x not in seen:
            seen.add(x)
            out.append(x)
    return out


def invert(d: dict) -> dict:
    """Map each value to a sorted list of the keys that had it."""
    out: dict = {}
    for k, v in d.items():
        out.setdefault(v, []).append(k)
    return {v: sorted(ks) for v, ks in out.items()}


def average_by_group(rows: list[tuple[str, str, float]]) -> dict[str, float]:
    """rows of (name, group, mark) -> {group: mean mark}."""
    totals: dict[str, list[float]] = {}
    for _, group, mark in rows:
        if group not in totals:
            totals[group] = [0, 0]
        totals[group][0] += mark
        totals[group][1] += 1
    return {g: s / c for g, (s, c) in totals.items()}


def squares_of_evens(xs: list[int]) -> list[int]:
    """[x*x for even x], via a comprehension."""
    return [x * x for x in xs if x % 2 == 0]


def passing(marks: dict[str, float], threshold: float = 50) -> dict[str, float]:
    """Sub-dict of entries with mark >= threshold."""
    return {name: mk for name, mk in marks.items() if mk >= threshold}


def most_frequent(xs: list):
    """Most common item, ties broken by first appearance; ValueError if empty."""
    if not xs:
        raise ValueError("empty input")
    counts = Counter(xs)
    return max(counts, key=counts.get)


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Indices (i, j), i < j, with nums[i] + nums[j] == target, in O(n); else None."""
    seen: dict[int, int] = {}
    for j, x in enumerate(nums):
        i = seen.get(target - x)
        if i is not None:
            return (i, j)
        seen[x] = j
    return None


def only_one_course(reg: dict[str, set[str]]) -> set[str]:
    """IDs that appear in exactly one course's set."""
    counts = Counter(sid for ids in reg.values() for sid in ids)
    return {sid for sid, c in counts.items() if c == 1}


def _words(text: str) -> set[str]:
    return {w.strip(string.punctuation) for w in text.casefold().split()} - {""}


def build_index(docs: dict[str, str]) -> dict[str, set[str]]:
    """Inverted index: word -> set of doc ids containing it."""
    index: dict[str, set[str]] = {}
    for doc_id, text in docs.items():
        for w in _words(text):
            index.setdefault(w, set()).add(doc_id)
    return index


def search(index: dict[str, set[str]], query: str) -> set[str]:
    """Doc ids containing ALL query words (case-insensitive)."""
    words = _words(query)
    if not words:
        return set()
    return set.intersection(*(index.get(w, set()) for w in words))
