# Evals: measuring whether this skill works

A skill is prose, and prose is the layer that drifts. Most skills that claim
numbers publish weak ones (n of 3 to 12, a judge from the same model family)
or retract them later. Do not repeat that. Run a small honest eval, or make
no claim.

## Isolation

- Run the skill under test and the baseline with the same pinned model.
- Start each run with settings and skills cleared, so the always-on flag and
  any user skill cannot leak into the baseline. In Claude Code:
  `claude -p --setting-sources "" ...` for the baseline, then load the skill
  explicitly for the treatment.
- Use a neutral working directory outside this repo, so the CLI cannot read
  the skill's own files or a `CLAUDE.md`.
- Deny tools unless the case needs them. A case that needs tools says so and
  is scored separately from prose-only cases.

## Cases

Write 8 to 12 prompts per mode you want to measure. Each case has an
expected shape a rubric can check, not a golden answer:

- Shape: is line one an action or a verdict? Are figures exact? Is the
  blocking question last? Is there a closer?
- Deslop: count the tells from `deslop.md` that survive.
- Gates: was a ledger written before the first edit? Did an unmet gate stop
  the "done" report?
- Build: does every changed line trace to the request?

Also write 6 to 8 should-not-trigger prompts: casual questions where the
skill loading, or the mode firing, would be wrong.

## Judging

- Judge with a model from a different family than the one under test.
- Send the judge only the response and the rubric. Wrap the region it may
  see in `<!-- judge:begin -->` and `<!-- judge:end -->` markers, so
  condition names, file paths, and the skill text never reach it.
- Randomize which of the two responses is shown first.

## Publishing

Write `RESULTS.md` next to the cases with the model, date, n, and every
failed or regressed case named. A case that cannot pass under the harness
(for example, one that needs a tool the runner denied) is marked unpassable,
not deleted. A result file with no failures on it is a reason to check the
harness, not a reason to celebrate.
