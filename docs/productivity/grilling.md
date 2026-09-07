Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=grilling
```

```bash
npx skills update grilling
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/grilling)

## What it does

`grilling` is the interview that stress-tests a plan or design before you build it. It maps the work as a **design tree**, then asks every currently answerable question at the tree's **frontier**.

Questions arrive in rounds rather than one at a time. Before the first round and whenever an answer exposes a new decision shape, the agent scans the engineering-principle triggers against the current frontier. Experience First keeps product choices aimed at the user's result; Keep Execution Unblocked preserves the division that the agent finds observable facts while you make genuine product decisions. Other matched principles shape recommendations without waiting for you to name them.

## When to reach for it

Type `/grilling`, or the agent reaches for it automatically when a task fits.

Reach for it when a plan still has silent assumptions or dependent decisions. In practice, you will usually enter through [grill-me](https://aihero.dev/skills-grill-me) or [grill-with-docs](https://aihero.dev/skills-grill-with-docs), which add the right wrapper around the same interview.

## Rounds and the frontier

The frontier is the set of questions that can be answered now without guessing at an unsettled prerequisite. The skill asks that whole set in one numbered round, separates each question visually, and gives each a recommended answer. Questions blocked by another answer wait for the next round.

This keeps related work moving without flattening dependencies into a bulk questionnaire. The interview ends when the frontier is empty and every branch has been visited, then waits for you to confirm the shared understanding.

## Where it fits

`grilling` is the interview primitive under the main build chain. [grill-with-docs](https://aihero.dev/skills-grill-with-docs) uses it before [to-spec](https://aihero.dev/skills-to-spec), while [triage](https://aihero.dev/skills-triage), [wayfinder](https://aihero.dev/skills-wayfinder), and [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) use it inside their own flows. Its decision defaults come from [engineering-principles](https://aihero.dev/skills-engineering-principles). When you're unsure which entry point fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
