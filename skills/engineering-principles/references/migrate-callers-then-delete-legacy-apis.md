# Migrate Callers Then Delete Legacy APIs

**Apply when:** an internal API is replaced while callers still exist.

Prefer one verifiable wave: inventory every caller, migrate them, update tests to the new contract, prove no caller remains, and delete the old API and compatibility tests.

Use expand-contract only when an atomic cutover cannot remain buildable, deployable, or operationally safe. The expansion, migration batches, and final deletion are one bounded sequence. Create the deletion ticket up front and block it on every migration batch so compatibility cannot become the accidental steady state.

Preserve compatibility for external consumers only when the product or versioning contract requires it. Name that contract and its removal or support policy explicitly.
