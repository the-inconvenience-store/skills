# React

Read this **with** [typescript.md](./typescript.md) — that file carries the baseline (size budgets, anti-slop, aliases, filename case, tests, monorepo layout) and this one adds what React needs on top. Neither is complete alone.

Applies to React SPAs, Next.js, React Native, Expo, Remix / React Router v7, and TanStack Start. Framework-specific additions are at the bottom.

## Docs to read before configuring

| Read | For |
| --- | --- |
| <https://www.react.doctor/docs/configuration/eslint-and-oxlint-plugins> | Wiring `oxlint-plugin-react-doctor`, the ESLint-only presets (`recommended`, `next`, `react-native`, `tanstack-start`, `tanstack-query`, `preact`, `all`), and which rules don't run standalone |
| <https://www.react.doctor/docs/rules> | The rule catalogue — several hundred rules, so read the index and pick groups, don't enumerate |
| <https://oxlint-tailwindcss.pages.dev/setup> | `oxlint-tailwindcss` install, the `entryPoint` setting, and the monorepo glob→CSS mapping |
| <https://oxlint-tailwindcss.pages.dev/rules/> | Per-rule pages for the 24 Tailwind rules |
| <https://github.com/rxrdev/oxlint-plugin-i18n-literal> | The i18n literal rules, presets, and ignore options |
| <https://github.com/alan2207/bulletproof-react/tree/master/docs> | The structure and standards this file condenses, if a decision needs the original argument |
| <https://oxc.rs/docs/guide/usage/linter/rules/> | The native `react`, `react-perf`, `jsx-a11y`, and `nextjs` rule lists |

## Structure

Condensed from bulletproof-react. The whole point is that **a feature is a unit you can read, move, or delete without tracing the rest of the app**.

```sh
src
├── app/            # application layer: routes/pages, app.tsx, provider.tsx, router.tsx
├── assets/         # static files
├── components/     # shared components used across the whole app
├── config/         # global config, exported env vars
├── features/       # feature modules — most code lives here
├── hooks/          # shared hooks
├── lib/            # reusable libraries preconfigured for this app
├── stores/         # global state stores
├── testing/        # test utilities and mocks
├── types/          # shared types
└── utils/          # shared utility functions
```

A feature carries only the folders it needs:

```sh
src/features/awesome-feature
├── api/            # request declarations and query/mutation hooks for this feature
├── assets/
├── components/     # components scoped to this feature
├── hooks/
├── stores/
├── types/
└── utils/
```

Three rules govern how code moves between those folders:

- **No cross-feature imports.** `features/discussions` never imports from `features/comments`. Features compose at the **app** layer, which is what keeps each one independently readable.
- **Imports flow one way**: `shared → features → app`. Shared code (`components`, `hooks`, `lib`, `types`, `utils`, `config`) is reachable from anywhere; `features` may reach shared; `app` may reach both. Never the reverse. A shared component importing from a feature is the moment "shared" stops meaning anything.
- **No barrel files.** Import the file directly (`@/features/discussions/api/get-discussions`), not through a re-exporting `index.ts`. Barrels break tree-shaking and hide where a symbol actually lives.

`api/` may instead live at `src/api/` when most requests are shared between features. Pick one and say which in the conventions doc.

### Enforcing the structure

Unidirectional flow is two `overrides` entries — general, and no maintenance as features are added:

```jsonc
{
  "overrides": [
    {
      "files": ["src/components/**", "src/hooks/**", "src/lib/**", "src/types/**", "src/utils/**", "src/config/**", "src/stores/**"],
      "rules": {
        "eslint/no-restricted-imports": ["error", { "patterns": [
          { "group": ["@/features/*", "@/features/**", "@/app/*", "@/app/**"],
            "message": "Shared code cannot import from features or app. Imports flow shared → features → app." }
        ]}]
      }
    },
    {
      "files": ["src/features/**"],
      "rules": {
        "eslint/no-restricted-imports": ["error", { "patterns": [
          { "group": ["@/app/*", "@/app/**"],
            "message": "Features cannot import from app. Compose features at the app layer instead." }
        ]}]
      }
    }
  ]
}
```

Cross-feature bans need **one override per feature**, because the rule has to allow a feature to import its own files:

```jsonc
{
  "files": ["src/features/discussions/**"],
  "rules": {
    "eslint/no-restricted-imports": ["error", { "patterns": [
      { "group": ["@/features/*", "@/features/**", "!@/features/discussions/**", "@/app/*", "@/app/**"],
        "message": "No cross-feature imports. Compose features at the app layer." }
    ]}]
  }
}
```

Generate one of these per feature found in step 1, and say plainly in the conventions doc that **adding a feature means adding its override** — an unlisted feature is silently unenforced. On a repo where features churn constantly, [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) expresses the same rule once with a back-reference instead of one entry per feature; offer it as the alternative, at the cost of a second tool in the check pipeline.

