"""Inverted index over title and author words (PY-11)."""
import string


def words(text: str) -> set[str]:
    return {w.strip(string.punctuation) for w in text.casefold().split()} - {""}


class SearchIndex:
    def __init__(self):
        self._index: dict[str, set[str]] = {}

    def add(self, book_id: str, *texts: str) -> None:
        for text in texts:
            for w in words(text):
                self._index.setdefault(w, set()).add(book_id)

    def search(self, query: str) -> set[str]:
        terms = words(query)
        if not terms:
            return set()
        return set.intersection(*(self._index.get(t, set()) for t in terms))
