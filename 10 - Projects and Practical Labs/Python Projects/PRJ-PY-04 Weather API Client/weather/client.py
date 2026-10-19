"""WeatherService: URL building, retries with backoff, TTL cache (all dependencies injectable)."""
from __future__ import annotations

import re
import time
import urllib.parse

from .parsing import Current, DayForecast, Place, parse_current, parse_daily, parse_place
from .transport import ServerError

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
CITY_RE = re.compile(r"[^\W\d_][\w .'-]{0,59}")


def validate_city(raw: str) -> str:
    city = " ".join(raw.split())
    if not CITY_RE.fullmatch(city):
        raise ValueError("city name must be 1-60 letters/spaces/.'- and start with a letter")
    return city


def build_url(base: str, params: dict) -> str:
    return f"{base}?{urllib.parse.urlencode(params)}"


class WeatherService:
    def __init__(self, transport, clock=time.monotonic, sleep=time.sleep, ttl: float = 600, attempts: int = 3):
        self.transport, self.clock, self.sleep = transport, clock, sleep
        self.ttl, self.attempts = ttl, attempts
        self._cache: dict[str, tuple[float, dict]] = {}
        self.network_calls = 0

    def _get(self, url: str) -> dict:
        hit = self._cache.get(url)
        if hit and self.clock() - hit[0] < self.ttl:
            return hit[1]
        for attempt in range(1, self.attempts + 1):
            try:
                self.network_calls += 1
                payload = self.transport.get_json(url, timeout=10)
                self._cache[url] = (self.clock(), payload)
                return payload
            except ServerError:
                if attempt == self.attempts:
                    raise
                self.sleep(0.5 * 2 ** (attempt - 1))
        raise AssertionError("unreachable")

    def find_place(self, city: str) -> Place:
        url = build_url(GEOCODE_URL, {"name": validate_city(city), "count": 1, "format": "json"})
        return parse_place(self._get(url))

    def current(self, place: Place) -> Current:
        url = build_url(FORECAST_URL, {"latitude": place.latitude, "longitude": place.longitude,
                                       "current": "temperature_2m,wind_speed_10m,weather_code",
                                       "timezone": "auto"})
        return parse_current(self._get(url))

    def forecast(self, place: Place, days: int = 3) -> list[DayForecast]:
        if not 1 <= days <= 7:
            raise ValueError("days must be 1-7")
        url = build_url(FORECAST_URL, {"latitude": place.latitude, "longitude": place.longitude,
                                       "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
                                       "forecast_days": days, "timezone": "auto"})
        return parse_daily(self._get(url))
