# Ship: commit messages, pull requests, changelogs

A diff answers what. The text beside it answers why, to a reader who has lost
every bit of context you hold right now. The test for every rule: someone
lands on this line from `git blame` in six months and has to decide whether
they can change it. Does what you wrote help?

## Subject

`type(scope): subject`. Scope optional. Nothing else on line one.

Types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`,
`chore`. Pick by what the change does to the codebase, not which files it
touched. Moving a function is `refactor` even when the diff is all deletions.

1. **Imperative.** "add", never "added" or "adds". It completes "this commit
   will ___".
2. **Lowercase after the colon, no trailing period.** A label, not a
   sentence.
3. **72 characters, shorter is better.** `git log --oneline` truncates.
4. **What changed, not what you did.** The author is already recorded.
5. **One concern.** A subject that needs "and" is two commits.

Bad: `fix(auth): fixed a bug where the token was not refreshed properly.`
Good: `fix(auth): refresh the token before it expires, not after`

Bad: `feat: update UserService.ts and auth.ts`
Good: `feat(auth): accept magic links as a second sign-in path`

The file list is in the diff. A subject that restates it says nothing.

## Body

Skip it when the subject is the whole truth. Write one when any holds:

1. The why is not obvious from the diff.
2. You rejected an approach a reader would otherwise try again.
3. The change works around something outside this repo.
4. It breaks something or changes behavior anyone depends on.
5. It fixes a bug whose symptom differs from its cause.

Blank line after the subject. Wrap at 72. Explain the why and the constraint;
the diff already shows the what. Name the rejected alternative; that is the
single most valuable line a body carries. Lead a bug fix with the symptom,
because a future reader searches by what they see.

```
fix(cache): clear the index when invalidating a key

Stale reads survived invalidation because the key was dropped from the
store but left in the index, so the next lookup found it and returned a
tombstone.

Clearing both in one call rather than sweeping the index on read: the
sweep was slower on large stores and only masked the bug.
```

## Breaking changes

Mark them twice, for two different readers. `type(scope)!: subject` catches
the eye in the log. A `BREAKING CHANGE:` footer is what release tooling
parses, and it states what a caller must do to migrate.

## What never appears

1. **AI attribution.** No `Co-Authored-By` naming a model, no "Generated
   with", no robot footer. When a harness adds one by default, turn that
   setting off once (Claude Code: `includeCoAuthoredBy: false`) rather than
   fighting it per commit. A commit message ends with its body.
2. **`wip`, `misc`, `stuff`, `fixes`, `updates`.** Unfinished work still has
   a subject that says what the commit does.
3. **A ticket number alone.** `fix: JIRA-4821` sends the reader out of the
   repo to learn anything. Ticket in a footer, meaning in the subject.
4. **An apology or a hedge.** "hopefully fixes", "attempt at". Say what you
   verified instead.

## Pull requests

The title follows the subject rules; it becomes the merge commit and the
release note. The body answers four questions in order and stops:

1. What changed, in two or three plain sentences.
2. Why, including the alternative you rejected.
3. How to verify, as commands a reviewer can run. Not "tested locally".
4. What is out of scope, when the diff visibly leaves something unfinished.

No screenshot gallery unless the change is visual. No checkbox list nobody
reads. No summary of the file list. A single-commit PR whose body already
answers all four reuses that body.

## Changelogs

Written for someone deciding whether to upgrade, in their language.

Bad: `refactor UserRepository to use the new connection pool`
Good: `queries no longer hang when the database restarts`

An internal refactor with no observable effect gets no entry. Group by
Added, Changed, Fixed, Removed. Every breaking change at the top of its
release with the migration step attached.

## Before you commit

1. Read the subject alone. Does it say what the commit does?
2. Does the body explain something the diff cannot?
3. Is the rejected alternative named, if there was one?
4. Exactly one concern?
5. Cut list and Pre-send over both. A slopped message is a failed pass even
   when the code is right.
