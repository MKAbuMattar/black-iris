---
name: black-iris-factory
description: Spec, build, review in parallel, and merge one feature, with a human on business calls. black-iris mode, typed only.
license: GPL-2.0-only
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob, Agent]
metadata: {author: MKAbuMattar, part-of: black-iris, logo: ../black-iris/assets/modes/factory.svg}
---

# black-iris: Factory

One mode of black-iris, without loading the other modes.

1. Read `../black-iris/references/factory.md` and follow it for this request.
2. Apply the Cut list and the Pre-send check from `../black-iris/SKILL.md` to
   everything you write, including commits and comments.
3. Read nothing else from black-iris unless that reference points at it.

Paths are relative to this skill's folder. If `../black-iris/` is missing,
this folder was installed alone: say so in one line and point the user at
the whole set, which `npx skills add MKAbuMattar/black-iris` or the plugin
installs together.

Text after the command is the feature and its flags, or `approve <ID>` with
answers. With no feature in the input or the conversation, ask for it in one
line.
