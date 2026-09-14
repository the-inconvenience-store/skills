---
name: setup-inconvenient-skills
description: Configure a repo for the engineering skills — issue tracking, triage labels, domain docs, development guardrails, and repeatable real-surface verification. Run once before first use of the other engineering skills.
disable-model-invocation: true
---

# Setup Inconvenient Skills

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub by default; GitLab, Beads, and local markdown are also supported out of the box)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them
- **Guardrails** — the approved lint, format, test, reproducible setup, dependency, CI, and hook baseline
- **Verification** — the project-local route for launching, driving, proving, and cleaning up each real user-facing surface

This is a prompt-driven setup, not a deterministic script. Explore, present what you found, confirm the repository-specific choices, write their shared configuration, then establish guardrails and verification through their owning skills.

## Process

### 1. Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` and `.git/config` — is this a GitHub repo? Which one?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and any `src/*/docs/adr/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use
- `.beads/` — sign that the repo uses the Beads (`bd`) issue tracker
- Is the `triage` skill installed? (a `triage` skill folder alongside this one, or `triage` in your available skills.) This decides whether Section B runs at all.
- Monorepo signals — a `pnpm-workspace.yaml`, a `workspaces` field in `package.json`, or a populated `packages/*` with its own `src/`. Present only in a genuinely large multi-package repo; their absence means single-context, which is almost every repo.

**Done when:** the tracker evidence, existing agent guidance, domain layout, prior setup output, triage availability, and monorepo shape are all accounted for.

### 2. Present findings and ask

Summarise what's present and what's missing. Then take the sections in order — one section, one answer, then the next.

Lead each section with the recommended answer so the user can accept it in a word. Give a one-line explainer only when the choice genuinely branches; skip the section entirely when exploration already settled it (Section B when `triage` isn't installed, Section C when there's no monorepo).

**Section A — Issue tracker.**

> Explainer: The "issue tracker" is where issues live for this repo. Skills like `to-tickets`, `triage`, and `to-spec` read from and write to it — they need to know whether to call `gh issue create`, call `bd create`, write a markdown file under `.scratch/`, or follow some other workflow you describe. Pick the place you actually track work for this repo.

Default posture: these skills were designed for GitHub. If `.beads/` exists, propose Beads. Otherwise, if a `git remote` points at GitHub, propose GitHub; if it points at GitLab (`gitlab.com` or a self-hosted host), propose GitLab. Otherwise (or if the user prefers), offer:

