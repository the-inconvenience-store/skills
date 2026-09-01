# Dependency-specific rules

Every library has documented anti-patterns, and a rule that catches one is worth far more than a note in `CLAUDE.md` asking an agent not to do it. This is where a lint setup stops being generic and starts knowing something about *this* project.

The discipline in one line: **search before you author, and propose before you install.**

## The loop

Run this once per notable dependency. A notable dependency is one an agent will write code against every day — a state library, a data-fetching library, an ORM, a schema validator, a form library, a router, a test library. Not `clsx`.

### 1. List the dependencies

From step 1's detection, plus a direct question: *"Anything you're about to adopt that I should set rules up for now?"* Rules are cheapest to add before the first hundred call sites exist.

### 2. Read what the library says goes wrong

The library's own docs, not your memory of them. Look for the pages titled "common mistakes", "gotchas", "performance", "important defaults", or a migration guide's "don't do this" section. Those pages are where a rule candidate comes from, and they are also the citation that justifies it to the user.

### 3. Search for an existing plugin

**On a React project, check react.doctor first.** It is by far the largest source of library-specific rules in the ecosystem, and its coverage is easy to miss because the rules live under one `react-doctor/*` namespace rather than one plugin per library. Its families already cover TanStack Query and Start, React Router / Remix, Zustand, Jotai, Redux, Valtio, MobX, Framer Motion, React Native and Expo, Zod v4, styled-components, shadcn, react-markdown, Preact, R3F / three.js, Remotion, and Ink — plus Firebase and Supabase authorization checks. A rule already in a plugin you've installed costs one config line. See the families table in [react.md](./react.md), and enumerate against the installed plugin rather than the docs site.

**TypeScript / JavaScript** otherwise, in order:

- `eslint-plugin-<library>` and `@<scope>/eslint-plugin-<library>` on npm. Oxlint's JS plugin API is ESLint v9-compatible, so an ESLint plugin generally works unmodified via `jsPlugins`.
- `oxlint-plugin-<library>` — a smaller field, but native.
- The library's own repo. Several ship a plugin in-tree that isn't obviously named.

**Go**: check golangci-lint's own catalogue first — it already bundles library-specific linters that are easy to miss (`testifylint`, `ginkgolinter`, `zerologlint`, `loggercheck`, `spancheck`, `protogetter`, `sqlclosecheck`, `rowserrcheck`, `arangolint`, `clickhouselint`, `gosmopolitan`, `promlinter`, `musttag`). A linter that's already in the binary needs one line in `enable`, and that beats everything below.

An existing plugin beats a rule you write, always. It has tests, it has users, and it tracks the library's own changes.

### 4. Author only when nothing exists

And only when the anti-pattern is **syntactically detectable**. "Don't over-fetch" is not a lint rule. "`useStore()` called with no selector argument" is.

**In Go, reach for config before code.** Most of what would be a custom rule elsewhere is already expressible in golangci-lint's existing linters, and a config entry needs no plugin build, no version pinning, and no maintenance:

- **A banned import** → `depguard`, with a `desc` that cites the reason.
- **A banned function or identifier** → `forbidigo`, which takes regex patterns and an optional `pkg` qualifier to disambiguate a package name.
- **A banned module** → `gomodguard_v2`, which also handles version constraints and recommended replacements.
- **A required struct tag** → `musttag`. **A required import alias** → `importas`.
- **A structural pattern** → `gocritic`'s [ruleguard](https://github.com/quasilyte/go-ruleguard) rules, written declaratively as AST patterns rather than as a compiled plugin.

Writing an actual golangci-lint plugin is a last resort — it is a compiled Go plugin or a custom binary build, both of which tie the rule to a specific linter and toolchain version. Exhaust the list above first.

### 5. Propose, then install

Never install an authored rule silently. Every proposal is one block:

> **`project/no-unselected-store`** — `error`
>
> Catches: `const state = useStore()` — subscribing to the whole store, so the component re-renders on every unrelated change.
>
> ```ts
> const bears = useStore();              // flagged
> const bears = useStore((s) => s.bears); // fine
> ```
>
> Why: <https://zustand.docs.pmnd.rs/guides/prevent-rerenders-with-use-shallow>

The user takes it or leaves it. A declined proposal goes in the report as a known gap, not into the config.

## Leads

Plugins that exist for libraries this skill commonly encounters. **Verify each one before installing** — check it's still published, still maintained, and compatible with the installed oxlint version. This is a list of places to look, not a manifest.