Verify the negation pattern actually works in the installed oxlint version — at the prove step, import across features and watch it fail, then import within a feature and watch it pass.

## Plugins

### react.doctor — the biggest single win

`oxlint-plugin-react-doctor` catches the React-specific faults no generic rule sees. It carries **roughly 880 rules**, organised into Accessibility, Architecture, Bugs, Bundle Size, Correctness, Design, Maintainability, Next.js, and Performance.

```jsonc
{
  "jsPlugins": [{ "name": "react-doctor", "specifier": "oxlint-plugin-react-doctor" }],
  "rules": { /* the clusters below */ }
}
```

**Read <https://www.react.doctor/docs/rules> and work the index category by category.** The starter clusters below are a floor, not a ceiling — they are the rules that pay off on every React codebase, chosen so a first run is useful rather than overwhelming. The catalogue is much larger than this file, and it grows.

#### Three things to settle before writing the rule list

**1. The presets are an ESLint feature. Under oxlint you enumerate.**

react.doctor ships named configs — `recommended` (the framework-independent rules), `next`, `react-native`, `tanstack-start`, `tanstack-query`, `preact`, and `all` (every rule across every framework). They are reachable only through `eslint-plugin-react-doctor`'s flat config:

```js
// eslint.config.js — ESLint only
import reactDoctor from "eslint-plugin-react-doctor";
export default [
  reactDoctor.configs.recommended,
  reactDoctor.configs.next,
  reactDoctor.configs["react-native"],
  reactDoctor.configs["tanstack-start"],
  reactDoctor.configs["tanstack-query"],
  reactDoctor.configs.preact,
];
```

`oxlint-plugin-react-doctor` **exports no configs**, and oxlint's `extends` takes config files, not a plugin's exported presets. Under oxlint you name every rule in `rules`.

So use the preset names as a **shopping list**, not as config: they tell you which rule families a given stack needs. Map what step 1 detected onto the families table further down, and enumerate those. If the project is on ESLint rather than oxlint, the presets are the better route and worth mentioning as one advantage of Section B's coexist branch.

**2. It ports oxlint's native React rules — don't run both.**

The plugin's `react-builtins/` and `a11y/` buckets are **100 rules ported from oxlint's own `react`, `react_perf`, and `jsx_a11y` crates**, re-exposed as `react-doctor/*`. `rules-of-hooks`, `exhaustive-deps`, `alt-text`, `jsx-key`, `no-array-index-key` and the rest all exist in both places.

Pick one source and say which:

- **react.doctor's copies** (recommended when the plugin is installed) — one plugin, one namespace, and its `exhaustive-deps` and `rules-of-hooks` run on its own scope-analysis and control-flow port. Then **drop `react`, `react-perf`, and `jsx-a11y` from `plugins`** and skip the two native clusters below.
- **oxlint's natives** — native Rust rules, faster, and take the react.doctor plugin for everything else. Then skip react.doctor's `react-builtins/` and `a11y/` rules.

Enabling both double-reports about a hundred rules, which is the fastest way to get the whole config deleted.

**3. Project-scan rules do not run under the plugin.**

react.doctor's whole-project checks — the `security-scan` family, and `unused-file`, `unused-export`, `unused-type`, `unused-dependency`, `unused-dev-dependency`, `circular-dependency` — **register metadata in the plugin but never fire**. They need the react.doctor CLI, which is a separate tool with its own `doctor.config.*`.

Naming them in `.oxlintrc.json` produces a config that looks like it covers dead code and does not. If the user wants those checks, the answer is the CLI in CI, not a rule entry. A handful of other CLI-only rules exist too (`duplicate-jsx-subtree`, `no-high-complexity-react-function`, `no-derived-useState`, `prefer-useReducer`, `require-reduced-motion`) — which is why the next point matters.

#### Verify every rule against the installed plugin

Rule names in the docs site track the **CLI**; the plugin is a subset and moves independently. An unrecognised plugin rule can sit in the config doing nothing rather than failing loudly, so check before committing to a list:

```bash
grep -oE '"react-doctor/[a-z0-9-]+"' \
  node_modules/oxlint-plugin-react-doctor/dist/index.d.ts \
  | tr -d '"' | sed 's|react-doctor/||' | sort -u
```

Diff your intended rule list against that. Anything missing is CLI-only — drop it and say so in the report rather than leaving an inert entry.

Then add with discretion, on two further tests:

- **Does the fault it catches exist in this codebase?** The `r3f-*` (79 rules), `three-*` (106), `remotion-*`, `ink-*`, and `mobx-*` families are dead weight unless the library is a dependency. Match the family to what step 1 detected.
- **What is the finding count on this repo?** The prove step answers this. A cluster producing hundreds of hits is a decision for the user, not a rule to switch on quietly.

