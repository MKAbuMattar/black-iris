#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""siq.py: the black-iris Siq handoff, carried through compaction.

Everything a session knows has to pass through compaction, the way everything
reaching Petra passes through the Siq. This script meters the context, asks
the model to write the handoff while its context is still whole, and prints
the handoff back after compaction.

    siq.py meter <transcript.jsonl>   fill, inferred window, threshold, cycle
    siq.py extract <transcript.jsonl> the fallback extract for the last slice
    siq.py hook stop                  Stop hook: stdin JSON from Claude Code
    siq.py hook start                 SessionStart hook: stdin JSON
    siq.py arm                        enable Siq for this chat
    siq.py on | off [--project]       global, or this project only
    siq.py prune                      keep the newest 20 handoffs per project

Handoffs live at ~/.BLACK_IRIS_AGENTS/projects/<slug>/handoffs/<session>.md.
Every hook path exits 0 except the one deliberate Stop block, which exits 2
with the reason on stderr, the channel the hooks reference documents for Stop.

Standard library only.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

CAP = 4096          # bytes re-injected after compaction; the lint checks this number
SHARE = 0.70        # of the inferred window, where the Stop hook asks for a handoff
KEEP = 20           # handoffs kept per project
SMALL, LARGE = 200_000, 1_000_000
MODEL_SECTIONS = ("Decisions", "Verified", "Corrections")


# ------------------------------------------------------------ store

def base():
    return Path.home() / ".BLACK_IRIS_AGENTS"


def project_root(cwd=None):
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return env
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd or None,
                             capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except OSError:
        pass
    return cwd or os.getcwd()


def store(cwd=None):
    return base() / "projects" / project_root(cwd).replace("/", "-")


def handoff_path(session, cwd=None):
    return store(cwd) / "handoffs" / f"{session}.md"


def enabled(session, cwd=None):
    s = store(cwd)
    return any(p.exists() for p in (s / "siq" / f"on-{session}", s / "siq-on", base() / "siq-on"))


# ------------------------------------------------------------ transcript

def rows(path):
    out = []
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        pass
    return out


def usage_of(r):
    u = (r.get("message") or {}).get("usage") or {}
    return int(u.get("input_tokens", 0)) + int(u.get("cache_read_input_tokens", 0)) + \
        int(u.get("cache_creation_input_tokens", 0))


def boundaries(rs):
    return [i for i, r in enumerate(rs) if r.get("subtype") == "compact_boundary"]


def model_of(r):
    m = (r.get("message") or {}).get("model") or ""
    return "" if m.startswith("<") else m   # "<synthetic>" is harness bookkeeping, not a model


def meter(rs):
    """Fill now, the inferred window, the threshold, and the compaction cycle.

    The window is inferred for the model running now, from that model's own
    history in this transcript, because a session can switch models and a
    200k model compacts long before a 1M one."""
    marks = boundaries(rs)
    current = next((model_of(r) for r in reversed(rs) if r.get("type") == "assistant" and model_of(r)), "")
    seen, autos, active = 0, [], ""
    for r in rs:
        if r.get("type") == "assistant" and model_of(r):
            active = model_of(r)
            if active == current:
                seen = max(seen, usage_of(r))
        elif r.get("subtype") == "compact_boundary" and active == current:
            md = r.get("compactMetadata") or {}
            seen = max(seen, int(md.get("preTokens", 0)))
            if md.get("trigger") == "auto":
                autos.append(int(md.get("preTokens", 0)))
    # ponytail: the window is not recorded, so it is inferred: a 1m tag, or this model past 200k
    # anywhere in the transcript, means 1M. A 1M session still under 200k reads as 200k and is asked
    # once early; add a model table if that early ask ever costs more than the turn it takes.
    window = LARGE if seen > SMALL or "1m" in current.lower() else SMALL
    threshold = int(SHARE * window)
    if autos:   # this model's observed auto trigger beats the guess
        threshold = min(threshold, int(0.85 * autos[-1]))
    last = next((usage_of(r) for r in reversed(rs) if r.get("type") == "assistant" and usage_of(r)), 0)
    return {"fill": last, "window": window, "threshold": threshold, "cycle": len(marks),
            "model": current, "percent": round(100 * last / window, 1)}


def text_of(content):
    if isinstance(content, str):
        return content
    return " ".join(b.get("text", "") for b in content or [] if isinstance(b, dict) and b.get("type") == "text")


