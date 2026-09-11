# Results

**Not yet run. No number here, and none anywhere else in the repo.**

`PRODUCT.md` says "Not measured. No benchmark is claimed." That stays true
until this file has a model, a date, an n, and every failed case named. The
harness below exists so the run is cheap when someone does it; a harness is
not a result.

## What exists

| Piece | State |
|---|---|
| `cases.jsonl` | 54 cases, 46 should-trigger and 8 should-not-trigger |
| `cases.py` | parser and coverage report, shared by runner and judge |
| `run.sh` | collects responses for one condition into `out/<condition>/` |
| `rubric.md` | what the judge is told, and what it is not shown |
| this file | the honest empty result |

## Coverage against the floor

`references/evals.md` asks for 8 to 12 prompts per measured mode. Run
`python3 evals/cases.py stats` for the live count. At the time of writing:

- Measurable: shape 10, build 8, context 8, deslop 8, gates 8, should-not-trigger 8.
- **Not measurable: memory 2, ship 2.** Below the floor. Either write six more
  cases each or say plainly that those two modes are unmeasured. Do not
  publish a number for them off 2 cases.

## How to run it

```bash
./evals/run.sh baseline  claude-opus-5
./evals/run.sh treatment claude-opus-5
```

Then judge with a model from a different family, following `rubric.md`, and
replace this file.

## What would make a result untrustworthy

Any of these, and the number is not worth publishing:

1. **Judge from the same family as the model under test.** It shares the
   habits being measured.
2. **Fewer than 8 cases for the mode the claim is about.** n of 3 is an
   anecdote with a percent sign.
3. **The baseline saw the skill.** An always-on flag or a user-level skill
   leaking into the baseline makes the two conditions the same condition.
4. **A zero-failure result.** That is a reason to check the harness, not to
   celebrate. `evals.md` says so and it is right.
5. **A failed case quietly dropped.** A case that cannot pass under the
   harness is marked unpassable and stays in the file.
