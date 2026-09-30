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

## Common questions

**Can I go back to one question at a time?**
Yes, and a large part of the audience does. Add this to your global `CLAUDE.md`:

```
When grilling, ask one question at a time.
```

The round-based default is genuinely contested. Practitioners who read slowly, who work in a second language, or who use the sequential format as focus scaffolding all report the one-at-a-time rhythm is better for them, and the opt-out is supported rather than tolerated.

**Where did `/batch-grill-me` go?**
Into this skill. Round-based questioning shipped briefly as a separate skill, then moved into `grilling` itself, so everything built on the primitive (`grill-me`, `grill-with-docs`, `triage`, `wayfinder`) got it at once. There is no `batch-grill-me` to install, and no separate sequential skill either; the `CLAUDE.md` line above is the way back to one-at-a-time.

**Asking a whole round at once must lose the questions my earlier answers would have raised. Doesn't it?**
This is the most common objection to the round design, and the frontier is the answer to it: a round only ever contains questions that do not depend on each other, so no answer in a round can invalidate another question in that round. Answers still reshape everything downstream: the next round is recomputed, not pre-written. What you lose is smaller than "all questions at once" implies, and larger than nothing: see the frontier's limit above.

**It ran out of questions and started building.**
A confirmation gate exists precisely for this: the skill is not finished when the frontier empties, it is finished when you say the understanding is shared. Weaker and faster [models](https://www.aihero.dev/ai-coding-dictionary/model) still break it; this is reported most often on lower-effort or non-frontier models, which collapse "interview until shared understanding" into a couple of questions and an outline. If yours does it, the reliable fix is a line in your own `AGENTS.md` or `CLAUDE.md` telling the agent not to implement without permission.

**It answered its own questions instead of asking me.**
That is a bug in the run, not the intended behaviour, and it was the reason facts and decisions were separated in the skill's text. It shows up most when another skill runs `grilling` inside a resolve-this-ticket frame, where the surrounding task reads as licence to keep moving. The same constraint is why there is no async mode: people have asked for a variant that reads a GitHub issue and posts one consolidated decision memo, and that is a different skill, because a grilling session that nobody answers has produced the agent's opinion rather than yours.

**Can I cap the number of questions?**
No, and a cap is deliberately out of scope. Some plans need three questions and some need fifty; a fixed ceiling either truncates the hard case or feels arbitrary on the easy one. Steering in plain language is the intended control: tell it to wrap up, or stop and accept the plan where it stands. If a session is running very long, the cause is usually that the scope was too big; break the work up and grill the pieces.

**I installed `grill-me` on its own and nothing happens.**
`grill-me` is a one-line skill whose whole body is "run a `/grilling` session", so it needs this skill installed too. The same is true of `grill-with-docs`, which additionally needs [domain-modeling](https://aihero.dev/skills-domain-modeling). Installing the whole set avoids the problem; installing selectively means installing the primitives as well.

**`grill-with-docs` ran, but it never loaded `grilling`.**
A real and unfixed rough edge, reported across [harnesses](https://www.aihero.dev/ai-coding-dictionary/harness) and models: a skill that names another skill does not reliably cause that skill to load, and `grill-with-docs` names two. The tell is a session that asks everything at once with no recommendations attached: that is the model improvising an interview rather than running this one. Asking the agent directly whether it loaded `grilling` and `domain-modeling` usually recovers it.

## Where it fits

`grilling` is the interview primitive under the main build chain. [grill-with-docs](https://aihero.dev/skills-grill-with-docs) uses it before [to-spec](https://aihero.dev/skills-to-spec), while [triage](https://aihero.dev/skills-triage), [wayfinder](https://aihero.dev/skills-wayfinder), and [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) use it inside their own flows. Its decision defaults come from [engineering-principles](https://aihero.dev/skills-engineering-principles). When you're unsure which entry point fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
