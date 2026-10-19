"""Discrete-mathematics verification toolkit (GST06106).

Use it to CHECK answers you have worked out by hand, never instead of working them out.
Python 3.10+, standard library only.

    python -c "from dm_tools import *; print_truth_table('p -> q', ['p', 'q'])"
"""
from __future__ import annotations

import itertools
import math
import re
from collections.abc import Callable, Hashable, Iterable
from fractions import Fraction

# ---------------------------------------------------------------- logic (DM-01..04, DM-17)
_TOKEN_RE = re.compile(r"\s*(<->|->|\(|\)|[A-Za-z_][A-Za-z0-9_]*)")


def _tokenize(expr: str) -> list[str]:
    pos, tokens = 0, []
    expr = expr.strip()
    while pos < len(expr):
        m = _TOKEN_RE.match(expr, pos)
        if not m:
            raise ValueError(f"cannot parse near {expr[pos:]!r}")
        tokens.append(m.group(1))
        pos = m.end()
        while pos < len(expr) and expr[pos].isspace():
            pos += 1
    return tokens


def _parse(tokens: list[str]):
    """Recursive-descent parser. Precedence (high->low): not, and, xor, or, ->, <->.

    '->' is right-associative (p -> q -> r means p -> (q -> r)). Constants: T, F.
    Returns a nested tuple AST, e.g. ('->', ('var', 'p'), ('var', 'q')).
    """
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def take(expected=None):
        nonlocal pos
        tok = peek()
        if tok is None or (expected and tok != expected):
            raise ValueError(f"expected {expected or 'token'}, got {tok!r}")
        pos += 1
        return tok

    def iff():
        left = imp()
        while peek() == "<->":
            take()
            left = ("<->", left, imp())
        return left

    def imp():
        left = disj()
        if peek() == "->":
            take()
            return ("->", left, imp())          # right-associative
        return left

    def disj():
        left = xor()
        while peek() == "or":
            take()
            left = ("or", left, xor())
        return left

    def xor():
        left = conj()
        while peek() == "xor":
            take()
            left = ("xor", left, conj())
        return left

    def conj():
        left = neg()
        while peek() == "and":
            take()
            left = ("and", left, neg())
        return left

    def neg():
        if peek() == "not":
            take()
            return ("not", neg())
        return atom()

    def atom():
        tok = peek()
        if tok == "(":
            take("(")
            node = iff()
            take(")")
            return node
        if tok in ("T", "F"):
            take()
            return ("const", tok == "T")
        if tok is None or tok in ("and", "or", "xor", "not", "->", "<->", ")"):
            raise ValueError(f"unexpected {tok!r}")
        take()
        return ("var", tok)

    tree = iff()
    if pos != len(tokens):
        raise ValueError(f"unexpected trailing tokens {tokens[pos:]}")
    return tree


def _eval(node, env: dict[str, bool]) -> bool:
    kind = node[0]
    if kind == "var":
        return bool(env[node[1]])
    if kind == "const":
        return node[1]
    if kind == "not":
        return not _eval(node[1], env)
    a, b = _eval(node[1], env), _eval(node[2], env)
    return {"and": a and b, "or": a or b, "xor": a != b, "->": (not a) or b, "<->": a == b}[kind]


def evaluate(expr: str, env: dict[str, bool]) -> bool:
    """Evaluate a propositional formula using and, or, xor, not, ->, <->, T, F and parentheses."""
    return _eval(_parse(_tokenize(expr)), env)


def truth_table(expr: str, variables: list[str]) -> list[tuple[tuple[bool, ...], bool]]:
    rows = []
    for values in itertools.product([True, False], repeat=len(variables)):
        rows.append((values, evaluate(expr, dict(zip(variables, values)))))
    return rows


def print_truth_table(expr: str, variables: list[str]) -> None:
    head = " ".join(variables) + " | " + expr
    print(head)
    print("-" * len(head))
    for values, result in truth_table(expr, variables):
        print(" ".join("T" if v else "F" for v in values) + " | " + ("T" if result else "F"))


def is_tautology(expr: str, variables: list[str]) -> bool:
    return all(r for _, r in truth_table(expr, variables))


def is_contradiction(expr: str, variables: list[str]) -> bool:
    return not any(r for _, r in truth_table(expr, variables))


def equivalent(e1: str, e2: str, variables: list[str]) -> bool:
    return all(evaluate(e1, dict(zip(variables, v))) == evaluate(e2, dict(zip(variables, v)))
               for v in itertools.product([True, False], repeat=len(variables)))


def valid_argument(premises: list[str], conclusion: str, variables: list[str]) -> bool:
    """Valid iff every row making all premises true also makes the conclusion true."""
    for values in itertools.product([True, False], repeat=len(variables)):
        env = dict(zip(variables, values))
        if all(evaluate(p, env) for p in premises) and not evaluate(conclusion, env):
            return False
    return True


def minterms(expr: str, variables: list[str]) -> list[int]:
    """Indices (binary, first variable = most significant) of rows where expr is true."""
    out = []
    for i, values in enumerate(itertools.product([False, True], repeat=len(variables))):
        if evaluate(expr, dict(zip(variables, values))):
            out.append(i)
    return out


