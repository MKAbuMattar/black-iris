#!/usr/bin/env sh
# Stop hook: remind the model to harvest memory when a session did real work
# and the store has nothing in it. Off unless you ask for it.
#
# Opt in:  mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/memory-nudge
# Opt out: rm ~/.BLACK_IRIS_AGENTS/memory-nudge
#
# The channel, from the Claude Code hooks reference. Section "Exit code 0":
# stdout goes to the debug log for most events, the exceptions being
# UserPromptSubmit, UserPromptExpansion, SessionStart and PostModelSwitch. Stop
# is not an exception, so a Stop hook that prints plain text is talking to a log
# file. Section "Decision control" lists Stop among the events that honour
# hookSpecificOutput.additionalContext, and that is the only channel used here.
#
# This never blocks. It exits 0 on every path, prints at most once per session,
# and says nothing at all when the store already has an index.

base="${HOME}/.BLACK_IRIS_AGENTS"
[ -f "${base}/memory-nudge" ] || exit 0

payload=''
[ -t 0 ] || payload=$(head -c 65536 2>/dev/null)
session=$(printf '%s' "$payload" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$session" ] || session=nosession

proj="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
store="${base}/projects/$(printf '%s' "$proj" | tr '/' '-')"

# Nothing to say when the store already has an index. A session that has been
# harvested before does not need reminding; Memory's own rule is to write when
# the knowledge appears, not to sweep at the end.
[ -f "${store}/memory/MEMORY.md" ] && exit 0

# Only nudge when the session actually changed something. A session that read
# code and answered a question has nothing to harvest, and a reminder there is
# the kind of noise that gets a hook switched off.
git -C "$proj" rev-parse --git-dir >/dev/null 2>&1 || exit 0
[ -n "$(git -C "$proj" status --porcelain 2>/dev/null)" ] || exit 0

marker="${store}/tmp/memory-nudge-${session}"
mkdir -p "${store}/tmp" 2>/dev/null
[ -f "$marker" ] && exit 0
: > "$marker" 2>/dev/null

printf '{"hookSpecificOutput":{"hookEventName":"Stop","additionalContext":"This project has uncommitted work and no black-iris memory index yet. If this session worked out a procedure, hit a trap worth recording symptom first, closed a decision with a rejected alternative, or took a correction from the user, run the black-iris memory mode and write it as episodic before the transcript goes. If none of those happened, ignore this."}}\n'
exit 0
