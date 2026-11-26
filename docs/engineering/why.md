Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=why
```

```bash
npx skills update why
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/why)

## What it does

`why` investigates the rationale for an existing design, historical change, or measured threshold. It treats what the code does as a lead, not as evidence of what its authors intended.

## When to reach for it

Type `/why`, or the agent reaches for it automatically when a task fits. Use it to ask what tradeoff led to a decision, what evidence set a threshold, or what changed in the history of a reproduced regression. Use [how](https://aihero.dev/skills-how) if you want to trace current behavior instead.

## What the record can tell you

A **recorded** reason comes from a cited primary record, such as the PR discussion that explains a decision or measurements that justify a threshold. An **inferred** reason fits the evidence but was not stated. An **unknown** is a question the available record leaves open.

For a recent agent-authored change, `why` also looks for the conversation that led to it. It matches the conversation to the actual edit and distinguishes the user's decision from the agent's proposal.

## Common questions

**What if there is no decision record?**

A commit message, issue, PR discussion, measurement, or relevant agent conversation can still carry the reason. If the history is inaccessible or cannot be linked to the change, the answer makes that gap explicit rather than presenting an inference as intent.

**Can history establish the cause of a bug?**

Finding a candidate change can inform a hypothesis. It does not reproduce the reported behavior or test that hypothesis. Start with [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) when something is failing now.

## Where it fits

`why` is a standalone, read-only historical investigation. [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) can use its findings after reproduction when history might change the next hypothesis. Use [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) to choose a route.
