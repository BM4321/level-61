"""Choose whether tests run against the reference solutions or your own exercises.

    python -m pytest                        -> tests solutions/pyNN_solutions.py
    PY_TARGET=exercises python -m pytest    -> tests exercises/pyNN_exercises.py
"""
import importlib
import os

TARGET = os.environ.get("PY_TARGET", "solutions")
if TARGET not in ("solutions", "exercises"):
    raise ValueError("PY_TARGET must be 'solutions' or 'exercises'")


def load(lesson: str):
    """Import e.g. load('py06') -> solutions.py06_solutions."""
    return importlib.import_module(f"{TARGET}.{lesson}_{TARGET}")
