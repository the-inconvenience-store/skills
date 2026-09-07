# Maintain project verification

Keep existing driving instructions and feature maps aligned with the application. The unit of coverage is each mapped user-facing feature.

## Outcomes

End with exactly one outcome:

- **clean** — every mapped feature received source and live coverage; nothing changed.
- **changed** — verified corrections were made only within the verification artifact or helpers it owns.
- **blocked** — complete coverage or a safe correction was impossible; name the blocker.

## 1. Locate and index

Read `docs/agents/verification/README.md` and locate every surface. Check that its surface and feature indexes match the directories: no missing, duplicate, stale, or unindexed entries.

If no artifact exists, route to Create. If several unrelated verification conventions exist, identify which is authoritative from repository pointers; ask only when the repository cannot resolve the ownership conflict.

**Done when:** every surface and feature index entry is accounted for and the authoritative artifact is known.

## 2. Compare every feature with source

For several independent feature files, dispatch one read-only subagent per feature in parallel. For a small map, inspect directly. Each inspection returns:

- The feature's source entry points.
- How the public path currently works.
- Likely documentation or harness drift with citations.
- One concise live-driving recipe.

Require one result per feature. Sweep recent user-facing source changes for concrete capabilities missing from the map; a file name alone is not evidence of a missing feature.

**Done when:** every mapped feature has a source-backed result and every proposed missing feature has a concrete public entry point.

## 3. Reconcile the live pass

Spot-check every claimed drift. Merge overlapping recipes into as few known application states as practical. Shared UI, server, or device instances are driven serially; source inspection may be parallel.

**Done when:** the live-pass plan covers every feature and names each shared application state.

## 4. Drive every mapped feature

A live pass is required even when source appears clean. Follow each surface's Launch, Doctor, Drive, Evidence, Cleanup, and Isolation rules.

Maintain these invariants throughout:

1. Never drive an instance that has not passed Doctor since its last surprising result.
2. Evidence captured so far survives every reset and cleanup.
3. Failed-drive residue is removed before retrying.
4. Every mapped feature is driven at least once or marked unreachable with the concrete prerequisite and attempted route.

A broken Doctor or driver caused by verification drift may be fixed and retried once. Re-run every changed harness path live before accepting it.

**Done when:** every mapped feature has live evidence or a concrete unreachable prerequisite and attempted route.

## 5. Classify mismatches

- Wrong or missing user-facing description is **documentation drift**; correct it.
- Working behavior the documented harness cannot drive is a **harness gap**; correct the owned instructions or helper.
- Application behavior that is actually broken is a **product regression**; report it and do not change the documentation to describe the bug as intended.

Edit only `docs/agents/verification/` and helper scripts explicitly owned by it. Product code is outside this branch.

**Done when:** every mismatch is classified and every proposed edit stays inside the verification ownership boundary.

## 6. Finish

Run final cleanup after the last re-proof and confirm evidence remains. For `changed`, report every correction and its live proof. For `clean`, report feature and surface coverage. For `blocked`, report completed coverage plus the exact remainder.

**Done when:** final cleanup is confirmed, evidence remains accessible, and exactly one outcome reports the complete coverage result.
