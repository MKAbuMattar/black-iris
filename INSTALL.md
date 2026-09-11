# Install black-iris

One skill folder, `skills/black-iris/`, works everywhere that reads Agent
Skills. Every route below ends with the same thing: that folder, references
included, in a place your agent scans. Only Claude Code also gets the
SessionStart hook; every other agent gets the skill and can add an always-on
snippet by hand.

Commands assume the repo is published at `github.com/MKAbuMattar/black-iris`.
Until it is pushed, use the local-path routes.

What every route shares:

- Invoke by name. `/black-iris` where slash skills exist, `$black-iris` in
  Codex, or ask for it in words. Shape, Build, and the Cut list stay on until
  "stop black-iris" or "normal mode".
- Per-project files go to `~/.BLACK_IRIS_AGENTS/projects/<slug>/`. Nothing
  is written into your repo or `~/.claude`.
- Always-on flag: `mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/always-on`.
  Only the Claude Code plugin route reads it.

## Claude Code

Plugin route, gives the skill and the hook:

```bash
claude plugin marketplace add MKAbuMattar/black-iris
claude plugin install black-iris@black-iris
```

Local plugin route, no publish needed, one session at a time:

```bash
claude --plugin-dir /path/to/black-iris
```

Skill-only route, no hook:

```bash
python3 skills/black-iris/scripts/universal/install.py            # symlink into ~/.claude/skills
python3 skills/black-iris/scripts/universal/install.py --always-on   # also set the flag
python3 skills/black-iris/scripts/universal/install.py --uninstall
```

`scripts/linux/install.sh`, `scripts/mac/install.sh`, and
`scripts/windows/install.ps1` do the same in each platform's shell.

Verify: start a new session and type `/black-iris`, or run `claude plugin list`.
Update: `claude plugin marketplace update black-iris`. Uninstall:
`claude plugin uninstall black-iris` then `claude plugin marketplace remove black-iris`.

With the flag set and the plugin loaded, every session start, resume, clear,
and compaction re-injects the skill body and the project's `MEMORY.md`, about
11 KB. The references are not injected; the model reads the one its mode names
when that mode fires.
Without the plugin the flag does nothing.

Claude for IDE (the VS Code and JetBrains extensions) runs the same Claude
Code underneath and reads the same `~/.claude/skills` and plugin list. Any
route above covers it; open a new IDE chat after installing.

## Codex

```bash
codex plugin marketplace add MKAbuMattar/black-iris --ref main
codex plugin add black-iris@black-iris
```

The repo ships `.codex-plugin/plugin.json` and a Codex marketplace file at
`.agents/plugins/marketplace.json`, which is what the first command reads.
Type `$black-iris`. The skill allows implicit invocation, so Codex may also
pick it up from the description. Skill-only alternative:

```bash
npx skills add MKAbuMattar/black-iris -a codex        # or copy skills/black-iris to ~/.codex/skills/
```

Update: `codex plugin marketplace upgrade black-iris`, then remove and add.
Uninstall: `codex plugin remove black-iris` and `codex plugin marketplace remove black-iris`.
Always-on: paste the snippet at the end of this file into `~/.codex/AGENTS.md`.

## Kimi Code CLI

In a session: `/plugins`, choose Custom, paste
`https://github.com/MKAbuMattar/black-iris`, choose Trust and install.
Invoke with `/skill:black-iris`. Update: `/plugins`, cursor to Black Iris,
press `R`. Uninstall: same menu, press `D`.

## Gemini CLI

```bash
gemini extensions install https://github.com/MKAbuMattar/black-iris
```

The extension loads `GEMINI.md`, which imports the full skill, so the rules
apply from message one. This route is always-on by construction. Needs `git`.
Verify: `gemini extensions list`. Update: `gemini extensions update black-iris`.
Uninstall: `gemini extensions uninstall black-iris`.

## OpenCode

OpenCode reads Agent Skills natively and the model invokes them through its
skill tool by description.

```bash
npx skills add MKAbuMattar/black-iris -a opencode -y     # this workspace
npx skills add MKAbuMattar/black-iris -a opencode -g -y  # all projects
```

Manual: copy `skills/black-iris` into `.agents/skills/` in the project or
`~/.config/opencode/skills/`. Ask for it in words ("use black-iris"). No hook
and no always-on flag; paste the snippet below into `~/.config/opencode/AGENTS.md`
for that.

