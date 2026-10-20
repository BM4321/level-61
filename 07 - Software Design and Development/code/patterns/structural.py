"""Structural patterns around LabBook: Decorator, Adapter, Facade-style helpers."""
from __future__ import annotations

from labbook.domain import Booking
from labbook.events import Event
from labbook.repository import BookingRepository


class LoggingRepository:
    """DECORATOR: same interface as the wrapped repository, adds behaviour (call logging)."""

    def __init__(self, inner: BookingRepository, log: list[str]):
        self.inner, self.log = inner, log

    def add(self, booking: Booking) -> Booking:
        result = self.inner.add(booking)
        self.log.append(f"add #{result.booking_id} {result.ws_id}")
        return result

    def get(self, booking_id: int) -> Booking:
        self.log.append(f"get #{booking_id}")
        return self.inner.get(booking_id)

    def save(self, booking: Booking) -> None:
        self.inner.save(booking)
        self.log.append(f"save #{booking.booking_id} {booking.status.value}")

    def for_workstation(self, ws_id: str) -> list[Booking]:
        return self.inner.for_workstation(ws_id)

    def for_user(self, user_id: str) -> list[Booking]:
        return self.inner.for_user(user_id)


class ThirdPartySmsClient:
    """Pretend vendor SDK with an interface we do not control (no network: records calls)."""

    def __init__(self) -> None:
        self.sent: list[dict] = []

    def transmit(self, msisdn: str, text: str, sender_id: str = "LABBOOK") -> dict:
        self.sent.append({"msisdn": msisdn, "text": text, "sender": sender_id})
        return {"status": "QUEUED", "id": len(self.sent)}


class SmsNotificationAdapter:
    """ADAPTER: makes the vendor client look like an EventBus handler (callable taking an Event)."""

    def __init__(self, client: ThirdPartySmsClient, phone_book: dict[str, str]):
        self.client, self.phone_book = client, phone_book

    def __call__(self, event: Event) -> None:
        number = self.phone_book.get(event.user_id)
        if number:                                   # users without a phone number are skipped
            self.client.transmit(number, f"LabBook: {event.name.split('.')[-1]} #{event.booking_id}")
