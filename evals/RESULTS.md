# Results

**Still not the eval. This is a smoke test, and it says so.**

`../docs/en/PRODUCT.md` keeps saying no benchmark is claimed, and that stays true. What
follows is eight cases run live with mechanical scoring. It is enough to find a
real defect, which it did, and nowhere near enough to publish a number.

## What this run was

| | |
|---|---|
| Date | 2026-09-11 |
| Runner | Claude Code CLI 2.1.268, `claude -p --plugin-dir <repo>` |
| Model | **not pinned.** The CLI default, whatever it was that day |
| Conditions | treatment only. **No baseline was run** |
| Judge | none. Mechanical regex only |
| n | 8: six should-trigger, two should-not-trigger |
| Working dir | a fresh temp directory outside the repo |

Four of the five things `evals.md` requires are missing: a pinned model, both
conditions, a judge from another family, and randomised order. Treat every
number below as an observation, not a measurement.

## What it found

**One real defect.** Case `shape-07`, the prompt "Thanks, that worked.",
returned:

> Noted. Anything else?

That is a closing offer. Cut list item 5 and Shape rule 10 both forbid it, and
rule 10 says plainly that "want me to X?" is not an ending. The cause was a gap
in rule 10: it wanted an action for the reader, an acknowledgement has none, so
the model invented a closer to fill the empty slot.

**Fixed.** Rule 10 now says that when a turn leaves neither an action nor a
question, the reply ends on what changed and stops, and an acknowledgement ends
after its first line. Re-probed with three phrasings of the same case:

| Prompt | Before | After |
|---|---|---|
| "Thanks, that worked." | `Noted. Anything else?` | `Glad it's sorted.` |
| "Perfect, thanks." | not run | no closer, 50 chars |
| "Great, that fixed it." | not run | no closer, ends on a reader action |

Three probes is not a measurement. It is the case that failed, now passing.

**One weaker signal.** Case `shape-02` gave the p99 shift as "7.5x" and never
restated 120ms and 900ms. Shape rule 4 says never drop the figure that makes a
claim actionable. Defensible either way, so it is recorded and not counted.

**Both should-not-trigger cases passed.** "Hey, how's it going?" got 65
characters with no mode announced, and "What is the capital of Portugal?" got
"Lisbon." The greeting contained an em dash, which is the strongest evidence
available that the skill genuinely did not engage: its Cut list bans them.

## What the scoring got wrong

Three of the four initial failures were the scoring, not the skill.
`deslop-01` and `deslop-05` were flagged for containing "leveraging",
"cutting-edge", "crucial" and a not-X-but-Y. Every one of those appears inside
a quotation, because naming the triggering line is what the Deslop process
tells the model to do. A regex cannot tell quoted input from emitted output.

That is the negative-control lesson from `gates.md` arriving in its own eval: a
check that fires on the wrong thing looks exactly like a finding. Any future
scorer must read only the delivered text, not the mode's working.

## Raw tally

Mechanical checks: 20 of 24 passed. After removing the three scoring artifacts,
one genuine failure remains, `shape-07`.

## Routing smoke, 2026-09-30

`evals/mizan.py --per-mode 2`: the first two cases of each mode, 26 in all,
run with only this plugin loaded (`--setting-sources ""`), Claude Code
2.1.285, model claude-opus-5-5 (the CLI default, not pinned). No judge: a
case is a hit when the model opened the expected `references/<mode>.md`
before its first written answer. Quality was not scored.

**Routed right: 18 of 26.** No false fire and no wrong mode: every failure
is a miss, the skill or the reference never opened.

| mode | n | hit | miss |
|---|---|---|---|
| athar, build, council, dabke, jerash, none, shape | 2 each | 2 each | 0 |
| gates, memory, ship, siq | 2 each | 1 each | 1 each |
| context, deslop | 2 each | 0 | 2 each |

Missed, by name:

- `deslop-01`, `deslop-02`: "Deslop this" and "Humanize" were answered
  from the model's own knowledge without loading the skill, though both
  words are in the description's trigger list. Traced by hand for
  `deslop-01`.
- `context-01`, `context-02`: bulk-data asks with no data present.
- `gates-01`, `ship-01`, `memory-02`, `siq-01`: one miss each.

The first run of this smoke scored 11 of 26 and was a harness bug, not a
result: headless `-p` denies the Skill tool unless it is allowed, so only
slash-command cases could load the skill. `mizan.py` now allows Skill and
the read tools.

Not weighed: ideate, name, prompt, review. They have no cases yet.

## Still needed for a real result

1. A pinned model, recorded here by id.
2. A baseline condition with settings and skills cleared.
3. A judge from a different model family, seeing only the text between the
   judge markers.
4. Randomised order, with the seed recorded.
5. All 66 cases, not eight.

Until then this file publishes no benchmark, and neither does anything else in
the repo.
