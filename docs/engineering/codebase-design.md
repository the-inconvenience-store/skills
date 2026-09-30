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

## Common questions

**How do I actually build a deep module in TypeScript?**

This is the most-asked question about the skill and the skill does not answer it. It defines what a deep module *is*; it says nothing about how to stop a stray import from reaching past the interface. [Issue #458](https://github.com/mattpocock/skills/issues/458) put it plainly: "let's say we're happy with the interface, it hides the details, etc. But how do we enforce it? I think without linting or clear guardrails, humans and LLMs alike will start making it messy over time." The upstream maintainer's answer, in that thread, was three options: wrap it in a class or IIFE and accept that the class gets enormous; make it a package in a monorepo and accept the monorepo tooling; or use a linter like [dependency-cruiser](https://github.com/sverweij/dependency-cruiser) to forbid imports that bypass the interface, with Effect named as the best mechanism and dependency-cruiser the second-best. A `setup-ts-deep-modules` draft that wires dependency-cruiser to exactly that shape (entry points at a package root, everything in a subfolder private) sits in this repo's `in-progress/` directory. Drafts there don't ship in the plugin and have no docs page, so you would be copying it in by hand.

**I pointed a session at it and it burned 100k [tokens](https://www.aihero.dev/ai-coding-dictionary/token) redesigning things I never asked about.**

Known, and filed as [issue #449](https://github.com/mattpocock/skills/issues/449). The skill is model-invoked and describes itself as vocabulary, but nothing in it hard-stops an agent from treating it as a runnable process. Told to "resume in /codebase-design and drive the open decisions", an agent reached for the most action-shaped content it could find: the parallel sub-agents in `DESIGN-IT-TWICE.md`. It re-explored code a previous session had already mapped, and ran a long way before asking anything. None of the guardrails a driver skill has (checkpoints, one question at a time, no auto-advance) are present here, because a reference has none. The workaround is to name a driver skill and let this one sit underneath it: `/grill-with-docs`, `/improve-codebase-architecture` or `/tdd` with `codebase-design` as the vocabulary. The issue is open.

**Where did `design-an-interface` go? And is there an `/interface-design` skill?**

`design-an-interface` was removed and absorbed into this skill. Nothing was lost: its "design it twice" technique (parallel sub-agents generating radically different designs, from Ousterhout) ships here as `DESIGN-IT-TWICE.md`. Separately, several people have asked for a dedicated `/interface-design` skill for the deep-module/thin-interface philosophy; that philosophy already lives here, and no separate skill is planned. If you came looking for either name, this is the page.

**Isn't this a file-structure convention, such as folders, barrel files, feature slices?**

No, and the skill has held that line under repeated pushback. [Issue #95](https://github.com/mattpocock/skills/issues/95) proposed a formalised fractal-tree file structure as the concrete implementation of deep modules; the reply was that the two are orthogonal: "deep modules are about the design of the interface and accessing through a strict interface, no matter what the file system looks like. It seems perfectly possible that you could have shallow modules with this approach." The same came up in #458: "I think you might be tying the concept of modules too closely to the file system. The file system can certainly be a useful hint to the shape of modules, but there's no need to use the file system in the construction of deep modules." The glossary defines **module** as scale-agnostic on purpose.

**Does `tdd` actually use this vocabulary?**

It does now. For a long time it did not. The inline deep-module notes that used to live inside `tdd` were removed in v1.0 in favour of this shared skill, but the pointer replacing them was never added, so `tdd` defined "seam" for itself and referenced nothing. The gap is closed: the pointer is now in the skill, reached when the shape of the interface is the open question rather than the tests. `tdd` still owns "seam" as the boundary you *test* at; this skill owns the module shape behind it.

**Does the design-it-twice pattern work outside Claude Code?**

Not cleanly. `DESIGN-IT-TWICE.md` says "spawn 3+ sub-agents in parallel using the Agent tool", which is Claude Code's [tool](https://www.aihero.dev/ai-coding-dictionary/tool) by Claude Code's name. The repo ships metadata for other [harnesses](https://www.aihero.dev/ai-coding-dictionary/harness), including Codex, and those may expose nothing under that name, so the parallel-design phase is less portable than the skill's metadata suggests. Tracked in [issue #564](https://github.com/mattpocock/skills/issues/564), open.

**Can I add my own concepts to the glossary, such as connascence, module secrets, [progressive disclosure](https://www.aihero.dev/ai-coding-dictionary/progressive-disclosure)?**

People have proposed exactly those. [Issue #180](https://github.com/mattpocock/skills/issues/180) adds Parnas's module secrets and Page-Jones's connascence as a naming layer for *what* is leaking across a seam, with a working diff attached; [issue #303](https://github.com/mattpocock/skills/issues/303) proposes progressive disclosure inside the implementation, so a module that is deep at its public interface isn't one undifferentiated slab underneath. Both are open and unmerged. The glossary as shipped is deliberately small, and the reason it stays small is stated in the skill itself: consistent language is the whole point, and a term nobody uses consistently is worse than no term.

## Where it fits

`codebase-design` is a **reach-for-it-anytime standalone** — the shared vocabulary layer under the engineering skills. Its closest neighbour is [domain-modeling](https://aihero.dev/skills-domain-modeling), the parallel vocabulary skill for the problem domain rather than the module structure. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
