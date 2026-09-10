# Contributing

Read `AGENTS.md` first. It is the contract for anyone, human or agent, who
edits this repo.

## Kinds of change

- **A rule is wrong or a model misreads it.** Open an issue with the prompt,
  the output, and the reading you expected. Quote the rule.
- **A tell, a trap, or a technique is missing.** Name the source it comes from
  and the file and section where it belongs. Keep the proposed text to three
  sentences in the skill's plain style.
- **An install route for a new agent.** Cite the agent's own documentation
  for paths and commands. Include install, invoke, verify, update, uninstall,
  and where an always-on snippet goes.

## Rules for the text

- No em or en dashes, no curly quotes, no AI vocabulary. The lint enforces the
  first two; a reviewer enforces the third.
- One idea per sentence. A rule the model has to reread is a rule it will
  skip.
- `SKILL.md` does not grow. If your change adds a line there, your PR cuts
  one, and says which.
- Deslop patterns keep their numbers. New patterns take the next number.

## Before opening a PR

```bash
python3 skills/black-iris/scripts/universal/check.py
bash skills/black-iris/scripts/linux/check.sh
```

Both print `clean`. Then test in a fresh session from a neutral directory, and
put the prompt and the reply in the PR.

## Commit and PR text

Follow `skills/black-iris/references/ship.md`. Subject `type(scope): subject`,
imperative, lowercase, 72 characters. Body when the why is not in the diff.
No AI attribution trailer of any kind. The PR template asks four questions;
answer them and stop.

## License

By contributing you agree your change is licensed under GPL-2.0-only, the
same as the rest of the skill.
