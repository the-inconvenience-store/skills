# Prove It Works

**Apply when:** work is about to be called complete.

Identify the observable claim, then check the real artifact directly. Run the public path, read the actual value, inspect the produced file or diff, and verify the full input-to-output chain. Compilation, tests, cached representations, and agent reports are supporting signals rather than substitutes for the claimed result.

Choose the least expensive evidence sufficient for the observable claim and repository requirements. Broader checks earn their cost by covering additional relevant failure modes.

For user-facing application behavior, call the Skill tool with `verify`. Its `VERIFIED`, `NOT VERIFIED`, and `INCONCLUSIVE` verdicts preserve the evidence boundary.

Inspect delegated changes and validate their integration yourself. Reuse recorded checks whose scope and inputs remain valid; repeat them when integration changes those inputs or the evidence is insufficient. Apply Sequence Verifiable Units to check validity and required fresh evidence. A worker's completion report alone is not proof. When a check passes too easily, test the observation method before concluding the system is correct.
