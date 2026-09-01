# Go

The rules and conventions for a Go project. Self-contained — Go has its own toolchain, its own linter, and its own answers to most of what [typescript.md](./typescript.md) solves with plugins, so nothing there carries over.

Default linter: **golangci-lint v2**. It aggregates ~120 analysers behind one binary and one config file, which is why it is the only realistic choice — the alternative is wiring a dozen tools by hand.

## Docs to read before configuring

| Read | For |
| --- | --- |
| <https://golangci-lint.run/docs/linters/> | The linter catalogue. Read it — the list below is a starting set, not the whole field |
| <https://golangci-lint.run/docs/linters/configuration/> | Every linter's settings, with defaults and commented examples |
| <https://golangci-lint.run/docs/configuration/file/> | The v2 config file: `run`, `linters`, `formatters`, `severity`, `output` |
| <https://golangci-lint.run/docs/welcome/install/local/> | Install methods and the current version |
| <https://github.com/mgechev/revive/blob/master/RULES_DESCRIPTIONS.md> | revive's ~100 rules — it carries several checks nothing else has |

Read the settings page for anything you set options on. `cyclop`, `gocognit`, `funlen`, `mnd`, `godox`, `depguard`, and `revive` all have options that matter.

## Severity: Go has no warn tier

This is the one place the skill's severity policy does not translate, and it needs saying to the user up front.

golangci-lint's `severity` block only annotates output — the docs are explicit that it "only affects output formats that support setting severity information." **Every enabled linter fails the run.** There is no per-linter equivalent of oxlint's `"warn"`.

So the budget checks — complexity and file size, the two things the policy wants as nudges rather than defects — need one of two treatments. Ask the user which:

- **Calibrated and blocking** (recommended, and the default): the budget linters go in `linters.enable` with thresholds set generously enough that they fire only on genuine outliers. One config, one command, and the budget has teeth.
- **Advisory second pass**: keep the budget linters' `settings` in the config but leave them **out** of `linters.enable`, then run them separately with the exit code forced to zero. Settings are read whether or not a linter is enabled, so this needs no second config file — just a second command:

  ```bash
  golangci-lint run                                                              # blocking
  golangci-lint run --enable-only=cyclop,gocognit,funlen,dupl --issues-exit-code=0  # advisory
  ```

Everything outside the budget group is blocking either way.

## Install

Install the **pinned binary**. golangci-lint's own docs warn that `go install`, the tools pattern, and `go.mod` `tool` directives "aren't guaranteed to work" — the linter compiles against a specific Go toolchain and dependency set, and building it from source in your module's context is what produces the mysterious version-skew failures.

```bash
curl -sSfL https://golangci-lint.run/install.sh | sh -s -- -b $(go env GOPATH)/bin v2.13.2
```

Resolve the current version rather than using the one written here. Pin the same version in CI and in a `Makefile`/`Taskfile` variable so a developer's machine and the pipeline never disagree about what "lint passes" means — a floating version means a green local run and a red CI run with no code change between them.

## Config skeleton

`.golangci.yml` at the repo root (or the workspace root — see **Monorepo** below).

```yaml
version: "2"

run:
  timeout: 10m
  relative-path-mode: gomod
  tests: true
  modules-download-mode: readonly
  allow-parallel-runners: true

linters:
  default: standard      # errcheck, govet, ineffassign, staticcheck, unused
  enable:
    # the groups below
  settings:
    # per-linter options
  exclusions:
    paths:
      - vendor
      - third_party
      # generated code — parsed for type info, findings suppressed
      - ".*\\.pb\\.go$"
      - ".*\\.connect\\.go$"
      - ".*_generated\\.go$"
      - "mocks?/.*\\.go$"

formatters:
  enable:
    - gofumpt
    - goimports
    - gci
```

`linters.default: standard` keeps the five default analysers and adds to them. `default: all` is the opposite trap — it enables everything including the mutually contradictory style linters (`wsl_v5` and `nlreturn` will argue with your formatter), and produces a finding count nobody triages.

**`run.timeout`** deserves a number, not a default. CI runners are slower and more contended than a laptop, and a module that lints in seconds standalone can blow past five minutes when several golangci-lint processes share two vCPUs. Ten minutes costs nothing when nothing is wrong and prevents a class of flaky-CI investigation that goes nowhere.

