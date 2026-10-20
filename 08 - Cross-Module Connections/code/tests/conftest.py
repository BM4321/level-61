import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for sub in ("08 - Cross-Module Connections/code", "05 - Information System Project Management/code",
            "04 - Final Year Project I/code", "02 - Cyber Security/code",
            "07 - Software Design and Development/code"):
    sys.path.insert(0, str(ROOT / sub))
