# Fix Root Causes

**Apply when:** a bug, failure, or performance regression is being diagnosed.

Reproduce the exact reported symptom before changing production code. Build a tight, red-capable feedback loop, minimise the case, form falsifiable hypotheses, and collect runtime evidence until one mechanism survives.

Fix that mechanism at the point where the violated invariant is owned. A guard that only suppresses the exception, retry that only lowers frequency, or special case for the observed input is not a root-cause fix.

When this principle is applied outside an active diagnosis workflow, call the Skill tool with `diagnosing-bugs` for the full procedure. After the fix, call the Skill tool with `verification` against the original public path.
