"""PY-01: watch CPython's pipeline: source -> AST -> bytecode -> execution.

Run:  python examples/py01_pipeline.py
"""
import ast
import dis
import sys

source = "total = 2 + 3 * 4\nprint(total)"

print("Python version:", sys.version.split()[0])
print("\n--- 1. AST of the first statement ---")
tree = ast.parse(source)
print(ast.dump(tree.body[0], indent=2))

print("\n--- 2. Bytecode (instruction names vary by Python version) ---")
code = compile(source, "<demo>", "exec")
dis.dis(code)

print("\n--- 3. Execution ---")
exec(code)

print("\n--- 4. A syntax error is caught before anything runs ---")
try:
    compile('print("start")\nif True\n    pass', "<bad>", "exec")
except SyntaxError as exc:
    print(f"SyntaxError on line {exc.lineno}: {exc.msg}")
