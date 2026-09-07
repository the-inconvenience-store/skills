Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=code-review
```

```bash
npx skills update code-review
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/code-review)

## What it does

`code-review` reviews the diff between `HEAD` and a fixed point you supply — a commit, branch, tag, or merge-base — along two separate axes: **Standards** (does the code follow this repo's documented conventions?) and **Spec** (does it implement what the originating issue or spec asked for?). It runs each axis as its own parallel sub-agent and reports them side by side. It never merges or re-ranks the two sets of findings — keeping them separate is the whole point, because a change can pass one axis and fail the other, and a single blended verdict lets one mask the other.

## When to reach for it

Type `/code-review`, or the agent reaches for it automatically when you ask to review a branch, a PR, work-in-progress changes, or anything "since X".

Reach for this when there is a diff to judge against a known-good point and you want the two questions — *is it built right?* and *is it the right thing?* — answered independently. It runs at the end of the build loop; for actually writing the code test-first, use [tdd](https://aihero.dev/skills-tdd), and for building a whole spec into code use [implement](https://aihero.dev/skills-implement), which runs its own `/code-review` pass before committing.

## Prerequisites

The **Spec** axis needs somewhere to find the originating spec — an issue reference in the commit messages, a path you pass in, or a spec under `docs/`/`specs/`. That issue-tracker wiring comes from [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills); without a spec the Spec axis simply skips and says so. The **Standards** axis always carries a Fowler smell baseline and adds only the [engineering principles](https://aihero.dev/skills-engineering-principles) whose triggers appear in the diff.

## Two axes, never merged

The defining idea is the **two axes**. **Standards** asks whether the diff conforms to how this repo writes code: its documented standards, a fixed Fowler smell baseline, and only the engineering principles triggered by this change. Repository standards override the baselines; smells and principles remain judgment calls rather than hard violations. **Spec** asks the orthogonal question — does the code do what the issue or spec actually asked, without missing requirements or smuggling in scope creep?

They run as parallel sub-agents so neither pollutes the other's context, and the final report presents them under separate `## Standards` and `## Spec` headings with a per-axis summary. Real-surface execution remains the job of [verification](https://aihero.dev/skills-verification), not a third review axis.

## It's working if

- It pins and confirms the fixed point first (`git rev-parse`), failing fast on a bad ref or empty diff rather than inside the sub-agents.
- Standards and Spec findings arrive in two distinct blocks, each citing its source — a repo standard or baseline smell for one, a quoted spec line for the other.
- When no spec can be found, the Spec axis reports "no spec available" instead of inventing requirements.

## Where it fits

`code-review` is the review step at the tail of the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

Its closest neighbour is [implement](https://aihero.dev/skills-implement), which drives the build, calls this review, addresses accepted findings, and then invokes [verification](https://aihero.dev/skills-verification) against the final state. Upstream, [to-spec](https://aihero.dev/skills-to-spec) and [to-tickets](https://aihero.dev/skills-to-tickets) provide the behavior and proof it judges. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
