"""Generate exercises/pyNN_exercises.py from solutions/pyNN_solutions.py.

Keeps imports, constants, signatures and docstrings; replaces every function
body with `raise NotImplementedError`. Existing exercise files are NOT
overwritten unless --force is given (so your own work is never destroyed).

    python make_exercise_stubs.py py04            # create if missing
    python make_exercise_stubs.py py04 --force    # regenerate (destroys edits!)
"""
import ast
import sys
from pathlib import Path

HERE = Path(__file__).parent


class Stubber(ast.NodeTransformer):
    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        doc = ast.get_docstring(node)
        body: list[ast.stmt] = []
        if doc:
            body.append(ast.Expr(ast.Constant(doc)))
        body.append(ast.Raise(exc=ast.Name("NotImplementedError", ast.Load()), cause=None))
        node.body = body
        return node

    visit_AsyncFunctionDef = visit_FunctionDef


def main() -> None:
    lesson = sys.argv[1]
    force = "--force" in sys.argv
    src = HERE / "solutions" / f"{lesson}_solutions.py"
    dst = HERE / "exercises" / f"{lesson}_exercises.py"
    if dst.exists() and not force:
        print(f"{dst.name} exists; not overwriting (use --force)")
        return
    tree = Stubber().visit(ast.parse(src.read_text(encoding="utf-8")))
    ast.fix_missing_locations(tree)
    header = (f'"""{lesson.upper()} exercises: implement each function, then run\n'
              f'    PY_TARGET=exercises python -m pytest tests/test_{lesson}.py\n"""\n')
    body = ast.unparse(tree)
    # drop the solutions' own module docstring
    if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
        body = ast.unparse(ast.Module(body=tree.body[1:], type_ignores=[]))
    dst.write_text(header + "\n" + body + "\n", encoding="utf-8")
    print(f"wrote {dst}")


if __name__ == "__main__":
    main()
