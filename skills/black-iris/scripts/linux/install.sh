#!/usr/bin/env bash
# Install black-iris as a personal skill.
#   scripts/linux/install.sh              link into ~/.claude/skills
#   scripts/linux/install.sh --always-on  also set the SessionStart re-inject flag
#   scripts/linux/install.sh --uninstall  remove link and flag
set -eu
skill="$(cd "$(dirname "$0")/../.." && pwd)"
dest="$HOME/.claude/skills/$(basename "$skill")"
flag="$HOME/.BLACK_IRIS_AGENTS/always-on"
case "${1:-}" in
  --uninstall) rm -rf "$dest" "$flag"; echo "removed $dest and $(basename "$flag")"; exit 0 ;;
esac
mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
ln -s "$skill" "$dest"
echo "linked $dest -> $skill"
[ "${1:-}" = "--always-on" ] && { mkdir -p "$(dirname "$flag")"; touch "$flag"; echo "always-on flag set: $flag"; }
echo "Start a new session; skills and hooks load at session start."
