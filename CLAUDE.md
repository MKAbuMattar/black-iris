@AGENTS.md

## Claude Code specifics

- Validate the skill folder with the skill-builder validator if it is
  installed: `bash ~/.claude/skills/skill-builder/scripts/validate-skill.sh skills/black-iris`.
  Target is 100%.
- Test a change in a fresh session from a neutral directory, never from this
  repo, so the CLI cannot read the skill's own files as project context:
  `cd "$(mktemp -d)" && echo '/black-iris <a small how-to question>' | claude -p`.
- Load the hook for a session without publishing: `claude --plugin-dir "$PWD"`.
- A second model reviewing this skill catches what this one misses. Before a
  release, pipe `SKILL.md` and the references into a model from another family
  and ask for ranked findings; `skills/black-iris/references/evals.md` says how
  to keep that judge blind.
