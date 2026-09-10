# What black-iris is

A single Agent Skill that makes a coding agent behave the way a careful senior
engineer with an ADHD reader would: answer first, exact numbers, warnings
kept, code changes that trace to the request, a checkable definition of done,
and prose without machine tells.

## Who it is for

- People who read agent output on a phone, in a terminal, or between
  interruptions, and lose anything past the first screen.
- Teams that ship agent-written commits, PRs, and docs and do not want them to
  read as generated.
- Anyone who has watched an agent say "done" with a failing test.

## What it replaces

The usual stack of separate skills: one for prose, one for prompts, one for
completion gates, one for ideation, one for memory, one for response shape,
each with its own packaging and its own drift. Black-iris keeps every idea
that can live in a prompt in one folder and drops the rest.

## What it is not

- Not a checker. Gates are a discipline the model follows, not a program that
  blocks it. The one enforcement is Claude Code's permission prompt, which the
  skill deliberately does not pre-approve.
- Not an output style. It is a skill, so it costs nothing until invoked, and
  it works in every harness that reads `SKILL.md`.
- Not a diagram tool, a linter, or a memory database. It defers to a diagram
  skill for diagrams and uses a plain folder of markdown for memory.
- Not measured. No benchmark is claimed. `references/evals.md` says how to
  run an honest one.

## Principles

1. The prompt is the product. Packaging is thin manifests over one folder.
2. Nothing in the user's repo. Per-project state lives in
   `~/.BLACK_IRIS_AGENTS/`.
3. A claim the model cannot check is a claim it does not make.
4. Fewer words to the reader, never fewer to the work.
5. Stable ids, one source of truth per rule, lint over discipline.
