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

The agent captures a reference baseline before editing production code, then compares the running implementation against that baseline and corrects in-scope differences. It follows existing application contracts rather than treating every detail in a mockup as authorization for new backend features.

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

Comparisons pair the same screen, state, viewport, and content. A first pass across the requested screens identifies corrections before broad validation. The agent batches fixes and refreshes only affected captures, preserving successful evidence until a relevant change invalidates it. In-scope differences still require correction or your explicit acceptance.

## A visual loop, not a release framework

Project instructions own testing, review, commits, and deployment. `parity` adds no mandatory principle scan, TDD orchestration, or separate verification-skill phase. Unless project policy says otherwise, affected checks run during corrections and broad checks run once the UI is visually coherent.

Missing backend capabilities, unrelated bugs, and infrastructure failures are reported separately. They do not automatically expand the task. A failure that prevents observing a requested screen leaves that screen blocked, not falsely verified.

## Common questions

**Is this tied to Claude Design exports?**

No. Claude Design folders and ZIPs are one input path. Screenshots, other runnable exports, design-tool files, and live pages can also supply the reference. A screenshot proves only the visible state; hidden behavior and unsupplied responsive layouts are not treated as observed facts.

**What if the design conflicts with the project's components?**

The agent first reuses or appropriately extends existing components. If a design-system constraint prevents a match, it names the conflict and asks for a decision rather than quietly sacrificing fidelity or creating a parallel component system.

**How is this different from `/implement` or the upstream `/match`?**

`implement` starts from settled behavior and test seams. `parity` supplies the visual inspection, implementation, and correction loop. Use it directly for design reproduction; when you explicitly combine it with `implement`, the enclosing workflow runs engineering gates once. It is inspired by [match](https://github.com/raphaelsalaja/skills/tree/main/skills/match), with handling for export folders, source-plus-render inspection, and project component reuse.

**Does it promise pixel-perfect results everywhere?**

Only inspected viewports and states can support a parity claim. Screenshot-derived measurements remain estimates, and inferred responsive behavior is identified separately. The report includes paired captures, accepted deviations, and any missing observations.

**Will it implement backend functionality implied by the mockup?**

Only when explicitly in scope. It identifies missing capabilities early and continues independent visual work while a decision is pending. Approving one feature does not approve every other feature later discovered in the references.

**Does every fix restart verification?**

No. Only affected captures, interactions, and checks become stale. Final proof closes remaining gaps instead of repeating successful work. Unrelated findings are reported separately rather than absorbed into an unbounded repair cycle.

## It's working if

- The agent inspects the references and captures the baseline before production edits.
- Implementation captures are paired with the reference at matching sizes and states.
- Visible discrepancies cause fixes and fresh comparisons.
- The final report includes comparison evidence and real-surface behavior verification.

## Where it fits

`parity` is a standalone visual implementation loop that can also supplement an explicitly invoked [implement](https://aihero.dev/skills-implement) workflow without duplicating its engineering gates. For the wider map, use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
