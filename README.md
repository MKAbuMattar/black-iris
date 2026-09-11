<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/hero-en-dark.svg">
  <img src=".github/assets/readme/hero-en-light.svg" width="100%" alt="black-iris: one skill, twelve disciplines for a coding agent, with its routing table of modes">
</picture>
</p>

<p align="center">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/logo-dark.svg">
  <img src=".github/assets/readme/logo-light.svg" width="112" alt="black-iris logo, a geometric black iris">
</picture>
</p>

<h1 align="center">black-iris</h1>
<p align="center"><em>السوسنة السوداء</em></p>
<p align="center">One skill, twelve disciplines for a coding agent.</p>

<p align="center"><a href="README.md">English</a> | <a href="README_ES.md">Espanol</a> | <a href="README_AR.md">العربية</a></p>

<p align="center">One skill for a coding agent, twelve disciplines. It shapes every reply for a reader with ADHD, cuts AI tells from anything the agent writes, keeps code changes surgical, writes completion gates before long work, fans out isolated ideation branches, writes prompts for other tools, consolidates session memory, keeps bulk data out of the context window, and handles commit text, naming, and diff review. One 200-line router plus ten reference files.</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/section-install-en-dark.svg">
  <img src=".github/assets/readme/section-install-en-light.svg" width="100%" alt="Install">
</picture>

Claude Code, plugin with the session-start hook:

```bash
claude plugin marketplace add MKAbuMattar/black-iris
claude plugin install black-iris@black-iris
```

Any agent that reads Agent Skills, skill only:

```bash
npx skills add MKAbuMattar/black-iris -g
```

Every other agent, including Codex, Kimi, Gemini CLI, OpenCode, Z Code,
DeepSeek Harness, Copilot, Zed, Hermes, Pi, Antigravity, and Cursor, is in
[INSTALL.md](INSTALL.md).

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/section-use-en-dark.svg">
  <img src=".github/assets/readme/section-use-en-light.svg" width="100%" alt="Use">
</picture>

Type `/black-iris` once and every mode loads in full. Shape, Build, and the
Cut list stay on until you say "stop black-iris". To load one mode alone, name
it: `/black-iris deslop`, or ask with its trigger words.

| Load one mode | Or say | What it does |
|---|---|---|
| `/black-iris deslop` | "deslop", "humanize" | Remove AI tells, keep every fact |
| `/black-iris gates` | "gates", "do not stop until done" | A checkable ledger before long work |
| `/black-iris ideate` | "ideate", "brainstorm" | Isolated parallel branches, then a verdict |
| `/black-iris prompt` | "write a prompt for X" | One paste-ready prompt for a named tool |
| `/black-iris memory` | "autodream", "consolidate memory" | Harvest and verify session knowledge |
| `/black-iris ship` | "commit message", "PR body" | Conventional commits with a real why |
| `/black-iris name` | "rename", "name this" | Identifiers that read true |
| `/black-iris review` | "review this diff" | Five ranked findings, no rewrites |

Dial the length with `/black-iris lite`, `full`, or `deep`.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/section-store-en-dark.svg">
  <img src=".github/assets/readme/section-store-en-light.svg" width="100%" alt="Where it writes">
</picture>

Everything per project goes under `~/.BLACK_IRIS_AGENTS/projects/<slug>/`:
gate ledgers, memory, scratch. Nothing lands in your repo or in `~/.claude`.
Set `~/.BLACK_IRIS_AGENTS/always-on` to have the Claude Code hook re-inject
the whole skill, references included, and your project's memory index at
every session start.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme/section-repo-en-dark.svg">
  <img src=".github/assets/readme/section-repo-en-light.svg" width="100%" alt="Repo">
</picture>

- `skills/black-iris/` is the skill: `SKILL.md`, `references/`, `scripts/`.
- `hooks/` is the Claude Code SessionStart hook.
- Root manifests package the same skill for Codex (plugin and marketplace),
  Kimi, Qwen, Gemini, Antigravity, and Pi.

Lint before committing: `python3 skills/black-iris/scripts/universal/check.py`.

License: GPL-2.0-only for the skill and the whole repo. See [.github/LICENSE](.github/LICENSE).
