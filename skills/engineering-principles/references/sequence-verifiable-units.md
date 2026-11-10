# Sequence Verifiable Units

**Apply when:** work spans several slices, commits, tickets, or migration batches, or validation must be scoped, scheduled, or rerun.

Break the work into the smallest units that each end in a meaningful check. Order prerequisite scaffold and risky unknowns before dependent behavior. Verify and integrate one unit before starting dependent work so a failure has a narrow search space; finished work on a side branch is not progress. Make the change easy, then make the easy change: land behavior-preserving restructuring as its own unit, proved unchanged by existing checks, before the behavior change that needs it.

Within a unit, use focused checks to answer implementation questions. Run the required final validation once the relevant implementation and generated artifacts stabilize; a focused result does not replace broader coverage. Schedule independent checks together when their resource and mutable-state requirements permit it. Repository instructions own the required commands and evidence; run a separate build only for a required build path not already exercised by those checks.

A successful check stands while its scope, relevant source, dependencies, generated artifacts, configuration, toolchain, and execution environment remain unchanged. Record the command and scope; rerun checks whose results a later change could affect. Reuse normal caches where permitted by repository policy, and require fresh execution when external state, nondeterminism, or an explicit evidence contract demands it. A cached result cannot substitute for required fresh race, integration, or live evidence.

For product work, prefer tracer bullets that deliver a complete public path through the necessary layers. For migrations that cannot be atomic, keep each expand-contract batch buildable and reserve a final unit for deleting the old path.

The sequence should tell the engineering story: baseline or failing reproduction, enabling structure, behavior, cleanup, and final real-surface proof.
