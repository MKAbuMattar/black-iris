#!/usr/bin/env python3
"""One runnable check for skills/black-iris/jerash/hippodrome.py: a full race
on a scratch home, 7 entrants so a bye happens, with a rejected answer so the
final runs. Exit 0 on pass.  python3 tests/test_hippodrome.py"""
import json, os, sys, tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
home = tempfile.mkdtemp()
os.environ["HOME"] = home
os.environ["CLAUDE_PROJECT_DIR"] = "/tmp/jerash-test-project"
sys.path.insert(0, str(root / "skills/black-iris/jerash"))
import hippodrome as H  # noqa: E402

# sizing
assert H.plan(100, 10, False) == {"field": 100, "rounds": 7, "heats": 99, "calls": 595, "waves": 70}
assert H.plan(16, 10, True)["calls"] == 16 + 5 * 15 + 1
assert H.rounds_for(7) == [3, 2, 1]

# the rubric table is the only source of weights
w = H.load_rubric()
assert [c for c, _ in w] == ["sound", "complete", "usable", "holds"] and sum(x for _, x in w) == 100

# refuse a rematch with no reason
try:
    H.init("t", 4, 1, rejected="old", reason=None)
    raise SystemExit("FAIL: a rejected answer without a reason was accepted")
except H.RaceError:
    pass

s = H.init("Name a function that removes duplicate emails.", 7, seed=11, rejected="func1", reason="says nothing")
cards = [tuple(e["card"].values()) for e in s["entrants"].values()]
assert len(set(cards)) == 7, "two entrants share a lane card"
assert Path(s["dir"]).is_relative_to(Path(home)), "race written outside the store"
assert H.next_step(s) == "entry"

def score(e, total):  # a verdict where e scores `total` on every criterion
    return {c: total for c, _ in w} | {"broken": False}

def play(state):
    """Write every missing output for the current phase, like the subagents would."""
    phase = H.next_step(state)
    if phase in H.PHASES:
        for j in H.write_briefs(state, phase):
            assert Path(j["brief"]).is_file()
            for o in j["outputs"]:
                if o.endswith("verdict.json"):
                    if j["kind"] == "final":
                        body = {"scores": {"X": score("X", 6), "Y": score("Y", 6)}, "standing": {}, "why": "tie"}
                    else:
                        h = j["heat"]  # the lower entrant id wins, unless it is broken
                        lo, hi = sorted((h["left"], h["right"]))
                        body = {"scores": {lo: score(lo, 8), hi: score(hi, 5)}, "standing": {}, "why": "lower id"}
                        if h["id"] == "r1h01":
                            body["scores"][lo]["broken"] = True   # broken loses despite the higher total
                    Path(o).write_text(json.dumps(body))
                else:
                    Path(o).write_text(f"output of {j['id']}\n")
    elif phase == "collect":
        assert H.collect(state) == []
    elif phase == "advance":
        H.advance(state)
    return phase

steps = []
for _ in range(60):
    p = play(s)
    steps.append(p)
    if p == "done":
        break
    s = json.loads((Path(s["dir"]) / "state.json").read_text())
assert steps[-1] == "done", steps
assert s["champion"] and sum(1 for e in s["entrants"].values() if e["out_round"] is None) == 1
first = s["rounds"]["1"]["heats"][0]
assert first["winner"] == max(first["left"], first["right"]), "a broken entry beat a sound one"
assert s["rounds"]["1"]["bye"], "odd field produced no bye"
assert s["final"]["winner"] in ("champion", "rejected") and "coin" in s["final"]["why"]
assert Path(s["dir"], "final", "X.md").read_text() != "" and Path(s["dir"], "final", "Y.md").read_text() != ""
print("hippodrome: pass", len(steps), "steps, champion", s["champion"])
