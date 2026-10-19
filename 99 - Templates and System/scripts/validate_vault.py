#!/usr/bin/env python3
"""Validate the Semester 6 Obsidian vault.

Checks performed:
  1. Every [[wikilink]] / ![[embed]] resolves to exactly one note (by basename).
  2. No two Markdown files share a basename (Obsidian link ambiguity).
  3. Notes have YAML frontmatter; lessons carry the required fields.
  4. topic_id values are unique.
  5. No near-empty notes (fewer than MIN_WORDS words of body text).
  6. Every ```python fence parses with ast (unless marked as a demo of invalid code).
  7. Every ```mermaid fence starts with a known diagram keyword.
  8. Placeholder markers (TODO, TBD, lorem ipsum) are reported.

Usage:
    python "99 - Templates and System/scripts/validate_vault.py" [--strict]

Exit status is 1 when any error is found (warnings never fail the run unless --strict).
Requires Python 3.10+ and only the standard library.
"""
from __future__ import annotations

import ast
import re
import sys
from collections import defaultdict
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {".git", ".obsidian", "__pycache__", ".pytest_cache", "node_modules", ".venv"}
MIN_WORDS = 60
LESSON_FIELDS = ["title", "module", "module_code", "topic_id", "type", "difficulty",
                 "syllabus_status", "status", "mastery", "tags"]
MERMAID_KINDS = ("graph", "flowchart", "sequenceDiagram", "classDiagram", "stateDiagram",
                 "stateDiagram-v2", "erDiagram", "gantt", "pie", "mindmap", "timeline",
                 "journey", "quadrantChart", "gitGraph", "block-beta", "xychart-beta")
# A python fence whose first line contains one of these markers is not parsed.
NO_PARSE_MARKERS = ("# syntax-error-demo", "# not-runnable", "# python2")

WIKILINK = re.compile(r"!?\[\[([^\]\|#]+)(?:#[^\]\|]*)?(?:\|[^\]]*)?\]\]")
FENCE = re.compile(r"^```([\w+-]*)\s*\n(.*?)^```\s*$", re.S | re.M)
INLINE_CODE = re.compile(r"`[^`\n]*`")
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|lorem ipsum)\b", re.I)


def md_files() -> list[Path]:
    out = []
    for p in VAULT.rglob("*.md"):
        if any(part in SKIP_DIRS for part in p.relative_to(VAULT).parts):
            continue
        out.append(p)
    return sorted(out)


def split_frontmatter(text: str) -> tuple[dict[str, str] | None, str]:
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---", 4)
    if end == -1:
        return None, text
    raw = text[4:end]
    fields: dict[str, str] = {}
    for line in raw.splitlines():
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fields[m.group(1)] = m.group(2).strip()
    return fields, text[end + 4:]


def strip_code(text: str) -> str:
    text = FENCE.sub("", text)
    return INLINE_CODE.sub("", text)


def main() -> int:
    strict = "--strict" in sys.argv
    errors: list[str] = []
    warnings: list[str] = []
    files = md_files()
    # Attachments (non-md) may also be link targets.
    all_targets: dict[str, list[Path]] = defaultdict(list)
    for p in VAULT.rglob("*"):
        if p.is_file() and not any(part in SKIP_DIRS for part in p.relative_to(VAULT).parts):
            key = p.stem if p.suffix == ".md" else p.name
            all_targets[key.lower()].append(p)

    names: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        names[p.stem.lower()].append(p)
    for name, paths in names.items():
        if len(paths) > 1:
            errors.append(f"DUPLICATE NOTE NAME '{name}': " + ", ".join(str(x.relative_to(VAULT)) for x in paths))

    topic_ids: dict[str, list[Path]] = defaultdict(list)
    link_count = 0
    py_blocks = mermaid_blocks = 0
    for p in files:
        rel = p.relative_to(VAULT)
        text = p.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        if fm is None:
            errors.append(f"MISSING FRONTMATTER: {rel}")
            fm = {}
        if fm.get("type", "").strip('"') == "lesson" and "Templates" not in rel.parts:
            for f in LESSON_FIELDS:
                if f not in fm:
                    errors.append(f"LESSON MISSING FIELD '{f}': {rel}")
        tid = fm.get("topic_id", "").strip('"')
        if tid:
            topic_ids[tid].append(p)

        words = len(re.findall(r"\w+", strip_code(body)))
        if words < MIN_WORDS and fm.get("type", "").strip('"') not in ("template",):
            warnings.append(f"SHORT NOTE ({words} words): {rel}")

        prose = strip_code(body)
        for m in PLACEHOLDER.finditer(prose):
            warnings.append(f"PLACEHOLDER '{m.group(0)}': {rel}")

        is_template = "Templates" in rel.parts and rel.parts[0].startswith("99")
        for m in WIKILINK.finditer(strip_code(text)):
            if is_template:
                continue  # templates contain deliberate placeholder links
            link_count += 1
            target = m.group(1).strip().rstrip("\\").strip()
            key = Path(target).stem.lower() if target.lower().endswith(".md") else target.lower()
            key = key.split("/")[-1]
            hits = all_targets.get(key, [])
            if not hits:
                errors.append(f"BROKEN LINK [[{target}]] in {rel}")
            elif len(hits) > 1:
                errors.append(f"AMBIGUOUS LINK [[{target}]] in {rel}")

        for fm_ in FENCE.finditer(body):
            lang, code = fm_.group(1).lower(), fm_.group(2)
            first = code.lstrip().splitlines()[0] if code.strip() else ""
            if lang in ("python", "py"):
                py_blocks += 1
                if any(mark in first.lower() for mark in NO_PARSE_MARKERS):
                    continue
                if first.startswith(">>>"):
                    continue  # interactive session transcript
                try:
                    ast.parse(code)
                except SyntaxError as exc:
                    errors.append(f"PYTHON SYNTAX ERROR {rel} (block line {exc.lineno}): {exc.msg}")
            elif lang == "mermaid":
                mermaid_blocks += 1
                head = first.strip().split()[0] if first.strip() else ""
                if head not in MERMAID_KINDS:
                    errors.append(f"MERMAID UNKNOWN DIAGRAM TYPE '{head}' in {rel}")
                if not code.strip() or len(code.strip().splitlines()) < 2:
                    errors.append(f"MERMAID EMPTY DIAGRAM in {rel}")

    for tid, paths in topic_ids.items():
        if len(paths) > 1:
            errors.append(f"DUPLICATE topic_id {tid}: " + ", ".join(str(x.relative_to(VAULT)) for x in paths))

    print(f"Vault: {VAULT}")
    print(f"Markdown notes: {len(files)} | wikilinks: {link_count} | python fences: {py_blocks} | mermaid fences: {mermaid_blocks}")
    print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    if errors or (strict and warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
