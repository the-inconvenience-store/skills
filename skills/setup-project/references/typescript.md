# TypeScript baseline

The rules every TypeScript or JavaScript project gets, whatever framework sits on top. A React project reads this **and** [react.md](./react.md).

Default linter: **oxlint**. Fast enough to run on every commit, which is the only reason pre-commit hooks survive contact with a real repo.

Severities follow the skill's policy. Where a rule here deviates — or is worth offering rather than assuming — it says so at the rule.

## Docs to read before configuring

| Read | For |
| --- | --- |
| <https://oxc.rs/docs/guide/usage/linter/config.md> | `.oxlintrc.json` schema: `plugins`, `categories`, `rules`, `overrides`, `ignorePatterns`, `settings`, `jsPlugins`, `options` |
| <https://oxc.rs/docs/guide/usage/linter/plugins.md> | Which plugins are on by default, and that setting `plugins` **replaces** the default set |
| <https://oxc.rs/docs/guide/usage/linter/type-aware.md> | Type-aware mode — required by a chunk of the `typescript/` rules below |
| <https://oxc.rs/docs/guide/usage/linter/rules/<plugin>/<rule>.md> | Any individual rule's options. Append `.md` to any `oxc.rs` docs URL for the LLM-optimised copy |
| <https://github.com/dmmulroy/anti-slop> | The anti-slop plugin, its install script, and its rule list |
| <https://oxc.rs/docs/guide/usage/linter/js-plugins.md> | Authoring a custom rule, and the `jsPlugins` alias form |

Read the rule pages for anything you set options on. `complexity`, `max-lines`, `no-magic-numbers`, `no-warning-comments`, `filename-case`, and `no-restricted-imports` all have options that matter and that move between versions.

## Config skeleton

One `.oxlintrc.json` at the repo root. Add `$schema` so editors validate it.

```jsonc
{
  "$schema": "./node_modules/oxlint/configuration_schema.json",
  "plugins": ["eslint", "typescript", "unicorn", "oxc", "import", "promise"],
  "categories": {
    "correctness": "error",
    "suspicious": "error",
    "perf": "error",
    "pedantic": "off",
    "style": "off",
    "restriction": "off"
  },
  "ignorePatterns": [
    "dist/**",
    "build/**",
    "coverage/**",
    ".next/**",
    ".claude/**",
    ".agents/**",
    ".codex/**",
    ".cursor/**",
    "tools/oxlint/**"
  ],
  "rules": {
    /* the groups below */
  }
}
```

`plugins` **replaces** oxlint's default set, so the list has to name every plugin you want — including the defaults (`eslint`, `typescript`, `unicorn`, `oxc`). Forgetting one silently drops its rules.

`pedantic`, `style`, and `restriction` stay `off` as categories: too noisy wholesale, and most of what this skill wants lives in them. Name those rules individually in `rules` instead — an explicitly-listed rule beats its category setting.

### Type-aware rules

A number of the `typescript/` rules below need type information. Turn it on:

```jsonc
{ "options": { "typeAware": true } }
```

It is slower — measure it against the repo before wiring it into `pre-commit`. If it's too slow for a hook, run the type-aware pass in CI and the fast pass on commit. Read the type-aware doc for how to scope it.

## Rule groups

### Size and complexity — the two that matter most

```jsonc
{
  "eslint/complexity": ["warn", { "max": 12 }],
  "eslint/max-lines": ["warn", { "max": 500, "skipBlankLines": true, "skipComments": true }],
  "eslint/max-lines-per-function": ["error", { "max": 80, "skipBlankLines": true, "skipComments": true }],
  "eslint/max-depth": ["error", { "max": 3 }],
  "eslint/max-params": ["error", { "max": 4 }],
  "eslint/max-nested-callbacks": ["error", { "max": 3 }],
  "unicorn/max-nested-calls": ["error", { "max": 3 }]
}
```

`complexity` and `max-lines` are the **standing `"warn"` exceptions** — they are budgets, and a file at 520 lines is a nudge to split, not a broken build. Everything else in this group is `"error"`: a 200-line function or a 7-parameter signature is a defect now, not a budget overrun.

