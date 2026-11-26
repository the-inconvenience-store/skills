Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=technical-writing
```

```bash
npx skills update technical-writing
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/technical-writing)

## What it does

`technical-writing` structures engineering documents around one **reader job**: learn, do, look up, or understand. It chooses what the reader needs before it polishes sentences.

## When to reach for it

Type `/technical-writing`, or the agent reaches for it when drafting or reviewing human-facing engineering docs. Use it when a README buries setup, a guide combines too many tasks, or a design explanation never names the tradeoff.

## Common questions

**Does it replace my existing doc template?** No. A repo template can combine modes. The skill uses the intended reader job to organize each section within that template.

**Is this for skill instructions or PR bodies?** Use [writing-for-agents](https://aihero.dev/skills-writing-for-agents) for instructions an agent follows and [pr](https://aihero.dev/skills-pr) for a reviewer's briefing. Technical writing focuses on documents people use beyond the review.

## Where it fits

Use it whenever an engineering document needs structure. It calls [unslop](https://aihero.dev/skills-unslop) once for the final copy pass, after the structure and evidence are in place. [Ask Inconvenient](https://aihero.dev/skills-ask-inconvenient) helps choose the writing route.
