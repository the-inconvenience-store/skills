# React rules

Layer this catalogue on the JavaScript/TypeScript baseline. Present relevant groups for approval and verify every selected rule against the installed plugin: react.doctor's CLI, ESLint plugin, and oxlint plugin do not necessarily expose the same rules.

Choose one source for overlapping hooks, React, and accessibility rules. Running react.doctor ports alongside native `react`, `react-perf`, and `jsx-a11y` copies produces duplicate diagnostics. Whole-project rules such as dead exports and dependency cycles belong in a CLI/CI scan, not a single-file plugin entry.

Default to error except explicit budgets. Framework and library families apply only when their dependency is present.

## react.doctor baseline

All unqualified rule IDs in this section use the `react-doctor/` prefix.

### Effects and lifecycle

`no-fetch-in-effect`, `no-async-effect-callback`, `effect-needs-cleanup`, `effect-listener-cleanup-mismatch`, `effect-observer-needs-disconnect`, `effect-raf-loop-needs-cancel`, `no-effect-chain`, `no-self-updating-effect`, `no-set-state-after-await-in-effect`, `no-effect-event-in-deps`, `no-mirror-prop-effect`, `no-prop-callback-in-effect`, `no-stale-timer-ref`, `debounce-no-cleanup`, `prefer-use-effect-event`.

Prefix each with `react-doctor/`. This is the highest-priority React group.

### Derived state and updates

- Derived state: `no-derived-state`, `no-derived-state-effect`, `no-adjust-state-on-prop-change`, `no-reset-all-state-on-prop-change`, `no-event-trigger-state`, `no-initialize-state`.
- Updates: `no-direct-state-mutation`, `no-impure-state-updater`, `no-side-effect-in-state-updater-function`, `no-cascading-set-state`, `no-chain-state-updates`, `no-boolean-toggle-without-functional-update`, `no-mutating-reducer-state`, `no-mutating-array-method-on-prop-or-hook-result`, `no-mutate-then-set-or-return-same-reference`, `no-set-state-in-render`, `no-render-in-render`, `no-pass-live-state-to-parent`, `no-uncontrolled-input`, `no-controlled-input-value-without-state-update`.

### Render purity

`no-create-context-in-render`, `no-create-store-in-render`, `no-create-ref-in-function-component`, `no-create-object-url-in-render`, `no-create-object-url-without-revoke`, `no-ref-current-in-render`, `no-nondeterministic-id-value-in-render-body`, `no-random-key`, `no-impure-call-at-module-scope`, `no-unguarded-browser-global-in-render-or-hook-init`, `no-unguarded-browser-global-at-module-scope`, `no-hydration-branch-on-browser-global`, `no-match-media-in-state-initializer`, `no-nested-component-definition`, `no-inline-hoc-on-component`, `no-call-component-as-function`.

### Async and data safety

`no-fetch-response-used-without-status-check`, `no-collapse-request-error-to-empty-state`, `no-floating-then-in-jsx-handler`, `no-promise-then-side-effect-in-effect-without-catch`, `no-async-event-handler-without-reentry-guard`, `no-loading-flag-reset-outside-finally`, `no-unsafe-json-parse`, `no-unguarded-throwing-parse-call`, `no-unguarded-numeric-input-parse`, `no-object-keys-values-entries-on-maybe-undefined`, `no-array-find-result-member-access-without-guard`, `no-non-null-assertion-on-maybe-undefined-result`, `no-arithmetic-on-optional-chained-operand`, `no-nullish-coalescing-arithmetic-precedence`, `no-collapsed-literal-or-chain-as-value`, `no-object-or-array-coerced-to-string-in-template-literal`.

### Maintainability and rendering performance

