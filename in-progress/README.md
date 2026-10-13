# In Progress

Skills that are still being developed. They're not ready to ship, so expect rough edges, breaking changes, and abandoned experiments. They're excluded from the plugin and the top-level README until they graduate to a stable bucket.

- **[loop-me](./loop-me/SKILL.md)**: Grill yourself into implementable workflow specs over multiple sessions, using the current directory as a stateful workspace. User-invoked.
- **[chief-of-staff](./chief-of-staff/SKILL.md)**: Pursue a long-running goal in one session by co-ordinating subagents and recurring schedules, communicating through context pointers and tending the agents' environment. User-invoked.
- **[claude-handoff](./claude-handoff/SKILL.md)**: Hand the current conversation off to a fresh background agent that picks up the work immediately, seeded with a handoff summary via `claude --bg`. User-invoked.
- **[implement-spec-swarm](./implement-spec-swarm/SKILL.md)**: `implement-spec` with a `swarm` mode: herdr-launched coding agents, each with its own role, CLI, and model, implement the ticket graph in worktrees while the invoking session orchestrates. Merges back into `implement-spec` on promotion. User-invoked.
- **[setup-ts-deep-modules](./setup-ts-deep-modules/SKILL.md)**: Wire dependency-cruiser into a TypeScript repo so each package is a deep module: implementation hidden in subfolders, reachable only through its entry-point files, tests exercising it through those. User-invoked.
