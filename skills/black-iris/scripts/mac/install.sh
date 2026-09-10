#!/usr/bin/env bash
# macOS entry point. Identical to Linux: symlink into ~/.claude/skills.
exec bash "$(dirname "$0")/../linux/install.sh" "$@"
