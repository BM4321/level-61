"""PY-23: call the Open-Meteo API (needs internet; not testable in the vault build environment).
Run: python examples/py23_http.py [lat lon]
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from solutions.py23_solutions import ClientError, ServerError, UrllibTransport, WeatherClient  # noqa: E402

lat, lon = (float(sys.argv[1]), float(sys.argv[2])) if len(sys.argv) == 3 else (-6.82, 39.28)
client = WeatherClient(UrllibTransport())
try:
    print(client.current(lat, lon))
except (ClientError, ServerError, ValueError) as exc:
    print("Could not get weather:", exc)
