import math

from pm_tools import (EVM, Activity, all_paths, communication_channels, cpm, decision_value, discounted_payback,
                      duration_for_probability, emv, irr, npv, pareto, payback_period, pert, pert_project,
                      prob_complete_by, roi, sprints_needed)

A = Activity
NET = [A("A", 3), A("B", 4, ("A",)), A("C", 2, ("A",)), A("D", 5, ("B",)), A("E", 3, ("C",)), A("F", 4, ("C",)),
       A("G", 2, ("D", "E")), A("H", 3, ("F",)), A("I", 2, ("G", "H"))]


def test_q1_cpm():
    s = cpm(NET)
    assert s.duration == 16 and s.critical == ["A", "B", "D", "G", "I"]
    table = {n: (s.es[n], s.ef[n], s.ls[n], s.lf[n], s.total_float[n]) for n in s.order}
    assert table == {"A": (0, 3, 0, 3, 0), "B": (3, 7, 3, 7, 0), "C": (3, 5, 5, 7, 2), "D": (7, 12, 7, 12, 0),
                     "E": (5, 8, 9, 12, 4), "F": (5, 9, 7, 11, 2), "G": (12, 14, 12, 14, 0),
                     "H": (9, 12, 11, 14, 2), "I": (14, 16, 14, 16, 0)}
    assert (s.free_float["E"], s.free_float["C"]) == (4, 0)
    assert sorted(d for _, d in all_paths(NET)) == [12, 14, 16]
    slipped = cpm([a if a.name != "F" else A("F", 7, ("C",)) for a in NET])
    assert slipped.duration == 17 and slipped.critical == ["A", "C", "F", "H", "I"]


def test_q2_pert():
    est = {"A": (2, 3, 4), "B": (3, 4, 8), "D": (4, 5, 9), "G": (1, 2, 3), "I": (1, 2, 4)}
    assert [round(pert(*est[k])[0], 2) for k in "ABDGI"] == [3.0, 4.5, 5.5, 2.0, 2.17]
    te, sd = pert_project(est, list("ABDGI"))
    assert (round(te, 2), round(sd, 2)) == (17.17, 1.36)
    assert round(prob_complete_by(18, te, sd), 2) == 0.73 and round(duration_for_probability(0.9, te, sd), 1) == 18.9


def test_q3_evm():
    e = EVM(120e6, 60e6, 54e6, 63e6)
    assert (e.sv, e.cv, e.spi, round(e.cpi, 3)) == (-6e6, -9e6, 0.9, 0.857)
    assert (round(e.eac_cpi), round(e.etc), round(e.vac)) == (140_000_000, 77_000_000, -20_000_000)
    assert round(e.tcpi_bac, 3) == 1.158 and e.eac_atypical == 129e6


def test_q4_business_case():
    cf = [-50e6, 15e6, 20e6, 20e6, 15e6]
    assert round(npv(0.12, cf) / 1e6, 2) == 3.11 and round(irr(cf), 3) == 0.149
    assert payback_period(cf) == 2.75 and round(discounted_payback(0.12, cf), 2) == 3.67
    assert roi(70e6, 50e6) == 0.4


def test_q5_risk():
    assert emv({"R1": (0.3, 10e6), "R2": (0.1, 40e6)}) == {"R1": 3e6, "R2": 4e6}
    tree = ("decision", {"Build in-house": ("chance", [(0.6, 30e6), (0.4, 45e6)]),
                         "Buy package": ("chance", [(0.8, 32e6), (0.2, 40e6)])})
    value, choice = decision_value(tree)
    assert math.isclose(value, 33.6e6) and choice == ["Buy package"]
    assert math.isclose(decision_value(tree[1]["Build in-house"])[0], 36e6)


def test_q6_people_quality_agile():
    assert communication_channels(12) == 66
    p = pareto({"requirements": 18, "design": 7, "coding": 25, "testing": 5, "deployment": 3, "documentation": 2})
    assert [(c, n) for c, n, _ in p[:2]] == [("coding", 25), ("requirements", 18)] and p[1][2] == 71.7
    assert sprints_needed(80, [18, 22, 20]) == (4, 4, 5)
