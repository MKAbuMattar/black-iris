---
description: Race 100 entrants for the best answer, or --quick 16
argument-hint: [--quick | --field N] [--seed S] <task, or why the last answer was wrong>
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Agent
---

Run the black-iris Jerash mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/jerash.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no task in the input or the conversation, ask for it in one line.
