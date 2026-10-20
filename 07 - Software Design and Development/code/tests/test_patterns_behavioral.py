from datetime import datetime

import pytest

from labbook.app import demo_directory
from labbook.domain import BookingStatus, TimeSlot
from labbook.errors import InvalidTransition, LabBookError, RuleViolation
from labbook.events import EventBus
from labbook.repository import InMemoryBookingRepository
from labbook.service import BookingService
from patterns.behavioral import BookCommand, CommandHistory, RepairTicket, WaitingList

SLOT = TimeSlot(datetime(2026, 3, 2, 9), datetime(2026, 3, 2, 11))


def make():
    repo, bus = InMemoryBookingRepository(), EventBus()
    return BookingService(repo, demo_directory(), bus), repo, bus


def test_waiting_list_observer():
    svc, repo, bus = make()
    wl = WaitingList(repo)
    bus.subscribe("booking.cancelled", wl)
    b = svc.book("u-amina", "LAB1-01", SLOT)
    with pytest.raises(RuleViolation):
        svc.book("u-baraka", "LAB1-01", SLOT)
    assert wl.join("u-baraka", "LAB1-01", SLOT) == 1
    assert wl.join("u-drm", "LAB1-01", SLOT) == 2
    assert wl.join("u-baraka", "LAB1-01", SLOT) == 1          # joining twice keeps position
    svc.cancel("u-amina", b.booking_id)
    assert wl.offers == [("u-baraka", "LAB1-01", SLOT)]
    assert svc.book("u-baraka", "LAB1-01", SLOT).status is BookingStatus.CONFIRMED


def test_command_undo():
    svc, repo, _ = make()
    h = CommandHistory()
    h.run(BookCommand(svc, "u-amina", "LAB1-01", SLOT))
    assert repo.get(1).status is BookingStatus.CONFIRMED
    h.undo_last()
    assert repo.get(1).status is BookingStatus.CANCELLED
    with pytest.raises(LabBookError):
        h.undo_last()
    with pytest.raises(RuleViolation):        # failing command is not recorded
        h.run(BookCommand(svc, "u-amina", "LAB1-03", SLOT))
    assert h.done == []


def test_state_pattern_ticket():
    t = RepairTicket("LAB1-03")
    with pytest.raises(InvalidTransition):
        t.start()
    t.assign("u-juma")
    t.assign("u-neema")                        # reassign before start
    t.start()
    with pytest.raises(InvalidTransition):
        t.assign("u-juma")
    with pytest.raises(InvalidTransition):
        t.resolve("   ")
    t.resolve("Replaced faulty PSU")
    assert (t.state.name, t.technician, t.resolution) == ("resolved", "u-neema", "Replaced faulty PSU")
    with pytest.raises(InvalidTransition):
        t.resolve("again")
