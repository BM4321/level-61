"""LAB-CS-02: hashing and integrity verification with a SHA256SUMS manifest and an HMAC-signed manifest.

Run:      python lab02_integrity.py [workdir]        (default: ./lab02_workspace)
Cleanup:  python lab02_integrity.py --cleanup [workdir]
Only files inside the workdir that this script creates are touched.
"""
import hashlib
import hmac
import shutil
import sys
from pathlib import Path

FILES = {
    "results_2026.csv": "reg_no,course,grade\nDEMO/001,CST06102,A\nDEMO/002,CST06102,B+\n",
    "policy.txt": "All grade changes require approval by the examinations officer.\n",
    "installer_readme.txt": "Version 1.4.2 of the demo tool.\n",
}
DEMO_KEY = b"lab02-demo-key-not-a-real-secret"


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(65536), b""):
            h.update(block)
    return h.hexdigest()


def write_manifest(workdir: Path) -> str:
    lines = [f"{sha256_file(workdir / name)}  {name}" for name in sorted(FILES)]
    text = "\n".join(lines) + "\n"
    (workdir / "SHA256SUMS").write_text(text, encoding="utf-8")
    return text


def verify_manifest(workdir: Path) -> list[str]:
    report = []
    for line in (workdir / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        path = workdir / name
        if not path.exists():
            report.append(f"{name}: MISSING")
        else:
            report.append(f"{name}: {'OK' if hmac.compare_digest(sha256_file(path), digest) else 'FAILED'}")
    return report


def sign(text: str) -> str:
    return hmac.new(DEMO_KEY, text.encode(), hashlib.sha256).hexdigest()


def main(workdir: Path) -> None:
    workdir.mkdir(exist_ok=True)
    for name, content in FILES.items():
        (workdir / name).write_text(content, encoding="utf-8")

    print("== Step 1: create manifest ==")
    manifest = write_manifest(workdir)
    print(manifest, end="")
    tag = sign(manifest)
    print("HMAC-SHA256 tag of manifest:", tag)

    print("\n== Step 2: verify untouched files ==")
    print("\n".join(verify_manifest(workdir)))

    print("\n== Step 3: tamper with one grade (B+ -> A) and verify again ==")
    p = workdir / "results_2026.csv"
    p.write_text(p.read_text(encoding="utf-8").replace("B+", "A"), encoding="utf-8")
    print("\n".join(verify_manifest(workdir)))

    print("\n== Step 4: attacker also rewrites SHA256SUMS ==")
    forged = write_manifest(workdir)
    print("plain manifest check now says:", verify_manifest(workdir))
    print("HMAC check of forged manifest:", "VALID" if hmac.compare_digest(sign(forged), tag) else "INVALID (tampering detected)")

    print("\n== Step 5: avalanche effect ==")
    for s in (b"grade=B+", b"grade=A"):
        print(f"{s!r:12} {hashlib.sha256(s).hexdigest()}")


def cleanup(workdir: Path) -> None:
    if workdir.exists() and (workdir / "SHA256SUMS").exists():
        shutil.rmtree(workdir)
        print("removed", workdir)
    else:
        print("nothing to clean (or not a lab02 workspace):", workdir)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "--cleanup":
        cleanup(Path(args[1] if len(args) > 1 else "lab02_workspace"))
    else:
        main(Path(args[0] if args else "lab02_workspace"))
