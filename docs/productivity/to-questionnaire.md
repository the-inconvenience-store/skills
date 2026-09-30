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

## Common questions

**Does it read my grilling session and extract the questions from it?**
Not as a step of its own. The skill has no ingest phase: it asks about the send, then drafts. What makes it work after a grilling session is that you run it in the **same conversation**, so the [session](https://www.aihero.dev/ai-coding-dictionary/session) is already in [context](https://www.aihero.dev/ai-coding-dictionary/context) and the drafting can draw on it. Start it in a fresh session and it knows nothing about the grilling; you'll be re-supplying the topic yourself when you answer "what do you need back?".

**The missing answers don't all live with the same person. Can it split them by recipient?**
No. Step one asks for *the* recipient, singular, and the tone and context of the whole document are pitched at them. If three people hold three parts of the answer, run it three times, once per person. Routing questions by discipline or role inside a single document is a request people have made; it isn't what shipped.

**Are the questions dependent: does it skip sections based on earlier answers?**
No. The dependent-question design was explored and did not ship. The output is a static document: themed groups, most-important-first, every question live. The objection against it is a fair one: a [model](https://www.aihero.dev/ai-coding-dictionary/model) planning more than two or three questions ahead of a real answer plans badly, and a branching document has to plan all of them ahead of every answer.

**What if the recipient doesn't know either?**
The document tells them to say so. "I don't know" and partial answers are asked for explicitly, and a flagged uncertainty is worth more than a guess, because a vague answer and a confidently wrong one look identical once they're back in your context.

**Does it send it anywhere (Slack, an issue tracker, email)?**
No. It writes a Markdown file in the current directory and tells you the path. Delivery is yours: paste it into a [ticket](https://www.aihero.dev/ai-coding-dictionary/ticket), drop it in a Slack thread, attach it to an email, or open it on a shared screen and work through it live. People have wired up all four by hand.

**Isn't this just `/grill-me` in batch mode?**
No, and the distinction is worth holding. `grill-me` already asks in **rounds**: the whole frontier at once, then recomputed from your answers, so the "give me all the questions at once" need is met there. `to-questionnaire` is about a different axis: not how the questions are delivered, but whose head the answers are in. Answering them yourself faster is `grill-me`; getting them out of someone else is this.

**Couldn't I just ask the agent for this without a skill?**
Yes, and plenty of people did before it existed: `OPEN_QUESTIONS.md` files, spreadsheets sent to clients, a "needs more info" ticket per unanswered question. The skill buys you two things: the interview never drifts onto the subject, and the document comes out in a shape a non-technical recipient can actually fill in. If you already have a house format that works, the honest answer is that you don't need this.

## It's working if

- Every fact or decision you said you need is covered by a question.
- The recipient has enough context to answer without knowing the earlier conversation.
- Questions target the recipient's knowledge rather than asking you to guess it.

## Where it fits

`to-questionnaire` is a reach-for-it-anytime standalone used at the boundary of your own knowledge. Answers commonly feed back into [grill-with-docs](https://aihero.dev/skills-grill-with-docs) or [to-spec](https://aihero.dev/skills-to-spec). [ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) places it in the wider map.