**Exclude generated code by path.** Protobuf, connect, mock, and `stringer` output will fail half the rules here and none of it is worth fixing. The files are still parsed for type information, so excluding them doesn't weaken the analysis of the code that imports them.

## Linter groups

### Complexity — cyclop and gocognit, not gocyclo

Three linters claim to measure complexity, and picking the wrong combination gets you duplicate diagnostics for a single fault.

- **`gocyclo`** computes cyclomatic complexity per function — the number of independent paths. Options: `min-complexity`.
- **`cyclop`** computes the **same metric**, and adds `package-average`. It is a strict superset.
- **`gocognit`** computes **cognitive** complexity, which is a genuinely different measurement: it penalises nesting and breaks in linear flow, and does not penalise structures that are trivially readable.

**Run `cyclop` + `gocognit`. Drop `gocyclo`.**

`gocyclo` and `cyclop` measure the same thing, so enabling both reports one problem twice — the reason to keep `cyclop` is `package-average`, which catches the package where no single function is over budget but every function sits just under it.

`gocognit` earns its place because the two metrics genuinely disagree, and each is right where the other is wrong:

- A flat 15-case `switch` scores 15 cyclomatic (fails) and about 1 cognitive (passes). The cognitive score is correct — a flat dispatch table is one of the most readable structures in Go, and failing it teaches people to hide the switch in a map, which is worse.
- Three nested loops with a labelled `break` score 4 cyclomatic (passes) and 9+ cognitive (fails). Here the cognitive score is correct — that is exactly the code nobody can hold in their head.

Cyclomatic answers "how many paths must a test cover"; cognitive answers "can a person read this". Agents produce failures of both kinds, so both belong.

```yaml
linters:
  enable:
    - cyclop
    - gocognit
    - funlen
    - nestif
  settings:
    cyclop:
      max-complexity: 12       # matches the TypeScript baseline
      package-average: 0.0     # start disabled; see below
    gocognit:
      min-complexity: 20       # docs suggest 10–20; cognitive scores run higher than cyclomatic
    funlen:
      lines: 80
      statements: 40
      ignore-comments: true
    nestif:
      min-complexity: 4
```

`cyclop.package-average` needs calibrating against the repo before it means anything. Measure first — run with it disabled, look at the distribution, then set it slightly below the current worst package so it ratchets. A number picked out of the air either fires on everything or never fires.

#### maintidx — the composite metric

Path count and line count are both single-axis. `maintidx` computes the **Maintainability Index**, a composite of Halstead volume, cyclomatic complexity, and lines of code — so it catches the function that passes every individual budget while still being a slog to read, and it is the closest thing golangci-lint has to a volume-weighted metric.

```yaml
linters:
  enable:
    - maintidx
  settings:
    maintidx:
      under: 20      # report functions scoring below this; 0–100, higher is better
```

The scale is inverted from everything else here — a **high** index means good maintainability. The default `20` is the "genuinely unmaintainable" floor and is the right starting point; raising it toward 100 makes the rule fire on almost everything.

It belongs in the budget group, not the blocking one, on the same reasoning as `cyclop` — and it overlaps them by construction, so watch the finding counts at the prove step. If `maintidx` only ever fires on functions `cyclop` and `funlen` already caught, it is paying runtime for nothing; drop it. It earns its place on codebases where the failures are long-flat-and-dense rather than deeply branched.

**File length** has no dedicated linter — `revive`'s `file-length-limit` rule is the only route, and it is the Go equivalent of `max-lines`:

```yaml
    revive:
      rules:
        - name: file-length-limit
          arguments: [{ max: 500, skipBlankLines: true, skipComments: true }]
        - name: max-control-nesting
          arguments: [4]
        - name: argument-limit
          arguments: [5]
        - name: cognitive-complexity
          disabled: true       # gocognit owns this
        - name: cyclomatic
          disabled: true       # cyclop owns this
        - name: function-length
          disabled: true       # funlen owns this
```

Disable revive's own complexity rules explicitly. revive overlaps three of the dedicated linters, and leaving them on is the same duplicate-diagnostic problem as `gocyclo` + `cyclop`.

Note that Go files legitimately run longer than TypeScript ones — a package is many files and the language has no `export` keyword forcing splits — so 500 is a looser bound here than it looks.

### Correctness — the bugs that compile

