# JavaScript and TypeScript rules

This is the authored baseline for agent-maintained code. Present applicable groups in the proposal; preserve coherent existing policy and calibrate noisy rules before enabling them. Default to `error` except the explicit budget rules.

Verify every rule and option against the chosen linter and installed plugin versions. Rule IDs below use oxlint-compatible namespaces; map them deliberately when another linter is approved. Within a comma-separated family, unqualified IDs inherit the namespace of the first fully qualified ID.

## Size and complexity

Budgets are advisory; structural limits block.

- `eslint/complexity`: warn at `12`.
- `sonarjs/cognitive-complexity`: warn at `15` when the plugin loads reliably.
- `eslint/max-lines`: warn at `500`, excluding blank lines and comments.
- `eslint/max-lines-per-function`: error at `80`, excluding blank lines and comments.
- `eslint/max-depth`: `3`; `eslint/max-params`: `4`; `eslint/max-nested-callbacks`: `3`; `unicorn/max-nested-calls`: `3`.
- `sonarjs/no-identical-functions`, `sonarjs/no-duplicated-branches`, `sonarjs/no-collapsible-if`, `sonarjs/no-nested-conditional`: error. `no-identical-functions` is the highest-value duplication check.

Measure plugin cost and findings. If cognitive and cyclomatic rules report the same code without adding information, keep the one that explains the project better.

## Type laundering and escape hatches

When the project accepts [anti-slop](https://github.com/dmmulroy/anti-slop), read that repository's current installation instructions and enable its generic rules at error. It is installed from the repository, so do not infer its files or setup from the rule names below:

- `anti-slop/no-chained-type-assertions`, `no-conditional-empty-object-spread`, `no-known-value-widening`, `no-module-mocking`, `no-reflect-apply`, `no-reflect-get`, `no-runtime-typeof`, `no-shape-in-symbol-names`.
- `anti-slop/no-unknown-parameters`, `no-unknown-returns`, `no-unknown-type-aliases`, `no-unsafe-dictionary-type`, `no-widen-then-assert`, `require-safety-comment-for-type-assertion`.
- Offer `anti-slop/no-object-parameters` separately: banning options objects is an architectural position.
- Enable the `anti-slop-effect` group only when Effect is a direct dependency or the user requests it.

Keep the escape routes closed:

- `typescript/ban-ts-comment`: require a description for `ts-expect-error`; reject `ts-ignore` and `ts-nocheck`.
- `typescript/prefer-ts-expect-error`, `typescript/no-explicit-any`, `typescript/no-non-null-assertion`, `typescript/no-unsafe-type-assertion`, `unicorn/no-abusive-eslint-disable`.

## Unfinished work and magic values

- `eslint/no-warning-comments`: flag `TODO`, `FIXME`, `XXX`, `HACK`, `WIP`, `for now`, `placeholder`, `stub`, `implement later`, and `not implemented`. Explain that accepted TODOs must move to the issue tracker; offer warn if the team intentionally keeps inline TODOs.
- `eslint/no-empty-function`, `eslint/no-empty`.
- Propose a narrow project rule such as `project/no-stub-implementation` for lone `throw new Error("Not implemented")` or equivalent return stubs. Search for an existing maintained rule first.
- `eslint/no-magic-numbers`: default ignored numbers `-1, 0, 1, 2`; ignore array indexes and default values; enforce constants. Tune domain constants with the user.

## Imports, placement, and names

Offer these when the repository has or accepts the supporting conventions:

- `import/no-relative-parent-imports`, after a matching compiler, bundler, and test-runner alias exists.
- `import/no-cycle`, `import/no-duplicates`, `typescript/consistent-type-imports` with inline type imports.
- `import/no-default-export`, with explicit overrides for framework routes, configuration, and stories that require defaults.
- `oxc/no-barrel-file`.
- `eslint/no-restricted-imports` for approved dependency boundaries, with messages that name the supported route.
- `unicorn/filename-case` with `kebabCase` only when the user accepts that filename convention.

Derive dependency-boundary restrictions from the real architecture. A copied `no-restricted-imports` pattern enforces somebody else's design.

## Readability

Recommended at error:

- `eslint/eqeqeq` with the null exception, `no-else-return`, `no-nested-ternary`, `no-param-reassign`, `no-shadow`, `no-var`, `prefer-const`, `prefer-template`.
- `eslint/no-console` allowing `warn` and `error`, `require-await`, `no-throw-literal`.
- `unicorn/catch-error-name`, `consistent-function-scoping`, `custom-error-definition`, `error-message`, `explicit-length-check`, `no-lonely-if`, `no-negated-condition`, `no-unreadable-array-destructuring`, `no-unreadable-iife`, `prefer-node-protocol`, `throw-new-error`.

Offer rather than assume `unicorn/no-array-reduce` and `unicorn/no-null`; both encode legitimate but disputable style positions.

## Type-aware safety

Enable only when the chosen linter has working type-aware analysis. Keep a faster syntactic pass for local hooks if necessary.

- Promises: `typescript/no-floating-promises`, `no-misused-promises`, `await-thenable`.
- Exhaustiveness and conditions: `no-unnecessary-condition`, `no-unnecessary-type-assertion`, `switch-exhaustiveness-check`.
- Values crossing unsafe boundaries: `no-unsafe-argument`, `no-unsafe-assignment`, `no-unsafe-call`, `no-unsafe-member-access`, `no-unsafe-return`.
- Error and syntax improvements: `only-throw-error`, `prefer-nullish-coalescing`, `prefer-optional-chain`, `use-unknown-in-catch-callback-variable`.

`no-floating-promises` is the priority when the full set is too expensive.

## Compiler checks

The linter does not replace the compiler. For a new strict TypeScript project, propose `strict`, `noUncheckedIndexedAccess`, `noImplicitOverride`, `noFallthroughCasesInSwitch`, `noUnusedLocals`, `noUnusedParameters`, `verbatimModuleSyntax`, and `isolatedModules`.

Offer `exactOptionalPropertyTypes` separately and count its findings before enabling it in an existing project. `noUncheckedIndexedAccess` deserves the same migration check.

## Tests

For Vitest, recommend:

- Unfinished tests: `vitest/no-disabled-tests`, `no-focused-tests`, `no-commented-out-tests`, `expect-expect`.
- Correctness: `vitest/no-identical-title`, `no-conditional-in-test`, `no-conditional-expect`, `valid-expect`, `prefer-strict-equal`.
- Naming: `vitest/consistent-test-filename` with the project's accepted test suffix.

Map to the Jest equivalents when Jest is detected. Offer colocated unit tests, coverage thresholds, and test-directory changes as separate choices; they are not implied by accepting these lint rules.

## Overrides

Tests, generated files, framework entry points, stories, and configuration files often need scoped exceptions. Make each override explain a real context. Blanket disables and repository-wide ignore patterns are not rollout strategies.
