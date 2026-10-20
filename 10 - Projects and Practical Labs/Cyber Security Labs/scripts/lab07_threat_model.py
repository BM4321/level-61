"""LAB-CS-07: generate a STRIDE-per-element worksheet for a sample web application's data-flow diagram.

Run:  python lab07_threat_model.py            (prints the worksheet as Markdown)
This automates the bookkeeping only. The thinking (which threats are real, what the mitigations are)
is the lab's actual work.
"""

# STRIDE-per-element applicability, as commonly taught with Microsoft's threat-modeling approach.
APPLICABLE = {
    "external_entity": "SR",
    "process": "STRIDE",
    "data_store": "TRID",      # repudiation applies mainly to stores holding logs/audit data
    "data_flow": "TID",
}
NAMES = {"S": "Spoofing", "T": "Tampering", "R": "Repudiation", "I": "Information disclosure",
         "D": "Denial of service", "E": "Elevation of privilege"}

# Sample system: the hostel maintenance web app (fictional).
ZONES = {"Student": "internet", "Warden": "internet", "Web app": "dmz",
         "Request DB": "internal", "Photo store": "internal", "Email service": "third_party"}
ELEMENTS = [
    ("Student", "external_entity"), ("Warden", "external_entity"), ("Web app", "process"),
    ("Request DB", "data_store"), ("Photo store", "data_store"), ("Email service", "external_entity"),
]
FLOWS = [
    ("Student", "Web app", "login + new request (HTTPS)"),
    ("Warden", "Web app", "assign technician (HTTPS)"),
    ("Web app", "Request DB", "SQL queries"),
    ("Web app", "Photo store", "upload / fetch photos"),
    ("Web app", "Email service", "status notifications"),
    ("Web app", "Student", "request status pages"),
]


def worksheet() -> str:
    rows = ["| ID | Element | Type | Threat category | Threat (fill in) | Mitigation (fill in) |",
            "|---|---|---|---|---|---|"]
    n = 0
    items = [(name, kind) for name, kind in ELEMENTS] + [(f"{a} → {b}: {label}", "data_flow") for a, b, label in FLOWS]
    for name, kind in items:
        for letter in APPLICABLE[kind]:
            n += 1
            rows.append(f"| T{n:02} | {name} | {kind.replace('_', ' ')} | {NAMES[letter]} | | |")
    crossing = [f"- {a} → {b} ({label}): {ZONES[a]} → {ZONES[b]}" for a, b, label in FLOWS if ZONES[a] != ZONES[b]]
    return ("## STRIDE worksheet\n\n" + "\n".join(rows) + f"\n\nTotal candidate threats: {n}\n\n"
            "## Flows crossing trust boundaries (analyse these first)\n\n" + "\n".join(crossing) + "\n")


if __name__ == "__main__":
    print(worksheet())