## Z Code

Z Code reads Agent Skills from `~/.zcode/skills/<skill-name>/SKILL.md` and
lets a skill reference other files in its folder, so the references resolve.

```bash
mkdir -p ~/.zcode/skills
cp -R skills/black-iris ~/.zcode/skills/
```

Or, in Z Code, open Settings, Skills, click Import, and point it at
`skills/black-iris` as a Symlink (tracks this repo) or a Copy, Global or
Project. Click Refresh if a hand-copied folder does not show. Invoke with
`$black-iris` in chat, or from the Skills group in the `/` menu. Uninstall by
removing the folder or the import. No hook and no always-on flag; use the
snippet below in Z Code's rules if you want it on every session.

## DeepSeek Harness (dsh)

dsh reads Agent Skills as `<name>/SKILL.md` folders from, in priority order:
`<project>/.dsh/skills`, `<project>/.agents/skills`, any `customSkillDirs` in
config, `~/.dsh/skills`, and `~/.agents/skills`. The project root is the
nearest directory with `.git`. The folder name must match the frontmatter
`name`, which `black-iris` does, and relative `references/` paths resolve
through the skill folder.

```bash
mkdir -p ~/.dsh/skills
cp -R skills/black-iris ~/.dsh/skills/                              # every project
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/  # this project only
```

`npx skills add MKAbuMattar/black-iris -a codex` lands in `.agents/skills/`,
which dsh scans as well. Copy rather than symlink; symlink following is a
provider setting that may be off. dsh honors the same `disable-model-invocation`
and `user-invocable` frontmatter keys as Claude Code, both defaulting to true,
so black-iris is available to the model's skill tool and to you by name. No
hook and no always-on flag; put the snippet below in the profile's system
prompt or `AGENTS.md`. The plugin route (`dsh plugin add github:<owner>/<repo>`)
needs a Cordis plugin that registers a SkillProvider; black-iris does not ship
one, because the bare skill root does the same job.

## T3 Code

T3 Code is a desktop GUI that drives Codex or Claude Code underneath. It has
no skill store of its own. Install black-iris into the agent T3 Code is
configured to use, with the Claude Code or Codex route above, then invoke it
in the T3 Code chat the same way. If you use the Claude Code plugin route, the
hook works there too.

## GitHub Copilot (VS Code and Copilot CLI)

Copilot reads Agent Skills natively from `.github/skills/`, `.claude/skills/`,
and `.agents/skills/` in the project, and `~/.copilot/skills/`,
`~/.claude/skills/`, and `~/.agents/skills/` globally.

```bash
npx skills add MKAbuMattar/black-iris -a github-copilot        # this project
npx skills add MKAbuMattar/black-iris -a github-copilot -g     # all projects
```

Manual: `cp -R skills/black-iris ~/.copilot/skills/`. Type `/black-iris` in
chat. The Claude Code skill-only install above also satisfies Copilot, since
it scans `~/.claude/skills/`. Update: `npx skills update black-iris`.
Uninstall: `npx skills remove black-iris`. Always-on: the snippet below in
`.github/copilot-instructions.md`.

## GitHub Copilot in JetBrains

A different route from the one above, and from Junie and JetBrains AI
Assistant. GitHub's docs list repository-wide instructions
(`.github/copilot-instructions.md`) and path-specific instructions
(`.github/instructions/**/*.instructions.md`) as supported for Copilot Chat in
JetBrains IDEs. They do not document Agent Skills loading there, so this is a
snippet route: the always-on core works, and the modes that need a reference
file do not.

Put the snippet below in `.github/copilot-instructions.md`. It is the same
file the VS Code route uses, so a repository set up for one is already set up
for the other. Verify by asking Copilot Chat in the IDE what its first rule
for shaping a reply is. Update and uninstall are edits to that file.

For Copilot coding agent in JetBrains, GitHub's docs also list `AGENTS.md`,
`CLAUDE.md`, and `GEMINI.md`; the snippet works in any of them. Source:
GitHub Docs, "Adding repository custom instructions for GitHub Copilot",
JetBrains tool tab, and "Custom instructions support".

## Kiro

