"""Operational views for wardens and technicians. Pure functions over Request lists (no I/O)."""
from __future__ import annotations

import heapq
from collections import Counter
from datetime import datetime, timedelta

from .models import OPEN_STATUSES, Priority, Request

PRIORITY_RANK = {Priority.URGENT: 0, Priority.NORMAL: 1, Priority.LOW: 2}


def repeat_rooms(requests: list[Request], now: datetime, days: int = 30, threshold: int = 3) -> list[tuple[str, int]]:
    """Rooms with >= threshold reports in the last `days` days, most reports first (ties by room code)."""
    since = now - timedelta(days=days)
    counts = Counter(r.room_code for r in requests if since <= r.created_at <= now)
    return sorted(((room, n) for room, n in counts.items() if n >= threshold), key=lambda x: (-x[1], x[0]))


def work_queue(requests: list[Request]) -> list[Request]:
    """Open requests in the order a technician should take them: most urgent first, then oldest."""
    heap = [(PRIORITY_RANK[r.priority], r.created_at, r.id, r) for r in requests if r.status in OPEN_STATUSES]
    heapq.heapify(heap)
    return [heapq.heappop(heap)[3] for _ in range(len(heap))]


def possible_duplicates(requests: list[Request]) -> dict[tuple[str, str], list[int]]:
    """Open requests sharing (room, category): candidates for a warden to merge or reject as duplicates."""
    groups: dict[tuple[str, str], list[int]] = {}
    for r in requests:
        if r.status in OPEN_STATUSES:
            groups.setdefault((r.room_code, r.category), []).append(r.id)
    return {k: sorted(v) for k, v in sorted(groups.items()) if len(v) > 1}
