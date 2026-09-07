Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=implement
```

```bash
npx skills update implement
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/implement)

## What it does

`implement` builds the work described in a spec or set of tickets. Before editing, it proactively scans the full engineering-principle trigger index against the work and reads every matched leaf; you do not need to name principles. It then drives implementation through test-driven development and automated checks, reviews the result, and proves the changed behavior through its real user or consumer surface.

It does **not** decide what to build. The spec is already settled and the seams are already agreed; `implement` executes that plan rather than reopening it. Principles guide implementation decisions below that contract, and an `INCONCLUSIVE` verification result is reported rather than disguised by passing tests.

## When to reach for it

You invoke this by typing `/implement` — the agent won't reach for it on its own.

Reach for it once the work is written down as a spec or split into tickets and you're ready to turn that into code. If the spec doesn't exist yet, write it first — for that, use [to-spec](https://aihero.dev/skills-to-spec), or [to-tickets](https://aihero.dev/skills-to-tickets) to break a spec into tickets. If you just want to build something test-first without a full spec, drop to [tdd](https://aihero.dev/skills-tdd) directly.

## Pre-agreed seams

The idea `implement` runs on is the **seam** — the stable interface a feature is tested at, chosen before any code is written. It doesn't invent seams mid-build; it uses the ones already picked (during [to-spec](https://aihero.dev/skills-to-spec)) and writes tests against them via [tdd](https://aihero.dev/skills-tdd). Working at pre-agreed seams is what keeps the implementation honest: the tests target something durable, so the code underneath can move without the tests moving.

Around that core it keeps the loop tight: typecheck often, run narrow test files as it goes, and run the whole suite once the implementation is coherent. It then runs separate Standards and Spec review agents, addresses accepted findings, and calls [verification](https://aihero.dev/skills-verification) against the final state.

## Where it fits

`implement` is the build and proof step near the end of the main chain:

```txt
grill-with-docs → to-spec → to-tickets → implement
                                          ├─ tdd
                                          ├─ code-review
                                          └─ verification
```

Reach for it after the work has been specced and sequenced, not before. Its key neighbours are [to-tickets](https://aihero.dev/skills-to-tickets), which produces tickets with blocking edges and real-surface proof, and [tdd](https://aihero.dev/skills-tdd), which writes tests at each agreed seam. [engineering-principles](https://aihero.dev/skills-engineering-principles) supplies selective decision rules, [code-review](https://aihero.dev/skills-code-review) challenges the diff, and [verification](https://aihero.dev/skills-verification) proves the result before completion. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
