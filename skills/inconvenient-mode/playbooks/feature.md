# Feature

1. Name the public behavior to add or preserve, the data shape that owns it, and the narrowest check that would catch a regression. Use the accepted spec and project conventions as evidence; resolve any missing product decision before editing.
2. For test-first behavior changes, call the Skill tool with `tdd` and use its seam agreement before writing tests. If a hard failure must be explained before the work can proceed, use [Bug fix](bug-fix.md) to establish the cause before editing.
3. Run the applicable repository checks. When the change affects behavior on a running surface or public library interface, call the Skill tool with `verify`. Reuse an already observed result unless a later change invalidated it. Report any proof gap rather than treating a proxy as a pass.