Kiro reads Agent Skills from `.kiro/skills/` in the workspace and
`~/.kiro/skills/` for every project, one skill per directory as
`<skills-root>/<skill-name>/SKILL.md`.

```bash
npx skills add MKAbuMattar/black-iris -a kiro          # this workspace
cp -R skills/black-iris ~/.kiro/skills/                # all projects
```

Invoke by typing `/` in chat and picking it, or let Kiro match your request
against the skill description. Verify in the Kiro panel under **Agent Steering
& Skills**; Kiro's docs document no CLI command to list skills, so the panel
is the check. Update: re-copy the folder, or `npx skills update black-iris`.
Uninstall: delete the directory.

Always-on: the snippet below in `.kiro/steering/`, which is where Kiro keeps
instructions that apply to every session.

One trap. Kiro's docs say a custom agent does not load skills by default. If
you run black-iris under a custom agent rather than the default one, add it to
that agent's `resources` field with the `skill://` URI scheme, or the folder
will sit there unread. Source: Kiro docs, "Agent Skills", "Steering", and
"Creating custom agents".

## Oh My Pi (omp)

OMP discovers skills one level under a `skills/` root: `.agents/skills/` is
the canonical project location and `.github/skills/` is also read.

```bash
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/
```

Invoke with `/skill:black-iris`. OMP's docs recognise that token both at the
start of a message and inside ordinary prose. Update: re-copy the folder.
Uninstall: delete `.agents/skills/black-iris`.

Verify by invoking it, because OMP's skills documentation lists no command to
enumerate loaded skills. Do not trust a silent install.

Always-on: the snippet below in `AGENTS.md` at the project root. OMP walks
ancestor directories from the working directory to find `AGENTS.md` files and
merges them as persistent context. Source: `can1357/oh-my-pi`,
`docs/skills.md`.

## Zed

Zed's Agent reads Agent Skills. Copy the whole folder, because the URL import
takes only SKILL.md and black-iris needs its `references/` directory:

```bash
cp -R skills/black-iris ~/.config/zed/skills/
```

Type `/black-iris` in the Agent Panel. Verify in the Skills manager.
Uninstall: delete `~/.config/zed/skills/black-iris`. Always-on: the snippet
below in `~/.config/zed/AGENTS.md`.

## Hermes

```bash
hermes skills install MKAbuMattar/black-iris/skills/black-iris
```

Type `/black-iris`. Verify: `hermes skills list`. Update:
`hermes skills update black-iris`. Uninstall: `hermes skills uninstall black-iris`.
Always-on: the snippet below in the working directory's `AGENTS.md`, or in
your persona `SOUL.md` for every session.

## Pi

```bash
pi install https://github.com/MKAbuMattar/black-iris
```

The package exposes the skill; type `/skill:black-iris`. Verify: `pi list`.
Update: `pi update https://github.com/MKAbuMattar/black-iris`. Uninstall:
`pi remove https://github.com/MKAbuMattar/black-iris`. No Pi extension ships,
so there is no footer toggle or always-on flag on Pi.

## Antigravity

```bash
agy plugin install https://github.com/MKAbuMattar/black-iris
```

Verify: `agy plugin list`. Update: uninstall then install. Uninstall:
`agy plugin uninstall black-iris`, or `agy plugin disable black-iris` to keep
it. Always-on: the snippet below in `~/.gemini/GEMINI.md`.

## Cline

```bash
npx skills add MKAbuMattar/black-iris -a cline        # this project, .agents/skills/
npx skills add MKAbuMattar/black-iris -a cline -g     # all projects, ~/.agents/skills/
```

Manual: copy `skills/black-iris` into `.agents/skills/` or `~/.agents/skills/`.
Ask for it by name in chat. Always-on: the snippet below in `.clinerules`.

## TRAE

```bash
npx skills add MKAbuMattar/black-iris -a trae         # this project, .trae/skills/
npx skills add MKAbuMattar/black-iris -a trae -g      # all projects, ~/.trae/skills/
```

Manual: copy `skills/black-iris` into `.trae/skills/` or `~/.trae/skills/`.
Always-on: the snippet below in TRAE's project rules.

## Qoder

```bash
npx skills add MKAbuMattar/black-iris -a qoder        # this project, .qoder/skills/
npx skills add MKAbuMattar/black-iris -a qoder -g     # all projects, ~/.qoder/skills/
```

