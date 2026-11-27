# Pull requests

Choose the pass the user asked for: **review** the diff, **status** an existing PR, or **prepare** a PR or shipping handoff. Run only the requested passes. Keep them read-only: no fixes, replies, thread resolution, check reruns, rebases, or retargeting. The user owns every push, PR creation or update, and merge or queue action.

## Review or status

1. **Pin the diff.** Record the PR URL, base ref and SHA, and full head SHA, or the local base and head if there is no PR. Review that revision, not a moving branch name. If the checked-out code differs, inspect the pinned revision read-only or report that you could not review it. If either SHA changes between evidence and handoff, report the drift and redo affected evidence before drawing conclusions about the new revision.
2. **Read status once, when there is a PR.** For GitHub, run the bundled helper with a finite command deadline in your runner. For another forge, use its read-only view and name any equivalent facts you could not obtain.

   ```bash
   bash <skill-dir>/scripts/pr-status.sh owner/repo 123
   ```

3. **Report conflicts and stale bases first.** If GitHub reports a conflict or outdated base, name the affected branch and base and hand off reconciliation to the user. Note any callers that need reconciling when the patch moves or removes code. Do not turn unknown mergeability into a pass.
4. **Keep evidence separate.** Report failed checks and pending checks by name and link, followed by the approval decision and feedback still open. A failed check is not a diagnosis; use its logs before attributing it to the diff. A pending check or missing approval is a next check for the user, not a reason to poll. For human or automated comments, read [Review feedback](../references/review-feedback.md). For a requested Standards and Spec review, call the Skill tool with `code-review` once the review checkout's `HEAD` matches the pinned head. If it does not match and you cannot reach that revision within scope, report the gap; an analysis of another checkout is not that review.

### What the GitHub helper reports

- `number`, `url`, `state`, `mergedAt`, `isDraft`: PR identity and lifecycle. A queued PR is not merged; report a merge only when GitHub reports `MERGED`.
- `headRefName`, `headRefOid`, `baseRefName`, `baseRefOid`: the observed refs and SHAs for comparison with the pinned diff.
- `mergeable`, `mergeStateStatus`: GitHub's mergeability signals at observation time. `UNKNOWN` is unresolved; `BLOCKED` does not identify the blocker.
- `reviewDecision`: GitHub's aggregate review signal. `REVIEW_REQUIRED`, `CHANGES_REQUESTED`, and `APPROVED` describe different states; empty or null means no aggregate decision reported. This is not a reviewer list or proof that the required people approved the pinned revision.
- `statusCheckRollup`: the visible checks and commit statuses for the latest PR commit in GitHub's response. A `CheckRun` is pending until its `status` is `COMPLETED`. Read its `conclusion`: report `SUCCESS`, `NEUTRAL`, and `SKIPPED` separately, and flag unsuccessful results such as `FAILURE`, `CANCELLED`, `TIMED_OUT`, and `ACTION_REQUIRED`. A legacy `StatusContext` uses `state`: `FAILURE` or `ERROR` is failed, `PENDING` or `EXPECTED` is pending, and `SUCCESS` passed. Report unfamiliar values as unknown. An empty rollup means no checks were returned, not that checks passed.

The helper prints `gh pr view` JSON for one explicit PR (`[host/]owner/repo` and a positive PR number). It does not fetch additional pages, review threads, individual approvals, check logs, required-check rules, or queue or deployment status. Consult the PR and repository policy read-only if any of those matter; otherwise mark them unknown. Exit 0 means the read succeeded, regardless of the PR's state. A nonzero exit means the snapshot is unavailable. No result authorizes a change or a merge.

## Prepare or hand off

1. **Prepare a draft for the user.** Confirm the intended base, head, and scope; keep unrelated changes out of the draft. Use the repository's title convention. For a PR body, call the Skill tool with `pr` and give it the pinned diff, the reason for the change, observed verification, and merge risk. Separate checks you ran from checks still needed.
2. **Hand off shipping evidence.** Distinguish CI and review from independent verification: name who ran the changed behavior, what they observed, and which head and base they tested. Mark missing or stale evidence explicitly. For a stack, report the dependencies and the verified run from its bottom, stopping at the first gap. An upper PR with good evidence still depends on its unverified parent.
3. **Stop at the user decision.** Return the title and body if requested, the PR or branches and SHAs, the separate findings and evidence, and the next action and owner. For publishing from the working branch, recommend `/ship` with the outstanding gates. For a merge, hand the decision to the authorized maintainer.
