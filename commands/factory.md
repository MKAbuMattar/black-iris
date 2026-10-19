---
description: Spec, build, review in parallel, and merge one feature
argument-hint: <feature> [--merge] | approve <ID> [answers]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Agent
---

Run the black-iris Factory mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/factory.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no feature in the input or the conversation, ask for it in one line.
