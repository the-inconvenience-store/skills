Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=domain-modeling
```

```bash
npx skills update domain-modeling
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/domain-modeling)

## What it does

`domain-modeling` builds and sharpens a project's **ubiquitous language** as you design — challenging fuzzy terms, stress-testing relationships with concrete scenarios, and writing the glossary and decisions down the moment they crystallise.

This is the **active** discipline, not the passive one. Merely reading `GLOSSARY.md` to borrow its vocabulary is a one-line habit any skill can do; this skill is for when you are *changing* the model — coining a canonical term, catching a contradiction between the code and what you just said, recording a hard-to-reverse decision. And it keeps the glossary clean: `GLOSSARY.md` is a glossary and nothing else — no implementation details, no spec, no scratch pad.

## When to reach for it

Type `/domain-modeling`, or the agent reaches for it automatically when a task fits — when codebase terminology is under discussion, when a `GLOSSARY.md` is being written or edited, or when an ADR is being recorded or edited.

Reach for it when the *words* are the problem: two people mean different things by "cancellation", "account" is doing three jobs, or a design conversation keeps snagging on a concept that has never been named precisely. If instead the module's *shape* is the problem — where the seam goes, how deep the interface is — use [codebase-design](https://aihero.dev/skills-codebase-design). If you want the plan itself interrogated before you build, use [grilling](https://aihero.dev/skills-grilling).

## Prerequisites

The skill writes into two places, both created lazily — only once there is something to record. Resolved terms go into `GLOSSARY.md` at the root (or, in a multi-context repo flagged by a `GLOSSARY-MAP.md`, into the per-context `GLOSSARY.md`). Decisions go into `docs/adr/`. Nothing needs to exist up front; the first resolved term creates the glossary, the first real trade-off creates the ADR.

## Glossary vs. ADR

Two artifacts, two different bars:

- **The glossary** (`GLOSSARY.md`) captures language. Every time a vague term is made canonical, it's written down inline — not batched — so the shared vocabulary stays current with the conversation. It stays ruthlessly free of implementation detail.
- **An ADR** captures a decision, and the bar is high: offered only when the choice is **hard to reverse**, **surprising without context**, and **the result of a real trade-off**. Miss any one of the three and there is no ADR. This is what keeps `docs/adr/` a record of consequential forks rather than a diary.

The move that makes it click: when you state how something works, the skill cross-references the code and surfaces the contradiction — "your code cancels entire Orders, but you just said partial cancellation is possible — which is right?" The language and the code are forced to agree.

## Pulled out on purpose

`domain-modeling` is the **single source of truth** for building the project's ubiquitous language, split out as its own model-invoked skill so any other skill can reach it. [grill-with-docs](https://aihero.dev/skills-grill-with-docs) leans on it to record terms and decisions as a grilling session runs, [triage](https://aihero.dev/skills-triage) uses it to keep tickets in the project's own words, and [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) reaches for it while it works.

Keeping it standalone means you can also reach for it directly — as a **reference** for how to sharpen a model — without committing to the steps any of those skills mandate. The language lives in one place, and everything that needs it points there.

## Common questions

**My `GLOSSARY.md` is 500 lines. 1,000. 3,000. What do I do?**
The size is a symptom, not the disease: the file has absorbed implementation detail and decisions that were never glossary material. The fix is a direct instruction: `/grill-with-docs make my GLOSSARY.md more concise and remove any implementation details from it`. Run it against a bloated file and most of it goes. Only reach for a `GLOSSARY-MAP.md` split once the file is genuinely lean and still covers two domains that a reader would not want to hold at once; splitting a bloated file just gives you several bloated files. The skill's guidance here is not yet strong enough to prevent the growth in the first place, and the issue tracking that is still open.

**Why is it `GLOSSARY.md` and not `CONTEXT.md`? It used to be `CONTEXT.md`.**
This was the most-argued naming question in the whole skill set, and it is now settled on `GLOSSARY.md`. The case that won: the file is "a glossary and nothing else", so `GLOSSARY.md` says exactly what it is, and with agents in the loop everything is [context](https://www.aihero.dev/ai-coding-dictionary/context), which makes `CONTEXT.md` the less informative of the two names. The case against it was the map: `CONTEXT-MAP.md` pointing at several `CONTEXT.md` files reads naturally in a way `GLOSSARY-MAP.md` does not, and `context` is the standing DDD word for a bounded area of the model. That cost was accepted. If your repo still has a `CONTEXT.md`, rename it and its map; nothing reads the old name any more.

**Where did `/ubiquitous-language` go?**
It was removed, and it was not deprecated. Its job moved into `domain-modeling`, which maintains the whole model continuously rather than dumping a glossary out of one conversation. Vocabulary enforcement got more load-bearing, not less: it now runs underneath grilling, triage and mapping rather than as a separate pass you remember to do.

**How do I get a glossary for a codebase that has none?**
Ask for it explicitly rather than waiting for it to accumulate. `/grill-with-docs help me scaffold my existing repo with a GLOSSARY.md` is the documented route; expect a long interrogation: one user reported 50+ questions before the file was in shape. Incidental use builds the glossary far too slowly on a brownfield repo.

**Can I keep the domain model and use my own ADR format?**
Not cleanly today. The glossary half and the ADR half ship in one skill, so a team with an established ADR convention (different template, different location, different naming) gets instructions that conflict with its house style. The current options are to copy the skill locally and edit it, or to override the ADR conventions in your repo's own agent docs. Splitting the two apart is [an open request](https://github.com/mattpocock/skills/issues/557).

**Does a glossary actually earn its keep? It is one more artifact to review, and it can go stale.**
Sometimes it does not, and it is worth being honest about where. DDD gets less useful the closer it gets to the implementation: the payoff is upstream, in naming and concept alignment, not in aggregates and layer ceremony. Synonym control matters at naming boundaries: module names, table names, status enums, issue titles, CLI commands. It matters much less in ordinary prose. There is also a live objection that domain terms compress communication *between humans* who already share them, and that an agent responds the same way to the plain-English description. On that reading, the glossary's value is keeping you and your reviewers aligned with what the agent is doing, not making the agent better. On a one-day build, skip it. And an unreviewed, agent-authored glossary is worse than none: it becomes confident-sounding lore that later sessions treat as truth.

**Can it turn my vague prompts into domain language for me?**
No, and there is no plan for a skill that does. A domain language you do not understand yourself becomes meaningless drivel once written down. This skill enforces precision once you have the understanding; it does not manufacture vocabulary you do not have. The related trap is using domain words without doing the modelling: right nouns over the wrong conceptual structure produce output that reads correct and is not.

## Where it fits

`domain-modeling` is a **reach-for-it-anytime standalone** that runs *underneath* other skills as often as at a fixed step. Its closest neighbour is [codebase-design](https://aihero.dev/skills-codebase-design), because a shared language is what lets you name a deep module and its seam precisely; downstream, a settled glossary is exactly what [to-spec](https://aihero.dev/skills-to-spec) synthesises into a spec written in the project's own words. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
