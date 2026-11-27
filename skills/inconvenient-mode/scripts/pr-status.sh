#!/usr/bin/env bash

usage() {
  printf 'Usage: bash pr-status.sh [host/]owner/repo <pr-number>\n'
}

if [[ $# -eq 1 && $1 == --help ]]; then
  usage
  exit 0
fi

if [[ $# -ne 2 || ! $1 =~ ^([[:alnum:]][[:alnum:].-]*/)?[[:alnum:]][[:alnum:]-]*/[[:alnum:]_.-]+$ || ! $2 =~ ^[1-9][0-9]*$ ]]; then
  usage >&2
  exit 64
fi

if ! command -v gh >/dev/null 2>&1; then
  printf 'pr-status: GitHub CLI (gh) is required\n' >&2
  exit 127
fi

fields=number,url,state,mergedAt,isDraft,headRefName,headRefOid,baseRefName,baseRefOid,mergeable,mergeStateStatus,reviewDecision,statusCheckRollup
GH_PROMPT_DISABLED=1 GH_PAGER=cat exec gh pr view "$2" --repo "$1" --json "$fields" </dev/null
