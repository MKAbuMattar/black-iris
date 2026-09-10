# Changelog

Format follows Keep a Changelog. Entries are written for someone deciding
whether to upgrade.

## 1.0.0 - 2026-09-10

### Added

- Eleven modes in one skill: Shape, Build, Deslop, Gates, Ideate, Prompt,
  Memory, Ship, Name, Review, Diagram, routed from a 200-line `SKILL.md`.
- A lite, full, deep dial for reply length that never trims the work.
- Claude Code SessionStart hook, gated by `~/.BLACK_IRIS_AGENTS/always-on`,
  that re-injects the skill, its references, and the project's memory index.
- On invocation the skill reads all nine references at once, so every mode
  is fully loaded for the session.
- Per-project store at `~/.BLACK_IRIS_AGENTS/projects/<slug>/` for gate
  ledgers, memory, backups, and scratch. Nothing is written into the repo.
- Lint and installer in Python, bash, and PowerShell under
  `skills/black-iris/scripts/`.
- Manifests for Claude Code, Codex, Kimi, Qwen, Gemini, Antigravity, and Pi.
- `INSTALL.md` covering more than thirty agents and harnesses.

### Changed

- Memory and gate files live outside `~/.claude` and outside the repo, in
  `~/.BLACK_IRIS_AGENTS`. The memory automation uses Stop and SessionStart,
  because PreCompact has no channel to the model. Deslop pattern ids are
  stable and lint-checked.

### Security

- The skill grants itself Read, Grep, Glob, and Agent only. Bash, Write, and
  Edit go through the harness permission prompt.
