# Athar: follow the trace to the root

A Bedouin tracker reads athar, the marks a camel leaves in the sand, back to
where it went. A bug leaves marks the same way: an error, a wrong value, a
test that fails on one machine. Athar reads them back to the cause and fixes
it there, never where the symptom surfaced.

## When

"Debug this", "why is this failing", "find the root cause", a bug that came
back after a fix, a flaky test, or Dabke handing over after two
investigations on one gate did not reach High confidence. A typo with an
obvious line is not an Athar job; fix it.

## The one rule

**No fix before a repro.** A repro is a command that shows the failure,
run this session, with its output read in full. A fix without one is a
guess you cannot check. If the bug will not reproduce, say so and add the
logging or assertion that will catch it next time, and stop there.

## The trail

1. **Reproduce.** Write the smallest command that shows the failure. Run it.
   Keep the exact output. Bulk output goes through Context mode.
2. **Shrink.** Cut the input, the test, and the setup until removing one more
   thing makes the failure go away. The smallest failing case usually names
   the cause on its own.
3. **Locate.** If it ever worked, let git find the change:
   `git bisect start <bad> <good> && git bisect run <repro>`. The repro must
   exit nonzero only on the failure you are chasing, or bisect lands on the
   wrong commit. If it never worked, walk backwards from the symptom: the
   value that is wrong, who set it, who called that.
4. **Hypothesize, one at a time.** Each hypothesis gets the test that would
   kill it before you run anything. Record it in `ATHAR.md` in the store:

   ```markdown
   - H1: the cache returns stale rows after a write
     KILL: write, read back without the cache, compare
     RESULT: killed, rows match; the cache is fine
   - H2: the ORM batches the update and the test reads before the flush
     KILL: flush explicitly before the read
     RESULT: holds, the test passes after an explicit flush
   ```

   Never test two hypotheses at once; a pass then proves neither.
5. **Fix at the root.** Grep every caller of the function the cause lives
   in. One guard in the shared path beats a patch in each caller, and
   patching only the path the report names leaves the others broken.
6. **Prove it.** Rerun the repro: it passes. Rerun the whole suite: nothing
   else broke. Keep the repro as a regression test beside the code.

## Traps

- **Three dead hypotheses means question the repro.** It may reproduce a
  different bug, or the environment may differ from the one that failed.
  Compare versions in the lockfile, the OS, the env vars, the data.
- **A pass that suppresses is not a fix.** Catching the exception, widening
  a tolerance, retrying until green, or skipping the flaky case hides the
  symptom and keeps the cause.
- **A flaky test is a bug with a hidden input.** Time, order, randomness,
  shared state, the network. Find the input, pin it, and the flake becomes
  a repro.
- **The last change is a suspect, not a verdict.** Bisect or the repro
  decides; recency does not.

## With the other modes

- **Dabke** hands over here when two investigations on a gate stall. The
  repro becomes that gate's `CHECK:`.
- **Gates** can own the proof: the repro and the full suite as two gates.
- **Memory.** The cause is a trap, written symptom first, so the next
  session finds it by the error it will see.
- **Ship.** The commit body names the root cause and the hypothesis that
  lost, because a reader will retry it.
- **Name.** When the cause was a misleading name, rename it in the same
  change, with every use found first.
