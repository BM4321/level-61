"""Small, tested research-method calculators for the Final Year Project I lessons (CST06103).

These support planning (sample sizes, reliability, simple descriptive statistics). They are teaching aids:
check the method your supervisor and department expect, and report the formula you used.
"""
from __future__ import annotations

import math
from statistics import NormalDist, mean, pvariance, stdev


def cochran_n0(confidence: float = 0.95, p: float = 0.5, margin: float = 0.05) -> float:
    """Cochran's sample size for a proportion, infinite population: n0 = z^2 p (1-p) / e^2."""
    z = NormalDist().inv_cdf(1 - (1 - confidence) / 2)
    return z * z * p * (1 - p) / (margin * margin)


def finite_correction(n0: float, population: int) -> int:
    """Finite population correction: n = n0 / (1 + (n0 - 1) / N), rounded up."""
    return math.ceil(n0 / (1 + (n0 - 1) / population))


def yamane(population: int, margin: float = 0.05) -> int:
    """Yamane (1967) simplified formula n = N / (1 + N e^2), rounded up (assumes 95% confidence, p = 0.5)."""
    return math.ceil(population / (1 + population * margin * margin))


def adjust_for_response_rate(n: int, response_rate: float) -> int:
    """Number of invitations needed to expect n responses."""
    return math.ceil(n / response_rate)


def cronbach_alpha(items: list[list[float]]) -> float:
    """Internal-consistency reliability. items[i][r] = score of respondent r on item i (k >= 2 items)."""
    k = len(items)
    if k < 2:
        raise ValueError("need at least two items")
    n = len(items[0])
    if any(len(col) != n for col in items):
        raise ValueError("every item needs the same number of respondents")
    totals = [sum(col[r] for col in items) for r in range(n)]
    item_var = sum(pvariance(col) for col in items)
    return k / (k - 1) * (1 - item_var / pvariance(totals))


def likert_summary(responses: list[int], scale: int = 5) -> dict[str, float]:
    """Median, mode, mean, % agree (top two boxes) for one Likert item. Report the median for ordinal data."""
    s = sorted(responses)
    n = len(s)
    median = s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
    mode = max(range(1, scale + 1), key=lambda v: (s.count(v), -v))
    agree = sum(1 for r in s if r >= scale - 1) / n
    return {"n": n, "median": median, "mode": mode, "mean": round(mean(s), 2),
            "sd": round(stdev(s), 2) if n > 1 else 0.0, "pct_agree": round(100 * agree, 1)}


def sus_score(answers: list[int]) -> float:
    """System Usability Scale (10 items, 1-5): odd items contribute (x-1), even items (5-x); total x 2.5."""
    if len(answers) != 10 or not all(1 <= a <= 5 for a in answers):
        raise ValueError("SUS needs 10 answers on a 1-5 scale")
    raw = sum((a - 1) if i % 2 == 0 else (5 - a) for i, a in enumerate(answers))
    return raw * 2.5


def boolean_query(concepts: list[list[str]]) -> str:
    """Combine synonym groups: OR within a concept, AND between concepts; quote multi-word phrases."""
    def term(t: str) -> str:
        return f'"{t}"' if " " in t and not t.endswith("*") else t
    groups = []
    for synonyms in concepts:
        if not synonyms:
            raise ValueError("empty concept group")
        inner = " OR ".join(term(s) for s in synonyms)
        groups.append(f"({inner})" if len(synonyms) > 1 else inner)
    return " AND ".join(groups)


_DOI = __import__("re").compile(r"^10\.\d{4,9}/\S+$")


def looks_like_doi(text: str) -> bool:
    """Syntax check only. A well-formed DOI can still be fake: resolve it at https://doi.org/ and read the paper."""
    return bool(_DOI.match(text.strip()))


_CITE = __import__("re").compile(
    r"\b([A-Z][A-Za-z'\-]+)(?: et al\.| (?:and|&) [A-Z][A-Za-z'\-]+)?,? \(?(\d{4}[a-z]?)\)?")


def citation_crosscheck(body: str, references: list[str]) -> dict[str, list[str]]:
    """Author-year consistency check: citations with no reference entry, and references never cited.

    Keys are 'Surname Year' of the FIRST author. A match proves only consistency, never that the source exists.
    """
    cited = {f"{m.group(1)} {m.group(2)}" for m in _CITE.finditer(body)}
    listed = {}
    for ref in references:
        m = __import__("re").match(r"\s*([A-Z][A-Za-z'\-]+),.*?\((\d{4}[a-z]?)\)", ref)
        if not m:
            raise ValueError(f"cannot parse reference: {ref!r}")
        listed[f"{m.group(1)} {m.group(2)}"] = ref
    return {"missing_from_references": sorted(cited - listed.keys()),
            "never_cited": sorted(listed.keys() - cited)}


_IDENTIFIERS = {
    "email": r"[\w.+-]+@[\w-]+\.[\w.-]+",
    "phone": r"(?:\+\d{1,3}[ -]?)?\d{3}[ -]?\d{3}[ -]?\d{3,4}\b",
    "student_id": r"\b[A-Z]{2,4}/\d{2,4}/\d{3,6}\b",
}


def identifier_scan(text: str, names: list[str] = ()) -> dict[str, int]:
    """Count likely direct identifiers in a transcript before it is shared. A zero count is not proof of anonymity."""
    import re
    counts = {k: len(re.findall(p, text)) for k, p in _IDENTIFIERS.items()}
    counts["known_names"] = sum(len(re.findall(rf"\b{re.escape(n)}\b", text)) for n in names)
    return counts


ALIGNMENT_FIELDS = ("problem", "rq", "objective", "method", "evaluation")


def alignment_gaps(rows: list[dict[str, str]]) -> list[str]:
    """Report empty cells in a problem-RQ-objective-method-evaluation matrix, and RQs or objectives used twice."""
    gaps = []
    for i, row in enumerate(rows, 1):
        label = row.get("rq") or f"row {i}"
        gaps += [f"{label}: no {f}" for f in ALIGNMENT_FIELDS if not row.get(f, "").strip()]
    for f in ("rq", "objective"):
        seen = [r[f] for r in rows if r.get(f, "").strip()]
        gaps += [f"{v}: appears in {seen.count(v)} rows" for v in sorted(set(seen)) if seen.count(v) > 1]
    return gaps


def word_budget(total: int, weights: dict[str, float]) -> dict[str, int]:
    """Split a word limit across sections in proportion to weights; largest-remainder rounding keeps the exact total."""
    if total < 0 or not weights or any(w < 0 for w in weights.values()) or sum(weights.values()) == 0:
        raise ValueError("need a non-negative total and non-negative weights with a positive sum")
    s = sum(weights.values())
    raw = {k: total * w / s for k, w in weights.items()}
    out = {k: int(v) for k, v in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - out[k], reverse=True)[: total - sum(out.values())]:
        out[k] += 1
    return out
