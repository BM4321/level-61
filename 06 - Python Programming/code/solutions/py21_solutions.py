"""PY-21 reference solutions (data structures and graph algorithms)."""
from __future__ import annotations

import heapq
from collections import deque


def balanced(text: str) -> bool:
    """True if (), [] and {} are properly nested and matched."""
    pairs = {")": "(", "]": "[", "}": "{"}
    stack: list[str] = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def eval_postfix(tokens: list[str]) -> float:
    """Evaluate a postfix expression with + - * /; ValueError if malformed."""
    stack: list[float] = []
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    for t in tokens:
        if t in ops:
            if len(stack) < 2:
                raise ValueError("not enough operands")
            b, a = stack.pop(), stack.pop()
            stack.append(ops[t](a, b))
        else:
            stack.append(float(t))
    if len(stack) != 1:
        raise ValueError("malformed expression")
    return stack[0]


class Queue:
    """FIFO queue built from two stacks (amortised O(1))."""

    def __init__(self):
        self._inbox: list = []
        self._outbox: list = []

    def enqueue(self, x) -> None:
        self._inbox.append(x)

    def dequeue(self):
        if not self._outbox:
            while self._inbox:
                self._outbox.append(self._inbox.pop())
        if not self._outbox:
            raise IndexError("dequeue from empty queue")
        return self._outbox.pop()

    def __len__(self) -> int:
        return len(self._inbox) + len(self._outbox)


class Node:
    """Singly linked list node. [given]"""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next


class LinkedList:
    """Singly linked list with head pointer and size."""

    def __init__(self):
        self.head: Node | None = None
        self._size = 0

    def prepend(self, value) -> None:
        self.head = Node(value, self.head)
        self._size += 1

    def append(self, value) -> None:
        new = Node(value)
        if self.head is None:
            self.head = new
        else:
            node = self.head
            while node.next:
                node = node.next
            node.next = new
        self._size += 1

    def find(self, value) -> bool:
        node = self.head
        while node:
            if node.value == value:
                return True
            node = node.next
        return False

    def remove(self, value) -> None:
        """Remove first occurrence; ValueError if absent."""
        prev, node = None, self.head
        while node:
            if node.value == value:
                if prev is None:
                    self.head = node.next
                else:
                    prev.next = node.next
                self._size -= 1
                return
            prev, node = node, node.next
        raise ValueError(f"{value!r} not in list")

    def reverse(self) -> None:
        prev, node = None, self.head
        while node:
            nxt = node.next
            node.next = prev
            prev, node = node, nxt
        self.head = prev

    def __iter__(self):
        node = self.head
        while node:
            yield node.value
            node = node.next

    def __len__(self) -> int:
        return self._size


class BSTNode:
    """Binary search tree node. [given]"""

    def __init__(self, key):
        self.key, self.left, self.right = key, None, None


class BST:
    """Unbalanced binary search tree (duplicates ignored)."""

    def __init__(self):
        self.root: BSTNode | None = None
        self._size = 0

    def insert(self, key) -> None:
        def _ins(node):
            if node is None:
                self._size += 1
                return BSTNode(key)
            if key < node.key:
                node.left = _ins(node.left)
            elif key > node.key:
                node.right = _ins(node.right)
            return node

        self.root = _ins(self.root)

    def __contains__(self, key) -> bool:
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def inorder(self) -> list:
        out: list = []

        def _walk(node):
            if node:
                _walk(node.left)
                out.append(node.key)
                _walk(node.right)

        _walk(self.root)
        return out

    def height(self) -> int:
        def _h(node):
            return -1 if node is None else 1 + max(_h(node.left), _h(node.right))

        return _h(self.root)

    def min(self):
        if self.root is None:
            raise ValueError("empty tree")
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def __len__(self) -> int:
        return self._size


class HashMap:
    """Separate-chaining hash map that doubles when load factor > 0.75."""

    def __init__(self, capacity: int = 8):
        self._buckets: list[list[tuple]] = [[] for _ in range(capacity)]
        self._size = 0

    def _bucket(self, key) -> list[tuple]:
        return self._buckets[hash(key) % len(self._buckets)]

    def put(self, key, value) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))
        self._size += 1
        if self._size / len(self._buckets) > 0.75:
            self._resize(2 * len(self._buckets))

    def get(self, key):
        for k, v in self._bucket(key):
            if k == key:
                return v
        raise KeyError(key)

    def delete(self, key) -> None:
        bucket = self._bucket(key)
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return
        raise KeyError(key)

    def _resize(self, capacity: int) -> None:
        old = self._buckets
        self._buckets = [[] for _ in range(capacity)]
        for bucket in old:
            for k, v in bucket:
                self._bucket(k).append((k, v))

    def capacity(self) -> int:
        return len(self._buckets)

    def __len__(self) -> int:
        return self._size


def bfs_shortest_path(graph: dict, start, goal) -> list | None:
    """Fewest-edges path start..goal in an adjacency-list graph, or None."""
    parents = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node == goal:
            path = []
            while node is not None:
                path.append(node)
                node = parents[node]
            return path[::-1]
        for nb in graph.get(node, []):
            if nb not in parents:
                parents[nb] = node
                queue.append(nb)
    return None


def bfs_distances(graph: dict, start) -> dict:
    """Hop distance from start to every reachable node."""
    dist = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for nb in graph.get(node, []):
            if nb not in dist:
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def has_cycle(graph: dict) -> bool:
    """Directed-graph cycle detection with three-colour DFS."""
    white, grey, black = 0, 1, 2
    colour = {u: white for u in graph}

    def visit(u) -> bool:
        colour[u] = grey
        for v in graph.get(u, []):
            if colour.get(v, white) == grey:
                return True
            if colour.get(v, white) == white and visit(v):
                return True
        colour[u] = black
        return False

    return any(colour[u] == white and visit(u) for u in list(graph))


def dijkstra(graph: dict, source) -> dict:
    """Shortest distances from source; graph = {u: [(v, weight), ...]}, weights >= 0."""
    dist = {source: 0}
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist.get(u, float("inf")):
            continue
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return dist