react.doctor's own docs default to `"warn"`; install at `"error"` per the severity policy, bar the budget rules noted below.

**Effects and lifecycle** — the largest source of real React bugs, and the cluster agents get wrong most often:

```jsonc
{
  "react-doctor/no-fetch-in-effect": "error",
  "react-doctor/no-async-effect-callback": "error",
  "react-doctor/effect-needs-cleanup": "error",
  "react-doctor/effect-listener-cleanup-mismatch": "error",
  "react-doctor/effect-observer-needs-disconnect": "error",
  "react-doctor/effect-raf-loop-needs-cancel": "error",
  "react-doctor/no-effect-chain": "error",
  "react-doctor/no-self-updating-effect": "error",
  "react-doctor/no-set-state-after-await-in-effect": "error",
  "react-doctor/no-effect-event-in-deps": "error",
  "react-doctor/no-mirror-prop-effect": "error",
  "react-doctor/no-prop-callback-in-effect": "error",
  "react-doctor/no-stale-timer-ref": "error",
  "react-doctor/debounce-no-cleanup": "error",
  "react-doctor/prefer-use-effect-event": "error"
}
```

**Derived state** — the single most common React mistake, and the one agents reproduce most reliably. Every rule here catches a variant of "copy a prop into state and try to keep them in sync":

```jsonc
{
  "react-doctor/no-derived-state": "error",
  "react-doctor/no-derived-state-effect": "error",
  "react-doctor/no-adjust-state-on-prop-change": "error",
  "react-doctor/no-reset-all-state-on-prop-change": "error",
  "react-doctor/no-event-trigger-state": "error",
  "react-doctor/no-initialize-state": "error"
}
```

**State updates** — mutation and sequencing faults that produce intermittent bugs rather than crashes, so nothing catches them at runtime:

```jsonc
{
  "react-doctor/no-direct-state-mutation": "error",
  "react-doctor/no-impure-state-updater": "error",
  "react-doctor/no-side-effect-in-state-updater-function": "error",
  "react-doctor/no-cascading-set-state": "error",
  "react-doctor/no-chain-state-updates": "error",
  "react-doctor/no-boolean-toggle-without-functional-update": "error",
  "react-doctor/no-mutating-reducer-state": "error",
  "react-doctor/no-mutating-array-method-on-prop-or-hook-result": "error",
  "react-doctor/no-mutate-then-set-or-return-same-reference": "error",
  "react-doctor/no-set-state-in-render": "error",
  "react-doctor/no-render-in-render": "error",
  "react-doctor/no-pass-live-state-to-parent": "error",
  "react-doctor/no-uncontrolled-input": "error",
  "react-doctor/no-controlled-input-value-without-state-update": "error"
}
```

**Render purity** — work that must not happen during render, because React may call render twice or throw the result away:

```jsonc
{
  "react-doctor/no-create-context-in-render": "error",
  "react-doctor/no-create-store-in-render": "error",
  "react-doctor/no-create-ref-in-function-component": "error",
  "react-doctor/no-create-object-url-in-render": "error",
  "react-doctor/no-create-object-url-without-revoke": "error",
  "react-doctor/no-ref-current-in-render": "error",
  "react-doctor/no-nondeterministic-id-value-in-render-body": "error",
  "react-doctor/no-random-key": "error",
  "react-doctor/no-impure-call-at-module-scope": "error",
  "react-doctor/no-unguarded-browser-global-in-render-or-hook-init": "error",
  "react-doctor/no-unguarded-browser-global-at-module-scope": "error",
  "react-doctor/no-hydration-branch-on-browser-global": "error",
  "react-doctor/no-match-media-in-state-initializer": "error",
  "react-doctor/no-nested-component-definition": "error",
  "react-doctor/no-inline-hoc-on-component": "error",
  "react-doctor/no-call-component-as-function": "error"
}
```

**Async and data safety** — where agent-written code silently swallows failures. This cluster is worth defending as hard as the effects one; every rule here is a bug that only shows up in production:

```jsonc
{
  "react-doctor/no-fetch-response-used-without-status-check": "error",
  "react-doctor/no-collapse-request-error-to-empty-state": "error",
  "react-doctor/no-floating-then-in-jsx-handler": "error",
  "react-doctor/no-promise-then-side-effect-in-effect-without-catch": "error",
  "react-doctor/no-async-event-handler-without-reentry-guard": "error",
  "react-doctor/no-loading-flag-reset-outside-finally": "error",
  "react-doctor/no-unsafe-json-parse": "error",
  "react-doctor/no-unguarded-throwing-parse-call": "error",
  "react-doctor/no-unguarded-numeric-input-parse": "error",
  "react-doctor/no-object-keys-values-entries-on-maybe-undefined": "error",
  "react-doctor/no-array-find-result-member-access-without-guard": "error",
  "react-doctor/no-non-null-assertion-on-maybe-undefined-result": "error",
  "react-doctor/no-arithmetic-on-optional-chained-operand": "error",
  "react-doctor/no-nullish-coalescing-arithmetic-precedence": "error",
  "react-doctor/no-collapsed-literal-or-chain-as-value": "error",
  "react-doctor/no-object-or-array-coerced-to-string-in-template-literal": "error"
}
```

