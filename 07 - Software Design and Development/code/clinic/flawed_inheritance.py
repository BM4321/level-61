"""FLAWED DESIGN, for critique only (SD Flawed Design Clinic, case F2): inheritance misuse."""


class Workstation:
    def __init__(self, ws_id):
        self.ws_id = ws_id
        self.bookings = []

    def book(self, user, hours):
        self.bookings.append((user, hours))
        return True


class GpuWorkstation(Workstation):
    def book(self, user, hours):
        # Strengthens the precondition: callers that work with any Workstation now break.
        if hours > 2:
            raise PermissionError("GPU sessions max 2 hours")
        return super().book(user, hours)


class OutOfServiceWorkstation(Workstation):
    def book(self, user, hours):
        raise NotImplementedError("cannot book")   # refused bequest


class BookingList(list):
    """Inherits ALL list methods, so callers can bypass the rules with append/insert/clear."""

    def add_booking(self, booking):
        if booking in self:
            raise ValueError("duplicate")
        self.append(booking)


def book_whole_lab(stations, user, hours):
    """Client code written against Workstation: works for the base class only."""
    return all(ws.book(user, hours) for ws in stations)
