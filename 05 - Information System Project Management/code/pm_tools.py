"""Project-management calculations for ITT06105 lessons: CPM, PERT, EVM, financial appraisal, levelling.

Standard library only. Every number quoted in the PM lessons is produced by these functions and
asserted in tests/test_pm_tools.py.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from statistics import NormalDist


# ------------------------------------------------------------------ CPM
@dataclass(frozen=True)
class Activity:
    name: str
    duration: float
    predecessors: tuple[str, ...] = ()


@dataclass(frozen=True)
class Schedule:
    es: dict[str, float]
    ef: dict[str, float]
    ls: dict[str, float]
    lf: dict[str, float]
    total_float: dict[str, float]
    free_float: dict[str, float]
    duration: float
    critical: list[str]          # critical activities in topological order
    order: list[str]


def topological_order(acts: dict[str, Activity]) -> list[str]:
    indeg = {a: 0 for a in acts}
    succ: dict[str, list[str]] = defaultdict(list)
    for a in acts.values():
        for p in a.predecessors:
            if p not in acts:
                raise ValueError(f"{a.name}: unknown predecessor {p}")
            succ[p].append(a.name)
            indeg[a.name] += 1
    ready = sorted(a for a, d in indeg.items() if d == 0)
    order = []
    while ready:
        n = ready.pop(0)
        order.append(n)
        for s in sorted(succ[n]):
            indeg[s] -= 1
            if indeg[s] == 0:
                ready.append(s)
        ready.sort()
    if len(order) != len(acts):
        raise ValueError("network contains a cycle")
    return order


def cpm(activities: list[Activity]) -> Schedule:
    """Activity-on-node critical path method with finish-to-start, zero-lag dependencies."""
    acts = {a.name: a for a in activities}
    order = topological_order(acts)
    succ: dict[str, list[str]] = defaultdict(list)
    for a in activities:
        for p in a.predecessors:
            succ[p].append(a.name)
    es, ef = {}, {}
    for n in order:
        es[n] = max((ef[p] for p in acts[n].predecessors), default=0.0)
        ef[n] = es[n] + acts[n].duration
    duration = max(ef.values())
    ls, lf = {}, {}
    for n in reversed(order):
        lf[n] = min((ls[s] for s in succ[n]), default=duration)
        ls[n] = lf[n] - acts[n].duration
    tf = {n: round(ls[n] - es[n], 9) for n in order}
    ff = {n: round(min((es[s] for s in succ[n]), default=duration) - ef[n], 9) for n in order}
    critical = [n for n in order if abs(tf[n]) < 1e-9]
    return Schedule(es, ef, ls, lf, tf, ff, duration, critical, order)


def all_paths(activities: list[Activity]) -> list[tuple[list[str], float]]:
    """Every start-to-end path with its length (small networks only), longest first."""
    acts = {a.name: a for a in activities}
    succ: dict[str, list[str]] = defaultdict(list)
    for a in activities:
        for p in a.predecessors:
            succ[p].append(a.name)
    starts = [a.name for a in activities if not a.predecessors]
    paths = []

    def walk(n, path):
        path = path + [n]
        if not succ[n]:
            paths.append((path, sum(acts[x].duration for x in path)))
        for s in succ[n]:
            walk(s, path)

    for s in starts:
        walk(s, [])
    return sorted(paths, key=lambda p: (-p[1], p[0]))


# ------------------------------------------------------------------ PERT
def pert(o: float, m: float, p: float) -> tuple[float, float]:
    """Beta-PERT expected time and standard deviation: te = (o + 4m + p) / 6, sd = (p - o) / 6."""
    if not o <= m <= p:
        raise ValueError("need optimistic <= most likely <= pessimistic")
    return (o + 4 * m + p) / 6, (p - o) / 6


def pert_project(estimates: dict[str, tuple[float, float, float]], critical: list[str]) -> tuple[float, float]:
    """Project expected duration and SD along a critical path (assumes independent activities)."""
    te = sum(pert(*estimates[a])[0] for a in critical)
    var = sum(pert(*estimates[a])[1] ** 2 for a in critical)
    return te, math.sqrt(var)


def prob_complete_by(target: float, mean: float, sd: float) -> float:
    """P(T <= target) under the normal approximation (central limit theorem)."""
    return NormalDist(mean, sd).cdf(target)


def duration_for_probability(prob: float, mean: float, sd: float) -> float:
    return NormalDist(mean, sd).inv_cdf(prob)


# ------------------------------------------------------------------ EVM
@dataclass(frozen=True)
class EVM:
    bac: float
    pv: float
    ev: float
    ac: float

    @property
    def sv(self): return self.ev - self.pv

    @property
    def cv(self): return self.ev - self.ac

    @property
    def spi(self): return self.ev / self.pv

    @property
    def cpi(self): return self.ev / self.ac

    @property
    def eac_cpi(self):          # typical: future work at current cost efficiency
        return self.bac / self.cpi

    @property
    def eac_atypical(self):     # future work at budgeted rate
        return self.ac + (self.bac - self.ev)

    @property
    def eac_cpi_spi(self):      # schedule pressure also affects cost
        return self.ac + (self.bac - self.ev) / (self.cpi * self.spi)

    @property
    def etc(self): return self.eac_cpi - self.ac

    @property
    def vac(self): return self.bac - self.eac_cpi

    @property
    def tcpi_bac(self): return (self.bac - self.ev) / (self.bac - self.ac)

    def tcpi_eac(self, eac: float): return (self.bac - self.ev) / (eac - self.ac)


def percent_complete_ev(budgets: dict[str, float], complete: dict[str, float]) -> float:
    """EV = sum(budget_i * fraction complete_i)."""
    return sum(budgets[k] * complete.get(k, 0.0) for k in budgets)


# ------------------------------------------------------------------ financial appraisal
def npv(rate: float, cashflows: list[float]) -> float:
    """cashflows[0] at time 0 (usually negative investment), then one per period."""
    return sum(cf / (1 + rate) ** t for t, cf in enumerate(cashflows))


def irr(cashflows: list[float], lo: float = -0.99, hi: float = 10.0, tol: float = 1e-10) -> float:
    """Internal rate of return by bisection (assumes one sign change)."""
    f_lo, f_hi = npv(lo, cashflows), npv(hi, cashflows)
    if f_lo * f_hi > 0:
        raise ValueError("IRR not bracketed")
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cashflows)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2


def payback_period(cashflows: list[float]) -> float | None:
    """Simple payback (undiscounted), interpolated within the period; None if never paid back."""
    cum = cashflows[0]
    for t in range(1, len(cashflows)):
        if cum + cashflows[t] >= 0:
            return t - 1 + (-cum) / cashflows[t]
        cum += cashflows[t]
    return None


def discounted_payback(rate: float, cashflows: list[float]) -> float | None:
    """Payback using discounted cash flows (interpolated); None if never paid back within the horizon."""
    return payback_period([cf / (1 + rate) ** t for t, cf in enumerate(cashflows)])


def roi(total_benefits: float, total_costs: float) -> float:
    return (total_benefits - total_costs) / total_costs


# ------------------------------------------------------------------ resources
def resource_profile(schedule: Schedule, activities: list[Activity], demand: dict[str, int],
                     shift: dict[str, float] | None = None) -> list[int]:
    """Units of one resource needed in each whole time period, given start times (ES + optional shift)."""
    acts = {a.name: a for a in activities}
    shift = shift or {}
    horizon = int(math.ceil(max(schedule.es[n] + shift.get(n, 0) + acts[n].duration for n in acts)))
    profile = [0] * horizon
    for n, a in acts.items():
        start = int(schedule.es[n] + shift.get(n, 0))
        for t in range(start, start + int(a.duration)):
            profile[t] += demand.get(n, 0)
    return profile


def shifts_feasible(schedule: Schedule, activities: list[Activity], shift: dict[str, float]) -> bool:
    """Check precedence and the project end date after delaying activities by `shift` periods."""
    acts = {a.name: a for a in activities}
    start = {n: schedule.es[n] + shift.get(n, 0) for n in acts}
    if any(start[n] + acts[n].duration > schedule.duration for n in acts):
        return False
    return all(start[n] >= start[p] + acts[p].duration for n in acts for p in acts[n].predecessors)


def level_resources(schedule: Schedule, activities: list[Activity], demand: dict[str, int]):
    """Resource LEVELLING within float (project end unchanged): exhaustive search, small networks only.

    Returns (minimum peak, shifts achieving it with the fewest total delay periods, profile).
    """
    from itertools import product

    movable = [n for n in schedule.order if schedule.total_float[n] > 0]
    ranges = [range(int(schedule.total_float[n]) + 1) for n in movable]
    best = None
    for combo in product(*ranges):
        shift = {n: d for n, d in zip(movable, combo) if d}
        if not shifts_feasible(schedule, activities, shift):
            continue
        prof = resource_profile(schedule, activities, demand, shift)
        key = (max(prof), sum(shift.values()), sorted(shift.items()))
        if best is None or key < best[0]:
            best = (key, shift, prof)
    assert best is not None
    return best[0][0], best[1], best[2]


def crash_schedule(activities: list[Activity], crash: dict[str, tuple[float, float]], target: float):
    """Crash one period at a time, choosing the cheapest set of activities that shortens EVERY critical path.

    crash: name -> (minimum duration, cost per period of shortening). Small networks only (subset search).
    Returns (list of steps (duration_after, activities_shortened, step_cost), final activities, total cost).
    """
    from itertools import combinations

    current = {a.name: a for a in activities}
    steps, total = [], 0.0
    while True:
        sched = cpm(list(current.values()))
        if sched.duration <= target:
            return steps, list(current.values()), total
        paths = [set(p) for p, length in all_paths(list(current.values())) if abs(length - sched.duration) < 1e-9]
        candidates = [n for n in sched.critical if n in crash and current[n].duration > crash[n][0]]
        best = None
        for k in range(1, len(candidates) + 1):
            for combo in combinations(candidates, k):
                if all(path & set(combo) for path in paths):
                    cost = sum(crash[n][1] for n in combo)
                    if best is None or cost < best[0]:
                        best = (cost, combo)
        if best is None:
            return steps, list(current.values()), total      # cannot crash further
        cost, combo = best
        for n in combo:
            a = current[n]
            current[n] = Activity(a.name, a.duration - 1, a.predecessors)
        total += cost
        steps.append((cpm(list(current.values())).duration, combo, cost))
