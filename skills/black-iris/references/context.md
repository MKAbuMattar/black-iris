# Context: where the data goes

The context window is a budget spent once. A byte a tool returns is charged
whether or not it was needed, it stays charged for the rest of the session,
and the model that spent it cannot get it back. Compaction is not a refund.
It is a lossy summary bought with the detail you were about to use.

This mode governs what enters the window. It says nothing about how the reply
reads, which is Shape's job. The two are independent, and a reply can be
correct on one and wrong on the other.

One rule sits under everything here: **name the answer you need before you
fetch the thing that contains it.** A read with no named target is how a
window fills with material nobody ever looks at.

## When

A task that analyzes, counts, filters, compares, searches, parses, or
transforms data. Logs, test output, a coverage report, a dependency tree, a
directory of sources, an API response, a page snapshot, a database dump.

Skip it when the artifact is small and the whole artifact is the answer. A
12-line config that the user asked to see is a read, not a processing job.
The discipline has to cost less than the window it saves.

## Derive, do not dump

1. **Name the target first.** Write the question as a value: the count, the
   matching lines, the one key, the diff between two numbers. If you cannot
   state what you are looking for, you are browsing, and browsing belongs in
   a script that prints its findings.
2. **One script beats N reads.** Counting functions across 40 files is one
   program that prints one number, never 40 reads and mental arithmetic. The
   model is better used as a code generator than as a data processor, and a
   script that is wrong is wrong visibly, where a misread is wrong silently.
3. **Print the value, not the container.** A script that ends by printing the
   whole file it just loaded has moved the dump, not removed it. Print the
   match, the count, the key, or a line range you named in advance.
4. **Bound every read you cannot justify whole.** Line ranges, head and tail,
   a grep with context. An unbounded read of an artifact you have not sized
   is a bet that it is small.
5. **Size before you fetch, when sizing is cheap.** A line count, a byte
   count, or a record count costs almost nothing and tells you whether the
   next call is safe. `wc -l` before `cat` is the whole habit.

## Think in code

The instinct to read data and reason over it in the reply is the expensive
one. Turn the question into a program whose output is the answer.

Before: read 47 files to find which export a symbol.
After: one command that prints the 3 filenames that do.

This holds for the obvious cases (counting, filtering, joining, diffing) and
for the ones that look like judgment. "Which of these tests are flaky" starts
as a script that groups failures by name and prints the ones that appear more
than once. Judgment is applied to the 6 lines that come back, not the 6000
that went in.

A script is also a claim you can re-run. A conclusion you reached by reading
is not.

## Sandbox tools, when they exist

Some harnesses have tools that run code or fetch data and keep the raw bytes
out of the conversation, returning only what the code printed. The
context-mode MCP server is one, with a `ctx_` tool family (`ctx_execute`,
`ctx_execute_file`, `ctx_search`, `ctx_index`, and others). It is a separate
third-party project under its own license, not a dependency of this skill.

The rules:

- **Probe, never assume.** Use such a tool only when you can see it in the
  session's tool list. Naming a tool that is not there wastes a turn and
  teaches the user the skill is broken.
- **Prefer it for bulk work when it is there.** That is what it is for.
- **Apply the same discipline when it is not.** Every rule above works with
  an ordinary shell and an ordinary file read. The tool makes the saving
  larger; it is not what makes the saving correct.
- **Say which you used.** One clause: "counted with a script over 40 files"
  or "read the 3 files directly". The user cannot see your tool calls the way
  you can.

## The cost you cannot see

- **Output you read back is charged twice.** When a tool writes its result
  somewhere and you then read that location, the bytes enter the window once
  as the result and once as the read. A full dump through such a path costs
  double what it looks like.
- **A failed call still costs.** A 40 KB error page is 40 KB. Size the target
  before retrying the same call a second and third time.
- **Retrieval is not free either.** A search that returns 30 candidate chunks
  to find one fact spent thirty chunks. Ask for fewer and narrower.
- **Your own output is charged.** A reply that pastes the log it just
  analyzed spends the window a second time on the way out.

## Anti-patterns

- Reading a directory to find out what is in it, when a listing answers it.
- Loading a file to check whether a string appears in it.
- Fetching a whole API response to read one field, twice, because the first
  fetch scrolled out of view.
- Pasting a tool's full output into the reply so the user can see you did the
  work. Report the finding and where it came from.
- Re-reading a file you already read this session because it is easier than
  scrolling. Note the fact the first time instead.

## Where this meets the other modes

- **Build.** Build rule 1 says read the whole flow the change touches. That
  is not in tension with this mode. Reading the code you are about to change
  is a bounded, named read with a clear target. Reading a corpus to compute
  a statistic is the thing this mode routes into a script.
- **Gates.** A `CHECK:` command should print a token, never a log. A gate
  whose check dumps its output into the window has spent the budget to prove
  one boolean. `EXPECT:` exists so the check can stay quiet.
- **Memory.** An episode records the command and the finding, not the output.
  A memory entry that pastes 200 lines of a log has stored the dump where it
  will be re-read by every future session that greps near it.
- **Review.** Review a diff, not the files the diff touches, unless a hunk is
  unreadable without its surroundings. Then read that function, not the file.

## Report

When the job was a processing job, one line at the end says how the answer
was derived and what it cost: the approach, the number of items processed,
and what actually entered the window. "Counted 1,240 test names with one
script; 14 lines came back." A reader who cannot tell whether you measured or
guessed has to assume you guessed.
