from datetime import datetime

import pytest

from labbook.app import demo_directory
from labbook.domain import BookingStatus, TimeSlot
from labbook.errors import RuleViolation
from labbook.events import EventBus
from labbook.repository import InMemoryBookingRepository
from labbook.rules import WeeklyQuota
from labbook.service import BookingService
from patterns.creational import BookingBuilder, rules_from_config
from patterns.structural import LoggingRepository, SmsNotificationAdapter, ThirdPartySmsClient


def test_decorator_adds_logging_transparently():
    log = []
    repo = LoggingRepository(InMemoryBookingRepository(), log)
    svc = BookingService(repo, demo_directory(), EventBus())
    b = svc.book("u-amina", "LAB1-01", TimeSlot(datetime(2026, 3, 2, 9), datetime(2026, 3, 2, 10)))
    svc.cancel("u-amina", b.booking_id)
    assert log == ["add #1 LAB1-01", "get #1", "save #1 cancelled"]


def test_adapter_bridges_vendor_sdk_to_event_bus():
    client = ThirdPartySmsClient()
    bus = EventBus()
    bus.subscribe("booking.confirmed", SmsNotificationAdapter(client, {"u-amina": "+255700000001"}))
    svc = BookingService(InMemoryBookingRepository(), demo_directory(), bus)
    svc.book("u-amina", "LAB1-01", TimeSlot(datetime(2026, 3, 2, 9), datetime(2026, 3, 2, 10)))
    svc.book("u-baraka", "LAB1-02", TimeSlot(datetime(2026, 3, 2, 9), datetime(2026, 3, 2, 10)))  # no phone
    assert client.sent == [{"msisdn": "+255700000001", "text": "LabBook: confirmed #1", "sender": "LABBOOK"}]


def test_builder():
    b = BookingBuilder().by("u-baraka").on("LAB1-02").at(datetime(2026, 3, 3, 14), hours=2).confirmed().build()
    assert (b.user_id, b.ws_id, b.slot.hours, b.status) == ("u-baraka", "LAB1-02", 2.0, BookingStatus.CONFIRMED)
    assert BookingBuilder().build().slot.hours == 1.0


def test_factory_from_config():
    rs = rules_from_config([{"type": "in-service"}, {"type": "no-overlap"}, {"type": "weekly-quota", "max_hours": 4}])
    assert [r.name for r in rs.rules] == ["in-service", "no-overlap", "weekly-quota"]
    assert isinstance(rs.rules[2], WeeklyQuota) and rs.rules[2].max_hours == 4.0
    svc = BookingService(InMemoryBookingRepository(), demo_directory(), EventBus(), rules=rs)
    with pytest.raises(RuleViolation):
        svc.book("u-amina", "LAB1-01", TimeSlot(datetime(2026, 3, 2, 9), datetime(2026, 3, 2, 14)))   # 5 h > 4 h
    with pytest.raises(ValueError):
        rules_from_config([{"type": "teleport"}])
