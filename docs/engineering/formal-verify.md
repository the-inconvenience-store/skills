Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=formal-verify
```

```bash
npx skills update formal-verify
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/formal-verify)

## What it does

`formal-verify` checks a named **property**, such as "retries with the same operation ID produce at most one durable write." It can check modeled event orders that tests rarely exercise, or use a verifier that analyzes the implementation itself.

A verdict covers only the target and scope the tool actually checked. A model passing is a result about that model, not proof about the shipped code at the current revision.

## When to reach for it

Type `/formal-verify`, or the agent reaches for it automatically when you ask for formal proof or model checking, or when an existing project formal check applies to the change.

Use it for a specific promise with costly failures that ordinary examples are unlikely to expose. To observe what happens through the shipped UI, CLI, service, or library, use [verify](https://aihero.dev/skills-verify) instead.

## Prerequisites

The selected checker must support the target and scope of the claim. Existing checks can be recorded under `docs/agents/formal-verification/`; without a record, Run uses a direct or scratch check if available. Only Create and Maintain write permanent verification files.

For Go functions and methods, [Gobra](https://github.com/viperproject/gobra) can check whether the implementation satisfies an annotated contract, such as a postcondition that describes the result for every input that meets the preconditions.

## The property stays fixed

Create records a reusable check and proves that a deliberate break makes the named property fail. Run checks the requested property at the revision under review. Maintain compares the check with current source, then repairs drift without rewriting a product bug as intended behavior. A check can be up to date and still correctly report a failure.

## Common questions

**Does a passing TLA+ model prove my implementation is right?**

No. TLC explores the model under its configuration. A source correspondence review can show where the model applies, and a real-code replay can establish whether a reported schedule is possible in the implementation. If the claim is about what the actual code does for every input in a domain, use a code verifier that can analyze that code.

**What if there is no verifier for my code, or the check only covers small inputs?**

Generated-input tests on the implementation can still find bugs, but they are test evidence, not a formal verdict. A formal pass within a bound is useful evidence within that bound. A claim at every size needs evidence that covers every size.

**Do I need a statechart?**

No. A [statechart](https://aihero.dev/skills-statechart) is an optional view of the same checked model and configuration. Ask for one when a failing event sequence is easier to discuss as a path through states. The checker evidence, not the diagram, determines the verdict.

## Where it fits

`formal-verify` is a standalone tool for a specific formal obligation, not a default implementation gate. It complements [verify](https://aihero.dev/skills-verify), which proves behavior by driving the shipped surface. [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you when the kind of evidence you need is unclear.

The Create and Maintain branches adapt pstack's [Create Formal Verification](https://github.com/cursor/plugins/blob/b1fbf4b60ac6813b4583ccc356850dafcf492665/pstack/skills/create-formal-verification-skill/SKILL.md) and [Maintain Formal Verification](https://github.com/cursor/plugins/blob/b1fbf4b60ac6813b4583ccc356850dafcf492665/pstack/skills/maintain-formal-verification-skill/SKILL.md) from revision `b1fbf4b`.
