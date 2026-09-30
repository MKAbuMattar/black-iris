#!/usr/bin/env python3
"""One runnable check for skills/black-iris/siq/siq.py and its hook wrappers,
on a scratch home and a synthetic transcript. Exit 0 on pass.
python3 tests/test_siq.py"""
import json, os, subprocess, sys, tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
home = Path(tempfile.mkdtemp())
proj = home / "proj"; proj.mkdir()
env = dict(os.environ, HOME=str(home), CLAUDE_PROJECT_DIR=str(proj), CLAUDE_PLUGIN_ROOT=str(root))
os.environ.update(HOME=str(home), CLAUDE_PROJECT_DIR=str(proj))
sys.path.insert(0, str(root / "skills/black-iris/siq"))
import siq  # noqa: E402

def asst(tokens, model="claude-opus-5-5"):
    return {"type": "assistant", "message": {"model": model, "usage": {"input_tokens": tokens},
            "content": [{"type": "tool_use", "id": f"t{tokens}", "name": "Bash",
                         "input": {"command": "python3 -m pytest -q"}}]}}

def human(text):
    return {"type": "user", "origin": {"kind": "human"}, "message": {"content": [{"type": "text", "text": text}]}}

def result(tid, err):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": tid, "is_error": err}]}}

def boundary(pre, trig="auto"):
    return {"type": "system", "subtype": "compact_boundary", "compactMetadata": {"trigger": trig, "preTokens": pre}}

tr = home / "t.jsonl"
def write(rows):
    tr.write_text("".join(json.dumps(r) + "\n" for r in rows))

def hook(event, payload):
    p = subprocess.run(["sh", str(root / f"hooks/siq-{event}.sh")], input=json.dumps(payload),
                       capture_output=True, text=True, env=env)
    return p.returncode, p.stdout, p.stderr

# meter: 200k by default, 1M once this model passes 200k, per model after a switch
assert siq.meter([asst(100_000)])["window"] == 200_000
assert siq.meter([asst(300_000)])["window"] == 1_000_000
switched = [asst(900_000, "big-model"), asst(150_000, "small-model")]
assert siq.meter(switched)["window"] == 200_000, "a model switch must not inherit the old window"
assert siq.meter([asst(170_000), boundary(167_000), asst(20_000)])["threshold"] == int(0.85 * 167_000) \
    or siq.meter([asst(170_000), boundary(167_000), asst(20_000)])["threshold"] == 140_000

pay = {"session_id": "s1", "transcript_path": str(tr), "cwd": str(proj)}

# off by default: nothing happens even past the threshold
write([human("add a login page"), asst(150_000), result("t150000", True)])
assert hook("stop", pay)[0] == 0

# arm for this chat, and the next Stop binds it and blocks once
subprocess.run([sys.executable, str(root / "skills/black-iris/siq/siq.py"), "arm"], env=env, check=True)
rc, out, err = hook("stop", pay)
assert rc == 2 and "Decisions" in err, (rc, err)
assert (siq.store() / "siq" / "on-s1").exists() and not (siq.store() / "siq-arm").exists()
assert hook("stop", pay)[0] == 0, "asked twice in one cycle"
assert hook("stop", dict(pay, stop_hook_active=True))[0] == 0
hand = siq.handoff_path("s1")
assert hand.exists() and "## Open gates (script)" in hand.read_text()

# under the threshold: no ask
assert hook("stop", dict(pay, session_id="s2"))[0] == 0

# after a compaction with nothing written: the fallback extract, under the cap
write([human("add a login page"), asst(150_000), result("t150000", True), boundary(167_000), asst(15_000)])
rc, out, _ = hook("start", dict(pay, source="compact"))
assert rc == 0 and "no handoff was written" in out and "FAILED" in out and "add a login page" in out
assert len(out.encode()) <= siq.CAP + 400, len(out.encode())

# once the model writes its sections, the file itself comes back, capped
text = hand.read_text().replace("## Decisions\n(to write)", "## Decisions\nKept JWT; rejected sessions: no sticky LB." + " x" * 5000)
hand.write_text(text)
rc, out, _ = hook("start", dict(pay, source="compact"))
assert "written before compaction" in out and "Kept JWT" in out and "[clipped]" in out
assert len(out.encode()) <= siq.CAP + 200

# a new cycle asks again
write([asst(150_000), boundary(167_000), asst(150_000)])
assert hook("stop", pay)[0] == 2
print("siq: pass")
