#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""Read cases.jsonl. One parser, so the runner and the judge agree.

  python3 evals/cases.py tsv      id, tools, prompt  (what run.sh consumes)
  python3 evals/cases.py stats    coverage per mode against the n>=8 floor
  python3 evals/cases.py judge <id>   the checks for one case, for the judge
"""
import json
import sys
from pathlib import Path

CASES = Path(__file__).resolve().parent / "cases.jsonl"
FLOOR = 8  # references/evals.md: 8 to 12 prompts per measured mode


def load():
    rows = []
    for i, line in enumerate(CASES.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"cases.jsonl:{i}: {e}")
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        dupes = sorted({i for i in ids if ids.count(i) > 1})
        sys.exit(f"duplicate case ids: {', '.join(dupes)}")
    for r in rows:
        for key in ("id", "mode", "kind", "tools", "prompt", "checks"):
            if not r.get(key):
                sys.exit(f"{r.get('id', '?')}: missing {key}")
        if not r["prompt"].isascii():
            sys.exit(f"{r['id']}: prompt is not ASCII")
        if "\t" in r["prompt"] or "\n" in r["prompt"]:
            sys.exit(f"{r['id']}: prompt has a tab or newline; the runner is line based")
    return rows


def main():
    rows = load()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "stats"
    if cmd == "tsv":
        for r in rows:
            print(f"{r['id']}\t{r['tools']}\t{r['prompt']}")
    elif cmd == "judge":
        wanted = sys.argv[2]
        for r in rows:
            if r["id"] == wanted:
                print("\n".join(f"- {c}" for c in r["checks"]))
                return
        sys.exit(f"no case {wanted}")
    else:
        modes = {}
        for r in rows:
            modes.setdefault(r["mode"], []).append(r)
        print(f"{len(rows)} cases")
        short = []
        for mode in sorted(modes):
            n = len(modes[mode])
            mark = "" if n >= FLOOR else f"  under the floor of {FLOOR}"
            if n < FLOOR:
                short.append(mode)
            print(f"  {mode:<10} {n}{mark}")
        if short:
            print("not measurable yet: " + ", ".join(short))


main()
