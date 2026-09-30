Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=to-spec
```

```bash
npx skills update to-spec
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/to-spec)

## What it does

`to-spec` turns the current conversation and your codebase understanding into a spec, then publishes it to your issue tracker.

It does **not** interview you again. By the time you reach for it, the alignment work is done — `to-spec` synthesises what is already known rather than asking a fresh round of questions.

## When to reach for it

You invoke this by typing `/to-spec` — the agent won't reach for it on its own.

Reach for it once a change has been talked through and the domain language is settled, and you want that shared understanding written down before any code is written. If you *haven't* aligned yet, grill first — for that, use [grill-with-docs](https://aihero.dev/skills-grill-with-docs). To split the finished spec into tickets, use [to-tickets](https://aihero.dev/skills-to-tickets).

## Prerequisites

`to-spec` publishes into your issue tracker, so [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) must have configured the tracker and triage labels for this repo first. It applies the `ready-for-agent` label itself — no separate triage pass needed.

## What the spec includes

- **Problem statement** — what is broken or missing, and why it's worth solving, in the project's own vocabulary.
- **Solution** — the shape of the fix at a high level, before any implementation detail.
- **User stories** — an extensive, numbered list of the concrete behaviours the change must support, each one independently checkable.
- **Implementation decisions** — the choices already settled during the conversation, sharpened by the engineering principles their triggers select.
- **Testing decisions** — the seams where durable behavior tests will live.
- **Verification** — the real user or consumer path, observable result, durable side effects, and behavior that must remain unchanged.
- **Out-of-scope items** — what this change deliberately does *not* cover, to keep the ticket bounded.
- **Further notes** — anything else worth carrying forward that doesn't fit the sections above.

## Deep modules

Before writing the spec, `to-spec` sketches the **seams** at which the feature will be tested and looks for **deep module** opportunities — a lot of functionality hidden behind a small, stable interface. It prefers existing seams to new ones and the highest seam possible, ideally just one across the whole change.

That matters for agentic development: a good interface gives tests something durable to target, so the code underneath can change without the tests moving.

## Common questions

**Where did `/to-prd` go?**
It is this skill, renamed in v1.1. "Spec" is now the single through-line term, and the old `to-prd` slug is dead; reinstall under the new name. The pair that replaced the old vocabulary is *spec* and *tickets*: the spec is the destination and the decisions that fix it, the [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) are the execution steps that get there. If you pivot, delete the unfinished tickets and keep the spec.

**Why does the spec get the `ready-for-agent` label? I don't want an agent implementing off it.**
The label means "no further triage needed": the document is complete enough for an agent to work from. It is an input designation, not a work order. But if you run [AFK](https://www.aihero.dev/ai-coding-dictionary/afk) agents that poll for `ready-for-agent`, that distinction isn't visible to them, and they will happily try to build the whole spec in one run instead of picking up the ticket slices. This is the most-reported rough edge on the skill. Until it changes, exclude the parent spec explicitly in your AFK agent's prompt, or strip the label once `/to-tickets` has run.

**Why not go straight from grilling to `/to-tickets` and skip the spec?**
Often you should; the spec earns its step only on multi-session work. Where it pays is that the tickets are disposable and the spec isn't: each ticket is sized for one fresh context window and gets deleted or closed, while the spec stays as the one place the reasoning behind them lives. On a single-session change that buys you nothing, and you have paid an extra synthesis step where the [model](https://www.aihero.dev/ai-coding-dictionary/model) can drift. Go grilling → `/implement`.

**I just finished a wayfinder map. What do I feed it?**
The main map issue: `/to-spec #<map_issue>`, not the individual decision tickets. [wayfinder](https://aihero.dev/skills-wayfinder) produces decisions rather than deliverables, scattered across a map; `to-spec` is the step that collapses them into one buildable document. Looping the map straight into `/implement` throws that collapse away.

**Is the spec for me to review, or is it just for the agent?**
Mostly for the agent, and it reads that way: complete, dense, reference-heavy. The parts worth your eyes are the seams and the out-of-scope section, because those are the two places a wrong decision is cheapest to catch and most expensive to discover later. Reading the whole thing end to end is a real complaint people have, and there is no summary mode: the honest answer is that if the spec surprises you, the grilling was too shallow, not the spec too long.

**Do I keep the spec frozen once tickets start, or let the agent rewrite it?**
Nothing keeps it in sync, so in practice it is a snapshot of what you knew at that moment, and it goes stale the first time implementation teaches you something. Treat it as throwaway once the work ships. The artifacts meant to outlive it are your `GLOSSARY.md` and your ADRs; if something learned during implementation deserves to last, it belongs there, not in an edited spec.

**My work is a refactor or a module boundary, not a feature. Does the template fit?**
Less well, and this is a known limitation. The template leans hard on user stories, which is the wrong shape for architectural work: you end up writing stories nobody asked for around decisions that are really about interfaces and invariants. Lean on the implementation-decisions and testing-decisions sections instead, and let the durable architectural calls land as ADRs via [grill-with-docs](https://aihero.dev/skills-grill-with-docs) rather than trying to make the spec carry them.

**Will it check the tracker for related work, or cite the ADRs it's respecting?**
No to both. It reads and respects the ADRs covering the area it touches, but it doesn't link them, and it doesn't search the tracker for overlapping issues before drafting, so a spec can quietly duplicate work someone already filed. Search the tracker yourself first if the area is busy.

**`/to-tickets` couldn't read my spec: it kept truncating.**
Very large specs can outgrow what a tracker issue will serve back cleanly, and there is no local copy to fall back on. The fix is context hygiene: don't [clear](https://www.aihero.dev/ai-coding-dictionary/clearing) or [compact](https://www.aihero.dev/ai-coding-dictionary/compaction) between `/to-spec` and `/to-tickets`. Run them in the same window and the spec never has to be re-fetched at all.

## It's working if

- It starts writing the spec instead of asking you a fresh round of questions.
- It checks the seams with you before writing, and proposes as few as possible.
- The spec comes back in your project's domain vocabulary, not generic boilerplate.
- It names how the completed behavior will be proved through its real surface.

## Where it fits

`to-spec` is a step in the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

Reach for it after the plan and domain language are resolved, and before you break the work into implementation tickets. Its key neighbours are [grill-with-docs](https://aihero.dev/skills-grill-with-docs), which sharpens the context so the spec is precise, and [to-tickets](https://aihero.dev/skills-to-tickets), which turns the spec into tickets carrying an explicit proof for [implement](https://aihero.dev/skills-implement) to build and [verification](https://aihero.dev/skills-verification) to exercise. [engineering-principles](https://aihero.dev/skills-engineering-principles) supplies selective defaults without reopening settled decisions. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
