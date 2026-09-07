# React

React adds framework-specific checks to the JavaScript/TypeScript proposal. It does not choose the project's architecture.

## Inspect

- Identify the framework and version from installed dependencies and configuration, not from filenames alone.
- Read the existing React, hooks, accessibility, framework, test, and styling configuration.
- Inspect the current directory and import structure before proposing boundaries or naming rules.
- Detect generated routes or components and framework-required default exports before enabling generic restrictions.
- Determine whether this is an application, a component library, or another React package; application architecture guidance does not automatically fit libraries.

## Propose

Before proposing lint changes, read [rules/react.md](./rules/react.md). Verify the selected rules against the installed plugin and present opinionated groups separately.

For a new React application, ask whether the user wants to adopt [Bulletproof React standards](./bulletproof-react.md). Lead with a recommendation based on the expected size and team: adopt them for an application expected to grow; skip them for a small throwaway app or package where feature architecture does not fit. Summarize the package—feature modules, one-way imports, direct imports, state boundaries, an explicit API layer, and user-facing tests—so the user can decide without reading the source first.

For an established application, raise this choice only when the user asked to restructure it or inspection found inconsistent boundaries. State the migration size before recommending adoption. Read `bulletproof-react.md` only when this branch is live.

Offer only rule groups supported by the chosen linter and current compatible plugins:

- hooks and render correctness;
- framework-specific correctness;
- accessibility;
- performance rules with a low false-positive rate for this project;
- styling or design-token rules when the detected styling system can enforce them reliably.

Verify plugin rule names and compatibility against the installed version before writing configuration. Prefer one implementation when native and third-party plugins duplicate the same rule family.

If accepted, include the selected Bulletproof React standards in the proposal and name which are mechanically enforced versus documented. If declined, do not smuggle them in through import, filename, or directory rules.

If Tailwind or another class-based design system is present, make the linter and formatter read the same project configuration or stylesheet entry point. Demonstrate that they converge instead of rewriting each other's output.

## Verify

Exercise a representative React-specific finding, not only a generic TypeScript rule. Also test any framework override or import boundary added by the proposal: one import that should fail and one nearby import that should pass.

Use current official documentation for React, the detected framework, and the selected linter plugins. Catalogue sizes, presets, and standalone-versus-plugin capabilities are volatile and do not belong in this reference.
