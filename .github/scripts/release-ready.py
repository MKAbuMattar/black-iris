#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Release readiness, checked on every push and pull request.

Three assertions:

1. Every root manifest that carries a top-level "version" carries the same one.
2. `.github/CHANGELOG.md` has a section for that version.
3. `.github/workflows/release.yml` validates every one of those manifests
   against the tag. A manifest that carries a version but is missing from the
   release workflow's list would ship stale, because the tag gate would never
   look at it.

The manifest list is discovered, never hardcoded here, so adding a manifest
with a version enrolls it in all three assertions automatically.

Run from anywhere:  python3 .github/scripts/release-ready.py
Exit 0 on clean, 1 on any hit.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
fails = []


def hit(msg):
    fails.append(msg)
    print(f"FAIL: {msg}")


# Every manifest the repo keeps at the root or in a plugin directory.
candidates = sorted(
    set(ROOT.glob("*.json"))
    | set(ROOT.glob(".claude-plugin/*.json"))
    | set(ROOT.glob(".codex-plugin/*.json"))
    | set(ROOT.glob(".agents/plugins/*.json"))
)

versioned = {}
for p in candidates:
    rel = p.relative_to(ROOT).as_posix()
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        hit(f"{rel} is not valid JSON: {e}")
        continue
    if isinstance(data, dict) and isinstance(data.get("version"), str):
        versioned[rel] = data["version"]

if not versioned:
    hit("no manifest carries a version")
    sys.exit(1)

for name, v in sorted(versioned.items()):
    print(f"  {name}: {v}")

distinct = sorted(set(versioned.values()))
if len(distinct) > 1:
    hit("manifests disagree: " + ", ".join(distinct))
ver = versioned.get("package.json", distinct[0])

changelog = ROOT / ".github/CHANGELOG.md"
if not changelog.exists():
    hit("no .github/CHANGELOG.md")
elif not re.search(rf"^## \[?{re.escape(ver)}\]?( |$)", changelog.read_text(encoding="utf-8"), re.M):
    hit(f"no '## {ver}' section in .github/CHANGELOG.md")

workflow = ROOT / ".github/workflows/release.yml"
if not workflow.exists():
    hit("no .github/workflows/release.yml")
else:
    m = re.search(r"for f in ([^\n;]+?); do", workflow.read_text(encoding="utf-8"))
    if not m:
        hit("could not find the version file list in .github/workflows/release.yml")
    else:
        listed = set(m.group(1).split())
        for name in sorted(versioned):
            if name not in listed:
                hit(f"{name} carries a version but release.yml never checks it against the tag")
        for name in sorted(listed - set(versioned)):
            hit(f"release.yml checks {name}, which carries no version")

if not fails:
    print(f"clean: {len(versioned)} manifests at {ver}, changelog section present")
sys.exit(1 if fails else 0)
