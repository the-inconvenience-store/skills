---
name: status
description: Give a brief progress report on the current work, including completion estimate and blockers.
disable-model-invocation: true
---

Report the status of the current task using the conversation and available task tracking. Reply with exactly five short bullets, one sentence each:

- **Progress:** Approximate percentage complete against the full requested scope, labelled as an estimate.
- **Done:** Main outcomes completed so far, distinguishing implemented work from verified results.
- **Now:** What is currently in progress, or say nothing is active.
- **Next / remaining:** Immediate next step first, then the other outstanding work.
- **Blockers:** Unresolved blockers and what or who is needed to resolve them; say "None" if there are none.

Ground the report in known state. If context is insufficient for a meaningful percentage, say "Unknown" and name the missing scope rather than inventing precision. Reserve 100% for completed and verified work. Keep this a snapshot: respond without starting new work or changing task state.
