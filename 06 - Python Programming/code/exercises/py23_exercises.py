"""PY23 exercises: implement each function, then run
    PY_TARGET=exercises python -m pytest tests/test_py23.py
"""

from __future__ import annotations
import json
import time
import urllib.error
import urllib.parse
import urllib.request
BASE = 'https://api.open-meteo.com/v1/forecast'

class ClientError(Exception):
    """4xx: the request is wrong; do not retry."""

class ServerError(Exception):
    """5xx, 429 or network failure: retryable."""

def build_url(base: str, params: dict) -> str:
    """base?urlencoded-params."""
    raise NotImplementedError

def parse_current(payload: dict) -> dict:
    """Validate and extract {'time', 'temperature', 'unit'}; ValueError on bad shape."""
    raise NotImplementedError

def classify_status(code: int) -> str:
    """'success', 'retryable', 'client_error' or 'other'."""
    raise NotImplementedError

def get_api_key(env, name: str) -> str:
    """Read a key from a mapping (e.g. os.environ); RuntimeError naming the variable if unset."""
    raise NotImplementedError

class UrllibTransport:
    """Real network transport (standard library). [given]"""

    def get_json(self, url: str, timeout: float) -> dict:
        req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': 'semester6-weather-client/1.0'})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if classify_status(exc.code) == 'retryable':
                raise ServerError(f'HTTP {exc.code}') from exc
            raise ClientError(f'HTTP {exc.code}') from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ServerError(f'network problem: {exc}') from exc

class WeatherClient:
    """Current-weather client using an injected transport."""

    def __init__(self, transport, base: str=BASE):
        raise NotImplementedError

    def current(self, lat: float, lon: float) -> dict:
        raise NotImplementedError

class CachedWeatherClient(WeatherClient):
    """Adds a TTL cache and retries with exponential backoff on ServerError."""

    def __init__(self, transport, ttl: float=600, clock=time.monotonic, sleep=time.sleep, attempts: int=3, base: str=BASE):
        raise NotImplementedError

    def current(self, lat: float, lon: float) -> dict:
        raise NotImplementedError
