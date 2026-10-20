from datetime import datetime

import pytest

from labbook.app import create_app, demo_directory
from labbook.domain import Booking, BookingStatus, Role, TimeSlot, User, Workstation
from labbook.errors import InvalidTransition, NotFound, PermissionDenied, RuleViolation, ValidationError
from labbook.events import Event, EventBus, Outbox
from labbook.repository import InMemoryBookingRepository, SqliteBookingRepository
from labbook.rules import GpuForLecturersAndApprovedOnly, NoOverlap, OpeningHours, RuleSet, WeeklyQuota, default_rules
from labbook.service import BookingService


def slot(day, h1, h2, m1=0, m2=0):
    return TimeSlot(datetime(2026, 3, day, h1, m1), datetime(2026, 3, day, h2, m2))


# ------------------------------------------------------------------ domain
def test_timeslot_validation_and_overlap():
    with pytest.raises(ValidationError):
        slot(2, 10, 9)
    with pytest.raises(ValidationError):
        TimeSlot(datetime(2026, 3, 2, 7), datetime(2026, 3, 2, 16))       # 9 hours
    assert slot(2, 9, 11).overlaps(slot(2, 10, 12))
    assert not slot(2, 9, 11).overlaps(slot(2, 11, 12))                    # touching is fine
    assert slot(2, 9, 11, 0, 30).hours == 2.5
    assert slot(2, 9, 11) == slot(2, 9, 11)                                # value object equality


def test_state_machine():
    b = Booking(1, "u", "w", slot(2, 9, 10))
    b.transition(BookingStatus.CONFIRMED)
    b.transition(BookingStatus.CHECKED_IN)
    b.transition(BookingStatus.COMPLETED)
    assert b.history[-1] == (BookingStatus.CHECKED_IN, BookingStatus.COMPLETED) and not b.active
    with pytest.raises(InvalidTransition):
        b.transition(BookingStatus.CANCELLED)
    c = Booking(2, "u", "w", slot(2, 9, 10))
    with pytest.raises(InvalidTransition):
        c.transition(BookingStatus.CHECKED_IN)                             # must be confirmed first


# ------------------------------------------------------------------ rules
STUDENT = User("s", "S", Role.STUDENT)
LECT = User("l", "L", Role.LECTURER)
WS = Workstation("W1", "LAB1")
GPU = Workstation("G1", "LAB2", has_gpu=True)


def test_no_overlap_ignores_cancelled():
    old = Booking(1, "x", "W1", slot(2, 9, 11), BookingStatus.CONFIRMED)
    new = Booking(None, "s", "W1", slot(2, 10, 12))
    with pytest.raises(RuleViolation) as e:
        NoOverlap().check(new, STUDENT, WS, [old])
    assert e.value.rule == "no-overlap"
    old.status = BookingStatus.CANCELLED
    NoOverlap().check(new, STUDENT, WS, [old])


def test_opening_hours():
    OpeningHours().check(Booking(None, "s", "W1", slot(2, 7, 9)), STUDENT, WS, [])
    with pytest.raises(RuleViolation):
        OpeningHours().check(Booking(None, "s", "W1", slot(2, 21, 23)), STUDENT, WS, [])


def test_weekly_quota_students_only():
    # 2 March 2026 is a Monday
    existing = [Booking(i, "s", "W1", slot(d, 9, 13), BookingStatus.CONFIRMED) for i, d in enumerate([2, 3], 1)]  # 8 h
    rule = WeeklyQuota(max_hours=10)
    rule.check(Booking(None, "s", "W1", slot(4, 9, 11)), STUDENT, WS, existing)     # 10 h total: allowed
    with pytest.raises(RuleViolation):
        rule.check(Booking(None, "s", "W1", slot(4, 9, 12)), STUDENT, WS, existing)  # 11 h
    rule.check(Booking(None, "s", "W1", slot(9, 9, 13)), STUDENT, WS, existing)     # next week: fresh quota
    rule.check(Booking(None, "l", "W1", slot(4, 9, 15)), LECT, WS, [Booking(9, "l", "W1", slot(3, 9, 15), BookingStatus.CONFIRMED)])


def test_new_rule_plugs_in_without_changing_service():
    rules = RuleSet(default_rules().rules + [GpuForLecturersAndApprovedOnly({"u-baraka"})])
    svc, _o, _a = create_app()
    svc.rules = rules
    with pytest.raises(RuleViolation):
        svc.book("u-amina", "LAB2-GPU1", slot(2, 9, 10))
    assert svc.book("u-baraka", "LAB2-GPU1", slot(2, 9, 10)).status is BookingStatus.CONFIRMED
    assert svc.book("u-drm", "LAB2-GPU1", slot(2, 10, 11)).status is BookingStatus.CONFIRMED


# ------------------------------------------------------------------ repository contract (both implementations)
@pytest.fixture(params=["memory", "sqlite"])
def repo(request):
    return InMemoryBookingRepository() if request.param == "memory" else SqliteBookingRepository()


