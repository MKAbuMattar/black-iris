# Changelog

Format follows Keep a Changelog. Entries are written for someone deciding
whether to upgrade.

## 1.3.0 - 2026-09-11

### Changed

- The always-on hook costs about 11 KB per session instead of about 94 KB. It
  injects the router and your project's memory index, and no longer pastes all
  ten reference files into every session start, resume, clear, and compaction.
  The model opens a reference when the mode that needs it fires. If you relied
  on every mode being pre-loaded without invoking the skill, run
  `/black-iris` once in a session to get the old behaviour.

## 1.2.0 - 2026-09-11

### Added

- A Context mode, for tasks that analyze, count, filter, parse, or search bulk
  data. The agent names the answer before fetching the thing that contains it,
  turns the question into a script, and prints the value it needs in place of
  the corpus it came from. When a sandbox tool family is present in the
  session, such as the `ctx_*` tools from the separate context-mode MCP
  server, bulk work routes through it. When none is present the same
  discipline applies with ordinary shell and file tools, so nothing has to be
  installed for the mode to work.

## 1.1.0 - 2026-09-11

### Changed

- Memory now records how well each entry was checked. An episode is what
  happened on one dated occasion, a semantic entry is the claim that outlived
  the occasion, and a playbook is written only after you have run its steps
  and a check passed. A claim moves up a level on a second sighting, so one
  guess can no longer end up filed as a procedure that a later session runs.
- Memory is harvested when the knowledge appears: after a check passes, after
  a user correction, after a decision closes. The previous end-of-session
  harvest lost that detail to compaction before anything was written.
- Entries written before this release carry no class. The consolidation pass
  adds one the next time it runs over them. Nothing migrates a store on its
  own, and no entry is deleted for lacking a class.

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