- Maintainability: `no-giant-component` at warn; `no-many-boolean-props`, `no-generic-handler-names`, `no-polymorphic-children`, `no-render-prop-children`, `no-barrel-import`, `no-full-lodash-import`, `no-moment` at error.
- Rendering: `rerender-dependencies`, `rerender-functional-setstate`, `rerender-lazy-state-init`, `rerender-lazy-ref-init`, `rerender-memo-before-early-return`, `no-whole-object-dep-with-member-reads`, `no-mutable-in-deps`, `hooks-no-nan-in-deps`, `no-usememo-simple-expression`, `no-inline-prop-on-memo-component`, `no-unthrottled-scroll-mutation`, `no-locale-format-in-render`, `no-unbounded-animation-frame-loop`.

Check whether React Compiler is enabled before proposing rendering rules. Prefer the installed compiler-specific rule, such as `react-compiler-no-manual-memoization`, when manual memoization rules become redundant.

### Client-side security

`no-secrets-in-client-code`, `public-env-secret-name`, `auth-token-in-web-storage`, `dangerous-html-sink`, `no-eval`, `window-open-without-noopener`, `postmessage-origin-risk`, `untrusted-redirect-following`, `no-dynamic-import-path`, `unsafe-json-in-html`, `no-unescaped-dynamic-string-in-regexp`.

Enable `firebase-*`, `supabase-*`, `nosql-injection-risk`, and `raw-sql-injection-risk` only for the matching backend. Whole-project secret and configuration scanning requires the react.doctor CLI or a dedicated scanner.

### Accessibility additions

`html-no-nested-interactive`, `html-label-has-single-control`, `html-no-nested-form`, `html-no-invalid-table-nesting`, `form-control-requires-name`, `radio-input-missing-name`, `fieldset-requires-legend`, `dialog-has-accessible-name`, `details-requires-summary`, `data-table-requires-accessible-name`, `no-skipped-heading-level`, `no-multiple-main-landmarks`, `no-focusable-content-in-aria-hidden`, `no-invisible-focus-control`, `no-outline-none`, `no-uninformative-aria-label`, `no-placeholder-only-field`, `role-button-requires-complete-keyboard-activation`, `no-disabled-zoom`, `require-reduced-motion`.

Some releases expose `require-reduced-motion` only through the CLI. Move unavailable rules to an optional CLI pass rather than leaving inert config.

### Creative-direction rules — explicit opt-in

Present this family as one separate decision because it encodes visual direction rather than correctness:

`no-default-purple-page-gradient`, `no-generic-purple-blue-icon-gradient`, `no-decorative-blur-orb`, `no-decorative-radial-spotlight`, `no-decorative-grid-background`, `no-decorative-pulse`, `no-repeated-glass-surfaces`, `no-repeated-section-shells`, `no-uniform-feature-card-grid`, `no-empty-card-shell`, `no-nested-card-surface`, `no-emoji-heading-decoration`, `no-fake-browser-chrome`, `design-no-vague-button-label`, `design-no-em-dash-in-jsx-text`, `design-no-three-period-ellipsis`, `no-generic-marketing-copy`, `no-placeholder-persona-copy`, `no-repeated-kicker-labels`, `no-tiny-text`, `no-low-contrast-inline-style`, `no-flat-page-type-scale`, `no-monotonous-page-spacing`, `no-transition-all`, `no-z-index-9999`.

## Native React alternative

When native rules own the overlap, recommend:

Unqualified IDs in each bullet inherit that bullet's `react/`, `react-perf/`, or `jsx-a11y/` namespace.

- Correctness: `react/rules-of-hooks`, `exhaustive-deps`, `jsx-key`, `no-array-index-key`, `no-unstable-nested-components`, `jsx-no-constructed-context-values`, `no-danger`, `jsx-no-target-blank`, `no-children-prop`, `void-dom-elements-no-children`, `set-state-in-effect`, `no-deriving-state-in-effects`.
- Maintainability: `react/no-multi-comp`, `jsx-max-depth` at `5`, `jsx-no-useless-fragment`, `self-closing-comp`, `jsx-curly-brace-presence`, `jsx-pascal-case`, `function-component-definition`, `hook-use-state`, `button-has-type`.
- Performance, only without compiler coverage: `react-perf/jsx-no-new-object-as-prop`, `jsx-no-new-array-as-prop`, `jsx-no-new-function-as-prop`, `jsx-no-jsx-as-prop`.

