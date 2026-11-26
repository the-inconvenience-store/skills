# Fix Root Causes

**Apply when:** a bug, failure, or performance regression is being diagnosed, or performance is being optimized.

Reproduce the exact reported symptom before changing production code. Build a tight, red-capable feedback loop, minimise the case, form falsifiable hypotheses, and collect runtime evidence until one mechanism survives. For performance, profile before changing code, optimize the measured constraint, and re-measure because the constraint moves.

Fix that mechanism at the point where the violated invariant is owned. A guard that only suppresses the exception, retry that only lowers frequency, or special case for the observed input is not a root-cause fix.

**Attack the Premise:** If two attempted fixes based on the same assumption fail the same check, set the failed fixes aside. Write down the shared assumption and run a probe whose result would differ if it were false. Use the observed result to revise or narrow the hypothesis before attempting another fix.

When this principle is applied outside an active diagnosis workflow, call the Skill tool with `diagnosing-bugs` for the full procedure. After the fix, call the Skill tool with `verify` against the original public path.
