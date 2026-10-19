"""Self-tests of the toolkit against well-known results."""
from dm_tools import *  # noqa: F403


def test_logic():
    assert is_tautology("p or not p", ["p"])
    assert equivalent("not (p and q)", "(not p) or (not q)", ["p", "q"])
    assert equivalent("(p -> q)", "(not p) or q", ["p", "q"])
    assert valid_argument(["(p -> q)", "p"], "q", ["p", "q"])          # modus ponens
    assert not valid_argument(["(p -> q)", "q"], "p", ["p", "q"])      # affirming the consequent


def test_precedence():
    assert equivalent("not p -> q", "(not p) -> q", ["p", "q"])
    assert equivalent("p and q -> r", "(p and q) -> r", ["p", "q", "r"])
    assert equivalent("p -> q -> r", "p -> (q -> r)", ["p", "q", "r"])
    assert not equivalent("p -> q -> r", "(p -> q) -> r", ["p", "q", "r"])
    assert evaluate("T and not F", {})


def test_counting():
    assert multiset_perm([1, 4, 4, 2]) == 34650                          # MISSISSIPPI
    assert derangements(4) == 9
    assert count_functions(3, 2) == {"all": 8, "injective": 0, "surjective": 6}
    assert count_divisible(100, [2, 3, 5]) == 74


def test_recurrence_and_graphs():
    assert iterate_recurrence([1, 1], [0, 1], 10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
    konigsberg = [("A", "B"), ("A", "B"), ("A", "C"), ("A", "C"), ("A", "D"), ("B", "D"), ("C", "D")]
    assert euler_status("ABCD", konigsberg) == "none"
    assert euler_status("ABC", [("A", "B"), ("B", "C"), ("C", "A")]) == "circuit"
    assert euler_status("ABC", [("A", "B"), ("B", "C")]) == "path"
    total, tree = kruskal("ABCD", [("A", "B", 1), ("B", "C", 4), ("A", "C", 3), ("C", "D", 2), ("B", "D", 5)])
    assert total == 6 and len(tree) == 3
