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

`to-tickets` publishes into your issue tracker, so [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) must have configured the tracker and its triage label vocabulary for this repo first. On a real tracker it applies the ready-for-agent label as it publishes.

## One artifact, two readings

The blocking edges are the whole point. They make one set of tickets read two ways, depending on the tracker:

- **Local files** → one file per ticket under `.scratch/<feature>/issues/`, numbered blockers-first, the edges written as text. You work them top-to-bottom, by hand, staying in the loop.
- **A real tracker (GitHub, Linear)** → one issue per ticket, the edges as native blocking links (or sub-issues). Any ticket whose blockers are all done is on the **frontier** and can be grabbed — so several agents can run at once.

The edges live in the ticket regardless of medium; the medium only decides whether anything acts on them in parallel. `to-tickets` produces the artifact — how you run it (sequential by hand, or a parallel fleet) is up to you.

## Vertical slices, not horizontal ones

The whole skill turns on one distinction. A **horizontal** slice ships one layer of the change — all the schema, or all the API — and nothing works until every layer lands. A **vertical** slice, the tracer bullet, ships one narrow path through *every* layer at once, so it can be demoed the moment it's done.

Before slicing, `to-tickets` applies the engineering principles for verifiable sequencing, useful intermediate states, migrations, and shared writes. It looks for prefactoring — "make the change easy, then make the easy change" — and orders that work first. It then quizzes you on the breakdown, blocking edges, proof, and what to merge or split before publishing anything.

## The wide-refactor exception

One shape breaks the tracer-bullet rule: a **wide refactor** — a single mechanical change (rename a column, retype a shared symbol) whose **blast radius** fans across the whole codebase, so one edit breaks thousands of call sites at once and no vertical slice can land green. `to-tickets` slices it as **expand–contract** instead: expand (add the new form beside the old so nothing breaks), migrate (move call sites over in batches sized by blast radius, one ticket per batch, CI green throughout because the old form still exists), then contract (delete the old form once no caller remains). When even the batches can't stay green alone, they share an integration branch that all block a final integrate-and-verify ticket, and green is promised only there.

## Where it fits

`to-tickets` is a step in the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

It sits between [to-spec](https://aihero.dev/skills-to-spec), which hands it settled behavior and verification decisions, and [implement](https://aihero.dev/skills-implement), which builds each ticket and runs its stated proof through [verification](https://aihero.dev/skills-verification). [engineering-principles](https://aihero.dev/skills-engineering-principles) decides when work should stay atomic, become a tracer bullet, or use bounded expand-contract. Work the frontier one ticket per fresh context, clearing between them. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
