---
name: setup-project
description: Set up a project's guardrails — lint rules, a formatter, file-structure conventions, git hooks, and optional agent hooks — so agents working in it produce maintainable code. Detects the stack, then installs and proves a rule set.
disable-model-invocation: true
---

# Setup Project

Wire a repo's **guardrails**: the lint rules, formatter, structure conventions, and hooks that keep an agent's output readable and maintainable without a human reading every line.

Guardrails sit at three distances from the code, and the distance decides what belongs where. **Config** (lint rules, formatter) is checked every time anything runs. **Git hooks** are the outer gate — they fire once, on code the author says is finished. **Agent hooks** are the inner loop — they fire on every file edit, so only fast, deterministic work that is correct on a half-written file goes there.

A rule the linter enforces beats a paragraph in `CLAUDE.md`. Prose an agent can skip; a failing lint run it cannot. So the output of this skill is mostly **config**, and the completion criterion is that the config **bites** — you have watched a rule fail on a violation.

Guided and configurable, in that order: detect the stack, present what you found, confirm each choice, install, prove, document.

## Route

Step 1 detects the stack. Read the reference files it selects **before** writing any config.

| Read | When |
| --- | --- |
| [references/typescript.md](./references/typescript.md) | Any TypeScript or JavaScript code. The baseline for that ecosystem. |
| [references/react.md](./references/react.md) | React, Next.js, React Native, Expo, Remix/React Router, TanStack Start. Read **with** `typescript.md` — they go hand in hand and neither is complete alone. |
| [references/go.md](./references/go.md) | Any Go code. Self-contained — nothing from `typescript.md` carries over. |
| [references/dependency-rules.md](./references/dependency-rules.md) | Step 4 — the project depends on libraries with documented anti-patterns (Zod, Zustand, TanStack Query, Drizzle, …). |
| [references/git-hooks.md](./references/git-hooks.md) | Step 5 — unless the user declines git hooks. |
| [references/agent-hooks.md](./references/agent-hooks.md) | Step 6 — optional. Format-on-edit and generated-code guards inside the agent's own loop. |

**A polyglot repo reads every language file that matches**, and gets one config per ecosystem rather than one config for the repo. The umbrella `lint` command runs them all; the git hook dispatches on the staged file's extension.

An unlisted language — Python, Rust, Ruby, Java, C# — is **out of scope**. Say so plainly, set up the languages that are covered, and name the gap in the report. Don't improvise a rule set from memory for an ecosystem this skill has no reference file for.

Each reference file names the **upstream install docs** for every linter and plugin it recommends. Read those pages before configuring; option names and versions move. Two shortcuts worth knowing: oxlint publishes an LLM-optimised Markdown copy of every docs page (append `.md` to any `oxc.rs` URL), and golangci-lint's settings page carries a commented example for every linter option.

Never configure a linter from memory.

## Severity policy

**Fail the build, unless a reference file names the exception.** A finding that doesn't fail is a finding agents learn to scroll past.

The standing exception is the **budget** tier — complexity and size limits. These are nudges rather than defects: a 520-line file is a signal to split, not a broken build. Each language file names its own budget rules and how that tier is expressed, because the mechanism differs:

- **oxlint** has a real `"warn"` severity — `eslint/complexity` and `eslint/max-lines` ship as `"warn"`, everything else as `"error"`.
- **golangci-lint has no warn tier at all** — its `severity` block only annotates output, so every enabled linter fails the run. `go.md` covers the two ways to get budget semantics anyway.

Everything outside the budget tier blocks, in every language.

## The guardrails that matter most

Not every project needs every plugin, but most need most. When the user trims the list, defend the ones below. The first four are **kinds** of guardrail that every language file implements, because each stops a failure mode that is about how agents write code rather than about a language:

- **Complexity and size budgets** — what stops an agent growing sprawling god-files and deeply-branched functions. Two axes, because path-count and line-count both miss unreadable-but-simple code: a **cyclomatic** limit plus a **cognitive** one. TS: `eslint/complexity` (12) + `eslint/max-lines` (500) + `sonarjs/cognitive-complexity` (15). Go: `cyclop` (12) + `gocognit` (20) + `funlen` + `revive/file-length-limit`, optionally `maintidx` for the composite view.
- **Unfinished-work markers** — the `TODO`, the empty function, the `throw new Error("Not implemented")` / `panic("not implemented")` that lets an agent skip the hard part and look finished. TS: `eslint/no-warning-comments`. Go: `godox` + `forbidigo`.
- **Magic values** — TS: `eslint/no-magic-numbers`. Go: `mnd` + `goconst`.
- **Import boundaries** — the rule that keeps an architecture from eroding one import at a time. TS: `import/no-relative-parent-imports` + `no-restricted-imports` patterns. Go: `depguard`, plus `internal/`, which the compiler enforces for free.

Then the stack-specific standouts:

- **react.doctor** — roughly 880 React-specific rules, and the largest single win on any React codebase. `react.md` names a starting set per cluster and carries the two traps: its presets are ESLint-only, and a handful of catalogue rules are CLI-only and inert in `.oxlintrc.json`. Verify against the installed plugin, then extend with discretion.
- **`oxlint-tailwindcss` restrictions** — `no-hardcoded-colors`, `no-arbitrary-value`, `prefer-theme-tokens`, `prefer-scale-token`. What stops an agent inventing `bg-[#3b82f6]` instead of reaching for the design system.
- **anti-slop** — the TypeScript rules against type laundering (`as unknown as`, `unknown` params, runtime `typeof` guards).
- **`errorlint` and `nilerr`** — Go's equivalent blind spot: an error compared with `==` instead of `errors.Is`, or checked and then discarded. Both fail silently and only once something upstream starts wrapping.

## Process

### 1. Detect

Read the repo before touching it. Don't ask the user anything you can find out yourself.

**Every repo:**