Manual: copy `skills/black-iris` into `.qoder/skills/` or `~/.qoder/skills/`.
Always-on: the snippet below in Qoder's rules.

## Droid (Factory)

```bash
npx skills add MKAbuMattar/black-iris -a droid        # this project, .agents/skills/
npx skills add MKAbuMattar/black-iris -a droid -g     # all projects, ~/.factory/skills/
```

Manual: copy `skills/black-iris` into `.agents/skills/` or `~/.factory/skills/`.
Restart `droid` so it rescans skills; it invokes matching skills from the
description on its own. Always-on: the snippet below in `AGENTS.md`.

## Kilo Code

```bash
npx skills add MKAbuMattar/black-iris -a kilo         # this project, .agents/skills/
npx skills add MKAbuMattar/black-iris -a kilo -g      # all projects, ~/.kilo/skills/
```

Manual: copy `skills/black-iris` into `.agents/skills/` or `~/.kilo/skills/`.
Always-on: the snippet below in `.kilocode/rules/`.

## Roo Code

```bash
npx skills add MKAbuMattar/black-iris -a roo          # this project, .roo/skills/
npx skills add MKAbuMattar/black-iris -a roo -g       # all projects, ~/.roo/skills/
```

Manual: copy `skills/black-iris` into `.roo/skills/` or `~/.roo/skills/`.
Always-on: the snippet below in `.roo/rules/`.

## Crush

```bash
npx skills add MKAbuMattar/black-iris -a crush        # this project, .crush/skills/
npx skills add MKAbuMattar/black-iris -a crush -g     # all projects, ~/.config/crush/skills/
```

Manual: copy `skills/black-iris` into `.crush/skills/` or
`~/.config/crush/skills/`. Always-on: the snippet below in `CRUSH.md` or
`AGENTS.md`, which Crush reads as context.

## Goose

Goose reads `.goose/skills/` and `.agents/skills/` in the project and
`~/.config/goose/skills/` globally, and also picks up `~/.claude/skills/`, so
the Claude Code skill-only install above already covers it. The folder name
must match the frontmatter name, which holds.

```bash
npx skills add MKAbuMattar/black-iris -a goose        # this project, .goose/skills/
npx skills add MKAbuMattar/black-iris -a goose -g     # all projects, ~/.config/goose/skills/
```

Always-on: the snippet below in `.goosehints`.

## Eigent

Eigent ships a skill catalog: `npx @eigent-ai/agent-skills list` and
`npx @eigent-ai/agent-skills install <name>`. Its docs do not say where those
land on disk or how to add a skill that is not in the catalog, so there is no
verified path for black-iris yet. What works today: paste the always-on
snippet below into the agent's system prompt or task instructions, keep
`skills/black-iris` in a workspace folder the agent can read, and ask for it
by name. Open an issue if you find the custom-skill path in Eigent's settings.

## OpenClaw

OpenClaw has a native skill installer and reads `SKILL.md` folders with
`name` and `description` frontmatter.

```bash
openclaw skills install MKAbuMattar/black-iris/skills/black-iris            # active workspace skills/
openclaw skills install MKAbuMattar/black-iris/skills/black-iris --global   # ~/.openclaw/skills/
```

Manual: copy `skills/black-iris` into `~/.openclaw/skills/` or the workspace
`skills/` folder. The skill is named by its frontmatter, so a subfolder is
fine. Always-on: the snippet below in the agent's persona or workspace
instructions.

## SillyTavern

SillyTavern is a chat frontend with no skill loader. Two honest options:

1. Paste the always-on snippet below into the system prompt of your preset,
   or into a character card's description, so Shape and the Cut list apply.
2. For a full mode, paste the body of the reference you need (for example
   `references/deslop.md`) as an Author's Note or a lorebook entry set to
   always-on, and invoke it by name in chat.

No hook, no store, no `/black-iris` command.

## Qwen Code

```bash
qwen extensions install MKAbuMattar/black-iris
```

The shipped `qwen-extension.json` points Qwen Code at `skills/`. Qwen Code
also reads Agent Skills from `~/.qwen/skills/` and `.qwen/skills/` directly,
per its skills docs, so a plain copy works too. Type `/black-iris`, or run
`/skills` to confirm it is listed. Verify: `qwen extensions list`. Update:
`qwen extensions update black-iris`. Uninstall:
`qwen extensions uninstall black-iris`.

