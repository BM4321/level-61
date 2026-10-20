import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[1]
for sub in (HERE, ROOT / "05 - Information System Project Management/code", ROOT / "02 - Cyber Security/code",
            ROOT / "04 - Final Year Project I/code", ROOT / "07 - Software Design and Development/code",
            ROOT / "08 - Cross-Module Connections/code"):
    sys.path.insert(0, str(sub))
