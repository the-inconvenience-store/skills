Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=blast-radius
```

```bash
npx skills update blast-radius
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/blast-radius)

## What it does

`blast-radius` finds where a change could break a downstream consumer, shared state, or durable data. It tests the one **safety assumption** that makes the change safe on the exact source under review, or reports that assumption as unproven.

## When to reach for it

Type `/blast-radius`, or the agent reaches for it automatically when a task fits. Use it when a small-looking diff could have effects that a list of direct callers would miss. Use [code-review](https://aihero.dev/skills-code-review) for conformance to the spec and repo standards, or [verify](https://aihero.dev/skills-verify) to check whether the finished behavior works on its real surface.

## Evidence beyond the diff

A reader of old records might never call the writer you changed. The useful question is whether the reader can still handle records emitted by the new code. A focused run through that boundary can support or contradict the assumption. The report separates confirmed failure paths, cleared paths, and plausible paths that remain unchecked.

## Common questions

**Do I have to commit my changes first?**

No. When using it on its own, tell it whether to include staged or working-tree changes. When called from [code-review](https://aihero.dev/skills-code-review), it keeps the review's pinned revision and diff scope. It does not switch refs or leave edits to the product.

**What if the right version cannot be run safely?**

The assumption is unproven. The report names the missing evidence rather than treating a check on a different revision or a mocked boundary as proof.

## Where it fits

`blast-radius` is a standalone risk check that [code-review](https://aihero.dev/skills-code-review) also uses for material risks. Its evidence stays separate from the review's Spec and Standards findings. Use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) to choose a route.
