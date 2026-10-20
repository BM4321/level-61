"""Small, tested helpers for the cross-module notes (X-01 to X-07 and the integrated cases).

Each function is short on purpose: the notes show the idea, and the tests pin every number they quote.
"""
from __future__ import annotations

import heapq
import itertools
import math
from collections.abc import Callable, Iterable

# ---------- X-01 logic and sets ----------

def truth_table(fn: Callable[..., bool], names: list[str]) -> list[tuple[dict[str, bool], bool]]:
    rows = []
    for values in itertools.product([False, True], repeat=len(names)):
        env = dict(zip(names, values))
        rows.append((env, bool(fn(**env))))
    return rows


def equivalent(f: Callable[..., bool], g: Callable[..., bool], names: list[str]) -> tuple[bool, list[dict[str, bool]]]:
    """Exhaustive check: (True, []) or (False, every assignment where f and g differ)."""
    diffs = [env for env, fv in truth_table(f, names) if fv != bool(g(**env))]
    return (not diffs, diffs)


# ---------- X-02 graphs ----------

Graph = dict[str, dict[str, float]]


def undirected(edges: Iterable[tuple[str, str, float]]) -> Graph:
    g: Graph = {}
    for a, b, w in edges:
        g.setdefault(a, {})[b] = w
        g.setdefault(b, {})[a] = w
    return g


def dijkstra(graph: Graph, source: str) -> tuple[dict[str, float], dict[str, str]]:
    dist = {source: 0.0}
    prev: dict[str, str] = {}
    heap = [(0.0, source)]
    done: set[str] = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in graph.get(u, {}).items():
            if w < 0:
                raise ValueError("Dijkstra needs non-negative weights")
            if d + w < dist.get(v, math.inf):
                dist[v], prev[v] = d + w, u
                heapq.heappush(heap, (d + w, v))
    return dist, prev


def path_to(prev: dict[str, str], source: str, target: str) -> list[str]:
    path = [target]
    while path[-1] != source:
        if path[-1] not in prev:
            return []
        path.append(prev[path[-1]])
    return path[::-1]


def kruskal(edges: list[tuple[str, str, float]]) -> tuple[list[tuple[str, str, float]], float]:
    parent: dict[str, str] = {}

    def find(x: str) -> str:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    chosen = []
    for a, b, w in sorted(edges, key=lambda e: (e[2], e[0], e[1])):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            chosen.append((a, b, w))
    return chosen, sum(w for _, _, w in chosen)


def find_cycle(deps: dict[str, list[str]]) -> list[str]:
    """Return one dependency cycle (first node repeated at the end), or [] if the graph is acyclic."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {n: WHITE for n in deps}
    stack: list[str] = []

    def visit(n: str) -> list[str]:
        colour[n] = GREY
        stack.append(n)
        for m in deps.get(n, []):
            if colour.get(m, WHITE) == GREY:
                return stack[stack.index(m):] + [m]
            if colour.get(m, WHITE) == WHITE:
                found = visit(m)
                if found:
                    return found
        stack.pop()
        colour[n] = BLACK
        return []

    for n in sorted(deps):
        if colour[n] == WHITE:
            found = visit(n)
            if found:
                return found
    return []


def longest_path_dag(durations: dict[str, float], preds: dict[str, list[str]]) -> tuple[float, list[str]]:
    """Project duration as the longest path in an activity-on-node DAG (what CPM's forward pass computes)."""
    order, seen = [], set()

    def visit(n: str) -> None:
        if n in seen:
            return
        seen.add(n)
        for p in preds.get(n, []):
            visit(p)
        order.append(n)

    for n in sorted(durations):
        visit(n)
    finish: dict[str, float] = {}
    best_pred: dict[str, str | None] = {}
    for n in order:
        ps = preds.get(n, [])
        bp = max(ps, key=lambda p: (finish[p], p)) if ps else None
        finish[n], best_pred[n] = (finish[bp] if bp else 0.0) + durations[n], bp
    end = max(finish, key=lambda n: (finish[n], n))
    path = [end]
    while best_pred[path[-1]] is not None:
        path.append(best_pred[path[-1]])  # type: ignore[arg-type]
    return finish[end], path[::-1]


# ---------- X-04 quality ----------

def defect_removal_efficiency(found_before_release: int, found_after_release: int) -> float:
    total = found_before_release + found_after_release
    if total == 0:
        raise ValueError("no defects recorded")
    return found_before_release / total


def defect_density(defects: int, loc: int) -> float:
    """Defects per thousand lines of code (KLOC)."""
    return defects / (loc / 1000)


def cost_of_quality(prevention: float, appraisal: float, internal_failure: float,
                    external_failure: float) -> dict[str, float]:
    conformance = prevention + appraisal
    nonconformance = internal_failure + external_failure
    return {"conformance": conformance, "nonconformance": nonconformance,
            "total": conformance + nonconformance}


# ---------- X-05 security risk economics ----------

def rosi(ale_before: float, ale_after: float, annual_cost: float) -> float:
    """Return on security investment: (risk reduction - cost) / cost."""
    return (ale_before - ale_after - annual_cost) / annual_cost


# ---------- X-CASE-02 inventory ----------

def safety_stock(z: float, sd_daily_demand: float, lead_time_days: float) -> float:
    return z * sd_daily_demand * math.sqrt(lead_time_days)


def reorder_point(mean_daily_demand: float, lead_time_days: float, safety: float) -> float:
    return mean_daily_demand * lead_time_days + safety


def eoq(annual_demand: float, order_cost: float, holding_cost_per_unit_year: float) -> float:
    return math.sqrt(2 * annual_demand * order_cost / holding_cost_per_unit_year)
