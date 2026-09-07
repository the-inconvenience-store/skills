# Project verification format

The generated artifact is portable agent-facing documentation under `docs/agents/verification/`, not a harness-specific installed skill.

## Layout

Use one directory per independently launched surface:

```text
docs/agents/verification/
├── README.md
├── <surface>/
│   ├── README.md
│   └── features/
│       ├── README.md
│       └── <feature>.md
└── <another-surface>/
    └── ...
```

The root `README.md` indexes every surface and states when to choose each. A repository with one surface still uses the same layout; one stable shape is cheaper than a special case.

Helpers follow the repository's existing convention for scripts or test drivers. The surface README points at them. Do not create a new script hierarchy when the repository already has one.

## Surface README

Every `<surface>/README.md` contains these H2 sections:

- **Surface** — what a user or consumer touches and which application or package owns it.
- **Launch** — exact command, required environment, readiness signal, and teardown handle.
- **Doctor** — one read-only check that says whether this instance is safe and useful to drive.
- **Drive** — the repository's real harness, commands, selectors, prompts, routes, or API entry points.
- **Evidence** — what proves actions and results, where captures go, and how secrets are redacted.
- **Cleanup** — how to stop only what the run started and remove scratch state without deleting evidence.
- **Isolation** — whether concurrent instances are safe and how their ports, profiles, data, or sessions differ.
- **Feature map** — a link to `features/README.md` and the rule that every user-facing feature belongs there.

Write exact repository instructions, not generic examples. A command must be runnable as written. A selector must exist in the current application.

## Feature map

`features/README.md` indexes every feature file with a one-line user outcome. Each feature file contains:

- **User outcome** — the capability and result in the user's language.
- **How to reach it** — the path from a clean, known state.
- **How to drive it** — exact interactions using the surface harness.
- **Proof** — observable output and durable side effects that must hold.
- **Gotchas** — prerequisites, permissions, destructive edges, or state that must be reset.

Features are user capabilities, not routes, files, components, or implementation layers. Split a feature only when its paths can be reached and proved independently.

## Evidence invariants

- Capture the action and resulting state, not only the final screen.
- Check promised side effects through a public or operationally valid read path.
- Keep evidence outside cleanup-owned scratch state.
- Never capture credentials, tokens, private customer data, or authentication headers.
- A dry-run or test mode is trustworthy only after observing what it does and does not change.
