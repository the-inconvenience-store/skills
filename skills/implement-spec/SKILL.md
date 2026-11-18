---
name: implement-spec
description: Implement the result of /to-spec and /to-tickets in code.
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/bootstrap-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

Start every subagent with a fresh context window.

Delegate independently executable, substantive slices whose useful parallelism repays coordination cost. Keep small coupled edits inline; multiple files alone do not establish useful parallelism. Run eligible subagents in the background where possible.

## Steps

1. Read the spec and tickets to understand the task graph.

2. Call the Skill tool with `engineering-principles` unless its selection policy is already available in context. Apply that policy against the spec, task graph, and repository. Save relevant constraints, their rationale, and reference pointers as markdown notes outside the repo, accessible by future subagents.

3. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets: relevant codebase files or external documentation. It saves its markdown notes in the same notes directory. This lets **implementer subagents** focus on implementation rather than exploration.

4. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first ticket lands on it (a branch with no commits ahead of main can't open one), marked as closing the spec and tickets.

5. Use **implementer subagents** for tickets that meet the delegation threshold, each in its own worktree on its own branch. Handle small coupled tickets inline on the integration branch, applying the same implementation, checking, commit, and ticket-resolution requirements. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - before editing production code, reads the relevant principles notes, loads `engineering-principles` if its selection policy is not already in context, and applies that policy to its own ticket's decision surface, reusing supplied constraints and loading references only for missing detail or additional principles;
   - calls the Skill tool with `tdd` and builds the ticket one red-green vertical slice at a time, running typechecking and the narrow test files regularly;
   - commits as it works, using Conventional Commit-style messages, with `closes #ISSUENUM` in the footer of the commit that completes the ticket when the issue tracker is GitHub;
   - merges the integration branch tip into its own branch, runs the full test suite green, and commits before reporting done.

6. Once an **implementer subagent** completes, merge its work to the integration branch. Use a **merger subagent** only when the integration work meets the delegation threshold.

7. If this changes the **frontier** of available tickets, start newly unblocked work, delegating tickets that meet the threshold and handling small coupled tickets inline.

8. Once every ticket has merged, run typechecking and the full test suite on the integration branch, then call the Skill tool with `code-review`. Name the commit the integration branch was cut from as the fixed point: the review reads `git diff <fixed-point>...HEAD`, so commit anything outstanding first. Give every accepted Standards and Spec finding to one integration owner: fix small coupled findings inline, or use a single **implementer subagent** when the fixes meet the delegation threshold. Fix the findings, rerun affected checks, and commit; merge delegated work as in step 6. The review runs once: after the fix, rerun the focused checks for the fixed findings and move on.

9. Call the Skill tool with `verify` on the integration branch. Prove the spec's changed behavior through its real user or consumer surface. `INCONCLUSIVE` is not completion: report the exact gap instead of substituting tests or compilation for the missing observation.

10. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work.

11. Clean up all **implementer subagent** worktrees.

12. Report the integration branch (and PR, if any), the automated checks, the verification verdict, the observed result, and any principle that drove a non-obvious decision.
