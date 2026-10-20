"""Every number quoted in the PM lessons and case studies is asserted here."""
import math

import pytest

from pm_tools import (EVM, Activity, all_paths, cpm, crash_schedule, discounted_payback, duration_for_probability, irr,
                      level_resources, npv,
                      payback_period, percent_complete_ev, pert, pert_project, prob_complete_by,
                      resource_profile, roi, shifts_feasible, topological_order)

# Case PM-CASE-01 network (weeks)
REG = [Activity("A", 3), Activity("B", 4, ("A",)), Activity("C", 2, ("A",)), Activity("D", 5, ("A",)),
       Activity("E", 6, ("B", "C")), Activity("F", 4, ("B",)), Activity("G", 3, ("E", "F")),
       Activity("H", 2, ("D",)), Activity("I", 2, ("C", "H")), Activity("J", 2, ("G", "I")), Activity("K", 1, ("J",))]
REG_PERT = {"A": (2, 3, 4), "B": (3, 4, 6), "C": (1, 2, 3), "D": (3, 5, 10), "E": (4, 6, 11), "F": (3, 4, 5),
            "G": (2, 3, 5), "H": (1, 2, 3), "I": (1, 2, 4), "J": (1, 2, 3), "K": (1, 1, 1)}
REG_DEV = {"A": 2, "B": 2, "C": 2, "D": 0, "E": 3, "F": 2, "G": 3, "H": 1, "I": 2, "J": 2, "K": 1}


def test_cpm_registration_case():
    s = cpm(REG)
    assert s.duration == 19 and s.critical == ["A", "B", "E", "G", "J", "K"]
    table = {n: (s.es[n], s.ef[n], s.ls[n], s.lf[n], s.total_float[n], s.free_float[n]) for n in s.order}
    assert table["C"] == (3, 5, 5, 7, 2, 2)
    assert table["D"] == (3, 8, 7, 12, 4, 0)
    assert table["F"] == (7, 11, 9, 13, 2, 2)
    assert table["H"] == (8, 10, 12, 14, 4, 0)
    assert table["I"] == (10, 12, 14, 16, 4, 4)
    assert table["K"] == (18, 19, 18, 19, 0, 0)
    paths = [("-".join(p), length) for p, length in all_paths(REG)]
    assert paths == [("A-B-E-G-J-K", 19), ("A-B-F-G-J-K", 17), ("A-C-E-G-J-K", 17), ("A-D-H-I-J-K", 15),
                     ("A-C-I-J-K", 10)]


def test_cpm_errors():
    with pytest.raises(ValueError):
        cpm([Activity("X", 1, ("Y",))])
    with pytest.raises(ValueError):
        cpm([Activity("X", 1, ("Y",)), Activity("Y", 1, ("X",))])
    assert topological_order({"B": Activity("B", 1, ("A",)), "A": Activity("A", 1)}) == ["A", "B"]


def test_pert_registration_case():
    assert pert(2, 3, 4) == (3.0, 1 / 3)
    te, sd = pert(4, 6, 11)
    assert te == 6.5 and round(sd, 4) == 1.1667
    te, sd = pert_project(REG_PERT, ["A", "B", "E", "G", "J", "K"])
    assert round(te, 4) == 19.8333 and round(sd ** 2, 4) == 2.0833 and round(sd, 4) == 1.4434
    assert [round(prob_complete_by(t, te, sd), 4) for t in (19, 20, 21, 22)] == [0.2819, 0.546, 0.7905, 0.9333]
    assert round(duration_for_probability(0.95, te, sd), 2) == 22.21
    assert round(duration_for_probability(0.90, te, sd), 2) == 21.68
    with pytest.raises(ValueError):
        pert(5, 3, 4)


def test_evm_example():
    e = EVM(bac=60_000_000, pv=30_000_000, ev=25_000_000, ac=28_000_000)
    assert (e.sv, e.cv) == (-5_000_000, -3_000_000)
    assert round(e.spi, 4) == 0.8333 and round(e.cpi, 4) == 0.8929
    assert e.eac_cpi == 67_200_000 and e.eac_atypical == 63_000_000 and round(e.eac_cpi_spi) == 75_040_000
    assert e.etc == 39_200_000 and e.vac == -7_200_000 and round(e.tcpi_bac, 4) == 1.0938
    assert round(e.tcpi_eac(e.eac_cpi), 4) == round(e.cpi, 4)   # meeting EAC = continuing at current CPI