**Maintainability** — the React-shaped versions of the size budgets in [typescript.md](./typescript.md). They see components and hooks where `max-lines` sees only a file, so they catch the 400-line component that a 500-line file budget lets through:

```jsonc
{
  "react-doctor/no-giant-component": "warn",
  "react-doctor/no-many-boolean-props": "error",
  "react-doctor/no-generic-handler-names": "error",
  "react-doctor/no-polymorphic-children": "error",
  "react-doctor/no-render-prop-children": "error",
  "react-doctor/no-barrel-import": "error",
  "react-doctor/no-full-lodash-import": "error",
  "react-doctor/no-moment": "error"
}
```

`no-giant-component` is a budget, so it takes `"warn"` on the same reasoning as `complexity` and `max-lines`. It sees a *component* where `max-lines` sees only a file, which is what catches the 400-line component in a 480-line file.

Two more this cluster would want are **CLI-only** — `no-high-complexity-react-function` and `duplicate-jsx-subtree`. The second is a real loss: copy-pasted JSX is the most characteristic agent output there is, and it is exactly what a reviewer stops noticing after the third occurrence. If the user cares about it, that is an argument for running the react.doctor CLI in CI alongside the plugin — say so rather than leaving the gap silent. `sonarjs/no-identical-functions` from [typescript.md](./typescript.md) covers the non-JSX half of the same problem.

**Rendering performance** — offer these as a group, and ask whether the React Compiler is on first. With the compiler enabled, several become redundant and `react-compiler-no-manual-memoization` becomes the one that matters:

```jsonc
{
  "react-doctor/rerender-dependencies": "error",
  "react-doctor/rerender-functional-setstate": "error",
  "react-doctor/rerender-lazy-state-init": "error",
  "react-doctor/rerender-lazy-ref-init": "error",
  "react-doctor/rerender-memo-before-early-return": "error",
  "react-doctor/no-whole-object-dep-with-member-reads": "error",
  "react-doctor/no-mutable-in-deps": "error",
  "react-doctor/hooks-no-nan-in-deps": "error",
  "react-doctor/no-usememo-simple-expression": "error",
  "react-doctor/no-inline-prop-on-memo-component": "error",
  "react-doctor/no-unthrottled-scroll-mutation": "error",
  "react-doctor/no-locale-format-in-render": "error",
  "react-doctor/no-unbounded-animation-frame-loop": "error"
}
```

**Client-side security** — cheap to enable, and the failure mode is a leaked secret rather than a slow render:

```jsonc
{
  "react-doctor/no-secrets-in-client-code": "error",
  "react-doctor/public-env-secret-name": "error",
  "react-doctor/auth-token-in-web-storage": "error",
  "react-doctor/dangerous-html-sink": "error",
  "react-doctor/no-eval": "error",
  "react-doctor/window-open-without-noopener": "error",
  "react-doctor/postmessage-origin-risk": "error",
  "react-doctor/untrusted-redirect-following": "error",
  "react-doctor/no-dynamic-import-path": "error",
  "react-doctor/unsafe-json-in-html": "error",
  "react-doctor/no-unescaped-dynamic-string-in-regexp": "error"
}
```

The `firebase-*`, `supabase-*`, `nosql-injection-risk`, and `raw-sql-injection-risk` families go in only when the matching backend is a dependency — the Supabase and Firebase ones catch missing row-level security and client-owned authorization fields, which are the two ways an agent-built app ships a public database.

**The single-file rules above do run under the plugin; the whole-project ones don't.** react.doctor's `security-scan` category — repo-wide secret, configuration, and build-artifact checks — registers metadata in the plugin but only executes under the CLI. If secret scanning matters to this project, that is either the react.doctor CLI in CI or a dedicated tool like `gitleaks`; a rule entry in `.oxlintrc.json` will not do it.

**Accessibility** — react.doctor goes considerably further than `jsx-a11y`, and these are the additions rather than the overlap:

```jsonc
{
  "react-doctor/html-no-nested-interactive": "error",
  "react-doctor/html-label-has-single-control": "error",
  "react-doctor/html-no-nested-form": "error",
  "react-doctor/html-no-invalid-table-nesting": "error",
  "react-doctor/form-control-requires-name": "error",
  "react-doctor/radio-input-missing-name": "error",
  "react-doctor/fieldset-requires-legend": "error",
  "react-doctor/dialog-has-accessible-name": "error",
  "react-doctor/details-requires-summary": "error",
  "react-doctor/data-table-requires-accessible-name": "error",
  "react-doctor/no-skipped-heading-level": "error",
  "react-doctor/no-multiple-main-landmarks": "error",
  "react-doctor/no-focusable-content-in-aria-hidden": "error",
  "react-doctor/no-invisible-focus-control": "error",
  "react-doctor/no-outline-none": "error",
  "react-doctor/no-uninformative-aria-label": "error",
  "react-doctor/no-placeholder-only-field": "error",
  "react-doctor/role-button-requires-complete-keyboard-activation": "error",
  "react-doctor/no-disabled-zoom": "error",
  "react-doctor/require-reduced-motion": "error"
}
```

**Design** — the anti-slop rules for UI, and the cluster most worth raising with the user explicitly. **They are disabled by default**, so nothing here happens unless it is named.

This family catches the visual signature of AI-generated interfaces: the purple-blue gradient, the decorative blur orb, the glassmorphic card repeated six times, the emoji in the heading, the persona placeholder copy, the vague "Get started" button. None of it is broken, which is exactly why nothing else flags it, and why it accumulates until an app looks generated.

```jsonc
{
  "react-doctor/no-default-purple-page-gradient": "error",
  "react-doctor/no-generic-purple-blue-icon-gradient": "error",
  "react-doctor/no-decorative-blur-orb": "error",
  "react-doctor/no-decorative-radial-spotlight": "error",
  "react-doctor/no-decorative-grid-background": "error",
  "react-doctor/no-decorative-pulse": "error",
  "react-doctor/no-repeated-glass-surfaces": "error",
  "react-doctor/no-repeated-section-shells": "error",
  "react-doctor/no-uniform-feature-card-grid": "error",
  "react-doctor/no-empty-card-shell": "error",
  "react-doctor/no-nested-card-surface": "error",
  "react-doctor/no-emoji-heading-decoration": "error",
  "react-doctor/no-fake-browser-chrome": "error",
  "react-doctor/design-no-vague-button-label": "error",
  "react-doctor/design-no-em-dash-in-jsx-text": "error",
  "react-doctor/design-no-three-period-ellipsis": "error",
  "react-doctor/no-generic-marketing-copy": "error",
  "react-doctor/no-placeholder-persona-copy": "error",
  "react-doctor/no-repeated-kicker-labels": "error",
  "react-doctor/no-tiny-text": "error",
  "react-doctor/no-low-contrast-inline-style": "error",
  "react-doctor/no-flat-page-type-scale": "error",
  "react-doctor/no-monotonous-page-spacing": "error",
  "react-doctor/no-transition-all": "error",
  "react-doctor/no-z-index-9999": "error"
}
```

react.doctor calls these **creative-direction reviews** — its own framing is that the tag makes a rule opinionated, never optional-because-trivial. Present the whole family to the user as one yes/no with an example or two, and read the index for the rest; there are far more than these, particularly around typography and spacing. On a project with a real design system and a designer, some will conflict with deliberate choices — that is a reason to drop the specific rule, not the family.

**Project-graph rules — CLI only, not the plugin.** Dead code and cycles (`unused-file`, `unused-export`, `unused-type`, `unused-dependency`, `unused-dev-dependency`, `circular-dependency`) need a whole-project scan, so they exist in the react.doctor CLI and **do nothing in `.oxlintrc.json`**. Don't put them there.

They are worth wanting: `unused-export` and `unused-file` catch the cleanup agents never do on their own — an agent writes a helper, replaces it two turns later, and leaves the first one behind forever. If the user wants them, offer the react.doctor CLI as a **separate CI step** (its own `doctor.config.*`, with a `categories` block), never in a git hook — a full-project scan blows the pre-commit budget outright. `knip` is the alternative if they'd rather not add a second react.doctor surface.

**Library families** — enable only what step 1 detected. Counts are from the installed plugin; verify with the `grep` recipe above.

Four of these correspond to a named ESLint preset (`next`, `react-native`, `tanstack-start`, `tanstack-query`, plus `preact`) — under oxlint the preset name is just the label for the family you enumerate.

