#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 6 ]]; then
    printf 'Usage: bash log.sh <logfile> <phase> <decision> <why> <evidence> <result>\n' >&2
    exit 2
fi

logfile=$1
shift
mkdir -p -- "$(dirname -- "$logfile")"

clean() {
    local cell=$1
    cell=${cell//$'\t'/ }
    cell=${cell//$'\n'/ }
    cell=${cell//$'\r'/ }
    if [[ $cell =~ ^[[:space:]]*[=+@-] ]]; then
        cell="'$cell"
    fi
    printf '%s' "$cell"
}

ts=$(date -u +%Y-%m-%dT%H:%M:%SZ)
{
    if [[ ! -s $logfile ]]; then
        printf 'ts\tphase\tdecision\twhy\tevidence\tresult\n'
    fi
    printf '%s' "$ts"
    for cell in "$@"; do
        printf '\t'
        clean "$cell"
    done
    printf '\n'
} >> "$logfile"
