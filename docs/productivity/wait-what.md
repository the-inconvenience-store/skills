Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wait-what
```

```bash
npx skills update wait-what
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wait-what)

## What it does

`wait-what` tells the agent that its last message did not land and asks for a fresh explanation. The new version adds missing context, uses ASD-STE100 Simplified Technical English, and reuses terms from the relevant `GLOSSARY.md`. In a multi-context repo, it follows `GLOSSARY-MAP.md` to find the right one.

It repairs one message. It does not restart the task or alter the underlying decision.

## When to reach for it

You invoke this by typing `/wait-what` — the agent won't reach for it on its own.

Reach for it the moment you stop following an explanation. Only you know that the message missed, so invocation remains a human decision.

## Common questions

**Why not just type "explain that again"?**

You can, and often the result is the same message with different adjectives. What the skill adds is three specific constraints the plain ask doesn't carry: add the context you were missing rather than restating the conclusion, write in ASD-STE100 Simplified Technical English, and use the project's own terms from `GLOSSARY.md` instead of inventing new ones. Those are what turn a re-pitch into a different explanation rather than a louder one.

**It re-pitched, and then carried on doing what it was doing.**

That is correct behaviour. `wait-what` repairs one message; it does not restart the task, reopen the decision, or undo work. If the explanation lands and you now disagree with the decision underneath it, that is a separate conversation to have next.

**Why doesn't the agent notice on its own that I'm lost?**

Because it can't. The skill is user-invoked deliberately: only you know a message missed, and an agent that guessed would re-explain things you understood perfectly well. The cost is that you have to remember it exists, which is the trade every user-invoked skill makes.

**My repo has no `GLOSSARY.md`. Does it still work?**

Yes, minus the vocabulary half. You get the added context and the simplified English, and the agent falls back on whatever language the conversation has already established. The missing glossary is itself a signal: if the jargon keeps arriving, [grill-with-docs](https://aihero.dev/skills-grill-with-docs) is the upfront cure, because a shared language agreed early is what stops it.

## It's working if

- The re-pitch starts with enough context to recover your place.
- Sentences are short and use the project's existing vocabulary.
- The explanation keeps the original meaning without repeating the original wording.

## Where it fits

`wait-what` is a reach-for-it-anytime standalone that works inside any conversation or skill. It repairs confusion after the fact; [grill-with-docs](https://aihero.dev/skills-grill-with-docs) reduces it upfront by building shared project language. [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you over the full set.
