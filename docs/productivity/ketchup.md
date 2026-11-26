Quickstart:

```bash
npx skills add the-inconvenience-store/skills --skill=ketchup
```

```bash
npx skills update ketchup
```

[Source](https://github.com/the-inconvenience-store/skills/tree/main/skills/ketchup)

## What it does

`ketchup` catches you up on what changed in this chat and separates work the agent still owns from calls only you can make.

The recap starts just after the most recent actual human message before `/ketchup`, not after a notification or agent update. The one exception is an unresolved call for you from earlier in the same chat: that stays on the list.

## When to reach for it

You invoke this by typing `/ketchup`; the agent won't reach for it on its own.

Reach for it when you've stepped away and want to know what moved in this chat and what needs you now. For one reply that didn't land, use [wait-what](https://aihero.dev/skills-wait-what). To give another agent a document it can resume from, use [handoff](https://aihero.dev/skills-handoff).

## Your call

“Checks are still running” tells you where things stand. “Choose whether to release with the known limitation” asks you to act. The reply tells you what the choice changes, what the agent recommends and why, and what you risk, without making you open a link to decide.

## Common questions

**Does it finish pending work or post a status update elsewhere?**
No. It reads evidence already available and replies here. A screenshot or diagram appears only if it helps you understand the evidence; it doesn't trigger new work to produce one.

**What if older messages are missing or the latest status can't be checked?**
The agent tells you what's missing and covers what it can see. A last reported status is not a confirmation that the work is still in that state.

## Where it fits

`ketchup` is a standalone check-in for you while you stay in the same chat. [Handoff](https://aihero.dev/skills-handoff) is for when the work needs to travel to another agent. [Ask-inconvenient](https://aihero.dev/skills-ask-inconvenient) maps the full set.
