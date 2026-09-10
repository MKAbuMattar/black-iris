# Roadmap

Versions, not dates. Every item names its files and ends in a done-when that
a script or a person can check. What shipped is in `.github/CHANGELOG.md`;
this file only looks forward.

## 1.0.1: CI green before the first public tag

Goal: the release a clean machine installs is the release CI tested.

1. **First green run.** `.github/workflows/check.yml` exists and has never
   run. It lints on ubuntu and macos with `universal/check.py` and the bash
   lint, dry-runs the hook, parses every manifest, and runs `check.ps1` and
   `install.ps1` on windows-latest. The PowerShell scripts were written on a
   machine without pwsh. A red runner is fixed in the script that failed.
   Done when one run on the release commit is green on all three runners.
2. **Publish.** Push, tag `v1.0.1`, write the entry in `.github/CHANGELOG.md`.
   On a machine with no prior copy, verify the Claude Code plugin route and
   the Codex route from `INSTALL.md`. The other routes wait for the users
   who file issues; `INSTALL.md` cites each agent's own docs, not a test.
   Done when both routes install and the "Verify it works" step passes.

## 1.1.0: measured

Goal: retire "no benchmark is claimed" with numbers a skeptic can check.

1. **Run the eval.** Build `evals/cases/` and `evals/RESULTS.md` by
   following `skills/black-iris/references/evals.md`: 8 to 12 cases per
   measured mode, 6 to 8 should-not-trigger prompts, a judge from another
   model family, judge markers, randomized order.
   Done when `evals/RESULTS.md` carries the model, date, n, and every
   failed case by name. A zero-failure file triggers the harness audit the
   eval doc requires, not a celebration.
2. **Point the claim at the result.** Edit the "Not measured" bullet in
   `PRODUCT.md` to cite `evals/RESULTS.md` with its n and judge family.
   Done when `PRODUCT.md` makes no claim `evals/RESULTS.md` does not
   support.

## 1.2.0: an opt-in brake for Gates

Goal: an unchecked gate can stop a false "done", Claude Code only, for users
who turn it on.

1. **Check the channel before writing the hook.** Confirm in the Claude Code
   hooks reference that a Stop hook's block decision and reason reach the
   model. Hook recipes written from memory have shipped as no-ops before
   because nobody checked the event's output channel.
   Done when the header of `hooks/gates-stop.sh` cites the doc section and
   the output field it relies on.
2. **Ship it off by default.** Add `hooks/gates-stop.sh`, gated by
   `~/.BLACK_IRIS_AGENTS/gates-stop`, exit 0 on every path, reading the
   project's `GATES.md` from the store. Wire it in `hooks/hooks.json`,
   document it in `INSTALL.md`, and fix the enforcement wording in
   `PRODUCT.md` and `DESIGN.md`, which both say the permission prompt is
   the only enforcement.
   Done when the flag absent leaves a session unchanged, and the flag
   present blocks the stop and names the unchecked gate ids.

## On request

Each item waits for its trigger and ships as a minor version.

1. **OpenCode always-on plugin.** Trigger: an OpenCode user asks for
   always-on beyond the snippet `INSTALL.md` documents. Adds
   `.opencode/plugins/black-iris.mjs` on the
   `experimental.chat.system.transform` route.
   Done when a fresh OpenCode session carries the skill with no invocation
   and `INSTALL.md` carries the route.
2. **Gemini command route.** Trigger: a Gemini CLI user asks to invoke the
   skill without the extension's always-on behavior. Adds a self-contained
   command `toml` beside `gemini-extension.json`.
   Done when `/black-iris` runs in a fresh profile with the extension
   absent.
3. **Cursor mirror.** Trigger: a Cursor user reports the copy route broken.
   Adds `.cursor/skills/black-iris/` as a byte copy and a `cmp` step in
   `.github/workflows/check.yml` so it can never drift.
   Done when CI proves the mirror identical to the source on every push.
4. **Eigent route.** Trigger: Eigent documents where a custom skill folder
   lives. Replaces the unverified paragraph in `INSTALL.md`.
   Done when the section has an install, invoke, and verify step.

## Not planned

- A checker binary, a memory database, or an orchestration layer. The
  prompt is the product. Skills of this kind commonly carry 10 to 50 lines
  of packaging per line of prompt, and this repo exists to reverse that.
- Per-model prompt routing. Slugs and parameters rot monthly, per
  `DESIGN.md`. Routing stays by tool class.
- More translations. English, Spanish, and Arabic exist for the README and
  the install guide. Translated docs drift untested, so a new language ships
  only with a maintainer who uses it.
- A 2.0. No document here motivates a breaking change. A 2.0 opens when
  someone writes down what breaks and why the break is worth it.
