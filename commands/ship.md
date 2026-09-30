---
description: Commit message, PR body, or changelog entry
argument-hint: [commit | pr | changelog]
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

Run the black-iris Ship mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/ship.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no input, ask for it in one line.
