"""PY21 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py21.py
"""

from __future__ import annotations
import heapq
from collections import deque

def balanced(text: str) -> bool:
    """True if (), [] and {} are properly nested and matched."""
    raise NotImplementedError

def eval_postfix(tokens: list[str]) -> float:
    """Evaluate a postfix expression with + - * /; ValueError if malformed."""
    raise NotImplementedError

class Queue:
    """FIFO queue built from two stacks (amortised O(1))."""

    def __init__(self):
        raise NotImplementedError

    def enqueue(self, x) -> None:
        raise NotImplementedError

    def dequeue(self):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class Node:
    """Singly linked list node. [given]"""

    def __init__(self, value, next=None):
        self.value = value
        self.next = next

class LinkedList:
    """Singly linked list with head pointer and size."""

    def __init__(self):
        raise NotImplementedError

    def prepend(self, value) -> None:
        raise NotImplementedError

    def append(self, value) -> None:
        raise NotImplementedError

    def find(self, value) -> bool:
        raise NotImplementedError

    def remove(self, value) -> None:
        """Remove first occurrence; ValueError if absent."""
        raise NotImplementedError

    def reverse(self) -> None:
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class BSTNode:
    """Binary search tree node. [given]"""

    def __init__(self, key):
        self.key, self.left, self.right = (key, None, None)

class BST:
    """Unbalanced binary search tree (duplicates ignored)."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, key) -> None:
        raise NotImplementedError

    def __contains__(self, key) -> bool:
        raise NotImplementedError

    def inorder(self) -> list:
        raise NotImplementedError

    def height(self) -> int:
        raise NotImplementedError

    def min(self):
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

class HashMap:
    """Separate-chaining hash map that doubles when load factor > 0.75."""

    def __init__(self, capacity: int=8):
        raise NotImplementedError

    def _bucket(self, key) -> list[tuple]:
        raise NotImplementedError

    def put(self, key, value) -> None:
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def delete(self, key) -> None:
        raise NotImplementedError

    def _resize(self, capacity: int) -> None:
        raise NotImplementedError

    def capacity(self) -> int:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

def bfs_shortest_path(graph: dict, start, goal) -> list | None:
    """Fewest-edges path start..goal in an adjacency-list graph, or None."""
    raise NotImplementedError

def bfs_distances(graph: dict, start) -> dict:
    """Hop distance from start to every reachable node."""
    raise NotImplementedError

def has_cycle(graph: dict) -> bool:
    """Directed-graph cycle detection with three-colour DFS."""
    raise NotImplementedError

def dijkstra(graph: dict, source) -> dict:
    """Shortest distances from source; graph = {u: [(v, weight), ...]}, weights >= 0."""
    raise NotImplementedError