def test_ev_from_percent_complete():
    budgets = {"design": 8_000_000, "build": 20_000_000, "test": 6_000_000}
    assert percent_complete_ev(budgets, {"design": 1.0, "build": 0.5}) == 18_000_000


def test_financial_appraisal():
    flows = [-45e6, 18e6, 18e6, 18e6, 18e6]
    assert round(npv(0.12, flows)) == 9_672_288
    assert round(irr(flows), 4) == 0.2186
    assert payback_period(flows) == 2.5
    assert roi(72e6, 45e6) == 0.6
    assert payback_period([-10, 1, 1]) is None
    assert math.isclose(npv(irr(flows), flows), 0, abs_tol=1e-3)


def test_resource_profile_and_levelling():
    s = cpm(REG)
    assert resource_profile(s, REG, REG_DEV) == [2, 2, 2, 4, 4, 2, 2, 5, 6, 6, 7, 5, 3, 3, 3, 3, 2, 2, 1]
    peak, shift, profile = level_resources(s, REG, REG_DEV)
    assert peak == 5 and shift == {"H": 3, "I": 3}
    assert profile == [2, 2, 2, 4, 4, 2, 2, 5, 5, 5, 5, 4, 4, 5, 5, 3, 2, 2, 1]
    assert not shifts_feasible(s, REG, {"D": 1})       # D's float is shared with H: H would have to move too
    assert not shifts_feasible(s, REG, {"D": 1, "H": 1})   # ...and then I must move too (D-H-I share 4 weeks)
    assert shifts_feasible(s, REG, {"D": 1, "H": 1, "I": 1})
    assert not shifts_feasible(s, REG, {"I": 5})       # beyond total float: project would slip


def test_business_case_options_pm03():
    a = [-45e6, 18e6, 18e6, 18e6, 18e6]
    b = [-30e6, 8e6, 10e6, 12e6, 12e6]
    assert (round(npv(0.12, b)), round(irr(b), 4), payback_period(b), roi(42e6, 30e6)) == (1_282_376, 0.1387, 3.0, 0.4)
    assert round(discounted_payback(0.12, a), 2) == 3.15 and round(discounted_payback(0.12, b), 2) == 3.83
    assert [round(18e6 / 1.12 ** t) for t in range(1, 5)] == [16_071_429, 14_349_490, 12_812_044, 11_439_325]
    assert round(npv(0.18, a)) == 3_421_112 and round(npv(0.25, a)) == -2_491_200


def test_pm03_practice_answers():
    assert round(npv(0.10, [-20e6, 6e6, 8e6, 10e6])) == -420_736
    assert payback_period([-20e6, 6e6, 8e6, 10e6]) == 2.6
    assert round(npv(0.12, [-45e6] + [14.4e6] * 4)) == -1_262_169


CRASH = {"A": (2, 900_000), "B": (3, 600_000), "E": (4, 400_000), "G": (2, 700_000), "J": (1, 1_200_000),
         "F": (3, 300_000), "C": (1, 250_000)}


def test_crashing_pm06():
    steps, final, total = crash_schedule(REG, CRASH, 15)
    assert steps == [(18, ("E",), 400_000), (17, ("E",), 400_000), (16, ("B",), 600_000), (15, ("G",), 700_000)]
    assert total == 2_100_000 and cpm(final).duration == 15
    steps, final, total = crash_schedule(REG, CRASH, 12)
    assert [s[0] for s in steps] == [18, 17, 16, 15, 14, 13] and total == 4_200_000
    assert cpm(final).duration == 13          # A-D-H-I-J-K = 13 cannot be crashed further (D, H, I fixed)


SMALL = [Activity("A", 2), Activity("B", 3, ("A",)), Activity("C", 4, ("A",)), Activity("D", 2, ("B", "C")),
         Activity("E", 1, ("D",))]


def test_pm05_pm06_practice_answers():
    s = cpm(SMALL)
    assert s.duration == 9 and s.critical == ["A", "C", "D", "E"] and s.total_float["B"] == 1
    steps, _final, total = crash_schedule(SMALL, {"A": (1, 500), "B": (2, 200), "C": (2, 300), "D": (1, 400)}, 7)
    assert steps == [(8, ("C",), 300), (7, ("D",), 400)] and total == 700
    late_f = [a if a.name != "F" else Activity("F", 7, ("B",)) for a in REG]
    assert cpm(late_f).duration == 20 and cpm(late_f).critical == ["A", "B", "F", "G", "J", "K"]
    late_d3 = [a if a.name != "D" else Activity("D", 8, ("A",)) for a in REG]
    assert cpm(late_d3).duration == 19 and cpm(late_d3).total_float["D"] == 1
    late_d5 = [a if a.name != "D" else Activity("D", 10, ("A",)) for a in REG]
    assert cpm(late_d5).duration == 20 and cpm(late_d5).critical == ["A", "D", "H", "I", "J", "K"]


