Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=engineering-principles
```

```bash
npx skills update engineering-principles
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/engineering-principles)

## What it does

`engineering-principles` gives engineering workflows a shared vocabulary for recurring decisions: subtract before adding, model behavior structurally, keep retries idempotent, isolate parallel writers, and prove the real result.

It is selective rather than a 21-item checklist. The agent proactively scans every trigger against the current decision, loads only the matched leaves, and turns each into a concrete constraint, design choice, or proof obligation. You may name a principle for extra emphasis, but selection does not depend on you doing so.

## When to reach for it

Type `/engineering-principles`, or the agent reaches for it automatically while implementing, refactoring, reviewing, debugging, verifying, migrating, or dividing parallel work.

Name a principle directly when you want to steer a decision: “use Subtract Before You Add,” “apply Boundary Discipline,” or “Prove It Works.” The name acts as a **leading word** that pulls in the full rule without making you repeat it. For module and seam vocabulary, use [codebase-design](https://aihero.dev/skills-codebase-design); for the project's domain language, use [domain-modeling](https://aihero.dev/skills-domain-modeling).

## Defaults below evidence

The principles sit below explicit product decisions, the accepted spec, repository standards, ADRs, and runtime evidence. They fill judgment gaps; they do not overturn recorded intent.

This matters when useful principles pull in different directions. A one-wave API migration is simpler, but an independently deployed consumer may require bounded expand-contract. The skill preserves agreed behavior and a working feedback loop, then prefers the smaller reversible step.

## Twenty-one leading words

The index covers five families:

- **Shape:** Laziness Protocol, Foundational Thinking, Redesign from First Principles, Subtract Before You Add, Minimize Reader Load, Outcome-Oriented Execution, Experience First, Exhaust the Design Space, and Build the Lever.
- **Architecture:** Model Behavior Structurally, Boundary Discipline, Type System Discipline, Make Operations Idempotent, Migrate Callers Then Delete Legacy APIs, and Separate Before Serializing Shared State.
- **Verification:** Prove It Works, Fix Root Causes, and Sequence Verifiable Units.
- **Collaboration:** Guard the Context Window and Keep Execution Unblocked.
- **Learning:** Encode Lessons in Structure.

Two names are deliberately adapted to this workflow. **Model Behavior Structurally** leaves domain language to `domain-modeling`. **Keep Execution Unblocked** preserves the split that facts belong to the agent while product decisions belong to you.

## It's working if

- Relevant principles change visible engineering decisions without waiting for you to name them.
- Only principles relevant to the current decision are loaded.
- Existing specs, ADRs, and evidence remain authoritative.
- Conditional rules state their boundary, such as atomic migration versus bounded expand-contract.
- Reports name a principle only when it resolved a conflict or drove a non-obvious choice.

## Where it fits

`engineering-principles` is a **model-invoked vocabulary layer** beneath the engineering flow. [to-spec](https://aihero.dev/skills-to-spec), [to-tickets](https://aihero.dev/skills-to-tickets), [implement](https://aihero.dev/skills-implement), [diagnosing-bugs](https://aihero.dev/skills-diagnosing-bugs), [codebase-design](https://aihero.dev/skills-codebase-design), and [code-review](https://aihero.dev/skills-code-review) reach for the relevant principles at their own decision points. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