## Windsurf

Cascade reads `.windsurf/skills/` in the project and
`~/.codeium/windsurf/skills/` globally, per Windsurf's skills docs.

```bash
npx skills add MKAbuMattar/black-iris -a windsurf        # this project
npx skills add MKAbuMattar/black-iris -a windsurf -g     # all projects
```

Always-on: the snippet below in a Windsurf rule with always-on trigger.

## Warp

Warp agents read Agent Skills from `.agents/skills/` in the project and
`~/.agents/skills/` globally, per Warp's skills docs.

```bash
npx skills add MKAbuMattar/black-iris -a warp            # this project
npx skills add MKAbuMattar/black-iris -a warp -g         # all projects
```

Always-on: the snippet below in Warp's agent rules.

## Junie (JetBrains)

Junie reads `.junie/skills/` in the project and `~/.junie/skills/` globally,
per its agent-skills docs. Copy `skills/black-iris` into either. Always-on:
the snippet below in `.junie/guidelines.md`.

## JetBrains AI Assistant

AI Assistant loads skill directories configured under Settings, Tools, AI
Assistant, Skills, per its agent-skills help page. Point it at a copy of
`skills/black-iris`. Always-on: the snippet below in the assistant's
project rules.

## Mistral Vibe

Vibe follows the Agent Skills spec and reads `~/.vibe/skills/` and
`.vibe/skills/`, per the Mistral Vibe docs. Copy `skills/black-iris` into
either and invoke by name.

## OpenHands

OpenHands reads `.agents/skills/` (recommended) and the older
`.openhands/skills/`, per its skills docs.

```bash
mkdir -p .agents/skills && cp -R skills/black-iris .agents/skills/
```

Always-on: the snippet below in `.openhands/microagents/repo.md`.

## Other skills-CLI targets

The skills CLI knows the skill directory of many more agents. These paths
come from that CLI's agent table and were not checked against each vendor's
own docs; treat them as a starting point.

```bash
npx skills add MKAbuMattar/black-iris -a augment       # .augment/skills, ~/.augment/skills
npx skills add MKAbuMattar/black-iris -a continue      # .continue/skills, ~/.continue/skills
npx skills add MKAbuMattar/black-iris -a devin         # .devin/skills, ~/.config/devin/skills (Devin for Terminal)
npx skills add MKAbuMattar/black-iris -a tabnine       # .tabnine/agent/skills
npx skills add MKAbuMattar/black-iris -a replit        # .agents/skills
npx skills add MKAbuMattar/black-iris -a grok          # .grok/skills
npx skills add MKAbuMattar/black-iris --all            # every agent the CLI detects on this machine
```

The same CLI covers the long tail: Lingma, CodeBuddy, CodeArts Agent, Rovo
Dev, Cortex Code, MiniMax Code, iFlow CLI, AiderDesk, Zencoder, and others.
`--all` installs into whichever of them it finds.

## Agents with no skill loader

Aider, Amazon Q Developer, Gemini Code Assist, Sourcegraph Cody, Void, Xcode,
Bolt, v0, Lovable, Manus, and cloud Devin read no skill folders. For these,
paste the always-on snippet below into whatever persistent instructions they
do read: Amazon Q rules, `GEMINI.md` or `AGENTS.md` for Gemini Code Assist,
a project rules file elsewhere. The modes that need a reference file are not
available there.

## Cursor, Amp, and other agent-skills harnesses

```bash
npx skills add MKAbuMattar/black-iris                  # this workspace
npx skills add MKAbuMattar/black-iris -g               # all projects
npx skills add MKAbuMattar/black-iris -a cursor -y     # one agent only
npx skills add MKAbuMattar/black-iris --all            # every agent the CLI detects
```

Manual: copy `skills/black-iris` into the path your agent scans, for example
`~/.cursor/skills/`. Copy, do not symlink; Cursor does not follow symlinks on
every platform. New chat, type `/black-iris`. Verify: `npx skills list`
(`npx skills ls -g` if global). Update: `npx skills update black-iris`.
Uninstall: `npx skills remove black-iris`. Always-on: Cursor Settings, Rules,
User Rules, or a project rule under `.cursor/rules/` with `alwaysApply: true`.

