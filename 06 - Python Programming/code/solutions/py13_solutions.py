"""PY-13 reference solutions (requirements parsing, dynamic import, versions)."""
import importlib
import operator

_OPS = {"==": operator.eq, "!=": operator.ne, ">=": operator.ge,
        "<=": operator.le, ">": operator.gt, "<": operator.lt}


def parse_requirement(line: str) -> tuple[str, str] | None:
    """'requests==2.32.3' -> ('requests', '==2.32.3'); None for blank/comment lines."""
    line = line.split("#", 1)[0].strip()
    if not line:
        return None
    for i, ch in enumerate(line):
        if ch in "=<>!~":
            return line[:i].strip(), line[i:].replace(" ", "")
    return line, ""


def read_requirements(text: str) -> dict[str, str]:
    """Lower-cased name -> specifier; ValueError on duplicate names."""
    result: dict[str, str] = {}
    for raw in text.splitlines():
        parsed = parse_requirement(raw)
        if parsed is None:
            continue
        name, spec = parsed
        key = name.lower()
        if key in result:
            raise ValueError(f"duplicate requirement: {name}")
        result[key] = spec
    return result


def import_by_name(dotted: str):
    """'math.sqrt' -> the object; ValueError if no module part."""
    module_name, _, attr = dotted.rpartition(".")
    if not module_name:
        raise ValueError("expected 'module.attribute'")
    module = importlib.import_module(module_name)
    return getattr(module, attr)


def version_tuple(v: str) -> tuple[int, ...]:
    """'1.10.2' -> (1, 10, 2)."""
    return tuple(int(part) for part in v.split("."))


def satisfies(version: str, spec: str) -> bool:
    """Single-operator check, e.g. satisfies('1.10', '>=1.9') -> True."""
    for op in ("==", "!=", ">=", "<=", ">", "<"):
        if spec.startswith(op):
            return _OPS[op](version_tuple(version), version_tuple(spec[len(op):]))
    raise ValueError(f"unsupported spec {spec!r}")
