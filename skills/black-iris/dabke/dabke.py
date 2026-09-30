#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""dabke.py: the black-iris Dabke loop, one step after another until done.

A dabke line keeps moving until the song ends. This script keeps a task
moving: while a loop is on for the chat, the Stop hook refuses the stop and
hands the model its next step, until the gate ledger has no unmet gate.

    dabke.py start "<brief>" [--max N]   arm a loop for this chat (default 40 steps)
    dabke.py status                      the loop state for this project
    dabke.py stop                        end every loop in this project now
    dabke.py hook stop                   Stop hook: stdin JSON from Claude Code

State lives at ~/.BLACK_IRIS_AGENTS/projects/<slug>/dabke/<session>.json and
the step log beside it as <session>.md. Done is GATES.md with every gate met
or abandoned; nothing else ends the loop early except a stall (two stops in a
row with no change to the ledger or the log) or the step budget.

The hook exits 2 with the next step on stderr, the channel the hooks
reference documents for Stop. It ignores stop_hook_active on purpose, since
continuing is the point; the stall and budget rules are what keep it from
trapping a session. Every error exits 0. Standard library only.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "siq"))
import siq  # noqa: E402  store paths and payload reading are shared, not copied

MAX = 40        # steps per loop unless --max says otherwise
STALLS = 2      # stops in a row with nothing changed before the loop lets go


def home(cwd=None):
    return siq.store(cwd) / "dabke"


def unmet(ledger):
    text = ledger.read_text(encoding="utf-8")
    gone = set(re.findall(r"^ABANDON:\s*([A-Za-z0-9_.-]+)", text, re.M))
    ids = re.findall(r"^- \[ \]\s*([A-Za-z0-9_.-]+):", text, re.M)
    return [i for i in ids if i not in gone]


def digest(*paths):
    h = hashlib.sha256()
    for p in paths:
        h.update(p.read_bytes() if p.exists() else b"-")
    return h.hexdigest()


def say(msg):
    print(msg, file=sys.stderr)
    return 2


def hook_stop(p):
    session, cwd = p.get("session_id") or "nosession", p.get("cwd")
    d = home(cwd)
    state_path, log = d / f"{session}.json", d / f"{session}.md"
    arm = siq.store(cwd) / "dabke-arm"
    if arm.exists():   # the session id is only visible to a hook, so start arms and the Stop binds
        d.mkdir(parents=True, exist_ok=True)
        st = json.loads(arm.read_text(encoding="utf-8"))
        st.update(step=0, stalls=0, digest="", final=False)
        state_path.write_text(json.dumps(st), encoding="utf-8")
        if not log.exists():
            log.write_text(f"# Dabke log {session}\n\nbrief: {st['brief']}\n\n", encoding="utf-8")
        arm.unlink()
    if not state_path.exists():
        return 0
    st = json.loads(state_path.read_text(encoding="utf-8"))
    ledger = siq.store(cwd) / "GATES.md"

    def release():
        state_path.unlink(missing_ok=True)
        return 0

    if st.get("final"):
        return release()
    if ledger.exists() and not unmet(ledger):
        return release()
    now = digest(ledger, log)
    st["stalls"] = st["stalls"] + 1 if now == st["digest"] else 0
    if st["stalls"] >= STALLS:
        return release()
    st.update(step=st["step"] + 1, digest=now)
    if st["step"] >= st["max"]:
        st["final"] = True
    state_path.write_text(json.dumps(st), encoding="utf-8")

    head = f"Dabke step {st['step']} of {st['max']}. Brief: {st['brief']}\n"
    if st["final"]:
        return say(head + f"Step budget spent. Stop working. Rerun every gate in {ledger}, then report "
                   "HANDOFF REQUIRED in line one with the unmet ids and what each needs, per "
                   "references/gates.md. The next stop ends the loop.")
    if not ledger.exists():
        return say(head + f"No gate ledger yet. Write {ledger} first, per references/gates.md: one "
                   "observable outcome per gate with CHECK: and EXPECT:. The loop ends when every gate "
                   "is met or abandoned.")
    stall = ("Nothing changed in the ledger or the log since the last step. One more stop without a "
             "change ends the loop, so either make progress, add ABANDON: <id> <reason>, or ask the "
             "user the one blocking question.\n") if st["stalls"] else ""
    return say(head + stall + f"Unmet gates: {' '.join(unmet(ledger))}. Ledger: {ledger}. Log: {log}.\n"
               "Take the next unmet gate. Rate confidence before acting, per references/dabke.md. High "
               "needs all four: you read the failure itself, you read the current file you will change, "
               "every outside fact is checked against the installed version, and you can name the check "
               "that proves it. Anything less: investigate first, in this order: the failing log, the "
               "actual file, the lockfile, the upstream source at that version, its release notes, every "
               "use of the name. Then act, run the gate's CHECK:, and append one line to the log: step, "
               "gate, confidence, what you read, what you changed, check result. Do not report done.")


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    cmd = a[0] if a else "help"
    try:
        if cmd == "hook":
            return hook_stop(siq.read_payload()) if a[1:2] == ["stop"] else 0
        if cmd == "start":
            words = [w for w in a[1:] if not w.startswith("--")]
            n = int(a[a.index("--max") + 1]) if "--max" in a else MAX
            if "--max" in a:
                words.remove(a[a.index("--max") + 1])
            brief = " ".join(words).strip()
            if not brief:
                print('usage: dabke.py start "<brief>" [--max N]')
                return 1
            s = siq.store()
            s.mkdir(parents=True, exist_ok=True)
            (s / "dabke-arm").write_text(json.dumps({"brief": brief, "max": max(n, 1)}), encoding="utf-8")
            print(f"Dabke armed, {max(n, 1)} steps. The next stop binds it to this chat. Ledger: {s / 'GATES.md'}")
        elif cmd == "status":
            s = siq.store()
            for q in sorted(home().glob("*.json")):
                st = json.loads(q.read_text(encoding="utf-8"))
                print(f"{q.stem}: step {st['step']} of {st['max']}, stalls {st['stalls']}: {st['brief']}")
            if (s / "dabke-arm").exists():
                print("armed, not yet bound")
        elif cmd == "stop":
            n = 0
            for q in list(home().glob("*.json")) + [siq.store() / "dabke-arm"]:
                if q.exists():
                    q.unlink()
                    n += 1
            print(f"Dabke stopped: {n} loop(s) ended. Logs are kept in {home()}")
        else:
            print(__doc__)
    except Exception as e:   # a hook must never trap a session
        print(f"dabke: {e}", file=sys.stderr)
        return 0 if cmd == "hook" else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
