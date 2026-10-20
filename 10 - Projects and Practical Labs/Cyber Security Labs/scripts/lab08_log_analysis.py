"""LAB-CS-08: analyse an SSH/sudo authentication log and build an incident timeline.

Run:  python lab08_log_analysis.py [logfile]     (default: ../data/auth_sample.log, a CONSTRUCTED log)
To analyse a real log, use only one from a machine you administer, e.g. a copy of /var/log/auth.log.
"""
import hashlib
import re
import sys
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

AUTH = re.compile(r"^(?P<ts>\S+) host=(?P<host>\S+) sshd\[\d+\]: (?P<result>Accepted|Failed) (?P<method>password|publickey) "
                  r"for (?P<invalid>invalid user )?(?P<user>\S+) from (?P<ip>\S+) port \d+")
SUDO = re.compile(r"^(?P<ts>\S+) host=(?P<host>\S+) sudo: (?P<user>\S+) : .*COMMAND=(?P<command>.+)$")
DEFAULT_LOG = Path(__file__).resolve().parent.parent / "data" / "auth_sample.log"


def parse(lines):
    events, skipped = [], 0
    for line in lines:
        line = line.rstrip("\n")
        if m := AUTH.match(line):
            e = m.groupdict()
            e["kind"] = "login_" + e.pop("result").lower()
            e["invalid"] = bool(e["invalid"])
        elif m := SUDO.match(line):
            e = m.groupdict()
            e["kind"] = "sudo"
        else:
            skipped += line.strip() != ""
            continue
        e["ts"] = datetime.fromisoformat(e["ts"].replace("Z", "+00:00"))
        events.append(e)
    return events, skipped


def bursts(events, threshold, window):
    by_ip = {}
    for e in events:
        if e["kind"] == "login_failed":
            by_ip.setdefault(e["ip"], []).append(e["ts"])
    out = {}
    for ip, ts in by_ip.items():
        ts.sort()
        start = best = 0
        for end in range(len(ts)):
            while ts[end] - ts[start] > window:
                start += 1
            best = max(best, end - start + 1)
        if best >= threshold:
            out[ip] = best
    return out


def spraying(events, min_users=5, window=timedelta(minutes=10)):
    by_ip = {}
    for e in events:
        if e["kind"] == "login_failed":
            by_ip.setdefault(e["ip"], []).append((e["ts"], e["user"]))
    out = {}
    for ip, items in by_ip.items():
        items.sort()
        start = 0
        for end in range(len(items)):
            while items[end][0] - items[start][0] > window:
                start += 1
            users = {u for _, u in items[start:end + 1]}
            if len(users) >= min_users:
                out[ip] = max(out.get(ip, 0), len(users))
    return out


def success_after_failures(events, min_failures=3):
    streak, hits = {}, []
    for e in sorted((x for x in events if x["kind"].startswith("login_")), key=lambda x: x["ts"]):
        if e["kind"] == "login_failed":
            streak[e["ip"]] = streak.get(e["ip"], 0) + 1
        else:
            if streak.get(e["ip"], 0) >= min_failures:
                hits.append(e)
            streak[e["ip"]] = 0
    return hits


def main(path: Path) -> None:
    raw = path.read_bytes()
    print(f"evidence: {path.name}  sha256={hashlib.sha256(raw).hexdigest()}")
    events, skipped = parse(raw.decode("utf-8").splitlines())
    print(f"parsed {len(events)} events, skipped {skipped} unparseable lines")
    print("by kind:", dict(Counter(e["kind"] for e in events)))
    print("failures by IP:", dict(Counter(e["ip"] for e in events if e["kind"] == "login_failed").most_common()))
    print("invalid usernames tried:", sorted({e["user"] for e in events if e.get("invalid")}))

    print("\n== Detections ==")
    print("D1 fast bursts (>=5 in 2 min):", bursts(events, 5, timedelta(minutes=2)))
    print("D2 slow guessing (>=3 in 1 h):", bursts(events, 3, timedelta(hours=1)))
    print("D3 spraying (>=5 users in 10 min from one IP):", spraying(events))
    hits = success_after_failures(events)
    print("D4 success after >=3 failures:", [(h["user"], h["ip"], h["ts"].isoformat()) for h in hits])

    print("\n== Timeline for each D4 hit (events from the same IP or user, next 10 minutes) ==")
    for h in hits:
        print(f"-- {h['user']} from {h['ip']}")
        start = h["ts"] - timedelta(minutes=1)
        for e in sorted(events, key=lambda x: x["ts"]):
            near = start <= e["ts"] <= h["ts"] + timedelta(minutes=10)
            related = e.get("ip") == h["ip"] or e["user"] == h["user"]
            if near and related:
                what = e.get("command") or f"{e['kind']} ({e.get('method')}) for {e['user']} from {e.get('ip')}"
                print(f"   {e['ts'].strftime('%H:%M:%S')}Z  {what}")


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG)
