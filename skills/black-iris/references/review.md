# Review: someone else's diff

Findings, not rewrites. A person already decided to make this change. Your
job is to catch what will hurt them, not to reshape it into the diff you
would have written. A review that touches everything reads thorough and is
noise; the one real bug drowns in it.

## Process

1. **Read the whole diff before writing a finding.** A line that looks wrong
   alone is usually explained forty lines down.
2. **Read the commit message and PR body too.** They are part of the change.
   A correct diff under a subject that lies about it is a defect.
3. **Establish the change's own intent** from title, body, and diff. Every
   finding is measured against that intent, not against what you would have
   built.
4. **Collect, then rank** by the order below.
5. **Cut the tail.** Report what matters and say how many you dropped.

## What to flag, in order

1. **Correctness.** It does not do what it says. Wrong condition, off by one,
   unhandled null, unreachable branch, a test that passes for the wrong
   reason. A correctness finding names the file and line you read; a
   plausible name or a nearby file is not verification.
2. **Data loss and security.** Anything that deletes, overwrites, or exposes.
   A missing transaction boundary, a committed credential, an unbounded
   query, a permission check that moved.
3. **A name that will mislead.** A verb that lies, a boolean named for its
   false case, a half-landed rename. These cause future bugs rather than
   being one, which is why they outrank the rest.
4. **The commit message or PR body.** A subject that does not describe the
   change, a missing body where the why is not obvious, an AI attribution
   trailer, an unmarked breaking change.
5. **Slop in shipped text.** Comments, docstrings, error messages, and
   user-facing strings this diff introduced, by the Cut list.

## Not yours to flag

Every item here is how a review becomes an argument.

- **Style the linter owns.** If the tool is silent, the style is fine. Want
  the rule? Change the tool config in its own PR.
- **A convention the repo already uses.** You are reviewing a diff, not the
  codebase around it.
- **The author's voice** in prose that carries no tells. Plain is not wrong.
- **Anything outside the diff.** Pre-existing problems get a separate note at
  the end, marked pre-existing, never as a blocker.
- **The approach, once it works.** "I would have done this differently" is
  not a finding. If it is actually wrong, say why it fails; that makes it
  correctness.
- **Scope you wish were larger.** Asking for the follow-up in this PR is how
  a two-line fix becomes a two-week branch.

## Output

One line per finding, anchored to `file:line`.

```
src/auth.ts:42  correctness  refreshToken() returns before awaiting the
                             write, so a failed write reports success.
src/auth.ts:88  naming       isNotExpired reads as a double negative at both
                             call sites. isValid, or invert the check.
commit subject  ship         "fix: auth stuff" does not say what was fixed.
```

Then one line: what blocks the merge, what to fix now, what is a follow-up.

Rewrite code only when asked. A finding names the problem and the shape of
the fix. A patch nobody requested moves the decision away from the person who
owns the change.

## Severity

- **Blocking:** correctness, data loss, security, a lie in the subject.
- **Fix now:** a misleading name, a missing body on a non-obvious change, a
  tell in a shipped string.
- **Follow-up:** everything else. Say it once, let it go.

A clean diff gets one line saying so. Manufacturing a finding to look
diligent trains the author to skim your reviews, and that costs you the next
real bug. A review with no blocking findings says "no blockers" in line one,
because that is the only thing the author is waiting to read.

## Volume

Five findings, ranked. Past five, split into blocking and the rest, and say
what you dropped. Forty comments do not communicate forty problems. They
communicate that the reviewer had a list and the author now has a chore.