def extract(rs, cap=CAP):
    """The fallback: what the last slice before compaction holds, when no handoff was written."""
    marks = boundaries(rs)
    end = marks[-1] if marks else len(rs)
    start = marks[-2] + 1 if len(marks) > 1 else 0
    part = rs[start:end]
    asks, files, results, cmds = [], [], {}, []
    for r in part:
        m = r.get("message") or {}
        c = m.get("content")
        if r.get("type") == "user":
            if (r.get("origin") or {}).get("kind") == "human":
                t = " ".join(text_of(c).split())
                if t and not t.startswith("<command-"):
                    asks.append(t[:180])
            if isinstance(c, list):
                for b in c:
                    if isinstance(b, dict) and b.get("type") == "tool_result":
                        results[b.get("tool_use_id")] = bool(b.get("is_error"))
        elif r.get("type") == "assistant" and isinstance(c, list):
            for b in c:
                if not (isinstance(b, dict) and b.get("type") == "tool_use"):
                    continue
                inp = b.get("input") or {}
                if b.get("name") in ("Edit", "Write", "NotebookEdit") and inp.get("file_path"):
                    files.append(inp["file_path"])
                elif b.get("name") == "Bash":
                    cmd = " ".join(str(inp.get("command", "")).split())
                    if re.search(r"\b(test|pytest|check|lint|build|make|npm run|cargo|go test)\b", cmd):
                        cmds.append((b.get("id"), cmd[:140]))
    lines = ["## Asks (extracted, the user's words)"] + [f"- {a}" for a in asks[-8:]]
    if files:
        lines += ["", "## Files changed (extracted)"] + [f"- {f}" for f in dict.fromkeys(files)][-15:]
    if cmds:
        lines += ["", "## Last checks (extracted)"]
        lines += [f"- {'FAILED' if results.get(i) else 'ok'}: `{c}`" for i, c in cmds[-6:]]
    return clip("\n".join(lines), cap)


def clip(text, cap, tail=""):
    data = text.encode("utf-8")
    if len(data) + len(tail.encode()) <= cap:
        return text + tail
    room = max(cap - len(tail.encode()) - 20, 0)
    cut = data[:room].decode("utf-8", "ignore")
    nl = cut.rfind("\n")
    if nl > len(cut) - 200:   # end on a line break only when one is close; never drop a long line whole
        cut = cut[:nl]
    return cut + "\n[clipped]" + tail


# ------------------------------------------------------------ the handoff file

def sections(text):
    out, name = {}, None
    for line in text.splitlines():
        m = re.match(r"^## (.+?)\s*$", line)
        if m:
            name = m.group(1).split(" (")[0]
            out[name] = []
        elif name:
            out[name].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def open_gates(cwd=None):
    ledger = store(cwd) / "GATES.md"
    if not ledger.exists():
        return "none: no GATES.md in the store"
    text = ledger.read_text(encoding="utf-8")
    gone = set(re.findall(r"ABANDON:\s*(\S+)", text))   # abandoned is a handoff, not unmet, as in gates-stop.sh
    unmet = [l.strip() for l in text.splitlines()
             if re.match(r"\s*- \[ \]", l) and re.sub(r"\s*- \[ \]\s*([^:\s]+).*", r"\1", l) not in gone]
    return "\n".join(unmet) or "none: every gate is met"


def write_skeleton(session, transcript, cycle, cwd=None):
    """Header and Open gates are the script's; the model's three sections are kept as they are."""
    p = handoff_path(session, cwd)
    p.parent.mkdir(parents=True, exist_ok=True)
    old = sections(p.read_text(encoding="utf-8")) if p.exists() else {}
    body = [f"# Siq handoff {session}", "",
            f"- project: {project_root(cwd)}", f"- transcript: {transcript}",
            f"- compaction cycle: {cycle}", f"- updated: {time.strftime('%Y-%m-%d %H:%M')}", ""]
    for name in MODEL_SECTIONS:
        body += [f"## {name}", old.get(name, "") or "(to write)", ""]
    body += ["## Open gates (script)", open_gates(cwd), ""]
    p.write_text("\n".join(body), encoding="utf-8")
    return p


def written(session, cwd=None):
    p = handoff_path(session, cwd)
    if not p.exists():
        return False
    s = sections(p.read_text(encoding="utf-8"))
    return any(s.get(n, "(to write)") not in ("", "(to write)") for n in MODEL_SECTIONS)


