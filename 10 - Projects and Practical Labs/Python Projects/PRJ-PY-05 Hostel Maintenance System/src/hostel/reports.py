"""Management reports computed from requests. Pure functions: easy to test."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta

from .models import OPEN_STATUSES, Priority, Request, Status

URGENT_TARGET = timedelta(hours=24)


def summary(requests: list[Request], now: datetime) -> dict[str, object]:
    by_status = Counter(r.status.value for r in requests)
    open_requests = [r for r in requests if r.status in OPEN_STATUSES]
    resolved = [r for r in requests if r.resolved_at is not None]
    hours = [(r.resolved_at - r.created_at).total_seconds() / 3600 for r in resolved if r.resolved_at]
    return {
        "total": len(requests),
        "by_status": {s.value: by_status.get(s.value, 0) for s in Status},
        "open_by_priority": {p.value: sum(r.priority is p for r in open_requests) for p in Priority},
        "mean_hours_to_resolve": round(sum(hours) / len(hours), 1) if hours else None,
        "overdue_urgent": [r.id for r in open_requests
                           if r.priority is Priority.URGENT and now - r.created_at > URGENT_TARGET],
    }
