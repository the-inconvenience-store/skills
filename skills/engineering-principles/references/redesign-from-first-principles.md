# Redesign from First Principles

**Apply when:** a new requirement repeatedly fights the current shape.

Redesign as if the requirement had been a day-one assumption. Reconsider ownership, data shape, interfaces, and lifecycle instead of attaching another conditional or adapter at the point where the symptom appears.

Preserve accepted behavior, not accidental structure. Ground the redesign in current callers, recorded decisions, and runtime evidence. If the design is costly to reverse and lacks precedent, apply Exhaust the Design Space before committing.

One awkward edge case is not evidence that the architecture is wrong. Redesign when the same workaround or escape hatch appears across independent parts of the implementation.
