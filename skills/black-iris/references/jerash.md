# Jerash: beat the answer that was rejected

The hippodrome at Jerash still stages chariot races, and a race there has a
standing champion who must beat every challenger or give up the lane. This
mode works the same way. The answer the user rejected holds the title. Fresh
attempts challenge it one at a time, two blind judges decide each challenge,
and the run ends when the holder has defended twice in a row.

Ideate makes options for an open question. Council judges a decision that has
options. Jerash starts from a concrete answer that already failed and asks
what beats it. With no failed answer there is nothing to race against: say so
and point at Ideate.

## When

Only when typed: `/black-iris:jerash`, `/black-iris jerash`, or the user names
the mode. When the user says "try again", "bad answer", or "that is wrong"
without naming it, answer normally and add one closing line offering it with
its cost: "For a rematch against this answer: `/black-iris:jerash`, at most 18
Agent calls." Never spawn anything on those phrases.

## Step 1: the incumbent and the reason

1. **The incumbent** is the answer the user rejected. Take it from the
   conversation, word for word. If there is none in this session, ask for it
   pasted or as a path. Do not reconstruct it from memory.
2. **The reason** is why it was rejected, in the user's words. If the user has
   not said, ask exactly one question: "What was wrong with it?" The run does
   not start without a reason. A rematch with no reason optimizes against the
   same judgment that produced the bad answer.
3. **The task** is what the incumbent was answering: the request, every
   constraint the user stated, the files or data it depends on, given as
   absolute paths. A challenger sees nothing but what you write here, so write
   it for a stranger. Add no requirement the user never gave, and no view of
   your own about the right answer.

Save all three in the run folder before anything else:

```bash
P=${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}
R=~/.BLACK_IRIS_AGENTS/projects/$(printf '%s' "$P" | tr '/' '-')/jerash/$(date +%Y%m%d-%H%M%S)
mkdir -p "$R/entries"
```

`$R/task.md`, `$R/reason.md`, `$R/entries/00-incumbent.md`. The ledger is
`$R/ledger.md`. Only you write the ledger. Nothing goes in the repo or `/tmp`.

## Step 2: the cost, once

Each challenge is three Agent calls: one challenger, two judges. The default
cap is 6 challengers, so at most 18 calls, and the run usually stops sooner.
The user may raise the cap to 10, which is 30 calls. State the maximum and the
stop rule in one line, then start.

## Step 3: the ledger

Write the header, then one line per challenge as it happens:

```markdown
# Jerash run <run id>
Holder: 00-incumbent
Cap: 6    Defenses in a row: 0

- [ ] C1  frame: <frame>  vs <holder>  judge-1: <X|Y>  judge-2: <X|Y>  holder after: <id>
```

Read the ledger before every challenge and update it after. A line is checked
only when both verdicts are recorded. After compaction, reread the ledger and
continue from the first unchecked line. The ledger holds ids and verdicts,
never the texts; the texts live in `entries/`, and you do not read them during
the run.

## Step 4: one challenge

**The challenger.** Pick the next frame from the frame table in
`references/ideate.md`, a different one each challenge, at least one tagged
`wild` among the first three. Spawn one Agent with this brief:

```
The file <R>/task.md is a task. The answer at <R>/entries/<holder>.md was
given for it and fell short. The person who asked said why, in
<R>/reason.md. Write a better answer.

Work from this vantage: <frame name>. <frame vantage prompt>

Fix what the reason names first. Keep everything the task requires. Start
from the vantage, not from the old text: editing it line by line is not the
job, and a new answer that shares its mistake loses. You cannot ask anything:
where the task is unclear, take the most reasonable reading and state it in
one line at the top. If the task is about code, give the exact change as a
diff or full files; do not edit the user's project.

Write only the answer, for the person who asked, to
<R>/entries/<nn>-<frame-slug>.md. Say nothing about this process. Reply with
one line: WROTE <path>.
```

**The judges.** Two Agents, spawned together, isolated. Each sees the two
answers under the labels X and Y. Judge 1 gets the holder as X and the
challenger as Y; judge 2 gets them the other way round, which cancels the pull
of going first. Neither is told which answer is the holder.

```
Two answers to the same task follow. Task: <R>/task.md. The person who asked
rejected an earlier answer for this reason: <R>/reason.md.

Answer X: <path>
Answer Y: <path>

Read both in full before you decide. Decide in this order, and stop at the
first question that separates them:

1. Which one fixes what the reason names?
2. Which one is correct? Check claims, code, and numbers yourself; an answer
   that says it is right is not evidence.
3. Which one meets more of what the task requires?
4. Which one the person could act on now without guessing?

Length and confident wording earn nothing. If the task is code and running it
settles the question, run it only inside <R>/scratch/. Change no other file.

Reply with exactly two lines:
PICK X|Y
WHY <the one difference that decided it>
```

**The call.** Map both picks back to holder or challenger. The challenger takes
the title only when both judges picked it. A split, or two picks for the
holder, is a defense. Record the line, set the new holder, and reset or
increment "Defenses in a row".

If a call returns nothing, run it once more. A challenger that fails twice
forfeits and the holder defends. A judge that fails twice gets a third fresh
run; never decide a challenge yourself.

## Step 5: stop

Stop when the holder has defended twice in a row, or when the cap is reached.

Then read the holder's file, the only entry you read, and reply:

1. **Line one: the verdict.** "The rejected answer held" or "A new answer took
   the title from <frame>, after <n> challenges".
2. **The holder's answer**, in full.
3. **What changed** against the rejected answer: the reason the user gave and
   how the holder answers it, from the judges' WHY lines.
4. **The record**: challenges run, title changes, the ledger path.

If the rejected answer held against its first two challengers, that is the
finding: six calls say the candidates were not the problem. Say plainly that
the task or the reason probably is, and ask which.

If the holder changes files in the user's project, do not apply it. Ask.

## Rules that do not bend

- Every challenger and judge works blind and isolated. A challenger sees the
  task, the reason, and the current holder, never another challenger.
- The task file is the same bytes for everyone. Never add a hint to one call.
- You run the race. You never write an entry and never pick a winner.
- Only the ledger records state, and only you write it.
- The user says stop: stop. The ledger resumes it later.
