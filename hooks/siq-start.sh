#!/usr/bin/env sh
# Siq start hook. The logic lives in skills/black-iris/siq/siq.py, stdlib only.
# Off unless enabled: siq.py on (all chats), on --project, or arm (this chat).
# Fail-open: no Python that runs, or any error, exits 0.
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
[ -f "${root}/hooks/lib.sh" ] || exit 0
. "${root}/hooks/lib.sh"
py=$(find_python) || exit 0
"$py" "${root}/skills/black-iris/siq/siq.py" hook start
rc=$?
[ "$rc" -eq 2 ] && exit 2
exit 0
