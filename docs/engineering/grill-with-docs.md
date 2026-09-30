Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=grill-with-docs
```

```bash
npx skills update grill-with-docs
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/grill-with-docs)

## What it does

`grill-with-docs` interviews you relentlessly about a plan or design in frontier-based rounds until you and the agent reach a shared understanding — and it writes the vocabulary and decisions down as you go.

The grilling **leaves a paper trail**. A plain interview sharpens your thinking and then evaporates when the session ends; this one captures each term the moment it's resolved into a `GLOSSARY.md` glossary, and records the hard, one-way decisions as ADRs. The alignment survives the conversation instead of living only in your head.

## When to reach for it

You invoke this by typing `/grill-with-docs` — the agent won't reach for it on its own.

Reach for it at the very start of a change, when the plan is still fuzzy and the domain language isn't settled, and you want to stress-test both before any code exists. If you only want the interview and don't need the artifacts, use [grilling](https://aihero.dev/skills-grilling); if the plan is already clear and you just need to pin down or record terminology, use [domain-modeling](https://aihero.dev/skills-domain-modeling). And if the change is too big to hold in one session and its route is still foggy — a greenfield project, a huge feature build — start upstream with [wayfinder](https://aihero.dev/skills-wayfinder): it charts the effort as a map of decisions, then hands back to this main flow once the way is clear.

## Prerequisites

This skill is stateful — it writes into your repo as it grills. Resolved terms land in a `GLOSSARY.md` glossary at the root (or the relevant context's `GLOSSARY.md` if a `GLOSSARY-MAP.md` marks a multi-context repo), and genuinely hard-to-reverse decisions land as ADRs under `docs/adr/`. Both are created lazily — nothing exists until the first term or decision crystallises — so you don't need to scaffold anything up front, but you do need to be somewhere it's safe to write these files.

## The grill

The engine is a **grill**: a relentless, one-question-at-a-time walk down the decision tree, resolving dependencies between decisions before moving on, with a recommended answer offered for every question. Questions the codebase can answer are answered by reading the codebase, not by asking you.

What makes this variant its own skill is where the answers go. As the grill runs, fuzzy language gets sharpened into canonical terms and written to the glossary inline — not batched at the end. The glossary stays a glossary: pure vocabulary, no implementation details, no spec. ADRs are offered sparingly, only when a decision is hard to reverse, surprising without context, and the result of a real trade-off. Most sessions produce a sharper glossary and few or no ADRs, and that's the intended shape.

## Common questions

**Should I use this or `/wayfinder`?**
Scope decides it. Use this for anything you can settle in one session; use [wayfinder](https://aihero.dev/skills-wayfinder) when the effort is too big to hold in one, and it charts the work as a map of decision [tickets](https://www.aihero.dev/ai-coding-dictionary/ticket) first. Wayfinder is slower and denser, and reaching for it on a well-scoped feature is the common mistake. It does not replace this skill: it can drop into a grilling session for the parts of the map that suit one.

**It ran, but no `GLOSSARY.md` and no ADRs appeared.**
Two known causes. The mundane one: nothing qualified. ADRs need all three gates, and a session about a change with no new vocabulary genuinely has nothing to write. The real bug: when the skill runs inside another orchestration layer (a spec-driven-development wrapper, a multi-agent framework, a rule that invokes it as a step in someone else's pipeline), the file-writing half is reported to silently not happen, while the interview still runs. This is filed and unfixed. If you are in that setup, check the working directory before you trust the session's output.

**It asked everything at once, with no recommendations, and never mentioned `GLOSSARY.md`.**
That is the skill failing to load its two dependencies. Because `SKILL.md` is a one-line delegation, an agent that does not pick up [grilling](https://aihero.dev/skills-grilling) and [domain-modeling](https://aihero.dev/skills-domain-modeling) guesses at what grilling means, and you get an undifferentiated question dump. Partial loading is the more confusing case: `grilling` loads, `domain-modeling` does not, and you get a good interview with no paper trail. It correlates with model and [effort](https://www.aihero.dev/ai-coding-dictionary/effort) level, and it is the most reported problem with this skill. If you suspect it, ask the agent directly which skills it loaded.

**Where did all my other decisions go?**
Into the conversation only. This is the most substantive open complaint about the skill: the glossary is not a spec, most answers do not earn an ADR, and there is no ledger tying each resolved answer through to a spec, a ticket and a test. Precise answers (ordering guarantees, negative requirements, numeric defaults) get softened into weaker prose downstream, and the result can look complete while missing the thing you actually decided. The mitigation available today is to keep the session and feed it straight to [to-spec](https://aihero.dev/skills-to-spec), and to re-read the spec against your own answers rather than assuming it captured them.

**Can I point it at an existing repo that has no docs at all?**
Yes. This is the right skill for a codebase with no ADRs, no domain language and no design principles: invoke it and say "help me document my repo". The community pattern pairs it with [improve-codebase-architecture](https://aihero.dev/skills-improve-codebase-architecture) for building or repairing a `GLOSSARY.md`. Expect to steer it: it will read code and ask you about what it finds, and you are the one who says which of the words already in the codebase are the right ones.

**What should I do when the session ends?**
The skill's closing message tends to be open-ended, which is a known rough edge. In the main flow the answer is [to-spec](https://aihero.dev/skills-to-spec), in the same conversation. If the change is small enough to build immediately, go straight to [implement](https://aihero.dev/skills-implement) instead.

**Why is it called that?**
Nobody is happy with the name. There is an open suggestion to rename it `grill-domain-model`, which describes the behaviour more honestly. Nothing has moved on it. If a rename ever lands, the docs page moves with it and the URL changes.

## It's working if

- It asks one round at a time. Each round contains only independent questions whose prerequisites are settled.
- Terms get written to `GLOSSARY.md` the moment they resolve, in your project's own words.
- It reaches into the codebase to answer its own questions where it can.
- ADRs stay rare — you're not asked to rubber-stamp reversible choices.

## Where it fits

`grill-with-docs` is the opening step of the main build chain:

```txt
grill-with-docs → to-spec → to-tickets → implement → code-review
```

It comes first, before anything is written down as a spec: it produces the shared understanding and settled vocabulary that [to-spec](https://aihero.dev/skills-to-spec) then synthesises into a spec without re-interviewing you. Its close neighbours are [grilling](https://aihero.dev/skills-grilling), the same interview without the docs, and [domain-modeling](https://aihero.dev/skills-domain-modeling), the glossary-and-ADR discipline it drives. When you're unsure which skill or flow fits, [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you.
