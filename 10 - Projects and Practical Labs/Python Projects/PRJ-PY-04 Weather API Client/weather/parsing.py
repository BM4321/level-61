"""Pure validation/parsing of API payloads (treat responses as untrusted input)."""
from __future__ import annotations

from dataclasses import dataclass

# Subset of WMO weather interpretation codes as listed in the Open-Meteo documentation.
WMO_CODES = {0: "clear sky", 1: "mainly clear", 2: "partly cloudy", 3: "overcast", 45: "fog",
             48: "depositing rime fog", 51: "light drizzle", 53: "drizzle", 55: "dense drizzle",
             61: "slight rain", 63: "rain", 65: "heavy rain", 71: "slight snow", 73: "snow",
             75: "heavy snow", 80: "rain showers", 81: "heavy rain showers", 82: "violent rain showers",
             95: "thunderstorm"}


class ResponseError(ValueError):
    """API response did not have the expected shape or values."""


@dataclass(frozen=True)
class Place:
    name: str
    country: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class Current:
    time: str
    temperature: float
    wind_speed: float
    description: str


@dataclass(frozen=True)
class DayForecast:
    date: str
    t_min: float
    t_max: float
    precipitation_mm: float


def describe(code) -> str:
    try:
        return WMO_CODES.get(int(code), f"code {int(code)}")
    except (TypeError, ValueError):
        return "unknown"


def _num(container: dict, key: str, low: float, high: float) -> float:
    try:
        value = float(container[key])
    except (KeyError, TypeError, ValueError) as exc:
        raise ResponseError(f"missing or non-numeric field {key!r}") from exc
    if not low <= value <= high:
        raise ResponseError(f"implausible {key}={value}")
    return value


def parse_place(payload: dict) -> Place:
    results = payload.get("results") if isinstance(payload, dict) else None
    if not results:
        raise LookupError("place not found")
    r = results[0]
    return Place(str(r.get("name", "?")), str(r.get("country", "")),
                 _num(r, "latitude", -90, 90), _num(r, "longitude", -180, 180))


def parse_current(payload: dict) -> Current:
    cur = payload.get("current") if isinstance(payload, dict) else None
    if not isinstance(cur, dict):
        raise ResponseError("missing 'current' block")
    return Current(str(cur.get("time", "")), _num(cur, "temperature_2m", -90, 60),
                   _num(cur, "wind_speed_10m", 0, 500), describe(cur.get("weather_code")))


def parse_daily(payload: dict) -> list[DayForecast]:
    d = payload.get("daily") if isinstance(payload, dict) else None
    if not isinstance(d, dict):
        raise ResponseError("missing 'daily' block")
    try:
        cols = [d["time"], d["temperature_2m_min"], d["temperature_2m_max"], d["precipitation_sum"]]
    except KeyError as exc:
        raise ResponseError(f"missing daily field {exc}") from exc
    if len({len(c) for c in cols}) != 1:
        raise ResponseError("daily arrays have different lengths")
    days = []
    for day, lo, hi, rain in zip(*cols):
        rec = {"lo": lo, "hi": hi, "rain": rain}
        days.append(DayForecast(str(day), _num(rec, "lo", -90, 60), _num(rec, "hi", -90, 60), _num(rec, "rain", 0, 2000)))
    return days
