Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=how
```

```bash
npx skills update how
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/how)

## What it does

`how` explains how a named part of your repository works today or where new work belongs in its existing structure. It stays read-only and grounds the answer in the path the code actually takes, not a redesign or a guess based on directory names.

## When to reach for it

Type `/how`, or the agent reaches for it automatically when a task fits. Use it when you need to follow a request, understand where data or control passes between modules, or decide which existing layer owns a change. To learn why that layer was chosen, use [why](https://aihero.dev/skills-why).

## Follow the handoffs

A useful walkthrough starts somewhere you can open in the editor. It shows the handoffs that matter to the question: where a request becomes a job, who writes the state, or which consumer reads it next. For a placement question, it points to the closest precedent and the module that already owns the responsibility.

## Common questions

**Will it move the code or recommend a redesign?**

No. It can name a location for a proposed change based on today's ownership. The answer does not modify the repository or propose a replacement architecture.

**Can it tell me why the owners put it there?**

Not from the code alone. `how` shows which layer owns the work now. [why](https://aihero.dev/skills-why) looks for the historical reason in records from the decision.

## Where it fits

`how` is a standalone walkthrough you can use before changing unfamiliar code. [blast-radius](https://aihero.dev/skills-blast-radius) is the next question when you have a diff and want to know what could break outside it. Use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) to choose a route.
