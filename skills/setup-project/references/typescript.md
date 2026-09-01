# JavaScript and TypeScript

Use this reference to shape the proposal, not as a fixed rule list. Installed configuration, repository conventions, and current official documentation are the sources of truth.

## Inspect

- Read `package.json`, the lockfile, workspace configuration, compiler configuration, and existing lint/format scripts.
- Count the JavaScript and TypeScript actually in use. A leftover config file is not evidence that a tool is active.
- Identify runtime and framework constraints, generated paths, path aliases, test tooling, and whether typechecking already runs in CI.
- Run existing checks before proposing a migration; record their behavior and current failures.

Read [react.md](./react.md) as well when React or a React framework is present.

## Propose

Before proposing lint changes, read [rules-typescript.md](./rules-typescript.md) and present the relevant groups with their consequences. The catalogue is the recommended baseline, not automatic consent.

Keep a working linter and formatter unless replacement solves a named problem. When choosing for a new repo, compare current support for the rules and plugins the project needs, speed on this repository, editor integration, and migration cost. ESLint, oxlint, and Biome have different coverage; tool count alone does not settle the choice.

Propose rule groups rather than hundreds of individual rules:

- correctness and suspicious constructs;
- TypeScript safety, including async/promise handling when type information is available;
- imports and dependency boundaries already present in the architecture;
- test mistakes supported by the detected runner;
- maintainability budgets, only with thresholds calibrated to the project.

Style belongs to the formatter where possible. Preserve the existing formatter in an established repo; changing one can rewrite most files without improving enforcement.

Treat compiler strictness, file naming, import aliases, test placement, and directory structure as separate choices. Infer them from an existing repo or include them in the proposal for a new repo. Do not smuggle an architectural migration into linter setup.

For a linter migration, account for every existing plugin, rule override, ignore, and CI invocation. Report unmapped behavior before removing the old tool. Coexistence is reasonable when a required rule has no replacement, provided the extra runtime is visible in the proposal.

## Commands and hooks

Give the repo explicit commands for lint, format-fix, format-check, and typecheck when TypeScript is present. Use the detected package manager. Keep the full typecheck out of pre-commit when it exceeds the agreed hook budget; run it at pre-push or in CI instead.

When hooks operate on staged files, verify partially staged files are preserved and formatter changes are re-staged intentionally. See [git-hooks.md](./git-hooks.md) after the user approves hooks.

## Verify

- Run the new commands from the repository root and from any workspace location developers are expected to use.
- Demonstrate one representative lint failure in a disposable file, then remove it and confirm a pass.
- If a tool was replaced, compare the old and new checks against the repository before removing the old configuration.
- Name pre-existing violations rather than weakening rules or adding blanket disables to obtain a green run.

Consult the current official documentation for the chosen tools before installing or configuring them. Option names, plugin compatibility, and migration coverage change.
