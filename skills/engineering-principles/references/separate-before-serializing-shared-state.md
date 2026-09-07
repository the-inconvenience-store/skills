# Separate Before Serializing Shared State

**Apply when:** concurrent actors may write the same file, branch, key, process, database row, or in-memory object.

First remove unnecessary sharing. Give workers separate worktrees, branches, output paths, ports, profiles, fixtures, partitions, or immutable inputs. Aggregate completed artifacts through one explicit owner.

Serialize only when one shared writer is a real invariant of the domain. Put that ownership in the structure rather than relying on timing, politeness, retries, or an undocumented lock order.

Before parallelizing, name every shared mutable resource and how it is isolated or owned. If that cannot be stated, the workstreams are not independent yet.
