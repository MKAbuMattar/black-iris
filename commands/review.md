---
description: Five ranked findings on someone else's diff
argument-hint: [PR number, branch, or path]
disable-model-invocation: true
allowed-tools: Read, Grep, Glob
---

Run the black-iris Review mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/review.md` and follow it.
2. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
3. With no input, ask for it in one line.
