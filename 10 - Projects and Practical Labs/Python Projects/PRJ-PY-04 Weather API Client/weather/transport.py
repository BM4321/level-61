"""Network adapter: maps urllib errors to two meaningful categories."""
import json
import urllib.error
import urllib.request


class ClientError(Exception):
    """Request rejected (4xx): do not retry."""


class ServerError(Exception):
    """Server/network problem (5xx, 429, timeout): retryable."""


class UrllibTransport:
    user_agent = "semester6-weather-client/1.0 (student project)"

    def get_json(self, url: str, timeout: float) -> dict:
        req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 429 or exc.code >= 500:
                raise ServerError(f"HTTP {exc.code}") from exc
            raise ClientError(f"HTTP {exc.code}") from exc
        except (urllib.error.URLError, TimeoutError) as exc:
            raise ServerError(f"network problem: {exc}") from exc
        except json.JSONDecodeError as exc:
            raise ServerError("response was not valid JSON") from exc
