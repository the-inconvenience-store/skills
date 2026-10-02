# Treat Observable Behavior as Contract

**Apply when:** a change alters output, ordering, error shape or text, timing, defaults, identifiers, or a file or wire format that anything outside the changed module can observe.

With enough consumers, every observable behavior is depended on by somebody, whether or not it was promised. Before changing, inventory what becomes visibly different at the public surface, including behavior the documentation never mentions.

Classify each difference as intended, incidental, or a break. Keep incidental behavior stable when changing it buys nothing. When a break is intended, name it in the PR, changelog, or migration note, and move internal callers with Migrate Callers Then Delete Legacy APIs.

Do not freeze implementation detail that nothing outside the module can reach. Behavior visible only to the module's own tests is not a contract; rewrite those tests against the public behavior.
