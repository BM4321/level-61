"""Library: the single place where lending rules (invariants) are enforced."""
from __future__ import annotations

import json
from collections import deque
from datetime import date, timedelta
from pathlib import Path

from .errors import (BookUnavailableError, LoanLimitError, MemberBlockedError, NotFoundError,
                     NotOnLoanError)
from .models import Book, Loan, Member, Policy
from .search import SearchIndex


class Library:
    """Invariants: open loans of a book <= its copies; open loans of a member <= policy.max_loans."""

    def __init__(self, policy: Policy | None = None, clock=date.today):
        self.policy = policy or Policy()
        self.clock = clock
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.loans: list[Loan] = []
        self.reservations: dict[str, deque[str]] = {}
        self._index = SearchIndex()
        self._next_loan_id = 1

    # ---- registration -------------------------------------------------
    def add_book(self, book: Book) -> None:
        if book.book_id in self.books:
            raise ValueError(f"duplicate book id {book.book_id}")
        self.books[book.book_id] = book
        self._index.add(book.book_id, book.title, book.author)

    def add_member(self, member: Member) -> None:
        if member.member_id in self.members:
            raise ValueError(f"duplicate member id {member.member_id}")
        self.members[member.member_id] = member

    # ---- queries --------------------------------------------------------
    def _book(self, book_id: str) -> Book:
        try:
            return self.books[book_id]
        except KeyError:
            raise NotFoundError(f"no book {book_id}") from None

    def _member(self, member_id: str) -> Member:
        try:
            return self.members[member_id]
        except KeyError:
            raise NotFoundError(f"no member {member_id}") from None

    def open_loans(self, *, book_id: str | None = None, member_id: str | None = None) -> list[Loan]:
        return [ln for ln in self.loans if ln.is_open
                and (book_id is None or ln.book_id == book_id)
                and (member_id is None or ln.member_id == member_id)]

    def available_copies(self, book_id: str) -> int:
        return self._book(book_id).copies - len(self.open_loans(book_id=book_id))

    def search(self, query: str) -> list[Book]:
        return sorted((self.books[b] for b in self._index.search(query)), key=lambda b: b.title)

    def overdue(self) -> list[Loan]:
        today = self.clock()
        return sorted((ln for ln in self.open_loans() if ln.days_overdue(today) > 0), key=lambda ln: ln.due_on)

    # ---- commands -------------------------------------------------------
    def borrow(self, member_id: str, book_id: str) -> Loan:
        member, _ = self._member(member_id), self._book(book_id)
        today = self.clock()
        if not member.active:
            raise MemberBlockedError(f"{member_id} is inactive")
        if member.fines_cents >= self.policy.max_fine_before_block_cents:
            raise MemberBlockedError(f"{member_id} has unpaid fines of {member.fines_cents / 100:.2f}")
        if any(ln.days_overdue(today) > 0 for ln in self.open_loans(member_id=member_id)):
            raise MemberBlockedError(f"{member_id} has overdue books")
        if len(self.open_loans(member_id=member_id)) >= self.policy.max_loans:
            raise LoanLimitError(f"{member_id} already has {self.policy.max_loans} books")
        queue = self.reservations.get(book_id)
        if queue and queue[0] != member_id and self.available_copies(book_id) <= len(queue):
            raise BookUnavailableError(f"{book_id} is reserved for another member")
        if self.available_copies(book_id) <= 0:
            raise BookUnavailableError(f"no copies of {book_id} available")
        if queue and queue[0] == member_id:
            queue.popleft()
        loan = Loan(self._next_loan_id, book_id, member_id, today, today + timedelta(days=self.policy.loan_days))
        self._next_loan_id += 1
        self.loans.append(loan)
        return loan

    def return_book(self, member_id: str, book_id: str) -> int:
        """Close the loan; returns the fine charged in cents (0 if on time)."""
        today = self.clock()
        for ln in self.open_loans(member_id=member_id, book_id=book_id):
            ln.returned_on = today
            fine = ln.days_overdue(today) * self.policy.fine_per_day_cents
            self._member(member_id).fines_cents += fine
            return fine
        raise NotOnLoanError(f"{member_id} does not have {book_id}")

    def reserve(self, member_id: str, book_id: str) -> int:
        """Join the FIFO reservation queue; returns queue position (1-based)."""
        self._member(member_id), self._book(book_id)
        queue = self.reservations.setdefault(book_id, deque())
        if member_id in queue:
            raise ValueError(f"{member_id} already reserved {book_id}")
        queue.append(member_id)
        return len(queue)

    def pay_fine(self, member_id: str, amount_cents: int) -> int:
        if amount_cents <= 0:
            raise ValueError("payment must be positive")
        m = self._member(member_id)
        m.fines_cents = max(0, m.fines_cents - amount_cents)
        return m.fines_cents

    # ---- persistence --------------------------------------------------------
    def save(self, path: Path) -> None:
        data = {
            "books": [vars(b) for b in self.books.values()],
            "members": [vars(m) for m in self.members.values()],
            "loans": [{**vars(ln), "borrowed_on": ln.borrowed_on.isoformat(), "due_on": ln.due_on.isoformat(),
                       "returned_on": ln.returned_on.isoformat() if ln.returned_on else None} for ln in self.loans],
            "reservations": {k: list(v) for k, v in self.reservations.items()},
            "next_loan_id": self._next_loan_id,
        }
        Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path, policy: Policy | None = None, clock=date.today) -> Library:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        lib = cls(policy, clock)
        for b in data["books"]:
            lib.add_book(Book(**b))
        for m in data["members"]:
            lib.add_member(Member(**m))
        for ln in data["loans"]:
            lib.loans.append(Loan(ln["loan_id"], ln["book_id"], ln["member_id"],
                                  date.fromisoformat(ln["borrowed_on"]), date.fromisoformat(ln["due_on"]),
                                  date.fromisoformat(ln["returned_on"]) if ln["returned_on"] else None))
        lib.reservations = {k: deque(v) for k, v in data["reservations"].items()}
        lib._next_loan_id = data["next_loan_id"]
        return lib
