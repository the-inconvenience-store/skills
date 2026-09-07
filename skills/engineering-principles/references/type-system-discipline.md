# Type System Discipline

**Apply when:** a signature or model permits invalid domain states, semantic primitives are interchangeable, or external data enters as trusted.

Make illegal states unrepresentable where the language permits it. Use distinct variants for distinct states, semantic types for identifiers and units that must not mix, and exhaustive handling for closed sets.

Parse external values at a boundary before treating them as domain data. Derive types from the authoritative schema when one exists. Prefer narrowing and construction functions over casts, unchecked assertions, optional fields that are always required in practice, or escape hatches such as `any`.

Do not add type machinery that makes ordinary valid states harder to express. The type should remove caller knowledge, not move runtime confusion into generic syntax.
