# Design

## One router, ten references

`SKILL.md` is a routing table plus the rules that must be true on every reply:
Shape, Build, the Cut list, the Pre-send check, and one paragraph per mode
with the hard rule the model needs before it opens the file. Everything else
is a reference. On a bare `/black-iris` the model reads every reference named
in the table, so all modes are loaded for that session; otherwise the table
says which one file to open when a mode fires.

The always-on hook injects the router and nothing else. It used to cat every
reference too, which cost 94 KB against the router's 11 KB, and it fires on
compact, so the event that exists to free the window spent a fifth of it again
before the first reply. A skill with a mode about keeping bulk data out of
context should not open every session by dumping 82 KB of its own prose. CI
asserts the payload carries no reference block and stays under 20 KB.

The 16,000-byte cap on `SKILL.md` keeps the always-on core cheap. It replaced
a 200-line cap that had started buying compression at the cost of clarity.
The Ship, Name, and Review handoffs were cut for space because those modes
always load their reference anyway. Diagram has no handoff and no reference
because its table row is the whole contract.

## The dial

Three levels of how much to say, never how much to do or how long to think.
`lite` for questions and acknowledgments, `full` for deliverables, `deep` when
the user asks to be walked through. The escape hatch ("brevity is
suspended for this reply") is what stops a terse skill from truncating a
deliverable.

## Store outside the repo

Gate ledgers, memory, backups, and scratch go to
`~/.BLACK_IRIS_AGENTS/projects/<slug>/`. The slug is the project root with
`/` as `-`, derived by one command in `memory.md` that every mode and the hook
share: `CLAUDE_PROJECT_DIR`, then git's top level, then `pwd`. Defining it
once was a review finding; two derivations had already drifted.

## The hook

A SessionStart hook, gated by a flag file, prints the skill body and the
project's `MEMORY.md`. SessionStart is one of four events whose plain stdout
reaches the model; PreCompact is not one of them, and the autodream recipe
that used it was a no-op. The hook prints its own root path so an always-on
session can resolve `references/`. It exits 0 on every path.

## Enforcement is the permission prompt, plus one opt-in brake

The frontmatter grants Read, Grep, Glob, and Agent only. Bash, Write, and Edit
go through the harness prompt, which is the confirm step the destructive-action
rule relies on. An earlier draft pre-approved them, and a reviewer pointed out
that one `/black-iris` would then have changed the permission posture of the
whole session.

`hooks/gates-stop.sh` is the second one, off unless you create
`~/.BLACK_IRIS_AGENTS/gates-stop`. It refuses a stop while the ledger lists
unmet gates. It was written against the hooks reference rather than from
memory: the "Exit code 2 behavior per event" table is what says a Stop hook
can block and that stderr carries the reason to the model, and exit 2 plus
stderr is the whole mechanism. No JSON output field is involved, because a
recipe built on the wrong field is a silent no-op, which is exactly what
happened to the PreCompact autodream recipe this project shipped and then
retracted.

Two things it deliberately does not do. It never decides whether a gate
should have passed; it reads the ids you wrote. And it blocks at most once per
ledger state per session, so a model that changes nothing stops on the second
try and can never be trapped in a loop.

## Jerash, Siq, and Dabke carry the only scripts

Jerash races 100 entrants by default, 595 Agent calls in 70 waves, and that
size cannot live in a context window or a markdown ledger. So it is the one
mode with state code: `jerash/hippodrome.py` holds the race in one JSON file
in the store and `next` says what to run, so a compacted session resumes
from disk. The rubric weights live only in `jerash/rubric.md`, which the
script parses, and the brief templates live only in `jerash/briefs.md`. The
lane cards in `jerash/lanes.json` are named for places in Jordan; the names
are handles and the `how` lines are the instructions. A tie the rubric
cannot break goes to the run's seeded coin, recorded, so a replayed seed
gives the same race.

Siq is the other one, because no prompt can see its own context size.
`siq/siq.py` reads the fill from the transcript's usage records, infers the
window per model, and asks from the Stop hook once per compaction cycle at
about 70 percent, while the model still holds the session. It asks for the
three sections the built-in summary lacks, Decisions, Verified, and
Corrections, and writes Open gates itself. SessionStart reads the file back
after compaction, capped at 4096 bytes, and falls back to an extract from
the transcript when nothing was written. Full design: `SIQ.md`.

Dabke is the third. A loop that must not stop needs something outside the
model to refuse the stop, and the hook needs state the model cannot forget:
`dabke/dabke.py` keeps the brief, the step count, and a digest of the ledger
and the step log on disk. The hook hands the next step on stderr while the
ledger has an unmet gate. It ignores `stop_hook_active`, because continuing
is the point, and two other rules keep it from trapping a session: a stop
with nothing changed gets one warning and the second lets go, and the step
budget, 40 by default, ends with a handoff report. Confidence is defined as
four observable proofs rather than a feeling, so "not High" always has a
concrete next read: the failing log, the file, the lockfile, the upstream
source, the release notes, the uses of the name.

## Gates without a checker

The ledger format is kept; no checker program ships with it. The model runs
`CHECK:` itself and records exit code and matched token. What is kept instead
is every rule that makes a ledger honest: a green check proves the command
and not the English, negative controls, independently measured numbers,
abandonment as a non-success state, three claim classes, and the last-good
artifact trap.

## Stable pattern ids

Deslop patterns are numbered once. The Cut list cites pattern 17 by number.
Removing a pattern leaves a gap, and the lint checks that ids are unique and
ascending rather than pinning a count.

## Two-model review

Every section was audited by a second model from another family, mode by
mode, and then by a third reviewer with the full file set. Their
findings are applied, not summarized, and the ones that changed behavior are
recorded above. How to keep such a reviewer blind is in `references/evals.md`.

## What was left out on purpose

- Any depth tree, lease, or dispatch machinery. The Stop hook that was
  listed here is now `hooks/gates-stop.sh`, off by default.
- A diagram renderer. Diagram mode defers to a dedicated skill.
- Per-model prompt slugs and parameters. They rot monthly; routing is by
  tool class.
- Translations without a maintainer. Translated docs drift untested.
