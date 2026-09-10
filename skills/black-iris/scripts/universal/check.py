#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""black-iris self-lint: the rules this skill teaches, applied to this skill.

Canonical implementation. linux/, mac/, and windows/ hold the same checks in
the shell native to each platform for machines without python3.

Run from anywhere:  python3 scripts/universal/check.py   (or: uv run ...)
Exit 0 on clean, 1 on any hit.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[2]
ROOT = SKILL.parents[1]
fails = []


def hit(msg):
    fails.append(msg)
    print(f"FAIL: {msg}")


def want(label, expected, actual):
    if expected != actual:
        hit(f"{label}: expected {expected}, found {actual}")


def count(pattern, text, flags=re.M):
    return len(re.findall(pattern, text, flags))


def section(text, start, end):
    m = re.search(rf"^{re.escape(start)}.*?(?=^{re.escape(end)})", text, re.S | re.M)
    return m.group(0) if m else ""


# Every byte ASCII: covers dashes and curly quotes (Cut list 1 and 9) and
# anything else that would slip past a code-point list.
text_files = sorted(p for ext in ("*.md", "*.py", "*.sh", "*.ps1", "*.json")
                    for base in (SKILL, ROOT / "hooks") for p in base.rglob(ext))
for f in text_files:
    for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if not line.isascii():
            hit(f"{f.relative_to(ROOT)}:{i}: non-ASCII byte (Cut list 1 and 9)")
        if re.match(r"^Co-[Aa]uthored-[Bb]y:", line):
            hit(f"{f.relative_to(ROOT)}:{i}: AI trailer (Cut list 10)")

skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
want("shape rules", 10, count(r"^\d+\. \*\*", section(skill, "## Shape", "## Build")))
want("build rules", 5, count(r"^\d+\. \*\*", section(skill, "## Build", "## Cut list")))
want("cut list items", 10, count(r"^\d+\. ", section(skill, "## Cut list", "Full catalog")))
ids = [int(n) for n in re.findall(r"^### (\d+)\. ", (SKILL / "references/deslop.md").read_text(encoding="utf-8"), re.M)]
if ids != sorted(set(ids)):
    hit("deslop pattern ids must be unique and ascending (stable ids, gaps allowed)")
ideate = (SKILL / "references/ideate.md").read_text(encoding="utf-8")
want("ideate frames", 15, count(r"^\| \*\*", section(ideate, "## Frames", "## Output")))

lines = skill.count("\n")
if lines > 200:
    hit(f"SKILL.md is {lines} lines, over the 200 budget")
m = re.search(r"^description: >\n(.*?)^license:", skill, re.S | re.M)
desc = " ".join(m.group(1).split()) if m else ""
if len(desc) > 1024:
    hit(f"description is {len(desc)} chars, over the 1024 cap")
if not desc:
    hit("description block not found")

named = set(re.findall(r"`references/([a-z-]+\.md)`", skill))
on_disk = {p.name for p in (SKILL / "references").glob("*.md")}
for f in sorted(named - on_disk):
    hit(f"SKILL.md points at missing references/{f}")
for f in sorted(on_disk - named):
    hit(f"references/{f} exists but SKILL.md never points at it")

hooks = ROOT / "hooks/hooks.json"
if hooks.exists():
    try:
        json.loads(hooks.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        hit(f"hooks.json is not valid JSON: {e}")
reinject = ROOT / "hooks/reinject.sh"
if reinject.exists() and sys.platform != "win32":
    if subprocess.run(["sh", "-n", str(reinject)]).returncode != 0:
        hit("reinject.sh has a syntax error")

if not fails:
    print("clean")
sys.exit(1 if fails else 0)