The five defaults (`errcheck`, `govet`, `ineffassign`, `staticcheck`, `unused`) are the floor. These are the additions that catch faults agents produce reliably:

```yaml
    - bodyclose            # unclosed HTTP response bodies — a leak that only shows under load
    - sqlclosecheck
    - rowserrcheck
    - contextcheck         # a function that uses a non-inherited context
    - noctx                # HTTP requests sent without a context
    - containedctx         # context.Context stored in a struct field
    - fatcontext           # contexts bloated inside a loop
    - errorlint            # Go 1.13+ wrapping: %w, errors.Is/As instead of == and type asserts
    - errname              # ErrFoo sentinels, FooError types
    - nilerr               # returns nil after checking err != nil
    - nilnesserr
    - nilnil               # returning (nil, nil)
    - durationcheck        # time.Duration multiplied by a Duration
    - copyloopvar
    - intrange
    - makezero
    - reassign
    - recvcheck            # mixed value and pointer receivers on one type
    - exhaustive           # non-exhaustive enum switches
    - forcetypeassert      # x.(T) without the ok form
    - asasalint
    - errchkjson
    - gocheckcompilerdirectives
    - protogetter          # only with protobuf
```

`errorlint` is the standout, and worth enabling all three of its checks — an error compared with `==` instead of `errors.Is` breaks the moment anything upstream starts wrapping, and it breaks silently:

```yaml
    errorlint:
      errorf: true
      asserts: true
      comparison: true
```

`nilerr` and `nilnil` both catch shapes of "the error was handled and then discarded", which is the Go dialect of swallowing a failure.

### Escape hatches

```yaml
    - nolintlint
```

```yaml
    nolintlint:
      require-explanation: true
      require-specific: true
      allow-unused: false
```

A bare `//nolint` disables every linter on that line and says nothing about why. `require-specific` forces `//nolint:errcheck`, `require-explanation` forces a reason after it. Without these two the whole config degrades one suppression at a time, and nothing in review catches it.

### Unfinished work

```yaml
    - godox
    - forbidigo
```

```yaml
    godox:
      keywords: [TODO, FIXME, BUG, HACK, XXX, WIP, OPTIMIZE]
    forbidigo:
      analyze-types: true
      forbid:
        - pattern: '^fmt\.Print.*$'
          msg: Use the structured logger, not fmt.Print.
        - pattern: '^print(ln)?$'
        - pattern: '^panic$'
          msg: Return an error instead of panicking outside package init.
```

`godox` is the highest-friction rule here and the one most likely to be argued about — it means a `TODO` cannot be committed. Present it with its consequence and the alternative out loud: TODOs go to the issue tracker. If the user wants them kept, the honest fallback in Go is to move `godox` to the advisory pass rather than drop it, since there is no `"warn"` tier.

Go's version of "agent fakes a finished function" is `panic("not implemented")`, and `forbidigo`'s `^panic$` pattern catches it — along with legitimate panics, which is why it needs a real conversation before it goes in. The narrower alternative is `revive`'s `deep-exit` rule (catches `os.Exit`/`log.Fatal` outside `main`) plus reviewing panics by hand.

### Magic values

```yaml
    - mnd
    - goconst
```

```yaml
    mnd:
      checks: [argument, case, condition, operation, return, assign]
      ignored-numbers: ["2", "10", "64", "100", "0644", "0755"]
      ignored-functions: ["strconv\\.Parse.*", "math\\..*", "time\\.(Duration|Sleep)"]
    goconst:
      min-len: 3
      min-occurrences: 3
      match-constant: true
      numbers: false
```

`0`, `1`, `1.0`, and `0.0` are always ignored by `mnd`, so the list only needs the domain's own noise: bit widths, base-10, file modes. Tune it against the actual finding list in the prove step — too short and every `strconv.ParseInt(s, 10, 64)` fails; too long and the rule stops meaning anything.

`goconst` catches the repeated string literal, which is the other half of the same problem and the one that produces genuine bugs when one of five copies gets a typo.

### Imports and architecture

**Go has no relative imports**, so the `../../utils` problem that `typescript.md` spends a rule on does not exist here — every import is a full module path. What Go needs instead is a rule about *which* module paths a package may reach.

`depguard` is that rule, and it is the most valuable configurable linter in the Go set, because it is the only way to enforce an architecture the compiler doesn't already know about:

