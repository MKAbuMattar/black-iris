#!/usr/bin/env python3
# /// script
# requires-python = ">=3.8"
# ///
"""hippodrome.py: the race state for the black-iris Jerash mode.

One JSON file holds the whole race, so the orchestrator never has to keep a
100-entrant bracket in its context, and a compacted session picks up where it
stopped.

    hippodrome.py plan [--field N | --quick]       heats, calls, and waves; writes nothing
    hippodrome.py init --task FILE [--field N | --quick] [--seed S]
                       [--rejected FILE --reason FILE] [--wave W]
    hippodrome.py next                              what to do now, and the command for it
    hippodrome.py briefs <phase>                    write the briefs still to run, listed in waves
    hippodrome.py pending <phase>                   outputs still missing for a phase
    hippodrome.py collect                           read this round's verdicts, record winners
    hippodrome.py advance                           close the round, pair the survivors
    hippodrome.py status                            who is still racing, per round
    hippodrome.py champion                          the last entrant, its lane, what it beat
    hippodrome.py card <entrant>                    one entrant's lane card

Phases: entry, then per round critique, reply, judge; then final, only when a
rejected answer exists. Runs live in the black-iris store:
~/.BLACK_IRIS_AGENTS/projects/<slug>/jerash/<run>/. Every command after init
finds the run through jerash/LATEST; --run picks another.

Standard library only.
"""
import argparse
import json
import math
import os
import random
import re
import subprocess
import sys
import time
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIELD, QUICK, WAVE = 100, 16, 10
PHASES = ("entry", "critique", "reply", "judge", "final")


class RaceError(Exception):
    pass


# ------------------------------------------------------------ store and files

def project_root():
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return env
    try:
        out = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip()
    except OSError:
        pass
    return os.getcwd()


def races_dir():
    """The same slug rule as references/memory.md: the project path with / as -."""
    return Path.home() / ".BLACK_IRIS_AGENTS" / "projects" / project_root().replace("/", "-") / "jerash"


def filled(path):
    """An output counts once it exists and has something in it."""
    p = Path(path)
    return p.is_file() and p.stat().st_size > 0


def load_rubric():
    """Criterion weights, from the table in rubric.md. The page is the source."""
    rows = re.findall(r"^\| ([a-z]+) \| (\d+) \|", (HERE / "rubric.md").read_text(encoding="utf-8"), re.M)
    if not rows:
        raise RaceError("rubric.md has no criteria table")
    return [(name, int(w)) for name, w in rows]


def load_decks():
    data = json.loads((HERE / "lanes.json").read_text(encoding="utf-8"))
    decks = {}
    for key in ("approach", "route", "priority"):
        cards = data.get(key) or []
        ids = [c["id"] for c in cards]
        if not cards or len(set(ids)) != len(ids):
            raise RaceError(f"lanes.json deck '{key}' is empty or repeats an id")
        decks[key] = {c["id"]: c for c in cards}
    return decks


def load_briefs():
    text = (HERE / "briefs.md").read_text(encoding="utf-8")
    found = dict(re.findall(r"<!-- brief:([a-z]+) -->\n(.*?)\n<!-- /brief -->", text, re.S))
    missing = [p for p in PHASES if p not in found]
    if missing:
        raise RaceError("briefs.md is missing: " + ", ".join(missing))
    return found


def fill(template, values):
    """One pass, so a task that itself contains {{braces}} survives untouched."""
    wanted = set(re.findall(r"\{\{([a-z_]+)\}\}", template))
    gaps = sorted(wanted - set(values))
    if gaps:
        raise RaceError("no value for: " + ", ".join(gaps))
    return re.sub(r"\{\{([a-z_]+)\}\}", lambda m: str(values[m.group(1)]), template)


# ------------------------------------------------------------ sizing

