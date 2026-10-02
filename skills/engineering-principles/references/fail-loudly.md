# Fail Loudly

**Apply when:** code catches an error, calls a remote or slow dependency, retries, falls back to a default, or receives malformed input.

Surface a failure where it happens, with the context needed to diagnose it. A catch block earns its place only by handling a named failure mode: recovering, translating at a boundary, or adding context before rethrowing. Reject malformed input with a precise error rather than guessing what the sender meant; tolerated malformation becomes an undocumented contract.

Bound every failure path: a timeout on each remote call, a finite retry budget with backoff for transient errors only, and a limit on queued and concurrent work.

A fallback or degraded mode is valid when the product requires it. Make it observable through a log, metric, or visible state so degradation is never mistaken for success.
