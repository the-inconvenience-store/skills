# Protect the Signal

**Apply when:** a test, type check, lint rule, assertion, threshold, or other check fails and the tempting fix changes the check rather than the code.

A check is evidence only while it can fail. Fix the code that violates it. Skipping or deleting a test, loosening an assertion, special-casing the test input, adding a suppression or cast, or raising a threshold turns the check green without making the claim true.

Change a check only when the check itself is wrong: it asserts obsolete behavior, pins an implementation detail, or observes nondeterministically. State that reason in the diff or report, and keep or replace the coverage it provided.

The same holds for delegated work. When inspecting another agent's diff, treat every weakened check as a claim to verify.
