Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=ask-inconvenient
```

```bash
npx skills update ask-inconvenient
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ask-inconvenient)

## What it does

`ask-inconvenient` is the router over the skills in this repo. You describe the situation you're in; it tells you which skill or flow fits and in what order to run them.

It **does no work itself**. It doesn't grill, write a spec, or fix anything — it only orients. It exists for the user-invoked skills above all: nothing fires those for you, so `ask-inconvenient` is the memory you offload that to. It also maps model-invoked disciplines such as [verification](https://aihero.dev/skills-verification) and the three vocabulary layers: [domain-modeling](https://aihero.dev/skills-domain-modeling), [codebase-design](https://aihero.dev/skills-codebase-design), and [engineering-principles](https://aihero.dev/skills-engineering-principles).

## When to reach for it

You invoke this by typing `/ask-inconvenient` — the agent won't reach for it on its own.

Reach for it whenever you're unsure which skill or flow a situation calls for: you have an idea and don't know where to start, a pile of bug reports and don't know if they're for `/triage`, or two skills that look interchangeable and you can't tell them apart. If you already know the skill you want, skip the router and invoke it directly.

## Flows, not just skills

The idea `ask-inconvenient` gives you to think with is the **flow** — a path *through* the skills rather than a single one. Before the first engineering flow, [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) records repository configuration, invokes [guardrails](https://aihero.dev/skills-guardrails), then creates the project route through [verification](https://aihero.dev/skills-verification). Most feature work then runs along one main flow: grill → spec → tickets → implement through TDD → review → real-surface verification. On-ramps merge bugs, incoming requests, and codebase-health work onto it; standalones remain available when only one discipline is needed.

## Phase boundaries

The router also helps at the boundary between two phases. It works through five choices in order: continue when the next phase needs the current conversation as a primary source; `/clear` when the context is disposable; `/handoff` when the work must travel to another harness, directory, or person; a subagent for tightly scoped AFK work; otherwise `/compact`. The decision belongs at the boundary, not halfway through a phase.

## Where it fits

`ask-inconvenient` is the **router** — the standalone map that sits over the whole set. It is the node every other docs page links back to as [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient), so it never sits *in* a chain; it points *into* every chain. From here you'll most often land on [grill-with-docs](https://aihero.dev/skills-grill-with-docs), the head of the main flow, or [triage](https://aihero.dev/skills-triage), the on-ramp for work you didn't create. It also knows the standalone paths through [to-questionnaire](https://aihero.dev/skills-to-questionnaire), [wizard](https://aihero.dev/skills-wizard), and [wait-what](https://aihero.dev/skills-wait-what). When even the router's own picture is stale, its [Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ask-inconvenient) is the map of record.