def test_repository_contract(repo):
    b = repo.add(Booking(None, "u1", "W1", slot(2, 9, 10)))
    assert b.booking_id == 1
    repo.add(Booking(None, "u2", "W1", slot(2, 7, 8)))
    got = repo.get(1)
    assert (got.user_id, got.slot, got.status) == ("u1", slot(2, 9, 10), BookingStatus.REQUESTED)
    got.transition(BookingStatus.CONFIRMED)
    repo.save(got)
    assert repo.get(1).status is BookingStatus.CONFIRMED
    assert {x.user_id for x in repo.for_workstation("W1")} == {"u1", "u2"}
    assert [x.booking_id for x in repo.for_user("u2")] == [2]
    with pytest.raises(NotFound):
        repo.get(99)


# ------------------------------------------------------------------ service (use cases)
@pytest.fixture(params=["memory", "sqlite"])
def app(request):
    return create_app(request.param)


def test_book_confirm_notify(app):
    svc, outbox, audit = app
    b = svc.book("u-amina", "LAB1-01", slot(2, 9, 11))
    assert b.status is BookingStatus.CONFIRMED
    assert outbox.messages == ["to u-amina: booking.confirmed #1 LAB1-01 2026-03-02 09:00-11:00"]
    assert audit.lines == ["booking.confirmed booking=1 user=u-amina"]
    with pytest.raises(RuleViolation):
        svc.book("u-baraka", "LAB1-01", slot(2, 10, 12))


def test_cancel_permissions(app):
    svc, outbox, _ = app
    b = svc.book("u-amina", "LAB1-01", slot(2, 9, 11))
    with pytest.raises(PermissionDenied):
        svc.cancel("u-baraka", b.booking_id)
    assert svc.cancel("u-juma", b.booking_id).status is BookingStatus.CANCELLED   # technician may cancel
    assert outbox.messages[-1] == "to u-amina: booking.cancelled #1 by u-juma"
    svc.book("u-baraka", "LAB1-01", slot(2, 10, 12))                               # slot free again


def test_check_in_and_errors(app):
    svc, _, _ = app
    b = svc.book("u-amina", "LAB1-02", slot(3, 14, 16))
    with pytest.raises(PermissionDenied):
        svc.check_in("u-baraka", b.booking_id)
    assert svc.check_in("u-amina", b.booking_id).status is BookingStatus.CHECKED_IN
    with pytest.raises(NotFound):
        svc.book("u-nobody", "LAB1-02", slot(3, 9, 10))
    with pytest.raises(NotFound):
        svc.book("u-amina", "NOPE", slot(3, 9, 10))


def test_failing_subscriber_does_not_break_booking():
    bus = EventBus()
    def broken(event):
        raise RuntimeError("SMTP down")
    out = Outbox()
    bus.subscribe("booking.confirmed", broken)
    bus.subscribe("booking.confirmed", out)
    svc = BookingService(InMemoryBookingRepository(), demo_directory(), bus)
    svc.book("u-amina", "LAB1-01", slot(2, 9, 10))
    assert len(out.messages) == 1 and bus.errors[0][0] == "broken"


def test_service_with_fake_rules_is_easy_to_test():
    class AllowAll:
        name = "allow"
        def check(self, *a):
            pass
    svc = BookingService(InMemoryBookingRepository(), demo_directory(), EventBus(), rules=AllowAll(), auto_confirm=False)
    assert svc.book("u-amina", "LAB1-03", slot(2, 23 - 1, 23)).status is BookingStatus.REQUESTED


def test_cli(capsys):
    from labbook.cli import main
    assert main(["--user", "u-amina", "--ws", "LAB1-01", "--start", "2026-03-02T09:00", "--end", "2026-03-02T11:00"]) == 0
    assert "booking #1 confirmed" in capsys.readouterr().out
    assert main(["--user", "u-amina", "--ws", "LAB1-03", "--start", "2026-03-02T09:00", "--end", "2026-03-02T11:00"]) == 1
    assert "out of service" in capsys.readouterr().out


# ------------------------------------------------------------------ gaps found by line_coverage.py (SD-14)
def test_my_bookings_sorted(app):
    svc, _, _ = app
    svc.book("u-amina", "LAB1-02", slot(3, 14, 15))
    svc.book("u-amina", "LAB1-01", slot(2, 9, 10))
    assert [b.slot.start.day for b in svc.my_bookings("u-amina")] == [2, 3]
    assert svc.my_bookings("u-baraka") == []


def test_save_unknown_booking_raises(repo):
    with pytest.raises(NotFound):
        repo.save(Booking(None, "u", "W1", slot(2, 9, 10)))      # never added
    with pytest.raises(NotFound):
        repo.save(Booking(77, "u", "W1", slot(2, 9, 10)))        # unknown id


def test_quota_does_not_double_count_same_workstation(app):
    """Regression (found in SD-17): bookings on the same workstation were counted twice for the quota."""
    svc, _, _ = app
    svc.book("u-amina", "LAB1-01", slot(2, 9, 13))     # 4 h
    svc.book("u-amina", "LAB1-01", slot(3, 9, 13))     # 8 h, previously refused as "12 h"
    svc.book("u-amina", "LAB1-01", slot(4, 9, 11))     # exactly 10 h: allowed
    with pytest.raises(RuleViolation):
        svc.book("u-amina", "LAB1-01", slot(5, 9, 10))  # 11 h
