#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Prepare a release: bump every versioned manifest, stamp the changelog.

The mechanical half of cutting a release. It never writes changelog prose.
You write the `## Unreleased` bullets while the work happens, in the language
of someone deciding whether to upgrade; this only renames that heading to the
version and the date.

Every refusal is decided before the first byte is written, so a rejected run
leaves the tree exactly as it found it. Re-running with the same version is a
no-op, so rerunning the workflow is safe.

Run from anywhere:  python3 .github/scripts/prepare-release.py 1.2.0
Exit 0 on success, 1 on any refusal.
"""
import datetime
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from manifests import SEMVER, VERSION_LINE, repo_root, versioned  # noqa: E402


def die(msg):
    print(f"FAIL: {msg}")
    sys.exit(1)


def read_raw(path):
    """Read without newline translation, so a CRLF file stays CRLF on write."""
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


if len(sys.argv) != 2:
    die("usage: prepare-release.py <version>")
ver = sys.argv[1].lstrip("v")
if not re.match(SEMVER, ver):
    die(f"{ver!r} is not a semver such as 1.2.0 or 1.2.0-rc.1")

ROOT = repo_root()

# Decide everything first. Nothing below this block touches the disk.
found, bad = versioned(ROOT)
for rel, err in bad:
    die(f"{rel} is not valid JSON: {err}")
if not found:
    die("no manifest carries a version")

writes = []   # (path, new text)
report = []   # human-readable lines

for rel in sorted(found):
    p = ROOT / rel
    text = read_raw(p)
    new, n = re.subn(VERSION_LINE, lambda m: m.group("lead") + ver + m.group("tail"),
                     text, count=1, flags=re.M)
    if n != 1:
        die(f"{rel} carries a version but no version line matched")
    if json.loads(new).get("version") != ver:
        die(f"{rel} did not end up at {ver}; the version line is not the top-level key")
    if new == text:
        report.append(f"  {rel}: already {ver}")
    else:
        writes.append((p, new))
        report.append(f"  {rel}: {found[rel]} -> {ver}")

cl = ROOT / ".github/CHANGELOG.md"
if not cl.exists():
    die("no .github/CHANGELOG.md")
text = read_raw(cl)
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")

if re.search(rf"^## \[?{re.escape(ver)}\]?( |\r?$)", text, re.M):
    report.append(f"  .github/CHANGELOG.md: already has a {ver} section")
    new = text
else:
    new, n = re.subn(r"^## \[?Unreleased\]?[^\r\n]*", f"## {ver} - {today}",
                     text, count=1, flags=re.M | re.I)
    if n != 1:
        die(
            f"no '## Unreleased' heading and no '## {ver}' section in "
            ".github/CHANGELOG.md. Write the entries first; this script does "
            "not invent them."
        )
    report.append(f"  .github/CHANGELOG.md: Unreleased -> {ver} - {today}")

section = re.split(r"^## ", new, flags=re.M)[1]
if not section.split("\n", 1)[1].strip():
    die(f"the {ver} changelog section is empty. A release with no notes helps nobody.")
if new != text:
    writes.append((cl, new))

# Every refusal is behind us.
for p, content in writes:
    p.write_text(content, encoding="utf-8", newline="")

print("\n".join(report))
print(f"prepared {ver}, {len(writes)} files written")