```yaml
    - depguard
    - importas
    - gomodguard_v2
```

```yaml
    depguard:
      rules:
        # Keep a vendor SDK behind the one package that owns it.
        provider-sdks-behind-the-gateway:
          files:
            - "$all"
            - "!**/internal/gateway/**"
          deny:
            - pkg: "github.com/some/provider-sdk"
              desc: "Provider SDKs stay behind internal/gateway. See ADR-012."
        # Keep the domain layer free of transport and storage concerns.
        domain-stays-pure:
          files:
            - "**/internal/domain/**"
          deny:
            - pkg: "net/http"
              desc: "The domain layer must not know about transport."
            - pkg: "database/sql"
              desc: "The domain layer must not know about storage."
```

Two things make `depguard` rules worth writing rather than documenting. The `desc` is the whole interface — it appears at the point of failure, so a rule that cites the ADR teaches the constraint instead of just blocking. And the `files` list with `!` negation is what expresses "everywhere except the package that owns this", which is the shape almost every architectural boundary actually has.

Derive the rules from the repo's real boundaries — ask the user what must not import what, and check for existing ADRs. A `depguard` block copied from an example enforces someone else's architecture.

`importas` pins import aliases so the same package isn't `v1`, `apiv1`, and `corev1` in three files. Useful mainly with generated API clients.

### Naming and file placement

```yaml
    revive:
      rules:
        - name: filename-format
          arguments: ["^[_a-z][_a-z0-9]*\\.go$"]      # snake_case, Go's convention
        - name: package-directory-mismatch
        - name: var-naming
        - name: error-naming
        - name: error-strings
        - name: receiver-naming
        - name: confusing-naming
        - name: import-alias-naming
        - name: package-comments
```

Go's filename convention is **snake_case**, not kebab — `user_service.go`, and `user_service_test.go` beside it. `package-directory-mismatch` catches the package whose name has drifted from its directory, which is the thing that makes an import statement lie about what it imports.

**Test placement is free in Go.** The toolchain requires `_test.go` files to live in the same directory as the code they test, so the adjacency that `typescript.md` has to enforce through a config glob is enforced by the compiler here. Nothing to configure.

What is worth configuring is *which package* tests live in:

```yaml
    - testpackage
```

`testpackage` requires `package foo_test` rather than `package foo` — an external test package, which can only reach the exported surface. That makes the test suite an enforcement mechanism for the package's public interface: if a test needs an unexported symbol, either the symbol should be exported or the test is testing the implementation. `export_test.go` remains available for the cases where you genuinely need a peephole, and the linter's default `skip-regexp` already allows it.

### Readability

```yaml
    - dupl
    - dupword
    - misspell
    - whitespace
    - modernize          # rewrites to current language and stdlib features
    - perfsprint
    - prealloc
    - wastedassign
    - unconvert
    - unparam            # unused function parameters
    - usestdlibvars
    - mirror
    - exptostd
    - predeclared        # shadowing len, cap, new, …
    - goprintffuncname
    - godot
    - nakedret
    - dogsled
    - iface
    - interfacebloat
```

```yaml
    dupl:
      threshold: 150
    revive:
      rules:
        - name: early-return
        - name: indent-error-flow
        - name: superfluous-else
        - name: unnecessary-if
        - name: unnecessary-stmt
        - name: flag-parameter        # a bool parameter that switches behaviour
        - name: deep-exit             # os.Exit / log.Fatal outside main
        - name: unhandled-error
        - name: unchecked-type-assertion
        - name: use-any
        - name: use-errors-new
        - name: identical-branches
        - name: unused-parameter
        - name: unused-receiver
        - name: bool-literal-in-expr
        - name: constant-logical-expr
        - name: range-val-in-closure
        - name: modifies-parameter
        - name: unexported-return
```

`early-return`, `indent-error-flow`, and `superfluous-else` together enforce the single most Go-specific readability convention there is — handle the error and return, keep the happy path at the left margin. It is also the convention agents drift from most, because the `if/else` shape is what every other language taught them.

`flag-parameter` is the sleeper: a boolean argument that switches what a function does is two functions wearing a trench coat, and it is the most common way a small function becomes an unreadable one.

Four more worth **offering rather than assuming**, because each is a real position a team can reject:

- **`ireturn`** — accept interfaces, return concrete types. Correct as a default, wrong often enough (constructors returning an interface for testability) to need agreement.
- **`gochecknoglobals`** — right for application code, hostile to the sentinel-error and registry patterns that are idiomatic Go.
- **`wrapcheck`** — every error from another package must be wrapped. Excellent for error provenance, and noisy on a codebase that hasn't been doing it.
- **`err113`** — no dynamic errors, all sentinels. The strictest of the four, and the one most likely to be declined.

`gocritic` sits in the same bracket: a large, high-quality diagnostic set that is best introduced by enabling its `diagnostic` and `style` tags and reviewing the count, rather than switched on whole.

### Security

```yaml
    - gosec
    - bidichk
    - asciicheck
```

```yaml
    gosec:
      severity: medium
      confidence: medium
```

`gosec` covers the OWASP-shaped faults — hardcoded credentials, weak crypto, SQL string concatenation, unsafe file permissions, unhandled `crypto/rand` errors. The `severity`/`confidence` floor is what keeps it from drowning the run in low-confidence findings; start at `medium`/`medium` and lower it only if the user wants the long tail.

`bidichk` catches bidirectional-unicode trojan-source attacks, and costs nothing.

### Tests

```yaml
    - testpackage
    - thelper
    - tparallel
    - paralleltest
    - usetesting        # t.Setenv, t.TempDir, t.Context over the manual equivalents
    - testableexamples
    - testifylint       # only with stretchr/testify
```

`thelper` and `tparallel` catch the two things that make a failing test point at the wrong line: a helper that never calls `t.Helper()`, and `t.Parallel()` used in a way that breaks subtest isolation.

**Coverage** is a separate tool — golangci-lint doesn't measure it:

```bash
go test -race -coverprofile=coverage.out -covermode=atomic ./...
go tool cover -func=coverage.out | tail -1
```