def test_monte_carlo_shows_merge_bias():
    from pm_tools import monte_carlo
    runs = monte_carlo(REG, REG_PERT, runs=10_000, seed=2026)
    mean = sum(runs) / len(runs)
    p21 = sum(r <= 21 for r in runs) / len(runs)
    te, sd = pert_project(REG_PERT, ["A", "B", "E", "G", "J", "K"])
    assert 19.7 < mean < 20.1                       # build machine: 19.864
    assert 0.74 < p21 < prob_complete_by(21, te, sd)  # build machine: 0.7652 < analytic 0.7905


def test_pm07_practice_answers():
    from pm_tools import monte_carlo
    assert round(prob_complete_by(33, 30, 2), 4) == 0.9332
    te, sd = pert_project(REG_PERT, ["A", "B", "E", "G", "J", "K"])
    assert round(duration_for_probability(0.80, te, sd), 3) == 21.048
    narrower = dict(REG_PERT, D=(3, 5, 7))
    base = monte_carlo(REG, REG_PERT, 10_000, 2026)
    better = monte_carlo(REG, narrower, 10_000, 2026)
    assert sum(r <= 21 for r in better) > sum(r <= 21 for r in base)   # build machine: 7735 vs 7652


def test_resource_constrained_pm08():
    from pm_tools import resource_constrained
    end5, start5, prof5 = resource_constrained(REG, REG_DEV, 5)
    assert end5 == 19 and max(prof5) == 5                      # levelling within float suffices
    end4, start4, prof4 = resource_constrained(REG, REG_DEV, 4)
    assert end4 == 23 and max(prof4) <= 4                      # E (3) and F (2) can no longer overlap
    assert (start4["E"], start4["F"], start4["G"]) == (7, 13, 17)
    assert resource_constrained(REG, REG_DEV, 3)[0] == 27
    with pytest.raises(ValueError):
        resource_constrained(REG, REG_DEV, 2)                  # E needs 3 developers


def test_resource_leave_scenario_pm08():
    from pm_tools import resource_constrained
    end, start, _ = resource_constrained(REG, REG_DEV, 5, limit_at={8: 4, 9: 4})
    assert end == 20 and start["F"] == 10 and start["G"] == 14


REG_COST = {"A": 3e6, "B": 6e6, "C": 3e6, "D": 12e6, "E": 12e6, "F": 6e6, "G": 4.5e6, "H": 2e6, "I": 2.5e6,
            "J": 2.4e6, "K": 0.6e6}


def test_cost_baseline_pm09():
    from pm_tools import cost_baseline
    per, cum = cost_baseline(cpm(REG), REG, REG_COST)
    assert sum(REG_COST.values()) == 54e6 and round(cum[-1]) == 54_000_000
    assert [round(x) for x in cum] == [1_000_000, 2_000_000, 3_000_000, 8_400_000, 13_800_000, 17_700_000,
                                       21_600_000, 27_500_000, 32_000_000, 36_500_000, 41_250_000, 44_500_000,
                                       46_500_000, 48_000_000, 49_500_000, 51_000_000, 52_200_000, 53_400_000,
                                       54_000_000]
    assert round(per[3]) == 5_400_000                      # week 4: B, C, D all running
    assert round(npv(0.12, [-60e6] + [18e6] * 4)) == -5_327_712
    assert round(npv(0.12, [-60e6] + [22e6] * 4)) == 6_821_686 and round(irr([-60e6] + [22e6] * 4), 3) == 0.173


def test_case01_week10_evm_pm10():
    done = {"A": 1, "B": 1, "C": 1, "D": 1, "E": 0.4, "F": 0.5, "H": 1}
    ev = percent_complete_ev(REG_COST, done)
    ac = sum([3.2e6, 6.5e6, 2.8e6, 13.5e6, 6.0e6, 3.5e6, 2.2e6])
    assert (ev, ac) == (33_800_000, 37_700_000)
    e = EVM(bac=54e6, pv=36.5e6, ev=ev, ac=ac)
    assert (e.sv, e.cv) == (-2_700_000, -3_900_000)
    assert round(e.spi, 3) == 0.926 and round(e.cpi, 4) == 0.8966
    assert round(e.eac_cpi) == 60_230_769 and e.eac_atypical == 57_900_000 and round(e.eac_cpi_spi) == 62_030_564
    assert round(e.vac) == -6_230_769 and round(e.tcpi_bac, 4) == 1.2393 and round(e.tcpi_eac(60e6), 4) == 0.9058


