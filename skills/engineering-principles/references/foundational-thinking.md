# Foundational Thinking

**Apply when:** choosing core data structures, shared types, or scaffold that every later slice needs.

Name the data shape before writing the logic. Trace its dominant reads, writes, invariants, ownership, and concurrent actors; choose a structure that makes those operations obvious and invalid states difficult.

Build scaffold first only when every subsequent slice benefits from it: a stable shared type, a tight feedback loop, or a required verification route. Subtract obsolete structure before adding foundations.

Keep the foundation narrow. Three explicit statements are cheaper than a speculative framework. Each foundational change should land as a coherent, verifiable unit that later work can rely on.
