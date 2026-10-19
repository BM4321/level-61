import math
import subprocess
import sys
from pathlib import Path

import pytest

from _target import load

m = load("py13")


def test_parse_requirement():
    assert m.parse_requirement("requests==2.32.3") == ("requests", "==2.32.3")
    assert m.parse_requirement("pytest >= 8  # tests") == ("pytest", ">=8")
    assert m.parse_requirement("rich") == ("rich", "")
    assert m.parse_requirement("   ") is None
    assert m.parse_requirement("# comment") is None


def test_read_requirements():
    text = "Requests==2.32.3\n\n# dev\npytest>=8\n"
    assert m.read_requirements(text) == {"requests": "==2.32.3", "pytest": ">=8"}
    with pytest.raises(ValueError):
        m.read_requirements("a==1\nA==2")


def test_import_by_name():
    assert m.import_by_name("math.sqrt") is math.sqrt
    assert m.import_by_name("os.path.join")("a", "b") in ("a/b", "a\\b")
    with pytest.raises(ValueError):
        m.import_by_name("sqrt")


@pytest.mark.parametrize("version, spec, ok", [("1.10", ">=1.9", True), ("1.9", ">=1.10", False),
                                               ("2.0.0", "<3", True), ("3.0", "!=3.0", False),
                                               ("1.4.2", "==1.4.2", True), ("0.9", ">1.0", False)])
def test_satisfies(version, spec, ok):
    assert m.satisfies(version, spec) is ok


def test_demo_package_runs():
    pkg = Path(__file__).resolve().parents[1] / "examples" / "py13_demo_pkg"
    out = subprocess.run([sys.executable, "main.py"], cwd=pkg, capture_output=True, text=True, check=True).stdout
    assert "'grades': {'Ali': 'A', 'Bea': 'B', 'Chen': 'F'}" in out
    out2 = subprocess.run([sys.executable, "-m", "gradebook.grading"], cwd=pkg, capture_output=True,
                          text=True, check=True).stdout
    assert out2.strip() == "['F', 'C', 'A']"
