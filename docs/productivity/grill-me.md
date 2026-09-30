Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=grill-me
```

```bash
npx skills update grill-me
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/grill-me)

## What it does

`grill-me` runs a relentless interview about a plan or design, walking every branch of the decision tree until you and the agent reach a **shared understanding**.

It asks in **frontier-based rounds** and waits after each round. Every question in a round is independent: if one answer is needed before another question makes sense, that question waits for the next frontier. Where a fact can be found in the environment, the agent looks it up instead of asking you. Each question comes with a recommended answer, so you are reacting to a proposal rather than staring at a blank prompt.

## When to reach for it

You invoke this by typing `/grill-me` — the agent won't reach for it on its own.

Reach for it before you build, when a plan feels roughly right but you can sense unresolved decisions hiding in it — the moment you want the soft spots found and forced into the open. If you want that same interrogation to also leave a paper trail of ADRs and a glossary behind, use [grill-with-docs](https://aihero.dev/skills-grill-with-docs) instead. And if the effort is too big to hold in one session and the route to the goal is still foggy — a greenfield project, a huge feature build — start further upstream with [wayfinder](https://aihero.dev/skills-wayfinder), which charts it as a map of decisions first and then merges back into this flow.

## The decision tree

The session walks the plan as a tree of decisions, resolving dependencies between them one by one — a parent decision settled before the choices that hang off it. The point is not to reach agreement quickly; it is to make every implicit call explicit, so nothing important is left silently assumed. You come out the other side with a plan whose branches have all been visited.

`grill-me` is **stateless**: it writes nothing and leaves no workspace behind. It runs anywhere, and the only artifact is the sharpened understanding in the conversation itself. That is the deliberate contrast with [grill-with-docs](https://aihero.dev/skills-grill-with-docs), which captures the same interview as durable ADRs and a glossary.

## Common questions

**How many questions should I expect, and how do I know when it ends?**
Count rounds, not questions. Forty-six questions across four rounds is an ordinary session. It ends when the frontier is empty: every branch visited, nothing left silently assumed.

**It asked me two hundred questions. What went wrong?**
Usually the scope was too large. Ask the agent to break the work into smaller pieces first, then grill each one. Very long sessions also drift into the **[dumb zone](https://www.aihero.dev/ai-coding-dictionary/smart-zone)**, where the [context window](https://www.aihero.dev/ai-coding-dictionary/context-window) is full enough that the questions get worse.

**Can I go back to one question at a time?**
Yes. Add this to your global `CLAUDE.md`:

```
When grilling, ask one question at a time.
```

**What if I genuinely don't know the answer?**
Say so. "I don't know" is a real answer, and a question you can't answer is usually a sign to prototype rather than to guess.

**Do I start a fresh session before writing the spec?**
No. The value of the session is the [context](https://www.aihero.dev/ai-coding-dictionary/context) you just built. Hand the same conversation straight to [to-spec](https://aihero.dev/skills-to-spec).

**Does the model matter?**
More than for most skills. Grilling leans on the [model](https://www.aihero.dev/ai-coding-dictionary/model)'s own sense of how systems break, so give it your best one. Implementation mostly follows context and tolerates a cheaper model.

## Where it fits

`grill-me` is a reach-for-it-anytime standalone — the pre-build stress test you run whenever a plan needs hardening. It is the stateless, user-invoked front door to the [grilling](https://aihero.dev/skills-grilling) primitive; its closest neighbour is [grill-with-docs](https://aihero.dev/skills-grill-with-docs), the stateful sibling that runs the same interview but additionally records the decisions as ADRs and a glossary. If the outcome is a spec you want written down, hand off to [to-spec](https://aihero.dev/skills-to-spec), which synthesises the settled understanding into a spec without re-interviewing you. When you're unsure which flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
