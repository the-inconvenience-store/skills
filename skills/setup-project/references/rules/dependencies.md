# Dependency rules

Use this branch for libraries the project writes against regularly: state, data fetching, routing, schemas, forms, databases, testing, logging, and observability. The rule is **search before authoring; propose before installing**.

## Search

1. Read the library's current official guidance for common mistakes, performance traps, and unsafe defaults.
2. Search the chosen linter's built-ins and already-installed plugins.
3. Check the library's own maintained plugin.
4. Author a project rule only when no maintained rule exists and the anti-pattern is syntactically precise.

An existing maintained rule wins. Verify that each lead below is still maintained, compatible, and exported by the installed version.

## Leads

| Detected library | Look first |
| --- | --- |
| TanStack Query | `react-doctor/query-*`; then `@tanstack/eslint-plugin-query` |
| TanStack Start or Router | `react-doctor/tanstack-start-*`; then TanStack's maintained plugin |
| React Router or Remix | `react-doctor/react-router-*` |
| Zustand, Jotai, Redux, Valtio, MobX | Corresponding react.doctor family |
| Framer Motion | `react-doctor/motion-*` |
| Zod v4 | `react-doctor/zod-v4-*` for migration mistakes; inspect schema-hygiene gaps separately |
| Firebase or Supabase | Corresponding react.doctor authorization/security family |
| Drizzle | Maintained Drizzle ESLint rules, especially update/delete without `where` |
| Testing Library | `eslint-plugin-testing-library` |
| Storybook | `eslint-plugin-storybook` |
| Effect | [anti-slop](https://github.com/dmmulroy/anti-slop)'s opt-in Effect rules |
| Tailwind or i18n | The conditional groups in [react.md](./react.md) |

For Go, check bundled linters before adding tooling:

| Detected library | Bundled linter candidates |
| --- | --- |
| testify | `testifylint` |
| Ginkgo or Gomega | `ginkgolinter` |
| zerolog, zap, logr, klog | `zerologlint`, `loggercheck` |
| `log/slog` | `sloglint` |
| OpenTelemetry | `spancheck` |
| protobuf | `protogetter`, `musttag` |
| `database/sql`, sqlx, pgx | `sqlclosecheck`, `rowserrcheck`, `unqueryvet` |
| Prometheus | `promlinter` |
| ArangoDB or ClickHouse | `arangolint`, `clickhouselint` |
| Locale-sensitive or portability-heavy code | `gosmopolitan` when its policy fits |

## Project rules

Prefer configuration over authored code:

- banned import: `depguard`;
- banned identifier or call: `forbidigo` or a maintained syntax rule;
- banned module/version: `gomodguard_v2`;
- required tag or alias: `musttag` or `importas`;
- Go AST pattern: a narrow ruleguard rule before a compiled plugin.

Propose an authored rule with four facts: its name and severity, the exact bad syntax, the accepted replacement, and the upstream guidance that justifies it. Include a failing and passing example. Install it only after approval, test both examples, and report a declined proposal as a known gap.