- **Working tree** — `git status`. Unrelated changes are preserved, never stashed or reverted.
- **Languages present** — manifests first (`package.json`, `go.mod`, `go.work`, `Cargo.toml`, `pyproject.toml`), then the actual file-extension counts, which are what tell you whether a manifest is load-bearing or a leftover. A repo can be more than one language; note the share of each.
- **Repo shape** — **monorepo** or single-package. Node signals: `pnpm-workspace.yaml`, a `workspaces` field, `turbo.json`, `nx.json`, `lerna.json`. Go signals: `go.work`, or several `go.mod` files. List the packages or modules, and which are apps vs libraries.
- **Existing lint and format config** — for every ecosystem found. Read them; anything already configured is merged into, never overwritten.
- **Existing hooks and hook manager** — `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, `.overcommit.yml`, a `simple-git-hooks` key in `package.json`, `.vite-hooks/`, `git config core.hooksPath`, and `.git/hooks` itself. Also the staged-file runner: `lint-staged` config, `pretty-quick`, a `staged` block in `vite.config.ts`. An existing manager settles Section F without asking.
- **Tests** — the runner, where test files sit today, and any existing coverage config or threshold.
- **CI** — `.github/workflows/*`, or another provider's config. The lint command has to land somewhere that runs it.
- **Agent instructions** — `CLAUDE.md`, `AGENTS.md`. One of them gets the context pointer in step 7.

**Node / TypeScript, if present:**

- **Package manager** — the `packageManager` field first, then lockfiles (`pnpm-lock.yaml`, `yarn.lock`, `bun.lock*`, `package-lock.json`). Use it for every command below.
- **TypeScript vs JavaScript** — `tsconfig.json`, and the `.ts`/`.tsx` vs `.js`/`.jsx` split. A JS-only repo still gets `typescript.md`'s rules minus the type-aware ones.
- **Framework** — from `package.json` dependencies: `next` → Next.js; `expo` → Expo; `react-native` → React Native; `react` + `vite` → React SPA; `@tanstack/react-start`; `react-router` v7 / `@remix-run/*`. `vue`, `svelte`, `solid`, `angular` are out of scope — offer the `typescript.md` baseline alone and don't improvise framework rules.
- **Styling** — `tailwindcss` and its major version, plus the CSS entry point (the file containing `@import "tailwindcss"`). In a monorepo there may be one per package.
- **i18n** — `i18next`, `react-i18next`, `next-intl`, `@lingui/*`, `@formatjs/*`, or a `t(` convention already in the source.
- **Path aliases** — `compilerOptions.paths` in `tsconfig.json`, and the bundler's matching alias config.
- **Existing structure** — does `src/features/` exist? Is the tree feature-sliced or flat? What case are filenames in today?

**Go, if present:**

- **Go version and toolchain** — the `go` and `toolchain` lines in `go.mod`. They set what `run.go` and the modernisation linters can assume.
- **Module layout** — one module or several; is there a `go.work`? Is code under `internal/`, `pkg/`, `cmd/`, or flat at the root?
- **Existing config** — `.golangci.yml` / `.golangci.yaml` / `.golangci.toml`, and its `version` field. A v1 config needs migrating before anything here applies.
- **Generated code** — `.pb.go`, `.connect.go`, `_generated.go`, mocks. These get excluded, and finding them now saves a large false finding count in step 6.
- **Frameworks and infrastructure** — the HTTP/gRPC framework, the logger (`log/slog`, zap, zerolog), OpenTelemetry, the database driver, protobuf. Each turns on a specific linter and turning them on blind wastes runtime.

Then read the stack reference files the Route table selects — `typescript.md` (plus `react.md` if a React framework was detected), `go.md`, or both in a polyglot repo. The other two references are read at their own steps.

**Done when:** you can state every language present and its share, the repo shape, the per-ecosystem framework and tooling, and the existing lint/hook setup — each from something you read, not assumed — and the stack reference files are read.

### 2. Present and confirm

Summarise the detection in a short block: stack, repo shape, what's already configured, what's missing.

Then take the sections below **in order — one section, one answer, then the next**. Lead each with the recommended answer so the user can accept it in a word. Skip any section detection already settled (no Tailwind → no Section D question about it; no i18n library → don't offer the i18n rules).

**Section A — Scope.** Which code gets the rules. Default: **everything**, one config per ecosystem at the repo root, with path-glob overrides for packages that differ. Offer per-package or per-module configs only when they genuinely diverge in stack — a React app and a Node service, or a service and a codegen tool. Single-package repo: one config, no question needed.

Note the language files' warning about per-module configs in Go: golangci-lint reads the nearest config and **replaces** rather than merges, so anything the module still wants must be restated.

**Section B — Linter.** One per ecosystem, and in both cases the default is not really in question — it is the tool the rest of the reference file is written against:

- **TypeScript / JavaScript / React** → **oxlint**. Fast enough to run on every commit, which is what makes hooks tolerable.
- **Go** → **golangci-lint v2**. It aggregates ~120 analysers behind one binary and one config, and the alternative is wiring a dozen tools by hand.

Where something else is already configured, name the branch:

- **ESLint or Biome** → **Replace** (recommended): oxlint covers the rules that matter here and most of the plugins this skill installs are oxlint-native. Migrate with `npx @oxlint/migrate` and read what it reports as unmapped before deleting the old config. **Coexist** only for a genuinely irreplaceable plugin — name it; it costs two lint runs per commit.
- **A v1 `.golangci.yml`** → migrate to v2 with `golangci-lint migrate` before applying anything from `go.md`. The `linters`/`formatters` split and the `exclusions` layout both changed.

**Section C — Formatter.** Every project gets one, and the question is only which. A formatter is what makes formatting stop being a thing anyone — human or agent — has an opinion about, and it removes the largest source of pure noise from a diff.

Keep an existing formatter if one is configured; migrating formatters rewrites the whole repo and buys nothing. Otherwise the default per ecosystem:

- **TypeScript / JavaScript / CSS / JSON / Markdown** → **Prettier**, unless the repo is all-oxlint and wants one toolchain, in which case **oxfmt**. Biome's formatter if Biome is already there. Whichever it is, `--write` for the fix command and `--check` for the CI one.
- **Go** → **`golangci-lint fmt`**, which owns formatting in v2 (gofumpt + goimports + gci, per `go.md`). `golangci-lint fmt --diff` is the CI check.

Two things to settle here rather than later:

- **Tailwind class order**, if Tailwind is present. `prettier-plugin-tailwindcss`, `oxfmt`, and `oxlint-tailwindcss`'s `enforce-sort-order` all produce the same output *provided they read the same CSS entry point*. Point them at it, or they rewrite each other's output on every save.
- **Where it runs.** Three places, and all three want the same tool: the `pre-commit` hook (fix), CI (check), and optionally the agent's own edit loop (Section G). Confirm the fix and check commands now — several later steps reference them.

**Section D — Rule groups.** Present the groups the reference files describe, each marked as recommended-on, and let the user drop any. Give one line per group saying what it stops agents doing. State the severity policy explicitly here, including the language difference: in TypeScript the budget rules land as `"warn"`; in Go there is no warn tier, so the budget group either blocks with calibrated thresholds or moves to a separate advisory command — that is a decision the user makes in this section.

**Section E — Structure conventions.** For React, this is the bulletproof-react layout in `react.md`: feature folders, unidirectional imports, absolute aliases, kebab-case filenames, tests adjacent to the files they cover. For Go it is `go.md`'s `cmd/` + `internal/` layout with snake_case filenames, `depguard` rules for the layering, and `testpackage` for external test packages — with much less to decide, because the compiler already enforces `internal/` and test adjacency.

An **existing** tree is the fork that matters. Say how many files currently violate each convention, then offer:

- **Enforce going forward** (recommended for a populated repo) — rules on, existing violations listed in the report for the user to work through.
- **Enforce and migrate now** — rename and move files to match. Only when the user asks; it is a large, review-heavy diff.
- **Skip this convention** — the rule doesn't go in.

Never migrate a tree without being asked.

**Section F — Git hooks.** Two questions, in this order.

*Which hooks?* Default: **on** — `pre-commit` formatting and linting staged files (plus typecheck where the language needs a separate one), `commit-msg` enforcing Conventional Commits, and `post-merge` reinstalling dependencies when a pull brings a changed lockfile. Each is independently declinable.

*Which manager?* Skip this if step 1 found one already — an existing manager wins, because two of them fighting over `.git/hooks` produces hooks that silently stop running. Otherwise ask, leading with **husky** (the default wherever a `package.json` exists) and offering: plain `core.hooksPath` (no manager, no dependency), lefthook (Go-only, polyglot, monorepos), simple-git-hooks (husky's job in ~1 KB), Vite+ `vp` (if the project already uses it), pre-commit (Python-leaning repos), Overcommit (Ruby). Yorkie, ghooks, and git-hooks-js are unmaintained — add to one only if it is already installed.

The choice matters less than it looks, because `git-hooks.md` puts each hook's logic in a repo script and leaves the manager pointing at it. See `git-hooks.md`.

**Section G — Agent hooks.** Optional, and **off unless asked for** — these write into `.claude/`, `.codex/`, or `.cursor/`, which is a developer's own tooling rather than the repo's build. Offer three, and name which harnesses to configure:

- **Format on file edit** (recommended) — the formatter from Section C, running inside the agent's loop so its output arrives already formatted.
- **Block edits to generated code** (recommended **if** step 1 found a code generator — sqlc, Prisma, buf/protobuf, mockery, GraphQL Codegen, …) — an agent editing generated output does work that vanishes at the next generate.
- **Complexity nudge on file edit** (worth offering) — reports the Section D budget rules against the file just edited, once per function per session. The one lint-shaped check that belongs in the inner loop: a 19-branch function is 19 branches deep whether or not the next edit lands, and the fix is two minutes' work now versus a refactor nobody wants at commit. `agent-hooks.md` ships the script.
- **Lint on file edit** (default **no**) — per-edit lint derails a turn, because mid-refactor code is legitimately broken between edits. If the user wants general lint inside the loop, `agent-hooks.md` puts it on the end-of-turn event instead.

**Section H — Coverage thresholds.** Default: **on but low** — a floor that ratchets, not a target. Reasonable start is 60% lines/functions on a repo with tests, `0` (recording only) on a repo without. A threshold high enough to fail on day one gets deleted by day two.

**Done when:** every applicable section has an explicit answer from the user, and no section was decided on their behalf.

### 3. Install and configure

Work from the reference files and the upstream docs you read, not from memory.

- **Tooling** — resolve current versions rather than recalling them, and **pin every one**. A floating linter version means a green local run and a red CI run with no code change between them.
  - Node: `npm view <pkg> version`, installed as devDependencies. For plugins that must match the linter's version (oxlint's own JS plugin API), read the installed `oxlint` version and pin the companion package to exactly that.
  - Go: the pinned golangci-lint **binary**, per `go.md` — its docs warn that `go install` and `go.mod` tool directives aren't guaranteed to work. Put the version in one variable that CI and the local target both read.
  - Don't change the package manager, the Go toolchain line, or any unrelated version range.
- **Config** — merge into any existing config; keep every existing rule, ignore, and override. Add the `$schema` line (oxlint) or `version: "2"` (golangci-lint) so editors validate the file.
- **Formatter** — install and configure the tool chosen in Section C, and write its ignore file (`.prettierignore`, or the `formatters.exclusions` block) covering the same generated and vendored paths as the linter's. The two lists serve the same fact and must not drift.
- **Ignores** — exclude build output, vendored code, and generated code (`.pb.go`, `.connect.go`, mocks, codegen output), plus agent tooling directories (`.claude/`, `.agents/`, `.cursor/`, `.codex/`, …). Don't blanket-ignore dot-directories; some repos keep real source in them.
- **Commands** — per ecosystem, a `lint`, a `format` (fix), and a `format:check`. Then one umbrella command that runs them all, folded into whatever already runs typecheck (`check`, `ci`, `validate`, a `Makefile`/`Taskfile` target). If there is no umbrella command, create one and say it needs adding to CI. **CI runs the check variant, never the fix variant** — a pipeline that rewrites files produces a green build over unformatted source. In a polyglot repo say plainly which command covers which language; a `lint` script that silently skips half the repo is worse than no script.

**Done when:** tooling is installed at pinned, resolved versions, every ecosystem's lint and format config is written with existing entries preserved, and single commands lint and format the whole repo.

### 4. Dependency-specific rules

The project's dependencies each have documented anti-patterns, and a rule that catches one is worth more than a note asking an agent not to do it.

List the notable dependencies detected in step 1, ask the user to add any you missed or any they plan to adopt, then follow [references/dependency-rules.md](./references/dependency-rules.md): search for an existing plugin first, and only author a custom rule when none exists. Every custom rule is **proposed with its diagnostic message and an example of what it catches**, and installed only if the user takes it.

**Done when:** every notable dependency has been through the search-then-propose loop, and the user has accepted or declined each proposal.

### 5. Git hooks

Unless declined in Section F, follow [references/git-hooks.md](./references/git-hooks.md).

**Done when:** the hooks the user accepted exist as repo scripts, are executable, the chosen manager points at each, a fresh clone gets them, and step 7 has proved each one.

### 6. Agent hooks — optional

Skip entirely unless Section G took something. This step writes into a developer's harness config (`.claude/`, `.codex/`, `.cursor/`), not the repo's build, so a project is fully set up without it.

Follow [references/agent-hooks.md](./references/agent-hooks.md). Configure only the harnesses the user named, and only after checking each one's current docs — these hook systems are young and their events, payload field names, and feature flags have all moved recently.

**Done when:** the hooks the user accepted exist, are executable, and step 7 has proved each one — or the step was skipped and the report says so.

### 7. Prove the rules bite

**This is the completion criterion for the whole skill.** A config that doesn't fail on a violation is worth nothing, and a config that fails on everything gets ripped out. Both are found here, not by the user tomorrow.

1. **Run every lint and format command on the repo as it stands** — each ecosystem's, plus the umbrella. Record the finding count per rule or linter.
2. **Triage the findings.** A rule producing hundreds of hits on existing code is mis-scoped for this repo — either the user opted into migrating (Section E), or it needs a narrowing exclusion, or it comes out. Decide with the user; do not silence it by lowering severity, adding blanket `oxlint-disable` / `//nolint` comments, or weakening options to make the number go down.
3. **Prove a rule fires.** Pick one high-value rule from each group installed, in each language. Introduce the violation it targets in a scratch file, run lint, and confirm it fails with that rule's name. Revert. Confirm lint passes again. Prove the formatter too: mangle a file's formatting, confirm the check command fails, run the fix command, confirm it passes.
4. **Prove each git hook fires.** For `commit-msg`, attempt a commit with a non-conventional message and watch it be rejected, then a conventional one and watch it pass. For `pre-commit`, stage a badly-formatted file with a lint error and watch the format land and the commit be blocked. Then clone the repo to a temp directory, install, and confirm the hooks are live there too — a hook set that works only on the machine that created it is the most common failure of the whole step. For `post-merge`, merge a branch whose only change is the lockfile and watch the install run — then merge one that doesn't touch it and watch the hook stay quiet, which is the half that proves the guard works rather than the hook running on every merge.
5. **Prove each agent hook fires**, if step 6 ran. Write a badly-formatted file and read it back already formatted; write a syntactically broken one and confirm the edit still succeeds. Attempt an edit to a generated file and confirm the block fires with a message naming the source file and the regenerate command. Edit an over-budget function twice and confirm the complexity nudge arrives once, not twice. `agent-hooks.md` carries the full list.

If a rule or hook doesn't fire, it is not wired correctly — fix it before finishing. A silently-inert plugin is the failure this step exists to catch, and an agent hook is the easiest of all to leave inert (a missing `chmod +x`, a payload field named differently by that harness).

**Done when:** you have observed, for every installed group and every installed hook, a pass → a fail on a real violation → a pass again.

### 8. Document and report

**Write the conventions doc.** One file the agents in this repo will actually read — `docs/agents/project-conventions.md`, or alongside an existing agent-docs convention. Cover only what config cannot express: the file structure and why imports flow one way, where a new feature or package goes, where a test goes, the aliases or module boundaries, and the commit format. Keep it to the copy-me tree plus a paragraph per convention. The rule list belongs in the lint config, not here — a doc that restates config goes stale.

Where the config carries a **maintenance obligation**, say so here, because nothing else will: a new React feature needs its cross-feature `overrides` entry, a new workspace package needs its commitlint scope, a new Go module needs adding to the `depguard` rules. An unlisted one is silently unenforced.

**Add the context pointer.** One line in `CLAUDE.md` if it exists, else `AGENTS.md` (create `AGENTS.md` only if neither exists — never create the other one alongside an existing file). This line is what makes an agent find the conventions instead of tripping over them:

```markdown
Structure, imports, and commit conventions: [docs/agents/project-conventions.md](./docs/agents/project-conventions.md). Run `<lint command>` and `<format command>` before committing.
```

**Report.** Tell the user, plainly:

- Which linters, formatters, plugins, and rule groups were installed per language, and which were declined.
- Every rule that does **not** block, and why — the `"warn"` tier in TypeScript, and anything moved to Go's advisory pass.
- Any language present in the repo that this skill has no reference file for, and is therefore not covered at all.
- Existing violations found in step 7 and not fixed — count per rule — as the work left over.
- Which git hooks are live, and what each blocks.
- Which **agent** hooks were installed, for which harnesses, and whether the config is project-level or user-level. Say plainly that a teammate on a different harness has nothing installed — agent hooks don't travel the way a git hook does.
- What was left out and why.

**Done when:** the conventions doc exists, the agent-instructions file points at it, and the report names the leftover violations rather than burying them.
