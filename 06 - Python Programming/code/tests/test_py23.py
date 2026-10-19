import pytest

from _target import load

m = load("py23")

SAMPLE = {"latitude": -6.8, "longitude": 39.3,
          "current_units": {"time": "iso8601", "temperature_2m": "°C"},
          "current": {"time": "2026-10-19T12:00", "temperature_2m": 29.4}}


class FakeTransport:
    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def get_json(self, url, timeout):
        self.urls.append(url)
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r


def test_build_url_encodes():
    url = m.build_url("https://geocoding.example/search", {"name": "Dar es Salaam", "count": 1})
    assert url == "https://geocoding.example/search?name=Dar+es+Salaam&count=1"


def test_parse_current():
    assert m.parse_current(SAMPLE) == {"time": "2026-10-19T12:00", "temperature": 29.4, "unit": "°C"}
    for bad in ({}, {"current": {}}, {"current": {"temperature_2m": "hot"}}, {"current": {"temperature_2m": 999}}):
        with pytest.raises(ValueError):
            m.parse_current(bad)


@pytest.mark.parametrize("code, kind", [(200, "success"), (204, "success"), (404, "client_error"),
                                        (401, "client_error"), (429, "retryable"), (503, "retryable"),
                                        (301, "other")])
def test_classify_status(code, kind):
    assert m.classify_status(code) == kind


def test_get_api_key():
    assert m.get_api_key({"K": " abc "}, "K") == "abc"
    with pytest.raises(RuntimeError) as info:
        m.get_api_key({"K": ""}, "K")
    assert "K" in str(info.value)


def test_weather_client_validates_before_network():
    t = FakeTransport([SAMPLE])
    c = m.WeatherClient(t)
    with pytest.raises(ValueError):
        c.current(100, 0)
    assert t.urls == []
    assert c.current(-6.82, 39.28)["temperature"] == 29.4
    assert "latitude=-6.82" in t.urls[0] and "current=temperature_2m" in t.urls[0]


def test_cache_and_retry():
    now = [1000.0]
    sleeps = []
    t = FakeTransport([m.ServerError("503"), SAMPLE, SAMPLE])
    c = m.CachedWeatherClient(t, ttl=600, clock=lambda: now[0], sleep=sleeps.append)
    assert c.current(-6.82, 39.28)["temperature"] == 29.4
    assert sleeps == [0.5] and len(t.urls) == 2
    now[0] += 300
    c.current(-6.82, 39.28)
    assert len(t.urls) == 2                      # cache hit
    now[0] += 301
    c.current(-6.82, 39.28)
    assert len(t.urls) == 3                      # expired → refetch


def test_client_error_not_retried():
    sleeps = []
    t = FakeTransport([m.ClientError("404"), SAMPLE])
    c = m.CachedWeatherClient(t, sleep=sleeps.append)
    with pytest.raises(m.ClientError):
        c.current(0, 0)
    assert sleeps == [] and len(t.urls) == 1
