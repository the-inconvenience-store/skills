Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=parity
```

```bash
npx skills update parity
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/parity)

## What it does

`parity` implements supplied designs in an existing application, using its components and real behavior. It accepts HTML exports, ZIPs, screenshots, design files, and live references, including folders containing several screens and states.

The agent captures a reference baseline before editing production code, then compares the running implementation against that baseline and corrects the differences. Working interactions and passing tests alone do not establish visual parity.

## When to reach for it

You invoke this by typing `/parity`; the agent won't reach for it on its own.

Reach for it when you have a design to reproduce, rather than a visual direction to explore. For an undecided design, use [prototype](https://aihero.dev/skills-prototype). For agreed behavior described by a spec or tickets, use [implement](https://aihero.dev/skills-implement).

For example:

```text
/parity Implement the page editor from ~/Desktop/cOS/pages.
Use the exported HTML and supplied screenshots as the references,
including the phone layout and save/conflict states.
Reuse this project's design-system components.
```

## Prerequisites

Provide an existing project and accessible design references. The agent needs browser or equivalent surface-driving tools to inspect runnable references and the actual application. Runtime or access gaps are reported as unverified, not replaced with a claim based on code inspection.

## A fixed baseline

The baseline makes **parity** checkable. Reading exported code explains its structure and values; rendering it reveals the actual result. When both are available, the skill requires both, as well as opening supplied images.

Comparisons pair the same screen, state, viewport, and content. Differences lead to corrections and new captures, not just a list at the end. The reference stays fixed unless source evidence or your decision changes the target. Any remaining discrepancy requires your acceptance; otherwise that target remains incomplete.

## Common questions

**Is this tied to Claude Design exports?**

No. Claude Design folders and ZIPs are one input path. Screenshots, other runnable exports, design-tool files, and live pages can also supply the reference. A screenshot proves only the visible state; hidden behavior and unsupplied responsive layouts are not treated as observed facts.

**What if the design conflicts with the project's components?**

The agent first reuses or appropriately extends existing components. If a design-system constraint prevents a match, it names the conflict and asks for a decision rather than quietly sacrificing fidelity or creating a parallel component system.

**How is this different from `/implement` or the upstream `/match`?**

`implement` starts from settled behavior and test seams. `parity` starts from visual references and owns the baseline-to-correction loop. It is inspired by [match](https://github.com/raphaelsalaja/skills/tree/main/skills/match), with explicit handling for export folders, source-plus-render inspection, project integration, and correction of remaining differences before completion.

**Does it promise pixel-perfect results everywhere?**

Only inspected viewports and states can support a parity claim. Screenshot-derived measurements remain estimates, and inferred responsive behavior is identified separately. The report includes paired captures, accepted deviations, and any missing observations.

## It's working if

- The agent inspects the references and captures the baseline before production edits.
- Implementation captures are paired with the reference at matching sizes and states.
- Visible discrepancies cause fixes and fresh comparisons.
- The final report includes comparison evidence and real-surface behavior verification.

## Where it fits

`parity` is a standalone design-to-implementation workflow. It uses [engineering-principles](https://aihero.dev/skills-engineering-principles) for implementation decisions and [verify](https://aihero.dev/skills-verify) to prove final behavior. You do not need to invoke `implement` alongside it. For the wider map, use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
