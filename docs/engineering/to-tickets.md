Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=to-tickets
```

```bash
npx skills update to-tickets
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/to-tickets)

## What it does

`to-tickets` breaks a plan, spec, or the current conversation into a set of **tickets** — each a tracer-bullet vertical slice — and publishes them to your configured tracker, with every ticket declaring its blockers and its real-surface proof.

Every ticket is a **tracer bullet** — a thin *vertical* slice that cuts through all integration layers end-to-end, never a horizontal slice of one layer. A completed slice is independently demoable, states the public path and observable result that prove it, and is safe to hand to a fresh agent.

## When to reach for it

You invoke this by typing `/to-tickets` — the agent won't reach for it on its own.

Reach for it once you have an agreed plan or a written spec and you want it split into tickets. Point it at the conversation, or pass a spec or issue reference and it fetches the body and comments first. If the change hasn't been written up as a spec yet, produce one first — for that, use [to-spec](https://aihero.dev/skills-to-spec).

## Prerequisites

`to-tickets` publishes into your issue tracker, so [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) must have configured the tracker and its triage label vocabulary for this repo first. On a real tracker it applies the ready-for-agent label as it publishes, and checks the label exists before the first create — on GitHub a missing label fails the create outright and takes the ticket with it.

## One artifact, two readings

The blocking edges are the whole point. They make one set of tickets read two ways, depending on the tracker:

- **Local files** → one file per ticket under `.scratch/<feature>/issues/`, numbered blockers-first, the edges written as text. You work them top-to-bottom, by hand, staying in the loop.
- **A real tracker (GitHub, Linear)** → one issue per ticket, the edges as native blocking links (or sub-issues). Any ticket whose blockers are all done is on the **frontier** and can be grabbed — so several agents can run at once.

Native is the default on a real tracker, and the "Blocked by" body line is only the fallback for trackers that have no such edge. GitHub does have one — `gh issue create --blocked-by`, plus `--parent` for the sub-issue link — and because blockers are published first, their numbers are always known by the time a dependent ticket is created. An edge written as body text on a tracker that supports the real thing is invisible to the frontier query.

The edges live in the ticket regardless of medium; the medium only decides whether anything acts on them in parallel. `to-tickets` produces the artifact — how you run it (sequential by hand, or a parallel fleet) is up to you.

## Vertical slices, not horizontal ones

The whole skill turns on one distinction. A **horizontal** slice ships one layer of the change — all the schema, or all the API — and nothing works until every layer lands. A **vertical** slice, the tracer bullet, ships one narrow path through *every* layer at once, so it can be demoed the moment it's done.

Before slicing, `to-tickets` applies the engineering principles for verifiable sequencing, useful intermediate states, migrations, and shared writes. It looks for prefactoring — "make the change easy, then make the easy change" — and orders that work first. It then quizzes you on the breakdown, blocking edges, proof, and what to merge or split before publishing anything.

## The wide-refactor exception

One shape breaks the tracer-bullet rule: a **wide refactor** — a single mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so one edit breaks thousands of call sites at once and no vertical slice can land green. `to-tickets` slices it as **expand–contract** instead: expand (add the new form beside the old so nothing breaks), migrate (move call sites over in batches sized by blast radius, one ticket per batch, CI green throughout because the old form still exists), then contract (delete the old form once no caller remains). When even the batches can't stay green alone, they share an integration branch that all block a final integrate-and-verify ticket, and green is promised only there.

## Common questions

