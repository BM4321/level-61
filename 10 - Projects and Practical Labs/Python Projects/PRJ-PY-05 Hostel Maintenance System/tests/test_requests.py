from dataclasses import replace

import pytest

from hostel.errors import ConcurrentUpdateError, PermissionDenied, TransitionError, ValidationError
from hostel.models import ALLOWED, HistoryEntry, Priority, Status
from hostel.repository import SqliteRepository

S = Status


def submit(w, who="res1", room="A-101", category="electrical", text="Socket sparks when the kettle is plugged in"):
    return w["svc"].submit(w[who], room, category, text)


def test_happy_path_and_audit_trail(world):
    w = world
    r = submit(w)
    assert r.status is S.NEW and r.priority is Priority.URGENT
    w["svc"].transition(w["warden"], r.id, S.ASSIGNED, assignee="TECH01")
    w["clock"].advance(hours=2)
    w["svc"].transition(w["tech1"], r.id, S.IN_PROGRESS)
    w["clock"].advance(hours=3)
    w["svc"].transition(w["tech1"], r.id, S.RESOLVED, note="Replaced the socket")
    w["svc"].transition(w["warden"], r.id, S.CLOSED)
    trail = [(h.old_status, h.new_status, h.actor) for h in w["repo"].history(r.id)]
    assert trail == [(None, S.NEW, "STU/21/0001"), (S.NEW, S.ASSIGNED, "WARDEN01"), (S.ASSIGNED, S.IN_PROGRESS, "TECH01"),
                     (S.IN_PROGRESS, S.RESOLVED, "TECH01"), (S.RESOLVED, S.CLOSED, "WARDEN01")]
    assert w["repo"].get_request(r.id).resolved_at == w["clock"].now


@pytest.mark.parametrize("old", list(Status))
def test_every_disallowed_transition_is_rejected(world, old):
    w = world
    r = submit(w)
    stored = replace(w["repo"].get_request(r.id), status=old, assignee="TECH01", resolved_at=w["clock"].now)
    w["repo"].save_change(stored, S.NEW, HistoryEntry(r.id, S.NEW, old, "test", w["clock"].now, "fixture"))
    for new in set(Status) - ALLOWED[old]:
        with pytest.raises(TransitionError):
            w["svc"].transition(w["warden"], r.id, new, assignee="TECH01")


def test_permissions(world):
    w = world
    r = submit(w)
    with pytest.raises(PermissionDenied):
        w["svc"].transition(w["res1"], r.id, S.ASSIGNED, assignee="TECH01")
    with pytest.raises(ValidationError):
        w["svc"].transition(w["warden"], r.id, S.ASSIGNED, assignee="STU/21/0002")   # not a technician
    w["svc"].transition(w["warden"], r.id, S.ASSIGNED, assignee="TECH01")
    with pytest.raises(PermissionDenied):
        w["svc"].transition(w["tech2"], r.id, S.IN_PROGRESS)                        # not the assignee
    with pytest.raises(PermissionDenied):
        submit(w, who="res1", room="B-204")                                          # not their room
    with pytest.raises(PermissionDenied):
        submit(w, who="tech1")
    assert submit(w, who="warden", room="B-204").reporter == "WARDEN01"


def _resolve(w):
    r = submit(w)
    w["svc"].transition(w["warden"], r.id, S.ASSIGNED, assignee="TECH01")
    w["svc"].transition(w["tech1"], r.id, S.IN_PROGRESS)
    w["svc"].transition(w["tech1"], r.id, S.RESOLVED)
    return r


def test_reopen_window_and_owner(world):
    w = world
    r = _resolve(w)
    with pytest.raises(PermissionDenied):
        w["svc"].transition(w["res2"], r.id, S.REOPENED)
    w["clock"].advance(days=7)
    reopened = w["svc"].transition(w["res1"], r.id, S.REOPENED, note="Sparking again")
    assert reopened.status is S.REOPENED and reopened.resolved_at is None
    w["svc"].transition(w["warden"], r.id, S.ASSIGNED, assignee="TECH02")
    w["svc"].transition(w["tech2"], r.id, S.IN_PROGRESS)
    w["svc"].transition(w["tech2"], r.id, S.RESOLVED)
    w["clock"].advance(days=7, seconds=1)
    with pytest.raises(TransitionError):
        w["svc"].transition(w["res1"], r.id, S.REOPENED)


