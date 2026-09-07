# Outcome-Oriented Execution

**Apply when:** a plan introduces intermediate architecture, compatibility code, or migration states.

Every intermediate state must do at least one useful job:

- Deliver observable value.
- Preserve a required migration or deployment invariant.
- Establish verified scaffold that later work immediately consumes.

Delete states that exist only to make the plan appear smooth. Do not preserve an old and new path without an explicit reason and removal condition.

Tracer bullets are valid intermediate states because each is independently useful and verifiable. Expand-contract is valid when an atomic cutover cannot stay safe; its contract step and deletion ticket must already be part of the sequence.
