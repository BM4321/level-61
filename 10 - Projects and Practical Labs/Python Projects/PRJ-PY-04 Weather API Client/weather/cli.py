"""python -m weather "Dar es Salaam" [--days 3]"""
import argparse
import sys

from .client import WeatherService
from .parsing import ResponseError
from .transport import ClientError, ServerError, UrllibTransport


def format_report(place, current, days) -> str:
    lines = [f"Weather for {place.name}, {place.country} ({place.latitude:.2f}, {place.longitude:.2f})",
             f"  Now ({current.time}): {current.temperature:.1f} °C, wind {current.wind_speed:.0f} km/h, "
             f"{current.description}"]
    for d in days:
        lines.append(f"  {d.date}: {d.t_min:.0f}–{d.t_max:.0f} °C, rain {d.precipitation_mm:.1f} mm")
    return "\n".join(lines)


def main(argv=None, service: WeatherService | None = None) -> int:
    p = argparse.ArgumentParser(prog="weather", description="Current weather and forecast (Open-Meteo)")
    p.add_argument("city")
    p.add_argument("--days", type=int, default=3)
    args = p.parse_args(argv)
    service = service or WeatherService(UrllibTransport())
    try:
        place = service.find_place(args.city)
        print(format_report(place, service.current(place), service.forecast(place, args.days)))
        return 0
    except (ValueError, LookupError) as exc:            # includes ResponseError
        kind = "unexpected API response" if isinstance(exc, ResponseError) else "error"
        print(f"{kind}: {exc}", file=sys.stderr)
        return 1
    except ClientError as exc:
        print(f"request rejected by the service: {exc}", file=sys.stderr)
        return 1
    except ServerError as exc:
        print(f"service unavailable, try again later: {exc}", file=sys.stderr)
        return 2
