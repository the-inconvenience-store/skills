Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=wait-what
```

```bash
npx skills update wait-what
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/wait-what)

## What it does

`wait-what` tells the agent that its last message did not land and asks for a fresh explanation. The new version adds missing context, uses ASD-STE100 Simplified Technical English, and reuses terms from the relevant `CONTEXT.md`. In a multi-context repo, it follows `CONTEXT-MAP.md` to find the right one.

It repairs one message. It does not restart the task or alter the underlying decision.

## When to reach for it

You invoke this by typing `/wait-what` — the agent won't reach for it on its own.

Reach for it the moment you stop following an explanation. Only you know that the message missed, so invocation remains a human decision.

## It's working if

- The re-pitch starts with enough context to recover your place.
- Sentences are short and use the project's existing vocabulary.
- The explanation keeps the original meaning without repeating the original wording.

## Where it fits

`wait-what` is a reach-for-it-anytime standalone that works inside any conversation or skill. It repairs confusion after the fact; [grill-with-docs](https://aihero.dev/skills-grill-with-docs) reduces it upfront by building shared project language. [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) routes you over the full set.
