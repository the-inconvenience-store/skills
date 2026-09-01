# Agent hooks

Hooks that fire inside the **agent's** loop, not git's: a script the harness runs every time the agent edits a file, or finishes a turn, or tries to touch something it shouldn't.

The framing that decides what goes where:

- **Agent hooks are the inner loop.** They fire dozens of times per turn, on partial and mid-refactor code. Put work here that is fast, deterministic, and correct on an incomplete file.
- **Git hooks are the outer gate.** They fire once, on code the author is claiming is finished. Put the verdicts here.

Mixing those up is the failure mode this file exists to prevent: a lint check on every edit derails the turn, and a formatter that only runs at commit time means every diff carries formatting noise the agent had to be told about.

This step is **optional** and per-developer. Agent hooks configure a person's tooling, not the repo's build, so a project can be fully set up without them. Ask before writing anything into `.claude/`, `.codex/`, or `.cursor/`.

## What to install

Three things, in descending order of how often the answer is yes:

| Hook | Default | Why |
| --- | --- | --- |
| **Format on file edit** | **yes** | Nearly free, and it removes an entire class of noise from every diff |
| **Block edits to generated code** | **yes, if the project has a code generator** | An agent editing generated output produces work that vanishes on the next `go generate` |
| **Complexity nudge on file edit** | **offer it** | A budget the agent hears about while the code is fresh, not at commit |
| **Lint on file edit** | **no** — see below | Usually derails the turn. Lint at end-of-turn or at commit instead |

## Where hooks live

Every major harness now has hooks, and they have converged on almost the same shape: a JSON file listing events, each event holding matchers and commands, each command receiving a JSON payload on **stdin** and signalling a block through **exit code 2** or a JSON decision on stdout.

| Harness | Config | File-edit event | Docs |
| --- | --- | --- | --- |
| Claude Code | `.claude/settings.json` (project) or `~/.claude/settings.json` | `PostToolUse` with matcher `Edit\|Write`; `PreToolUse` to block | <https://code.claude.com/docs/en/hooks> |
| Codex | `.codex/hooks.json` or `[hooks]` in `.codex/config.toml` | `PostToolUse` matching `apply_patch` (aliases: `Edit`, `Write`); `PreToolUse` to block | <https://learn.chatgpt.com/docs/hooks> |
| Cursor | `.cursor/hooks.json` | `afterFileEdit`; `beforeShellExecution` / `beforeReadFile` to block | <https://cursor.com/docs/agent/hooks> |

**Read the harness's docs before writing the config.** These systems are young and moving — Codex's hooks shipped recently and its feature flag and event coverage have already changed once; Cursor's schema carries an explicit `version` field. Ask the user which harnesses to configure rather than writing all three, and configure only what you can verify against current docs.

Two things to check per harness, because they differ and both are load-bearing:

- **Whether the file-edit event fires at all.** Codex historically fired `PreToolUse`/`PostToolUse` for Bash only; `apply_patch` support came later. If the harness doesn't fire on edits, the formatter hook simply cannot exist there — say so rather than writing a config that does nothing.
- **Where the edited file's path is in the payload.** Claude Code puts it at `tool_input.file_path`, Cursor at `file_path`. Getting this wrong produces a hook that silently formats nothing.

Project-level config is shared and checked in; user-level config is per-machine. **Default to project-level for the generated-code block** (it protects the repo, and everyone needs it) and let the user choose for the formatter (it is a preference, and some people have editor format-on-save already).

## Format on file edit

The highest-value hook and the easiest to get subtly wrong.

**On-edit formatting must be layout-only.** This is the rule that matters, and it is not obvious: a formatter that *removes* code is dangerous mid-turn. `goimports` prunes unused imports; `oxlint --fix` deletes unused variables. Between two edits, an import the agent just added is legitimately unused — the next edit was going to use it. Prune it and the agent's next edit fails to compile against a file it didn't write, and it spends the rest of the turn confused about why.

So split the work across the two loops:

| | On edit (agent hook) | On commit (git hook) |
| --- | --- | --- |
| TypeScript | `prettier --write`, or `oxfmt` | `oxlint --fix`, then the formatter |
| Go | `gofumpt -w` | `golangci-lint fmt` (gofumpt + goimports + gci) |

Three more properties the script needs:

- **Exit 0 no matter what.** A formatter fails on syntactically invalid code, and mid-edit code is often invalid. A hook that reports that failure interrupts the agent with a problem the next edit was about to fix. Swallow it.
- **Touch only the edited file.** Never `--write .`; take the path from the payload.
- **Be fast.** It runs on every edit. Anything that loads a type graph is too slow for this loop.

A dispatch-on-extension script covers a polyglot repo:

