#!/usr/bin/env sh
# Dabke stop hook. The logic lives in skills/black-iris/dabke/dabke.py, stdlib only.
# Off unless a loop is on for this chat: dabke.py start "<brief>".
# Fail-open: no Python that runs, or any error, exits 0.
# The one exception is the deliberate Stop block, exit 2 with the next step on
# stderr, the channel the hooks reference documents for Stop (as gates-stop).
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
[ -f "${root}/hooks/lib.sh" ] || exit 0
. "${root}/hooks/lib.sh"
py=$(find_python) || exit 0
"$py" "${root}/skills/black-iris/dabke/dabke.py" hook stop
rc=$?
[ "$rc" -eq 2 ] && exit 2
exit 0