- **GitHub** — issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** — issues live in the repo's GitLab Issues (uses the [`glab`](https://gitlab.com/gitlab-org/cli) CLI)
- **Beads** — issues live in the repo-local Beads database (uses the [`bd`](https://github.com/steveyegge/beads) CLI)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

Record the choice in `docs/agents/issue-tracker.md`. The GitHub and GitLab templates carry a "PRs as a request surface" flag, defaulted **off** — leave it off and don't raise it; a user who wants external PRs in the triage queue can flip the flag in the file later.

**Section B — Triage label vocabulary.** Skip this section entirely if the `triage` skill isn't installed (exploration told you) — an uninstalled skill needs no labels.

If it is installed, ask exactly one question:

> Do you want to keep the default triage labels? (recommended: **yes**)

The defaults are the five canonical roles, each label string equal to its name: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. On **yes**, write them as-is. Only if the user says no — usually because their tracker already uses other names (e.g. `bug:triage` for `needs-triage`) — collect the overrides so `triage` applies existing labels instead of creating duplicates.

Then check which of the agreed label strings the tracker actually has (on GitHub, `gh label list`). `docs/agents/triage-labels.md` is only a mapping; writing it does not create anything. Name the missing ones and ask whether to create them, since that writes to the shared tracker. Step 4 does the creating.

**Section C — Domain docs.** Default to **single-context** — one `CONTEXT.md` + `docs/adr/` at the repo root. This fits almost every repo; write it without asking.

Offer **multi-context** — a root `CONTEXT-MAP.md` pointing to per-context `CONTEXT.md` files — only when exploration found monorepo signals. Then confirm which layout they want.

**Done when:** the issue tracker, applicable triage vocabulary, and domain-doc layout are each confirmed by the user or settled by the stated repository default.

### 3. Confirm and edit

Show the user a draft of:

- The configuration portion of the `## Agent skills` block to add to whichever of `CLAUDE.md` / `AGENTS.md` is being edited (see step 4 for selection rules). The verified runtime pointer is added later by step 6.
- The contents of `docs/agents/issue-tracker.md`, `docs/agents/domain.md`, and `docs/agents/triage-labels.md` (the last only when `triage` is installed)

Let them edit before writing.

**Done when:** the user has approved the exact configuration block and every applicable configuration document.

### 4. Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

The block:

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.
```

Include the `### Triage labels` sub-block, and write `docs/agents/triage-labels.md`, only when `triage` is installed and Section B ran. When it isn't, both are omitted.

Then write the docs files using the seed templates in this skill folder as a starting point:

- [issue-tracker-github.md](./issue-tracker-github.md) — GitHub issue tracker
- [issue-tracker-gitlab.md](./issue-tracker-gitlab.md) — GitLab issue tracker
- [issue-tracker-beads.md](./issue-tracker-beads.md) — Beads issue tracker
- [issue-tracker-local.md](./issue-tracker-local.md) — local-markdown issue tracker
- [triage-labels.md](./triage-labels.md) — label mapping (only if `triage` is installed)
- [domain.md](./domain.md) — domain doc consumer rules + layout

For "other" issue trackers, write `docs/agents/issue-tracker.md` from scratch using the user's description.

**Create the labels the user approved in Section B.** On GitHub that is `gh label create "<name>" --force` per missing string; other trackers use their own command. This matters because GitHub rejects `gh issue create --label <missing>` outright rather than creating the label, so an uncreated label means `/triage` and `/to-tickets` lose the whole write, not just the label. If `/wayfinder` is installed, create its labels too: `wayfinder:map`, `wayfinder:research`, `wayfinder:prototype`, `wayfinder:grilling`, `wayfinder:task`. Where the tracker has no label concept (local markdown), there is nothing to create — the role strings live in each file's `Status:` line.

**Done when:** the chosen agent file contains one current `## Agent skills` block, every approved configuration document exists under `docs/agents/`, and every approved label string either already existed in the tracker or was created.

### 5. Establish guardrails

After the chosen agent file and every applicable `docs/agents/*.md` file have been written, call the Skill tool with `guardrails`. Run that workflow through proposal, approval, implementation, and verification before continuing.

**Done when:** the approved project guardrails work and every guardrail verification gap is named.

### 6. Establish real-surface verification

Call the Skill tool with `verification` after guardrails are complete, so it sees the repository's final launch and check commands. Request Create for a missing `docs/agents/verification/` artifact; the verification skill routes an existing artifact to Maintain. Let that skill own the artifact format, repository interview, feature map, live drive, evidence, and cleanup.

After the verification artifact is proved, update the existing `## Agent skills` block with this pointer:

```markdown
### Verification

Follow `docs/agents/verification/README.md` to launch and doctor each real user-facing surface, drive its public path, capture evidence, and clean up.
```

Preserve the rest of the approved block and do not add the pointer before the target exists.

**Done when:** `docs/agents/verification/README.md` exists, one mapped feature is `VERIFIED` by following it, and the chosen agent file points to it.

### 7. Done

Tell the user the setup is complete and name the configuration, guardrails, and verification artifacts now available to the engineering skills. Mention the maintenance paths: edit tracker or domain config directly, call `guardrails` when the quality strategy changes, and call `verification` with Maintain when application surfaces move.

**Done when:** the final report names every created or updated setup surface and any unresolved guardrail or verification gap.
