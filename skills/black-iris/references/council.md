# Council: five advisors, anonymous peer review, one verdict

One model, one answer, and no way to tell whether it was the good answer or
the mid one. This mode runs a decision through five advisors who think from
different angles and never see each other, has them review each other's work
without names, and ends with a chairman who commits to a verdict. It follows
Andrej Karpathy's LLM Council, with five thinking lenses inside one model
standing in for five models.

Ideate and Council are neighbors. Ideate makes options for an open question.
Council judges a decision that already has options and stakes. An ask with no
options yet is an Ideate ask; offer it, or run Ideate first and Council on its
shortlist.

## When

This costs about 11 Agent calls and one to three minutes, so it runs for
decisions where being wrong is expensive.

**Always run it** on "council this", "run the council", "war room this",
"pressure-test this", "stress-test this", "debate this", or
`/black-iris council`. The user opted in; do not second-guess.

**Run it when the ask has all three:** a real decision or tradeoff ("should I
X or Y", "which option", "is this the right move", "I am torn between"),
stakes the user names or that are plain from context, and no single right
answer.

**Do not run it** for a factual question, a creation task ("write me a
tweet"), a processing task ("summarize this"), or a casual "should I" with
no tradeoff. "Should I use markdown for this" is not a council question.
Answer it.

If the user already knows the answer and wants a blessing, the council will
say things they do not want to hear. That is what it is for.

## Step 1: frame the question

Two things before any advisor runs, at most 30 seconds and three files.

**Gather context.** The question is the tip of something larger. Look for the
two or three files that let advisors give grounded advice instead of generic
takes: the project's `CLAUDE.md` or `AGENTS.md`, the store's
`memory/MEMORY.md` and any entry it points at that touches the decision, any
file the user named, and any earlier council transcript under
`~/.BLACK_IRIS_AGENTS/projects/<slug>/council/` so the same ground is not
re-run. Use Glob and short Reads. Stop at three files.

**Write the framed question.** One neutral prompt every advisor receives:

1. The decision, stated as the choice it is.
2. Context from the user's message.
3. Context from the files: stage, audience, constraints, past results,
   numbers.
4. What is at stake, and why the call matters now.

No opinion of yours goes in. No steering. If the question is too vague to
frame ("council this: my business"), ask exactly one clarifying question,
then proceed. Keep the framed question; the transcript needs it.

## Step 2: convene, five subagents in parallel

Spawn all five at once. Sequential spawning lets earlier answers bleed into
later ones and wastes the wall clock. Each advisor gets only its lens, the
framed question, and the instruction below. None sees another's output.

The five lenses, and the tensions they create:

- **The Contrarian.** Assumes the idea has a fatal flaw and hunts for it.
  What is wrong, what is missing, what fails first. Not a pessimist; the
  friend who asks the question you are avoiding.
- **The First Principles Thinker.** Ignores the surface question and asks
  what is being solved. Strips assumptions, rebuilds from the ground. The
  most useful output here is sometimes "you are asking the wrong question."
- **The Expansionist.** Hunts upside everyone else missed. What could be
  bigger, what adjacent opening is hiding, what is undervalued. Risk is the
  Contrarian's job, not this one's.
- **The Outsider.** Has no context about the user, the field, or the history,
  and answers only what is on the page. Experts carry blind spots; the
  Outsider catches what is obvious to the user and opaque to everyone else.
- **The Executor.** Cares about one thing: can this be done, and what is the
  fastest path. What do you do Monday morning. A brilliant idea with no first
  step gets called out.

Contrarian against Expansionist is downside against upside. First Principles
against Executor is rethink everything against just do it. The Outsider sits
between them and keeps the rest honest.

Advisor prompt, filled per lens:

```
You are the <lens name> on a council.

Your thinking style: <lens description above>

A user brought this decision to the council:

---
<framed question>
---

Respond from your angle only. Be direct and specific. Do not hedge, do not
balance; the other advisors cover what you leave out. If you see a fatal
flaw, say it. If you see a large upside, say it.

150 to 300 words. No preamble. Start with your analysis.
```

## Step 3: peer review, five more subagents in parallel

This step is what makes the council more than asking five times.

Collect the five responses. Label them Response A through E in a random
order, so no reviewer can map a letter to a lens and no letter gets the
first-position advantage. Spawn five reviewers, one per lens, each seeing all
five anonymized responses:

```
You are reviewing the output of a council. Five advisors answered this
decision independently:

---
<framed question>
---

Response A:
<text>

Response B:
<text>

Response C:
<text>

Response D:
<text>

Response E:
<text>

Answer three questions. Refer to responses by letter. Be specific.

1. Which response is strongest, and why? Pick one.
2. Which response has the largest blind spot, and what is it missing?
3. What did all five miss that the council should weigh?

Under 200 words.
```

## Step 4: the chairman

One final subagent gets everything: the framed question, the five responses
with their lens names restored, and the five reviews. It writes the verdict.
The chairman may side with one dissenter against four if the dissenter's
reasoning is stronger, and says so.

```
You are the chairman of a council. Synthesize five advisors and their peer
reviews into one verdict.

The decision:
---
<framed question>
---

ADVISOR RESPONSES

The Contrarian:
<text>

The First Principles Thinker:
<text>

The Expansionist:
<text>

The Outsider:
<text>

The Executor:
<text>

PEER REVIEWS
<all five>

Write the verdict in exactly this structure:

## Where the council agrees
Points several advisors reached independently. High-confidence signals.

## Where the council clashes
Real disagreements, both sides stated, and why reasonable advisors split.

## Blind spots the council caught
What surfaced only in peer review: things one advisor missed and another
flagged.

## The recommendation
One clear answer with its reasoning. Not "it depends". Not "consider both".

## The one thing to do first
A single concrete step. Not a list.

Be direct. Do not hedge. The user came for the clarity one perspective
cannot give.
```

## Step 5: present in chat

Line one is the recommendation in one sentence, because Shape rule 1 outranks
the section order. Then the five sections as the chairman wrote them, under
a heading that names the topic:

```
Council verdict on <topic>. Recommendation: <one sentence>.

### Where the council agrees
### Where the council clashes
### Blind spots the council caught
### The recommendation
### The one thing to do first
```

Bullets inside sections. No HTML report, no file, unless the user asks. Keep
every number and condition the advisors used; a rounded verdict is a wrong
verdict.

## Step 6: transcript, only on request

If the user asks, or says the decision is one they will revisit, write the
framed question, the five responses with lens names, the five reviews, and
the verdict to `~/.BLACK_IRIS_AGENTS/projects/<slug>/council/<date>-<topic>.md`.
Never into the repo.

## Rules that do not bend

- All five advisors run in parallel and isolated. Five sequential answers in
  one context is one wide answer wearing five hats.
- Reviews are anonymized and shuffled. Named responses get judged by lens
  reputation instead of merit.
- The chairman commits. "It depends" is a refusal to do the job.
- Trivial questions get a plain answer, not a council.
- Cost is disclosed once, up front, when the mode fires without an explicit
  trigger: "About 11 Agent calls and a couple of minutes; say skip for a
  direct answer."
