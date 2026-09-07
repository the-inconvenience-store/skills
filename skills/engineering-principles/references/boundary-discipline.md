# Boundary Discipline

**Apply when:** external input, framework state, transport errors, or validation logic is entering business behavior.

Parse and validate once where untrusted data crosses into the system: CLI arguments, configuration, network requests, storage records, environment variables, and third-party APIs. Convert it into trusted domain types there.

Inside the boundary, keep business functions direct and trust the established types and invariants. Convert internal results back to framework or transport shapes at the exit boundary.

Do not scatter defensive checks through every layer. Keep a guard inside only when the invariant can genuinely be broken there by concurrent state or an independently trusted subsystem.
