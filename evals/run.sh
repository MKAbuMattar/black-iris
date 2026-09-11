#!/usr/bin/env bash
# Collect responses for one condition. Judging is a separate step, on purpose:
# the judge must be a different model family from the one under test, and this
# script has no business picking it.
#
#   ./evals/run.sh baseline   claude-opus-5
#   ./evals/run.sh treatment  claude-opus-5
#
# Writes evals/out/<condition>/<case id>.md, each wrapped in judge markers so
# the judge sees the response and nothing that names the condition.
#
# Isolation, per references/evals.md:
#   - same pinned model for both conditions, passed as argument 2
#   - a neutral working directory outside this repo, so the CLI cannot read
#     the skill's own files or a CLAUDE.md as project context
#   - settings and skills cleared for the baseline, so an always-on flag or a
#     user skill cannot leak into it
#   - tools denied unless the case asks for them; those cases are scored apart
set -u

cond="${1:?usage: run.sh <baseline|treatment> <model>}"
model="${2:?usage: run.sh <baseline|treatment> <model>}"
repo="$(cd "$(dirname "$0")/.." && pwd)"
out="$repo/evals/out/$cond"
mkdir -p "$out"

case "$cond" in
  baseline|treatment) ;;
  *) echo "condition must be baseline or treatment"; exit 2 ;;
esac

command -v claude >/dev/null || { echo "claude CLI not on PATH"; exit 2; }
command -v python3 >/dev/null || { echo "python3 not on PATH"; exit 2; }

work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT
echo "condition: $cond   model: $model"
echo "workdir:   $work   (neutral, outside the repo)"

n=0
while IFS=$'\t' read -r id tools prompt; do
  [ -n "$id" ] || continue
  n=$((n + 1))
  args="--setting-sources "
  [ "$tools" = "none" ] && args="$args --disallowed-tools Bash,Write,Edit,Read,Glob,Grep"
  if [ "$cond" = "treatment" ]; then
    prompt="/black-iris $prompt"
    # The treatment needs the skill loaded; the baseline must not have it.
    args="--setting-sources user,project"
  fi
  printf '  %-12s ' "$id"
  body="$( cd "$work" && printf '%s' "$prompt" | claude -p --model "$model" $args 2>&1 )"
  {
    echo "<!-- judge:begin -->"
    printf '%s\n' "$body"
    echo "<!-- judge:end -->"
  } > "$out/$id.md"
  echo "ok"
done < <(python3 "$repo/evals/cases.py" tsv)

echo "wrote $n responses to $out"
echo
echo "Next, and not automatic: judge these with a model from a DIFFERENT"
echo "family than $model. Send the judge only the text between the markers"
echo "plus the case's checks from cases.jsonl. Randomize which condition it"
echo "sees first. Then write evals/RESULTS.md with model, date, n, and every"
echo "failed case by name."
