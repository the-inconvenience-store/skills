#!/usr/bin/env bash
# Run with Bash from any directory. Only the printed temporary directory is changed.
set -euo pipefail

script=${BASH_SOURCE[0]}
[[ $script == */* ]] || script=./$script
audit=$(CDPATH= cd -- "${script%/*}" && pwd -P)/worktree-audit.sh
repo_env=$(git rev-parse --local-env-vars)
for name in $repo_env; do unset "$name"; done
export LC_ALL=C GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_ALLOW_PROTOCOL=

sandbox=$(mktemp -d)
sandbox=$(cd "$sandbox" && pwd -P)
printf 'Fixture: %s\n' "$sandbox"
repo="$sandbox/main tree"
odd="$sandbox/"$'ancestor with space\tand\nnewline\n'

commit() {
  git -C "$1" -c user.name=Fixture -c user.email=fixture@example.invalid commit -qm "$2" "${@:3}"
}

fail() {
  printf 'worktree-audit.test: %s\n' "$1" >&2
  exit 1
}

expect_row() {
  local prefix suffix line
  printf -v prefix '%s\t%s\t%s\t%s\t' "$1" "$2" "$3" "$4"
  printf -v suffix '\t%q\t%q' "$5" "$6"
  while IFS= read -r line; do
    [[ $line == "$prefix"*"$suffix" ]] && return 0
  done <<< "$output"
  fail "expected row: $prefix...$suffix"
}

git init -q -b integration "$repo"
commit "$repo" base --allow-empty
git -C "$repo" worktree add -qb ancestor "$odd"
git -C "$repo" worktree add -qb current "$sandbox/current tree"
mkdir "$sandbox/current tree/nested"
git -C "$repo" worktree add -qb dirty "$sandbox/dirty tree"
printf 'untracked\n' > "$sandbox/dirty tree/keep.txt"
git -C "$repo" worktree add -qb ignored "$sandbox/ignored tree"
printf '/ignored.txt\n' > "$repo/.git/info/exclude"
printf 'ignored\n' > "$sandbox/ignored tree/ignored.txt"
git -C "$repo" worktree add -qb locked "$sandbox/locked tree"
git -C "$repo" worktree lock "$sandbox/locked tree"
git -C "$repo" worktree add -q --detach "$sandbox/detached tree"
git -C "$repo" worktree add -qb squashed "$sandbox/squashed tree"
printf 'squash me\n' > "$sandbox/squashed tree/change.txt"
git -C "$sandbox/squashed tree" add change.txt
commit "$sandbox/squashed tree" feature
git -C "$repo" merge -q --squash squashed
commit "$repo" squash

before=$(git -C "$repo" worktree list --porcelain)
output=$(cd "$sandbox/current tree/nested" && bash "$audit" -b refs/heads/integration "$repo")
printf '%s\n' "$output"
base_commit=$(git -C "$repo" rev-parse --verify HEAD)
[[ $output == "# Base: refs/heads/integration ($base_commit)"$'\n'* ]] || fail 'expected the pinned integration commit'
expect_row main,anchor clean ancestor hold refs/heads/integration "$repo"
expect_row current clean ancestor hold refs/heads/current "$sandbox/current tree"
expect_row - clean ancestor review-candidate refs/heads/ancestor "$odd"
expect_row - dirty ancestor hold refs/heads/dirty "$sandbox/dirty tree"
expect_row - dirty ancestor hold refs/heads/ignored "$sandbox/ignored tree"
expect_row locked clean ancestor hold refs/heads/locked "$sandbox/locked tree"
expect_row detached,no-branch clean ancestor hold - "$sandbox/detached tree"
expect_row - clean not-ancestor hold refs/heads/squashed "$sandbox/squashed tree"
[[ $(git -C "$repo" worktree list --porcelain) == "$before" ]] || fail 'worktree registrations changed'
[[ $(< "$sandbox/dirty tree/keep.txt") == untracked ]] || fail 'untracked contents changed'
[[ $(< "$sandbox/ignored tree/ignored.txt") == ignored ]] || fail 'ignored contents changed'
if missing=$(bash "$audit" -b refs/heads/missing "$repo" 2>/dev/null) || [[ -n $missing ]]; then
  fail 'a missing base must fail without inventory output'
fi
printf 'OK: offline worktree audit\n'