## Any other agent (manual)

1. Copy `skills/black-iris/` whole, with `references/`, into the directory
   your agent scans for skills. If it scans nothing, put it anywhere the
   agent can read.
2. If the agent cannot read YAML frontmatter, feed it the body only:

   ```bash
   awk '/^---[[:space:]]*$/ && c<2 { c++; next } c>=2' skills/black-iris/SKILL.md
   ```

   Paste that into the system prompt or rules file, and tell the agent where
   the `references/` folder lives so the mode table's paths resolve.
3. Invoke by name in the first message of a session.

## Optional: refuse a stop while gates are unmet

Claude Code plugin route only, and off unless you ask for it.

```bash
mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/gates-stop   # on
rm ~/.BLACK_IRIS_AGENTS/gates-stop                                       # off
```

With the flag set, `hooks/gates-stop.sh` runs when Claude Code is about to
stop. If the project's `GATES.md` in the store still lists unmet gates, it
refuses the stop and names their ids, so a "done" cannot land on top of an
unchecked ledger. Without the flag it exits immediately and your sessions are
unchanged.

What it does not do. It never judges whether a gate should have passed; it
reads the ids you wrote. An `ABANDON:` line is a decision, so an abandoned
gate never counts as unmet and a handoff stop goes through. And it blocks at
most once per ledger state per session, so changing nothing lets the next stop
through rather than trapping the turn in a loop.

Verify: with the flag set and a ledger holding an unmet gate, ask for a stop
and you get the gate ids back. Without a ledger there is nothing to block.

## Optional: a nudge to harvest memory

Claude Code plugin route only, off unless you ask for it.

```bash
mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/memory-nudge   # on
rm ~/.BLACK_IRIS_AGENTS/memory-nudge                                       # off
```

With the flag set, `hooks/memory-stop.sh` speaks up once per session when the
project has uncommitted work and the store still has no memory index, which is
the state where a session's traps and decisions are about to be lost. It never
blocks; it adds one line of context asking whether anything is worth writing.

It stays quiet in every other case: no flag, a clean tree, a session that
already has an index, and any session it has already spoken in. Memory's own
rule is to write when the knowledge appears, so this is a backstop for the
store that was never started, not a sweep at the end.

## Always-on snippet for agents without the hook

Paste into the agent's persistent rules file. It carries the always-on core
only; the other modes still need the skill folder installed.

```markdown
## black-iris core

Shape every response for a reader with ADHD. Line one is the answer or the
action. Number multi-step work, fewest steps that work. Restate state every
turn. Numbers, thresholds, and scoped conditions stay exact. A warning is the
last thing to cut. An answer stops at its point; a deliverable ships bare.
Estimates in concrete units, saying whose time. Show what now works. Cap lists
at five. End with one action under two minutes, or the blocking question, and
nothing after it.

Build: read the flow the change touches, surface assumptions, every changed
line traces to the request, state the check before the work, minimum code in
the repo's idiom, comments carry the why.

Cut: no em or en dashes, no AI vocabulary (delve, leverage, seamless,
robust, crucial, showcase, utilize), no "not just X but Y", no filler, no
rule of three, name the actor, no decorative emoji or title case, never sign
work as AI. Delete any opener that announces and any closer that recaps.

Break these when asked to explain, before a destructive action, after three
failed fixes, or when a wrong guess costs a rewrite. "stop black-iris" turns
them off.
```

## Verify it works

Ask any agent a small how-to question after invoking the skill. Line one
should be a command or a verdict, there should be no em dashes and no closing
offer, and a risk should sit next to the step it guards. If replies still
open with "Sure" or end with "Let me know", start a new session; skills are
indexed at session start.

## Troubleshooting

- `/black-iris` missing from autocomplete: restart the agent.
- Always-on flag has no effect: it needs the Claude Code plugin route, not the
  skill symlink, and a new session after the plugin loads.
- `marketplace add` fails: use the `owner/repo` form, or a local path to the
  repo root, not to `.claude-plugin/`.
- A reference path does not resolve: the agent got SKILL.md without its
  folder. Reinstall the whole `skills/black-iris/` directory.
