Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=recall
```

```bash
npx skills update recall
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/recall)

## What it does

`recall` reconstructs the **current state** of recent work from past chats and project records. It checks whether the branch, PR, or issue still says what the old conversation said.

## When to reach for it

You invoke this by typing `/recall`; it does not run on its own. Use it when you remember the topic but not which attempts landed or what remained open.

## Common questions

**Will it search every conversation?** No. It defaults to the active workspace and the past seven days. Name another period or workspace if needed. If history is inaccessible, the brief names the gap.

**Does it resume the work?** No. It gives you one suggested next move and stops.

## Where it fits

Use it before picking up a topic across sessions. [Ketchup](https://aihero.dev/skills-ketchup) covers this chat; [handoff](https://aihero.dev/skills-handoff) packages context you already have. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) helps choose.
