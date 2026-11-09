Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=triage
```

```bash
npx skills update triage
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/triage)

## What it does

`triage` moves issues on your project's tracker through a small **state machine** of triage roles: categorise them, verify the claim, grill them into shape if needed, and leave a ready-for-agent brief.

It *recommends and waits*: it tells you its category and state call with reasoning, then acts only on your direction. The normal evaluation verifies a bug or PR before writing an agent brief; an explicit state override skips that investigation. Raw incoming reports belong here, not tickets that [to-tickets](https://aihero.dev/skills-to-tickets) already made agent-ready.

## When to reach for it

You invoke this by typing `/triage` and describing what you want in natural language; the agent won't reach for it on its own. "Show me anything that needs my attention", "let's look at #42", "move #42 to ready-for-agent".

| What you have | Reach for |
| --- | --- |
| Raw incoming reports to evaluate | `/triage` |
| A rough idea of your own | [grill-with-docs](https://aihero.dev/skills-grill-with-docs) |
| A settled conversation to publish | [to-spec](https://aihero.dev/skills-to-spec) |
| A spec to split into agent-ready work | [to-tickets](https://aihero.dev/skills-to-tickets) |
| A confirmed bug needing root-cause investigation | [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) |

## Prerequisites

`triage` reads and writes your issue tracker, so [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills) must have configured the tracker and label mapping first. The roles below are **canonical**; the mapping supplies your tracker's actual label strings. A mapping does not itself create labels, so `triage` confirms they exist before its first label write and offers to create any missing ones. On GitHub, a missing label fails the write rather than creating the label.

External PR discovery is off by default in the GitHub and GitLab templates. To include it, enable the request-surface flag in `docs/agents/issue-tracker.md`; setup does not ask about that flag.

## The state machine

Every triaged item carries exactly one category (`bug` or `enhancement`) and one state:

| State | Means |
| --- | --- |
| `needs-triage` | Needs maintainer evaluation; the usual first state for an unlabeled issue |
| `needs-info` | Waiting on the reporter; returns to evaluation when they reply |
| `ready-for-agent` | Fully specified for an agent, normally with a brief attached |
| `ready-for-human` | A brief plus the reason human implementation is needed |
| `wontfix` | Closed with the reason recorded |

A conflicting pair of states is a reason to stop and ask, not choose one silently. A maintainer can also request a direct state override; the skill confirms the action and asks whether a missing agent brief should be written.

## A PR is an issue with attached code

Where the tracker treats external pull requests as a request surface, `triage` runs them through the same machine. `ready-for-agent` means an agent should take the next step on the diff; `ready-for-human` means it is ready for a human to merge. The brief describes what remains to do to the existing code, not how to rebuild it from nothing. Discovery surfaces only external PRs, but an explicitly named PR is always triaged regardless of author.

## Verify before you brief

The step that separates `triage` from ad-hoc labelling is verification. It reproduces the bug from the reporter's steps, or checks out the PR and runs the tests, and reports back: confirmed with a code path, failed, or insufficient detail (which is itself a strong `needs-info` signal). It also runs two codebase checks: **redundancy** (is this already implemented? then it's a `wontfix`) and **prior rejection** (does `.out-of-scope/` already say no?). A confirmed verification makes a far stronger agent brief; guessing does not.

The **agent brief** is the durable contract for later work; the original report remains context. It names interfaces, types, signatures, desired behavior, acceptance criteria, and scope boundaries, not file paths or line numbers that can go stale while the issue waits.

Closing as `wontfix` has three distinct outcomes:

| Reason | What is preserved |
| --- | --- |
| Already implemented | A comment pointing to the existing behavior, not a rejection record |
| Rejected bug | A polite explanation |
| Rejected enhancement | A `.out-of-scope/` record linked from the closing comment |

The rejection knowledge base has one Markdown file per **concept**, not per issue. It groups prior requests with the reason, so "night theme" can surface an old "dark mode" decision. The maintainer confirms whether that rejection still applies; a similar request is not automatically rejected.

## Common questions

**I ran `/to-spec` and `/to-tickets`, and now those tickets are sitting there untriaged. Do I run `/triage` over them?**
No. They are already agent-ready, because `to-tickets` applies the `ready-for-agent` label as it publishes, precisely so an AFK runner picks them up without another pass. The user who hit this had run the spec flow, seen `needs-triage` on the output, and found their AFK runner ignoring everything. `triage` is the on-ramp for work that arrives from outside; the spec flow is the lane for work you originate. They meet at `ready-for-agent`, not before.

**Is `triage` still relevant now that there's a `to-spec` → `to-tickets` → `implement` flow?**
Only if you have inbound work. `triage` predates that spine and does a different job: it is the lane for reports other people filed. If everything in your tracker came out of your own planning, you will rarely open it. If you maintain anything public, or your team files bugs at you, it is the front door. The main use is open-source repos taking issues from external contributors.

**The agent tried to apply `ready-for-agent` and `gh` said the label doesn't exist.**
An upstream bug ([#616](https://github.com/mattpocock/skills/issues/616)) that this fork closed. The failure mode is nasty, which is why: GitHub rejects `gh issue create --label <missing>` outright rather than creating the label, so a missing label loses the whole issue, not just the label. [bootstrap-skills](https://aihero.dev/skills-bootstrap-skills) now checks the agreed strings against `gh label list` and creates the missing ones with `gh label create --force`, and `triage` confirms the strings exist before its first label write of a session rather than firing blind. If you set the repo up before that landed, re-run `/bootstrap-skills`, or create the five state labels and two category labels once by hand.

**Five states aren't enough: what about blocked, or deferred, or implemented?**
This is the most-filed gap on the skill, in three shapes. An issue that is fully specified but waiting on another issue to close ([#139](https://github.com/mattpocock/skills/issues/139)), where the reporter's complaint was that `ready-for-agent` is "technically true" there but misleading, so an agent picks it up and hits a wall. Trigger-gated future work that is intended but not actionable yet ([#297](https://github.com/mattpocock/skills/issues/297)). And a terminal state for "implemented, awaiting verification", without which an AFK runner can re-queue finished tickets. The upstream maintainer has agreed the blocked case is real and is undecided on the name (`blocked` versus `paused`). None of it has shipped here either. The workaround people use is a repo-local extra label alongside the category, which keeps the canonical state slot occupied by something honest at the cost of the skill not knowing about it. One community derivative goes further, adding `needs-slicing`, `tracking` and effort labels. That works, but it is theirs, not the skill's.

**How is this different from `/diagnosing-bugs`?**
The verification step here is deliberately shallow (enough to answer "is this real, and roughly where does it live"), not to find a root cause. When a bug won't reproduce from the reporter's steps in a few minutes, the honest move is `needs-info`, or [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) if you want to chase it now. Neither skill's text currently mentions the other; a user found that seam, and it is still open.

**Can I point it at my whole backlog and let it run?**
You can ask, but watch what it reads. The "show what needs attention" pass is a cheap listing meant for *selection*, where you pick one, and then it gathers full [context](https://www.aihero.dev/ai-coding-dictionary/context) on the one you picked. Run it across twenty issues at once and an agent can quietly fall back to that cheap listing as its evidence base, which returns issue bodies but not comments. A user hit exactly this: three issues already carried a comment saying "already fixed, recommend closing", and all three got fresh agent briefs instead. If you want a bulk pass, say explicitly that comments must be read per issue.

**Does it work with Linear, or anything other than GitHub Issues?**
Yes, the tracker is config, not a hard-coded assumption, and people run it against Linear (via the `linear` CLI), GitLab, and plain markdown files under `.scratch/`. A common split is Linear for issues and planning, GitHub for code and PRs: skills that say "issue tracker" map to Linear, skills that say "PR" map to GitHub. On the local-markdown tracker there is an open template bug where the generated file can carry the acceptance criteria twice, once at the top level and once inside the agent brief ([#200](https://github.com/mattpocock/skills/issues/200)).

## It's working if

- Every item it touches ends with exactly one category role and one state role, never zero, and never two conflicting states.
- It hands you a recommendation with reasoning and waits, rather than relabelling on its own.
- During normal evaluation, it reports the bug reproduction or PR check before promoting the item; a direct override is clearly identified.
- Every comment it posts to the tracker opens with the `> *This was generated by AI during triage.*` disclaimer.
- Briefs describe behavioral contracts without stale file paths or line numbers, and prior rejections are surfaced for your decision.

## Where it fits

`triage` is an **on-ramp** and a periodic maintenance pass for incoming work, not a mandatory step in the idea-to-build chain. Its briefs feed [implement](https://aihero.dev/skills-implement) just as agent-ready tickets from [to-tickets](https://aihero.dev/skills-to-tickets) do. When a request needs sharpening, it runs [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) together, keeping the vocabulary and qualifying decisions in the repo. [to-spec](https://aihero.dev/skills-to-spec) is the neighboring route for work originating in your own conversation. When you're unsure which lane fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