def rounds_for(n):
    """Heats per round for a field of n: floor(m/2) heats, ceil(m/2) go through."""
    out, m = [], n
    while m > 1:
        out.append(m // 2)
        m = (m + 1) // 2
    return out


def plan(n, wave, final):
    heats = rounds_for(n)
    waves = math.ceil(n / wave) + sum(2 * math.ceil(2 * h / wave) + math.ceil(h / wave) for h in heats)
    calls = n + 5 * sum(heats) + (1 if final else 0)
    return {"field": n, "rounds": len(heats), "heats": sum(heats), "calls": calls,
            "waves": waves + (1 if final else 0)}


# ------------------------------------------------------------ state

def run_dir(args):
    root = races_dir()
    run = getattr(args, "run", None)
    if not run and (root / "LATEST").exists():
        run = (root / "LATEST").read_text().strip()
    if not run:
        raise RaceError(f"no race yet under {root}; run init first")
    return root / run


def load(args):
    d = run_dir(args)
    return json.loads((d / "state.json").read_text(encoding="utf-8"))


def save(state):
    p = Path(state["dir"]) / "state.json"
    tmp = p.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=1), encoding="utf-8")
    tmp.replace(p)   # atomic, so a crash mid-write never leaves half a race


def pair(ids, rng, rnd, run):
    ids = list(ids)
    rng.shuffle(ids)
    bye = ids.pop() if len(ids) % 2 else None
    heats = [{"id": f"r{rnd}h{i + 1:02d}", "left": ids[2 * i], "right": ids[2 * i + 1], "winner": None, "why": ""}
             for i in range(len(ids) // 2)]
    for h in heats:
        (Path(run) / f"r{rnd}" / h["id"]).mkdir(parents=True, exist_ok=True)
    return {"heats": heats, "bye": bye}


def init(task_text, n, seed, rejected=None, reason=None, wave=WAVE):
    if n < 2:
        raise RaceError("a race needs at least 2 entrants")
    if bool(rejected) != bool(reason):
        raise RaceError("--rejected and --reason go together: a rematch needs the reason")
    decks = load_decks()
    combos = list(product(*(sorted(decks[k]) for k in ("approach", "route", "priority"))))
    if n > len(combos):
        raise RaceError(f"only {len(combos)} distinct lane cards; field must be {len(combos)} or fewer")
    seed = seed if seed is not None else random.randrange(1 << 30)
    rng = random.Random(seed)
    # ponytail: plain sample of the combinations; spread per deck is even on average, not exactly
    cards = rng.sample(combos, n)
    run_id = time.strftime("%Y%m%d-%H%M%S")
    d = races_dir() / run_id
    (d / "entries").mkdir(parents=True, exist_ok=False)
    (d / "task.md").write_text(task_text.rstrip("\n") + "\n", encoding="utf-8")
    if rejected:
        (d / "rejected.md").write_text(rejected, encoding="utf-8")
        (d / "reason.md").write_text(reason.rstrip("\n") + "\n", encoding="utf-8")
    ids = [f"e{i + 1:03d}" for i in range(n)]
    entrants = {e: {"card": dict(zip(("approach", "route", "priority"), c)), "entry": str(d / "entries" / f"{e}.md"),
                    "out_round": None} for e, c in zip(ids, cards)}
    state = {"run": run_id, "dir": str(d), "seed": seed, "field": n, "wave": wave, "has_rejected": bool(rejected),
             "entrants": entrants, "round": 1, "rounds": {"1": pair(ids, rng, 1, d)}, "champion": None,
             "final": None}
    save(state)
    (races_dir() / "LATEST").write_text(run_id + "\n")
    return state


# ------------------------------------------------------------ jobs

def heat_path(state, heat, name):
    return str(Path(state["dir"]) / heat["id"].split("h")[0] / heat["id"] / name)


def jobs(state, phase):
    d, E = Path(state["dir"]), state["entrants"]
    if phase == "entry":
        return [{"id": f"entry-{e}", "kind": "entry", "entrant": e, "outputs": [E[e]["entry"]]} for e in E]
    if phase == "final":
        if not (state["champion"] and state["has_rejected"]):
            return []
        return [{"id": "final", "kind": "final", "outputs": [str(d / "final" / "verdict.json")]}]
    out = []
    for h in state["rounds"][str(state["round"])]["heats"]:
        sides = ((h["left"], h["right"]), (h["right"], h["left"]))
        if phase == "critique":
            out += [{"id": f"{h['id']}-critique-{me}", "kind": phase, "heat": h, "entrant": me, "rival": rv,
                     "outputs": [heat_path(state, h, f"critique-of-{rv}.md")]} for me, rv in sides]
        elif phase == "reply":
            out += [{"id": f"{h['id']}-reply-{me}", "kind": phase, "heat": h, "entrant": me, "rival": rv,
                     "outputs": [heat_path(state, h, f"reply-{me}.md"), heat_path(state, h, f"revised-{me}.md")]}
                    for me, rv in sides]
        elif phase == "judge":
            out.append({"id": f"{h['id']}-judge", "kind": phase, "heat": h,
                        "outputs": [heat_path(state, h, "verdict.json")]})
    return out


def missing(state, phase):
    return [j for j in jobs(state, phase) if not all(filled(o) for o in j["outputs"])]


def values(state, job):
    d, E, decks = Path(state["dir"]), state["entrants"], load_decks()
    v = {"task": (d / "task.md").read_text(encoding="utf-8").rstrip("\n"), "run": str(d),
         "rubric": str(HERE / "rubric.md"), "field": state["field"],
         "criteria": ", ".join(c for c, _ in load_rubric())}

    def lane(e):
        c = E[e]["card"]
        out = {}
        for k in ("approach", "route", "priority"):
            card = decks[k][c[k]]
            out[f"{k}_name"], out[f"{k}_how"] = card["name"], card["how"]
        return out

    k = job["kind"]
    if k == "entry":
        v.update(lane(job["entrant"]), entrant=job["entrant"], out=job["outputs"][0])
        v["rejected_note"] = (
            f"The person already got an answer to this task and rejected it: {d / 'rejected.md'}. "
            f"Their reason: {d / 'reason.md'}. Read both first. The last entry left is compared with that answer."
            if state["has_rejected"] else "No earlier answer exists. Work from the task.")
    elif k in ("critique", "reply"):
        h, me, rv = job["heat"], job["entrant"], job["rival"]
        v.update(lane(me), entrant=me, rival=rv, heat=h["id"], round=state["round"],
                 own_entry=E[me]["entry"], rival_entry=E[rv]["entry"],
                 critique=heat_path(state, h, f"critique-of-{me}.md"), out=job["outputs"][0])
        if k == "reply":
            v.update(reply_out=job["outputs"][0], revised_out=job["outputs"][1])
    elif k == "judge":
        h = job["heat"]
        v.update(heat=h["id"], round=state["round"], left=h["left"], right=h["right"], out=job["outputs"][0])
        for side in ("left", "right"):
            e = h[side]
            v[f"{side}_entry"] = heat_path(state, h, f"revised-{e}.md")
            v[f"{side}_critique"] = heat_path(state, h, f"critique-of-{e}.md")
            v[f"{side}_reply"] = heat_path(state, h, f"reply-{e}.md")
    elif k == "final":
        v.update(x_entry=str(d / "final" / "X.md"), y_entry=str(d / "final" / "Y.md"),
                 reason=str(d / "reason.md"), out=job["outputs"][0])
    return v


def write_briefs(state, phase):
    todo = missing(state, phase)
    if not todo:
        return []
    templates = load_briefs()
    d = Path(state["dir"])
    if phase == "final":
        # Blind: the final judge sees X and Y, never which one is the champion.
        fin = state["final"] or {}
        if not fin:
            order = ["champion", "rejected"]
            random.Random(state["seed"] + 1).shuffle(order)
            fin = state["final"] = {"X": order[0], "Y": order[1], "winner": None}
            save(state)
        (d / "final").mkdir(exist_ok=True)
        src = {"champion": state["entrants"][state["champion"]]["entry"], "rejected": str(d / "rejected.md")}
        for label in ("X", "Y"):
            (d / "final" / f"{label}.md").write_text(Path(src[fin[label]]).read_text(encoding="utf-8"), encoding="utf-8")
    for j in todo:
        for o in j["outputs"]:
            Path(o).parent.mkdir(parents=True, exist_ok=True)
        if j["kind"] == "entry":
            (d / "scratch" / j["entrant"]).mkdir(parents=True, exist_ok=True)
        p = d / "briefs" / phase / f"{j['id']}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(fill(templates[j["kind"]], values(state, j)) + "\n", encoding="utf-8")
        j["brief"] = str(p)
    return todo


# ------------------------------------------------------------ verdicts

def total(scores, weights):
    return sum(int(scores.get(c, 0)) * w for c, w in weights) / 10


def decide(verdict, a, b, weights, rng):
    """(winner, why). Broken loses to not broken; then total; then fewer standing; then sound; then a seeded coin."""
    s, st = verdict["scores"], verdict.get("standing", {})
    for e in (a, b):
        if e not in s:
            raise RaceError(f"verdict has no scores for {e}")
    key = {e: (not s[e].get("broken", False), total(s[e], weights), -int(st.get(e, 0)), int(s[e].get("sound", 0)))
           for e in (a, b)}
    if key[a] == key[b]:
        return rng.choice([a, b]), "exact tie, settled by the run's seeded coin"
    return (a if key[a] > key[b] else b), verdict.get("why", "")


def read_verdict(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def collect(state):
    weights, bad = load_rubric(), []
    rng = random.Random(f"{state['seed']}-{state['round']}")
    if state["champion"] and state["final"]:
        v = read_verdict(Path(state["dir"]) / "final" / "verdict.json")
        if v is None:
            raise RaceError("final verdict is missing or not JSON; rerun the final brief")
        w, why = decide(v, "X", "Y", weights, rng)
        state["final"].update(winner=state["final"][w], why=why,
                              totals={k: total(v["scores"][k], weights) for k in ("X", "Y")})
        save(state)
        return []
    for h in state["rounds"][str(state["round"])]["heats"]:
        if h["winner"]:
            continue
        v = read_verdict(heat_path(state, h, "verdict.json"))
        if v is None:
            bad.append(h["id"])
            continue
        h["winner"], h["why"] = decide(v, h["left"], h["right"], weights, rng)
        h["survived"] = v.get("survived", [])
    save(state)
    return bad


def advance(state):
    r = state["rounds"][str(state["round"])]
    open_heats = [h["id"] for h in r["heats"] if not h["winner"]]
    if open_heats:
        raise RaceError("heats without a winner: " + ", ".join(open_heats) + "; run collect")
    alive = []
    for h in r["heats"]:
        loser = h["right"] if h["winner"] == h["left"] else h["left"]
        state["entrants"][loser]["out_round"] = state["round"]
        rev = heat_path(state, h, f"revised-{h['winner']}.md")
        if filled(rev):
            state["entrants"][h["winner"]]["entry"] = rev
        alive.append(h["winner"])
    if r["bye"]:
        alive.append(r["bye"])
    if len(alive) == 1:
        state["champion"] = alive[0]
    else:
        state["round"] += 1
        rng = random.Random(f"{state['seed']}-pair-{state['round']}")
        state["rounds"][str(state["round"])] = pair(sorted(alive), rng, state["round"], state["dir"])
    save(state)
    return alive


def next_step(state):
    if missing(state, "entry"):
        return "entry"
    if state["champion"]:
        if state["has_rejected"] and not (state["final"] or {}).get("winner"):
            return "final" if missing(state, "final") or not state["final"] else "collect"
        return "done"
    for phase in ("critique", "reply", "judge"):
        if missing(state, phase):
            return phase
    heats = state["rounds"][str(state["round"])]["heats"]
    return "collect" if any(not h["winner"] for h in heats) else "advance"


# ------------------------------------------------------------ CLI

def main(argv=None):
    ap = argparse.ArgumentParser(prog="hippodrome.py")
    ap.add_argument("--run", help="a run id under the store; default is jerash/LATEST")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "init"):
        p = sub.add_parser(name)
        p.add_argument("--field", type=int, default=FIELD)
        p.add_argument("--quick", action="store_true")
        p.add_argument("--wave", type=int, default=WAVE)
        if name == "init":
            p.add_argument("--task", required=True)
            p.add_argument("--seed", type=int)
            p.add_argument("--rejected")
            p.add_argument("--reason")
        else:
            p.add_argument("--final", action="store_true", help="count the check against a rejected answer")
    for name in ("briefs", "pending"):
        sub.add_parser(name).add_argument("phase", choices=PHASES)
    for name in ("next", "collect", "advance", "status", "champion"):
        sub.add_parser(name)
    sub.add_parser("card").add_argument("entrant")
    a = ap.parse_args(argv)
    here = f"python3 {Path(__file__).resolve()}"
    try:
        if a.cmd in ("plan", "init"):
            n = QUICK if a.quick else a.field
        if a.cmd == "plan":
            p = plan(n, a.wave, a.final)
            print(f"{p['field']} entrants, {p['rounds']} rounds, {p['heats']} heats, "
                  f"{p['calls']} Agent calls in {p['waves']} waves of up to {a.wave}")
        elif a.cmd == "init":
            read = lambda f: Path(f).read_text(encoding="utf-8") if f else None
            s = init(read(a.task), n, a.seed, read(a.rejected), read(a.reason), a.wave)
            p = plan(n, a.wave, s["has_rejected"])
            print(f"race {s['run']} at {s['dir']}: {n} entrants, seed {s['seed']}, {p['calls']} Agent calls")
        else:
            state = load(a)
            if a.cmd == "next":
                step = next_step(state)
                print(step.upper() if step == "done" else f"{step}: {here} " +
                      ("briefs " + step if step in PHASES else step))
            elif a.cmd == "briefs":
                todo = write_briefs(state, a.phase)
                if not todo:
                    print(f"{a.phase}: nothing left to run")
                w = state["wave"]
                for i in range(0, len(todo), w):
                    print(f"wave {i // w + 1}: " + " ".join(j["brief"] for j in todo[i:i + w]))
            elif a.cmd == "pending":
                for j in missing(state, a.phase):
                    print(j["id"], " ".join(o for o in j["outputs"] if not filled(o)))
            elif a.cmd == "collect":
                bad = collect(state)
                print("collected" if not bad else "rerun these judges, verdict missing or not JSON: " + " ".join(bad))
            elif a.cmd == "advance":
                alive = advance(state)
                print(f"round {state['round'] - (0 if state['champion'] else 1)} closed: {len(alive)} of "
                      f"{state['field']} still racing" + (f"; {state['champion']} holds the lane" if state["champion"] else ""))
            elif a.cmd == "status":
                left = [e for e, v in state["entrants"].items() if v["out_round"] is None]
                print(f"round {state['round']}: {len(left)} of {state['field']} still racing"
                      + (f"; champion {state['champion']}" if state["champion"] else ""))
            elif a.cmd == "champion":
                c = state["champion"]
                if not c:
                    raise RaceError("no champion yet; run next")
                beat = [h for r in state["rounds"].values() for h in r["heats"] if h["winner"] == c]
                print(f"champion {c}: {state['entrants'][c]['entry']}")
                print("lane: " + " / ".join(state["entrants"][c]["card"].values()))
                for h in beat:
                    rival = h["right"] if h["left"] == c else h["left"]
                    print(f"  beat {rival} in {h['id']}: {h['why']}")
                fin = state.get("final") or {}
                if fin.get("winner"):
                    print(f"final against the rejected answer: {fin['winner']} won, totals {fin['totals']}; {fin.get('why', '')}")
            elif a.cmd == "card":
                c, decks = state["entrants"][a.entrant]["card"], load_decks()
                for k in ("approach", "route", "priority"):
                    print(f"{k}: {decks[k][c[k]]['name']}. {decks[k][c[k]]['how']}")
    except (RaceError, KeyError, FileNotFoundError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