Gate it with [`go-test-coverage`](https://github.com/vladopajic/go-test-coverage), which reads a small YAML file and supports per-file, per-package, and total thresholds. Same rule as everywhere: **set the threshold at or just below what the repo achieves today**, then ratchet. A threshold that fails on the day it lands is deleted within a week.

Run tests with `-race` in CI. Go's race detector finds a class of bug that no linter can, and concurrent code is where agent-written Go goes wrong most often.

### Observability — enable when detected

```yaml
    - sloglint          # log/slog
    - loggercheck       # zap, zerolog, logr, klog, kitlog
    - zerologlint
    - spancheck         # OpenTelemetry
    - musttag           # struct tags on marshaled types
    - canonicalheader
    - unqueryvet        # SELECT * in SQL
```

```yaml
    sloglint:
      context: scope        # require ctx only where the function already has one
      static-msg: true      # no fmt.Sprintf-built log messages
      key-naming-case: snake
    spancheck:
      checks: [end, record-error, set-status]
```

`sloglint`'s `static-msg` is the one that pays off later: a log message built with `Sprintf` cannot be grouped or alerted on, and an agent will build one every time unless something stops it. `spancheck` catches the span that never ends — a leak that shows up as missing traces rather than as an error.

## Formatters

Docs: <https://golangci-lint.run/docs/formatters/> and <https://golangci-lint.run/docs/formatters/configuration/>.

golangci-lint v2 owns formatting as well as linting, through a `formatters` block that is configured **separately from `linters`** and run by a separate command. Six are available: `gofmt`, `gofumpt`, `goimports`, `gci`, `golines`, `swaggo`.

Two commands, and both belong in the project:

```bash
golangci-lint fmt            # rewrites files in place
golangci-lint fmt --diff     # prints the diff, non-zero exit — the CI check
```

`fmt` is what the pre-commit hook runs; `fmt --diff` is what CI runs, so a badly formatted file fails the pipeline instead of arriving as a formatting-only diff in someone's review.

**The recommended set:**

```yaml
formatters:
  enable:
    - gofumpt          # supersedes gofmt — stricter, and backwards compatible
    - goimports        # adds/removes imports, groups local ones last
    - gci              # deterministic import section order
  settings:
    gofumpt:
      module-path: "github.com/org/repo"
      extra:
        group-params: true      # func f(a, b string) over func f(a string, b string)
        clothe-returns: true    # no naked returns in functions with named results
        balance-calls: true
    goimports:
      local-prefixes:
        - "github.com/org/repo"
    gci:
      sections:
        - standard
        - default
        - prefix(github.com/org/repo)
      custom-order: true
  exclusions:
    paths:
      - ".*\\.pb\\.go$"
      - ".*\\.connect\\.go$"
      - ".*_generated\\.go$"
```

Take the module path from `go.mod` — don't ask for something that's already written down. It appears three times above and must match in all three.

**Don't enable `gofmt` alongside `gofumpt`.** `gofumpt` is a strict superset: everything `gofmt` accepts, plus more. Running both is redundant, and the reason to reach for plain `gofmt` instead is only when a team has explicitly rejected gofumpt's extra rules. If you do use `gofmt`, its `rewrite-rules` are worth knowing — they mechanically migrate patterns like `interface{}` → `any` across a codebase.

`gofumpt`'s three `extra` rules are off by default and worth taking; they close the formatting decisions that otherwise get made differently in every file. Note the older `extra-rules: true` flag is deprecated in favour of the `extra` block — read the current docs rather than copying an older config.

**`goimports` and `gci` overlap, and that is fine** as long as they agree. `goimports` decides *which* imports exist and puts local ones after third-party; `gci` decides the exact section order and enforces it deterministically. `custom-order: true` is what makes `gci`'s `sections` list authoritative rather than advisory — without it, `gci` uses its own default order and your list is ignored. Set `local-prefixes` and `gci`'s `prefix(...)` to the same module path or the two will fight on every save.

`gci` also offers `blank`, `dot`, `alias`, and `localmodule` sections. They only apply if named — reach for them in a repo that has a real convention about blank imports (driver registration) worth pinning.

**`golines`** wraps long lines, and is worth **offering rather than assuming**. It rewrites code structure — breaking call arguments and chained methods across lines — rather than only adjusting whitespace, and some teams would rather have `lll` report a long line and decide by hand. If taken, `max-len: 120` pairs with `lll`'s default; leaving the two at different numbers means one tool creates work for the other.

```yaml
    golines:
      max-len: 120
      tab-len: 4
      shorten-comments: true
```

**`swaggo`** formats swag annotation comments. Enable it only if the repo has `swaggo/swag` annotations; it does nothing otherwise.

Exclude generated files from formatting as well as linting. Without it, every codegen run produces a formatting diff and people learn to ignore `git status`.

## Project structure

Go's own conventions, which the compiler partly enforces:

```sh
.
├── cmd/<binary>/main.go   # one directory per binary; main packages only
├── internal/              # everything else — compiler-enforced private
│   ├── <domain>/          # business logic, no transport or storage imports
│   ├── <transport>/       # HTTP/gRPC handlers
│   └── <storage>/         # repositories
├── pkg/                   # only if the repo genuinely publishes a library
└── go.mod
```

**`internal/` is the strongest boundary any language in this skill offers** — the compiler refuses imports of `internal/...` from outside the parent module. It costs nothing and cannot be bypassed by a `nolint` comment, so **default to putting everything under `internal/`** and moving a package out only when something outside the module needs it.

`pkg/` is widely cargo-culted and mostly a mistake: it means "anyone may import this forever", which is a promise most repos never intended to make. Ask before creating one.

Within `internal/`, layering is `depguard`'s job — the compiler has no opinion about whether the domain imports the transport layer, and without a rule it eventually will.

## Monorepo and multi-module

**Single module**: one `.golangci.yml` at the root. Nothing to decide.

**Multi-module with `go.work`**: one config at the workspace root, with `run.relative-path-mode: gomod` so exclusion paths resolve against each module's `go.mod` rather than the invocation directory. The import graph is cross-module, which is exactly why `depguard` rules belong at the root — a per-module config can't see the boundary it's meant to enforce.

Per-module `.golangci.yml` files are worth it only when modules genuinely diverge — a service and a code-generation tool have different rules about `fmt.Print`. golangci-lint reads the nearest config, so a per-module file **replaces** the root one rather than merging with it; anything the module still wants has to be restated. Say so, because the silent-loss failure here is easy to miss.

When lint runs in parallel across modules (`nx affected`, `turbo`, a matrix job), set `run.allow-parallel-runners: true` and raise `run.timeout` — parallel runners oversubscribe CI cores, and the resulting timeout looks like a hang rather than contention.