For native accessibility, enable:

`jsx-a11y/alt-text`, `anchor-has-content`, `anchor-is-valid`, `aria-props`, `aria-role`, `aria-unsupported-elements`, `click-events-have-key-events`, `heading-has-content`, `html-has-lang`, `iframe-has-title`, `img-redundant-alt`, `interactive-supports-focus`, `label-has-associated-control`, `no-autofocus`, `no-redundant-roles`, `no-static-element-interactions`, `role-has-required-aria-props`, `role-supports-aria-props`, `tabindex-no-positive`.

Map design-system components to their underlying DOM roles so these rules can see through wrappers.

## Tailwind

When the compatible Tailwind plugin can read the project's real design system, recommend:

All unqualified IDs in this section use the `tailwindcss/` prefix.

- Restrictions: `tailwindcss/no-hardcoded-colors`, `prefer-theme-tokens`, `prefer-scale-token`, `no-arbitrary-value`.
- Correctness: `no-unnecessary-arbitrary-value`, `no-unknown-classes`, `no-conflicting-classes`, `no-deprecated-classes`, `no-duplicate-classes`, `no-contradicting-variants`, `no-dark-without-light`, `no-unnecessary-whitespace`.
- Canonical output: `enforce-canonical`, `enforce-shorthand`, `enforce-sort-order`, `consistent-variant-order`.
- Budget: `max-class-count` at warn with default `25`.

The restriction group is the priority and the likely migration hotspot. Point linter and formatter at the same stylesheet entry point and demonstrate that they converge.

## Internationalized copy

Only when an i18n library is detected or planned, offer [`@rrazvan.dev/oxlint-plugin-i18n-literal`](https://www.npmjs.com/package/@rrazvan.dev/oxlint-plugin-i18n-literal) with `i18n-literal/no-literal-string`, `i18n-literal/no-literal-jsx-attribute`, and `i18n-literal/no-literal-template`. Tune ignored components, attributes, and data keys against the project; preserve the plugin's built-in ignores.

## Framework and library families

Enable only detected families and enumerate their current exported rules:

- Next.js: `nextjs-*` from react.doctor plus the native `nextjs` correctness set. Native recommendations are `no-html-link-for-pages`, `no-img-element`, `no-sync-scripts`, `no-head-element`, `no-async-client-component`, `no-document-import-in-page`, `no-head-import-in-document`, `no-script-component-in-head`, `no-styled-jsx-in-document`, `no-duplicate-head`, `no-page-custom-font`, `no-css-tags`, `no-before-interactive-script-outside-document`, `no-assign-module-variable`, `no-title-in-document-head`, `no-typos`, `no-unwanted-polyfillio`, `inline-script-id`, `google-font-display`, `google-font-preconnect`, `next-script-for-ga`.
- React Native or Expo: `rn-*`; omit DOM accessibility rules and use Tailwind rules only with a compatible NativeWind setup.
- TanStack Start and Query: `tanstack-start-*`, `query-*`.
- React Router or Remix: `react-router-*`.
- Preact: `preact-*`; Framer Motion: `motion-*`; Zustand/Jotai/Redux/Valtio/MobX: their named families.
- R3F/three.js, Remotion, Ink, Zod v4, styled-components, shadcn, and react-markdown: only their detected named families.
- Server Components: prioritize `server-auth-actions`, `server-no-mutable-module-state`, `server-sequential-independent-await`, `server-fetch-without-revalidate` when exported.

Never enable an `all` preset across unrelated frameworks.

## Whole-project CI checks

Offer `unused-file`, `unused-export`, `unused-type`, `unused-dependency`, `unused-dev-dependency`, `circular-dependency`, `duplicate-jsx-subtree`, and high-complexity React checks through the react.doctor CLI or another project scanner when the user wants them. Verify they actually execute; do not place CLI-only metadata in single-file linter configuration.
