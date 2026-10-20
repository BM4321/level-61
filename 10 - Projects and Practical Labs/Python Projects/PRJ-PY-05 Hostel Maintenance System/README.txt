hostel-maintenance 1.0.0
========================

Maintenance request tracking for student hostels. A teaching project for the
vault note "PRJ-PY-05 Hostel Maintenance System": standard library only
(sqlite3, hashlib.scrypt, argparse, logging).

NOT FOR PRODUCTION AS-IS. It has no web interface, no MFA, no per-IP rate
limiting, no email delivery for reset tokens and no security review. See the
project note's "Security notes and known limitations" before reusing any part.

Install (in a virtual environment)
----------------------------------
    python -m venv .venv
    . .venv/bin/activate            (Windows: .venv\Scripts\activate)
    python -m pip install -e ".[dev]"

Without installing, run from this folder with:  PYTHONPATH=src python -m hostel ...

Usage
-----
Passwords are prompted for (getpass); when stdin is not a terminal they are
read one per line, the --as user's password first.

    hostel --db hostel.db init
    hostel register WARDEN01 "Asha Warden" warden              (first user only)
    hostel --as WARDEN01 add-room A-101 A 2
    hostel --as WARDEN01 register STU/21/0001 "Baraka Resident" resident --room A-101
    hostel --as WARDEN01 register TECH01 "Daudi Technician" technician
    hostel --as STU/21/0001 submit A-101 electrical "Socket sparks near the desk"
    hostel --as WARDEN01 move 1 assigned --assignee TECH01
    hostel --as TECH01 move 1 in_progress
    hostel --as TECH01 move 1 resolved --note "Replaced the socket"
    hostel --as WARDEN01 move 1 closed
    hostel --as STU/21/0001 history 1
    hostel --as WARDEN01 report

Architecture (layers; arrows = "depends on")
--------------------------------------------
    cli  ->  services  ->  repository (interface)  <-  SqliteRepository / InMemoryRepository
               |                                         
               +-> models (domain rules, validation)     reports (pure functions)
               +-> security (scrypt hashing, policy, reset tokens)

Testing
-------
    python -m pytest        (42 tests; each repository test runs on both implementations)
    python -m mypy src/hostel