| Detected | Family | Preset |
| --- | --- | --- |
| Next.js | `nextjs-*` — 25 rules, well beyond oxlint's native `nextjs` plugin: unawaited async dynamic APIs, missing Suspense around `useSearchParams`, client fetching of server data, redirect inside `try`/`catch` | `next` |
| React Native / Expo | `rn-*` — 41 rules on lists, Reanimated, Pressable, bottom sheets, deprecated modules | `react-native` |
| TanStack Start | `tanstack-start-*` — 15 rules: loader waterfalls, unvalidated server function input, secrets in loaders, route property order | `tanstack-start` |
| TanStack Query | `query-*` — 9 rules: missing invalidation after a mutation, queries in effects, rest-destructuring the result, void query functions | `tanstack-query` |
| Preact | `preact-*` — 5 rules: React hook imports, `onInput` over `onChange`, render arguments | `preact` |
| React Router / Remix | `react-router-*` — 38 rules covering loaders, middleware, sessions, and route config | — |
| Framer Motion | `motion-*` — 12 rules: `AnimatePresence` keying and lifetime, motion values constructed in render | — |
| Zustand / Jotai / Redux / Valtio / MobX | `zustand-*` (4), `jotai-*` (3), `redux-*`, `valtio-*`, `mobx-*` | — |
| React Three Fiber / three.js | `r3f-*` (79), `three-*` (106) — by far the largest families, and pure noise without the dependency | — |
| Remotion / Ink | `remotion-*` (9), `ink-*` (22) | — |
| Zod v4 | `zod-v4-*` — deprecated error APIs and schema APIs | — |
| styled-components, shadcn, react-markdown | `styled-components-*`, `shadcn-*`, `react-markdown-*` | — |

The `all` preset enables every rule across every framework. Don't reach for it: on a Next.js app it turns on 106 three.js rules and 22 terminal-UI rules that can only ever produce noise.

**Server Components** — the `server-*` family, when the framework has them (Next App Router, TanStack Start). `server-auth-actions`, `server-no-mutable-module-state`, `server-sequential-independent-await`, and `server-fetch-without-revalidate` are the ones that catch real faults; module-scope mutable state in a server component is a cross-request data leak.

If the project also runs react.doctor's own CLI or GitHub Action, its config is a separate `doctor.config.*` file with a `categories` block (`Security`, `Bugs`, `Performance`, `Accessibility`, `Maintainability`). Category-level severity is a CLI feature — through the oxlint plugin, rules are named individually in `.oxlintrc.json`. Don't assume `categories` works there; check, and enumerate if it doesn't.

### Native oxlint plugins

**Skip this whole section if the react.doctor plugin is installed and you took its ported copies** — the two overlap by about 100 rules, per the fork above. This is the other branch: native Rust rules, no JS plugin in the loop.

Add to `plugins`, then name the rules that matter. `react` and `jsx-a11y` are **not** on by default.

```jsonc
{ "plugins": ["eslint", "typescript", "unicorn", "oxc", "import", "promise", "react", "react-perf", "jsx-a11y"] }
```

**React correctness** — the rules that catch actual bugs:

```jsonc
{
  "react/rules-of-hooks": "error",
  "react/exhaustive-deps": "error",
  "react/jsx-key": "error",
  "react/no-array-index-key": "error",
  "react/no-unstable-nested-components": "error",
  "react/jsx-no-constructed-context-values": "error",
  "react/no-danger": "error",
  "react/jsx-no-target-blank": "error",
  "react/no-children-prop": "error",
  "react/void-dom-elements-no-children": "error",
  "react/set-state-in-effect": "error",
  "react/no-deriving-state-in-effects": "error"
}
```

**React maintainability** — the rules that keep agent-written components readable:

```jsonc
{
  "react/no-multi-comp": "error",
  "react/jsx-max-depth": ["error", { "max": 5 }],
  "react/jsx-no-useless-fragment": "error",
  "react/self-closing-comp": "error",
  "react/jsx-curly-brace-presence": ["error", { "props": "never", "children": "never" }],
  "react/jsx-pascal-case": "error",
  "react/function-component-definition": ["error", { "namedComponents": "function-declaration" }],
  "react/hook-use-state": "error",
  "react/button-has-type": "error"
}
```

`react/no-multi-comp` and `jsx-max-depth` are the pair that stops the 600-line file holding five components and eight levels of nesting. `no-array-index-key` is the one that gets argued about — it is right nearly always, and the exceptions are static lists that never reorder; keep it at `"error"` and use a scoped disable comment where it genuinely doesn't apply.

**Accessibility** — enable the `jsx-a11y` plugin and take the correctness set at `"error"`:

```jsonc
{
  "jsx-a11y/alt-text": "error",
  "jsx-a11y/anchor-has-content": "error",
  "jsx-a11y/anchor-is-valid": "error",
  "jsx-a11y/aria-props": "error",
  "jsx-a11y/aria-role": "error",
  "jsx-a11y/aria-unsupported-elements": "error",
  "jsx-a11y/click-events-have-key-events": "error",
  "jsx-a11y/heading-has-content": "error",
  "jsx-a11y/html-has-lang": "error",
  "jsx-a11y/iframe-has-title": "error",
  "jsx-a11y/img-redundant-alt": "error",
  "jsx-a11y/interactive-supports-focus": "error",
  "jsx-a11y/label-has-associated-control": "error",
  "jsx-a11y/no-autofocus": "error",
  "jsx-a11y/no-redundant-roles": "error",
  "jsx-a11y/no-static-element-interactions": "error",
  "jsx-a11y/role-has-required-aria-props": "error",
  "jsx-a11y/role-supports-aria-props": "error",
  "jsx-a11y/tabindex-no-positive": "error"
}
```

