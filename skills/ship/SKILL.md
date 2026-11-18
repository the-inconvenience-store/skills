---
name: ship
description: Rebase onto main or master, resolve conflicts, commit and push your work, then open a PR using the pr skill.
disable-model-invocation: true
---

# Ship

Ship the working branch as a **review-ready** pull request. Preserve the intent of both the branch and upstream changes through the rebase.

## 1. Establish the branch and scope

Inspect the branch, working tree, index, remotes, upstream tracking, and existing PR. Identify the work this session owns, including untracked files. Use repository conventions and remote metadata to select the target repository and its `main` or `master` base, and the push remote (which may be a fork). Fetch those remotes; use the fetched base, not a stale local branch. Record the remote working-branch SHA, or its absence, for the push lease.

If on the base branch, create a descriptively named working branch before proceeding. A detached HEAD, an in-progress Git operation, ambiguous ownership, or an unclear target must be resolved before rewriting history.

Rebase requires a clean index and working tree. Temporarily stash the scoped uncommitted work, including its untracked files, recording the exact stash identity. Preserve unrelated staged and unstaged work in place; if it prevents a clean rebase, stop and ask the user to isolate it rather than stashing or committing it implicitly. For mixed-ownership hunks, use selective tooling or pause for clarification.

**Done when:** the working branch, fetched base, push destination, publication state, and owned changes are known, and the worktree is ready for rebase with any saved work recoverable.

## 2. Rebase and resolve conflicts

Rebase the working branch onto the fetched base. For each conflict, read the conflicting changes and their surrounding callers or contracts; reconcile both intents rather than choosing an entire side. During a rebase, Git's ours side is the upstream plus replayed commits, and theirs is the commit being replayed. Stage only resolved paths and continue until the rebase finishes. Skip a commit only when its intended change is already present.

Restore the exact saved stash after the rebase, preserving its staged state. Resolve any restoration conflicts with the same discipline. Keep the saved stash until all its work is restored; drop only that stash after successful recovery. If a conflict requires a product decision that the repository and conversation cannot settle, ask with the concrete conflict and leave all work recoverable.

**Done when:** the rebase has finished, saved work is restored, and every conflict is resolved without losing either side's intended behavior.

## 3. Verify and commit

Run the repository's relevant checks against the rebased result, including checks exercising conflict resolutions. Fix failures caused by this work; report unrelated failures accurately. A failed required check blocks shipping unless the user explicitly accepts it.

Commit all remaining owned changes with the repository's commit conventions and the harness's selective commit tooling when available. Include only this task's files or hunks; preserve unrelated work and existing commits. If everything is already committed, proceed without an empty commit. Honor commit and push hooks; when a hook changes files, include the owned corrections and rerun the affected check.

**Done when:** all intended work is committed and the checks pass, or the user has explicitly accepted the named failures.

## 4. Push and open the PR

Push the working branch to its intended remote, setting upstream tracking when needed. Use a normal push for a new branch or a fast-forward update. If rebasing rewrote a published branch, use `--force-with-lease=refs/heads/<branch>:<recorded-sha>` against the SHA recorded before the rebase. A rejected lease means someone updated the remote: fetch and reconcile their work before trying again. Never use an unconditional force push.

Call the Skill tool with "pr" to write the PR body from the actual branch diff and observed verification evidence. Use the hosting platform's authenticated CLI or API to open the PR against the selected `main` or `master` base. The pr skill owns the body format; this skill owns publishing it. If an open PR already exists for this head and base, update it rather than creating a duplicate.

Confirm the PR's head, base, and published commit match the intended branch. Return its URL with a concise verification result. Stop at an open PR, not a merge.

**Done when:** the remote contains the intended commits and an open PR targets the selected base, with its URL confirmed by the hosting platform.
