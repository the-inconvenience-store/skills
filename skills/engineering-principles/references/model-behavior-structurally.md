# Model Behavior Structurally

**Apply when:** the same state rule or shape assumption appears in several conditionals, files, or callers.

First settle the project's domain language. When that language is changing, call the Skill tool with `domain-modeling`. Then encode state, transitions, variants, and invariants so invalid combinations are difficult or impossible to represent.

The structure should make valid transitions clear and invalid states difficult to represent. Callers consume it; they do not reimplement its rules.

Do not create a framework for one local branch. The repeated knowledge, not the number of lines, is the signal that a model is missing.
