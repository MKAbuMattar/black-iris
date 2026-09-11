# Update black-iris

Every route below ends the same way: the newest `skills/black-iris/` folder in
the place your agent scans. Find your route, run its command, start a new
session. Skills and hooks are read at session start, so nothing you update
takes effect in the session you are sitting in.

Install routes are in [INSTALL.md](INSTALL.md). This file only covers updating
something already installed.

## Claude Code

Two commands, in this order.

```bash
claude plugin marketplace update black-iris
claude plugin update black-iris
```

Then restart Claude Code. The CLI says `restart required to apply`, and it
means it.

**`add` and `install` will not update you.** Both are create operations. Run
against an existing install they print `already on disk` and `already
installed`, fetch nothing, and leave you on the old version. This is the single
most common way to think you have updated when you have not.

Skill-only install instead of the plugin? Re-run the installer, which replaces
the link or copy in place:

```bash
python3 skills/black-iris/scripts/universal/install.py
```

## Which route am I on

| Your install used | Update with |
|---|---|
| `claude plugin install` | the two commands above, then restart |
| `npx skills add` | `npx skills update black-iris` |
| `codex plugin add` | `codex plugin marketplace upgrade black-iris`, then remove and add |
| `gemini extensions install` | `gemini extensions update black-iris` |
| `qwen extensions install` | `qwen extensions update black-iris` |
| `hermes skills install` | `hermes skills update black-iris` |
| `pi install` | `pi update https://github.com/MKAbuMattar/black-iris` |
| `agy plugin install` | `agy plugin uninstall black-iris`, then install again |
| `openclaw skills install` | run the install command again |
| Kimi `/plugins` menu | `/plugins`, cursor to Black Iris, press `R` |
| `cp -R` by hand | `git pull`, then re-run the same `cp -R` |
| the always-on snippet only | re-paste the snippet from `INSTALL.md` |

## The skills CLI

One command covers every agent installed this way: OpenCode, GitHub Copilot in
VS Code and the CLI, Kiro, Cline, TRAE, Qoder, Droid, Kilo Code, Roo Code,
Crush, Goose, Windsurf, Warp, Cursor, Amp, the Codex skill-only route, and the
long tail under "Other skills-CLI targets".

```bash
npx skills update black-iris
npx skills ls          # or: npx skills ls -g   for a global install
```

Installed into more than one agent? The CLI updates each copy it placed. Run
`npx skills ls` first if you want to see them.

## Per-agent managers

```bash
gemini extensions update black-iris      # Gemini CLI
qwen extensions update black-iris        # Qwen Code
hermes skills update black-iris          # Hermes
pi update https://github.com/MKAbuMattar/black-iris   # Pi
```

Codex and Antigravity have no in-place update. Codex refreshes the marketplace
first, then wants the plugin removed and added:

```bash
codex plugin marketplace upgrade black-iris
codex plugin remove black-iris && codex plugin add black-iris@black-iris

agy plugin uninstall black-iris
agy plugin install https://github.com/MKAbuMattar/black-iris
```

Kimi Code CLI is menu driven. In a session type `/plugins`, move the cursor to
Black Iris, press `R`.

## Copy routes

Z Code, DeepSeek Harness, Oh My Pi, Zed, OpenHands, and any install you made by
hand. Pull the repo, then re-run the copy you used, which overwrites in place.

```bash
git pull
cp -R skills/black-iris ~/.zcode/skills/          # Z Code
cp -R skills/black-iris ~/.dsh/skills/            # DeepSeek Harness
cp -R skills/black-iris .agents/skills/           # Oh My Pi
cp -R skills/black-iris ~/.config/zed/skills/     # Zed
```

Copy the whole folder every time. The references live beside `SKILL.md`, and a
copy that takes only `SKILL.md` leaves eight modes pointing at files that are
not there.

## Snippet-only routes

GitHub Copilot in JetBrains, Junie, JetBrains AI Assistant, Mistral Vibe,
Eigent, SillyTavern, and every agent under "Agents with no skill loader" carry
the always-on snippet rather than the skill folder. There is nothing to update
unless the snippet itself changed. Check the `black-iris core` section of
`INSTALL.md` against what you pasted, and replace it if they differ.

T3 Code drives Codex or Claude Code underneath. Update whichever of those it is
configured to use and T3 Code follows.

## Did it work

```bash
claude plugin list          # Claude Code: Version, and Status enabled
npx skills ls               # skills CLI routes
gemini extensions list      # Gemini CLI
qwen extensions list        # Qwen Code
hermes skills list          # Hermes
```

The version in `.claude-plugin/plugin.json` on `main` is the newest published
one. Releases are listed at
<https://github.com/MKAbuMattar/black-iris/releases>.

Then ask the agent a small how-to question in a new session. Line one should be
a command or a verdict, with no closing offer.

## When an update changes nothing

1. **You did not restart.** Skills and hooks are indexed at session start.
2. **You ran `add` or `install` again.** They no-op on an existing install.
   Use the `update` command for your route.
3. **You have two copies.** A global and a project install of the same skill
   both resolve; update both, or remove the one you do not want.
4. **`Status: failed to load` on the Claude Code plugin.** That was a manifest
   bug in every release up to 1.6.0. The fix only reaches you by updating, so
   run the two commands above and restart.
