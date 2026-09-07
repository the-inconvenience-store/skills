# Sequence Verifiable Units

**Apply when:** work spans several slices, commits, tickets, or migration batches.

Break the work into the smallest units that each end in a meaningful check. Order prerequisite scaffold and risky unknowns before dependent behavior. Verify one unit before starting the next so a failure has a narrow search space.

For product work, prefer tracer bullets that deliver a complete public path through the necessary layers. For migrations that cannot be atomic, keep each expand-contract batch buildable and reserve a final unit for deleting the old path.

The sequence should tell the engineering story: baseline or failing reproduction, enabling structure, behavior, cleanup, and final real-surface proof.