| Library | Look for |
| --- | --- |
| TanStack Query | `react-doctor/query-*` first (9 rules, `tanstack-query` preset); `@tanstack/eslint-plugin-query` otherwise |
| TanStack Start / Router | `react-doctor/tanstack-start-*` (15 rules, `tanstack-start` preset); `@tanstack/eslint-plugin-router` |
| React Router / Remix | `react-doctor/react-router-*` — 38 rules on loaders, middleware, sessions, route config |
| Zustand / Jotai / Redux / Valtio / MobX | `react-doctor/zustand-*`, `jotai-*`, `redux-*`, `valtio-*`, `mobx-*` |
| Framer Motion | `react-doctor/motion-*` — 12 rules |
| Zod v4 | `react-doctor/zod-v4-*` — deprecated error and schema APIs |
| Firebase / Supabase | `react-doctor/firebase-*`, `supabase-*` — missing row-level security, client-owned authorization fields |
| Drizzle | `eslint-plugin-drizzle` — the delete/update-without-`where` rules, which catch a whole-table wipe |
| Testing Library | `eslint-plugin-testing-library` — the query and `await` rules |
| Storybook | `eslint-plugin-storybook` |
| Effect | `anti-slop-effect`, the opt-in group in [anti-slop](https://github.com/dmmulroy/anti-slop) |
| Tailwind | `oxlint-tailwindcss` — see [react.md](./react.md) |
| i18next / next-intl | `@rrazvan.dev/oxlint-plugin-i18n-literal` — see [react.md](./react.md) |

Go libraries are mostly covered by linters already inside golangci-lint — the table's Go row is really "check `enable`, not npm":

| Library | Bundled linter |
| --- | --- |
| testify | `testifylint` |
| Ginkgo / Gomega | `ginkgolinter` |
| zerolog / zap / logr / klog | `zerologlint`, `loggercheck` |
| `log/slog` | `sloglint` |
| OpenTelemetry | `spancheck` |
| protobuf | `protogetter`, `musttag` |
| `database/sql`, sqlx, pgx | `sqlclosecheck`, `rowserrcheck`, `unqueryvet` |
| Prometheus | `promlinter` |

Libraries with no plugin worth knowing about, and the rule candidates their docs justify — each still needs the loop run properly, these are just the ones that come up most:

- **Zustand** — on a React project `react-doctor/zustand-*` already covers whole-store destructure, fresh selector results, mutating state, and `get()` during initialization. Elsewhere: selecting the whole store instead of a slice; creating a store inside a component.
- **Zod** — `z.any()` / `z.unknown()` in a schema, which discards the reason the schema exists; `.parse()` on untrusted input where `.safeParse()` belongs. (`react-doctor/zod-v4-*` covers only the v3→v4 deprecations, not schema hygiene.)
- **React Hook Form** — a controlled input wired without `register` or `Controller`.
- **Prisma** — a query in a loop where a single `in` query would do.
- **Go, any ORM or query builder** — a query inside a `for` loop; `context.Background()` in a request path where the request's context should flow through. `forbidigo` with a `pkg` qualifier catches the second one.

## Authoring

Vendor custom rules in `tools/oxlint/project-rules/`, add that path to `ignorePatterns`, and register with the alias form so the namespace is short and unmistakable:

```jsonc
{
  "jsPlugins": [{ "name": "project", "specifier": "./tools/oxlint/project-rules/index.ts" }],
  "rules": { "project/no-unselected-store": "error" }
}
```

The API is ESLint v9's — `meta` plus a `create(context)` returning visitor methods. Read <https://oxc.rs/docs/guide/usage/linter/js-plugins.md> for what's implemented, and <https://eslint.org/docs/latest/extend/custom-rules> for the API itself. A whole rule is usually this short:

```ts
// tools/oxlint/project-rules/rules/no-unselected-store.ts
export default {
  meta: {
    type: "problem",
    docs: { description: "Require a selector when subscribing to the store" },
    messages: {
      unselected: "Pass a selector: useStore((s) => s.field). Calling useStore() subscribes to every change.",
    },
  },
  create(context) {
    return {
      CallExpression(node) {
        if (node.callee.type === "Identifier" && node.callee.name === "useStore" && node.arguments.length === 0) {
          context.report({ node, messageId: "unselected" });
        }
      },
    };
  },
};
```

Three things make an authored rule worth having, and all three are cheap:

- **A message that says what to do instead.** "Avoid X" leaves an agent guessing; "Pass a selector: `useStore((s) => s.field)`" gets it fixed on the first try. The message is the rule's real interface — write it as the instruction it needs to be.
- **A narrow trigger.** A custom rule that fires on anything ambiguous is a rule the team disables. Prefer missing a case to inventing one.
- **Proof it fires.** Step 6 covers this: write the violation, watch it fail with that rule's name, revert, watch it pass. A custom rule that never fires is the failure mode here, and it is completely silent without that check.
