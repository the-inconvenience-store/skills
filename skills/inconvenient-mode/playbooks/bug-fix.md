# Bug fix

1. Call the Skill tool with `diagnosing-bugs` and isolate the mechanism using the reported failure, a matching reproduction where needed, and the smallest experiment that distinguishes competing causes. A diagnosis-only request ends with the supported cause and any evidence gap.
2. Fix the cause when a fix is in scope. If a useful test-first regression probe fits the project, call the Skill tool with `tdd` and use its seam agreement before adding the test. Keep the probe focused on the public failure.
3. Call the Skill tool with `verify` for the changed behavior. Drive the original trigger on the same surface and observe the corrected result. Report what failed before, what changed, and what now holds. If the original trigger cannot be driven, name the limit of the evidence.