def test_priority_and_visibility(world):
    w = world
    a = submit(w)
    b = submit(w, who="res2", room="B-204", category="furniture", text="Wardrobe door hinge is broken")
    assert b.priority is Priority.LOW
    assert w["svc"].set_priority(w["warden"], b.id, Priority.NORMAL).priority is Priority.NORMAL
    with pytest.raises(PermissionDenied):
        w["svc"].set_priority(w["res2"], b.id, Priority.URGENT)
    assert w["repo"].history(b.id)[-1].note == "priority low -> normal"
    w["svc"].transition(w["warden"], a.id, S.ASSIGNED, assignee="TECH01")
    assert [r.id for r in w["svc"].visible_to(w["res1"])] == [a.id]
    assert [r.id for r in w["svc"].visible_to(w["tech1"])] == [a.id]
    assert [r.id for r in w["svc"].visible_to(w["tech2"])] == []
    assert [r.id for r in w["svc"].visible_to(w["warden"])] == [a.id, b.id]
    with pytest.raises(PermissionDenied):
        w["svc"].history(w["res2"], a.id)
    w["svc"].transition(w["warden"], b.id, S.REJECTED, note="Duplicate of an earlier report")
    with pytest.raises(TransitionError):
        w["svc"].set_priority(w["warden"], b.id, Priority.URGENT)


def test_input_validation(world):
    w = world
    r = submit(w, text="Leak under\nthe sink\r\nFAKE LOG LINE")
    assert "\n" not in w["repo"].get_request(r.id).description
    for bad in ("short", "x" * 1001):
        with pytest.raises(ValidationError):
            submit(w, text=bad)
    with pytest.raises(ValidationError):
        submit(w, category="magic")
    with pytest.raises(ValidationError):
        submit(w, room="A101")
    hostile = "Door lock x'); DROP TABLE requests; -- broken"
    assert w["repo"].get_request(submit(w, text=hostile).id).description == hostile   # stored as data
    assert len(w["repo"].list_requests()) == 2


def test_optimistic_concurrency_between_two_connections(tmp_path, hasher, clock):
    from hostel.models import Role, Room
    from hostel.services import AuthService, RequestService
    path = str(tmp_path / "shared.db")
    a, b = SqliteRepository(path), SqliteRepository(path)
    a.add_room(Room("A-101", "A", 2))
    auth = AuthService(a, hasher, clock)
    res = auth.register("STU/21/0001", "Baraka Resident", Role.RESIDENT, "maple-signal-copper-4", "A-101")
    warden = auth.register("WARDEN01", "Asha Warden", Role.WARDEN, "violet-kettle-orbit-9")
    auth.register("TECH01", "Daudi Technician", Role.TECHNICIAN, "granite-paper-swift-2")
    auth.register("TECH02", "Eshe Technician", Role.TECHNICIAN, "cobalt-meadow-ferry-5")
    r = RequestService(a, clock).submit(res, "A-101", "plumbing", "Shower drain is blocked")
    stale = b.get_request(r.id)                                         # connection B reads NEW
    RequestService(a, clock).transition(warden, r.id, Status.ASSIGNED, assignee="TECH01")
    with pytest.raises(ConcurrentUpdateError):                          # B's write based on NEW must fail
        b.save_change(replace(stale, status=Status.ASSIGNED, assignee="TECH02"), Status.NEW,
                      HistoryEntry(r.id, Status.NEW, Status.ASSIGNED, "WARDEN01", clock(), ""))
    assert b.get_request(r.id).assignee == "TECH01" and len(b.history(r.id)) == 2
    a.close(); b.close()


def test_update_and_history_are_atomic(tmp_path, hasher, clock):
    from hostel.models import Role, Room
    from hostel.services import AuthService, RequestService
    repo = SqliteRepository(str(tmp_path / "atomic.db"))
    repo.add_room(Room("A-101", "A", 2))
    res = AuthService(repo, hasher, clock).register("STU/21/0001", "Baraka Resident", Role.RESIDENT,
                                                    "maple-signal-copper-4", "A-101")
    r = RequestService(repo, clock).submit(res, "A-101", "plumbing", "Shower drain is blocked")
    bad_entry = HistoryEntry(999, Status.NEW, Status.REJECTED, "WARDEN01", clock(), "")   # FK violation
    with pytest.raises(Exception):
        repo.save_change(replace(r, status=Status.REJECTED), Status.NEW, bad_entry)
    assert repo.get_request(r.id).status is Status.NEW                  # the UPDATE was rolled back too
    assert len(repo.history(r.id)) == 1
    repo.close()
