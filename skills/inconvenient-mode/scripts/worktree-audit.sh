#!/usr/bin/env bash
# Inventory Git worktrees without changing them. Run with Bash and a Git that
# supports `worktree list --porcelain -z`.
set -uo pipefail

usage() {
  printf '%s\n' 'Usage: bash worktree-audit.sh (-b|--base) <integration-ref> [--] [repo-path]' \
    'The base must resolve to a locally available commit. No fetch is performed.' \
    'The repo path defaults to the current directory.'
}

fail() {
  printf 'worktree-audit: %s\n' "$1" >&2
  exit 1
}

base=
while (($#)); do
  case $1 in
    -b|--base)
      if (($# < 2)) || [[ -n $base || -z $2 || $2 == -* ]]; then
        usage >&2
        exit 2
      fi
      base=$2
      shift 2
      ;;
    -h|--help) usage; exit 0 ;;
    --) shift; break ;;
    -*) usage >&2; exit 2 ;;
    *) break ;;
  esac
done
if [[ -z $base ]] || (($# > 1)); then
  usage >&2
  exit 2
fi
repo=${1:-.}

# Discover each checkout from disk, not from inherited hook/repo overrides.
repo_env=$(git rev-parse --local-env-vars) || fail 'cannot read Git environment names'
for name in $repo_env; do unset "$name"; done
# Older Git can ignore GIT_NO_LAZY_FETCH. Also block every transport.
export LC_ALL=C GIT_OPTIONAL_LOCKS=0 GIT_NO_LAZY_FETCH=1 GIT_ALLOW_PROTOCOL= GIT_NO_REPLACE_OBJECTS=1

# The sentinel preserves paths ending in newlines through command substitution.
git_path() {
  local value
  value=$(git -C "$1" rev-parse --path-format=absolute "$2" && printf '.') || return 1
  printf '%s.' "${value%$'\n.'}"
}

common_dir=$(git_path "$repo" --git-common-dir 2>/dev/null) || fail 'cannot locate the selected Git repository'
common_dir=${common_dir%.}
base_oid=$(git -C "$repo" rev-parse --verify --quiet --end-of-options "$base^{commit}") ||
  fail "integration ref is not a locally available commit: $(printf '%q' "$base")"
shallow=$(git -C "$repo" rev-parse --is-shallow-repository 2>/dev/null) || shallow=unknown
current=$(git_path . --show-toplevel 2>/dev/null) || current=
current=${current%.}
anchor=$(git_path "$repo" --show-toplevel 2>/dev/null) || anchor=
anchor=${anchor%.}

status_evidence() {
  local root common observed changes index
  root=$(git_path "$1" --show-toplevel 2>/dev/null) || { printf 'unknown-checkout'; return; }
  common=$(git_path "$1" --git-common-dir 2>/dev/null) || { printf 'unknown-checkout'; return; }
  if [[ ! ${root%.} -ef $1 || ! ${common%.} -ef $common_dir ]]; then
    printf 'unknown-checkout'; return
  fi
  observed=$(git -C "$1" rev-parse --verify --quiet HEAD 2>/dev/null) || { printf 'unknown-head'; return; }
  if [[ $observed != "$2" ]]; then printf 'changed-head'; return; fi

  # Status can invoke arbitrary configured clean filters. Hold instead. Disable
  # fsmonitor hooks and do not inspect submodule files with their own config.
  git -C "$1" config --get-regexp '^filter\..*\.(clean|process)$' >/dev/null 2>&1
  case $? in
    0) printf 'unknown-filters'; return ;;
    1) ;;
    *) printf 'unknown-config'; return ;;
  esac
  changes=$(git -C "$1" -c core.fsmonitor=false status --porcelain=v1 \
    --untracked-files=normal --ignored=matching --ignore-submodules=dirty 2>/dev/null) || { printf 'unknown-status'; return; }
  if [[ -n $changes ]]; then printf 'dirty'; return; fi

  # Status can omit edits under these index flags and inside submodules.
  index=$(git -C "$1" ls-files --stage -v 2>/dev/null) || { printf 'unknown-index'; return; }
  case $'\n'"$index" in
    *$'\n'[a-zS]' '*) printf 'unknown-index-flags' ;;
    *$'\n'?' 160000 '*) printf 'unknown-submodules' ;;
    *) printf 'clean' ;;
  esac
}

ancestry_evidence() {
  if [[ -z $1 || -e $common_dir/info/grafts ]]; then printf 'unknown'; return; fi
  git -C "$repo" merge-base --is-ancestor "$1" "$base_oid" 2>/dev/null
  case $? in
    0) printf 'ancestor' ;;
    1) if [[ $shallow == false ]]; then printf 'not-ancestor'; else printf 'unknown'; fi ;;
    *) printf 'unknown' ;;
  esac
}

inventory() {
  local field path= head= branch= flags= first=1 status ancestry assessment
  while IFS= read -r -d '' field; do
    case $field in
      'worktree '*)
        [[ -z $path ]] || return 1
        path=${field#worktree }
        ;;
      'HEAD '*) head=${field#HEAD } ;;
      'branch '*) branch=${field#branch } ;;
      bare|detached|locked|locked\ *|prunable|prunable\ *)
        flags=${flags:+$flags,}${field%% *}
        ;;
      '')
        [[ -n $path ]] || return 1
        if ((first)); then flags=${flags:+$flags,}main; first=0; fi
        if [[ -n $current && $path -ef $current ]]; then flags=${flags:+$flags,}current; fi
        if [[ -n $anchor && $path -ef $anchor ]]; then flags=${flags:+$flags,}anchor; fi
        if [[ -z $branch ]]; then flags=${flags:+$flags,}no-branch; fi
        case ,$flags, in
          *,bare,*|*,prunable,*) status=not-checked ;;
          *) status=$(status_evidence "$path" "$head") ;;
        esac
        ancestry=$(ancestry_evidence "$head")
        assessment=hold
        if [[ -z $flags && $status == clean && $ancestry == ancestor ]]; then
          assessment=review-candidate
        fi
        printf '%s\t%s\t%s\t%s\t%q\t%q\t%q\n' \
          "${flags:--}" "$status" "$ancestry" "$assessment" "${head:--}" "${branch:--}" "$path"
        path= head= branch= flags=
        ;;
      *) flags=${flags:+$flags,}unknown-record ;;
    esac
  done
  [[ -z $field && -z $path ]] && ((!first))
}

printf '# Base: %q (%s)\n' "$base" "$base_oid"
printf 'FLAGS\tSTATUS\tANCESTRY\tASSESSMENT\tHEAD\tBRANCH\tWORKTREE\n'
if ! git -C "$repo" worktree list --porcelain -z | inventory; then
  fail 'worktree inventory incomplete; disregard the rows above'
fi
