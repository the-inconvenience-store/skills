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

Reach for this when there is a diff to judge against a known-good point and you want the two questions — *is it built right?* and *is it the right thing?* — answered independently. It runs at the end of the build loop; for actually writing the code test-first, use [tdd](https://aihero.dev/skills-tdd), and for building a whole spec into code use [implement](https://aihero.dev/skills-implement), which commits its work and then runs its own `/code-review` pass over it.

## Prerequisites

The **Spec** axis needs somewhere to find the originating spec — an issue reference in the commit messages, a path you pass in, or a spec under `docs/`/`specs/`. That issue-tracker wiring comes from [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills); without a spec the Spec axis simply skips and says so. The **Standards** axis always carries a Fowler smell baseline and adds only the [engineering principles](https://aihero.dev/skills-engineering-principles) whose triggers appear in the diff.

## Two axes, never merged

The defining idea is the **two axes**. **Standards** asks whether the diff conforms to how this repo writes code: its documented standards, a fixed Fowler smell baseline, and only the engineering principles triggered by this change. Repository standards override the baselines; smells and principles remain judgment calls rather than hard violations. **Spec** asks the orthogonal question — does the code do what the issue or spec actually asked, without missing requirements or smuggling in scope creep?

They run as parallel sub-agents so neither pollutes the other's context, and the final report presents them under separate `## Standards` and `## Spec` headings with a per-axis summary. Real-surface execution remains the job of [verification](https://aihero.dev/skills-verification), not a third review axis.

Two sub-agents is the whole fan-out. Both briefs forbid the sub-agent from reaching for `/code-review` itself or spawning anything further, because a review agent that can rediscover this skill will start its own pair and the count climbs without a ceiling.

## Common questions

**It collides with Claude Code's own `/code-review`. What do I do?**

This is the most reported problem with the skill, and it is not fixed. Claude Code ships its own `/code-review`, which does something different: it hunts bugs in the diff, where this one checks spec compliance and repo standards. Installing this library means one of them wins, and which one wins depends on how you installed. Via the plugin marketplace, everything is aliased under an `inconvenient-skills:` prefix and the built-in becomes hard to reach at the unqualified name; via a plain skills install, the local file wins and this skill shadows the built-in. One clean answer is to remove Claude Code's built-in skills entirely: a large [context](https://www.aihero.dev/ai-coding-dictionary/context) saving, and the collision stops mattering. The shadowing itself is arguably a Claude Code [harness](https://www.aihero.dev/ai-coding-dictionary/harness) bug (a skill author should be free to name a skill anything), so the other answer is to rename the local copy. Editing the frontmatter or renaming the directory gets undone by `npx skills update`; the durable workaround reported by users is to fork the skill to a new name and drop `code-review` from the managed set, keeping a note of the commit you forked from so you can re-sync by hand.

**Its sub-agents keep invoking `/code-review` again and spawn more agents.**

An upstream bug that this fork closed. The original failure was that the Standards and Spec prompts did not forbid delegation, so a sub-agent could rediscover the skill and fan out again — one report reached 50-plus agents. Both sub-agent briefs here end with the guard: perform this review yourself, do not call the Skill tool with `code-review`, and do not spawn further agents. The skill also states up front that exactly two sub-agents run and neither delegates further. That is instruction-level rather than structural, so if you run this unattended it is still worth watching the agent count. Handling it at the harness level, so every skill inherits the guard, is the sturdier option if your harness offers one.

**Should I run it in the same [session](https://www.aihero.dev/ai-coding-dictionary/session) that wrote the code?**

Prefer a fresh one. As one reader put it: "Same context reviewing itself isn't review, it's confirmation bias with a slash command." The reviewing agent in the authoring session holds every assumption that shaped the code, which is exactly the context an independent reviewer would not have. This is also why people ask for [implement](https://aihero.dev/skills-implement) without its built-in review step: it runs the review inside the session that just wrote the diff. Invoking `/code-review` yourself from a clean session is the honest version.

**After every ticket, or once at the end?**

Both work, and the skill does not decide for you. Per-ticket keeps each diff small enough that the Spec axis has one clear spec to check against, which is the mode `implement` uses. Batching to the end of a branch catches interactions between tickets that the per-ticket passes each miss. If you are unsure, review per ticket and run one final pass against the branch point.

**Can I trust the findings?**

Not without checking. Sub-agent output is a hypothesis, not evidence: one team reported a dozen breaking changes that prose-based reviews had waved through. The skill aggregates the two reports verbatim or lightly cleaned rather than re-verifying each claim against the files, so a finding can cite the wrong location or overstate an impact. Read the citation on each finding before acting on it. That every finding is required to carry one (a standards rule, a smell plus its hunk, or a spec line) is what makes this checkable at all.

**Why does it find new problems every single time I run it?**

Because fixes create new surface, and because the judgement-call half of the Standards axis is not deterministic between runs. One reader described the loop plainly: "/code-review and /improve-code-architecture always find new stuff every time. I implement fixes, rerun these skills, and again and again." There is no convergence guarantee. Treat a pass as a list of leads, act on the ones with a cited rule behind them, and stop: do not run it in a loop until it comes back clean, because it will not.

**Does it review my uncommitted work?**

No. It diffs `<fixed-point>...HEAD`, three-dot, which is measured from the merge-base and excludes staged and working-tree changes. If `implement` has not made an interim commit, the work about to be committed is invisible to the review. Commit first, then review, then amend or add a fixup.

## It's working if

- It pins and confirms the fixed point first (`git rev-parse`), failing fast on a bad ref or empty diff rather than inside the sub-agents.
- Standards and Spec findings arrive in two distinct blocks, each citing its source — a repo standard or baseline smell for one, a quoted spec line for the other.
- When no spec can be found, the Spec axis reports "no spec available" instead of inventing requirements.
- Exactly two sub-agents appear in the trace. A climbing agent count means a sub-agent re-entered the skill.

## Where it fits

`code-review` is the review step at the tail of the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

Its closest neighbour is [implement](https://aihero.dev/skills-implement), which drives the build, calls this review, addresses accepted findings, and then invokes [verification](https://aihero.dev/skills-verification) against the final state. Upstream, [to-spec](https://aihero.dev/skills-to-spec) and [to-tickets](https://aihero.dev/skills-to-tickets) provide the behavior and proof it judges. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
