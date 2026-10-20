---
title: "Security Headers and Configuration Analysis"
module: "Cyber Security"
module_code: "ITT06102"
topic_id: "LAB-CS-05"
type: "lab"
difficulty: "intermediate"
status: "not-started"
mastery: 0
prerequisites:
  - "[[CS-11 Web Application Security]]"
tags:
  - semester-6
  - cyber-security
  - lab
---

# LAB-CS-05 Security Headers and Configuration Analysis

> [!danger] Ethics and scope
> The script starts two demo web servers on `127.0.0.1` (your own machine only) and reviews their responses. If you use `--review-file`, capture headers only from sites **you own or administer**. Even a header request counts as interacting with a system; get permission before you test.

**Script:** `scripts/lab05_headers.py` · **Tests:** `tests/test_labs.py::test_lab05` (passing; uses real local HTTP) · **Time:** 45–75 min · **Related lessons:** [[CS-11 Web Application Security]], [[CS-09 Network Security and Secure Communication]]

## Objectives
1. Read HTTP response headers and identify missing or weak security controls.
2. Explain what each header defends against: HSTS, CSP, `nosniff`, Referrer-Policy, `frame-ancestors`, cookie flags.
3. Recognise information leaks (version banners) and risky CORS settings.
4. Write a hardened header set and check it automatically.

## Prerequisites
- Python 3.10+ (standard library only: `http.server`, `urllib`).
- CS-11 §5.5.

## Setup
```bash
cd "10 - Projects and Practical Labs/Cyber Security Labs"
```
The servers bind to `127.0.0.1` on random free ports, are never reachable from other machines, and are stopped automatically.

## Procedure (commands)
1. `python scripts/lab05_headers.py`
2. Compare the two header lists line by line, and match each finding to the header that's missing or wrong.
3. Edit `INSECURE` in the script to fix one issue at a time (e.g. add `"X-Content-Type-Options": "nosniff"`), and re-run to watch the finding count fall.
4. Add `'unsafe-inline'` to the hardened CSP's `default-src` and re-run. What does the script report?
5. Optional, for your own site: `curl -sI https://<your-own-site> > headers.txt`, then `python scripts/lab05_headers.py --review-file headers.txt`.

## Expected output
Real output from the build machine (the `Date` lines will differ):
```text
== INSECURE demo server ==
  Server: Apache/2.4.41 (Ubuntu)
  Date: Tue, 20 Oct 2026 04:27:38 GMT
  X-Powered-By: PHP/7.2.24
  Set-Cookie: session=demo123; Path=/
  Access-Control-Allow-Origin: *
  Content-Type: text/html; charset=utf-8
  Content-Length: 20
  -> 11 finding(s)
     MISSING  HSTS missing: browsers may use plain HTTP
     MISSING  CSP missing: no second line of defence against XSS
     MISSING  nosniff missing: MIME-sniffing attacks possible
     MISSING  Referrer-Policy missing: full URLs may leak to other sites
     MISSING  clickjacking protection (frame-ancestors / X-Frame-Options)
     LEAK     server: Apache/2.4.41 (Ubuntu)  (version disclosure)
     LEAK     x-powered-by: PHP/7.2.24 (version disclosure)
     REVIEW   CORS allows any origin (acceptable only for truly public, non-credentialed data)
     COOKIE   session cookie missing secure
     COOKIE   session cookie missing httponly
     COOKIE   session cookie missing samesite

== HARDENED demo server ==
  Server: demo
  ...
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; base-uri 'self'
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Set-Cookie: session=demo123; Path=/; Secure; HttpOnly; SameSite=Lax
  -> 0 finding(s)
```
(The "Apache"/"PHP" banners are **fake** strings that the demo server sends; no Apache or PHP is running.)

## Interpretation
| Finding | Risk | Fix |
|---|---|---|
| No HSTS | The first visit or a typed `http://` can be downgraded or intercepted | `Strict-Transport-Security: max-age=31536000; includeSubDomains` (over HTTPS only) |
| No CSP | Any XSS bug can load or run arbitrary scripts | Start with `default-src 'self'`, then allow-list what's needed |
| No `nosniff` | Browsers may treat uploaded text as script or HTML | `X-Content-Type-Options: nosniff` |
| No Referrer-Policy | Full URLs, possibly with IDs or tokens, leak to other sites | `strict-origin-when-cross-origin` |
| No frame-ancestors | Clickjacking: the site is framed invisibly | `frame-ancestors 'none'` (or `X-Frame-Options: DENY`) |
| Version banners | Attackers match versions to known vulnerabilities | Remove or genericise `Server` and `X-Powered-By` |
| CORS `*` | Fine for public data; dangerous if combined with credentials or sensitive APIs | An explicit allow-list of origins |
| Cookie flags missing | Theft by XSS (no HttpOnly), sent over HTTP (no Secure), CSRF (no SameSite) | `Secure; HttpOnly; SameSite=Lax` |

Two caveats:
- Browsers **ignore HSTS sent over plain HTTP**. Our local demo uses HTTP only to show the header; in production HSTS must come over HTTPS.
- Headers are **defence in depth**. They don't fix XSS, CSRF or access-control bugs in the application ([[CS-11 Web Application Security]]).

## Cleanup
The servers stop when the script ends. If you created `headers.txt`, delete it. Revert your edits to the script with `git checkout scripts/lab05_headers.py`, or by hand.

## Questions
1. Why does HSTS have to be delivered over HTTPS?
2. What does `object-src 'none'` block, and why is it in the hardened CSP?
3. A developer says, "Our API returns `Access-Control-Allow-Origin: *`, so it's insecure." When is that correct, and when not?
4. Which finding would you fix first on a login page, and why?
5. Write a CSP for a page that loads scripts from itself and from `https://cdn.example.org`, images from anywhere over HTTPS, and must not be framed.

## Answers
> [!success]- Answers
> 1. Over HTTP an attacker could strip or inject the header, so browsers accept it only from a secure connection. After that, they automatically upgrade future requests for `max-age` seconds. Preload lists protect even the first visit.
> 2. It blocks plugin content (`<object>`, `<embed>`), a historical source of script execution that modern sites don't need. Disallowing it closes a CSP bypass route.
> 3. It's correct to worry if the API serves user-specific or sensitive data, or if the server also allows credentials (browsers refuse `*` together with credentials, so developers sometimes "fix" this by reflecting any `Origin`, which is dangerous). It's fine for truly public, read-only, non-credentialed data such as an open timetable.
> 4. The cookie flags (Secure, HttpOnly, SameSite) together with HSTS, because they protect the session token that represents the logged-in user. Without them, the session can be stolen through XSS or interception, or abused through CSRF.
> 5. `Content-Security-Policy: default-src 'self'; script-src 'self' https://cdn.example.org; img-src https:; object-src 'none'; base-uri 'self'; frame-ancestors 'none'`

## Defensive lessons
- Ship a baseline header set from the web server or framework configuration, so every route gets it.
- Remove version banners, and keep the software patched anyway.
- Set session cookies with `Secure; HttpOnly; SameSite`.
- Roll out CSP with `Content-Security-Policy-Report-Only` first, then enforce it.
- Automate header checks in CI against staging.

## Mastery checklist
- [ ] I can explain every one of the 11 findings
- [ ] I reduced the insecure server's findings to zero by editing its headers
- [ ] I wrote a CSP for a stated set of requirements
