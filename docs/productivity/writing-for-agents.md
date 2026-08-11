Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=writing-for-agents
```

```bash
npx skills update writing-for-agents
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/writing-for-agents)

## What it does

`writing-for-agents` is the reference for documents an agent consumes: skills, `AGENTS.md`, `CLAUDE.md`, specs, runtime prompts, and pointed-at reference files. The packaging changes, but the writing levers do not.

It was previously called `writing-great-skills`. The broader name reflects its actual scope. Skill-only mechanics such as frontmatter, invocation mode, and routers now live in a linked `SKILL-MECHANICS.md`, loaded only when the document being edited is a skill.

## When to reach for it

Type `/writing-for-agents`, or the agent reaches for it automatically when you create or edit a skill, `AGENTS.md`, or `CLAUDE.md`.

Reach for it when an agent-facing document fires unreliably, repeats environment facts that can go stale, buries its steps, or has grown too large to scan. It gives those problems a shared vocabulary and a set of editing tests.

## Context pointers and the two loads

A **context pointer** names material outside the current context and says when to load it. A skill description is a pointer; so is a line in `AGENTS.md` that sends an agent to another file. The wording decides whether the material is reached reliably.

Every pointer and document spends one of two budgets. Always-loaded material costs **context load**. Material the human must remember costs **cognitive load**. Progressive disclosure moves branch-specific reference behind a pointer while keeping steps and must-read rules in view.

## Completion criteria and pruning

Every step needs a checkable completion criterion with enough demand to force the required legwork. Vague criteria invite premature completion. The pruning test is equally concrete: keep one source of truth, remove stale sediment, and delete any sentence that does not change agent behavior from the default.

The environment is a source of truth too. A document that restates an easy lookup from a config file or command is a cache that can drift; keep the reason or unwritten convention, and let the agent inspect the environment for the fact.

## Where it fits

`writing-for-agents` is a model-invoked reference that sits underneath every agent-facing document in the repository. Its nearest neighbour is [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient), because the router manages the cognitive load created by user-invoked skills while this reference explains that trade.
