---
description: Trace a bug to its root cause, repro first
argument-hint: <the failure: error, test name, or what goes wrong>
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Run the black-iris Athar mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/athar.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no failure in the input or the conversation, ask for it in one line.
