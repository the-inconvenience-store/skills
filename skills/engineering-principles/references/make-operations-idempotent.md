# Make Operations Idempotent

**Apply when:** a command, job, webhook, migration, setup step, or lifecycle operation may retry or resume after partial progress.

Define the intended end state, then make each run converge on it. Repeating a completed operation should preserve the same externally observable result rather than duplicate records, compound mutations, or fail because prior work exists.

Use stable identities, upserts, compare-and-set transitions, checkpoints, or existence checks at the owning boundary as the domain requires. Idempotency keys and locks are tools, not the definition.

Prove first run, repeated run, and recovery after an interrupted intermediate state. Do not erase a legitimate repeated user action merely because the implementation cannot distinguish it from a retry.
