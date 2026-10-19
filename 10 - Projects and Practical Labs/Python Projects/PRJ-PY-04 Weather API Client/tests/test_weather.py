import json
from pathlib import Path

import pytest

from weather.cli import main
from weather.client import WeatherService, validate_city
from weather.parsing import Place, ResponseError, describe, parse_current, parse_daily, parse_place
from weather.transport import ClientError, ServerError

FIX = Path(__file__).parent / "fixtures"
GEO, CUR, DAILY = (json.loads((FIX / n).read_text(encoding="utf-8"))
                   for n in ("geocode_dar.json", "current_dar.json", "daily_dar.json"))


class FakeTransport:
    """Returns fixtures by URL content; can be scripted to fail."""
    def __init__(self, failures=None):
        self.failures = list(failures or [])
        self.urls = []

    def get_json(self, url, timeout):
        self.urls.append(url)
        if self.failures:
            raise self.failures.pop(0)
        if "geocoding" in url:
            return GEO
        return DAILY if "daily=" in url else CUR


def svc(transport, **kw):
    now = [0.0]
    s = WeatherService(transport, clock=lambda: now[0], sleep=kw.pop("sleep", lambda s: None), **kw)
    return s, now


@pytest.mark.parametrize("raw, ok", [("Dar es Salaam", "Dar es Salaam"), ("  Mwanza ", "Mwanza"),
                                     ("Saint-Étienne", "Saint-Étienne"), ("O'Fallon", "O'Fallon")])
def test_validate_city_ok(raw, ok):
    assert validate_city(raw) == ok


@pytest.mark.parametrize("bad", ["", "123", "a" * 61, "Dodoma; rm -rf /", "<script>"])
def test_validate_city_bad(bad):
    with pytest.raises(ValueError):
        validate_city(bad)


def test_parsers():
    assert parse_place(GEO) == Place("Dar es Salaam", "Tanzania", -6.82349, 39.26951)
    cur = parse_current(CUR)
    assert (cur.temperature, cur.wind_speed, cur.description) == (30.2, 18.4, "partly cloudy")
    days = parse_daily(DAILY)
    assert [d.precipitation_mm for d in days] == [0.0, 2.4, 11.0]
    assert describe(99) == "code 99" and describe(None) == "unknown"


@pytest.mark.parametrize("bad", [{}, {"current": {"temperature_2m": "hot", "wind_speed_10m": 1}},
                                 {"current": {"temperature_2m": 300, "wind_speed_10m": 1}}])
def test_parse_current_rejects(bad):
    with pytest.raises(ResponseError):
        parse_current(bad)


def test_parse_daily_rejects_ragged():
    bad = {"daily": {"time": ["a", "b"], "temperature_2m_max": [1], "temperature_2m_min": [1], "precipitation_sum": [0]}}
    with pytest.raises(ResponseError):
        parse_daily(bad)


def test_place_not_found():
    with pytest.raises(LookupError):
        parse_place({"generationtime_ms": 0.5})


def test_urls_and_cache():
    t = FakeTransport()
    s, now = svc(t)
    place = s.find_place("Dar es Salaam")
    assert "name=Dar+es+Salaam" in t.urls[0]
    s.current(place)
    s.current(place)
    assert s.network_calls == 2                    # second current() served from cache
    now[0] = 601
    s.current(place)
    assert s.network_calls == 3


def test_retry_then_success_and_give_up():
    sleeps = []
    t = FakeTransport([ServerError("503"), ServerError("timeout")])
    s, _ = svc(t, sleep=sleeps.append)
    assert s.find_place("Mwanza").country == "Tanzania"
    assert sleeps == [0.5, 1.0]
    t2 = FakeTransport([ServerError("x")] * 3)
    s2, _ = svc(t2)
    with pytest.raises(ServerError):
        s2.find_place("Mwanza")


def test_client_error_not_retried():
    t = FakeTransport([ClientError("400")])
    s, _ = svc(t)
    with pytest.raises(ClientError):
        s.find_place("Arusha")
    assert len(t.urls) == 1


def test_forecast_days_validated():
    s, _ = svc(FakeTransport())
    with pytest.raises(ValueError):
        s.forecast(Place("x", "y", 0, 0), days=10)


def test_cli_success_and_errors(capsys):
    s, _ = svc(FakeTransport())
    assert main(["Dar es Salaam"], service=s) == 0
    out = capsys.readouterr().out
    assert "Weather for Dar es Salaam, Tanzania" in out and "rain 11.0 mm" in out
    s2, _ = svc(FakeTransport([ServerError("503")] * 3))
    assert main(["Dodoma"], service=s2) == 2
    assert "service unavailable" in capsys.readouterr().err
    assert main(["123"], service=s) == 1
