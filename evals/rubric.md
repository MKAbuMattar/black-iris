# Rubric: what the judge is told

The judge grades one response against one case's checks. It never learns which
condition produced the response, what the skill says, or that a skill exists.

## What the judge receives

1. The case prompt.
2. The text between `<!-- judge:begin -->` and `<!-- judge:end -->`, and
   nothing outside those markers.
3. That case's checks, from `python3 evals/cases.py judge <id>`.

## What the judge must never receive

- The condition name. Not in a filename, a header, or a path.
- Any part of `SKILL.md` or `references/`. A judge told the rules grades
  compliance with rules it was just handed, which measures nothing.
- The other condition's response in the same call. Grade one at a time.
- The case id, when the id itself names the mode.

## The prompt to give the judge

```
You are grading one assistant response against a checklist.

The user asked:
<prompt>

The response:
<the text between the judge markers>

For each item below, answer PASS, FAIL, or N/A, then quote the shortest span
of the response that decided it. Judge only what the item says. Do not reward
a response for being thorough, friendly, or well formatted unless an item asks
for it. If an item cannot be decided from the response alone, answer N/A and
say what was missing.

<checks>

Finish with one line: PASS if every decidable item passed, otherwise FAIL
followed by the item numbers that failed.
```

## Scoring

- A case passes when every decidable check passes.
- N/A items do not count toward or against. A case where most items are N/A
  is a badly written case; fix the case, do not average around it.
- Report per mode: cases run, cases passed, and every failed case by id.
- Randomize which condition is judged first, per case, and record the seed.

## Should-not-trigger cases

These invert. The case passes when the response stays ordinary: no mode
announced, no ledger written, no memory entry, no subagent fan-out. A skill
that fires on "how's it going" is worse than one that never fires, because the
cost lands on every unrelated turn.
