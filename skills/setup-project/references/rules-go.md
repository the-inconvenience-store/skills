# Go rule catalogue

This is the authored baseline for agent-maintained Go. Present applicable groups in the proposal, preserve coherent existing policy, and calibrate thresholds against current code. Rule names assume current golangci-lint identifiers; verify availability and configuration against the pinned version.

Most enabled linters fail the run. If the current tool cannot express advisory severity, put accepted budgets in a separate non-blocking command or agree on calibrated blocking thresholds with the user.

## Complexity and size

Use complementary measurements without duplicates:

- `cyclop`: maximum cyclomatic complexity `12`; start `package-average` disabled and calibrate it from the repository.
- `gocognit`: minimum reported cognitive complexity `20`.
- `funlen`: `80` lines and `40` statements, ignoring comments.
- `nestif`: minimum complexity `4`.
- `maintidx`: report below `20` only when it catches cases the other measures miss.
- `revive/file-length-limit`: `500` lines excluding blank lines and comments; `max-control-nesting`: `4`; `argument-limit`: `5`.

Prefer `cyclop + gocognit`; omit `gocyclo` because it duplicates cyclomatic findings. Disable revive's `cognitive-complexity`, `cyclomatic`, and `function-length` when the dedicated linters own them.

## Correctness

Keep the standard floor—`errcheck`, `govet`, `ineffassign`, `staticcheck`, `unused`—then recommend:

- Resources and data access: `bodyclose`, `sqlclosecheck`, `rowserrcheck`.
- Contexts: `contextcheck`, `noctx`, `containedctx`, `fatcontext`.
- Errors: `errorlint` with `errorf`, `asserts`, and `comparison`; `errname`, `nilerr`, `nilnesserr`, `nilnil`, `errchkjson`.
- Language traps: `durationcheck`, `copyloopvar`, `intrange`, `makezero`, `reassign`, `recvcheck`, `exhaustive`, `forcetypeassert`, `asasalint`, `gocheckcompilerdirectives`.
- Protobuf only: `protogetter`.

`errorlint` and `nilerr` are priorities: wrapped-error comparisons and checked-then-discarded errors fail silently.

## Escape hatches and unfinished work

- `nolintlint`: require a specific linter and an explanation; reject unused suppressions.
- `godox`: flag `TODO`, `FIXME`, `BUG`, `HACK`, `XXX`, `WIP`, `OPTIMIZE`. Explain that accepted markers move to the issue tracker; offer an advisory pass if the team keeps them.
- `forbidigo`: propose bans for `fmt.Print*`, built-in `print/println`, and `panic` only after matching the repository's logger and panic policy. `panic` is opinionated; a narrower alternative is revive's `deep-exit` for `os.Exit` and `log.Fatal` outside `main`.

## Magic values

- `mnd`: check arguments, cases, conditions, operations, returns, and assignments. Start with domain-neutral exceptions such as `2`, `10`, `64`, `100`, `0644`, `0755`, then tune against real findings. Its built-in `0` and `1` exceptions need no duplication.
- `goconst`: repeated strings of length at least `3`, occurring at least `3` times; match existing constants. Keep numeric detection owned by `mnd`.

## Imports and architecture

- `depguard`: derive allowed and denied imports from actual package boundaries. Every denial message should name the owner, replacement, or ADR.
- `importas`: pin aliases when generated clients or versioned APIs otherwise drift.
- `gomodguard_v2`: banned modules, version constraints, and recommended replacements.

Prefer Go's compiler-enforced `internal/` boundary where it fits. A copied depguard example is not architecture.

## Naming and file placement

Recommended revive rules when the project accepts the conventions:

`filename-format` for snake_case, `package-directory-mismatch`, `var-naming`, `error-naming`, `error-strings`, `receiver-naming`, `confusing-naming`, `import-alias-naming`, `package-comments`.

Offer `testpackage` when tests should exercise only the exported package surface. Go already enforces test-file adjacency through `_test.go`; no extra placement rule is needed.

## Readability

Recommended linters:

`dupl` with threshold `150`, `dupword`, `misspell`, `whitespace`, `modernize`, `perfsprint`, `prealloc`, `wastedassign`, `unconvert`, `unparam`, `usestdlibvars`, `mirror`, `exptostd`, `predeclared`, `goprintffuncname`, `godot`, `nakedret`, `dogsled`, `iface`, `interfacebloat`.

Recommended revive rules:

`early-return`, `indent-error-flow`, `superfluous-else`, `unnecessary-if`, `unnecessary-stmt`, `flag-parameter`, `deep-exit`, `unhandled-error`, `unchecked-type-assertion`, `use-any`, `use-errors-new`, `identical-branches`, `unused-parameter`, `unused-receiver`, `bool-literal-in-expr`, `constant-logical-expr`, `range-val-in-closure`, `modifies-parameter`, `unexported-return`.

`early-return + indent-error-flow + superfluous-else` protect Go's left-margin happy path. `flag-parameter` catches functions doing two jobs.

Offer separately because they encode stronger team positions: `ireturn`, `gochecknoglobals`, `wrapcheck`, `err113`. Introduce `gocritic` by selected diagnostic/style tags and review its findings rather than enabling every check blindly.

## Security

- `gosec`: start at medium severity and medium confidence; adjust only after reviewing the findings.
- `bidichk`, `asciicheck`.

## Tests

- `testpackage`, `thelper`, `tparallel`, `paralleltest`, `usetesting`, `testableexamples`.
- `testifylint` only when testify is used.

Coverage is separate from lint. Offer a ratcheted coverage gate and `go test -race` as explicit test/CI choices, not implied linter setup.

## Observability and infrastructure

Enable only when detected:

- `sloglint` for `log/slog`; prefer static messages, scoped context requirements, and the project's key naming convention.
- `loggercheck` for zap/zerolog/logr/klog/kitlog; `zerologlint` for zerolog specifics.
- `spancheck` for OpenTelemetry with end, record-error, and set-status checks.
- `musttag` for marshaled types, `canonicalheader` for HTTP headers, `unqueryvet` for `SELECT *`.

## Formatter companion

When the approved tool supports them, propose `gofumpt`, `goimports`, and `gci` with the module path taken from `go.mod`. Do not run `gofmt` alongside its strict superset `gofumpt`. Configure `goimports` and `gci` with the same local module prefix so they converge.

Offer `golines` separately because it rewrites line structure; `120` is the starting budget. Enable `swaggo` formatting only when swag annotations are present. Exclude generated files from both formatting and linting.
