# Go

Use this reference for Go-specific decisions while preserving the repository's existing module and toolchain choices.

## Inspect

- Read every relevant `go.mod`, `go.work`, existing lint configuration, task runner, and CI command.
- Record the Go and toolchain versions, module boundaries, generated files, build tags, and use of `internal/`.
- Identify existing formatters and standalone analyzers before proposing an aggregator.
- Run the current checks and distinguish configuration failures from source findings.

## Propose

Before proposing lint changes, read [rules-go.md](./rules-go.md) and calibrate its thresholds against the repository.

For a new setup, an aggregator such as golangci-lint can provide one versioned command and configuration for many analyzers. Keep direct tools when the repo already manages them successfully or when the aggregator does not support a required analyzer. Resolve the current supported installation method and configuration schema from official documentation.

Propose linter groups rather than a catalogue:

- compiler/vet and correctness checks;
- error handling and resource cleanup;
- concurrency checks when the code uses concurrency;
- security checks appropriate to the program;
- import or dependency boundaries derived from the actual module design;
- test mistakes;
- maintainability budgets calibrated against current code.

Go formatters can change imports as well as layout. Keep edit-time formatting layout-only when the code may be incomplete; reserve import cleanup for an accepted commit-time or explicit format command.

Treat `cmd/`, `internal/`, `pkg/`, filename conventions, external test packages, coverage thresholds, and logging policy as separate project choices. Existing structure wins unless the user approves a migration.

In a multi-module repository, state which command covers which modules. Confirm whether the chosen linter discovers configuration by module, working directory, or nearest config; do not assume configs merge.

## Commands and hooks

Provide clear lint and format-check commands for the whole supported repository. Go analysis commonly operates on packages rather than arbitrary file lists, so a staged-file hook may need to map changed files to packages. Measure it and move slow analysis to pre-push or CI.

## Verify

- Run checks with the repository's pinned toolchain and from the directory CI uses.
- Demonstrate one representative Go finding in disposable code, then restore a passing state.
- Confirm generated and vendored code is excluded without excluding handwritten packages beside it.
- Preserve existing findings in the report rather than adding broad `nolint` directives.

Use current official Go and selected-tool documentation for installation, configuration, and formatter behavior.
