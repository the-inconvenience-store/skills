# Session review

## 1. Gather evidence

Inspect the selected session and its relevant child activity. For older sessions, discover records through native history, documented storage, or AgentTrace. For omp sessions, read [omp.md](omp.md). When AgentTrace is installed and recorded evidence is needed, use its [session-specific recipes](agenttrace.md#extract-tool-steps-and-inspect-a-specific-session); do not expand to a historical inventory. Name inaccessible evidence. Missing timing data does not block non-performance findings.

**Done when:** the session, relevant child activity, and evidence limits are explicit.

## 2. Find candidates

Scan these categories against concrete events. Keep only supported findings; a category with no evidence contributes nothing.

- **Navigation and access:** If the agent repeatedly searched, or the user supplied a fact the agent could have fetched, propose a pointer from a file it already reads or the narrower access that would have helped.
- **Checks and standards:** Read the repo's existing checks and CI wiring before proposing a new check. An existing but unwired or broken check is the finding. Use deterministic checks for mechanical rules and prefer an existing linter rule or plugin to a custom rule. Where Semgrep is already used, a suitable rule should name the safe alternative and have both match and non-match cases. If the finding needs Semgrep and the repo does not run it, or if the repo lacks a quality baseline, recommend `/guardrails`. Put reviewer judgment in the repo's coding standards, not in always-loaded steering.
- **Steering:** Find no-op instructions, duplicate guidance, and global rules that belong in a narrower reference, a reviewer standard, or a check. Keep navigation pointers where agents already look.
- **Tool economy:** If searches, checks, calls, polling, approvals, retries, dependencies, context pressure, or instruction costs consumed effort, use only the relevant parts of [shared diagnosis](diagnosis.md). A session review needs no full ledger or historical survey. Benchmark only to support a claimed measured improvement.

Apply either lens below when its trigger matches. Both can apply to one session; neither is a separate mode. Consolidate proposals with the same cause and fix.

**Done when:** every category has been considered and each retained candidate has concrete evidence and a distinct proposed change.

### Correct: a mistake recurred

Use when at least two distinct occurrences show the same underlying failure, not when one event appears twice in a transcript. Cite both occurrences. Use only evidence within the selected scope, including any past example the user supplied. If recurrence cannot be established, assess the finding normally without calling it recurring.

Propose the earliest reliable prevention: remove the wrong path through architecture, make invalid states unrepresentable with types, enforce the rule with deterministic lint or CI, then use a behavior test if the earlier options cannot guard the contract. Reserve prose for judgment. Explain why an earlier option would not work or would cost more than it is worth. Propose a validation that catches a real past mistake and accepts a valid case. For structural prevention, show why the old path becomes unavailable and how the supported path still works. Do not implement the change or add a standing rule table.

### Reflect: a skill failed to steer the work

Use when the record shows a missed activation, misleading instructions, a command or prerequisite the agent had to rediscover, or a skipped proof step that the skill should have guided. Read the implicated skill and relevant references. First check whether the harness could load it and whether the existing guidance was reached. If it already gives clear, reachable guidance, do not propose repeating it. Drop one-offs and details that will go stale.

For a missed activation, propose a narrower or clearer description only if the skill is meant to activate implicitly. For bad execution, identify the exact instruction or reference to change. For a failure a check can prevent, propose enforcement instead of more skill prose. Name the maintained source file and the behavior that should change next time, with a replay prompt or other check that separates old and new behavior. A managed plugin cache is evidence, never an edit destination; name a maintained source or propose an explicit local override. Leave all edits for a separate request.

See [credits.md](credits.md) for the upstream lenses and what was deliberately left out.
