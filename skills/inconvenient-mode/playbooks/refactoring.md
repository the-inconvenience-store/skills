# Refactoring

1. Pin the behavior to preserve. Reuse an existing characterization check when it covers the proposed seam; otherwise agree on the smallest useful comparison before moving code. Use an observed baseline for user-facing behavior when the existing evidence does not establish it.
2. Name the simpler target structure and the reader burden it removes. Remove dead paths before adding structure. Migrate callers with the seam, and keep new behavior or bug fixes outside the refactor.
3. Run the contract check on the final result. When meaningful equivalence needs a live check, call the Skill tool with `verify` on the affected surface. Report the contract, the proof, and the structure that got simpler.
