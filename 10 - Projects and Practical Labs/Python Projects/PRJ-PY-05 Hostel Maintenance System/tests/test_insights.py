from datetime import timedelta

from hostel.insights import possible_duplicates, repeat_rooms, work_queue
from hostel.models import Priority, Request, Status


def req(i, room, cat, prio, status, created):
    return Request(i, room, "S", cat, "x" * 10, prio, status, created)


def test_repeat_rooms_window_threshold_and_order(clock):
    t = clock()
    reqs = [req(1, "A-101", "plumbing", Priority.NORMAL, Status.CLOSED, t - timedelta(days=29)),
            req(2, "A-101", "electrical", Priority.URGENT, Status.NEW, t - timedelta(days=3)),
            req(3, "A-101", "plumbing", Priority.NORMAL, Status.NEW, t - timedelta(days=1)),
            req(4, "B-204", "furniture", Priority.LOW, Status.NEW, t - timedelta(days=31)),   # outside the window
            req(5, "B-204", "plumbing", Priority.NORMAL, Status.NEW, t - timedelta(days=2)),
            req(6, "B-204", "other", Priority.NORMAL, Status.NEW, t - timedelta(days=2)),
            req(7, "B-204", "other", Priority.NORMAL, Status.NEW, t),
            req(8, "C-300", "plumbing", Priority.NORMAL, Status.NEW, t),
            req(9, "B-204", "electrical", Priority.URGENT, Status.NEW, t)]
    assert repeat_rooms(reqs, t) == [("B-204", 4), ("A-101", 3)]
    assert repeat_rooms(reqs, t, threshold=5) == []
    assert repeat_rooms(reqs, t, days=40)[0] == ("B-204", 5)


def test_work_queue_urgent_then_oldest(clock):
    t = clock()
    reqs = [req(1, "A-101", "plumbing", Priority.NORMAL, Status.ASSIGNED, t - timedelta(hours=5)),
            req(2, "A-101", "electrical", Priority.URGENT, Status.NEW, t - timedelta(hours=1)),
            req(3, "B-204", "electrical", Priority.URGENT, Status.REOPENED, t - timedelta(hours=2)),
            req(4, "B-204", "furniture", Priority.LOW, Status.NEW, t - timedelta(days=3)),
            req(5, "C-300", "plumbing", Priority.NORMAL, Status.RESOLVED, t - timedelta(days=1))]  # not open
    assert [r.id for r in work_queue(reqs)] == [3, 2, 1, 4]


def test_possible_duplicates(clock):
    t = clock()
    reqs = [req(1, "A-101", "plumbing", Priority.NORMAL, Status.NEW, t),
            req(2, "A-101", "plumbing", Priority.NORMAL, Status.ASSIGNED, t),
            req(3, "A-101", "plumbing", Priority.NORMAL, Status.CLOSED, t),          # closed: not a duplicate
            req(4, "A-101", "electrical", Priority.URGENT, Status.NEW, t),
            req(5, "B-204", "plumbing", Priority.NORMAL, Status.NEW, t)]
    assert possible_duplicates(reqs) == {("A-101", "plumbing"): [1, 2]}
