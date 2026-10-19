import pytest

from _target import load

m = load("py09")


def test_count_vowels():
    assert m.count_vowels("Software Design") == 5
    assert m.count_vowels("") == 0
    assert m.count_vowels("rhythm") == 0


def test_normalise_and_acronym():
    assert m.normalise("  Dar es  Salaam ") == m.normalise("dar ES salaam") == "dar es salaam"
    assert m.acronym("portable network graphics") == "PNG"


@pytest.mark.parametrize("s, ok", [("Never odd or even", True), ("A man, a plan, a canal: Panama", True),
                                   ("abc", False), ("", True), ("!!", True)])
def test_palindromes(s, ok):
    assert m.is_palindrome_sentence(s) is ok
    assert m.is_palindrome_two_pointer(s) is ok


def test_caesar():
    assert m.caesar_shift("Attack at Dawn!", 3) == "Dwwdfn dw Gdzq!"
    assert m.caesar_shift("Dwwdfn dw Gdzq!", -3) == "Attack at Dawn!"
    assert m.caesar_shift("xyz", 3) == "abc"
    assert m.caesar_shift("abc", 26) == "abc"


def test_anagrams():
    assert m.are_anagrams("Listen", "Silent")
    assert m.are_anagrams("Dormitory", "dirty room")
    assert not m.are_anagrams("abc", "abd")
    assert not m.are_anagrams("aab", "abb")


def test_parse_settings():
    assert m.parse_settings("host=db1; port=5432 ;debug=true;") == {"host": "db1", "port": "5432", "debug": "true"}
    assert m.parse_settings("token=a=b") == {"token": "a=b"}
    with pytest.raises(ValueError):
        m.parse_settings("host=db1; broken")


def test_mask():
    assert m.mask("4111 1111 1111 1234") == "************1234"


def test_word_wrap():
    assert m.word_wrap("the quick brown fox", 10) == ["the quick", "brown fox"]
    assert m.word_wrap("", 5) == []
    assert m.word_wrap("supercalifragilistic is long", 6) == ["supercalifragilistic", "is", "long"]
    with pytest.raises(ValueError):
        m.word_wrap("x", 0)


def test_vigenere_round_trip():
    c = m.vigenere("Attack at dawn", "LEMON")
    assert c == "Lxfopv ef rnhr"
    assert m.vigenere(c, "LEMON", decrypt=True) == "Attack at dawn"
