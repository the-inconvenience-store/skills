---
name: show-me-your-work
description: Keep an append-only decision trail for long or unattended work.
disable-model-invocation: true
---

# Show Me Your Work

Keep one **decision trail** while work already authorized by the user is underway. This skill does not start or broaden the underlying task.

1. **Choose the log.** Use the user's named path or an existing log for this effort. Otherwise use a scratch path outside the repo and tell the user where it is. Keep it local by default. Do not commit or publish it unless requested. The coordinating agent is the sole writer; workers return evidence pointers.
2. **Append decisions as they happen.** Use the bundled helper with one row per consequential choice, pivot, blocker, or verification checkpoint. Cite the evidence rather than pasting output. Use the observed result, including inconclusive or not run. Omit routine actions and redact secrets or private material.

   ```sh
   bash <skill-dir>/scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>
   ```

   Pass each value as one quoted argument. The helper adds a UTC timestamp and keeps each cell on one line. When a fresh session takes over an existing log, read its tail and append a `start` row that identifies the new session and the prior context. Correct a bad row by appending a superseding row, not rewriting history.
3. **Hand it back.** Spot-check consequential rows against their evidence. Add a correction or a missing decision if needed. Return the path and flag any unverified results or decisions still needing the user. Stop when the reader can trace the important choices without reading the whole transcript.

Adapted from [pstack show-me-your-work](https://github.com/cursor/plugins/blob/b1fbf4b60ac6813b4583ccc356850dafcf492665/pstack/skills/show-me-your-work/SKILL.md). See [LICENSE](LICENSE).
