# In Progress

Skills that are still being developed. They're not ready to ship — expect rough edges, breaking changes, and abandoned experiments. They're excluded from the plugin and the top-level README until they graduate to a stable bucket.

- **[loop-me](./loop-me/SKILL.md)** — Grill yourself into implementable workflow specs over multiple sessions, using the current directory as a stateful workspace. User-invoked.
- **[wizard](./wizard/SKILL.md)** — Generate an interactive bash wizard that walks a human through a manual procedure (setup, a one-off migration, a state transition) — opening URLs, capturing values, writing `.env` and GitHub Actions secrets. User-invoked.
- **[claude-handoff](./claude-handoff/SKILL.md)** — Hand the current conversation off to a fresh background agent that picks up the work immediately, seeded with a handoff summary via `claude --bg`. User-invoked.
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)** — Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point files, tests exercising it through those. User-invoked.
- **[to-questionnaire](./to-questionnaire/SKILL.md)** — Turn a decision you can't fully answer into a Markdown questionnaire for someone else to fill in async, or over a meeting. It grills you about the send (who it's for, what you need back), not the subject. User-invoked.
- **[batch-grill-me](./batch-grill-me/SKILL.md)** — Relentless interview that walks the design tree in rounds instead of one question at a time — each round asks the whole frontier of decisions whose prerequisites are already settled, then recomputes from your answers. User-invoked.
