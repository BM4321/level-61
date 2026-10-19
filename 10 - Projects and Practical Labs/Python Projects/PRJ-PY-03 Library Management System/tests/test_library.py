from datetime import date

import pytest

from library.errors import (BookUnavailableError, LibraryError, LoanLimitError, MemberBlockedError,
                            NotFoundError, NotOnLoanError)
from library.models import Book, Member, Policy
from library.service import Library


class Clock:
    def __init__(self, d):
        self.today = d

    def __call__(self):
        return self.today


@pytest.fixture
def clock():
    return Clock(date(2026, 10, 1))


@pytest.fixture
def lib(clock):
    lib = Library(clock=clock)
    lib.add_book(Book("B1", "Python Programming Basics", "A. Mwangi", 2022, copies=1))
    lib.add_book(Book("B2", "Discrete Mathematics for Computing", "J. Okello", 2019, copies=2))
    for i in range(3, 7):
        lib.add_book(Book(f"B{i}", f"Book {i}", "Various", 2020))
    lib.add_member(Member("M1", "Amina"))
    lib.add_member(Member("M2", "Baraka"))
    return lib


def test_model_validation():
    with pytest.raises(ValueError):
        Book("B9", "  ", "x", 2000)
    with pytest.raises(ValueError):
        Book("B9", "T", "x", 2000, copies=0)
    with pytest.raises(ValueError):
        Member("", "x")


def test_borrow_sets_due_date(lib):
    loan = lib.borrow("M1", "B1")
    assert loan.due_on == date(2026, 10, 15) and lib.available_copies("B1") == 0


def test_copies_invariant(lib):
    lib.borrow("M1", "B2")
    lib.borrow("M2", "B2")
    with pytest.raises(BookUnavailableError):
        lib.borrow("M1", "B2")


def test_loan_limit(lib):
    for b in ("B3", "B4", "B5"):
        lib.borrow("M1", b)
    with pytest.raises(LoanLimitError):
        lib.borrow("M1", "B6")


def test_unknown_ids(lib):
    with pytest.raises(NotFoundError):
        lib.borrow("M9", "B1")
    with pytest.raises(NotFoundError):
        lib.borrow("M1", "B99")


def test_overdue_fine_and_block(lib, clock):
    lib.borrow("M1", "B1")
    clock.today = date(2026, 10, 20)
    assert [ln.book_id for ln in lib.overdue()] == ["B1"]
    with pytest.raises(MemberBlockedError):
        lib.borrow("M1", "B3")                  # has overdue book
    assert lib.return_book("M1", "B1") == 5 * 50_00
    assert lib.members["M1"].fines_cents == 25_000
    lib.borrow("M1", "B3")                      # fine below block threshold → allowed


def test_fine_threshold_blocks(lib):
    lib.members["M1"].fines_cents = 1_000_00
    with pytest.raises(MemberBlockedError):
        lib.borrow("M1", "B1")
    assert lib.pay_fine("M1", 60_000) == 40_000
    lib.borrow("M1", "B1")


def test_return_errors(lib):
    with pytest.raises(NotOnLoanError):
        lib.return_book("M1", "B1")
    assert issubclass(NotOnLoanError, LibraryError)


def test_reservation_queue(lib):
    lib.borrow("M1", "B1")
    assert lib.reserve("M2", "B1") == 1
    with pytest.raises(ValueError):
        lib.reserve("M2", "B1")
    lib.return_book("M1", "B1")
    with pytest.raises(BookUnavailableError):
        lib.borrow("M1", "B1")                   # reserved for M2
    lib.borrow("M2", "B1")
    assert "B1" in lib.reservations and len(lib.reservations["B1"]) == 0


def test_search(lib):
    assert [b.book_id for b in lib.search("python")] == ["B1"]
    assert [b.book_id for b in lib.search("MATHEMATICS okello")] == ["B2"]
    assert lib.search("unknown") == []


def test_save_load_round_trip(lib, clock, tmp_path):
    lib.borrow("M1", "B1")
    lib.reserve("M2", "B1")
    p = tmp_path / "lib.json"
    lib.save(p)
    lib2 = Library.load(p, clock=clock)
    assert lib2.available_copies("B1") == 0
    assert list(lib2.reservations["B1"]) == ["M2"]
    assert lib2.borrow("M1", "B2").loan_id == 2


def test_custom_policy(clock):
    lib = Library(Policy(max_loans=1, loan_days=7), clock=clock)
    lib.add_book(Book("X", "T", "A", 2000, copies=5))
    lib.add_member(Member("M", "N"))
    assert lib.borrow("M", "X").due_on == date(2026, 10, 8)
    with pytest.raises(LoanLimitError):
        lib.borrow("M", "X")
