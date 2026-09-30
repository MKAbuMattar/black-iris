---
name: black-iris-siq
description: Write the handoff before compaction and read it back after. black-iris mode, typed only.
license: GPL-2.0-only
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Bash]
metadata: {author: MKAbuMattar, part-of: black-iris, logo: ../black-iris/assets/modes/siq.svg}
---

# black-iris: Siq

One mode of black-iris, without loading the other fifteen.

1. Read `../black-iris/references/siq.md` and follow it for this request.
2. Apply the Cut list and the Pre-send check from `../black-iris/SKILL.md` to
   everything you write, including commits and comments.
3. Read nothing else from black-iris unless that reference points at it.

Paths are relative to this skill's folder. If `../black-iris/` is missing,
this folder was installed alone: say so in one line and point the user at
the whole set, which `npx skills add MKAbuMattar/black-iris` or the plugin
installs together.

Text after the command is the task and its flags. With no task in the input
or the conversation, ask for it in one line.
