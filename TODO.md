# TODO

Where each roadmap item stands. `ROADMAP.md` says what an item is and what
done means; this file says nothing but status, so the two cannot drift into
saying different things about the same work.

One item is worked at a time: pull request, merge, release, then the next.

## In flight

Nothing. Every unblocked item is done.

## Ready

- [ ] Verify two install routes on a clean machine. Needs a machine with no
      prior copy of the skill.

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
