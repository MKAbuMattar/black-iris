---
description: Loop a task until every gate is met, acting only at high confidence
argument-hint: [--max N] <brief> | stop | status
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

Run the black-iris Dabke mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/dabke.md` and follow it.
2. `stop` or `status` in the input: run
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/black-iris/dabke/dabke.py"` with it and
   report the line it prints. Otherwise start the loop on the brief.
3. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
4. With no brief in the input or the conversation, ask for it in one line.