Left unchecked, an agent grows one file until nothing in it can be reasoned about. These are the rules that stop it.

#### Cognitive complexity — the second metric

Cyclomatic complexity and line count both miss the same thing: **how hard the code is to read**. A flat fifteen-case `switch` scores 15 cyclomatic and fails, though it is one of the most readable structures there is. Three nested loops with a labelled break score 4 and pass, though nobody can hold them in their head.

Cognitive complexity measures the second thing — it penalises nesting and breaks in linear flow, and does not penalise structures that are trivially scannable. oxlint has no native rule for it, so it comes from `eslint-plugin-sonarjs` through the JS plugin bridge:

```jsonc
{
  "jsPlugins": [{ "name": "sonarjs", "specifier": "eslint-plugin-sonarjs" }],
  "rules": {
    "sonarjs/cognitive-complexity": ["warn", 15],
    "sonarjs/no-identical-functions": "error",
    "sonarjs/no-duplicated-branches": "error",
    "sonarjs/no-collapsible-if": "error",
    "sonarjs/no-nested-conditional": "error"
  }
}
```

`cognitive-complexity` joins the `"warn"` budget tier for the same reason as `complexity`. The rest are `"error"` — a duplicated branch body or an identical function is a defect, not a budget.

`no-identical-functions` is the one to defend hardest here: copy-pasted logic is the most characteristic agent output there is, and no complexity metric sees it, because two copies of a simple function are two simple functions.

This is the largest plugin in the file (about 4 MB) and it carries its own `typescript` dependency, so **verify it loads under oxlint's `jsPlugins` before committing to it** — run lint and confirm the rules actually report. If it doesn't load, that is a real case for Section B's coexist branch rather than something to work around.

### Type laundering — anti-slop

