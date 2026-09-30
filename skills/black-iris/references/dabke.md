# Dabke: the loop that does not stop until done

A dabke line keeps moving, step after step, until the song ends. Dabke keeps
a task moving the same way: the Stop hook refuses the stop and hands you
the next step, until every gate in the ledger is met or abandoned. Between
steps, one rule decides whether you act or read first: confidence.

## Start

1. **Write the brief as a prompt for a stranger** (Prompt mode): the goal,
   the constraints, what done looks like. The hook replays it at every step,
   including after compaction, so it has to stand alone.
2. **Arm the loop**:
   `python3 <skill-dir>/dabke/dabke.py start "<brief>" [--max N]`. Default
   40 steps. The next stop binds it to this chat.
3. **Write `GATES.md`** in the store, per `references/gates.md`. The ledger
   is the only definition of done. If you skip it, the first step asks for
   it.

Without the plugin's hooks, run the same loop by hand: after each step,
reread the ledger and continue while a gate is unmet.

## Every step

1. Take the next unmet gate.
2. **Rate confidence.** High, or not.
3. Not High: **investigate**, then rate again.
4. High: act, then run that gate's `CHECK:`.
5. Append one line to the step log the hook names. The first stop creates
   it; work done before that goes in the gate's `EVIDENCE:` line instead:
   `step 7 | G2 | High | read: pytest log, src/io.py, uv.lock | changed: src/io.py | check: exit=0 matched "2 passed"`.

## Confidence is evidence, not a feeling

**High** needs all four. Missing any one means it is not High.

1. **You read the failure itself.** The full failing output, from a run
   this session. A summary of the error is not the error.
2. **You read the current file you will change.** This session, after the
   last edit to it. What you remember of a file is an old copy.
3. **Every outside fact is checked against the installed version.** An API,
   a flag, a default, a config key: confirmed in the lockfile's version of
   the source or its release notes, never from memory.
4. **You can name the check that proves it.** The gate's `CHECK:` or a
   narrower command. No check you can name means no High.

## Investigate before acting

Anything less than High reads first, in this order, and stops as soon as the
missing proof is found:

1. **The failing log.** Rerun and read all of it. Bulk output goes through
   Context mode: filter it with a script and read the lines that matter.
2. **The actual file.** Read the whole function and its callers, not the
   line the error names.
3. **The lockfile.** The version installed, never the version you expect.
4. **The upstream source at that version.** The installed package on disk,
   or the tag in the upstream repo.
5. **The release notes** between the version you assumed and the one
   installed. A renamed option or a changed default hides here.
6. **The context for the name.** Every use of the identifier, its tests, its
   config, per Name mode. Grep before renaming.

Two investigations on one gate without reaching High: act only if the
change is small, reversible, and its check runs at once. Otherwise add
`ABANDON: <id> <reason>` to the ledger and move to the next gate. A guess
is never logged as High.

## What ends the loop

- **Every gate met or abandoned.** The hook lets the stop through. Write the
  final report per `references/gates.md`: rerun every gate, measured counts,
  and "HANDOFF REQUIRED" in line one if any gate was abandoned.
- **The step budget.** The last step asks for that report with the unmet ids.
- **A stall.** A stop with nothing changed in the ledger or the log gets one
  warning; a second ends the loop. Progress, an `ABANDON:` line, or one
  blocking question to the user are the three ways past a warning.
- **The user.** An interrupt fires no Stop hook, but the loop is still on
  for the next reply. When the user says stop, or changes direction, run
  `dabke.py stop` before anything else. A user message outranks the loop.

Never ask the user a question you can answer by investigating. Never report
done while the hook is still handing you steps.

## With the other modes

- **Gates** owns done. Dabke only keeps you walking toward it.
- **Siq** carries the loop through compaction. The loop's state is on disk
  and every step restates the brief, so a compacted session keeps its
  place. Write the Siq handoff when it asks; the log line for that step is
  "siq handoff".
- **Memory.** When an investigation changed the plan (the lockfile had a
  different version, the release notes renamed a flag), that is a trap:
  write the episode, symptom first. At the end, harvest.
- **Ship.** Commit per met gate only when the user allowed commits, with the
  message per `references/ship.md`. Never push from inside the loop unless
  the user asked.
- **Deslop.** The log, the ledger, and the final report follow the Cut list.