# ------------------------------------------------------------ hooks

def read_payload():
    if sys.stdin.isatty():
        return {}
    try:
        return json.loads(sys.stdin.read(1 << 20) or "{}")
    except (json.JSONDecodeError, OSError):
        return {}


def hook_stop(p):
    if p.get("stop_hook_active"):
        return 0
    session, cwd = p.get("session_id") or "nosession", p.get("cwd")
    s = store(cwd)
    arm = s / "siq-arm"
    if arm.exists():   # "for this chat": bind the arm to the session id only a hook can see
        (s / "siq").mkdir(parents=True, exist_ok=True)
        (s / "siq" / f"on-{session}").touch()
        arm.unlink()
    if not enabled(session, cwd):
        return 0
    rs = rows(p.get("transcript_path", ""))
    m = meter(rs)
    asked = s / "siq" / f"asked-{session}-c{m['cycle']}"
    if m["fill"] < m["threshold"] or asked.exists():
        return 0
    asked.parent.mkdir(parents=True, exist_ok=True)
    asked.touch()
    path = write_skeleton(session, p.get("transcript_path", ""), m["cycle"], cwd)
    print(f"Siq: context is at {m['percent']}% of an inferred {m['window'] // 1000}k window, "
          f"past the {round(100 * m['threshold'] / m['window'])}% handoff point. Before continuing, open "
          f"{path} and fill Decisions (chosen, rejected, why), Verified (command and result), and "
          f"Corrections (the user's words, verbatim), following references/siq.md: the Cut list, "
          f"names exactly as the code has them, and the whole file under {CAP} bytes. Merge what the "
          f"file already holds. Then carry on with the task.", file=sys.stderr)
    return 2


def hook_start(p):
    session, cwd, source = p.get("session_id") or "nosession", p.get("cwd"), p.get("source", "")
    if not enabled(session, cwd):
        return 0
    if source == "startup":
        hs = sorted((store(cwd) / "handoffs").glob("*.md"), key=lambda q: q.stat().st_mtime)
        if hs:
            print(f"Siq: the newest handoff for this project is {hs[-1]}. Read it if this work continues.")
        return 0
    if source not in ("compact", "resume"):
        return 0
    path = handoff_path(session, cwd)
    tail = f"\n\nfull file: {path}"
    if written(session, cwd):
        print("Siq handoff, written before compaction. Trust it over memory of this session.\n")
        print(clip(path.read_text(encoding="utf-8"), CAP, tail))
    else:
        rs = rows(p.get("transcript_path", ""))
        print("Siq: no handoff was written before this compaction. This is the extract from the transcript, "
              f"which is still on disk. Rewrite Decisions, Verified, and Corrections into {path} from it "
              "before the next task.\n")
        print(extract(rs, CAP - len(tail.encode())) + tail)
    return 0


# ------------------------------------------------------------ CLI

def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    cmd = a[0] if a else "help"
    try:
        if cmd == "meter":
            print(json.dumps(meter(rows(a[1]))))
        elif cmd == "extract":
            print(extract(rows(a[1])))
        elif cmd == "hook":
            fn = {"stop": hook_stop, "start": hook_start}.get(a[1] if len(a) > 1 else "")
            return fn(read_payload()) if fn else 0
        elif cmd == "arm":
            s = store()
            s.mkdir(parents=True, exist_ok=True)
            (s / "siq-arm").touch()
            print(f"Siq armed for this chat. The next Stop binds it to this session: {s / 'siq-arm'}")
        elif cmd in ("on", "off"):
            flag = (store() / "siq-on") if "--project" in a else (base() / "siq-on")
            flag.parent.mkdir(parents=True, exist_ok=True)
            flag.touch() if cmd == "on" else flag.unlink(missing_ok=True)
            print(f"Siq {cmd}: {flag}")
        elif cmd == "prune":
            hs = sorted((store() / "handoffs").glob("*.md"), key=lambda q: q.stat().st_mtime)
            for q in hs[:-KEEP]:
                q.unlink()
            print(f"kept {min(len(hs), KEEP)}, removed {max(len(hs) - KEEP, 0)}")
        else:
            print(__doc__)
    except Exception as e:   # a hook must never trap a session
        print(f"siq: {e}", file=sys.stderr)
        return 0 if cmd == "hook" else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
