"""PY-19: the messy original (DO NOT imitate). Refactored version: solutions/py19_solutions.py"""


def r(d, f):
    s = 0
    o = ""
    for k in d:
        s = s + d[k]
        if d[k] >= 70:
            g = "A"
        elif d[k] >= 60:
            g = "B"
        elif d[k] >= 50:
            g = "C"
        elif d[k] >= 40:
            g = "D"
        else:
            g = "F"
        if f:
            o = o + k.upper() + ": " + str(d[k]) + " " + g + "\n"
        else:
            o = o + k + ": " + str(d[k]) + " " + g + "\n"
    o = o + "AVG: " + str(round(s / len(d), 1))
    return o


if __name__ == "__main__":
    print(r({"ali": 72, "bea": 55}, False))
    print(r({"ali": 72, "bea": 55}, True))
