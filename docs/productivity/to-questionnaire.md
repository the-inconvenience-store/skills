Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=to-questionnaire
```

```bash
npx skills update to-questionnaire
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/to-questionnaire)

## What it does

`to-questionnaire` turns a decision you cannot settle alone into a Markdown questionnaire for the person who holds the missing knowledge.

It **grills the send, not the subject**. The skill asks you who will receive the questionnaire and what you need back, then aims the document at the gap between that person's knowledge and your decision.

## When to reach for it

You invoke this by typing `/to-questionnaire` — the agent won't reach for it on its own.

Reach for it when planning stalls on facts or decisions that live in someone else's head. If you can answer the questions yourself and want the agent to pressure-test those answers, use [grill-me](https://aihero.dev/skills-grill-me) instead.

## The artifact

The result is `to-questionnaire-<slug>.md` in the current directory. It explains the purpose and context, asks the most important questions first, keeps each question to one idea, and leaves an answer stub beneath it. The questionnaire works asynchronously or as the agenda for a meeting.

## It's working if

- Every fact or decision you said you need is covered by a question.
- The recipient has enough context to answer without knowing the earlier conversation.
- Questions target the recipient's knowledge rather than asking you to guess it.

## Where it fits

`to-questionnaire` is a reach-for-it-anytime standalone used at the boundary of your own knowledge. Answers commonly feed back into [grill-with-docs](https://aihero.dev/skills-grill-with-docs) or [to-spec](https://aihero.dev/skills-to-spec). [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) places it in the wider map.
