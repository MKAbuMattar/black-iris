#!/usr/bin/env python3
"""One runnable check for skills/black-iris/dabke/dabke.py and its hook
wrapper, on a scratch home. Exit 0 on pass.
python3 tests/test_dabke.py"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
home = Path(tempfile.mkdtemp())
proj = home / "proj"; proj.mkdir()
env = dict(os.environ, HOME=str(home), CLAUDE_PROJECT_DIR=str(proj), CLAUDE_PLUGIN_ROOT=str(root))
store = home / ".BLACK_IRIS_AGENTS/projects" / str(proj).replace("/", "-")
ledger, log = store / "GATES.md", store / "dabke/s1.md"
cli = [sys.executable, str(root / "skills/black-iris/dabke/dabke.py")]

def run(*a):
    return subprocess.run(cli + list(a), capture_output=True, text=True, env=env)

def stop(active=True, session="s1"):
    p = subprocess.run(["sh", str(root / "hooks/dabke-stop.sh")], capture_output=True, text=True, env=env,
                       input=json.dumps({"session_id": session, "cwd": str(proj), "stop_hook_active": active}))
    return p.returncode, p.stderr

# off by default: no loop, no block
assert stop() == (0, "")

# start arms; the next stop binds and asks for a ledger first
assert "armed, 9 steps" in run("start", "fix the import bug", "--max", "9").stdout
rc, err = stop()
assert rc == 2 and "No gate ledger yet" in err and "step 1 of 9" in err and "fix the import bug" in err, err
assert "s1: step 1 of 9" in run("status").stdout

# with unmet gates it hands over the next step; stop_hook_active does not end it
ledger.write_text("- [ ] G1: imports\n  CHECK: x\n- [ ] G2: rejects\nABANDON: G2 no fixture\n")
rc, err = stop()
assert rc == 2 and "Unmet gates: G1." in err and "G2" not in err.split("Unmet gates:")[1].split(".")[0], err
assert "investigate first" in err and "lockfile" in err and str(log) in err

# a stop that changed nothing warns, a second releases
rc, err = stop()
assert rc == 2 and "Nothing changed" in err, err
assert stop() == (0, "") and not (store / "dabke/s1.json").exists()

# budget: the last step asks for the handoff report, the next stop releases
run("start", "again", "--max", "2")
log.write_text("a\n"); assert stop()[0] == 2
log.write_text("b\n"); rc, err = stop()
assert rc == 2 and "Step budget spent" in err and "HANDOFF REQUIRED" in err, err
log.write_text("c\n"); assert stop() == (0, "")

# every gate met or abandoned: released at once
run("start", "last")
ledger.write_text("- [x] G1: imports\n- [ ] G2: rejects\nABANDON: G2 no fixture\n")
assert stop() == (0, "")

# another chat in the project is untouched, stop ends them all, garbage is fail-open
ledger.write_text("- [ ] G3: open\n")
run("start", "other"); assert stop(session="s2")[0] == 2 and not (store / "dabke/s1.json").exists()
assert "Dabke stopped: 1" in run("stop").stdout and stop(session="s2") == (0, "")
p = subprocess.run(["sh", str(root / "hooks/dabke-stop.sh")], input="{nope", capture_output=True, text=True, env=env)
assert p.returncode == 0
print("dabke: pass")
