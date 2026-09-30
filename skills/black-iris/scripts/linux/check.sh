#!/usr/bin/env bash
# black-iris self-lint, bash edition. Same checks as universal/check.py.
# Uses only POSIX tools plus bash 3.2, so mac/check.sh delegates here.
set -u
cd "$(dirname "$0")/../.." || exit 1
fail=0
hit()  { printf 'FAIL: %s\n' "$1"; fail=1; }
want() { [ "$2" = "$3" ] || hit "$1: expected $2, found $3"; }
num()  { tr -d '[:space:]'; }   # BSD wc pads its output.

# Every byte ASCII (Cut list 1 and 9), in the skill and in the hooks. In the C
# locale a byte over 0x7F is neither printable nor space, on GNU and BSD grep.
inc="--include=*.md --include=*.py --include=*.sh --include=*.ps1 --include=*.json"
LC_ALL=C grep -rn $inc '[^[:print:][:space:]]' . ../../hooks && hit "non-ASCII byte present (Cut list 1 and 9)"
grep -rnE $inc '^Co-[Aa]uthored-[Bb]y:' . ../../hooks && hit "AI trailer present (Cut list 10)"

# Counts this skill asserts about itself.
want "shape rules"     10 "$(awk '/^## Shape/,/^## Build/'         SKILL.md | grep -cE '^[0-9]+\. \*\*' | num)"
want "build rules"      5 "$(awk '/^## Build/,/^## Cut list/'      SKILL.md | grep -cE '^[0-9]+\. \*\*' | num)"
want "cut list items"  10 "$(awk '/^## Cut list/,/^Full catalog/'  SKILL.md | grep -cE '^[0-9]+\. ' | num)"
ids=$(grep -oE '^### [0-9]+\. ' references/deslop.md | tr -dc '0-9\n')
[ "$ids" = "$(printf '%s\n' "$ids" | sort -n | uniq)" ] || hit "deslop pattern ids must be unique and ascending"
want "ideate frames"   15 "$(awk '/^## Frames/,/^## Output/' references/ideate.md | grep -cE '^\| \*\*' | num)"

# Spec budgets.
# The router's cost is bytes, not lines. A line budget bought compression that
# cost clarity; the length cap stops a long line from gaming the byte budget.
n=$(wc -c < SKILL.md | num)
[ "$n" -le 16000 ] || hit "SKILL.md is $n bytes, over the 16000 budget (about 4k tokens)"
awk 'length($0) > 100 && $0 !~ /^\|/ && $0 !~ /^   / { print FILENAME":"NR": prose line is "length($0)" chars, over 100" }' SKILL.md | while read -r l; do hit "$l"; done
d=$(awk '/^description: >/,/^license:/' SKILL.md | sed '1d;$d' | tr -d '\n' | tr -s ' ' | wc -c | num)
[ "$d" -le 1024 ] || hit "description is $d chars, over the 1024 cap"

# References named in the table exist, and every reference is named.
for f in $(grep -oE '`references/[a-z-]+\.md`' SKILL.md | sed 's#`references/##; s#`##' | sort -u); do
  [ -f "references/$f" ] || hit "SKILL.md points at missing references/$f"
done
for f in references/*.md; do
  grep -q "\`references/$(basename "$f")\`" SKILL.md || hit "$f exists but SKILL.md never points at it"
done

# Mode commands: every routed reference has a skills/black-iris-<mode>/ folder
# that names it, and every such folder points at a reference that exists.
for d in ../black-iris-*/; do
  d=${d%/}; n=$(basename "$d")
  [ -f "$d/SKILL.md" ] || { hit "$n/ has no SKILL.md"; continue; }
  grep -q "^name: $n\$" "$d/SKILL.md" || hit "$n/SKILL.md name does not match its folder"
  grep -q 'disable-model-invocation: true' "$d/SKILL.md" || hit "$n/SKILL.md must set disable-model-invocation: true"
  for f in $(grep -oE '`\.\./black-iris/references/[a-z-]+\.md`' "$d/SKILL.md" | sed 's#.*/##; s#`##'); do
    [ -f "references/$f" ] || hit "$n/SKILL.md points at missing references/$f"
  done
done
for f in $(grep -oE '`references/[a-z-]+\.md`' SKILL.md | sed 's#`references/##; s#`##' | sort -u); do
  [ "$f" = evals.md ] && continue
  grep -lq "\`\.\./black-iris/references/$f\`" ../black-iris-*/SKILL.md 2>/dev/null || hit "references/$f is routed but has no skills/black-iris-<mode>/ command"
done

# Hook files parse.
h=../../hooks
[ -f "$h/hooks.json" ] && { python3 -c 'import json,sys;json.load(open(sys.argv[1]))' "$h/hooks.json" 2>/dev/null || hit "hooks.json is not valid JSON"; }
[ -f "$h/reinject.sh" ] && { sh -n "$h/reinject.sh" || hit "reinject.sh has a syntax error"; }

[ "$fail" = 0 ] && echo clean
exit "$fail"
