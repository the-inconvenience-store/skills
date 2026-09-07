# Encode Lessons in Structure

**Apply when:** the same correction, failure mode, or instruction has appeared more than once.

Put the lesson at the earliest reliable enforcement point: a type that excludes the invalid state, a parser at the boundary, a lint rule, an executable check, generated metadata, a task, or a repeatable script. Prefer a failing mechanism over prose that asks every future agent to remember.

Use agent instructions only when the rule is judgment-dependent and cannot be represented structurally. Keep one source of truth and point to it rather than repeating the meaning across skills, standards, and repository guidance.

The encoding must itself be proved: demonstrate the bad case failing and the valid case passing.
