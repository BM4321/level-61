"""Creational patterns: a Builder for test data, and a registry-based Factory for rules from config."""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Callable

from labbook.domain import Booking, BookingStatus, TimeSlot
from labbook.rules import (BookingRule, GpuForLecturersAndApprovedOnly, NoOverlap, OpeningHours, RuleSet,
                           WeeklyQuota, WorkstationInService)


class BookingBuilder:
    """BUILDER: readable construction of test bookings with sensible defaults."""

    def __init__(self) -> None:
        self._user, self._ws = "u-amina", "LAB1-01"
        self._start, self._hours = datetime(2026, 3, 2, 9, 0), 1.0
        self._status = BookingStatus.REQUESTED

    def by(self, user_id: str) -> BookingBuilder:
        self._user = user_id
        return self

    def on(self, ws_id: str) -> BookingBuilder:
        self._ws = ws_id
        return self

    def at(self, start: datetime, hours: float = 1.0) -> BookingBuilder:
        self._start, self._hours = start, hours
        return self

    def confirmed(self) -> BookingBuilder:
        self._status = BookingStatus.CONFIRMED
        return self

    def build(self) -> Booking:
        slot = TimeSlot(self._start, self._start + timedelta(hours=self._hours))
        return Booking(None, self._user, self._ws, slot, self._status)


RULE_TYPES: dict[str, Callable[[dict], BookingRule]] = {
    "in-service": lambda cfg: WorkstationInService(),
    "opening-hours": lambda cfg: OpeningHours(),
    "no-overlap": lambda cfg: NoOverlap(),
    "weekly-quota": lambda cfg: WeeklyQuota(max_hours=float(cfg.get("max_hours", 10))),
    "gpu-access": lambda cfg: GpuForLecturersAndApprovedOnly(set(cfg.get("approved", []))),
}


def rules_from_config(config: list[dict]) -> RuleSet:
    """FACTORY: build a RuleSet from data (e.g. a per-university JSON file). Unknown names fail loudly."""
    rules: list[BookingRule] = []
    for item in config:
        try:
            rules.append(RULE_TYPES[item["type"]](item))
        except KeyError:
            raise ValueError(f"unknown rule type: {item.get('type')!r}") from None
    return RuleSet(rules)
