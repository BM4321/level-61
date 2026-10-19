import pytest

from _target import load

m = load("py11")


def test_word_counts():
    assert m.word_counts("The cat. The hat!") == {"the": 2, "cat": 1, "hat": 1}
    assert m.word_counts("... !!") == {}


def test_common():
    assert m.common([3, 1, 2, 3, 4], [4, 3, 9]) == [3, 4]
    assert m.common([], [1]) == []


def test_invert():
    assert m.invert({"Ali": "B", "Bea": "A", "Chen": "B"}) == {"B": ["Ali", "Chen"], "A": ["Bea"]}


def test_average_by_group():
    rows = [("Ali", "CS", 71), ("Bea", "IT", 88), ("Chen", "CS", 64), ("Dan", "IT", 52)]
    assert m.average_by_group(rows) == {"CS": 67.5, "IT": 70.0}


def test_comprehensions():
    assert m.squares_of_evens([1, 2, 3, 4]) == [4, 16]
    assert m.passing({"a": 49, "b": 50, "c": 80}) == {"b": 50, "c": 80}


def test_most_frequent():
    assert m.most_frequent(["b", "a", "a", "b", "c"]) == "b"
    assert m.most_frequent([1]) == 1
    with pytest.raises(ValueError):
        m.most_frequent([])


@pytest.mark.parametrize("nums, target, expected", [([2, 7, 11, 15], 9, (0, 1)), ([3, 3], 6, (0, 1)),
                                                    ([1, 2, 3], 7, None), ([5, 1, 4], 9, (0, 2))])
def test_two_sum(nums, target, expected):
    assert m.two_sum(nums, target) == expected


def test_only_one_course():
    reg = {"PY": {"S1", "S2", "S3"}, "DM": {"S2", "S3", "S4"}, "CS": {"S3", "S5"}}
    assert m.only_one_course(reg) == {"S1", "S4", "S5"}


def test_index_search():
    docs = {"d1": "Python programming basics.", "d2": "Discrete maths for programming", "d3": "Python security"}
    idx = m.build_index(docs)
    assert m.search(idx, "programming") == {"d1", "d2"}
    assert m.search(idx, "PYTHON programming") == {"d1"}
    assert m.search(idx, "missing") == set()
    assert m.search(idx, "") == set()