If the app uses a component library that wraps DOM elements, map them so the rules see through the wrapper:

```jsonc
{ "settings": { "jsx-a11y": { "components": { "Link": "a", "Button": "button", "Image": "img" } } } }
```

Accessibility is one of the areas an agent will not fix on its own, because a missing label breaks nothing it can observe. That is exactly why it belongs in the linter.

**Performance** — `react-perf` catches props that get a fresh identity on every render:

```jsonc
{
  "react-perf/jsx-no-new-object-as-prop": "error",
  "react-perf/jsx-no-new-array-as-prop": "error",
  "react-perf/jsx-no-new-function-as-prop": "error",
  "react-perf/jsx-no-jsx-as-prop": "error"
}
```

Offer these rather than assuming them — on a codebase using the React Compiler, they are largely redundant and can be noisy. Ask whether the compiler is on.

### Tailwind

Only when Tailwind v4 is detected. `oxlint-tailwindcss` reads the project's real design system — `@theme` tokens, shadcn variables, plugins — which is what makes it deterministic across machines.

`settings.tailwindcss.entryPoint` is **required**: point it at the CSS file containing `@import "tailwindcss"`. Misconfiguration surfaces as a single `designSystemUnavailable` diagnostic rather than silently disabling the rules — if you see that in the prove step, the path is wrong.

```jsonc
{
  "jsPlugins": ["oxlint-tailwindcss"],
  "settings": { "tailwindcss": { "entryPoint": "src/styles.css" } },
  "rules": {
    "tailwindcss/no-hardcoded-colors": "error",
    "tailwindcss/prefer-theme-tokens": "error",
    "tailwindcss/prefer-scale-token": "error",
    "tailwindcss/no-arbitrary-value": "error",
    "tailwindcss/no-unnecessary-arbitrary-value": "error",
    "tailwindcss/no-unknown-classes": "error",
    "tailwindcss/no-conflicting-classes": "error",
    "tailwindcss/no-deprecated-classes": "error",
    "tailwindcss/no-duplicate-classes": "error",
    "tailwindcss/no-contradicting-variants": "error",
    "tailwindcss/no-dark-without-light": "error",
    "tailwindcss/no-unnecessary-whitespace": "error",
    "tailwindcss/enforce-canonical": "error",
    "tailwindcss/enforce-shorthand": "error",
    "tailwindcss/enforce-sort-order": "error",
    "tailwindcss/consistent-variant-order": "error",
    "tailwindcss/max-class-count": ["warn", { "max": 25 }]
  }
}
```

The four **restriction** rules — `no-hardcoded-colors`, `prefer-theme-tokens`, `prefer-scale-token`, `no-arbitrary-value` — are the ones to defend hardest. Without them an agent writes `bg-[#3b82f6] p-[13px]` every time it can't immediately find the right token, and the design system quietly stops being the source of truth. They are also the most likely to produce a large finding count on an existing codebase; count them in the prove step and let the user decide between migrating and scoping to new code.

`max-class-count` is the one genuine `"warn"` here, on the same reasoning as `complexity` — a budget, not a defect.

`enforce-sort-order` produces the same output as `oxfmt` and `prettier-plugin-tailwindcss`. Point the formatter at the same `entryPoint` or the two will fight on every save.

Monorepos map globs to CSS entry points, with a `"**"` fallback last:

```jsonc
{ "settings": { "tailwindcss": { "entryPoint": [
  { "files": "packages/ui/**", "use": "packages/ui/src/styles.css" },
  { "files": "**", "use": "src/global.css" }
]}}}
```

### i18n literals

Only when an i18n library is detected, or the user says the app is going multi-language. `@rrazvan.dev/oxlint-plugin-i18n-literal` flags user-visible copy that skipped the translation function.

```jsonc
{
  "jsPlugins": [{ "name": "i18n-literal", "specifier": "@rrazvan.dev/oxlint-plugin-i18n-literal" }],
  "settings": { "i18n-literal": { "presets": ["react"] } },
  "rules": {
    "i18n-literal/no-literal-string": "error",
    "i18n-literal/no-literal-jsx-attribute": "error",
    "i18n-literal/no-literal-template": "error"
  }
}
```