# ---------------------------------------------------------------- sets (DM-06)
def power_set(s: Iterable) -> list[frozenset]:
    items = list(s)
    return [frozenset(c) for r in range(len(items) + 1) for c in itertools.combinations(items, r)]


def cartesian(*sets: Iterable) -> set[tuple]:
    return set(itertools.product(*sets))


# ---------------------------------------------------------------- relations (DM-10)
def is_reflexive(rel: set[tuple], domain: Iterable) -> bool:
    return all((a, a) in rel for a in domain)


def is_symmetric(rel: set[tuple]) -> bool:
    return all((b, a) in rel for a, b in rel)


def is_antisymmetric(rel: set[tuple]) -> bool:
    return all(a == b or (b, a) not in rel for a, b in rel)


def is_transitive(rel: set[tuple]) -> bool:
    return all((a, d) in rel for a, b in rel for c, d in rel if b == c)


def equivalence_classes(domain: Iterable[Hashable], related: Callable[[object, object], bool]) -> list[set]:
    classes: list[set] = []
    for x in domain:
        for cls in classes:
            if related(x, next(iter(cls))):
                cls.add(x)
                break
        else:
            classes.append({x})
    return classes


# ---------------------------------------------------------------- functions (DM-07)
def is_injective(f: dict) -> bool:
    return len(set(f.values())) == len(f)


def is_surjective(f: dict, codomain: Iterable) -> bool:
    return set(codomain) <= set(f.values())


def count_functions(m: int, n: int) -> dict[str, int]:
    """Numbers of all / injective / surjective functions from an m-set to an n-set."""
    surj = sum((-1) ** k * math.comb(n, k) * (n - k) ** m for k in range(n + 1))
    return {"all": n ** m, "injective": math.perm(n, m) if m <= n else 0, "surjective": surj}


# ---------------------------------------------------------------- counting (DM-11..13, DM-18)
def perm(n: int, r: int) -> int:
    return math.perm(n, r)


def comb(n: int, r: int) -> int:
    return math.comb(n, r)


def multiset_perm(counts: Iterable[int]) -> int:
    """Arrangements of a word with repeated letters, e.g. MISSISSIPPI -> [1, 4, 4, 2]."""
    counts = list(counts)
    total = math.factorial(sum(counts))
    for c in counts:
        total //= math.factorial(c)
    return total


def combinations_with_repetition(n: int, r: int) -> int:
    """Stars and bars: choose r items from n kinds with repetition."""
    return math.comb(n + r - 1, r)


def derangements(n: int) -> int:
    d = [1, 0]
    for k in range(2, n + 1):
        d.append((k - 1) * (d[k - 1] + d[k - 2]))
    return d[n]


def count_divisible(limit: int, divisors: list[int]) -> int:
    """How many of 1..limit are divisible by at least one divisor (inclusion-exclusion)."""
    total = 0
    for r in range(1, len(divisors) + 1):
        for combo in itertools.combinations(divisors, r):
            lcm = math.lcm(*combo)
            total += (-1) ** (r + 1) * (limit // lcm)
    return total


def binomial_coefficients(n: int) -> list[int]:
    return [math.comb(n, k) for k in range(n + 1)]


def probability(favourable: int, total: int) -> Fraction:
    return Fraction(favourable, total)


# ---------------------------------------------------------------- recurrences (DM-14)
def iterate_recurrence(coeffs: list[int], initial: list[int], n: int, f: Callable[[int], int] = lambda k: 0) -> list[int]:
    """a_k = coeffs[0]*a_{k-1} + coeffs[1]*a_{k-2} + ... + f(k); returns a_0..a_n."""
    a = list(initial)
    for k in range(len(initial), n + 1):
        a.append(sum(c * a[k - 1 - i] for i, c in enumerate(coeffs)) + f(k))
    return a[: n + 1]


# ---------------------------------------------------------------- graphs (DM-15..16)
def degrees(edges: list[tuple]) -> dict:
    deg: dict = {}
    for u, v in edges:
        deg[u] = deg.get(u, 0) + 1
        deg[v] = deg.get(v, 0) + 1
    return deg


def is_connected(vertices: Iterable, edges: list[tuple]) -> bool:
    vertices = list(vertices)
    if not vertices:
        return True
    adj: dict = {v: set() for v in vertices}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    seen, stack = {vertices[0]}, [vertices[0]]
    while stack:
        for w in adj[stack.pop()]:
            if w not in seen:
                seen.add(w)
                stack.append(w)
    return len(seen) == len(vertices)


def euler_status(vertices: Iterable, edges: list[tuple]) -> str:
    """'circuit', 'path', or 'none' for an undirected multigraph (connected on non-isolated vertices)."""
    deg = degrees(edges)
    used = [v for v in vertices if deg.get(v, 0) > 0]
    if not is_connected(used, edges):
        return "none"
    odd = sum(1 for v in used if deg[v] % 2)
    return "circuit" if odd == 0 else "path" if odd == 2 else "none"


def kruskal(vertices: Iterable, weighted_edges: list[tuple]) -> tuple[int, list[tuple]]:
    """Minimum spanning tree: returns (total weight, edges as (u, v, w))."""
    parent = {v: v for v in vertices}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    tree, total = [], 0
    for u, v, w in sorted(weighted_edges, key=lambda e: (e[2], e[0], e[1])):
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            tree.append((u, v, w))
            total += w
    return total, tree
