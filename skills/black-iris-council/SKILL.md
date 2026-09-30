---
name: black-iris-council
description: Five advisors, anonymous review, one verdict. black-iris mode, typed only.
license: GPL-2.0-only
disable-model-invocation: true
allowed-tools: [Read, Grep, Glob, Agent]
metadata: {author: MKAbuMattar, part-of: black-iris, logo: ../black-iris/assets/modes/council.svg}
---

# black-iris: Council

One mode of black-iris, without loading the other fifteen.

1. Read `../black-iris/references/council.md` and follow it for this request.
2. Apply the Cut list and the Pre-send check from `../black-iris/SKILL.md` to
   everything you write, including commits and comments.
3. Read nothing else from black-iris unless that reference points at it.

Paths are relative to this skill's folder. If `../black-iris/` is missing,
this folder was installed alone: say so in one line and point the user at
the whole set, which `npx skills add MKAbuMattar/black-iris` or the plugin
installs together.

Text after the command is the input for this mode. With no input, ask for it
in one line.
