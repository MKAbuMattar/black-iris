#!/usr/bin/env sh
# Siq start hook. The logic lives in skills/black-iris/siq/siq.py, stdlib only.
# Off unless enabled: siq.py on (all chats), on --project, or arm (this chat).
# Fail-open: no python3, or any error, exits 0.
command -v python3 >/dev/null 2>&1 || exit 0
root="${CLAUDE_PLUGIN_ROOT:-$(cd "$(dirname "$0")/.." && pwd)}"
python3 "${root}/skills/black-iris/siq/siq.py" hook start
rc=$?
[ "$rc" -eq 2 ] && exit 2
exit 0
