#!/usr/bin/env bash
#
# Advisory complexity nudge — a post-edit agent hook.
#
# Runs the project's own linter against the file that was just edited, and if a
# complexity or size budget is over, hands the agent a short note saying so and
# what to do about it. Silent when nothing is over budget.
#
# Two rules this script must never break:
#   1. It never fails the tool call. Every failure path exits 0.
#   2. It never nudges twice about the same function in one session, so it
#      cannot nag an agent into a refactor loop.
#
# Thresholds are NOT defined here — it invokes the project's real linter with
# the project's real config, so the numbers always match what CI enforces.
#
# Usage:
#   Hook mode:   receives the harness's JSON payload on stdin.
#   Manual mode: complexity-nudge.sh path/to/file.ts
#
# Adapt before shipping: the stdin field names and the stdout response shape
# differ per harness, and the harnesses change. See agent-hooks.md.

set -uo pipefail   # deliberately no -e: a hook that dies must still exit 0

# --------------------------------------------------------------------------
# 1. Find the edited file
# --------------------------------------------------------------------------

payload=""
if [ $# -gt 0 ]; then
  file_path="$1"
else
  payload=$(cat 2>/dev/null || true)
  # Field names by harness: Claude Code and Codex nest under tool_input;
  # Cursor puts file_path at the top level. Try each, take the first hit.
  file_path=$(printf '%s' "$payload" | jq -r '
    .tool_input.file_path // .file_path // .tool_input.path //
    .tool_input.filePath // (.edits[0]?.file_path) // empty
  ' 2>/dev/null || true)
fi

[ -n "${file_path:-}" ] || exit 0
[ -f "$file_path" ] || exit 0

# --------------------------------------------------------------------------
# 2. Locate the repo, and a scratch dir for the once-per-function state
# --------------------------------------------------------------------------

repo_root="${CLAUDE_PROJECT_DIR:-}"
if [ -z "$repo_root" ]; then
  repo_root=$(git -C "$(dirname "$file_path")" rev-parse --show-toplevel 2>/dev/null || pwd)
fi

session=$(printf '%s' "${payload:-}" | jq -r '.session_id // .conversation_id // "manual"' 2>/dev/null || echo manual)
state_file="${TMPDIR:-/tmp}/complexity-nudge-${session//[^A-Za-z0-9_-]/_}"
touch "$state_file" 2>/dev/null || state_file=""

# --------------------------------------------------------------------------
# 3. Ask the project's linter — findings as: line<TAB>rule<TAB>message
# --------------------------------------------------------------------------

findings=""

case "$file_path" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs)
    oxlint="$repo_root/node_modules/.bin/oxlint"
    [ -x "$oxlint" ] || exit 0
    findings=$(
      "$oxlint" --config "$repo_root/.oxlintrc.json" --format json "$file_path" 2>/dev/null |
      jq -r '
        .diagnostics[]?
        | select(.code | test("complexity|cognitive|max-lines-per-function|max-depth|max-nested-callbacks"))
        | [(.labels[0].span.line | tostring), .code, .message] | @tsv
      ' 2>/dev/null || true
    )
    ;;

  *.go)
    command -v golangci-lint >/dev/null 2>&1 || exit 0
    run=(golangci-lint run
         --enable-only=cyclop,gocognit,funlen,nestif,maintidx
         --issues-exit-code=0
         --output.json.path=stdout
         "$(dirname "$file_path")")
    # Go analysis loads a type graph, so cap it — a slow hook is a deleted hook.
    command -v timeout >/dev/null 2>&1 && run=(timeout 25s "${run[@]}")
    abs_path=$(cd "$(dirname "$file_path")" && pwd)/$(basename "$file_path")
    findings=$(
      "${run[@]}" 2>/dev/null |
      jq -r --arg f "$abs_path" --arg b "$(basename "$file_path")" '
        .Issues[]?
        | select((.Pos.Filename == $f) or (.Pos.Filename | endswith($b)))
        | [(.Pos.Line | tostring), .FromLinter, .Text] | @tsv
      ' 2>/dev/null || true
    )
    ;;

  *) exit 0 ;;
esac

[ -n "$findings" ] || exit 0

# --------------------------------------------------------------------------
# 4. Name the offending function, and drop anything already nudged about
# --------------------------------------------------------------------------

name_at_line() {
  local line
  line=$(sed -n "${1}p" "$file_path" 2>/dev/null || true)
  local name
  name=$(printf '%s' "$line" | sed -nE \
    -e 's/.*func[[:space:]]+\([^)]*\)[[:space:]]*([[:alnum:]_]+).*/\1/p' \
    -e 's/.*func[[:space:]]+([[:alnum:]_]+).*/\1/p' \
    -e 's/.*function[[:space:]]+([[:alnum:]_$]+).*/\1/p' \
    -e 's/.*(const|let|var)[[:space:]]+([[:alnum:]_$]+).*/\2/p' | head -1)
  printf '%s' "$name"
}

notes=""
while IFS=$'\t' read -r line rule message; do
  [ -n "${line:-}" ] || continue

  name=$(name_at_line "$line")
  where="${name:+$name() }at $(basename "$file_path"):${line}"

  key="${file_path}|${name:-$line}|${rule}"
  if [ -n "$state_file" ] && grep -qxF "$key" "$state_file" 2>/dev/null; then
    continue   # already said this once; saying it again is nagging
  fi
  [ -n "$state_file" ] && printf '%s\n' "$key" >> "$state_file"

  notes+="  - ${where} — ${message} [${rule}]"$'\n'
done <<< "$findings"

[ -n "$notes" ] || exit 0

# --------------------------------------------------------------------------
# 5. Nudge — advisory, specific, and with an explicit way to decline
# --------------------------------------------------------------------------

read -r -d '' nudge <<EOF || true
Complexity budget exceeded in code you just edited:

${notes}
This is advisory — it will not fail the build or block the commit. Fix it now
while the code is fresh, or say in one line why it stays.

What usually works, in order:
  1. Extract the body of the largest branch into a named function. The name is
     the point: it says what the branch is for, which the condition does not.
  2. Replace an if/else ladder over one value with a lookup table or a switch.
  3. Hoist the error and edge cases into guard clauses that return early, so
     the happy path runs down the left margin with no nesting.
  4. If the function is doing two jobs, split it at the seam between them.

Leave it alone when the branching is essential and already flat — a dispatch
table, a parser, an exhaustive switch over a closed set. Hiding that behind
indirection to satisfy a counter makes the code worse, not better. Say so and
move on.
EOF

# Emit the fields the major harnesses read. Each ignores keys it doesn't know,
# so one object serves all of them. Exit 0 — this is a nudge, not a gate.
jq -n --arg msg "$nudge" '{
  continue: true,
  systemMessage: $msg,
  agentMessage: $msg,
  hookSpecificOutput: {
    hookEventName: "PostToolUse",
    additionalContext: $msg
  }
}' 2>/dev/null || printf '%s\n' "$nudge"

exit 0
