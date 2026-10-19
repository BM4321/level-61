"""PY-14: files, CSV and JSON in a temporary folder. Run: python examples/py14_files.py"""
import csv
import json
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as d:
    folder = Path(d)
    csv_path = folder / "marks.csv"
    rows = [{"id": "S1", "name": "Amina", "mark": 78}, {"id": "S2", "name": "Baraka, J.", "mark": 64}]
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "name", "mark"])
        w.writeheader()
        w.writerows(rows)
    print(csv_path.read_text(encoding="utf-8"))
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            print(row, type(row["mark"]).__name__)

    data = {"student": "Amina", "marks": [78, 81], "active": True, "mentor": None, 1: "int key"}
    text = json.dumps(data, indent=2)
    print(text)
    print("round trip equal?", json.loads(text) == data, "(int key became a string)")
