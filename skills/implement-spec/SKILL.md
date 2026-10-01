---
name: implement-spec
description: Implement the result of /to-spec and /to-tickets in code.
disable-model-invocation: true
---

You have been provided a spec. This spec should have tickets associated with it, describing how to implement the spec.

The issue tracker should have been provided to you. If not, tell the user to run `/setup-inconvenient-skills`.

The goal is the entire spec implemented on a single **integration branch**, with every ticket resolved the way the issue tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking relationships between them. This means there is always a **frontier** of tickets which are ready to be grabbed.

Communication to and from subagents should be sparse. Communicate primarily through **context pointers**: to the spec, tickets, research notes, and previous commits. Don't duplicate information already available via pointers.

**Implementer subagents** should be run in the background where possible for maximum concurrency.

## Steps

1. Read the spec and tickets to understand the task graph.

2. Call the Skill tool with `engineering-principles`. Scan its full trigger index against the spec, the task graph, and the repository; read every matched leaf and turn it into a concrete constraint. User-named principles are mandatory additions, not a prerequisite for selection. Save the constraints as a markdown notes file in a directory outside the repo, accessible by all future subagents.

3. (optional) Use an **exploration subagent** to conduct any exploration required by the tickets — relevant codebase files or external documentation. It saves its markdown notes in the same notes directory. This lets **implementer subagents** focus on implementation rather than exploration.

4. Create the integration branch. If the issue tracker closes work through PRs, or the user asks for one, open a draft PR after the first merge in step 6 — a branch with no commits ahead of main can't open one — marked as closing the spec and tickets.

5. Use **implementer subagents** to implement each ticket, each in its own worktree on its own branch. Each implementer subagent:
   - confirms its worktree is based on the integration branch before starting, and resets onto it if not;
   - before editing production code, reads the principles notes, then calls the Skill tool with `engineering-principles` and scans its trigger index against its own ticket, adding a constraint for every matched leaf the notes miss;
   - calls the Skill tool with `tdd` and builds the ticket one red-green vertical slice at a time, running typechecking and the narrow test files regularly;
   - commits as it works, using Conventional Commit-style messages, with `closes #ISSUENUM` in the footer of the commit that completes the ticket when the issue tracker is GitHub;
   - merges the integration branch tip into its own branch, runs the full test suite green, and commits before reporting done.

6. Once an **implementer subagent** completes, merge its work to the integration branch with a **merger subagent**.

7. If this changes the **frontier** of available tickets, kick off more **implementer subagents** to work on the new tickets. This allows for maximum concurrency.

8. Once every ticket has merged, run typechecking and the full test suite on the integration branch, then call the Skill tool with `code-review`. Name the commit the integration branch was cut from as the fixed point: the review reads `git diff <fixed-point>...HEAD`, so commit anything outstanding first. Send every accepted Standards and Spec finding to a single **implementer subagent**, which fixes them, reruns the affected checks, and commits; merge its work as in step 6. The review runs once: after the fix, rerun the focused checks for the fixed findings and move on.

9. Call the Skill tool with `verification` on the integration branch. Prove the spec's changed behavior through its real user or consumer surface. `INCONCLUSIVE` is not completion: report the exact gap instead of substituting tests or compilation for the missing observation.

10. If a draft PR exists, mark it ready for review. Otherwise, resolve each ticket the way the issue tracker closes work.

11. Clean up all **implementer subagent** worktrees.

12. Report the integration branch (and PR, if any), the automated checks, the verification verdict, the observed result, and any principle that drove a non-obvious decision.
