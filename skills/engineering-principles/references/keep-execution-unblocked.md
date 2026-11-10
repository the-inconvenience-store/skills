# Keep Execution Unblocked

**Apply when:** a reversible execution choice is about to become a human checkpoint, or a background command, agent, or investigation is pending.

Facts are the agent's job. Inspect the repository, run the experiment, or use the available tool instead of asking the user to supply observable information. Proceed on reversible implementation details when the accepted behavior and repository precedent make the choice clear, then present the result for asynchronous correction.

Decisions are the user's job when they change product direction, scope, experience, risk acceptance, or another genuine preference. Irreversible external actions also require confirmation.

A running command, agent, or investigation blocks only work that depends on its result. Continue independent implementation, documentation, or review work before waiting at a completion barrier. Preserve prerequisite ordering and serialize work that shares mutable state.

Keep one owner responsible for each background job's completion and evidence. Use completion notifications when available rather than duplicate watchers or status polling. Before declaring the task complete, collect the actual terminal results of required jobs; successful submission is not successful execution.
