"""Tests added in SD-14 (boundary values, decision table R2, concurrency check)."""
import threading
from datetime import datetime

import pytest

from labbook.app import create_app
from labbook.domain import Booking, BookingStatus, TimeSlot
from labbook.errors import InvalidTransition, RuleViolation, ValidationError
from labbook.rules import WeeklyQuota
from tests.test_labbook import STUDENT, WS, slot


def test_timeslot_boundaries():
    with pytest.raises(ValidationError):
        slot(2, 9, 9)                                            # zero duration
    assert TimeSlot(datetime(2026, 3, 2, 7), datetime(2026, 3, 2, 15)).hours == 8.0   # exactly 8 h


def test_quota_week_edges_and_cancelled():
    rule = WeeklyQuota(max_hours=10)
    existing = [Booking(1, "s", "W1", slot(2, 9, 13), BookingStatus.CONFIRMED),
                Booking(2, "s", "W1", slot(3, 9, 13), BookingStatus.CONFIRMED)]          # 8 h
    sunday_late = Booking(None, "s", "W1", TimeSlot(datetime(2026, 3, 8, 21), datetime(2026, 3, 8, 22)))
    rule.check(sunday_late, STUDENT, WS, existing)                                     # 9 h, same week
    existing.append(Booking(3, "s", "W1", slot(4, 9, 11), BookingStatus.CANCELLED))    # does not count
    rule.check(Booking(None, "s", "W1", slot(5, 9, 11)), STUDENT, WS, existing)        # 10 h total


def test_cannot_cancel_after_check_in():
    svc, _, _ = create_app()
    b = svc.book("u-amina", "LAB1-01", slot(2, 9, 10))
    svc.check_in("u-amina", b.booking_id)
    with pytest.raises(InvalidTransition):
        svc.cancel("u-amina", b.booking_id)


@pytest.mark.xfail(strict=True, reason="KNOWN DEFECT: overlap check is not atomic; fix is SD-17 / case-study exercise 5")
def test_no_double_booking_under_concurrency(tmp_path):
    path = str(tmp_path / "lb.db")
    results, barrier = [], threading.Barrier(2)

    def worker(user):
        svc = create_app("sqlite", path)[0]           # separate connection per thread
        barrier.wait()
        try:
            results.append(str(svc.book(user, "LAB1-01", slot(2, 9, 10)).status))
        except RuleViolation:
            results.append("refused")

    threads = [threading.Thread(target=worker, args=(u,)) for u in ("u-amina", "u-baraka")]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert sorted(results) == ["BookingStatus.CONFIRMED", "refused"]
