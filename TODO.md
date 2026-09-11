# TODO

Where each roadmap item stands. `ROADMAP.md` says what an item is and what
done means; this file says nothing but status, so the two cannot drift into
saying different things about the same work.

One item is worked at a time: pull request, merge, release, then the next.

## In flight

Nothing. Every unblocked item is done.

## Ready

- [ ] Verify two install routes on a clean machine. Two of the three parts are
      done, against an isolated `HOME` rather than a clean machine:
      - Skill-only Claude Code route (`scripts/universal/install.py`): installs,
        lands all 10 references, sets the flag, the hook then emits 11,392
        bytes, and `--uninstall` removes both. The real home was byte-identical
        before and after. On Windows it correctly falls back to a copy and says
        why, since a symlink needs Developer Mode.
      - Codex route (`npx skills add -a codex`): pulls the published repo into
        `.agents/skills/black-iris`, all 10 references and all 4 script
        directories present, `SKILL.md` byte-identical to `main`.
      - Not done: the Claude Code **plugin marketplace** route, which writes to
        the real Claude Code config and cannot be isolated the same way. And
        neither install was exercised by invoking the skill in a live session,
        which is what the "Verify it works" step in `INSTALL.md` actually asks
        for. That last part needs a person or a clean machine.

## Blocked

- [ ] Run the eval. Needs a pinned model and a judge from a different model
      family. A judge from the same family shares the habits being measured,
      and the skill grading itself is not a result. `evals/rubric.md` says so.
- [ ] Point the claim at the result. Blocked behind the run above. Until it
      happens `PRODUCT.md` keeps saying no benchmark is claimed, which is
      true and should stay true.

## Waiting on a trigger

The four "On request" items in `ROADMAP.md`. Each waits for a user to ask.
Building one unasked contradicts the rule that put it there.

## Done

- [x] A Context mode, released in 1.2.0.
- [x] Episodic, semantic, and procedural memory, released in 1.1.0.
- [x] Branch-driven releases: push `release/vX.Y.Z`, merge, publish.
- [x] Release-readiness checked on every pull request.
- [x] The always-on hook injects the router only, 94 KB down to 11 KB.
- [x] Every eval mode meets the case floor of 8.
- [x] Roadmap headings stopped encoding versions; TODO.md added.
- [x] Install routes for Oh My Pi, Kiro, and Copilot in JetBrains.
- [x] An opt-in Stop hook that refuses a stop while gates are unmet.
