from datetime import datetime, timedelta, timezone

import pytest

from hostel.models import Role, Room
from hostel.repository import InMemoryRepository, SqliteRepository
from hostel.security import PasswordHasher
from hostel.services import AuthService, RequestService

# Fictional test passwords: never reuse test credentials anywhere real.
PW = {"WARDEN01": "violet-kettle-orbit-9", "STU/21/0001": "maple-signal-copper-4", "STU/21/0002": "lantern-quiet-river-7",
      "TECH01": "granite-paper-swift-2", "TECH02": "cobalt-meadow-ferry-5"}


class FakeClock:
    def __init__(self) -> None:
        self.now = datetime(2026, 3, 2, 8, 0, tzinfo=timezone.utc)

    def __call__(self) -> datetime:
        return self.now

    def advance(self, **kw: float) -> None:
        self.now += timedelta(**kw)


@pytest.fixture
def clock() -> FakeClock:
    return FakeClock()


@pytest.fixture
def hasher() -> PasswordHasher:
    return PasswordHasher(n=2**10)       # fast for tests; production default is 2**17


@pytest.fixture(params=["memory", "sqlite"])
def repo(request, tmp_path):
    if request.param == "memory":
        yield InMemoryRepository()
    else:
        r = SqliteRepository(str(tmp_path / "hostel.db"))
        yield r
        r.close()


@pytest.fixture
def world(repo, hasher, clock):
    """Two rooms, a warden, two residents, two technicians."""
    repo.add_room(Room("A-101", "A", 2))
    repo.add_room(Room("B-204", "B", 1))
    auth = AuthService(repo, hasher, clock)
    users = {
        "warden": auth.register("WARDEN01", "Asha Warden", Role.WARDEN, PW["WARDEN01"]),
        "res1": auth.register("STU/21/0001", "Baraka Resident", Role.RESIDENT, PW["STU/21/0001"], "A-101"),
        "res2": auth.register("STU/21/0002", "Chiku Resident", Role.RESIDENT, PW["STU/21/0002"], "B-204"),
        "tech1": auth.register("TECH01", "Daudi Technician", Role.TECHNICIAN, PW["TECH01"]),
        "tech2": auth.register("TECH02", "Eshe Technician", Role.TECHNICIAN, PW["TECH02"]),
    }
    return {"repo": repo, "auth": auth, "svc": RequestService(repo, clock), "clock": clock, **users}
