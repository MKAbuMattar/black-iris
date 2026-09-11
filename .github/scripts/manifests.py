#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Which root manifests carry a version, and where the repo keeps them.

One rule, read by release-ready.py and prepare-release.py, so a manifest is
enrolled in the check and in the bump at the same moment: when it gains a
top-level string "version". Nothing here hardcodes a filename.
"""
import json
from pathlib import Path

SEARCH = (
    "*.json",
    ".claude-plugin/*.json",
    ".codex-plugin/*.json",
    ".agents/plugins/*.json",
)

VERSION_LINE = r'^(?P<lead>[ \t]*"version"[ \t]*:[ \t]*")(?P<ver>[^"]*)(?P<tail>")'
SEMVER = r"^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z.]+(\.[0-9A-Za-z.]+)*)?$"


def repo_root():
    return Path(__file__).resolve().parents[2]


def versioned(root=None):
    """Return ({relative path: version}, [(path, parse error)])."""
    root = root or repo_root()
    found, bad = {}, []
    for p in sorted({q for pat in SEARCH for q in root.glob(pat)}):
        rel = p.relative_to(root).as_posix()
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            bad.append((rel, str(e)))
            continue
        if isinstance(data, dict) and isinstance(data.get("version"), str):
            found[rel] = data["version"]
    return found, bad
