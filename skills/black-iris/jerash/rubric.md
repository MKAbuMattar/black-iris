# Jerash rubric

The judge of every heat scores both entries against this page. `hippodrome.py`
reads the weights from the table below, adds up the totals, and advances the
higher one. Change a weight here and the script follows.

## Criteria

Each criterion is scored from 0 to 10.

| criterion | weight | the question |
|---|---|---|
| sound | 35 | Is it right? Claims, logic, code, and numbers you checked yourself hold up. |
| complete | 25 | Does it do everything the task text asks, and nothing the task forbids? |
| usable | 20 | Could the person who asked act on it now, without guessing at a step? |
| holds | 20 | After the critiques in this heat, is every point fixed or correctly answered? |

The total is the sum of score times weight, divided by 10, so it runs from 0
to 100.

## What the numbers mean

- **10**: you looked for a problem on this criterion and found none.
- **7**: small slips that would not change what the person does.
- **4**: one real problem the person would trip over.
- **1**: wrong at the root on this criterion.

Score each criterion on its own. A strong `sound` does not lift `usable`.

For `holds`: an unanswered critique that is right costs the most, a critique
answered with a wrong rebuttal costs the same, and a fix that broke something
new costs as much as the critique it fixed. With no critique in the heat,
score `holds` on the problems you found yourself.

## Broken

Mark an entry `broken` only for a flaw you confirmed that makes it unusable
for this task: code that cannot run, a false central claim, a hard limit the
task set and the entry breaks, or an answer to a different question. A broken
entry loses to any entry that is not broken, whatever the totals. Two broken
entries are decided by their totals.

## Ties

No heat is drawn. Equal totals go to the entry with fewer critiques still
standing, then to the higher `sound`. If those are equal too, the script
settles it with the run's seeded coin and records that it did.

## Not rewarded

- Length. A shorter entry that meets the task beats a longer one that meets
  it too.
- Claims about quality. "This robust solution" is not evidence; check it.
- A reply that says "fixed". Open the revised entry and look.
- The method. The judge never sees the lane cards and does not guess them.
