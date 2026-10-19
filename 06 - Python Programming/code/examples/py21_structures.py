"""PY-21: structures in action. Run: python examples/py21_structures.py"""
import heapq
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py21_solutions import BST, balanced, bfs_shortest_path, dijkstra, eval_postfix  # noqa: E402

print(balanced("([])"), balanced("(]"), eval_postfix("3 4 + 2 *".split()))
t = BST()
for k in (50, 30, 70, 20, 40, 60, 80):
    t.insert(k)
print("in-order:", t.inorder(), "height:", t.height())
graph = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}
print("BFS path A->F:", bfs_shortest_path(graph, "A", "F"))
print("Dijkstra:", dijkstra({"S": [("A", 7), ("B", 2)], "B": [("A", 3)], "A": []}, "S"))
print("top 3:", heapq.nlargest(3, [55, 91, 72, 38, 88, 64]))