Agents reach for `as unknown as T`, `unknown` parameters, and runtime `typeof` guards to make the type checker stop complaining. Every one of those is a type lie that survives into production. The [anti-slop](https://github.com/dmmulroy/anti-slop) plugin catches them.

It ships as a vendored plugin, not an npm dependency — read its `install-anti-slop` skill or repo README for the current install script, then:

- Copy the plugin into `tools/oxlint/anti-slop/`, and add that path to `ignorePatterns`.
- Install `@oxlint/plugins` pinned to **exactly** the repo's installed `oxlint` version, so both move together on upgrade.
- Register it and enable **every** generic rule at `"error"`:

```jsonc
{
  "jsPlugins": [{ "name": "anti-slop", "specifier": "./tools/oxlint/anti-slop/index.ts" }],
  "rules": {
    "anti-slop/no-chained-type-assertions": "error",
    "anti-slop/no-conditional-empty-object-spread": "error",
    "anti-slop/no-known-value-widening": "error",
    "anti-slop/no-module-mocking": "error",
    "anti-slop/no-object-parameters": "error",
    "anti-slop/no-reflect-apply": "error",
    "anti-slop/no-reflect-get": "error",
    "anti-slop/no-runtime-typeof": "error",
    "anti-slop/no-shape-in-symbol-names": "error",
    "anti-slop/no-unknown-parameters": "error",
    "anti-slop/no-unknown-returns": "error",
    "anti-slop/no-unknown-type-aliases": "error",
    "anti-slop/no-unsafe-dictionary-type": "error",
    "anti-slop/no-widen-then-assert": "error",
    "anti-slop/require-safety-comment-for-type-assertion": "error"
  }
}
```

The Effect group (`anti-slop-effect`) goes in **only** if `effect` is a direct dependency in a package manifest or the user asks for it — a transitive lockfile entry is not enough.

`anti-slop/no-object-parameters` is the one worth flagging to the user before installing: it bans single-object "options bag" parameters, which is a real style position, not just a slop guard. Some codebases are built on them. Offer it separately.

### Escape hatches

The rules above only hold if agents can't switch them off.

```jsonc
{
  "typescript/ban-ts-comment": ["error", { "ts-expect-error": "allow-with-description", "ts-ignore": true, "ts-nocheck": true }],
  "typescript/prefer-ts-expect-error": "error",
  "unicorn/no-abusive-eslint-disable": "error",
  "typescript/no-explicit-any": "error",
  "typescript/no-non-null-assertion": "error",
  "typescript/no-unsafe-type-assertion": "error"
}
```

`@ts-nocheck` at the top of a file deletes type safety for the whole file, and it's the first thing an agent reaches for under a deadline. `no-abusive-eslint-disable` stops the bare `// oxlint-disable-next-line` that disables everything rather than one named rule.

### Unfinished work

Agents bypass hard logic by leaving a marker and moving on. These make the marker fail the build, so the work either gets done or gets tracked as a real ticket.

```jsonc
{
  "eslint/no-warning-comments": ["error", { "terms": ["todo", "fixme", "xxx", "hack", "wip", "for now", "placeholder", "stub", "implement later", "not implemented"], "location": "anywhere" }],
  "eslint/no-empty-function": "error",
  "eslint/no-empty": "error",
  "vitest/no-disabled-tests": "error",
  "vitest/no-focused-tests": "error",
  "vitest/no-commented-out-tests": "error",
  "vitest/expect-expect": "error"
}
```

`no-warning-comments` is the highest-friction rule in this file, and the one most likely to be argued about. Present it explicitly with its consequence: a `TODO` cannot be committed. Say the alternative out loud — TODOs go to the issue tracker instead. If the user wants them kept, offer `"warn"` rather than dropping the rule.

`throw new Error("Not implemented")` — the other half of this pattern — has no built-in rule. Propose it as a custom rule (see **Custom rules** below); it is short and it is the single most common way an agent fakes a finished function.

### Magic values

```jsonc
{
  "eslint/no-magic-numbers": ["error", {
    "ignore": [-1, 0, 1, 2],
    "ignoreArrayIndexes": true,
    "ignoreDefaultValues": true,
    "enforceConst": true,
    "detectObjects": false
  }]
}
```

`ignore` is the option to tune with the user. Too small a list and every loop increment fails; too large and the rule stops meaning anything. `-1, 0, 1, 2` is a good default — it covers indices, `slice(0, 2)`, and `length - 1` while still catching `86400`, `0.25`, and `1024`.

### Imports and file placement

Absolute aliases, one direction of flow, no barrels, no cycles.

```jsonc
{
  "import/no-relative-parent-imports": "error",
  "import/no-cycle": "error",
  "import/no-duplicates": "error",
  "import/no-default-export": "error",
  "oxc/no-barrel-file": "error",
  "typescript/consistent-type-imports": ["error", { "prefer": "type-imports", "fixStyle": "inline-type-imports" }]
}
```

`import/no-relative-parent-imports` is what kills `../../utils/helper`. It requires the alias to exist first — set `compilerOptions.paths` in `tsconfig.json`, and the **matching alias in the bundler config**, or the rule will fail imports the build can't resolve:

```jsonc
// tsconfig.json
{ "compilerOptions": { "baseUrl": ".", "paths": { "@/*": ["./src/*"] } } }
```

One alias, `@/*` → `./src/*`. Short, and visibly distinct from a `node_modules` specifier, so nobody has to wonder what `@/lib/x` is. Resist multiple aliases (`@components`, `@hooks`); they buy nothing and each is one more thing to keep in sync across tsconfig, bundler, and test runner.

`import/no-default-export` needs `overrides` wherever a framework demands default exports — route files, config files, `*.stories.tsx`. Named exports are what make a symbol greppable and renameable; default exports let every importer call the same thing something different, which is exactly the drift that makes an agent-maintained codebase hard to navigate.

`oxc/no-barrel-file` stops `index.ts` files that re-export a whole subtree. Barrels break tree-shaking, and they make "where does this actually live" unanswerable without following two hops.

### Filenames

```jsonc
{ "unicorn/filename-case": ["error", { "case": "kebabCase" }] }
```

Kebab-case everywhere, including React components (`user-profile.tsx`, not `UserProfile.tsx`). One case for every file means a path is predictable from a name, which is how an agent finds a file without listing a directory. `index.*` files are exempt by the rule itself.

### Readability

The unicorn and eslint rules that most reliably improve agent-written code. All `"error"`.

```jsonc
{
  "eslint/eqeqeq": ["error", { "null": "ignore" }],
  "eslint/no-else-return": "error",
  "eslint/no-nested-ternary": "error",
  "eslint/no-param-reassign": ["error", { "props": true }],
  "eslint/no-shadow": "error",
  "eslint/no-var": "error",
  "eslint/prefer-const": "error",
  "eslint/prefer-template": "error",
  "eslint/no-console": ["error", { "allow": ["warn", "error"] }],
  "eslint/require-await": "error",
  "eslint/no-throw-literal": "error",
  "unicorn/catch-error-name": "error",
  "unicorn/consistent-function-scoping": "error",
  "unicorn/custom-error-definition": "error",
  "unicorn/error-message": "error",
  "unicorn/explicit-length-check": "error",
  "unicorn/no-lonely-if": "error",
  "unicorn/no-negated-condition": "error",
  "unicorn/no-unreadable-array-destructuring": "error",
  "unicorn/no-unreadable-iife": "error",
  "unicorn/prefer-node-protocol": "error",
  "unicorn/throw-new-error": "error"
}
```

`unicorn/consistent-function-scoping` is the sleeper here: it catches helper functions defined inside other functions that never close over anything, which is a signature agent pattern and the first step toward a 300-line function.

Two more worth **offering rather than assuming**, because both are genuine style positions a team can reasonably reject:

- `unicorn/no-array-reduce` — `reduce` is the most reliably unreadable array method, but banning it is opinionated.
- `unicorn/no-null` — coherent only if the codebase already treats `undefined` as its single absent value. On a codebase talking to a database or JSON API, it fights reality.

### Type safety, type-aware

Only with `"options": { "typeAware": true }`. These catch the bugs no syntactic rule can.

```jsonc
{
  "typescript/no-floating-promises": "error",
  "typescript/no-misused-promises": "error",
  "typescript/await-thenable": "error",
  "typescript/no-unnecessary-condition": "error",
  "typescript/no-unnecessary-type-assertion": "error",
  "typescript/switch-exhaustiveness-check": "error",
  "typescript/only-throw-error": "error",
  "typescript/prefer-nullish-coalescing": "error",
  "typescript/prefer-optional-chain": "error",
  "typescript/no-unsafe-argument": "error",
  "typescript/no-unsafe-assignment": "error",
  "typescript/no-unsafe-call": "error",
  "typescript/no-unsafe-member-access": "error",
  "typescript/no-unsafe-return": "error",
  "typescript/use-unknown-in-catch-callback-variable": "error"
}
```

`no-floating-promises` alone justifies turning type-aware mode on — an unawaited promise is the most common silent failure in agent-written async code.

## tsconfig

The linter can't fix a permissive compiler. Confirm these are on, and add any that are missing:

```jsonc
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "verbatimModuleSyntax": true,
    "isolatedModules": true
  }
}
```

`noUncheckedIndexedAccess` is the highest-value one after `strict`, and the one most likely to produce findings on an existing codebase — count them in the prove step before turning it on. `exactOptionalPropertyTypes` is the strictest and the most likely to be declined; offer it separately rather than folding it in silently.

## Tests

**Placement is deterministic: a unit test sits directly beside the file it covers.** `user-service.ts` is tested by `user-service.test.ts` in the same folder — never in a sibling `__tests__/` directory, never in a parallel `test/` tree. A test you can't find from the source file is a test nobody updates.

Integration and e2e tests are different animals — they cross module boundaries, so there is no single file to sit beside. They live in a dedicated directory (`e2e/`, or `src/app/**/*.integration.test.tsx` next to the route they exercise).

Enforce it through the test runner's `include` glob rather than a lint rule — a misplaced test simply doesn't run, which is loud:

```ts
// vitest.config.ts
test: {
  include: ["src/**/*.test.{ts,tsx}"],
  coverage: {
    provider: "v8",
    include: ["src/**/*.{ts,tsx}"],
    exclude: ["src/**/*.test.{ts,tsx}", "src/**/*.stories.tsx", "src/testing/**"],
    thresholds: { lines: 60, functions: 60, branches: 50, statements: 60 },
  },
}
```

Plus the filename rule and the test-quality rules:

```jsonc
{
  "plugins": ["vitest"],
  "rules": {
    "vitest/consistent-test-filename": ["error", { "pattern": ".*\\.test\\.[tj]sx?$" }],
    "vitest/no-identical-title": "error",
    "vitest/no-conditional-in-test": "error",
    "vitest/no-conditional-expect": "error",
    "vitest/valid-expect": "error",
    "vitest/prefer-strict-equal": "error"
  }
}
```

**Set the coverage threshold at or just below what the repo achieves today**, then ratchet. A threshold that fails on the day it lands gets deleted within a week; one that holds the current line and moves up on purpose survives. On a repo with no tests, set `0` and record the number — the ratchet needs a baseline more than it needs an aspiration.

`vitest/no-conditional-in-test` is worth defending: an `if` in a test is a test that silently passes when the branch it cares about isn't taken.

Jest projects get the equivalent from the `jest` plugin; the rule names map one to one.

## Monorepo and polyrepo

**Polyrepo** (one package — most repos): one `.oxlintrc.json` at the root. Nothing else to decide.

**Monorepo**: one root config with `overrides` keyed on path globs. One file to change, and packages that differ say so explicitly:

```jsonc
{
  "overrides": [
    {
      "files": ["packages/api/**"],
      "plugins": ["node"],
      "rules": { "eslint/no-console": "off" }
    },
    {
      "files": ["**/*.test.{ts,tsx}"],
      "rules": {
        "eslint/no-magic-numbers": "off",
        "eslint/max-lines": "off",
        "anti-slop/no-object-parameters": "off"
      }
    },
    {
      "files": ["**/*.config.{ts,js,mjs}", "**/*.stories.tsx"],
      "rules": { "import/no-default-export": "off" }
    }
  ]
}
```

The test override is not optional — test files are legitimately full of magic numbers (fixture data) and legitimately long. Leaving those rules on in tests produces exactly the noise that gets the whole config deleted.

Reach for per-package `.oxlintrc.json` files only when packages genuinely diverge in stack — a React app and a Node service in one repo. They inherit via `extends` from the root config; they don't restate it.

## Custom rules

Oxlint's JS plugin API is ESLint v9-compatible, so an ESLint rule works unmodified. Vendor custom rules in `tools/oxlint/<project>-rules/`, add that path to `ignorePatterns`, and register with the alias form:

```jsonc
{
  "jsPlugins": [{ "name": "project", "specifier": "./tools/oxlint/project-rules/index.ts" }],
  "rules": { "project/no-stub-implementation": "error" }
}
```

The one rule worth proposing on almost every project is `no-stub-implementation` — it catches the `throw new Error("Not implemented")` / `return null // TODO` pattern that `no-warning-comments` misses because there is no comment. Flag any function body that is a lone `throw` of an Error whose message matches `/not (yet )?implemented|unimplemented|todo/i`.

Everything else custom goes through [dependency-rules.md](./dependency-rules.md): search for an existing plugin first, author only when none exists, and always propose with the diagnostic message and a caught example before installing.

## Migrating from ESLint

`npx @oxlint/migrate` converts an existing ESLint config. It reports rules it could not map — **read that list with the user before deleting the ESLint config**. If something irreplaceable is on it, that is the case for Section B's coexist branch, and it should be named in the report.

The formatter is a separate decision from the linter. Prettier and `oxfmt` both work; if Tailwind is in play, both need pointing at the same CSS entry point as `oxlint-tailwindcss` so they agree byte-for-byte. Leave an existing formatter alone unless the user asks.
