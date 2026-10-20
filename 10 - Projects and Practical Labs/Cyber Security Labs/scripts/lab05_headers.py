"""LAB-CS-05: security headers and configuration analysis against LOCAL demo servers only.

Run:  python lab05_headers.py
Starts two tiny HTTP servers on 127.0.0.1 (random free ports), fetches each, reviews the headers,
then shuts them down. Optional: python lab05_headers.py --review-file headers.txt  (paste headers you
captured from your OWN site with `curl -sI https://your-site`).
"""
import http.server
import sys
import threading
import urllib.request

INSECURE = {
    "Server": "Apache/2.4.41 (Ubuntu)",
    "X-Powered-By": "PHP/7.2.24",
    "Set-Cookie": "session=demo123; Path=/",
    "Access-Control-Allow-Origin": "*",
}
HARDENED = {
    "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
    "Content-Security-Policy": "default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Set-Cookie": "session=demo123; Path=/; Secure; HttpOnly; SameSite=Lax",
}

CHECKS = [
    ("strict-transport-security", "HSTS missing: browsers may use plain HTTP"),
    ("content-security-policy", "CSP missing: no second line of defence against XSS"),
    ("x-content-type-options", "nosniff missing: MIME-sniffing attacks possible"),
    ("referrer-policy", "Referrer-Policy missing: full URLs may leak to other sites"),
]


def review(headers: dict[str, str]) -> list[str]:
    h = {k.lower(): v for k, v in headers.items()}
    out = [f"MISSING  {msg}" for name, msg in CHECKS if name not in h]
    csp = h.get("content-security-policy", "")
    if "unsafe-inline" in csp:
        out.append("WEAK     CSP allows 'unsafe-inline'")
    if "frame-ancestors" not in csp and "x-frame-options" not in h:
        out.append("MISSING  clickjacking protection (frame-ancestors / X-Frame-Options)")
    for leak in ("server", "x-powered-by"):
        if leak in h and any(c.isdigit() for c in h[leak]):
            out.append(f"LEAK     {leak}: {h[leak]} (version disclosure)")
    if h.get("access-control-allow-origin") == "*":
        out.append("REVIEW   CORS allows any origin (acceptable only for truly public, non-credentialed data)")
    if "set-cookie" in h:
        flags = {p.strip().split("=")[0].lower() for p in h["set-cookie"].split(";")[1:]}
        for flag in ("secure", "httponly", "samesite"):
            if flag not in flags:
                out.append(f"COOKIE   session cookie missing {flag}")
    return out


def make_handler(extra: dict[str, str]):
    class Handler(http.server.BaseHTTPRequestHandler):
        server_version = extra.get("Server", "demo")
        sys_version = ""

        def do_GET(self):  # noqa: N802 (http.server naming)
            body = b"<h1>Hostel demo</h1>"
            self.send_response(200)
            for k, v in extra.items():
                if k != "Server":
                    self.send_header(k, v)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    return Handler


def fetch_headers(config: dict[str, str]) -> dict[str, str]:
    srv = http.server.HTTPServer(("127.0.0.1", 0), make_handler(config))
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{srv.server_port}/", timeout=5) as resp:
            return dict(resp.headers.items())
    finally:
        srv.shutdown()
        srv.server_close()


def main() -> None:
    for label, config in (("INSECURE demo server", INSECURE), ("HARDENED demo server", HARDENED)):
        headers = fetch_headers(config)
        print(f"== {label} ==")
        for k, v in headers.items():
            print(f"  {k}: {v}")
        findings = review(headers)
        print(f"  -> {len(findings)} finding(s)")
        for f in findings:
            print("     " + f)
        print()


def review_file(path: str) -> None:
    headers = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if ":" in line and not line.upper().startswith("HTTP/"):
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
    print("\n".join(review(headers)) or "no findings")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--review-file":
        review_file(sys.argv[2])
    else:
        main()
