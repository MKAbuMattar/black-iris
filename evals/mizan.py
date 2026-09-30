#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""mizan.py: weigh the routing. Did each case open the mode it should?

A mizan is a scale. This one needs no judge: it runs each case through
`claude -p` with only this repo's plugin loaded, reads the stream, and
records which `references/<mode>.md` the model opened before its first
written answer. Then it stops that session, so a case costs a routing
decision, not a whole task.

    python3 evals/mizan.py                  every case
    python3 evals/mizan.py --per-mode 1     one case per mode, a smoke run
    python3 evals/mizan.py --mode athar     one mode
    python3 evals/mizan.py --always-on      the router already in context
    python3 evals/mizan.py --model M --jobs 4 --timeout 180

Per case: hit (opened the expected reference), wrong (opened others, not
it), miss (loaded the skill, opened no reference), skip (never loaded the
skill, so the description did not route it), false fire (a shape, build, or none case that
opened one), and extra (a hit that also opened others). Results go to
evals/out/mizan/<stamp>.jsonl; the table prints per mode.

Isolation: a neutral temp directory, --setting-sources "" so no user
plugin or always-on flag leaks in, Skill and the read tools allowed, and
Bash, Write, Edit, and Agent denied so no case changes files or spawns a
council. Standard library only.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILE = {"name": "naming"}          # modes whose reference is not <mode>.md
QUIET = {"shape", "build", "none"}  # rules are inline, nothing to open
REF = re.compile(r"black-iris/references/([a-z-]+)\.md$")


def cases():
    rows = [json.loads(l) for l in (ROOT / "evals/cases.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    return rows


def always_on():
    """What hooks/reinject.sh prints, minus the memory index: the router with its root."""
    body = (ROOT / "skills/black-iris/SKILL.md").read_text(encoding="utf-8").split("---\n", 2)[2]
    return (f"# black-iris skill root: {ROOT / 'skills/black-iris'}\n"
            "Read a `references/` file named in the routing table when that mode\n"
            "fires, resolving it against that root. Do not read them all up front.\n\n" + body)


def run(case, model, timeout, hook=False):
    cmd = ["claude", "-p", "--plugin-dir", str(ROOT), "--setting-sources", "",
           "--disallowed-tools", "Bash,Write,Edit,NotebookEdit,Agent",
           # headless -p denies any tool that would prompt, and the Skill tool prompts:
           # without this every natural-language case reads as a miss
           "--allowedTools", "Skill,Read,Glob,Grep",
           "--output-format", "stream-json", "--verbose"]
    if model:
        cmd += ["--model", model]
    if hook:   # ponytail: system prompt, not SessionStart context; close, not identical
        cmd += ["--append-system-prompt", always_on()]
    opened, err, used, loaded = [], "", "", False
    with tempfile.TemporaryDirectory() as work:
        p = subprocess.Popen(cmd, cwd=work, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, text=True)
        p.stdin.write(case["prompt"])
        p.stdin.close()
        start = time.time()
        try:
            for line in p.stdout:
                if time.time() - start > timeout:
                    err = "timeout"
                    break
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if r.get("type") == "system" and r.get("subtype") == "init":
                    used = r.get("model", "")
                if r.get("type") != "assistant":
                    continue
                blocks = r["message"].get("content") or []
                for b in blocks:
                    if b.get("type") == "tool_use" and b.get("name") == "Skill" \
                            and str(b.get("input", {}).get("skill", "")).startswith("black-iris"):
                        loaded = True
                    if b.get("type") == "tool_use" and b.get("name") == "Read":
                        m = REF.search(b.get("input", {}).get("file_path", ""))
                        if m and m.group(1) not in opened:
                            opened.append(m.group(1))
                if any(b.get("type") == "text" and b.get("text", "").strip() for b in blocks):
                    break   # the first written answer: routing is decided
        finally:
            p.kill()
            p.wait()
    return opened, err, used, loaded


def score(case, opened, loaded=False):
    mode = case["mode"]
    if mode in QUIET:
        return "false fire" if opened else "hit"
    want = FILE.get(mode, mode)
    if want in opened:
        return "extra" if len(opened) > 1 else "hit"
    if opened:
        return "wrong"
    return "miss" if loaded else "skip"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode")
    ap.add_argument("--per-mode", type=int)
    ap.add_argument("--model", default="")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--always-on", action="store_true", help="inject the router as the always-on hook does")
    a = ap.parse_args()
    rows = [r for r in cases() if not a.mode or r["mode"] == a.mode]
    if a.per_mode:
        seen = {}
        rows = [r for r in rows if seen.setdefault(r["mode"], []).append(r) or len(seen[r["mode"]]) <= a.per_mode]
    if not rows:
        sys.exit("no cases match")
    out = ROOT / "evals/out/mizan"
    out.mkdir(parents=True, exist_ok=True)
    log = out / f"{time.strftime('%Y%m%d-%H%M%S')}.jsonl"
    print(f"mizan: {len(rows)} cases, {a.jobs} at a time, model {a.model or 'CLI default'}"
          + (", always-on router injected" if a.always_on else ""))

    def one(r):
        opened, err, used, loaded = run(r, a.model, a.timeout, a.always_on)
        res = {"id": r["id"], "mode": r["mode"], "model": used, "opened": opened,
               "loaded": loaded, "score": score(r, opened, loaded), "error": err}
        print(f"  {r['id']:<12} {res['score']:<10} {' '.join(opened) or '-'}{'  ' + err if err else ''}", flush=True)
        return res

    with ThreadPoolExecutor(a.jobs) as pool:
        results = list(pool.map(one, rows))
    log.write_text("".join(json.dumps(r) + "\n" for r in results), encoding="utf-8")

    kinds = ["hit", "extra", "wrong", "miss", "skip", "false fire"]
    print(f"\n{'mode':<10} {'n':>3} " + " ".join(f"{k:>10}" for k in kinds))
    for mode in sorted({r["mode"] for r in results}):
        rs = [r for r in results if r["mode"] == mode]
        print(f"{mode:<10} {len(rs):>3} " + " ".join(f"{sum(r['score'] == k for r in rs):>10}" for k in kinds))
    good = sum(r["score"] in ("hit", "extra") for r in results)
    print(f"\nrouted right: {good} of {len(results)}. Log: {log}")
    missing = sorted({p.stem for p in (ROOT / "skills/black-iris/references").glob("*.md")} - {"evals"}
                     - {FILE.get(m, m) for m in {r["mode"] for r in cases()}})
    if missing:
        print("no cases yet, so not weighed: " + ", ".join(missing))


if __name__ == "__main__":
    main()
