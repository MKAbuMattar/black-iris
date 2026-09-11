# Working on black-iris

This repo is a prompt-only skill. The product is `skills/black-iris/SKILL.md`
and the ten files under `skills/black-iris/references/`. Everything else is
packaging.

## Before you edit

1. Read `skills/black-iris/SKILL.md` in full. It is about 12 KB by design.
2. Read the one reference file your change touches, not all ten.
3. Invoke the skill on yourself. Its Shape, Build, and Cut list rules apply to
   every reply and every file you write here.

## Hard constraints

- `SKILL.md` stays at or under 16,000 bytes, about 4,000 tokens, and no prose
  line runs past 100 characters. Table rows and indented blocks are exempt
  from the length cap. The budget was a 200-line cap until it started buying
  compression that cost clarity: prose folded into 156-character lines to pay
  for a table row. Bytes measure what the window actually pays; the length cap
  stops a long line from gaming the budget. Mode detail belongs in a reference
  file with a row in the routing table; `references/evals.md` is the one
  maintainer document there and is reached from the closing line instead.
- Every file under `skills/` and `hooks/` is pure ASCII. No em or en dash, no
  curly quote. The lint fails otherwise.
- Deslop pattern numbers are stable ids. Never renumber or reuse one; a
  removed pattern leaves a gap.
- Per-project files go under `~/.BLACK_IRIS_AGENTS/projects/<slug>/`. Never
  write to `~/.claude` or `/tmp` from the skill or the hook.
- The hook stays fail-open: it exits 0 on every path and runs only when the
  flag file exists.
- No AI attribution anywhere: no Co-Authored-By naming a model, no "Generated
  with", in commits, PRs, or docs. This is Cut list rule 10 and it applies to
  this repo's own history.

## After you edit

```bash
python3 skills/black-iris/scripts/universal/check.py   # lint, exit 0 or fail
bash skills/black-iris/scripts/linux/check.sh          # same checks in bash
```

Both must print `clean`. If you changed a count the lint asserts (Shape 10,
Build 5, Cut list 10, 15 ideate frames), update the assertion in all three
check scripts: `universal/check.py`, `linux/check.sh`, `windows/check.ps1`.

If you changed the hook, dry-run it with a scratch home:

```bash
H=$(mktemp -d); mkdir -p "$H/.BLACK_IRIS_AGENTS"; touch "$H/.BLACK_IRIS_AGENTS/always-on"
HOME=$H CLAUDE_PLUGIN_ROOT=$PWD sh hooks/reinject.sh | head -5
```

## Keep in sync

- A change to the skill's description goes to `SKILL.md` only. The root
  manifests carry a one-line summary, not the trigger list.
- A new mode needs: a routing-table row, a reference file named in that row,
  and a handoff paragraph only if the mode has a hard rule the model must
  know before reading the file.
- A new agent install route goes in `docs/en/INSTALL.md` with install, invoke,
  verify, update, uninstall, and where the always-on snippet goes, and its
  update command goes in `docs/en/UPDATE.md`. Cite the agent's own docs; do not
  infer commands.
- Docs live under `docs/<lang>/`, one of `en`, `es`, `ar`. Only `README.md`,
  `AGENTS.md`, `CLAUDE.md` and `GEMINI.md` stay at the root, because GitHub and
  the agents read them there and `gemini-extension.json` names `GEMINI.md`
  directly. A link from inside `docs/` to a repo-root path needs `../../`.

## Releases

Write the entries under a `## Unreleased` heading in `.github/CHANGELOG.md`
as the work happens, in the language of someone deciding whether to upgrade.
Then push a branch named for the version:

```bash
git switch -c release/v1.2.0 && git push -u origin release/v1.2.0
```

`release-branch.yml` bumps every versioned manifest, renames the `Unreleased`
heading to `## 1.2.0 - <date>`, and opens the pull request. Merge it and
`release.yml` tags `v1.2.0` and publishes, using the changelog section as the
release body. An `rc/v1.2.0-rc.1` branch publishes as a prerelease.

The merge has to be a human push. A push made with `GITHUB_TOKEN` never
starts another workflow run, so nothing publishes if a job pushes to main for
you. For the same reason the release pull request gets no `check.yml` run,
which is why `release-branch.yml` lints and checks readiness itself before it
commits anything.

Nothing here invents changelog prose. `prepare-release.py` refuses when there
is no `Unreleased` heading and no section for the version, and it decides
every refusal before writing a byte. A hand-pushed `v*` tag still works as
the escape hatch. The manifest list is discovered by
`.github/scripts/manifests.py`, so a new manifest is enrolled in the bump and
the check when it gains a `version` field.

## Branch and tag rules

Two rulesets, both active. `main` blocks direct pushes, force pushes, deletion
and merge commits, and needs a pull request whose five `check.yml` jobs pass:
`lint (ubuntu-latest)`, `lint (macos-latest)`, `windows`, `evals`,
`release-ready`. Reviews required: zero, so a solo maintainer merges their own
pull request. `refs/tags/v*` blocks deletion and force-push, so a published
release tag cannot move.

One thing keeps the release flow working and is easy to break. A push made with
`GITHUB_TOKEN` never starts a workflow, so `release-branch.yml`'s bump commit
gets no `push` run. Those five checks reach it only through the `pull_request`
event, which fires because a **person** opens the release pull request. If the
repository setting "Allow GitHub Actions to create and approve pull requests"
is ever turned on and the workflow opens that pull request itself, no checks
will run on it and it will never be mergeable.

`publish` is deliberately not a required check. It belongs to `release.yml` and
runs on `main` after the merge, so requiring it would wait on a job that cannot
start until the merge it is blocking has happened.

## Commits and PRs

Commit subject `type(scope): subject`, imperative, lowercase, 72 characters.
A body when the why is not in the diff, when you rejected an approach a reader
would retry, or when it breaks something. The PR template asks four questions;
answer them and stop. Full contract: `skills/black-iris/references/ship.md`.
