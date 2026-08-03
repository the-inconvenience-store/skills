# Issue tracker: Beads

Issues and specs (you may know a spec as a PRD) for this repo live in its repo-local [Beads](https://github.com/steveyegge/beads) database. Use the `bd` CLI for all operations.

## Conventions

- **Create an issue**: `bd create "<title>" --body-file -`. Pipe or use a heredoc for a multi-line body; add `--type`, `--labels`, or `--parent` as needed.
- **Read an issue**: `bd show <id> --json`, then `bd comments <id> --json` for its conversation history.
- **List issues**: `bd list --status open --json` with appropriate `--label`, `--type`, or `--parent` filters.
- **Comment on an issue**: `bd comment <id> "..."`
- **Apply / remove labels**: `bd label add <id> "..."` / `bd label remove <id> "..."`
- **Claim**: `bd update <id> --claim`
- **Close**: `bd close <id> --reason "..."`

Run commands from the repo so `bd` discovers the right database. Treat Beads IDs as opaque strings; don't assume they are numeric. If the repo is not initialized, ask before running `bd init`.

## When a skill says "publish to the issue tracker"

Create a Beads issue with `bd create`.

## When a skill says "fetch the relevant ticket"

Run `bd show <id> --json` and `bd comments <id> --json`.

## Wayfinding operations

Used by `/wayfinder`. The **map** is an epic bead with **child** beads as tickets.

- **Map**: an epic labelled `wayfinder:map`, holding the Notes / Decisions-so-far / Fog body. Create it with `bd create "<title>" --type epic --labels wayfinder:map --body-file -`.
- **Child ticket**: a task created with `bd create "<question>" --type task --parent <map> --no-inherit-labels --labels wayfinder:<type> --body-file -`, where `<type>` is `research`, `prototype`, `grilling`, or `task`.
- **Blocking**: Beads' native dependency edge. `bd dep add <child> <blocker>` means the child is blocked by the blocker. A ticket is unblocked when every blocker is closed.
- **Frontier query**: `bd ready --parent <map> --unassigned --sort oldest --json` lists the open, unblocked, unclaimed children in creation order.
- **Claim**: `bd update <id> --claim` — the session's first write.
- **Resolve**: `bd comment <id> "<answer>"`, then `bd close <id>`, then add the context pointer (gist + ticket ID) to the map with `bd comment <map> "<pointer>"`.
