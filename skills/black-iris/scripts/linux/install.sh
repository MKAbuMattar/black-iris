#!/usr/bin/env bash
# Install black-iris as personal skills: black-iris itself plus one
# black-iris-<mode> folder per mode, which read their reference from
# ../black-iris/ and so must sit beside it.
#   scripts/linux/install.sh              link into ~/.claude/skills
#   scripts/linux/install.sh --always-on  also set the SessionStart re-inject flag
#   scripts/linux/install.sh --uninstall  remove links and flag
set -eu
skill="$(cd "$(dirname "$0")/../.." && pwd)"
root="$(dirname "$skill")"
dir="$HOME/.claude/skills"
flag="$HOME/.BLACK_IRIS_AGENTS/always-on"
sources="$skill"
for s in "$root"/black-iris-*; do [ -f "$s/SKILL.md" ] && sources="$sources $s"; done
case "${1:-}" in
  --uninstall)
    for s in $sources; do rm -rf "$dir/$(basename "$s")"; done
    rm -f "$flag"; echo "removed skill folders and $(basename "$flag")"; exit 0 ;;
esac
mkdir -p "$dir"
for s in $sources; do
  d="$dir/$(basename "$s")"
  rm -rf "$d"
  ln -s "$s" "$d"
  echo "linked $d -> $s"
done
[ "${1:-}" = "--always-on" ] && { mkdir -p "$(dirname "$flag")"; touch "$flag"; echo "always-on flag set: $flag"; }
echo "Start a new session; skills and hooks load at session start."
