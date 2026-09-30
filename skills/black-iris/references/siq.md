# Siq: carry the session through compaction

Everything that reaches Petra passes through the Siq, a gorge a few metres
wide. Everything a long session knows has to pass through compaction the
same way. Compaction replaces the model's view with a summary; it keeps the
transcript on disk and the same session id. The built-in summary already
records intent, files, errors, every user message, pending tasks, and the
next step. It does not record why: the decisions and the options they beat,
the evidence that something works, and the corrections the user made. And it
lives only inside one transcript. Siq writes exactly those missing parts,
per chat and per project, and brings them back after compaction.

## The three moments

1. **The ask, at a Stop.** The Stop hook reads the context size from the
   transcript's own usage numbers. Past about 70 percent of the window
   (inferred per model; an earlier auto compaction of the same model moves
   the point earlier), it stops the turn once per compaction cycle and asks
   you to write the handoff. You still hold the whole session, so this is the
   moment the judgement is still yours to write.
2. **The read, after compaction.** SessionStart with `compact` or `resume`
   prints this chat's handoff, capped at 4096 bytes, with its full path.
3. **The fallback.** If compaction came mid-turn and no Stop asked, the same
   SessionStart prints an extract instead: the user's own asks from the last
   slice, the files changed, the last checks with pass or fail. It says the
   handoff was not written. Rewrite it from the extract before the next task.

A new chat on the same project gets one line at startup naming the newest
handoff. Read it only if the work continues.

## When asked, write the handoff

The file is `~/.BLACK_IRIS_AGENTS/projects/<slug>/handoffs/<session_id>.md`.
The hook names it and has already written the header and the Open gates
section from `GATES.md`. You fill three sections and leave the rest alone:

```markdown
## Decisions
- <what was chosen>. Rejected: <the option it beat>, because <why>.

## Verified
- `<command>`: <result that proves it>.

## Corrections
- "<the user's words, verbatim>". <what that changes from now on>.
```

Rules for the three sections:

- **Only what the summary lacks.** No task history, no file list, no next
  step: the summary has those. A line that restates the summary is cost with
  no return.
- **Decisions carry the loser.** A decision without the rejected option and
  the reason gets reopened by the next session.
- **Verified means a command and its result.** "Tests pass" is a claim;
  "`pytest -q`: 142 passed" is evidence. Nothing unverified goes here.
- **Corrections are verbatim.** The user's words, then what they change. A
  paraphrase loses the rule.
- **Names exactly as the code has them.** Paths, functions, flags, and ids
  copied, never described (Name mode).
- **The Cut list applies.** No filler, no dashes, no hedging adverbs
  (Deslop mode).
- **Merge, do not append.** The file may hold an earlier cycle. Keep what is
  still true, update what changed, delete what is superseded.
- **Under 4096 bytes, the whole file.** The read back is capped there; what
  does not fit is not read.

Then continue the task the hook interrupted.

## Enable it

Off by default. The most specific flag wins:

```bash
python3 <skill-dir>/siq/siq.py arm           # this chat only; the next Stop binds it
python3 <skill-dir>/siq/siq.py on --project  # every chat in this project
python3 <skill-dir>/siq/siq.py on            # every chat everywhere
python3 <skill-dir>/siq/siq.py off           # or: off --project
```

The hooks come with the plugin. A bare skill install has no hooks, so Siq
there is `/black-iris:siq` by hand: write the handoff now, in the format
above.

## Other commands

- `siq.py meter <transcript>`: fill, window, threshold, cycle, model.
- `siq.py extract <transcript>`: the fallback extract for the last slice.
- `siq.py prune`: keep the newest 20 handoffs for this project.

## Memory

Every handoff is an episodic record. Memory's harvest reads `handoffs/` and
promotes Decisions and Corrections that held across sessions into semantic
or procedural entries. Siq never writes to `memory/` itself.
