---
description: Write this chat's handoff now, or arm Siq for it
argument-hint: [arm | on --project | off]
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Bash
---

Run the black-iris Siq mode on this input: $ARGUMENTS

1. Read `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/references/siq.md` and follow it.
2. `arm`, `on`, or `off` in the input: run
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/black-iris/siq/siq.py"` with it and
   report the one line it prints. Otherwise write the handoff now.
3. Apply the Cut list and the Pre-send check from
   `${CLAUDE_PLUGIN_ROOT}/skills/black-iris/SKILL.md` to everything you write.
