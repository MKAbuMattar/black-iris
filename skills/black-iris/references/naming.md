# Name: variables, functions, files

Every word in a name is load-bearing, and the load-bearing word goes first. A
name is read far more often than written, and it is the one piece of
documentation the compiler helps you keep true.

## The test

Hide the value. Does the name say what is in there, or only what type it is?

Bad: `const data = await fetch(...)`. Every value is data.
Good: `const pendingInvoices = await fetch(...)`.

Bad: `function process(items)`. All code processes.
Good: `function dedupeByCustomer(invoices)`.

If the only names available are data, info, item, thing, handle, manager,
helper, or util, you do not yet know what it holds. Two minutes of thought
before a name.

## Variables

- **Content, not container.** `users`, not `userList`. The plural carries the
  shape, and the day it becomes a Set the name is a lie.
- **No type in the name.** `strName`, `arrItems`, `userObject` restate what
  the type system knows and rot under refactoring.
- **Length scales with scope.** `i` in a three-line loop is right. A name that
  crosses a hundred lines or leaves the file earns every character.
- **Booleans read as a yes-question.** `is`, `has`, `can`, `should`.
  `isExpired`, `hasWriteAccess`, `canRetry`. Never `flag`, `status`, `check`.
- **Never name a boolean for its false case.** `isNotReady`, `disableCache`,
  `hideBanner` each force a double negative at the call site, and
  `if (!isNotReady)` is a bug waiting for a tired reader.
- **Abbreviate only what the domain already abbreviates.** `id`, `url`, `db`,
  `api` read as words. `usr`, `calc`, `resp`, `mgr` save four characters and
  cost a lookup.

## Functions

- **A verb phrase, and the verb must be true.** `getUser` that also writes a
  cache entry lies, and a caller who trusts it will call it in a loop.
- **The name covers everything it does.** An honest name that needs "and" is
  the function telling you it does two things.
- **Match the verb to the cost.** `get` reads as cheap and local. `fetch`,
  `load`, `query` for anything that crosses a network or disk.
- **What it returns, not how.** `binarySearchUsers` leaks an implementation
  you will want to change. `findUser` survives it.
- **A predicate follows the boolean rules.** `isEligible(user)`, not
  `checkUser(user)`.

## Files and modules

Name the file for its primary export, in the repo's casing. One
`InvoiceTable` component lives in `InvoiceTable.tsx`, not `table.tsx` and not
`index.tsx` three directories deep.

`utils`, `helpers`, `common`, `misc` are one file with four names, and each
becomes a dumping ground within a month. A function with no home is a missing
concept, not a missing junk drawer.

## One concept, one name

Pick a word per concept and repeat it everywhere: variable, function, file,
column, API field, log line. `user` here, `account` two files over, and
`member` in the schema is three names for one thing, and every reader pays to
learn they are the same. Varying word choice is right in prose and wrong in
code.

When the codebase already picked a word, that word wins even when yours is
better. A reader can learn one odd word and cannot learn an unpredictable
mapping.

## When not to rename

Renaming is cheap in the editor and expensive everywhere else. Leave it when:

1. **It is public API.** A rename is a breaking change and gets its own
   commit with a migration note.
2. **It matches an in-repo convention you dislike.** Open a discussion; do
   not fork the convention inside one file.
3. **The rename is the whole diff and nobody asked.** Churn buries the real
   change and poisons `git blame`.
4. **It is only mildly worse.** The bar is "misleads a reader", not "is not
   what I would have written".

A misleading name is worth fixing on sight. A plain one is not.

## Before you name

1. Say what the thing is out loud. If the sentence needs "the thing that",
   you are not ready.
2. Will the name still be true after the change you already know is coming?
3. Does it collide with a word this repo uses for something else?
4. Read the call site, not the definition. Names are for the caller.
