Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=statechart
```

```bash
npx skills update statechart
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/statechart)

## What it does

Statechart turns a TLA+ model of a product flow, protocol, or service into a Mermaid statechart. The arrows come from states and transitions TLC actually explored in the model, not from a diagram sketched by the agent. The agent puts the states and actions into words the reader can judge.

## When to reach for it

Type `/statechart`, or the agent reaches for it automatically when a task calls for a model-based statechart or a visual explanation of a counterexample. Reach for it when someone needs to see what can happen next or how a modeled rule breaks. Use [formal-verify](https://aihero.dev/skills-formal-verify) when the main question is which rules hold for a bounded model, and [verify](https://aihero.dev/skills-verify) when the main question is what the running implementation does.

## Prerequisites

The chart runner needs Node 22.18 to 22.x, Node 23.6 or later, Bun 1.1.5 or later, or Deno 2.0 or later. It needs mise and network access on the first run unless you point it at an existing TLC jar and Java 11 or later. SVG output also needs Node and npm; the renderer is installed in scratch only when needed.

## Show the path, not just the bad state

A counterexample is a sequence of actions, not just a red box. The report names the rule and gives TLC's path to the violation, so the reader can see what actually leads there. If the chart groups model states together, it distinguishes states that break a rule from states that only sometimes break it.

## Common questions

**Do I need a formal-verify run first?** No. Statechart can use an existing TLA+ model and config or help you write them. If formal-verify hands off a model, the chart uses exactly the spec and config it checked.

**Why did I get a report but no full chart?** Above 500 states, the runner draws only counterexample paths. If there are no violations to draw, it produces the report without a Mermaid file.

**Does a counterexample prove the shipped code has a bug?** No. It shows how a rule breaks in that model and configuration. Replay the path against the implementation before calling it a real bug.

## Where it fits

Statechart is a standalone tool for reviewing stateful behavior. It can also present [formal-verify](https://aihero.dev/skills-formal-verify) findings from the same model, while [verify](https://aihero.dev/skills-verify) can supply real-surface evidence when a path needs replay. Browse the full map in [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient).
