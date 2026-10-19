"""PY-23 reference solutions (HTTP API client with injectable transport).

Live calls were NOT possible in the build environment (network policy); all tests use fakes.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.open-meteo.com/v1/forecast"


class ClientError(Exception):
    """4xx: the request is wrong; do not retry."""


class ServerError(Exception):
    """5xx, 429 or network failure: retryable."""


def build_url(base: str, params: dict) -> str:
    """base?urlencoded-params."""
    return f"{base}?{urllib.parse.urlencode(params)}"


def parse_current(payload: dict) -> dict:
    """Validate and extract {'time', 'temperature', 'unit'}; ValueError on bad shape."""
    try:
        current = payload["current"]
        units = payload.get("current_units", {})
        temp = float(current["temperature_2m"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"unexpected API response shape: {exc!r}") from exc
    if not -90 <= temp <= 60:
        raise ValueError(f"implausible temperature {temp}")
    return {"time": current.get("time"), "temperature": temp, "unit": units.get("temperature_2m", "°C")}


def classify_status(code: int) -> str:
    """'success', 'retryable', 'client_error' or 'other'."""
    if 200 <= code < 300:
        return "success"
    if code == 429 or 500 <= code < 600:
        return "retryable"
    if 400 <= code < 500:
        return "client_error"
    return "other"


def get_api_key(env, name: str) -> str:
    """Read a key from a mapping (e.g. os.environ); RuntimeError naming the variable if unset."""
    value = env.get(name, "").strip()
    if not value:
        raise RuntimeError(f"environment variable {name} is not set; see .env.example")
    return value


class UrllibTransport:
    """Real network transport (standard library). [given]"""

    def get_json(self, url: str, timeout: float) -> dict:
        req = urllib.request.Request(url, headers={"Accept": "application/json",
                                                   "User-Agent": "semester6-weather-client/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if classify_status(exc.code) == "retryable":
                raise ServerError(f"HTTP {exc.code}") from exc
            raise ClientError(f"HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ServerError(f"network problem: {exc}") from exc


class WeatherClient:
    """Current-weather client using an injected transport."""

    def __init__(self, transport, base: str = BASE):
        self.transport, self.base = transport, base

    def current(self, lat: float, lon: float) -> dict:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            raise ValueError("coordinates out of range")
        url = build_url(self.base, {"latitude": lat, "longitude": lon, "current": "temperature_2m"})
        return parse_current(self.transport.get_json(url, timeout=10))


class CachedWeatherClient(WeatherClient):
    """Adds a TTL cache and retries with exponential backoff on ServerError."""

    def __init__(self, transport, ttl: float = 600, clock=time.monotonic, sleep=time.sleep,
                 attempts: int = 3, base: str = BASE):
        super().__init__(transport, base)
        self.ttl, self.clock, self.sleep, self.attempts = ttl, clock, sleep, attempts
        self._cache: dict[tuple[float, float], tuple[float, dict]] = {}

    def current(self, lat: float, lon: float) -> dict:
        key = (round(lat, 2), round(lon, 2))
        hit = self._cache.get(key)
        if hit and self.clock() - hit[0] < self.ttl:
            return hit[1]
        for attempt in range(1, self.attempts + 1):
            try:
                result = super().current(lat, lon)
                self._cache[key] = (self.clock(), result)
                return result
            except ServerError:
                if attempt == self.attempts:
                    raise
                self.sleep(0.5 * 2 ** (attempt - 1))
        raise AssertionError("unreachable")
