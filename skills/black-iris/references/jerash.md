# Jerash: a hundred entrants race for one answer

The hippodrome at Jerash still stages chariot races. This mode runs one over a
task. A field of entrants, 100 by default, gets the same task and a different
lane card each. They write entries, then race in heats: two entrants critique
each other, answer the critiques and revise, and a judge scores the pair on
the rubric. The winner goes through to the next round until one entry holds
the lane. When the user rejected an earlier answer, the last entry meets that
answer in a blind final.

You run the race. You never write an entry, never critique, never judge, and
never pick a winner.

Ideate makes options for an open question and Council judges a decision.
Jerash is for when an answer came back wrong or weak and the user wants the
strongest one a field can produce.

## The files

Everything lives in `jerash/` beside this skill's `SKILL.md`:

- `hippodrome.py`, the race state. Every command below is
  `python3 <skill-dir>/jerash/hippodrome.py <command>`, written `HIPPO` here.
- `lanes.json`, three decks of lane cards, each card named for a place in
  Jordan. No two entrants draw the same full card.
- `rubric.md`, what the judges score and the weights. The script reads the
  weights from it.
- `briefs.md`, the brief templates the script fills for every subagent.

The race lives in the store, `~/.BLACK_IRIS_AGENTS/projects/<slug>/jerash/`,
never in the repo or `/tmp`. Each run gets its own folder and `jerash/LATEST`
names the current one.

## Step 1: size, cost, and consent

Read the size from the request, and treat everything else as the task:

| ask | field |
|---|---|
| nothing said | 100 entrants |
| `--quick` | 16 entrants |
| `--field N` | N entrants, 2 to 1080 |
| `--seed S` | fixes the cards and the pairings |
| `--wave W` | subagents per wave, default 10; raise only if the user raised Claude Code's limit |

Run `HIPPO plan --field N` (add `--final` when there is a rejected answer). It
prints rounds, heats, Agent calls, and waves; 100 entrants is 595 calls in 70
waves.

- **Typed** (`/black-iris:jerash`, `/black-iris jerash`, or the user asked
  for a race): say the size and the call count in one line, then start.
- **Fired by frustration** ("try again", "bad answer", "that is wrong") and
  never named: ask once before spending anything. Offer the full race (100
  entrants, 595 calls), `--quick` (16 entrants, 91 calls), or an ordinary
  retry, and wait.

Subagents write into the store, which sits outside the project. Before the
first wave, tell the user to run `/add-dir ~/.BLACK_IRIS_AGENTS` and switch to
accept-edits mode for the run, or they will approve hundreds of files one by
one. Do not change their settings yourself.

## Step 2: the task file

This step decides the result. **Subagents cannot see this conversation.**
Every entrant and judge knows only what the task file says, so write it for a
stranger:

- The request, in the user's own words where you can.
- Every requirement and constraint the user stated anywhere: audience,
  length, format, stack, what must not change.
- What a stranger would need: absolute paths of the files that matter, the
  data, the conventions in play.
- What done looks like, if the user said.

Add no requirement the user never gave and no view of your own about the
right answer; a hint in the task file pushes every entrant the same way.

When there is a rejected answer, save it word for word, and save the user's
reason for rejecting it. Ask for the reason in one question if they have not
given it. The race refuses a rejected answer without one.

## Step 3: start the race

```bash
HIPPO init --task task.md --field 100 --rejected old.md --reason reason.md
```

Write those three files in the store first, then run `init`. Drop
`--rejected` and `--reason` when there is nothing to beat, and `--seed` for a
random one; the seed is recorded either way.

## Step 4: the loop

Always drive it with `HIPPO next`. It reads the state and prints the next
step and its command. Every phase that runs subagents works the same way:

1. `HIPPO briefs <phase>` writes one brief per job still to run and lists
   them in waves.
2. Launch one wave at a time: one message, one Agent call per brief in that
   wave, each with the prompt "Read <brief path> and follow it exactly. It is
   your whole brief." Wait for the whole wave before the next.
3. After the last wave, run `HIPPO next`. A missing output sends you back to
   the same phase and `briefs` lists only what is missing. Rerun those once.
   A job that fails twice gets the line `NO OUTPUT` written into each of its
   output files (`HIPPO pending <phase>` lists them) and the race moves on. A
   judge that fails twice gets a third, fresh run; never decide a heat
   yourself.

The order: **entry** once; then each round **critique**, **reply**,
**judge**, `HIPPO collect`, `HIPPO advance`; then **final** once when a
rejected answer exists, and `HIPPO collect`. `next` prints DONE at the end.

After each `advance`, give the user one line: "Round 3 closed: 13 of 100
still racing." Never paste entries, critiques, or verdicts into the chat.

## Step 5: the result

Run `HIPPO champion`, then read the champion's entry at the path it prints.
It is the only entry you read in the whole race. Reply with:

1. **Line one: the verdict.** Who holds the lane, and against the rejected
   answer, whether the champion or the old answer won the final.
2. **The winning entry**, in full.
3. **Why it won**: the heats it took and what it beat, from `champion`, and
   its lane card on one line.
4. **The race**: entrants, rounds, and the run folder.
5. **The final**, when there was one, honestly. If the rejected answer
   scored higher, say so and show both.

If the entry changes files in the user's project, do not apply it. Ask.

## Rules that do not bend

- Every subagent gets the task through its brief, byte for byte the same.
  Never add a hint to one call and never edit one brief.
- Do not read entries, critiques, or verdicts during the race. `next`,
  `status`, and `pending` are all you need.
- Compacted mid-race: run `HIPPO status`, then `HIPPO next`, and continue.
- Run every command from the same project, so the store resolves to the same
  race.
- Subagents write only inside the run folder. If one wrote elsewhere, tell
  the user.
- The user says stop: stop. `HIPPO next` resumes the race later.
