"""Helpers to pull code out of the mock notes, so the tests check the notes themselves."""
import contextlib
import io
import re
from pathlib import Path

FOLDER = Path(__file__).resolve().parents[2]


def note(name: str) -> str:
    return (FOLDER / f"{name}.md").read_text(encoding="utf-8")


def question_snippets(text: str) -> dict[str, str]:
    """Map 'A1' -> code for every ```python fence whose first line is '# question <id>'."""
    found = {}
    for m in re.finditer(r"```python\n# question (\w+)\n(.*?)```", text, re.S):
        found[m.group(1)] = m.group(2)
    return found


def run(code: str) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        exec(compile(code, "<snippet>", "exec"), {})
    return buf.getvalue()
