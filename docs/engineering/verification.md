Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=verification
```

```bash
npx skills update verification
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/verification)

## What it does

`verification` proves behavior through the **real surface** a user or consumer touches: the running UI, CLI, service, mobile app, or public library interface.

It does not treat compilation, tests, screenshots without actions, or an agent's report as proof of the changed behavior. It drives the public path, observes its result and durable side effects, and returns `VERIFIED`, `NOT VERIFIED`, or `INCONCLUSIVE`.

## When to reach for it

Type `/verification`, or the agent reaches for it automatically when a task needs real-surface evidence.

Reach for it to prove a completed change, to create a repeatable project-local driving route, or to audit existing verification instructions after the application changes. During implementation the agent uses its Run branch; creation and maintenance happen only when that is the requested job.

## Prerequisites

Run mode uses project instructions under `docs/agents/verification/` when they exist. Without them, the skill performs the strongest direct check the repository and available tools support, reports the missing reusable route, and leaves permanent project files untouched.

## Three branches, one contract

**Create** learns how the repository actually launches and exposes its user-facing surfaces, writes portable instructions and feature maps, then proves one mapped feature by following those instructions cold.

**Run** selects the changed behavior, health-checks a known instance, drives the public path, captures the action and result, checks promised side effects, and cleans up what it started without deleting evidence.

**Maintain** compares every mapped feature with source and then drives every feature live. Documentation and owned harness drift are corrected; a product regression is reported rather than rewritten as intended behavior.

All three branches share one project format, so creation and maintenance cannot quietly teach different verification standards.

## Proof, not a proxy

The leading word is **proof**. A valid proof exercises the shipped path and observes what the consumer was promised. A test can preserve that contract and a typecheck can rule out a class of mistakes, but neither establishes that the running surface launches, accepts the interaction, and produces the promised state.

An inconclusive observation stays inconclusive. The skill never rounds it up because nearby checks passed.

## It's working if

- The final report names the public path and the observed result.
- Evidence shows the action as well as the resulting state.
- Promised files, records, messages, or other side effects are checked.
- Failed attempts leave no stale process or scratch state behind.
- Product regressions are reported instead of absorbed into the feature map.

## Where it fits

`verification` is bootstrapped by [setup-inconvenient-skills](https://aihero.dev/skills-setup-inconvenient-skills) after [guardrails](https://aihero.dev/skills-guardrails) establishes the repository's final launch and check commands. It then serves as the real-surface completion gate after [implement](https://aihero.dev/skills-implement) and the reusable driving route that [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs) can use to construct and rerun a bug-specific feedback loop. It complements [tdd](https://aihero.dev/skills-tdd): tests preserve behavior at a seam; verification proves the actual application path. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
