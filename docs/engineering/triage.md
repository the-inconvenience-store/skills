Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=triage
```

```bash
npx skills update triage
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/triage)

## What it does

`triage` moves issues on your project's tracker through a small **state machine** of triage roles — categorise them, verify the claim, grill them into shape if needed, and leave a ready-for-agent brief.

It never labels blind. Every triaged item carries exactly one **category** role (`bug` / `enhancement`) and one **state** role (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`), and it *recommends and waits* — it tells you its category and state call with reasoning, then acts only on your direction. Before anything is promoted to `ready-for-agent`, it verifies the claim first: a bug gets reproduced, a PR gets checked out and run.

## When to reach for it

You invoke this by typing `/triage` and describing what you want in natural language — the agent won't reach for it on its own. "Show me anything that needs my attention", "let's look at #42", "move #42 to ready-for-agent".

Reach for it when your issue tracker has raw, unevaluated reports and you want them sorted, verified, and turned into work an agent or human can pick up. To turn a settled conversation into a fresh spec instead, use [to-spec](https://aihero.dev/skills-to-spec); to split an existing spec into tickets, use [to-tickets](https://aihero.dev/skills-to-tickets). `triage` is the reverse direction — it processes what's *already* landed in the tracker.

## Prerequisites

`triage` reads and writes your issue tracker, so [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) must have configured the tracker and the label mapping first. The role names above are **canonical** — the actual label strings in your tracker may differ, and that mapping is what setup provides. The mapping says what a label is *called*, not that the tracker has it, so `triage` confirms the strings exist before its first label write and offers to create any that don't: on GitHub a missing label fails the write and takes the comment or state change with it. The config also decides whether external PRs count as a request surface, and who counts as external.

## A PR is an issue with attached code

Where the tracker treats external pull requests as a request surface, `triage` runs them through the *same* machine: same category roles, same states, same transitions — the states just read against the diff instead of a report. `ready-for-agent` means a brief is attached and an agent should take the next step on the code; `ready-for-human` means it's ready to merge. Discovery surfaces only external PRs, but an explicitly named PR is always triaged regardless of author.

## Verify before you brief

The step that separates `triage` from ad-hoc labelling is verification. It reproduces the bug from the reporter's steps, or checks out the PR and runs the tests, and reports back: confirmed with a code path, failed, or insufficient detail (which is itself a strong `needs-info` signal). It also runs two codebase checks — **redundancy** (is this already implemented? then it's a `wontfix`) and **prior rejection** (does `.out-of-scope/` already say no?). A confirmed verification makes a far stronger agent brief; guessing does not.

## Common questions

**I ran `/to-spec` and `/to-tickets`, and now those tickets are sitting there untriaged. Do I run `/triage` over them?**
No. They are already agent-ready, because `to-tickets` applies the `ready-for-agent` label as it publishes, precisely so an AFK runner picks them up without another pass. The user who hit this had run the spec flow, seen `needs-triage` on the output, and found their AFK runner ignoring everything. `triage` is the on-ramp for work that arrives from outside; the spec flow is the lane for work you originate. They meet at `ready-for-agent`, not before.

**Is `triage` still relevant now that there's a `to-spec` → `to-tickets` → `implement` flow?**
Only if you have inbound work. `triage` predates that spine and does a different job: it is the lane for reports other people filed. If everything in your tracker came out of your own planning, you will rarely open it. If you maintain anything public, or your team files bugs at you, it is the front door. The main use is open-source repos taking issues from external contributors.

**The agent tried to apply `ready-for-agent` and `gh` said the label doesn't exist.**
An upstream bug ([#616](https://github.com/mattpocock/skills/issues/616)) that this fork closed. The failure mode is nasty, which is why: GitHub rejects `gh issue create --label <missing>` outright rather than creating the label, so a missing label loses the whole issue, not just the label. [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) now checks the agreed strings against `gh label list` and creates the missing ones with `gh label create --force`, and `triage` confirms the strings exist before its first label write of a session rather than firing blind. If you set the repo up before that landed, re-run `/setup-inconvenient-skills`, or create the five state labels and two category labels once by hand.

**Five states aren't enough: what about blocked, or deferred, or implemented?**
This is the most-filed gap on the skill, in three shapes. An issue that is fully specified but waiting on another issue to close ([#139](https://github.com/mattpocock/skills/issues/139)), where the reporter's complaint was that `ready-for-agent` is "technically true" there but misleading, so an agent picks it up and hits a wall. Trigger-gated future work that is intended but not actionable yet ([#297](https://github.com/mattpocock/skills/issues/297)). And a terminal state for "implemented, awaiting verification", without which an AFK runner can re-queue finished tickets. The upstream maintainer has agreed the blocked case is real and is undecided on the name (`blocked` versus `paused`). None of it has shipped here either. The workaround people use is a repo-local extra label alongside the category, which keeps the canonical state slot occupied by something honest at the cost of the skill not knowing about it. One community derivative goes further, adding `needs-slicing`, `tracking` and effort labels. That works, but it is theirs, not the skill's.

**How is this different from `/diagnosing-bugs`?**
The verification step here is deliberately shallow (enough to answer "is this real, and roughly where does it live"), not to find a root cause. When a bug won't reproduce from the reporter's steps in a few minutes, the honest move is `needs-info`, or [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) if you want to chase it now. Neither skill's text currently mentions the other; a user found that seam, and it is still open.

**Can I point it at my whole backlog and let it run?**
You can ask, but watch what it reads. The "show what needs attention" pass is a cheap listing meant for *selection*, where you pick one, and then it gathers full [context](https://www.aihero.dev/ai-coding-dictionary/context) on the one you picked. Run it across twenty issues at once and an agent can quietly fall back to that cheap listing as its evidence base, which returns issue bodies but not comments. A user hit exactly this: three issues already carried a comment saying "already fixed, recommend closing", and all three got fresh agent briefs instead. If you want a bulk pass, say explicitly that comments must be read per issue.

**Does it work with Linear, or anything other than GitHub Issues?**
Yes, the tracker is config, not a hard-coded assumption, and people run it against Linear (via the `linear` CLI), GitLab, and plain markdown files under `.scratch/`. A common split is Linear for issues and planning, GitHub for code and PRs: skills that say "issue tracker" map to Linear, skills that say "PR" map to GitHub. On the local-markdown tracker there is an open template bug where the generated file can carry the acceptance criteria twice, once at the top level and once inside the agent brief ([#200](https://github.com/mattpocock/skills/issues/200)).

## It's working if

- Every item it touches ends with exactly one category role and one state role — never zero, never two conflicting states.
- It hands you a recommendation with reasoning and waits, rather than relabelling on its own.
- Bugs get reproduced and PRs get run before anything reaches `ready-for-agent`.
- Every comment it posts to the tracker opens with the `> *This was generated by AI during triage.*` disclaimer.

## Where it fits

`triage` is the **periodic maintenance** pass over your issue tracker — run it whenever reports pile up, to keep the queue sorted and the `ready-for-agent` column trustworthy. It sits at the front of the tracker, upstream of the build chain: the briefs it writes are what [tdd](https://aihero.dev/skills-tdd) later picks up to implement. When a request needs sharpening it leans on [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) to grill it into shape in frontier-based rounds. Its close neighbour is [to-spec](https://aihero.dev/skills-to-spec), which populates the tracker from a fresh conversation where `triage` processes what's already there. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
