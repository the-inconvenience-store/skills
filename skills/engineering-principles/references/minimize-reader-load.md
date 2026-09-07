# Minimize Reader Load

**Apply when:** answering one code question requires following many wrappers, aliases, mutable facts, or pass-through calls.

Count what a maintainer must hold in their head between the question and its answer. Collapse one-caller wrappers, shorten message chains, colocate state with the behavior that owns it, and shrink mutable scope.

Prefer a deep module that hides complexity behind a narrow interface. When the interface or seam itself needs redesign, call the Skill tool with `codebase-design`.

Do not flatten meaningful domain distinctions or hide operationally important behavior. The aim is locality: fewer places to inspect for one change, not fewer named concepts at any cost.
