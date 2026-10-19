import random

import pytest

from _target import load

m = load("py21")
G = {"A": ["B", "C"], "B": ["D"], "C": ["D", "E"], "D": ["F"], "E": ["F"], "F": []}


@pytest.mark.parametrize("text, ok", [("([])", True), ("(]", False), ("((", False), ("", True),
                                      ("f(a[1]) {x}", True), ("())", False)])
def test_balanced(text, ok):
    assert m.balanced(text) is ok


def test_eval_postfix():
    assert m.eval_postfix("3 4 + 2 *".split()) == 14.0
    assert m.eval_postfix("10 4 -".split()) == 6.0
    assert m.eval_postfix("8 2 /".split()) == 4.0
    for bad in ("+", "1 2", "1 +"):
        with pytest.raises(ValueError):
            m.eval_postfix(bad.split())


def test_queue_fifo():
    q = m.Queue()
    for i in range(5):
        q.enqueue(i)
    assert q.dequeue() == 0
    q.enqueue(5)
    assert [q.dequeue() for _ in range(5)] == [1, 2, 3, 4, 5]
    assert len(q) == 0
    with pytest.raises(IndexError):
        q.dequeue()


def test_linked_list():
    ll = m.LinkedList()
    for x in (2, 3):
        ll.append(x)
    ll.prepend(1)
    assert list(ll) == [1, 2, 3] and len(ll) == 3 and ll.find(2) and not ll.find(9)
    ll.reverse()
    assert list(ll) == [3, 2, 1]
    ll.remove(3)
    ll.remove(1)
    assert list(ll) == [2] and len(ll) == 1
    with pytest.raises(ValueError):
        ll.remove(42)
    empty = m.LinkedList()
    empty.reverse()
    assert list(empty) == []


def test_bst():
    t = m.BST()
    for k in (50, 30, 70, 20, 40, 60, 80, 30):
        t.insert(k)
    assert t.inorder() == [20, 30, 40, 50, 60, 70, 80]
    assert len(t) == 7 and t.height() == 2 and t.min() == 20
    assert 60 in t and 65 not in t
    chain = m.BST()
    for k in range(1, 6):
        chain.insert(k)
    assert chain.height() == 4
    assert m.BST().height() == -1


def test_hashmap_against_dict():
    hm, ref = m.HashMap(capacity=4), {}
    rng = random.Random(21)
    for _ in range(2000):
        k = rng.randint(0, 300)
        op = rng.random()
        if op < 0.6:
            hm.put(k, k * 2)
            ref[k] = k * 2
        elif k in ref:
            hm.delete(k)
            del ref[k]
    assert len(hm) == len(ref)
    for k, v in ref.items():
        assert hm.get(k) == v
    assert len(hm) / hm.capacity() <= 0.75
    with pytest.raises(KeyError):
        hm.get(-1)


def test_bfs():
    assert m.bfs_shortest_path(G, "A", "F") == ["A", "B", "D", "F"]
    assert m.bfs_shortest_path(G, "F", "A") is None
    assert m.bfs_shortest_path(G, "A", "A") == ["A"]
    d = m.bfs_distances(G, "A")
    assert d == {"A": 0, "B": 1, "C": 1, "D": 2, "E": 2, "F": 3}
    assert sorted(n for n, k in d.items() if k == 2) == ["D", "E"]


def test_has_cycle():
    assert not m.has_cycle(G)
    assert m.has_cycle({"A": ["B"], "B": ["C"], "C": ["A"]})
    assert m.has_cycle({"A": ["A"]})


def test_dijkstra():
    g = {"S": [("A", 7), ("B", 2)], "B": [("A", 3), ("C", 8)], "A": [("C", 1)], "C": []}
    assert m.dijkstra(g, "S") == {"S": 0, "B": 2, "A": 5, "C": 6}
