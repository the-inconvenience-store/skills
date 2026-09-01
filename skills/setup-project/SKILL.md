---
name: setup-project
description: Guided setup for a project's development guardrails and reproducible checks.
disable-model-invocation: true
---

# Setup Project

Set up a project's **guardrails** with the user: inspect what is already there, propose the smallest coherent setup, wait for approval, then install and verify it.

The proposal is the control point. The agent owns discovery and recommendations; the user owns the outcome. Preserve working conventions and tooling unless the proposal names a concrete reason to change them.

## Route

Read only the references selected by the repository and the live decision branch:

| Read | When |
| --- | --- |
| [references/typescript.md](./references/typescript.md) | The repo contains JavaScript or TypeScript. |
| [references/react.md](./references/react.md) | The repo contains React or a React framework; read with `typescript.md`. |
| [references/go.md](./references/go.md) | The repo contains Go. |
| [references/research-ecosystem.md](./references/research-ecosystem.md) | A detected language or framework has no bundled setup reference. |
| [references/rules-typescript.md](./references/rules-typescript.md) | The proposal adds or changes JavaScript or TypeScript lint rules. |
| [references/rules-react.md](./references/rules-react.md) | The proposal adds or changes React lint rules. |
| [references/bulletproof-react.md](./references/bulletproof-react.md) | A new React application or architecture overhaul may adopt Bulletproof React standards. |
| [references/rules-go.md](./references/rules-go.md) | The proposal adds or changes Go lint rules. |
| [references/dependency-rules.md](./references/dependency-rules.md) | Notable libraries need their own lint coverage. |
| [references/project-lifecycle.md](./references/project-lifecycle.md) | The setup covers reproducible installation, tests, generated code, dependency upkeep, or fresh-checkout verification. |
| [references/git-hooks.md](./references/git-hooks.md) | The proposal includes git hooks. |
| [references/agent-hooks.md](./references/agent-hooks.md) | The user asks for hooks inside an agent harness. |

For another ecosystem, follow `research-ecosystem.md` and build an equivalent evidence-backed setup. A missing bundled reference requires research; it is not permission to skip that language.

## Process

### 1. Inspect

Read the repository before asking questions or changing files:

- Check `git status` and preserve unrelated work.
- Identify languages, runtimes, package managers, frameworks, packages or modules, and whether the repo is new or established.
- Read existing tool-version files, lockfiles, setup commands, lint, format, compiler, test, code-generation, dependency-update, CI, and hook configuration. Check `core.hooksPath` as well as tracked hook-manager files.
- Read the project's agent instructions and contributor documentation for stated conventions.
- Run existing check commands when doing so is safe; record failures that predate this setup.
- Read the matching stack references above.

**Done when:** the current tools, commands, constraints, and gaps are supported by repository evidence.

### 2. Establish intent

Use the user's request and the repository as defaults. Ask only about choices that would materially change the result and cannot be inferred, such as:

- replacing an established tool;
- applying new rules to an existing codebase with many violations;
- adding commit-message policy, slow checks, CI changes, or agent-specific hooks;
- adopting project structure or naming conventions in a new repo.

If the workspace has not been scaffolded, ask what the project must do and which stack constraints already exist. Include the official scaffold or minimal initialization in the proposal instead of silently choosing a framework.

**Task runner — optional:** reuse an existing runner, or ask whether the user wants one and recommend only the runner that fits the repo—such as Nx, Turborepo, Taskfile, Makefile, or `mise`. If accepted, make its tasks the canonical command interface and use them for the rest of setup, hooks, CI, and verification. Add named tasks only when a task runner is accepted; otherwise use the ecosystem's native commands without creating task-shaped wrappers.

Bundle related choices into one short conversation. Offer a recommendation and its consequence; omit menus of irrelevant tools. If the user already expressed a preference, carry it into the proposal instead of asking again.

**Done when:** the desired scope and any hard constraints are known well enough to propose one setup.

### 3. Propose

Present one cohesive plan before installing or editing anything. Keep it short enough to approve as a whole and include:

- what stays, what changes, and why;
- the linter and formatter per ecosystem;
- the task runner and canonical task names, when accepted—including `bootstrap`, `check`, and `codegen` only where those jobs apply;
- the reproducible setup, test baseline, generated-code lifecycle, and dependency upkeep selected from `project-lifecycle.md`;
- the commands developers and CI will run;
- which accepted checks run at pre-commit, pre-push, commit-message, or CI time;
- how existing violations will be handled without hiding them;
- the files and dependencies expected to change.

Lead with the recommended setup. Include an alternative only where it changes a meaningful tradeoff. Treat new architecture, file-layout, naming, coverage, custom-rule, and agent-hook work as optional scope rather than implied setup.

Wait for the user's explicit approval or amendments.

**Done when:** the user has approved a concrete plan.

### 4. Implement

Implement only the approved plan:

- Use the detected package manager and current official installation/configuration documentation.
- Keep existing tools and configuration unless replacement was approved. During a migration, account for behavior the replacement cannot reproduce before removing the old tool.
- Pin tool versions according to the repository's existing dependency policy; do not introduce a new versioning policy incidentally.
- When a task runner was accepted, configure it first, then use its tasks for the remaining implementation and checks.
- Implement the approved lifecycle setup from `project-lifecycle.md`. When a task runner was accepted, name the generated-code task exactly `codegen`.
- Give each ecosystem clear `lint`, format-fix, and format-check commands, then connect them to an existing aggregate check when one exists.
- Keep lint and formatter ignores aligned for generated, vendored, and build output.
- Reuse the existing hook manager. Put only accepted, fast checks in local hooks; CI remains the complete gate.
- Add or update CI only when approved or necessary to make an approved check effective.

Store discoverable facts in configuration and scripts. Put only the commands needed to prepare, check, and maintain the project in its existing contributor or agent entrypoint; keep rule inventories out of prose.

**Done when:** every approved guardrail is installed and reachable through a named command or hook.

### 5. Verify

Verify in proportion to the change:

1. Run every new or changed lint, format-check, test, code-generation, dependency-audit, and aggregate command that the user accepted. Use the approved task runner when one was selected.
2. Use a disposable file or temporary edit to demonstrate one representative violation per configured ecosystem, then restore it and confirm the check passes. Preserve any pre-existing failures in the report.
3. Invoke hook scripts with controlled input or use the manager's test mechanism. Confirm both the relevant-file path and the no-op path.
4. Measure local hook duration. Move slow checks to pre-push or CI with the user's approval.
5. Verify the approved fresh-checkout path in CI or another disposable checkout: locked installation, `bootstrap` when that task exists, then the complete check. Obtain approval before creating a local clone or worktree solely for this test.

Do not create commits, merge branches, rewrite user files, clone the repository, or trigger dependency installation merely to test hooks unless the user explicitly approves that side effect. If a behavior cannot be exercised safely, report it as unverified.

**Done when:** the commands pass, representative failures are observed, installed hooks are exercised safely, and every verification gap is named.

### 6. Report

Tell the user:

- what changed and what was deliberately kept;
- the commands to run;
- which checks run locally and in CI;
- existing violations, researched ecosystems, dependency-update behavior, and any test, code-generation, or coverage gaps left over;
- anything approved but not verified, with the reason.

The setup is complete when the approved guardrails work and the user can see their boundaries. It is not complete merely because configuration files exist.
