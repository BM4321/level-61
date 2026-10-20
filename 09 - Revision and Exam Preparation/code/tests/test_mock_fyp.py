import math
from statistics import NormalDist

from fyp_tools import adjust_for_response_rate, cochran_n0, finite_correction, word_budget


def test_timing():
    weights = {"Problem and RQs": 2, "Literature and gap": 2, "Methodology": 3, "Design plan": 2,
               "Work plan and ethics": 2, "Summary": 1}
    assert word_budget(720, weights) == {"Problem and RQs": 120, "Literature and gap": 120, "Methodology": 180,
                                         "Design plan": 120, "Work plan and ethics": 120, "Summary": 60}
    assert 5 * 8 + 10 == 50                                                   # rubric total


def test_critique_sampling_numbers():
    n = finite_correction(cochran_n0(), 2400)
    assert n == 332 and adjust_for_response_rate(n, 0.5) == 664
    z = NormalDist().inv_cdf(0.975)
    margin = z * math.sqrt(0.25 / 100 * (2400 - 100) / (2400 - 1))
    assert round(margin * 100, 1) == 9.6
