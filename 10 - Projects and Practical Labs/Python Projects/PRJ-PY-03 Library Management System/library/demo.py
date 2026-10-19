"""Scripted demonstration: python -m library.demo"""
from datetime import date

from .errors import LibraryError
from .models import Book, Member
from .service import Library


class FakeClock:
    def __init__(self, today: date):
        self.today = today

    def __call__(self) -> date:
        return self.today


def main() -> None:
    clock = FakeClock(date(2026, 10, 1))
    lib = Library(clock=clock)
    lib.add_book(Book("B1", "Python Programming Basics", "A. Mwangi", 2022, copies=1))
    lib.add_book(Book("B2", "Discrete Mathematics for Computing", "J. Okello", 2019, copies=2))
    lib.add_member(Member("M1", "Amina"))
    lib.add_member(Member("M2", "Baraka"))
    print("search 'python':", [b.title for b in lib.search("python")])
    loan = lib.borrow("M1", "B1")
    print(f"M1 borrowed B1, due {loan.due_on}")
    try:
        lib.borrow("M2", "B1")
    except LibraryError as exc:
        print("M2 cannot borrow:", exc)
    print("M2 reserves B1, position", lib.reserve("M2", "B1"))
    clock.today = date(2026, 10, 20)           # 5 days late
    print("overdue loans:", [(ln.member_id, ln.book_id, ln.days_overdue(clock.today)) for ln in lib.overdue()])
    fine = lib.return_book("M1", "B1")
    print(f"M1 returned B1 late, fine {fine / 100:.2f}")
    print("M2 now borrows reserved B1, due", lib.borrow("M2", "B1").due_on)


if __name__ == "__main__":
    main()
