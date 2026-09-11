#!/usr/bin/env sh
# Stop hook: refuse a stop while the project's gate ledger still has unmet
# gates. Off unless you ask for it.
#
# Opt in:  mkdir -p ~/.BLACK_IRIS_AGENTS && touch ~/.BLACK_IRIS_AGENTS/gates-stop
# Opt out: rm ~/.BLACK_IRIS_AGENTS/gates-stop
#
# The channel, from the Claude Code hooks reference, section "Exit code 2
# behavior per event": the Stop row reads Can block = Yes, "Prevents Claude
# from stopping, continues the conversation", and the blocking reason is the
# hook's stderr, shown to the model as feedback. Exit 2 plus stderr is the
# only mechanism this hook uses. It does not rely on any JSON output field,
# because a recipe built on the wrong field ships as a silent no-op, which is
# what happened to this project's PreCompact autodream recipe.
#
# Every path exits 0 except the one deliberate block. A broken hook must never
# trap a session.

base="${HOME}/.BLACK_IRIS_AGENTS"
[ -f "${base}/gates-stop" ] || exit 0

# Drain stdin only when it is a pipe, so a dry run from a terminal cannot hang.
payload=''
[ -t 0 ] || payload=$(head -c 65536 2>/dev/null)
session=$(printf '%s' "$payload" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
[ -n "$session" ] || session=nosession

proj="${CLAUDE_PROJECT_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
store="${base}/projects/$(printf '%s' "$proj" | tr '/' '-')"
ledger="${store}/GATES.md"
[ -f "$ledger" ] || exit 0

# An abandoned gate is a decision, not an oversight. The ledger ends in
# handoff and stopping there is correct, so its id never counts as unmet.
abandoned=$(sed -n 's/^ABANDON:[[:space:]]*\([A-Za-z0-9_.-]*\).*/\1/p' "$ledger")
unmet=''
for id in $(sed -n 's/^- \[ \][[:space:]]*\([A-Za-z0-9_.-]*\):.*/\1/p' "$ledger"); do
  skip=0
  for a in $abandoned; do [ "$id" = "$a" ] && skip=1; done
  [ "$skip" -eq 0 ] && unmet="${unmet}${unmet:+ }${id}"
done
[ -n "$unmet" ] || exit 0

# Block once per ledger state per session. If the model changes the ledger,
# meeting a gate or abandoning it, the state changes and a later stop can be
# blocked again on its own merits. If the model changes nothing, the state is
# identical and the second stop goes through, so this can never trap a turn in
# a loop.
state=$(cksum < "$ledger" 2>/dev/null | tr -d ' ')
marker="${store}/tmp/gates-stop-${session}-${state}"
mkdir -p "${store}/tmp" 2>/dev/null
[ -f "$marker" ] && exit 0
: > "$marker" 2>/dev/null

printf 'Gate ledger has unmet gates: %s\n' "$unmet" >&2
printf 'Ledger: %s\n' "$ledger" >&2
printf 'Run each unmet gate CHECK:, record exit code and matched token as EVIDENCE:, or add ABANDON: <id> <reason> and report HANDOFF REQUIRED. Do not report the task complete while a gate is unmet.\n' >&2
exit 2
