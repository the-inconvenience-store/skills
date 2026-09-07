# Subtract Before You Add

**Apply when:** extending or rewriting code that already carries dead, duplicated, superseded, or transitional paths.

Remove what the new behavior makes obsolete before building on top. Delete dead adapters, redundant validation, stale branches, abandoned scaffolding, and tests that protect only obsolete implementation details.

Prove each deletion is safe through references and executable behavior. Do not combine unrelated cleanup with the requested change merely because it is nearby.

The result should expose the real remaining design. Adding to a simplified base is safer than teaching new code to coexist with weight that no longer has an owner.
