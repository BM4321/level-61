"""PY-20 debugging practice. This file contains a PLANTED BUG.

Run:  python examples/py20_debug_me.py      (expected 60.0, actual output differs)
Then insert breakpoint() before the return and inspect `passing` with:  p passing
"""


def average_passing(marks, pass_mark=50):
    passing = [m for m in marks if m > pass_mark]
    return sum(passing) / len(passing)


if __name__ == "__main__":
    print(average_passing([50, 60, 70]))
