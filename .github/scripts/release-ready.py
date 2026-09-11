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
import json
import re
import subprocess
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

# Claude Code loads hooks/hooks.json automatically. A plugin manifest that also
# declares it is a duplicate, and the whole plugin fails to load with no hook,
# no always-on flag and no skill. That shipped in every release from 1.0.0 to
# 1.6.0 and was only caught by installing the plugin on a clean config.
plugin_manifest = ROOT / ".claude-plugin/plugin.json"
if plugin_manifest.exists():
    try:
        pm = json.loads(plugin_manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        hit(f".claude-plugin/plugin.json is not valid JSON: {e}")
    else:
        declared = pm.get("hooks")
        if declared in ("./hooks/hooks.json", "hooks/hooks.json"):
            hit(".claude-plugin/plugin.json declares the standard hooks/hooks.json; "
                "Claude Code loads it automatically and the duplicate stops the plugin loading")

# A tracked text file must not carry a carriage return in the committed blob.
# One got in when an editing script detected CRLF and then wrote CRLF into
# content that already had it, leaving \r\r\n. Git normalises CRLF but not that,
# so 75 stray bytes reached main and the next edit could not match its own text.
text_exts = {".md", ".py", ".sh", ".ps1", ".json", ".yml", ".yaml", ".toml", ".txt"}
tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files"],
                         capture_output=True, text=True).stdout.split()
for rel in tracked:
    if Path(rel).suffix not in text_exts:
        continue
    blob = subprocess.run(["git", "-C", str(ROOT), "show", f"HEAD:{rel}"],
                          capture_output=True).stdout
    if b"\r" in blob:
        hit(f"{rel}: {blob.count(bytes([13]))} carriage returns in the committed blob")

changelog = ROOT / ".github/CHANGELOG.md"
if not changelog.exists():
    hit("no .github/CHANGELOG.md")
elif not re.search(rf"^## \[?{re.escape(ver)}\]?( |\r?$)", changelog.read_text(encoding="utf-8"), re.M):
    hit(f"no '## {ver}' section in .github/CHANGELOG.md")

if not fails:
    print(f"clean: {len(found)} manifests at {ver}, changelog section present")
sys.exit(1 if fails else 0)
