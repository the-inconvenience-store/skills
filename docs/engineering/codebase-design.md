Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=codebase-design
```

```bash
npx skills update codebase-design
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/codebase-design)

## What it does

`codebase-design` gives you a shared, precise vocabulary for designing **deep modules** — a lot of behaviour hidden behind a small interface, placed at a clean seam, testable through that interface.

It is a **language, not a refactoring plan**. When that language is applied to a concrete design, it pulls only the relevant [engineering principles](https://aihero.dev/skills-engineering-principles): foundational data shape, reader load, boundary placement, structural behavior, or competing designs when the choice is expensive to reverse.

## When to reach for it

Type `/codebase-design`, or the agent reaches for it automatically when a task fits.

Reach for it when you're designing or improving a module's interface, hunting for deepening opportunities, deciding where a seam goes, or making code more testable and AI-navigable. Other skills pull it in whenever they need the deep-module vocabulary. If you want to sharpen the project's *domain* terms rather than its module design, use [domain-modeling](https://aihero.dev/skills-domain-modeling) instead; to run a whole architecture pass over an existing codebase, use [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture).

## Deep, not shallow

A module is **deep** when a large amount of behaviour sits behind a small interface, and **shallow** when the interface is nearly as complex as the implementation. Depth is measured as **leverage** — how much a caller (or a test) can exercise per unit of interface they have to learn. Crucially, depth is a property of the *interface*, not the implementation: a deep module can be internally composed of small, swappable parts that just never surface to callers.

Two checks do most of the work. The **deletion test**: imagine deleting the module — if complexity vanishes, it was a pass-through; if it reappears across N callers, it was earning its keep. And **one adapter means a hypothetical seam; two adapters means a real one** — don't cut a seam until something actually varies across it.

## The interface is the test surface

Callers and tests cross the same seam, so a well-placed interface gives tests something durable to aim at while the code underneath moves freely. That's why the vocabulary insists on **seam** (Feathers' term — a place you can change behaviour without editing there) over the overloaded "boundary," and why "interface" here means *every fact a caller must know*: signatures, yes, but also invariants, ordering, error modes, and performance — not just the type-level surface.

## Pulled out on purpose

`codebase-design` is the **single source of truth** for deep-module vocabulary. Other skills point at it rather than restating the words: [tdd](https://aihero.dev/skills-tdd) borrows it to place a seam before writing the test, [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) uses it while restructuring existing code, and [to-spec](https://aihero.dev/skills-to-spec) speaks it when sketching test seams.

[Engineering-principles](https://aihero.dev/skills-engineering-principles) remains a separate decision layer. It says when to minimise reader load, redesign from first principles, or exhaust the design space; `codebase-design` supplies the module, interface, depth, seam, adapter, leverage, and locality terms needed to act on those decisions.

## Where it fits

`codebase-design` is a **reach-for-it-anytime standalone** — the shared vocabulary layer under the engineering skills. Its closest neighbour is [domain-modeling](https://aihero.dev/skills-domain-modeling), the parallel vocabulary skill for the problem domain rather than the module structure. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
