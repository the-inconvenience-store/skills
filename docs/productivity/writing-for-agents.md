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

## Common questions

**Where did `/writing-great-skills` go?**
It is this skill, renamed in v1.1. Practitioners were already pointing it at `AGENTS.md`, docs, specs, tickets and runtime prompts long before the name caught up; structure, leading words and pruning turn out to be the craft of any text an agent reads. There is no alias. Reinstall under the new name.

**"Writing for agents": so the agent does the writing?**
The other way round. You are the author; the agent is the reader. That is the whole difficulty of the genre: you are writing for a reader who has already read everything, so explanation is waste and precision is the entire job.

**Can't I just ask the agent to write it for me?**
You can, and it will produce something verbose. Left alone the model explains what it already knows, and it will not apply the no-op test or reach for a leading word on its own. Use the reference on the draft: a review pass is where most of its value lands.

**I asked an agent to trim a document and it cut the functionality.**
Agents told to "streamline" optimise for length, because length is the thing they can see. The no-op test is behavioural, not aesthetic: delete the line and ask whether the agent's behaviour changed. When a sentence fails, delete the whole sentence rather than trim words from it, and settle a disagreement about it by running the document, not by arguing.

**How do I know when it's done?**
When it works, and you can no longer find duplication, sediment or no-ops. There is no automated eval here; the check is a manual run plus the failure-mode vocabulary as a diagnostic. When a document misbehaves, that vocabulary is also the repair kit: name the failure mode first, then fix that.

**Should this live in `CLAUDE.md` or somewhere else?**
Ask which load you want to pay. `CLAUDE.md` loads into every [session](https://www.aihero.dev/ai-coding-dictionary/session) unconditionally; material behind a pointer costs only the pointer's own line until it fires. Anything that applies in one context out of ten is paying context load the nine other times.

**Do I need to rewrite my documents for each new model?**
Mostly no, and over-fitting to one model is its own trap. Updating for a new model is usually another no-op pass rather than a rewrite.

**My skill only works on the exact task I built it from.**
The common route (do the work once, then have the agent write it up as a skill) over-indexes on that one run, and the exemplars come out too specific. Keep the run as evidence, then abstract deliberately: strip what belonged to that repo and those files, and write for the class of task.

**English isn't my first language. Do I lose the leading-word advantage?**
No. Finding the word that packs the most behaviour into the fewest [tokens](https://www.aihero.dev/ai-coding-dictionary/token) is work the reference does for you. It is one of the things it is for.

## Where it fits

`writing-for-agents` is a model-invoked reference that sits underneath every agent-facing document in the repository. Its nearest neighbour is [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient), because the router manages the cognitive load created by user-invoked skills while this reference explains that trade.
