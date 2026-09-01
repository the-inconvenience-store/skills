# Bulletproof React standards

Use this reference only after the React branch asks whether the user wants these standards. [Bulletproof React](https://github.com/alan2207/bulletproof-react/tree/master) is an opinionated guide, not a template or framework; adopt the principles that fit and keep the resulting project internally consistent.

## The choice

Offer one explicit decision:

> **Adopt Bulletproof React-inspired application standards?** Recommended for an application expected to grow across features or contributors. This adds feature modules, one-way import boundaries, direct imports, explicit state and API boundaries, and a user-facing testing posture. It is optional for a small app and usually inappropriate for a component library.

Let the user accept the package, select parts, or decline it. For an existing application, include the number and kind of current violations and separate enforcement from migration; moving files requires its own approval.

## Structure and dependencies

Adapt the [source structure](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-structure.md) to the detected framework:

```text
src/
  app/          application composition, routes, and providers
  assets/       shared static assets
  components/   shared components
  config/       application configuration and typed environment access
  features/     feature-owned modules
  hooks/        shared hooks
  lib/          configured third-party libraries
  stores/       genuinely global client state
  testing/      shared test utilities and handlers
  types/        shared types
  utils/        shared utilities
```

A feature owns only the folders it needs: `api/`, `assets/`, `components/`, `hooks/`, `stores/`, `types/`, and `utils/`. Avoid empty furniture.

Dependencies flow `shared → features → app`:

- shared modules import no feature or app code;
- a feature imports shared code but not another feature;
- the app layer composes features and shared code;
- imports target the defining file directly rather than a barrel.

Translate `app/` to the framework's route layer—Next.js App Router, Expo Router, Remix, React Router, or TanStack Start—and preserve required route exports. Derive lint zones from the actual feature list; do not paste example paths.

## Project standards

The [project standards](https://github.com/alan2207/bulletproof-react/blob/master/docs/project-standards.md) complement this skill's lint, format, and hook proposal:

- TypeScript for application code when the stack permits it.
- One absolute source alias, commonly `@/*`, configured consistently in compiler, bundler, tests, and editor tooling.
- A single filename/folder convention, such as kebab-case, only when the user accepts it.
- Formatter and linter automation through the approved commands and hooks.

Enforce accepted import, alias, barrel, and naming rules mechanically. Document only the standards configuration cannot express.

## Components and styling

Keep feature-specific components with their feature and promote a component to `src/components` only when it is genuinely shared. Colocate a component's local helpers, state, styles, and tests. Wrap third-party UI primitives when the application needs a stable local interface or shared behavior.

Use the detected styling system and design tokens; Bulletproof React's library choices are examples rather than requirements. Read the current [components and styling guidance](https://github.com/alan2207/bulletproof-react/blob/master/docs/components-and-styling.md) when this part of the proposal needs more detail.

## State boundaries

Use the [state categories](https://github.com/alan2207/bulletproof-react/blob/master/docs/state-management.md) to stop every value drifting into a global store:

- **Component state:** start local; lift only when another component needs it.
- **Application state:** cross-cutting client concerns such as notifications, theme, and global modals.
- **Server cache state:** remote data owned by a query/cache layer rather than copied into a client store.
- **URL state:** shareable navigation state such as filters, tabs, and pagination.
- **Form state:** owned by the form boundary and its validation layer.

Choose libraries from the detected stack and user preferences; the boundary matters more than the brand.

## API, tests, errors, and security

- **API:** use one configured client per backend and define request declarations with request/response types or schemas, a fetcher, and the consuming query/mutation hook. See the [API layer guidance](https://github.com/alan2207/bulletproof-react/blob/master/docs/api-layer.md).
- **Tests:** emphasize integration tests across feature connections, unit tests for shared components and complex logic, and end-to-end tests for critical paths. Assert what the user observes and mock at the network boundary where practical. See the [testing guidance](https://github.com/alan2207/bulletproof-react/blob/master/docs/testing.md).
- **Errors:** centralize routine API error translation, place error boundaries around recoverable application regions, and connect production error reporting when the project needs it. Consult the [error-handling guidance](https://github.com/alan2207/bulletproof-react/blob/master/docs/error-handling.md).
- **Security:** keep secrets and authorization on trusted servers, expose only explicitly public environment values, validate untrusted data, and include dependency and secret scanning when accepted. Consult the [security guidance](https://github.com/alan2207/bulletproof-react/blob/master/docs/security.md).

## Proposal and completion

The proposal must list each selected standard, its enforcement mechanism, and any migration work. A selected standard is complete only when new code has a clear destination, prohibited dependencies fail mechanically where possible, framework exceptions pass, and remaining prose is short enough to serve as a real navigation aid.