**It produced twelve tickets for a three-line change.**
Over-decomposition is the most reported friction on this skill, and it is consistent across practitioners: the [model](https://www.aihero.dev/ai-coding-dictionary/model) defaults to atomic units and loses the grouping that would make them meaningful. The quiz step exists for exactly this: ask it to merge, and it will. The deeper answer is that the tickets have a floor: if the whole change fits in one context window, you don't need this skill at all. Go straight to [implement](https://aihero.dev/skills-implement).

**The tickets came out one per layer: all the schema in one, all the API in another.**
This is the failure the vertical-slice rule is written against, and the skill still produces it sometimes. Catch it at the quiz step by asking one question per ticket: what can I demo when this is done? A ticket with no answer is a horizontal slice. Some people add a "demo path" line to each ticket for this reason, and report it nudges the model toward vertical decomposition.

**On GitHub the tickets weren't created as sub-issues of the spec issue.**
Reported upstream across a dozen runs and several models, [most fully in issue #554](https://github.com/mattpocock/skills/issues/554), and worse on Codex than on Claude. This fork names the native commands explicitly, in both the skill and the GitHub tracker template: `gh issue create --parent <n>` at creation, or `gh issue edit <parent> --add-sub-issue <n>` after the fact. Both need `gh` ≥ 2.94, so check `gh --version` first; on an older `gh`, or where sub-issues aren't enabled, the fallback is a task list in the parent body plus `Part of #<map>` at the top of each child.

**"Blocked by" was written into the issue body instead of a real blocking link.**
Same class of problem, [reported upstream in issue #513](https://github.com/mattpocock/skills/issues/513), where the agent went as far as asserting GitHub has no native blocking relationship at all. It does, and this fork's skill and tracker template both say so and give the command: `gh issue create --blocked-by 12,15` at creation, or `gh issue edit <child> --add-blocked-by <n>` later. Because blockers are published first, their numbers are always available at creation time. The body text is the fallback for trackers with no native edge, not the default.

**Where do the local tickets go? The v1.1 notes said a root-level `tickets.md`.**
They did, and that was a bug: a single shared file also raced when parallel agents wrote to it. Local mode now writes one file per ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, in dependency order, matching the layout the local tracker template already described. The `NN` prefix is a real ticket ID, so `/implement 03` works instead of retyping a long title.

**It kept truncating when it tried to read my spec.**
A very large spec can outgrow what a tracker issue serves back cleanly, and there is no local copy to fall back on, so the agent then burns [tool calls](https://www.aihero.dev/ai-coding-dictionary/tool-call) re-fetching chunks and never reaches the end. Don't [clear](https://www.aihero.dev/ai-coding-dictionary/clearing) or [compact](https://www.aihero.dev/ai-coding-dictionary/compaction) between `/to-spec` and `/to-tickets`. Run them in the same context window and the spec never has to be fetched back at all.

**The acceptance criteria graded nothing: some passed before any work was done.**
The template asks for criteria and says nothing about whether they can fail, so this happens. Three shapes recur: a criterion already true at the base commit, a criterion that can only be satisfied by work another ticket owns, and one that restates the request rather than deriving from the artifact. Vertical slicing prevents most of it (a slice that delivers behaviour which didn't exist before is red at the base commit by construction), but the check is worth doing by hand. For each criterion, name the observation that would show it false, and confirm it fails at the commit the implementer starts from.

**The tickets are published. How do I actually run them?**
The skill stops at the artifact, and there is no auto-dispatch mode. Dispatch is manual: look at the board, count the tickets with no open blockers, and open that many agent sessions. One ticket per fresh context, cleared between them. Be aware that [implement](https://aihero.dev/skills-implement) does not reliably close or check off the ticket when it finishes, on GitHub or in local markdown, so the ticket's state is yours to update.

## Where it fits

`to-tickets` is a step in the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

It sits between [to-spec](https://aihero.dev/skills-to-spec), which hands it settled behavior and verification decisions, and [implement](https://aihero.dev/skills-implement), which builds each ticket and runs its stated proof through [verification](https://aihero.dev/skills-verification). [engineering-principles](https://aihero.dev/skills-engineering-principles) decides when work should stay atomic, become a tracer bullet, or use bounded expand-contract. Work the frontier one ticket per fresh context, clearing between them. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
