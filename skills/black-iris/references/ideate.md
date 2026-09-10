# Ideate: isolated divergence, then a real opinion

The first three answers a model gives are the answers a senior engineer
gives in thirty seconds. Correct and forgettable. The interesting answers
live past number three. This mode walks there, in parallel, without the
branches seeing each other.

## Pre-flight

This costs about 10 Agent calls and 30 to 90 seconds, 5 to 10 times a single
answer. Breadth is cheap and a missed idea is expensive; that trade is the
whole reason this mode exists.

**Step 1.** If the user typed `/black-iris ideate`, "ideate", "brainstorm
this", or asked for the mode by name, skip to the loop. They opted in. Do not
second-guess.

**Step 2.** Otherwise, three questions. Any "no" aborts.

1. Open-ended? Would a senior engineer give several viable answers, or one
   canonical one?
2. High-stakes? Architecture, a public API surface, a real product name, a
   schema, a fuzzy bug with no known cause. A side project at 11pm is not.
3. Open phrasing? "quick", "standard", "canonical", "textbook", "just",
   "one-line" all mean the user wants the direct answer.

On abort, answer directly. Optionally add one sentence offering the mode.

## The loop

Two strict phases. The critic strangles the generator when they share a
context.

### Phase 1: diverge, no critic

1. Pick 5 of the 15 frames, always including at least one `wild`. Four
   tagged `code` or `design` plus the wild one for a code-shaped problem; a
   mix for product or strategy. Vary picks across runs.
2. Spawn 5 parallel Agent calls, one per frame. Each gets only the problem,
   the user's context, the frame's vantage prompt, and this instruction:

   > You are in DIVERGENT mode. You are a generator, not a critic. Generate
   > 6 short distinct ideas under this frame, one phrase or sentence each.
   > Do not evaluate, rank, or hedge. The first three obvious answers
   > everyone would give are banned. Push past them into the awkward middle.
   > Weird and absurd ideas are welcome; they seed better ones.
   > Output a JSON array only: `[{"text": "...", "rationale": "..."}]`.

3. **The isolation invariant.** Parallel and isolated. Never serialize.
   Never pass one branch's output to another. Branches that see each other
   anchor each other and the method collapses into one wider thought.

Before spawning, reread the problem statement itself for anchors: a framing
that already assumes the answer ("how do we cache this" assumes a cache). If
you find one, give the branches the neutral question underneath it. An anchor
is also the stack, tool, or architecture the sentence happens to name; treat
those as choices and hand the branches the job underneath. Keep what is
genuinely fixed: compliance, budget, protocol limits. Score fit against the
stated problem, so a de-anchored idea still answers the real constraints.

### Phase 2: focus, critic on

1. **Score** each idea 0 to 10 on novelty (distance from the default),
   viability (could it ship), fit (does it address the stated problem). Flag
   traps: attractive ideas with a hidden cost, false economy, scaling cliff,
   or premature abstraction. A trap gets a specific, actionable line ("solid
   for a prototype, breaks past 10k concurrent users"), not a dismissal. Also
   record one strength per idea, the most concrete thing it gets right that a
   rival does not. Weak ideas get one too.
2. **Cluster** into 3 to 6 groups by underlying angle, not surface keyword.
   Label by angle: "remove the server", "cache-shaped", "batched window".
3. **Deepen the top 3** by weighted score (novelty 0.35, viability 0.40, fit
   0.25), traps excluded. One Agent call each:

   > You are in FOCUS mode. Take one promising idea and connect dots. Sketch
   > how it works in 4 to 8 sentences. Name the load-bearing risk. Name the
   > first concrete step a builder would take. Then give 3 to 5 sub-ideas:
   > variations, hybrids, things this unlocks. JSON only.

   Give each deepen call the other two survivors as siblings and ask for at
   least one hybrid: the focus idea crossed with a sibling from a different
   cluster. The strongest result is often a crossing of two candidates.

## Frames

| Frame | Vantage prompt | Tags |
|---|---|---|
| **3am on-call** | You are woken when this breaks. What design means you do not get paged? | code, design |
| **competitor breaking it** | You are hostile. How would you exploit, fail, or sabotage the obvious solution? Invert each into an idea. | code, design |
| **inversion** | Ask the opposite. If the goal is X, how would you guarantee not X? Negate each answer back. | code, design, general |
| **remove the fixed thing** | Name what everyone treats as fixed (framework, database, request-response, network). It is gone. What is possible? | code, design, wild |
| **$0, one hour** | No money, no team, one hour. The crudest version that still does the load-bearing thing. | code, general |
| **infinite budget, ten years** | Infinite compute and engineers, a decade. The maximalist version. | design, wild |
| **logistics** | Queues, batching, just-in-time, hub-and-spoke, returns, last mile. Apply them literally. | code, design |
| **regulator** | You audit for compliance and failure. What must be provable, traceable, or refusable here? | design, general |
| **biology** | Transplant a mechanism: immune systems, plasticity, cell signaling, evolution. Force-fit it. | code, wild |
| **speedrunner** | Glitches, skips, out-of-bounds tricks. The abusive-but-legal path. | code, wild |
| **hardware engineer** | Latency, memory layout, physical limits. Re-ask this as a firmware problem: bus, cache, timing budget. | code, wild |
| **10-year-old** | Curious, never seen software. Naive, unencumbered approaches. Ignore convention. | general, wild |
| **game designer** | Loops, rewards, friction, save states, speedrun tricks. The user is a player. | design, general |
| **markets** | Buyers, sellers, market makers. What is the auction, the futures contract, the clearing house here? | design, wild |
| **ant colony** | No central planner. Many dumb agents, local rules, pheromone trails. How does it solve itself? | code, wild |

## Output shape

Structure is half the value. Render in this order, never as one wall.

1. **Verdict, then brief.** Line one names the recommended idea in one
   sentence. Then one or two lines: the problem, and any reframe used.
2. **Wide set.** The pool grouped by cluster, each idea one phrase with score
   chips `[N7 V8 F9]`.
3. **Converge.** A shortlist of 2 to 4 with one reason each. Mark the
   non-obvious-but-viable pick: the highest-novelty idea on the shortlist
   that still clears viability. Traps listed separately with their one-line
   reason.
4. **Focus.** The 3 deepened branches: sketch, load-bearing risk, first step,
   child ideas.
5. **Provocation.** One wildcard question that opens a direction if nothing
   landed.

Close by restating the recommendation with its first step. "Here are 20
ideas, you decide" is a cop-out.

## Anti-patterns

- **Convergence disguised as divergence.** Ten variations of one idea share
  one assumption. You decorated.
- **Weird with no convergence.** Thirty unsorted absurdities are as useless
  as one safe answer.
- **Refusing to commit.** Diverge wide, then take a position.
- **Faking the isolation.** Writing five branches sequentially in one context
  is one wider thought. Use the Agent tool.

## Calibration

Scale to stakes: "name this product" is 3 frames by 4 ideas; "position this
product" is 5 by 8. A single identifier is Name mode, not this one. Default 5 by 6. Stop diverging when new candidates repeat
the shape of existing ones. Do not pad to hit a number. For serious strategy
work, label the wild cards so they do not read as unserious. For open
brainstorming or play, let it run loose.
