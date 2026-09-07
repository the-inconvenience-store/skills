# Laziness Protocol

**Apply when:** sizing a diff or considering another abstraction, wrapper, option, guard, signal, or layer.

Prefer deletion and the smallest change that fully satisfies the accepted behavior. Start by asking what can disappear, what the language or framework already provides, and whether an existing deep module should own the behavior.

A smaller diff is not automatically better. Do not omit required behavior, collapse distinct domain concepts, or hide complexity in callers to reduce line count. The target is less system, not less visible code.

A new abstraction earns its place only when it hides real complexity for more than one present caller or establishes an agreed seam. Otherwise keep the direct code.
