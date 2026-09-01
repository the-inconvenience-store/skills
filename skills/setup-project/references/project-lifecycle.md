# Project lifecycle

Read this reference when setup includes reproducible installation, a test baseline, generated code, dependency upkeep, or fresh-checkout verification. Select only the parts that fit the repository and put them in the proposal before implementation.

## Reproducible setup

- Reuse the repository's runtime and tool-version mechanism. If none exists, propose the ecosystem-standard mechanism and pin only versions required to reproduce the project.
- Commit the appropriate dependency lockfiles and make CI use the ecosystem's locked or frozen installation mode.
- When a task runner is accepted and fresh setup has more than an ordinary dependency install, offer a `bootstrap` task. Keep it safe to run repeatedly and limited to the preparation actions approved in the proposal.
- Without a task runner, use and document the native setup sequence. Do not add a `bootstrap` task or a wrapper whose only purpose is to imitate one.

## Complete check

Define the complete accepted gate: format-check, lint, typecheck or compilation, tests, and code-generation drift where applicable.

- With an accepted task runner, expose that gate as `check` and use it from CI and verification.
- Without a task runner, use the existing native aggregate command or the explicit native command sequence. Do not add a `check` task solely for naming consistency.
- Keep network-dependent or unusually slow checks outside the fast local path unless the user accepts the cost.

## Test baseline

If no test runner exists, recommend the maintained ecosystem standard and explain its fit. Treat adding it as an explicit proposal choice.

Exercise it against a small piece of real behavior or the scaffold's minimal entry point. If the project has no behavior to test yet, verify that test discovery runs and report the missing behavioral test; do not create an assertion that only tests configuration or the test framework itself. Coverage thresholds remain a separate user choice.

## Generated code

Detect generators from schemas, manifests, generated headers, and existing commands. Identify the source inputs, committed outputs, and tool versions.

- When a task runner is accepted, name the generation task exactly `codegen`.
- Without a task runner, retain the generator's native command and do not add a task alias.
- Align formatter and linter exclusions with generated outputs while keeping their handwritten neighbors checked.
- When generated output is committed, add an accepted CI drift check that runs generation in the disposable CI checkout and fails on a diff.
- Point contributors and agents to the source input and the `codegen` task or native command instead of inviting edits to generated output.

## Dependency upkeep

- Preserve or establish the lockfile policy and a supported vulnerability-audit command.
- Ask before adding Renovate, Dependabot, or another update service because it changes the repository workflow. If accepted, group routine updates at a cadence that fits the project and run the complete check on update changes.
- With an accepted task runner, expose a dependency audit task only when it improves the project interface. Without one, use the ecosystem's native audit command.
- Follow current official ecosystem and service documentation. Report audits that require network access, credentials, or unavailable registries as unverified.

## Fresh-checkout proof

Prefer CI because it already starts from a clean checkout. The proof installs the pinned toolchain and locked dependencies, runs `bootstrap` when that task exists, then runs the complete gate through `check` or the native commands.

Do not create a local clone or worktree solely for this proof without approval. If no safe disposable environment exists, report the fresh-checkout path as unverified and list the commands that should prove it.

## Minimal handoff

Update the repository's existing README, contributor guide, or agent instructions with only the commands needed to prepare, check, format, test, audit dependencies, and run code generation. Name task-runner tasks only when the runner was accepted. Keep tool explanations and rule catalogs in their configuration or this skill's disclosed references.
