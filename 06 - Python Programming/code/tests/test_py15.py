import json

import pytest

from _target import load

m = load("py15")


def test_safe_divide():
    assert m.safe_divide(10, 4) == 2.5
    assert m.safe_divide(1, 0) is None
    with pytest.raises(TypeError):
        m.safe_divide("1", 2)


@pytest.mark.parametrize("text, expected", [("42", 42), (" 7 ", 7), ("x", -1), (None, -1), ("4.5", -1)])
def test_parse_int_or_default(text, expected):
    assert m.parse_int_or_default(text, -1) == expected


def fake_input(values):
    it = iter(values)
    return lambda prompt: next(it)


def test_read_int(capsys):
    assert m.read_int("n? ", input_fn=fake_input(["x", "7"])) == 7
    assert "'x' is not a whole number" in capsys.readouterr().out
    with pytest.raises(ValueError, match="too many"):
        m.read_int("n? ", attempts=2, input_fn=fake_input(["a", "b"]))


def test_withdraw():
    assert m.withdraw(100, 30) == 70
    with pytest.raises(ValueError):
        m.withdraw(100, 0)
    with pytest.raises(m.InsufficientFundsError) as info:
        m.withdraw(50, 80)
    assert info.value.balance == 50 and info.value.amount == 80
    assert isinstance(info.value, m.BankError)


def test_load_config(tmp_path):
    p = tmp_path / "c.json"
    assert m.load_config(p) == {}
    p.write_text(json.dumps({"port": 8080}), encoding="utf-8")
    assert m.load_config(p) == {"port": 8080}
    p.write_text("{oops", encoding="utf-8")
    with pytest.raises(m.ConfigError) as info:
        m.load_config(p)
    assert isinstance(info.value.__cause__, json.JSONDecodeError)


def test_retry_succeeds_after_two_failures():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise TimeoutError("slow")
        return "ok"

    delays = []
    assert m.retry(flaky, attempts=3, delay=0.5, sleep=delays.append) == "ok"
    assert delays == [0.5, 1.0]


def test_retry_gives_up_and_ignores_other_errors():
    def always_timeout():
        raise TimeoutError("down")

    with pytest.raises(TimeoutError):
        m.retry(always_timeout, attempts=2, sleep=lambda s: None)

    def bad_value():
        raise ValueError("permanent")

    delays = []
    with pytest.raises(ValueError):
        m.retry(bad_value, attempts=3, sleep=delays.append)
    assert delays == []


def test_process_batch():
    results, failures = m.process_batch(["1", "x", "3"], int)
    assert results == [1, 3]
    assert [i for i, _ in failures] == [1] and isinstance(failures[0][1], ValueError)
