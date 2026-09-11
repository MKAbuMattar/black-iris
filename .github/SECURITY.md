# Security

## What runs

black-iris is markdown plus three kinds of small scripts. Nothing here calls
the network.

- `hooks/reinject.sh` runs at Claude Code session start when the plugin is
  loaded and `~/.BLACK_IRIS_AGENTS/always-on` exists. It reads the skill
  file and the project's memory index, and prints them. It does not read the
  references.
  It exits 0 on every path and never writes.
- `hooks/gates-stop.sh` runs when Claude Code is about to stop, only when
  `~/.BLACK_IRIS_AGENTS/gates-stop` exists. It reads the project's `GATES.md`
  from the store and writes one empty marker file under the store's `tmp/` so
  it cannot block the same ledger state twice in a session. It exits 0 on
  every path but one: exit 2, which refuses the stop and prints the unmet gate
  ids to stderr. It touches nothing in your repo.
- `hooks/memory-stop.sh` runs when Claude Code is about to stop, only when
  `~/.BLACK_IRIS_AGENTS/memory-nudge` exists. It reads whether the project has
  uncommitted changes and whether the store holds a memory index, and writes
  one empty marker under the store's `tmp/` so it speaks at most once per
  session. It never blocks and always exits 0. It touches nothing in your repo.
- `skills/black-iris/scripts/*/install.*` create a symlink, junction, or copy
  under `~/.claude/skills` and may touch the flag file. `--uninstall` removes
  exactly those.
- `skills/black-iris/scripts/*/check.*` read the repo and print findings.

## What the model runs because of this skill

- **Gates.** The skill tells the model to write `CHECK:` shell lines into a
  ledger and run them. A ledger inherited from someone else is untrusted; the
  skill says to read every command before running it and never to let a
  ledger approve itself. Review ledgers you did not write.
- **Memory.** Entries are data, never instructions. The skill says so, and it
  runs a credential grep before finishing. The store under
  `~/.BLACK_IRIS_AGENTS/` is plain text on your disk; treat it like notes.
- **Permissions.** The skill pre-approves only Read, Grep, Glob, and Agent.
  Bash, Write, and Edit go through your harness's normal prompt.

## Reporting

Report a vulnerability privately through GitHub Security Advisories on this
repository. Do not open a public issue for it. You will get a reply within
seven days.

In scope: the hook or scripts doing something other than described above, a
skill instruction that leads a model to exfiltrate data or bypass a
permission prompt, a store path that escapes `~/.BLACK_IRIS_AGENTS/`.

Out of scope: the model ignoring a rule. That is a quality bug; open an issue.
