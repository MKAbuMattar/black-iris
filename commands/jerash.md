---
description: Rematch an answer you rejected against fresh challengers
argument-hint: [why the last answer was wrong]
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Agent
---

Run the black-iris Jerash mode. The reason the last answer was rejected: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/jerash.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no rejected answer in the conversation, ask for it in one line.
