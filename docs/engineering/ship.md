Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=ship
```

```bash
npx skills update ship
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ship)

## What it does

`ship` takes finished branch work to an open pull request: it rebases onto the fetched `main` or `master`, resolves conflicts, verifies the result, commits remaining work, and pushes. It uses [pr](https://aihero.dev/skills-pr) to shape the body before publishing it.

Shipping stops at a **review-ready** PR, not a merge. The workflow preserves unrelated work and reconciles upstream intent rather than treating conflict resolution as choosing a side.

## When to reach for it

You invoke this by typing `/ship`, and the agent won't reach for it on its own. Use it when your implementation is ready to publish but still needs integration with the base branch. For the PR body alone, use [pr](https://aihero.dev/skills-pr).

## Prerequisites

A Git repository with a reachable `main` or `master`, push access to the working branch's remote, and an authenticated CLI or API for the hosting platform. Install `pr` alongside `ship`.

## Review-ready

Rebasing can change behavior even when Git reports no conflicts. Verification covers the integrated result before publication. A published branch that needs history rewritten gets an explicit force-with-lease tied to the remote commit observed before rebasing, so another contributor's intervening push is not silently overwritten.

Uncommitted work owned by the task is saved and restored across the rebase. Unrelated changes stay untouched; if they prevent a clean rebase, the agent pauses for isolation instead of sweeping them into a stash or commit.

## Common questions

**Does it replace `pr`?**

No. `ship` handles branch integration and publication; `pr` owns the body format and evidence presentation.

**Does it merge the PR?**

No. The endpoint is an open PR with a confirmed URL. An existing open PR for the same head and base is updated rather than duplicated.

**What happens when a conflict needs a decision?**

The agent resolves conflicts whose intended behavior is supported by the code and conversation. It asks when a product decision is missing and keeps the work recoverable. Failed required checks block publication unless you explicitly accept them.

## Where it fits

`ship` is the publication **chain step** after [implement](https://aihero.dev/skills-implement). It delegates the review presentation to [pr](https://aihero.dev/skills-pr). See [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) for the full flow.
