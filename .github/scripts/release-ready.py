#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Release readiness, checked on every push and pull request.

Three assertions:

1. Every root manifest that carries a top-level "version" carries the same one.
2. `.github/CHANGELOG.md` has a section for that version.
3. With a version argument, the manifests carry exactly that version. The
   release workflow passes the tag, so a tag can never publish a tree whose
   manifests say something else.

The manifest list is discovered by `manifests.py`, never hardcoded, so adding
a manifest with a version enrolls it here and in the bump at the same time.

Run from anywhere:  python3 .github/scripts/release-ready.py [version]
Exit 0 on clean, 1 on any hit.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifests import repo_root, versioned  # noqa: E402

ROOT = repo_root()
fails = []


def hit(msg):
    fails.append(msg)
    print(f"FAIL: {msg}")


expected = sys.argv[1].lstrip("v") if len(sys.argv) > 1 else None

found, bad = versioned(ROOT)
for rel, err in bad:
    hit(f"{rel} is not valid JSON: {err}")
if not found:
    hit("no manifest carries a version")
    sys.exit(1)

for rel, v in sorted(found.items()):
    print(f"  {rel}: {v}")

distinct = sorted(set(found.values()))
if len(distinct) > 1:
    hit("manifests disagree: " + ", ".join(distinct))
ver = found.get("package.json", distinct[0])

if expected and expected != ver:
    hit(f"manifests say {ver}, the release asks for {expected}")
    ver = expected

changelog = ROOT / ".github/CHANGELOG.md"
if not changelog.exists():
    hit("no .github/CHANGELOG.md")
elif not re.search(rf"^## \[?{re.escape(ver)}\]?( |\r?$)", changelog.read_text(encoding="utf-8"), re.M):
    hit(f"no '## {ver}' section in .github/CHANGELOG.md")

if not fails:
    print(f"clean: {len(found)} manifests at {ver}, changelog section present")
sys.exit(1 if fails else 0)