CASE01_RISKS = {"R1": (0.3, 4e6), "R2": (0.5, 3e6), "R3": (0.2, 6e6), "R4": (0.4, 2.5e6), "R5": (0.25, 4.4e6)}


def test_risk_emv_and_decision_tree_pm11():
    from pm_tools import decision_value, emv
    values = emv(CASE01_RISKS)
    assert values == {"R1": 1.2e6, "R2": 1.5e6, "R3": 1.2e6, "R4": 1.0e6, "R5": 1.1e6}
    assert round(sum(values.values())) == 6_000_000          # = the contingency reserve in PM-09
    tree = ("decision", {"build in-house": ("chance", [(0.6, 54e6), (0.4, 66e6)]),
                         "buy package + customise": ("chance", [(0.7, 50e6), (0.3, 72e6)])})
    assert decision_value(tree) == (56_600_000, ["buy package + customise"])
    assert decision_value(("chance", [(0.6, 54e6), (0.4, 66e6)]))[0] == 58_800_000
    assert round(0.05 * 6e6 + 0.5e6) == 800_000              # R3 mitigated: residual EMV + response cost < 1.2 M
    with pytest.raises(ValueError):
        decision_value(("chance", [(0.5, 1), (0.4, 2)]))


def test_pm11_pilot_option():
    from pm_tools import decision_value
    tree = ("decision", {"pilot first": ("chance", [(0.7, 52e6), (0.3, 60.8e6)]),
                         "build in-house": ("chance", [(0.6, 54e6), (0.4, 66e6)]),
                         "buy package + customise": ("chance", [(0.7, 50e6), (0.3, 72e6)])})
    value, choice = decision_value(tree)
    assert round(value) == 54_640_000 and choice == ["pilot first"]


def test_pm12_to_pm16_helpers():
    from pm_tools import communication_channels, control_limits, fpif_final_price, fpif_pta, pareto, sprints_needed
    assert [communication_channels(n) for n in (5, 6, 10, 12)] == [10, 15, 45, 66]
    lcl, mean, ucl = control_limits([1.6, 1.8, 1.7, 1.9, 1.5, 1.8, 1.7, 2.0, 1.6, 1.8, 1.9, 1.7])
    assert (round(lcl, 3), round(mean, 3), round(ucl, 3)) == (1.316, 1.75, 2.184)
    rows = pareto({"validation errors": 42, "login problems": 18, "slow pages": 12, "wrong timetable": 9,
                   "UI confusion": 6, "other": 3})
    assert rows[:3] == [("validation errors", 42, 46.7), ("login problems", 18, 66.7), ("slow pages", 12, 80.0)]
    assert fpif_pta(40e6, 4e6, 48e6, 0.8) == 45e6
    assert [fpif_final_price(ac, 40e6, 4e6, 48e6, 0.8) for ac in (38e6, 42e6, 46e6)] == [42.4e6, 45.6e6, 48e6]
    assert sprints_needed(120, [18, 22, 20, 24]) == (5, 6, 7)


def test_pm14_practice():
    from pm_tools import fpif_final_price, fpif_pta
    assert round(fpif_pta(100, 10, 120, 0.7), 2) == 114.29
    assert round(fpif_final_price(110, 100, 10, 120, 0.7), 9) == 117.0
    assert 20 / 0.8 == 25 and 30 / 1.5 == 20          # make-or-buy break-even months (hosting; practice 3)


def test_pm16_agile_numbers():
    from pm_tools import sprints_needed
    assert sprints_needed(90, [15, 18, 21]) == (5, 5, 6)
    e = EVM(18e6, 9e6, 8.1e6, 9.6e6)
    assert round(e.spi, 2) == 0.90 and round(e.cpi, 2) == 0.84
    e = EVM(24e6, 12e6, 10.5e6, 13e6)
    assert e.spi == 0.875 and round(e.cpi, 3) == 0.808 and round(e.eac_cpi / 1e6, 1) == 29.7
