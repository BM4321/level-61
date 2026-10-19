"""Domain exception hierarchy: callers can catch LibraryError for any rule violation."""


class LibraryError(Exception):
    """Base class for library rule violations (show the message to the user)."""


class NotFoundError(LibraryError):
    pass


class BookUnavailableError(LibraryError):
    pass


class LoanLimitError(LibraryError):
    pass


class MemberBlockedError(LibraryError):
    pass


class NotOnLoanError(LibraryError):
    pass
