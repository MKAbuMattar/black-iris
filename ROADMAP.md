# Roadmap

Ordered, not dated, and not numbered. A version number in a heading here went
stale twice in one day, because it assumed roadmap items are the only things
that ship. Every item names its files and ends in a done-when a script or a
person can check. What shipped is in `.github/CHANGELOG.md`; this file only
looks forward, and an item carries its own status when it has one.

## Next: the release a clean machine installs is the release CI tested

CI is green on ubuntu, macos, and windows, and `.github/workflows/release.yml`
publishes on a tag push: it lints, checks that all six versioned manifests
carry the tag's version, zips the skill, and publishes the changelog section
as the notes.

1. **Verify two routes on a clean machine.** With no prior copy, install the
   Claude Code plugin route and the Codex route from `INSTALL.md`. The other
   routes wait for the users who file issues; `INSTALL.md` cites each agent's
   own docs, not a test.
   Partly done, against an isolated `HOME` rather than a clean machine. The
   skill-only route installs, lands all ten references, sets the flag, yields
   an 11,392 byte hook payload, and uninstalls cleanly, with the real home
   identical before and after. The Codex route pulls the published repo into
   `.agents/skills/black-iris`, references and scripts intact, `SKILL.md`
   byte-identical to `main`.
   What is left needs the `claude` CLI, which is absent from the machine this
   was attempted on: the plugin marketplace route, and the "Verify it works"
   step, which means invoking the skill in a live session and reading the
   reply.
   Done when those two pass on a machine with the CLI and no prior copy, and
   the result is a line in `.github/CHANGELOG.md` for whatever version carries
   it.

## Then: measured

Goal: retire "no benchmark is claimed" with numbers a skeptic can check.

1. **Run the eval.** The harness exists and every mode meets the case floor:
   `evals/cases.jsonl` has 66, `evals/rubric.md` says what the judge may see,
   `evals/run.sh` collects one condition. What is left is the run itself, with
   a judge from a different model family and a randomized order. Two things
   gate it: no judge from another family is available here, and `run.sh`
   shells out to the `claude` CLI, which is not installed on the machine this
   was attempted on.
   Done when `evals/RESULTS.md` carries the model, date, n, and every
   failed case by name. A zero-failure file triggers the harness audit the
   eval doc requires, not a celebration.
2. **Point the claim at the result.** Edit the "Not measured" bullet in
   `PRODUCT.md` to cite `evals/RESULTS.md` with its n and judge family.
   Done when `PRODUCT.md` makes no claim `evals/RESULTS.md` does not
   support.

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
