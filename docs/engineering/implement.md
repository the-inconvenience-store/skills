Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=implement
```

```bash
npx skills update implement
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/implement)

## What it does

`implement` builds the work described in a spec or set of tickets. Before editing, it proactively scans the full engineering-principle trigger index against the work and reads every matched leaf; you do not need to name principles. It then drives implementation through test-driven development and automated checks, reviews the result, and proves the changed behavior through its real user or consumer surface.

It does **not** decide what to build. The spec is already settled and the seams are already agreed; `implement` executes that plan rather than reopening it. Principles guide implementation decisions below that contract, and an `INCONCLUSIVE` verification result is reported rather than disguised by passing tests.

## When to reach for it

You invoke this by typing `/implement` — the agent won't reach for it on its own.

Reach for it once the work is written down as a spec or split into tickets and you're ready to turn that into code. If the spec doesn't exist yet, write it first — for that, use [to-spec](https://aihero.dev/skills-to-spec), or [to-tickets](https://aihero.dev/skills-to-tickets) to break a spec into tickets. If you just want to build something test-first without a full spec, drop to [tdd](https://aihero.dev/skills-tdd) directly.

## Pre-agreed seams

The idea `implement` runs on is the **seam** — the stable interface a feature is tested at, chosen before any code is written. It doesn't invent seams mid-build; it uses the ones already picked (during [to-spec](https://aihero.dev/skills-to-spec)) and writes tests against them via [tdd](https://aihero.dev/skills-tdd). Working at pre-agreed seams is what keeps the implementation honest: the tests target something durable, so the code underneath can move without the tests moving.

Around that core it keeps the loop tight: typecheck often, run narrow test files as it goes, and run the whole suite once the implementation is coherent. It then runs separate Standards and Spec review agents, addresses accepted findings, and calls [verification](https://aihero.dev/skills-verification) against the final state.

The work is committed before that review runs, not after. [code-review](https://aihero.dev/skills-code-review) reads `git diff <fixed-point>...HEAD`, which cannot see staged or working-tree changes, so reviewing an uncommitted implementation reviews an empty diff and reports nothing wrong with it.

## Common questions

**It finished, but my ticket is still open and the acceptance criteria are still unchecked.**

Half-fixed here. Upstream, `implement` ends at the commit and never touches the work item at all. This version writes `closes #ISSUENUM` into the commit footer when GitHub is the configured tracker, so GitHub closes the issue when the commit lands on the default branch — which is what unblocks the next ticket, since `to-tickets` defines the frontier as tickets whose blockers are all closed. Three gaps remain: the footer does nothing on a branch that has not merged yet, other trackers have no equivalent, and nothing ticks the `- [ ]` acceptance boxes on the issue. Reconcile the criteria yourself.

It does act on `code-review`'s output, unlike upstream: accepted Standards and Spec findings get addressed, the affected checks rerun, and those edits are committed too.

**Can I point it at all my tickets at once, or run several in parallel?**

Not with `/implement`: one invocation, one ticket. For a whole spec in one run, use [implement-spec](https://aihero.dev/skills-implement-spec), which fans the tickets out to [subagents](https://www.aihero.dev/ai-coding-dictionary/subagent), each in its own worktree, across the ready frontier, and merges them onto one integration branch. Running several `/implement` sessions side by side in one checkout is worse than unsupported: one field report describes a `git commit --amend` in one session landing on another session's commit, a stash vanishing from `refs/stash`, and commits landing on the wrong branch, all in a single afternoon across three issues. The sessions share one working directory, one index, and one HEAD. Git worktrees are the community workaround, and note that `refs/stash` is shared across worktrees too, so worktrees alone do not fix the stash case.

**Can it open a pull request instead of committing?**

Not built in. It commits straight to the current branch, which several people find too eager: the code lands before they have had a chance to verify it works. There is no configuration flag and no PR mode. People override it in the invocation ("commit to a branch and open a PR") or by editing their local copy of the skill. When the agent does write the PR, [pr](https://aihero.dev/skills-pr) shapes its body.

**`code-review` says it cannot see my changes.**

`code-review` reviews `git diff <fixed-point>...HEAD`, three-dot, which excludes staged and working-tree changes. Upstream, `implement` invokes it before committing, so unless an interim commit already exists there is nothing in that diff and the review comes back empty. This fork closes that: the skill commits the outstanding work first and names the commit you branched from as the fixed point, and says why in the same sentence so the agent doesn't quietly skip it. If you are invoking `code-review` yourself rather than through `implement`, the same rule applies — commit first, then review against the point you branched from.

Separately, some people deliberately do not want the review inside the run at all, because an agent reviewing the code it just wrote is biased toward its own solution. Running [code-review](https://aihero.dev/skills-code-review) in a fresh session against a fixed point is a legitimate alternative, and is the same reason that skill runs its two axes in separate sub-agents.

**One ticket burned 150k tokens. Am I using it wrong?**

Probably the ticket is too big rather than the skill being misused. A run does codebase exploration, a red-green loop per seam, a full suite, and a review, so a non-trivial ticket exceeding 100k [tokens](https://www.aihero.dev/ai-coding-dictionary/token) is normal rather than a sign something broke. The lever is upstream: right-size the tickets in [to-tickets](https://aihero.dev/skills-to-tickets) so each fits one fresh window. If a single ticket keeps blowing out, split it rather than raising the [effort](https://www.aihero.dev/ai-coding-dictionary/effort) level.

**`/implement #2` in a fresh session worked on something completely unrelated.**

The agent resolved `#2` against another numbered list in context, such as a todo file or checklist, rather than the configured tracker. `implement` now fetches a passed reference from the issue tracker and states its title before starting, and asks when the reference is ambiguous. Check that the title matches the ticket you meant; passing the issue URL or `owner/repo#2` removes the ambiguity entirely.

## Where it fits

`implement` is the build and proof step near the end of the main chain:

```txt
grill-with-docs → to-spec → to-tickets → implement
                                          ├─ tdd
                                          ├─ code-review
                                          └─ verification
```

Reach for it after the work has been specced and sequenced, not before. Its key neighbours are [to-tickets](https://aihero.dev/skills-to-tickets), which produces tickets with blocking edges and real-surface proof, and [tdd](https://aihero.dev/skills-tdd), which writes tests at each agreed seam. [engineering-principles](https://aihero.dev/skills-engineering-principles) supplies selective decision rules, [code-review](https://aihero.dev/skills-code-review) challenges the diff, and [verification](https://aihero.dev/skills-verification) proves the result before completion. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
