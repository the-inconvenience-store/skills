# Security scanning

Read this reference when the user accepts Semgrep or Gitleaks. Both are optional, independent, and complement the dependency audit in `project-lifecycle.md`. Each one's main job is a **pre-commit** hook that catches vulnerabilities and secrets as soon as an agent or a person commits them. CI runs the same checks as the backstop, because `--no-verify` skips local hooks.

Follow current official documentation for each tool's install, hook, and CI configuration. Wire hooks through the hook manager selected in `git-hooks.md`.

## Semgrep

Semgrep finds code-level vulnerabilities and bug patterns with rules that work across languages. It also covers files the stack linters skip, such as CI workflows, Dockerfiles, and infrastructure-as-code. Layer it with `gosec`, the ESLint security rules, and the other stack analyzers. Drop a registry pack only when it duplicates rules that are already enabled.

### Edition

Use Semgrep Community Edition (`semgrep scan`). Use the Semgrep AppSec Platform (`semgrep ci`, `semgrep login`, `SEMGREP_APP_TOKEN`) only when the organization already uses it, because it adds an account and a credential.

### Rules live in the repository

A pre-commit hook needs its rules locally, so commit them under `.semgrep/`:

- `.semgrep/rules/`: project rules, including the agent-failure rules below.
- `.semgrep/vendor/`: registry packs selected for the detected stack (for example `p/typescript`, `p/react`, `p/golang`, `p/secrets`, `p/github-actions`), copied from a pinned `semgrep-rules` commit.

Add a sync script, or a task when a task runner was accepted, that refreshes the vendored packs to a new pinned commit. Treat it as dependency upkeep: run it on the same cadence and gate it on the complete check.

Pick named packs over `--config auto`. `auto` sends project metadata to Semgrep and chooses rules the reviewer cannot see.

**Licensing decides what gets vendored.** Registry rules use the Semgrep Rules License, which allows use "only for your own internal business purposes" and forbids distributing the rules. Check repository visibility (for example `gh repo view --json visibility`):

- **Private repository:** vendor the selected packs.
- **Public repository:** commit only project rules and rules under a license that allows redistribution. CI fetches the registry packs at run time with `--config p/<pack>`, so they are never redistributed. Say in the proposal that the hook then covers less than CI does.

### Agent-failure rules

Offer a starter set of project rules aimed at mistakes agents commonly make, written for the detected languages and frameworks:

- SQL or shell commands built by string concatenation or interpolation;
- TLS or certificate verification disabled;
- `eval`, dynamic `exec`, or unsafe deserialization of untrusted input;
- hardcoded credentials or tokens;
- wildcard CORS combined with credentials;
- caught errors that are swallowed or replaced with a default.

Each rule's `message` names the safe alternative, so the agent that triggered it can fix the code and commit again. Give every rule a positive and a negative test case using Semgrep's rule-test annotations, and run `semgrep --test` in CI.

### Hook

- Scan staged files only, which is what the official `semgrep/pre-commit` hook does.
- Point `--config` at `.semgrep/`, and pass `--error --skip-unknown-extensions --metrics off`.
- Measure the hook on a realistic staged change. If it exceeds the hook budget, move the slowest vendored packs to CI only, and keep Semgrep itself in pre-commit.

### CI

Run Semgrep with the same version and the same `.semgrep/` config over the whole repository. Public repositories also add their run-time registry packs here. On pull requests, `--baseline-commit` limits failures to new findings when existing findings were deferred. Uploading SARIF to GitHub code scanning is a separate choice: private repositories need GitHub Advanced Security for it.

### Existing findings

Run one full scan before turning on the gate, and triage the results with the user. Fix each finding, defer it through the CI baseline, or suppress it with `# nosemgrep: <rule-id>` and a stated reason. Keep `.semgrepignore` aligned with the lint ignores for generated, vendored, and build output.

## Gitleaks

Gitleaks detects hardcoded secrets in staged changes and in git history. It is MIT-licensed, ships as a single binary, and needs no network access, so it fits the pre-commit budget easily.

- **Hook:** the official `gitleaks` pre-commit hook runs `gitleaks git --pre-commit --redact --staged --verbose`. Use that command through whichever hook manager the repository uses.
- **Config:** add `.gitleaks.toml` only to tune the defaults. Start it with `[extend] useDefault = true`, and disable or add rules there.
- **CI:** run the pinned binary with `gitleaks git --redact` over the pushed range or the full history. `gitleaks-action` needs a license key (free) for repositories owned by an organization account. If the user hasn't approved obtaining that key, run the binary directly.
- **Existing findings:** scan the full history once. A secret found in history has already leaked, so report it for rotation; ignoring it does not make it safe. After triage, record accepted findings in a `--baseline-path` report or as fingerprints in `.gitleaksignore`. Mark known false positives inline with `gitleaks:allow`.

`p/secrets` in Semgrep overlaps with Gitleaks. When both are accepted, keep Gitleaks as the secret gate, since it is faster and also scans history, and leave out `p/secrets`.

## Agent hook

When the user also asks for agent hooks (`agent-hooks.md`), offer to run Semgrep with the project's `.semgrep/rules/` on the file named in the edit event. That puts findings in front of the agent before it commits. Make it fail open while the code is incomplete, and keep the git hook as the enforcing check.

## Verify

- Stage a disposable file containing a pattern from a project rule, and confirm the Semgrep hook blocks it with the rule's message. Do the same with a fake secret in a known format for the Gitleaks hook. Remove the file and confirm both hooks pass.
- Confirm that a staged change with no relevant files passes both hooks quickly.
- Record the measured hook runtime in the report.
- Run `semgrep --test` against the project rules.
- When CI was changed, report the CI scan as unverified until it has run.