```sh
#!/usr/bin/env bash
# .claude/hooks/format-file.sh
file=$(jq -r '.tool_input.file_path // empty')
[ -n "$file" ] && [ -f "$file" ] || exit 0

case "$file" in
  *.ts|*.tsx|*.js|*.jsx|*.mjs|*.cjs|*.json|*.css|*.md)
    npx --no -- prettier --write --ignore-unknown "$file" ;;
  *.go)
    gofumpt -w "$file" ;;
esac
exit 0    # never fail the edit
```

Wired up, per harness:

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/format-file.sh", "timeout": 30 }
        ]
      }
    ]
  }
}
```

```json
// .cursor/hooks.json
{
  "version": 1,
  "hooks": {
    "afterFileEdit": [{ "command": ".cursor/hooks/format-file.sh" }]
  }
}
```

Codex uses the same `hooks` / `matcher` / `type: "command"` shape as Claude Code in `.codex/hooks.json`, matching `apply_patch`. Its payload has no `CLAUDE_PROJECT_DIR` equivalent — use the `cwd` field from stdin, or an absolute path.

`chmod +x` the script. A non-executable hook fails silently in most harnesses, which looks exactly like a hook that isn't configured.

## Complexity nudge on file edit

The one lint-shaped check that does belong in the inner loop, because it is the exception to everything the next section says: a complexity budget is **not** a false positive on half-written code. A function that is 19 branches deep after this edit is 19 branches deep, whether or not the next edit lands.

It is also the check with the shortest useful half-life. Told now, the agent still has the function's structure in context and the fix is a two-minute extraction. Told at commit, across five files, it is a refactor nobody wants — which is why complexity findings are the ones that get `--no-verify`'d and then live forever.

[`scripts/complexity-nudge.sh`](../scripts/complexity-nudge.sh) implements it. Copy it into the project's hooks directory and wire it to the post-edit event:

```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/complexity-nudge.sh", "timeout": 30 }
        ]
      }
    ]
  }
}
```

Four things it does that a naive version doesn't, and all four are the reason it's worth copying rather than writing fresh:

- **It defines no thresholds.** It invokes the project's own linter with the project's own config, so the numbers it reports are exactly the ones CI enforces. A hook with its own hardcoded limit becomes a second, contradictory source of truth the first time someone tunes `.oxlintrc.json`.
- **It nudges once per function per session.** Every subsequent edit to the same file would otherwise re-report the same finding, and an agent nagged on every edit either refactors working code to make the noise stop or learns to ignore the channel. The dedup is what keeps it a nudge.
- **It says the finding is advisory, and names the fix.** "Complexity 19, max 12" tells an agent a number, not a move. The message lists the moves in order — extract the largest branch into a named function, replace the ladder with a lookup, hoist guards and return early, split at the seam.
- **It gives an explicit way to decline.** A flat dispatch table or an exhaustive switch scores badly and is correct as written; without permission to say so, an agent will hide it behind indirection and make the code worse. The message ends by telling it to leave that alone and say why.

**Rewrite it for the target project.** It is a starting point, not a drop-in: the stdin field names and stdout response shape differ per harness and both move between versions, the linter paths assume `node_modules/.bin/oxlint` and a `golangci-lint` on `PATH`, and the rule list is this skill's budget tier rather than whatever the project settled on. It handles TypeScript/JavaScript and Go; a third language needs a third `case` arm. Run it by hand against a known-complex file before wiring it up — `complexity-nudge.sh path/to/file.ts` works standalone.

It exits 0 on every path, including when the linter is missing, the payload is unparseable, or the file is a language it doesn't handle. A nudge that can fail an edit is worse than no nudge.

## Lint on file edit — usually don't

The tempting hook, and — for the *rest* of the rules — mostly a mistake.

An agent mid-refactor has a legitimately broken file between edits: a function extracted but not yet called, an import added before its use, a type widened before the callers catch up. Lint that state and the agent gets a real-looking error for a problem edit N+1 was already going to fix — so it stops, investigates, and often "fixes" something that wasn't broken. One noisy lint hook can burn a whole turn.

That is exactly what separates the complexity nudge above from a general lint hook: complexity is true about the file as it stands, while "unused variable" is a statement about work in progress.

Commit time is when the code is meant to be coherent. That is why `git-hooks.md` puts lint there.

**If the user wants lint feedback inside the loop, the right event is end-of-turn, not per-edit.** Every harness has one (`Stop` in Claude Code and Codex, `stop` in Cursor), and it fires exactly when the agent claims to be finished — which is the first moment its code is supposed to be coherent, and the last moment before a human looks at it. Blocking there (exit 2, with the lint output on stderr) sends the agent back to fix its own mess instead of yours:

```json
// .claude/settings.json
{
  "hooks": {
    "Stop": [
      { "hooks": [{ "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/lint-turn.sh", "timeout": 120 }] }
    ]
  }
}
```

```sh
#!/usr/bin/env bash
# .claude/hooks/lint-turn.sh — block the turn from ending on a lint failure
out=$(cd "$(git rev-parse --show-toplevel)" && npm run --silent lint 2>&1) || {
  echo "Lint failed — fix these before finishing:" >&2
  echo "$out" >&2
  exit 2
}
exit 0
```

Two things to say to the user before installing it. It **costs a full lint run on every turn**, so it only works if lint is fast — time it. And a `Stop` hook that blocks can loop: if the agent cannot fix the finding, it will keep trying. Keep the check narrow, and make sure the message says what to do.

The one class of check that genuinely belongs on **every edit** is the one that is never a false positive mid-refactor and never worth deferring: a secret written into source. If the project has `gitleaks` or similar, a `PreToolUse` hook that denies the write is worth more than a commit-time scan, because at commit time the secret is already on disk and in the agent's context.

## Block edits to generated code

Install this whenever the project has a code generator. An agent that edits generated output has done work that disappears at the next generate — and worse, it usually *looks* correct until someone regenerates and the fix silently reverts.

The value is entirely in the **denial message**. Blocking teaches nothing; blocking while naming the source file and the regenerate command turns a dead end into a redirect.

```sh
#!/usr/bin/env bash
# .claude/hooks/block-generated.sh
file=$(jq -r '.tool_input.file_path // empty')
[ -n "$file" ] || exit 0

