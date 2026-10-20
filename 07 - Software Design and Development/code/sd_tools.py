"""Small helpers used in SD lessons (requirements quality, traceability, metrics). Standard library only."""
from __future__ import annotations

import ast
import re

VAGUE = ["user-friendly", "user friendly", "fast", "quickly", "easy", "easily", "flexible", "robust",
         "efficient", "adequate", "appropriate", "as soon as possible", "etc", "and so on", "minimal",
         "state-of-the-art", "intuitive", "seamless", "secure"]
WEAK = ["should", "may", "might", "could", "can be", "if possible", "as appropriate"]


def requirement_smells(text: str) -> list[str]:
    """Flag common quality problems in a single requirement statement (heuristic, not a proof)."""
    t = " " + text.lower() + " "
    smells = []
    for w in VAGUE:
        if re.search(rf"(?<![a-z-]){re.escape(w)}(?![a-z-])", t):
            smells.append(f"vague term '{w}'")
    for w in WEAK:
        if re.search(rf"(?<![a-z]){re.escape(w)}(?![a-z])", t):
            smells.append(f"weak/optional wording '{w}'")
    if re.search(r"\band/or\b", t):
        smells.append("'and/or' is ambiguous")
    if " shall " in t and t.count(" shall ") > 1:
        smells.append("more than one 'shall' (split into separate requirements)")
    if re.search(r"\b(tbd|tba|to be decided)\b", t):
        smells.append("unresolved placeholder (TBD)")
    if re.search(r"\b(all|every|never|always)\b", t) and not re.search(r"\d", t):
        smells.append("universal quantifier without a measurable condition (check it is truly intended)")
    if " shall " not in t and " must " not in t:
        smells.append("no 'shall'/'must': unclear whether this is mandatory")
    return smells


def trace_gaps(requirements: dict[str, str], links: dict[str, list[str]], tests: set[str]) -> dict[str, list[str]]:
    """Find requirements with no linked test, and links pointing at unknown tests or requirements."""
    untested = sorted(r for r in requirements if not links.get(r))
    unknown_tests = sorted({t for ts in links.values() for t in ts if t not in tests})
    orphan_links = sorted(r for r in links if r not in requirements)
    orphan_tests = sorted(t for t in tests if all(t not in ts for ts in links.values()))
    return {"untested_requirements": untested, "unknown_tests": unknown_tests,
            "links_to_unknown_requirements": orphan_links, "tests_without_requirement": orphan_tests}


def _complexity(func: ast.AST) -> int:
    c = 1
    for sub in ast.walk(func):
        if isinstance(sub, (ast.If, ast.For, ast.While, ast.IfExp, ast.ExceptHandler, ast.AsyncFor, ast.comprehension)):
            c += 1
        elif isinstance(sub, ast.BoolOp):
            c += len(sub.values) - 1
        elif isinstance(sub, ast.Match):
            c += len(sub.cases) - 1
    return c


def cyclomatic_complexity(source: str) -> dict[str, int]:
    """McCabe complexity per function or method (1 + decision points), keyed 'Class.method' or 'function'."""
    result = {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result[node.name] = _complexity(node)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    result[f"{node.name}.{item.name}"] = _complexity(item)
    return result
