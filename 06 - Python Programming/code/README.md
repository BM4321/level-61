---
title: "Python Code Bank README"
type: "system"
module_code: "CST06102"
tags:
  - semester-6
  - python
---

# Python Code Bank

| Folder | Contents |
|---|---|
| `examples/` | Runnable examples from the lessons: `python examples/py06_functions.py` |
| `exercises/` | **Your** workspace. Function stubs with docstrings that raise `NotImplementedError` until you implement them. |
| `solutions/` | Reference solutions. Open them only after an honest attempt. |
| `tests/` | pytest tests. By default they check `solutions/`; set `PY_TARGET=exercises` to check your work. |

```bash
python -m pip install pytest
python -m pytest                          # all reference solutions should pass
PY_TARGET=exercises python -m pytest      # your progress (failures = not done yet)
PY_TARGET=exercises python -m pytest tests/test_py06.py   # one lesson only
```

Requires Python 3.10+. Tested on CPython 3.13. Uses only the standard library, plus pytest for testing.
