"""LAB-CS-04: audit Unix file permissions in a practice directory, fix them, and re-audit.

Run:      python lab04_permissions.py [workdir]     (default: ./lab04_workspace)
Audit an existing directory you OWN (read-only):  python lab04_permissions.py --audit-only PATH
Cleanup:  python lab04_permissions.py --cleanup [workdir]
POSIX systems only (Linux, macOS, WSL).
"""
import os
import shutil
import stat
import sys
from pathlib import Path

SECRET_SUFFIXES = (".env", ".pem", ".key", "id_rsa", "id_ed25519", ".db")


def symbolic(mode: int) -> str:
    return stat.filemode(stat.S_IFREG | mode)[1:]


def findings_for(rel: str, mode: int, is_dir: bool) -> list[str]:
    out = []
    name = os.path.basename(rel)
    if mode & stat.S_IWOTH and not (is_dir and mode & stat.S_ISVTX):
        out.append("HIGH   world-writable")
    if mode & stat.S_ISUID:
        out.append("HIGH   setuid bit")
    if mode & stat.S_ISGID and not is_dir:
        out.append("MEDIUM setgid bit")
    if not is_dir and name.endswith(SECRET_SUFFIXES) and mode & 0o077:
        out.append("HIGH   secret readable/writable by group or others (want 600)")
    if not is_dir and mode & 0o111 and name.endswith((".txt", ".csv", ".env", ".md")):
        out.append("LOW    data file marked executable")
    return out


def audit(root: Path) -> list[str]:
    lines = []
    for dirpath, dirnames, filenames in os.walk(root):
        for name in sorted(dirnames + filenames):
            full = Path(dirpath) / name
            st = os.lstat(full)
            if stat.S_ISLNK(st.st_mode):
                continue
            mode = stat.S_IMODE(st.st_mode)
            rel = str(full.relative_to(root))
            for f in findings_for(rel, mode, stat.S_ISDIR(st.st_mode)):
                lines.append(f"{f:62} {symbolic(mode)} {oct(mode)[2:]:>4} {rel}")
    return sorted(lines)


SETUP = {  # path: (content or None for directory, mode)
    "app": (None, 0o755),
    "app/main.py": ("print('hostel app')\n", 0o644),
    "app/.env": ("DEMO_SETTING=not-a-real-secret\n", 0o644),
    "app/notes.txt": ("todo\n", 0o755),
    "uploads": (None, 0o777),
    "shared_tmp": (None, 0o1777),
    "backup.sh": ("#!/bin/sh\necho backup\n", 0o777),
    "tools": (None, 0o755),
    "tools/report_tool": ("#!/bin/sh\necho report\n", 0o4755),
}
FIXES = {"app/.env": 0o600, "app/notes.txt": 0o644, "uploads": 0o750, "backup.sh": 0o700, "tools/report_tool": 0o755}


def setup(root: Path) -> None:
    root.mkdir(exist_ok=True)
    for rel, (content, _mode) in SETUP.items():
        p = root / rel
        if content is None:
            p.mkdir(exist_ok=True)
        else:
            p.write_text(content, encoding="utf-8")
    for rel, (_content, mode) in SETUP.items():
        os.chmod(root / rel, mode)
    (root / ".lab04").write_text("marker\n", encoding="utf-8")
    os.chmod(root / ".lab04", 0o644)


def main(root: Path) -> None:
    setup(root)
    print("== Step 1: audit the deliberately misconfigured workspace ==")
    print("\n".join(audit(root)) or "no findings")
    print("\n== Step 2: apply least-privilege fixes ==")
    for rel, mode in FIXES.items():
        os.chmod(root / rel, mode)
        print(f"chmod {oct(mode)[2:]:>4} {rel}")
    print("\n== Step 3: re-audit ==")
    print("\n".join(audit(root)) or "no findings")


def cleanup(root: Path) -> None:
    if (root / ".lab04").exists():
        shutil.rmtree(root)
        print("removed", root)
    else:
        print("not a lab04 workspace; nothing removed:", root)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a and a[0] == "--cleanup":
        cleanup(Path(a[1] if len(a) > 1 else "lab04_workspace"))
    elif a and a[0] == "--audit-only":
        print("\n".join(audit(Path(a[1]))) or "no findings")
    else:
        main(Path(a[0] if a else "lab04_workspace"))