Each literal is claimed by exactly one of the three rules, so enabling all three doesn't double-report. Add `recharts` to `presets` if charts are in use — naming any preset **replaces** the `["react"]` default, so list every one you want.

This is the plugin most likely to need tuning on a real codebase. Extend `ignoredComponents` for `<Trans>`-style wrappers, `ignoredAttributes` for test ids and tracking labels, and `ignorePatterns` for translation keys passed around as data. Do that tuning in the prove step against the actual finding list — extend the defaults, never `replaceX` them, which discards the built-in coverage of ARIA attributes, URLs, hex colours, and identifiers.

## Standards

What the linter can't express, and what goes in the conventions doc.

**Components.** Colocate state, styles, and helpers next to where they're used. Never define a `renderThing()` function inside a component — extract a component. Cap the props a component takes; past four or five, split it or compose with `children`. Wrap third-party components in a local one so a swap later is a one-file change.

**State, in four categories** — the categorisation is the useful part, because "put it in the store" is the default an agent reaches for and it is usually wrong:

- **Component state** — `useState` / `useReducer`. Start here, and lift only when something else genuinely needs it.
- **Application state** — global UI concerns: modals, notifications, theme. Zustand, Jotai, or context + hooks.
- **Server cache state** — data from the server. TanStack Query or SWR — **not** the global store. Caching server data in Redux is the single most common state mistake in a React codebase.
- **URL state** — filters, tabs, pagination. It belongs in the address bar, where it survives a refresh and can be shared.
- **Form state** — React Hook Form plus a schema validator (Zod), behind one abstracted `Form` component and one input component per field type.

**API layer.** One configured API client instance, reused everywhere. Each request is declared and exported — types plus schema, a fetcher, and a hook over it — colocated in the feature's `api/` folder, never assembled inline at the call site.

**Errors.** An interceptor on the client for API errors (toast, log out on 401, refresh tokens). Multiple error boundaries placed around sections rather than one at the root, so a failure contains itself. Error tracking wired to something like Sentry, with source maps uploaded.

**Testing.** Weight toward **integration** tests — they exercise the connections between parts, which is where the bugs are. Unit tests for shared components and complex logic; e2e (Playwright) for the critical paths only. Test what the user sees, not internal state, so a refactor doesn't rewrite the suite. MSW for mocking at the network boundary rather than mocking modules — which is also what `anti-slop/no-module-mocking` enforces.

## Framework additions

**Next.js.** Add `nextjs` to `plugins`. Take the whole set at `"error"` — every one of them catches a real Next-specific mistake:

```jsonc
{
  "nextjs/no-html-link-for-pages": "error",
  "nextjs/no-img-element": "error",
  "nextjs/no-sync-scripts": "error",
  "nextjs/no-head-element": "error",
  "nextjs/no-async-client-component": "error",
  "nextjs/no-document-import-in-page": "error",
  "nextjs/no-head-import-in-document": "error",
  "nextjs/no-script-component-in-head": "error",
  "nextjs/no-styled-jsx-in-document": "error",
  "nextjs/no-duplicate-head": "error",
  "nextjs/no-page-custom-font": "error",
  "nextjs/no-css-tags": "error",
  "nextjs/no-before-interactive-script-outside-document": "error",
  "nextjs/no-assign-module-variable": "error",
  "nextjs/no-title-in-document-head": "error",
  "nextjs/no-typos": "error",
  "nextjs/no-unwanted-polyfillio": "error",
  "nextjs/inline-script-id": "error",
  "nextjs/google-font-display": "error",
  "nextjs/google-font-preconnect": "error",
  "nextjs/next-script-for-ga": "error"
}
```

The structure needs one adjustment: Next owns `app/` (or `pages/`) for routing, so that directory **is** the app layer — `src/app/` holds routes, and `src/features/` stays exactly as above. Route files, `layout.tsx`, `page.tsx`, and `middleware.ts` all require default exports, so they need an `import/no-default-export` override. Enumerate react.doctor's `nextjs-*` family (the `next` preset's contents) — it covers faults oxlint's native `nextjs` plugin doesn't reach.

**React Native and Expo.** Skip `jsx-a11y` (DOM-specific) and skip Tailwind unless NativeWind is in use — with NativeWind, the Tailwind rules apply and `entryPoint` points at its CSS. Enumerate react.doctor's `rn-*` family (the `react-native` preset's contents). The bulletproof structure carries over unchanged; `app/` is Expo Router's route directory and takes the same default-export override as Next.

**TanStack Start / Router.** Route files are default exports — same override. Enumerate react.doctor's `tanstack-start-*` family, and `query-*` if TanStack Query is a dependency — the `tanstack-start` and `tanstack-query` presets respectively.

**Remix / React Router v7.** Route modules export `loader`, `action`, and a default component — the default-export override covers the routes directory.
