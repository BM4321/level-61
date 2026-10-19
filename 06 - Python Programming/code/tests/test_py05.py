import pytest

from _target import load

m = load("py05")


@pytest.mark.parametrize("n", [0, 1, 4, 100])
def test_sum_to(n):
    assert m.sum_to(n) == n * (n + 1) // 2


def test_factorial():
    assert [m.factorial(k) for k in range(6)] == [1, 1, 2, 6, 24, 120]
    with pytest.raises(ValueError):
        m.factorial(-1)


@pytest.mark.parametrize("n, k", [(10, 3), (15, 5), (1, 2), (100, 7)])
def test_count_multiples(n, k):
    assert m.count_multiples(n, k) == n // k


def test_is_prime():
    primes = [2, 3, 5, 7, 11, 13, 97, 7919]
    composites = [-7, 0, 1, 4, 9, 91, 7917]
    assert all(m.is_prime(p) for p in primes)
    assert not any(m.is_prime(c) for c in composites)


def test_fizzbuzz():
    assert m.fizzbuzz(15) == ["1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                              "11", "Fizz", "13", "14", "FizzBuzz"]
    assert m.fizzbuzz(0) == []


def test_multiplication_table():
    assert m.multiplication_table(3) == "   1   2   3\n   2   4   6\n   3   6   9"


def test_collatz_steps():
    assert m.collatz_steps(1) == 0
    assert m.collatz_steps(6) == 8
    assert m.collatz_steps(27) == 111
    with pytest.raises(ValueError):
        m.collatz_steps(0)


def test_patterns():
    assert m.right_triangle(3) == "*\n**\n***"
    assert m.pyramid(3) == "  *\n ***\n*****"


def test_primes_up_to():
    assert m.primes_up_to(1) == []
    assert m.primes_up_to(30) == [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    assert len(m.primes_up_to(10_000)) == 1229


def test_fizzbuzz_rules():
    out = m.fizzbuzz_rules(21, [(3, "Fizz"), (5, "Buzz"), (7, "Bazz")])
    assert out[14] == "FizzBuzz" and out[20] == "FizzBazz" and out[6] == "Bazz" and out[0] == "1"