deny() {
  jq -n --arg r "$1" '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:"deny",permissionDecisionReason:$r}}'
  exit 0
}

case "$file" in
  */db/*.sql.go|*/db/models.go|*/db/querier.go)
    deny "Generated by sqlc. Edit the query in db/query/*.sql or the schema in db/schema.sql, then run 'sqlc generate'." ;;
  *.pb.go|*.connect.go)
    deny "Generated from .proto. Edit the .proto definition, then run 'buf generate'." ;;
  */node_modules/.prisma/*|*/generated/prisma/*)
    deny "Generated by Prisma. Edit schema.prisma, then run 'prisma generate'." ;;
  *_gen.go|*_generated.go|*/mocks/*.go)
    deny "Generated file. Edit the source and re-run 'go generate ./...'." ;;
esac
exit 0
```

```json
// .claude/settings.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-generated.sh" }
        ]
      }
    ]
  }
}
```

Cursor blocks through `permission: "deny"` on its own events; Codex uses the same `permissionDecision` shape as Claude Code on `PreToolUse`. Check each harness's current output schema.

**Derive the path patterns from what the repo actually generates**, not from this list. Three places to look, in order:

1. **`.gitattributes`** — a `linguist-generated=true` entry is an existing, authoritative list of generated paths. If one exists, use it and skip the guessing.
2. **The generator's own config** — `sqlc.yaml`'s `out`, `buf.gen.yaml`'s output dirs, `schema.prisma`'s `generator` block, `.graphqlrc`, `openapi-generator` config, `gqlgen.yml`, `ent`'s target.
3. **`//go:generate` directives** and `go generate` targets, plus the file headers themselves — most generators write `// Code generated by X. DO NOT EDIT.` as the first line, which is both a detector and the exact string to cite back.

Common generators worth asking about: **Go** — sqlc, protobuf/buf, mockery, gomock, ent, gqlgen, `stringer`, wire. **Node** — Prisma, Drizzle Kit, GraphQL Code Generator, OpenAPI generators, Supabase type generation, `contentlayer`.

**Also exclude these paths from the linter.** If step 1 found generated code, both the block hook and the lint `ignorePatterns` / `exclusions` should cover the same paths — they are the same list, serving the same fact, and letting them drift means one of the two is wrong.

## Prove it works

A hook that silently does nothing is the default failure here, and it is indistinguishable from a hook that is working until the day it matters. Prove each one, the same way the rest of this skill proves a lint rule:

- **Formatter** — have the agent write a badly-formatted file, then read it back. It should already be formatted. Then write a syntactically broken file and confirm the edit still succeeds — that is the half that proves the hook fails open rather than blocking the agent on invalid input.
- **Generated-code block** — attempt an edit to a generated file. The block should fire, and the message should name the source file and the regenerate command. Then edit a normal file and confirm it goes through.
- **Complexity nudge** — edit a function that is genuinely over budget and confirm the note arrives naming that function. Edit it again and confirm the note does **not** repeat; that half proves the dedup, without which the hook becomes a nag. Then rename the linter binary out of the way and confirm the edit still succeeds silently.
- **Stop-hook lint**, if installed — leave a lint error in place and confirm the turn is blocked with the finding in the message, then fix it and confirm the turn ends.

Say in the report which harnesses were configured, where the config lives (project vs user), and that a teammate on a different harness has nothing installed — agent hooks are not shared the way a git hook is.
