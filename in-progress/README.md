# In Progress

Skills that are still being developed. They're not ready to ship — expect rough edges, breaking changes, and abandoned experiments. They're excluded from the plugin and the top-level README until they graduate to a stable bucket.

- **[loop-me](./loop-me/SKILL.md)** — Grill yourself into implementable workflow specs over multiple sessions, using the current directory as a stateful workspace. User-invoked.
- **[claude-handoff](./claude-handoff/SKILL.md)** — Hand the current conversation off to a fresh background agent that picks up the work immediately, seeded with a handoff summary via `claude --bg`. User-invoked.
- **[implement-spec](./implement-spec/SKILL.md)** — Drive a spec and its tickets to a single PR, reading the tickets as a task graph so implementer subagents run concurrently across the ready frontier. User-invoked.
- **[retro](./retro/SKILL.md)** — Run a retrospective on a finished coding session, ranking improvements to the agent's environment rather than its code: navigation, automated checks, coding standards, steering-file bloat, tool economy, and information access. User-invoked.
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)** — Wire dependency-cruiser into a TypeScript repo so each package is a deep module — implementation hidden in subfolders, reachable only through its entry-point files, tests exercising it through those. User-invoked.
