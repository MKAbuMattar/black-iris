#!/usr/bin/env sh
# SessionStart hook: re-inject the black-iris body and the project's memory
# index on startup, resume, clear, and compact, when the user opted in.
# Opt in:  mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/always-on
# Opt out: rm ~/.BLACK_IRIS_AGENTS/always-on
#
# The router only. An earlier version also cat'd every reference, which cost
# about 94 KB per injection against the router's 11 KB, and it fired on
# compact, so the event that exists to free the window spent a fifth of it
# again before the first reply. The routing table names the file each mode
# needs; the model reads that one when the mode fires.
#
# SessionStart plain stdout reaches the model (Stop and PreCompact stdout
# do not). Always exits 0 so a broken hook never blocks a session.
base="${HOME}/.BLACK_IRIS_AGENTS"
[ -f "${base}/always-on" ] || exit 0
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
f="${root}/skills/black-iris/SKILL.md"
[ -f "$f" ] || exit 0
printf '# black-iris skill root: %s\n' "${root}/skills/black-iris"
printf 'Read a `references/` file named in the routing table when that mode\n'
printf 'fires, resolving it against that root. Do not read them all up front.\n\n'
# Body only: everything after the second frontmatter fence.
awk '/^---[[:space:]]*$/ && c<2 { c++; next } c>=2' "$f"
# Project memory index. Same slug derivation as references/memory.md.
proj="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
idx="${base}/projects/$(printf '%s' "$proj" | tr '/' '-')/memory/MEMORY.md"
[ -f "$idx" ] && { printf '\n# Project memory index\n'; cat "$idx"; }
exit 0
